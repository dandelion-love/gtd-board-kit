---
type: Reference
title: PagerDuty urgency and escalation
description: PagerDuty splits incidents into high and low urgency, escalates only unacknowledged high-urgency work, folds repeat alerts into one incident, and can store events without paging anyone.
tags: [notifications, pagerduty, urgency, escalation, deduplication, prior-art]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: pd-dynamic, title: "PagerDuty Docs: Dynamic Notifications", resource: "https://docs.pagerduty.com/incident-management/incidents/dynamic-notifications", accessed: 2026-11-05}
  - {id: pd-escalation, title: "PagerDuty Docs: Escalation Policy Basics", resource: "https://docs.pagerduty.com/incident-management/schedules/escalation-policies", accessed: 2026-11-05}
  - {id: pd-events, title: "PagerDuty Docs: Event Management", resource: "https://docs.pagerduty.com/incident-management/incidents/event-management", accessed: 2026-11-05}
  - {id: pd-iag, title: "PagerDuty Docs: Intelligent Alert Grouping", resource: "https://docs.pagerduty.com/ai-automation/aiops/noise-reduction/alert-grouping/intelligent-alert-grouping", accessed: 2026-11-05}
  - {id: pd-sleep, title: "PagerDuty Community on DEV: Better sleep with dynamic notifications and support hours (2022)", resource: "https://dev.to/pdcommunity/better-sleep-with-pagerduty-dynamic-notifications-and-support-hours-4jkp", accessed: 2026-11-05}
---

# What it is

PagerDuty is an on-call paging service. Its job is to wake the right person only for
work that cannot wait. It is the clearest prior art for "how loud" and "what if nobody
answers".

# Urgency tiers

| Tier | Triggered by | Behaviour |
| --- | --- | --- |
| High | `critical`, `error` or unknown severity | high-urgency rules; escalates if not acknowledged[^pd-dynamic] |
| Low | `warning`, `info` | low-urgency rules; "cannot escalate"[^pd-dynamic] |

- Each person sets separate contact methods per tier. Email for low urgency is the
  suggested default.[^pd-sleep]
- Urgency can rise but never fall. A warning that turns critical becomes high.[^pd-dynamic]
- **Support hours**: a service can use one urgency inside a defined window and another
  outside it.[^pd-dynamic] The 2022 community post describes a checkbox to raise
  still-unacknowledged incidents to high when support hours begin.[^pd-sleep] The current
  docs page does not mention it, so treat it as unconfirmed.

# Acknowledge and escalate

- An escalation policy is an ordered list of levels. Level one is notified at once.[^pd-escalation]
- Each level has a timeout ("escalates after N min"); the default is 30 minutes.[^pd-escalation]
- **Acknowledge** stops escalation and further notifications but does not resolve the
  incident. If it re-triggers, escalation resumes.[^pd-escalation]
- A policy can repeat up to nine times, then stops notifying the last person.[^pd-escalation]

# Grouping, dedupe and suppression

- **Alert vs incident**: an alert is a raw event; only an incident notifies people.[^pd-events]
- **`dedup_key`**: later alerts with the same key join the open incident instead of
  creating a new one.[^pd-events]
- **Intelligent grouping** merges similar alerts that arrive within a rolling window,
  for incidents under 24 hours old.[^pd-iag]
- **Suppression** stores an event for review without creating an incident or paging
  anyone.[^pd-events]

# What the kit can take from it

- Two tiers are enough: "needs you now" (push, may escalate) and "FYI" (digest, never
  escalates).
- Give every ask a stable dedupe key, such as the issue and the ask type. A repeat
  updates the open ask; it does not send a second ping.
- Acknowledge means "I have seen it", not "done". Track both states on the issue.
- Escalation for a solo owner is a channel ladder, not a people ladder: board, then
  push, then a louder channel after a timeout. Cap the repeats.
- Quiet hours should downgrade, not drop: hold the ask and raise it when the window opens.
- Suppressed events still get recorded, so nothing is lost.

[^pd-dynamic]: PagerDuty Docs, Dynamic Notifications.
[^pd-escalation]: PagerDuty Docs, Escalation Policy Basics.
[^pd-events]: PagerDuty Docs, Event Management.
[^pd-iag]: PagerDuty Docs, Intelligent Alert Grouping.
[^pd-sleep]: PagerDuty Community, Better sleep with dynamic notifications (January 2022).
