---
type: Research Finding
title: Notification design principles
description: Eight rules, drawn from paging tools, notification platforms, chat and tracker inboxes, coding agents and interruption research, for notifying one busy owner only when they must act.
tags: [notifications, attention, design-principles, synthesis, urgency, digest]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: pd-dynamic, title: "PagerDuty Docs: Dynamic Notifications", resource: "https://docs.pagerduty.com/incident-management/incidents/dynamic-notifications", accessed: 2026-11-05}
  - {id: pd-escalation, title: "PagerDuty Docs: Escalation Policy Basics", resource: "https://docs.pagerduty.com/incident-management/schedules/escalation-policies", accessed: 2026-11-05}
  - {id: pd-events, title: "PagerDuty Docs: Event Management", resource: "https://docs.pagerduty.com/incident-management/incidents/event-management", accessed: 2026-11-05}
  - {id: novu-digest, title: "Novu Docs: Digest step", resource: "https://docs.novu.co/platform/workflow/add-and-configure-steps/configure-action-steps/digest", accessed: 2026-11-05}
  - {id: knock-throttle, title: "Knock Docs: Throttle function", resource: "https://docs.knock.app/designing-workflows/throttle-function", accessed: 2026-11-05}
  - {id: linear-notif, title: "Linear Docs: Notifications", resource: "https://linear.app/docs/notifications", accessed: 2026-11-05}
  - {id: gh-about-notif, title: "GitHub Docs: About notifications", resource: "https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications", accessed: 2026-11-05}
  - {id: iqbal-bailey-08, title: "Iqbal and Bailey, Effects of Intelligent Notification Management (CHI 2008)", resource: "https://www.interruptions.net/literature/Iqbal-CHI08.pdf", accessed: 2026-11-05}
  - {id: mark-08, title: "Mark, Gudith and Klocke, The Cost of Interrupted Work (CHI 2008)", resource: "https://www.interruptions.net/literature/Mark-CHI08.pdf", accessed: 2026-11-05}
  - {id: ancker-17, title: "Ancker et al., Repeated alerts and alert fatigue in clinical decision support (BMC Med Inform Decis Mak, 2017)", resource: "https://scholar.google.com/scholar?q=%22Effects+of+workload%2C+work+complexity%2C+and+repeated+alerts+on+alert+fatigue%22", doi: 10.1186/s12911-017-0430-8, accessed: 2026-11-05}
---

# Context

One owner, many agents, one board. The owner's attention is the scarcest resource.
These rules synthesise the sibling pages in this set.

# The rules

| # | Rule | Evidence |
| --- | --- | --- |
| 1 | **Push only what is actionable.** A push must name something only the owner can do: approve, decide, unblock, review. | interruptions raise stress even when people keep pace[^mark-08]; useful-but-not-actionable goes elsewhere |
| 2 | **One ask per message.** One issue, one question, one-step answers. Bundle extra asks on the same issue into that one message. | acceptance falls 30% per extra reminder in one encounter[^ancker-17] |
| 3 | **Two urgency tiers.** *Now* (push, may escalate) and *Later* (digest, never escalates). Urgency may rise, never fall. | high and low urgency; low "cannot escalate"[^pd-dynamic] |
| 4 | **Digest the rest.** Completions, CI results and FYI events go to a scheduled digest. Skip empty digests. | scheduled and look-back digests[^novu-digest]; general items suit coarse breakpoints[^iqbal-bailey-08] |
| 5 | **Acknowledge, then escalate by channel.** An unacknowledged *Now* ask moves up a channel ladder after a timeout, with a capped number of repeats. Acknowledge stops it; it does not resolve. | escalation levels, timeouts, repeat cap[^pd-escalation]; email only if still unread[^linear-notif] |
| 6 | **Quiet hours hold, they do not drop.** Outside the owner's window, *Now* asks wait and are delivered when it opens. A rationed break-through is the only exception. | support hours[^pd-dynamic]; defer to breakpoints[^iqbal-bailey-08] |
| 7 | **Dedupe and replace.** Each ask has a stable key (issue plus ask type). A repeat updates the open ask instead of sending again. Throttle pushes per key. | `dedup_key`[^pd-events]; throttle limit of 1 per window[^knock-throttle]; repeats drive fatigue[^ancker-17] |
| 8 | **The record stays in the system of record.** The issue or PR holds the ask, its state and the answer. A push is only a pointer. Every message carries a machine-readable reason. | reasons and filters[^gh-about-notif]; suppressed events still stored[^pd-events] |

# How the rules fit together

```text
event -> is it an ask for the owner? -- no --> board state + digest
             | yes
             v
         dedupe key exists? -- yes --> update the open ask (no push)
             | no
             v
         tier Now? -- no --> digest
             | yes
             v
         in quiet hours? -- yes --> hold until window opens
             | no
             v
         push one message -> wait for ack -> escalate by channel (capped)
```

# Measures

Track pushes per day, asks per issue, repeat pushes (target zero) and the acknowledge
rate; a falling rate means too many pushes.[^ancker-17]

# Open questions

- The right *Now* timeout for one owner is unknown. PagerDuty's 30-minute default is a
  team setting, not a solo one.[^pd-escalation]
- Whether to detect breakpoints automatically (for example after the owner merges a PR)
  or use fixed digest times needs a trial.

[^pd-dynamic]: PagerDuty Docs, Dynamic Notifications.
[^pd-escalation]: PagerDuty Docs, Escalation Policy Basics.
[^pd-events]: PagerDuty Docs, Event Management.
[^novu-digest]: Novu Docs, Digest step.
[^knock-throttle]: Knock Docs, Throttle function.
[^linear-notif]: Linear Docs, Notifications.
[^gh-about-notif]: GitHub Docs, About notifications.
[^iqbal-bailey-08]: Iqbal and Bailey, CHI 2008.
[^mark-08]: Mark, Gudith and Klocke, CHI 2008.
[^ancker-17]: Ancker et al., 2017.
