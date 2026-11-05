---
type: Reference
title: GitHub events a notifier can listen to
description: Webhooks, Actions triggers and the Slack or Teams apps carry GitHub events to other channels; the notifications API itself needs a classic personal token, so an App cannot read anyone's inbox.
tags: [github, webhooks, actions, notifications, bridge]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: gh-hooks, title: "GitHub Docs: Webhook events and payloads", resource: "https://docs.github.com/en/webhooks/webhook-events-and-payloads", accessed: 2026-11-05}
  - {id: gh-actions, title: "GitHub Docs: Events that trigger workflows", resource: "https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows", accessed: 2026-11-05}
  - {id: gh-notif-api, title: "GitHub Docs: REST API endpoints for notifications", resource: "https://docs.github.com/en/rest/activity/notifications", accessed: 2026-11-05}
  - {id: gh-slack, title: "GitHub integration for Slack", resource: "https://github.com/integrations/slack", accessed: 2026-11-05}
  - {id: dsh-deploy, title: "dsh-superagent-prototype: 006 Deployment", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs", file: 006-deployment.md, accessed: 2026-11-05, commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4}
---

# Three ways to see an event

| Mechanism | Fits | Catch |
| --- | --- | --- |
| **Webhook** (repository, organisation or App) | a server that relays events: `issues` (opened, labeled, assigned…), `issue_comment`, `pull_request`, `pull_request_review`[^gh-hooks] | needs a reachable HTTPS endpoint and a secret to verify signatures |
| **Actions workflow** `on: issues: [opened, labeled]`[^gh-actions] | a repo that wants a reaction with no server: comment with a mention, assign, or call a push service | a workflow file per repo; a secret for any outside service |
| **Slack or Teams app** | a channel feed, filtered by event and label[^gh-slack] | a chat tool, not a phone alert; no code |

Board events are thin. `projects_v2_item` exists for organisations and Apps only, not for
repository webhooks.[^gh-hooks] A notifier that wants "a card moved to Needs owner" is
better off listening for the `needs:*` **label** on the issue.

# The notifications API is a person's, not an App's

The inbox endpoints accept only a **classic personal access token**; GitHub App user and
installation tokens and fine-grained tokens do not work.[^gh-notif-api] They are built
for polling with `Last-Modified` and `X-Poll-Interval`; a 304 costs no rate
limit.[^gh-notif-api] This is why dsh-superagent needs its own user account: "A GitHub
App cannot be the agent, because dsh-superagent reads the account's
notifications."[^dsh-deploy]

# What the kit can take from it

- A notifier should listen to **events** (webhook or the server's own writes), never read
  a person's inbox. No classic token, no extra account.
- The trigger the kit already owns is the `needs:*` label plus the ask record. A
  notifier keys on those, so it works whether an agent, a person or a bridge added the
  label.
- A server that writes the ask itself (`item_report` with `attention`) does not need a
  webhook at all: it can notify in the same call.

[^gh-hooks]: GitHub Docs, Webhook events and payloads.
[^gh-actions]: GitHub Docs, Events that trigger workflows.
[^gh-notif-api]: GitHub Docs, REST notifications.
[^gh-slack]: GitHub integration for Slack.
[^dsh-deploy]: dsh-superagent 006 Deployment.
