---
type: Reference
title: GitHub Projects status move as approval
description: Moving a card between Status columns is the cheapest approval act on GitHub, but anyone with project write can do it and its history is not reliable.
tags: [github, projects, status, conventional]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: gh-projects-access, title: "GitHub Docs: Managing access to your projects", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-access-to-your-projects", accessed: 2026-11-02}
  - {id: gh-projects-auto, title: "GitHub Docs: Using the built-in automations", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations", accessed: 2026-11-02}
  - {id: gh-discussion-status, title: "GitHub Community discussion 209484: Projects status changes missing from issue timelines since 2026-09-24", resource: "https://github.com/orgs/community/discussions", find: "Projects status changes missing from issue timelines (ProjectV2ItemStatusChangedEvent) since 2026-09-24", accessed: 2026-11-02}
  - {id: applab, title: "AppLab backlog plugin README (v1.3.0)", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/README.md", accessed: 2026-11-02, commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6}
---

# What it is

A person drags a card to a column (for example Ready → Todo). Agents read the column and act.
The AppLab plugin's whole approval model is one such move.[^applab]

# What GitHub gives

| Fact | Source |
| --- | --- |
| Roles are Read, Write, Admin for the whole project; no per-field or per-column permission | [^gh-projects-access] |
| Built-in workflows can set Status (item added → Todo; closed or merged → Done) and close issues when Status changes | [^gh-projects-auto] |
| Status changes are recorded as `ProjectV2ItemStatusChangedEvent` / `project_v2_item_status_changed` in the issue timeline, but a public report says most were missing from about 2026-09-24, with no staff reply | [^gh-discussion-status] |

# Assessment

- **Cheap**: one drag, can be done in bulk in a table view.
- **Not enforceable**: an agent with project write can make the same move.[^gh-projects-access]
- **Weak audit**: who moved it may not be recorded, per the report above.[^gh-discussion-status]
- **Not a status of its own**: a merged PR or closed issue moves the card for you, which
  is right for Done, wrong for an approval column.[^gh-projects-auto]

# Make it safer

- Pair the move with a **label** the person adds (`agent-ready`), because label events carry
  their actor in the issue timeline. See [labels](github-labels-as-signals.md).
- Have the agent check, at claim time, that the latest move or label was made by a human
  account, and refuse otherwise.

# Open questions

- Is the timeline regression fixed? Re-test before relying on status history.
- Whether `projects_v2_item` webhooks (which would carry the sender) are available for
  user-owned projects was not confirmed for this page.

[^applab]: AppLab backlog README, `/refine`.
[^gh-projects-access]: GitHub Docs, project roles.
[^gh-projects-auto]: GitHub Docs, built-in workflows.
[^gh-discussion-status]: GitHub Community discussion 209484, closed unanswered 2026-10-04.
