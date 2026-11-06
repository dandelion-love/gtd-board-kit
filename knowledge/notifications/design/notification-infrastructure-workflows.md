---
type: Reference
title: Notification infrastructure workflows
description: Novu, Knock and Courier model a notification as a workflow of steps (digest or batch, throttle, preference check, channel routing with fallback), which gives the kit a ready vocabulary for its own send logic.
tags: [notifications, novu, knock, courier, digest, throttle, preferences, prior-art]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: novu-digest, title: "Novu Docs: Digest step", resource: "https://docs.novu.co/platform/workflow/add-and-configure-steps/configure-action-steps/digest", accessed: 2026-11-05}
  - {id: knock-batch, title: "Knock Docs: Batch function", resource: "https://docs.knock.app/designing-workflows/batch-function", accessed: 2026-11-05}
  - {id: knock-throttle, title: "Knock Docs: Throttle function", resource: "https://docs.knock.app/designing-workflows/throttle-function", accessed: 2026-11-05}
  - {id: knock-prefs, title: "Knock Docs: Preferences overview", resource: "https://docs.knock.app/preferences/overview", accessed: 2026-11-05}
  - {id: courier-routing, title: "Courier Docs: Routing and failover", resource: "https://www.courier.com/docs/send/routing", accessed: 2026-11-05}
  - {id: courier-digest, title: "Courier Docs: Digests setup", resource: "https://www.courier.com/docs/platform/preferences/digests-setup", accessed: 2026-11-05}
---

# What it is

Novu, Knock and Courier are hosted notification platforms. The kit will not use them,
but they encode the same send pipeline the kit needs. A trigger enters a **workflow**;
steps decide whether, when and where a message goes.

# The step vocabulary

| Step | Mechanism | Example |
| --- | --- | --- |
| Digest / batch | collect events per recipient (plus an optional key) for a window, then send once | Novu groups by subscriber plus one payload key[^novu-digest]; Knock by recipient plus a batch key[^knock-batch] |
| Look-back digest | send the first event now; start a digest only if a similar one went out recently | Novu "When events repeat"[^novu-digest] |
| Scheduled digest | deliver at calendar times in the recipient's time zone | Novu hourly/daily/weekly[^novu-digest]; Courier Daily, Weekly, Every weekday[^courier-digest] |
| Throttle | at most N runs per recipient (plus key) per window; default N is 1 | Knock throttle[^knock-throttle] |
| Preference check | send only if every applicable opt-in is true | Knock categories, workflows, channel types[^knock-prefs] |
| Routing with fallback | try channels in order and stop at the first that delivers | Courier `method: single`; `all` sends on every channel[^courier-routing] |

# Details worth copying

- **Batch caps.** Knock closes a batch early at a maximum activity count, and templates
  render only the first ten items by default.[^knock-batch] A digest should say "and 14 more".
- **Empty digests are skipped** by default in Courier.[^courier-digest]
- **Per-topic cadence chosen by the user.** Courier lets each user pick Instant or a
  schedule per topic; Instant means no batching.[^courier-digest]
- **Hold for the user's schedule.** Novu can extend a digest to the subscriber's next
  delivery window; if not, off-schedule email, SMS, push and chat steps are skipped
  while in-app still delivers.[^novu-digest]
- **Overrides.** A Knock workflow can be marked to ignore preferences, for messages
  that must always go out.[^knock-prefs]
- **Fallback order.** Courier example: push, then email if there is no push token, then
  SMS if email fails.[^courier-routing] It retries for about a day and caps a message at
  72 hours.[^courier-routing]

# What the kit can take from it

- Model the notifier as a small pipeline: classify, dedupe key, preference check,
  throttle, digest-or-push, route with fallback, record.
- Use a **look-back digest** for FYI events: the first one may go out, repeats roll up.
- Use a **throttle of 1 per issue per window** on pushes, keyed by issue and ask type.
- Keep a **must-send override** only for asks that block work, such as approvals.
- Treat the in-app surface (the board) as the channel that always receives; other
  channels are optional copies.
- Skip empty digests, and cap each digest with a count of what was left out.

[^novu-digest]: Novu Docs, Digest step.
[^knock-batch]: Knock Docs, Batch function.
[^knock-throttle]: Knock Docs, Throttle function.
[^knock-prefs]: Knock Docs, Preferences overview.
[^courier-routing]: Courier Docs, Routing and failover.
[^courier-digest]: Courier Docs, Digests setup.
