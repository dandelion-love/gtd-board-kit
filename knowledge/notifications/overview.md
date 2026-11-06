---
type: Research Finding
title: Notifying the owner, in one page
description: What GitHub, dsh-superagent, paging and inbox tools, interruption research and 2026 push technology say about when and how a board should reach its one busy owner, and the kit decision that follows.
tags: [notifications, attention, overview]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T05:00:00Z }
---

# The question

A board's owner is one person, often on a phone. Agents ask questions, open pull
requests and capture new issues all day. When should the board reach the owner, how
loud, through what, and with which actions?

# What the research says

| Finding | Pages |
| --- | --- |
| GitHub notifies only on mentions, assignment, review requests, participation and watching. Projects notify nobody; your own actions never notify you; there is no urgency, acknowledgement or quiet time beyond Mobile working hours | [GitHub](/notifications/github/) |
| dsh-superagent allows four reasons to speak (ack once, result, one question, cannot finish), enforced by the host; everything else waits on a pull panel; noise is fixed by subtraction | [When dsh-superagent speaks](/notifications/design/dsh-superagent-when-to-speak.md) |
| Paging and notification platforms converge on: push only the actionable, two urgency tiers, digest the rest, dedupe by key, acknowledge then escalate, quiet hours hold rather than drop, the record stays in the system of record | [Design principles](/notifications/design/notification-design-principles.md) |
| Interruptions cost stress even when output holds; repeats drive alert fatigue (acceptance fell 30% per extra reminder in one encounter); deferring to a breakpoint costs about 90 seconds | [Interruption cost](/notifications/design/interruption-cost-and-breakpoints.md), [Alert fatigue](/notifications/design/alert-fatigue-and-receptivity.md) |
| Hosted coding agents notify through the place the task came from (a review request, a thread reply); none has urgency tiers or digests | [AI coding agents](/notifications/design/ai-coding-agent-notifications.md) |
| Standard Web Push (RFC 8030, 8291, 8292), in the Declarative Web Push shape, is still the one technology that reaches Android, iOS (home-screen web app) and desktop with no vendor account. It cannot break iOS Focus; sockets do not survive on phones | [Push technology choice](/notifications/push-tech/push-tech-choice-2026.md) |
| ntfy is the most reusable existing service (self-hostable, priorities, action buttons, Web Push to browsers); Pushover is the only one with escalation until acknowledged; Apprise reaches many channels from one URL | [Push services compared](/notifications/push-services/push-services-compared.md) |
| Notification buttons work in Chrome, Edge and Firefox, not Safari or iOS web apps; no browser has inline reply. Buttons may only open or defer; anything that answers or approves goes through a signed-in page | [Notification actions](/notifications/push-tech/notification-actions.md) |

# What the kit decided

[Notify a person only when they must act](/decisions/notify-only-when-a-person-must-act.md):
three reasons to push, GitHub's own mention or review request as the push, new issues
wait in views, and an optional louder channel per repo that copies asks with a small,
safe action set.

# Open questions

- The right reminder interval for one owner, and whether a daily digest beats a
  breakpoint (after a merge) as the time to show "later" items.
- Whether the kit should ship a reference notifier, or only the contract and an ntfy
  recipe.
