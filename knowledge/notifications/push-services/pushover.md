---
type: Reference
title: Pushover
description: Pushover is a hosted, closed-source push service with apps for iOS, Android and desktop browsers; its emergency priority repeats until the user acknowledges, and its iOS app can send critical alerts that bypass mute.
tags: [notifications, push, pushover, escalation, acknowledgement, ios, critical-alerts]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: po-api, title: "Pushover: Message API", resource: "https://pushover.net/api", accessed: 2026-11-05}
  - {id: po-receipts, title: "Pushover: Receipts and callbacks API", resource: "https://pushover.net/api/receipts", accessed: 2026-11-05}
  - {id: po-pricing, title: "Pushover: Pricing", resource: "https://pushover.net/pricing", accessed: 2026-11-05}
  - {id: po-desktop, title: "Pushover: Desktop client", resource: "https://pushover.net/clients/desktop", accessed: 2026-11-05}
  - {id: po-critical, title: "Pushover support: critical alerts for emergency priority only", resource: "https://support.pushover.net/i148-option-to-have-critical-alerts-on-ios-for-emergency-priority-messages-only-not-high-priority-and-emergency-priority-as-it-is-now", accessed: 2026-11-05}
---

# What it is

A hosted service, not self-hostable and not open source. One-time 4.99 USD per
platform (iOS, Android, Desktop) after a 30-day trial; 10,000 messages a month free
per user; Teams 5 USD per user per month.[^po-pricing]

# How a sender posts

HTTPS POST to the messages endpoint on `api.pushover.net` with `token` (app, 30
chars) and `user` (user or group key).[^po-api] Limits: body 1024 chars, title 250,
`url` 512, `url_title` 100.[^po-api] Optional `device`, `ttl`, `tags`. Over quota returns
HTTP 429; after a 5xx wait at least 5 seconds before retrying.[^po-api]

# Priority

| Value | Behaviour |
| --- | --- |
| -2 | no notification (iOS: badge only) |
| -1 | quiet: no sound or vibration |
| 0 | normal |
| 1 | high: bypasses the user's quiet hours, shown red |
| 2 | emergency: repeats until acknowledged; needs `retry` and `expire` |

Source: [^po-api]. Emergency rules: `retry` at least 30 s; `expire` at most 10800 s
(3 h); at most 50 retries.[^po-api]

# Acknowledgement loop

- A priority-2 send returns a `receipt`.[^po-api]
- Poll the receipt at most once per 5 s, for up to a week. Fields: `acknowledged`,
  `acknowledged_at`, `acknowledged_by_device`, `expired`, `called_back`.[^po-receipts]
- Or pass `callback`: Pushover POSTs to your URL on acknowledge, retrying after a
  minute on non-2xx.[^po-receipts]
- Cancel by receipt or by tag, e.g. when the owner answers on GitHub instead.[^po-receipts]

# iOS and desktop

- iOS critical alerts sound even on mute or Do Not Disturb. They need an Apple
  entitlement, which Pushover holds. Originally they applied to both high and emergency
  priority; an option to limit them to emergency shipped in a TestFlight beta, date not
  given.[^po-critical]
- Desktop: a web app for Chrome, Firefox and Safari; macOS can receive without an open
  browser after Safari registration. 10 devices per account.[^po-desktop]

# 2026 status

Active and commercial; the API pages above were live on 2026-11-05.

# What the kit can take from it

- The **escalation model** is the reference design: priority 2, retry interval, hard
  expiry, receipt, callback on acknowledge, cancel by tag.
- For a busy owner on iOS, Pushover is the cheapest way to get a critical alert. A
  self-built server cannot get Apple's critical-alerts entitlement easily.
- Use it as an **optional adapter** (tagged by issue) beside the open default, not as
  the core: it is closed and paid.

[^po-api]: Pushover, Message API.
[^po-receipts]: Pushover, Receipts and callbacks API.
[^po-pricing]: Pushover, Pricing.
[^po-desktop]: Pushover, Desktop client.
[^po-critical]: Pushover support forum, critical alerts for emergency priority.
