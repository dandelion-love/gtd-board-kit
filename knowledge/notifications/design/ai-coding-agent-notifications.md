---
type: Reference
title: AI coding agent notifications
description: As of late 2026, hosted coding agents tell the human through the place the task came from (a PR review request, a Slack thread reply, a status emoji), and local agents expose hooks for "needs input" and "done"; none offers urgency tiers or digests.
tags: [notifications, ai-agents, copilot, codex, devin, cursor, claude-code, prior-art]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: copilot-review, title: "GitHub Docs: Reviewing a pull request created by Copilot", resource: "https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/review-copilot-prs", accessed: 2026-11-05}
  - {id: codex-slack, title: "OpenAI: Use Codex in Slack", resource: "https://learn.chatgpt.com/docs/third-party/slack", accessed: 2026-11-05}
  - {id: codex-forum, title: "OpenAI Developer Community: Notification when Codex web finishes a task", resource: "https://community.openai.com/t/feature-request-notification-when-codex-web-finishes-a-task", accessed: 2026-11-05}
  - {id: devin-slack, title: "Devin Docs: Slack integration", resource: "https://docs.devin.ai/integrations/slack", accessed: 2026-11-05}
  - {id: cursor-slack, title: "Cursor Docs: Slack integration", resource: "https://cursor.com/docs/integrations/slack", accessed: 2026-11-05}
  - {id: cc-hooks, title: "Claude Code Docs: Hooks guide", resource: "https://code.claude.com/docs/en/hooks-guide", accessed: 2026-11-05}
---

# What it is

A survey of how coding agents that work unattended tell a human they are needed.
Checked against vendor docs in November 2026. Features move fast; re-check before
relying on any detail.

# Who notifies, when, and how

| Agent | Done | Needs input | Channel |
| --- | --- | --- | --- |
| GitHub Copilot coding agent | finishes and **requests review** on its PR[^copilot-review] | iterate by mentioning `@copilot` in a PR comment[^copilot-review] | GitHub's own notifications |
| OpenAI Codex cloud (from Slack) | returns the result to the original thread[^codex-slack] | not documented | Slack thread; optional start message[^codex-slack] |
| Codex web | no completion alert as of September 2026; desktop app and CLI can notify at end of turn[^codex-forum] | desktop shows running, needs input, ready, blocked[^codex-forum] | desktop, terminal |
| Devin | marks runs completed or failed with an emoji[^devin-slack] | asks in the thread; code channels show working, blocked or done[^devin-slack] | Slack thread, DMs |
| Cursor cloud agents | Slack notification with a link to the PR; success or failure emoji[^cursor-slack] | posts a short plan and a running status under the thread[^cursor-slack] | Slack thread or another channel[^cursor-slack] |
| Claude Code (local) | `agent_completed` for background sessions[^cc-hooks] | `permission_prompt` after about 6 s waiting; `idle_prompt` about 60 s after a reply with no typing[^cc-hooks] | user-defined hook command |

# Patterns

- **Reply where asked.** Every hosted agent answers in the thread or PR that started
  the task. Nobody opens a new channel.
- **The deliverable is the notification.** Copilot's review request and Cursor's PR link
  are the "done" message.
- **Status is ambient.** Emoji reactions and status chips show working, blocked, done
  without a new ping.[^devin-slack][^cursor-slack]
- **Local agents wait before pinging.** Claude Code fires only after a prompt has
  waited a few seconds, or after a minute of silence.[^cc-hooks]
- **Users ask for completion alerts.** The Codex web request says users miss finished
  parallel tasks for 15 minutes or more.[^codex-forum]

# Gaps

- No agent documents urgency tiers, quiet hours, digests, or escalation when the human
  does not answer.
- None documents deduplication across many parallel agents talking to one owner.
- Devin and Cursor notification preferences beyond channel choice were not found.

# What the kit can take from it

- Make the PR review request the primary "done" signal. Owners already filter on it.
- Show progress as state on the board (labels, status field), not as messages.
- Ping only for "needs input" and "blocked", after a short grace delay so a fast
  self-recovery sends nothing.
- Fill the gap the vendors leave: one owner, many agents, so tiers, digest and dedupe
  belong in the kit, not in each agent.

[^copilot-review]: GitHub Docs, Reviewing a pull request created by Copilot.
[^codex-slack]: OpenAI, Use Codex in Slack.
[^codex-forum]: OpenAI Developer Community thread, with an OpenAI support reply dated September 2026.
[^devin-slack]: Devin Docs, Slack integration.
[^cursor-slack]: Cursor Docs, Slack integration.
[^cc-hooks]: Claude Code Docs, Hooks guide, Notification matchers.
