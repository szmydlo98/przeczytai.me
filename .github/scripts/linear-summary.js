#!/usr/bin/env node

const LINEAR_API_KEY = process.env.LINEAR_API_KEY;
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL_LINEAR;

if (!LINEAR_API_KEY || !DISCORD_WEBHOOK_URL) {
  console.error("Missing required env vars: LINEAR_API_KEY, DISCORD_WEBHOOK_URL");
  process.exit(1);
}

const since24h = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();

const QUERY_IN_PROGRESS = `
  query InProgressIssues {
    issues(
      filter: { state: { type: { eq: "started" } } }
      first: 50
      orderBy: updatedAt
    ) {
      nodes {
        identifier
        title
        url
        assignee { name }
        team { name }
      }
    }
  }
`;

// completedAt >= $after guards against returning all ever-completed issues.
const QUERY_COMPLETED = `
  query CompletedIssues($after: DateTime!) {
    issues(
      filter: {
        completedAt: { gte: $after }
        state: { type: { eq: "completed" } }
      }
      first: 50
      orderBy: updatedAt
    ) {
      nodes {
        identifier
        title
        url
        assignee { name }
        team { name }
      }
    }
  }
`;

async function linearFetch(query, variables = {}) {
  const res = await fetch("https://api.linear.app/graphql", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: LINEAR_API_KEY,
    },
    body: JSON.stringify({ query, variables }),
  });

  if (!res.ok) {
    throw new Error(`Linear API responded with ${res.status} ${res.statusText}`);
  }

  const json = await res.json();

  if (json.errors?.length) {
    throw new Error(`Linear GraphQL errors: ${JSON.stringify(json.errors)}`);
  }

  return json.data.issues.nodes;
}

async function postToDiscord(payload) {
  const res = await fetch(DISCORD_WEBHOOK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Discord webhook error ${res.status}: ${body}`);
  }
}

function issueLines(issues) {
  return issues.map((issue) => {
    const assignee = issue.assignee ? ` — ${issue.assignee.name}` : "";
    const team = issue.team ? ` \`${issue.team.name}\`` : "";
    return `**[${issue.identifier}](${issue.url})** ${issue.title}${team}${assignee}`;
  });
}

// Discord embed field values are capped at 1024 chars; trim gracefully.
function truncateToField(lines, emptyText) {
  if (lines.length === 0) return emptyText;

  const parts = [];
  let len = 0;
  for (const line of lines) {
    if (len + line.length + 1 > 1000) {
      parts.push(`…and ${lines.length - parts.length} more`);
      break;
    }
    parts.push(line);
    len += line.length + 1;
  }
  return parts.join("\n");
}

function buildPayload(inProgress, completed) {
  const dateLabel = new Date().toLocaleDateString("en-GB", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "Europe/Warsaw",
  });

  return {
    embeds: [
      {
        title: "📋 Daily Linear Summary",
        color: 0x5865f2,
        fields: [
          {
            name: `🔄 In Progress (${inProgress.length})`,
            value: truncateToField(
              issueLines(inProgress),
              "No issues currently in progress."
            ),
          },
          {
            name: `✅ Completed today (${completed.length})`,
            value: truncateToField(
              issueLines(completed),
              "Nothing completed in the last 24 hours. Keep pushing! 💪"
            ),
          },
        ],
        footer: { text: dateLabel },
        timestamp: new Date().toISOString(),
      },
    ],
  };
}

async function main() {
  const [inProgress, completed] = await Promise.all([
    linearFetch(QUERY_IN_PROGRESS),
    linearFetch(QUERY_COMPLETED, { after: since24h }),
  ]);

  console.log(
    `In progress: ${inProgress.length} | Completed today: ${completed.length}`
  );

  await postToDiscord(buildPayload(inProgress, completed));
  console.log("Posted to Discord.");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
