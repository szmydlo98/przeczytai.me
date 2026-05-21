#!/usr/bin/env node

const LINEAR_API_KEY = process.env.LINEAR_API_KEY;
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL_LINEAR;

if (!LINEAR_API_KEY || !DISCORD_WEBHOOK_URL) {
  console.error("Missing required env vars: LINEAR_API_KEY, DISCORD_WEBHOOK_URL");
  process.exit(1);
}

// Runs Monday 8 AM — "last week" is the preceding 7 days.
const since7d = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

const QUERY_CREATED = `
  query CreatedIssues($after: DateTimeOrDuration!) {
    issues(
      filter: { createdAt: { gte: $after } }
      first: 100
      orderBy: createdAt
    ) {
      nodes {
        identifier
        title
        url
        assignee { name }
        team { name }
        state { name type }
      }
    }
  }
`;

// completedAt >= $after prevents returning all ever-completed issues.
const QUERY_RESOLVED = `
  query ResolvedIssues($after: DateTimeOrDuration!) {
    issues(
      filter: {
        completedAt: { gte: $after }
        state: { type: { eq: "completed" } }
      }
      first: 100
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

function weekRange() {
  const end = new Date();
  const start = new Date(since7d);
  const fmt = (d) =>
    d.toLocaleDateString("en-GB", {
      day: "numeric",
      month: "short",
      timeZone: "Europe/Warsaw",
    });
  return `${fmt(start)} – ${fmt(end)}`;
}

function buildPayload(created, resolved) {
  const range = weekRange();
  const resolvedRate =
    created.length > 0
      ? Math.round((resolved.length / created.length) * 100)
      : null;

  const summaryParts = [
    `**${created.length}** issue${created.length !== 1 ? "s" : ""} created`,
    `**${resolved.length}** resolved`,
  ];
  if (resolvedRate !== null) {
    summaryParts.push(`${resolvedRate}% resolution rate`);
  }

  return {
    embeds: [
      {
        title: `📊 Weekly Linear Summary — ${range}`,
        description: summaryParts.join(" · "),
        color: 0xeb5757,
        fields: [
          {
            name: `🆕 Created (${created.length})`,
            value: truncateToField(
              issueLines(created),
              "No issues created this week."
            ),
          },
          {
            name: `✅ Resolved (${resolved.length})`,
            value: truncateToField(
              issueLines(resolved),
              "No issues resolved this week."
            ),
          },
        ],
        footer: { text: "przeczytai.me · Weekly digest" },
        timestamp: new Date().toISOString(),
      },
    ],
  };
}

async function main() {
  const [created, resolved] = await Promise.all([
    linearFetch(QUERY_CREATED, { after: since7d }),
    linearFetch(QUERY_RESOLVED, { after: since7d }),
  ]);

  console.log(`Created: ${created.length} | Resolved: ${resolved.length}`);

  await postToDiscord(buildPayload(created, resolved));
  console.log("Posted to Discord.");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
