# Linear → Discord Daily Summary — Setup Guide

Every day at ~8 AM Warsaw time a GitHub Actions workflow fetches all issues
completed in the last 24 hours from Linear and posts a Discord embed to a
channel of your choice.

---

## Prerequisites

- A [Linear](https://linear.app) workspace with at least one team
- A Discord server where you have **Manage Webhooks** permission

---

## Step 1 — Get a Linear API key

1. Open Linear → **Settings** → **API** (or go to `linear.app/settings/api`).
2. Under **Personal API keys**, click **Create key**.
3. Give it a descriptive label (e.g. `github-actions-summary`) and copy the key.
   It starts with `lin_api_…`.

> The key only needs read access. Linear does not offer scoped keys yet,
> so a personal key with your normal workspace access is the right choice.

---

## Step 2 — Create a Discord webhook

1. Open the Discord channel where you want the summary.
2. **Edit Channel** → **Integrations** → **Webhooks** → **New Webhook**.
3. Give it a name (e.g. `Linear Summary`) and optionally set an avatar.
4. Click **Copy Webhook URL** — it looks like
   `https://discord.com/api/webhooks/<id>/<token>`.

---

## Step 3 — Add secrets to the GitHub repository

1. Go to your repository on GitHub.
2. **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.

Add these two secrets:

| Secret name           | Value                       |
| --------------------- | --------------------------- |
| `LINEAR_API_KEY`      | The key from Step 1         |
| `DISCORD_WEBHOOK_URL_LINEAR` | The webhook URL from Step 2 |

Never commit either value to the repository.

---

## How it works

The workflow file is at [`.github/workflows/linear-summary.yml`](../.github/workflows/linear-summary.yml).

It runs the script [`.github/scripts/linear-summary.js`](../.github/scripts/linear-summary.js),
which does the following:

1. Calculates a timestamp for 24 hours ago.
2. Sends the GraphQL query below to `https://api.linear.app/graphql`.
3. Formats the results as a Discord embed and POSTs them to the webhook URL.
4. If no issues were completed, posts a friendly fallback message instead of
   silently doing nothing.

### Linear GraphQL query

```graphql
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
      completedAt
      assignee {
        name
      }
      team {
        name
      }
    }
  }
}
```

`$after` is set to exactly 24 hours before the workflow runs.

---

## Schedule

The cron is set to `0 7 * * *` (7:00 UTC):

- **Winter (UTC+1):** 8:00 AM Warsaw — exact match
- **Summer (UTC+2):** 9:00 AM Warsaw — 1 h later than ideal

This is an acceptable trade-off to avoid running two overlapping cron jobs
during DST transitions. Adjust to `0 6 * * *` (6:00 UTC → 8:00 AM summer)
if the summer offset matters more for your team.

---

## Running manually

Open **Actions** → **Linear Daily Summary** → **Run workflow** on any branch.
Useful for testing after you add the secrets.

---

## Troubleshooting

| Symptom                         | Fix                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `Missing required env vars`     | Check that both secrets are set and spelled correctly                                                                     |
| `Linear API responded with 401` | The `LINEAR_API_KEY` is invalid or expired — regenerate it                                                                |
| `Discord webhook error 404`     | The webhook was deleted — recreate it and update the secret                                                               |
| Workflow never fires            | GitHub can delay scheduled workflows on low-activity repos by up to 1 h; manually trigger once to verify everything works |
