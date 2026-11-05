---
type: Reference
title: Declarative Web Push
description: A Web Push payload in a fixed JSON shape that the browser shows itself, with no service worker code; shipped in Safari on iOS/iPadOS 18.4 and macOS Safari 18.5, still not in Chrome or Firefox in November 2026.
tags: [web-push, declarative, safari, webkit, w3c, browser-support]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: webkit-dwp, title: "WebKit blog: Meet Declarative Web Push (2025-03-27)", resource: "https://webkit.org/?p=16535", accessed: 2026-11-05}
  - {id: webkit-184, title: "WebKit blog: WebKit Features in Safari 18.4 (2025-03-31)", resource: "https://webkit.org/?p=16574", accessed: 2026-11-05}
  - {id: webkit-185, title: "WebKit blog: WebKit Features in Safari 18.5", resource: "https://webkit.org/?p=16923", accessed: 2026-11-05}
  - {id: w3c-push, title: "W3C Push API, Working Draft", resource: "https://www.w3.org/TR/push-api/", accessed: 2026-11-05}
  - {id: bcd-window, title: "MDN browser-compat-data: Window.pushManager", resource: "https://github.com/mdn/browser-compat-data/blob/main/api/Window.json", accessed: 2026-11-05}
  - {id: bcd-pushevent, title: "MDN browser-compat-data: PushEvent.notification", resource: "https://github.com/mdn/browser-compat-data/blob/main/api/PushEvent.json", accessed: 2026-11-05}
  - {id: aimtell, title: "Aimtell: The State of Declarative Web Push in 2026 (secondary)", resource: "https://aimtell.com/blog/state-of-declarative-web-push-2026", accessed: 2026-11-05}
---

# What it is

Classic Web Push hands an opaque payload to a service worker, which must call
`showNotification()`. Declarative Web Push lets the payload **be** the notification:
the browser parses it and shows it, even if no service worker exists.[^webkit-dwp]
Subscribing works from `window.pushManager`, without registering a worker.[^webkit-dwp]

# Payload shape

```json
{ "web_push": 8030,
  "notification": { "title": "Agent needs you", "body": "Which option?",
                    "navigate": "https://example.org/item", "lang": "en" },
  "mutable": false }
```

- `web_push: 8030` opts in; `notification.title` and `notification.navigate` are
  required.[^w3c-push] `body`, `lang`, `dir`, `silent` and an `app_badge` number are
  shown in WebKit's article.[^webkit-dwp]
- `mutable: true` sends a `push` event to a service worker, if any, which may replace
  the notification. If the worker fails, the declarative one is shown.[^w3c-push][^webkit-dwp]
- Not confirmed: whether the final draft keeps `app_badge` at top level; the current
  draft's member list did not show it.[^w3c-push]

# Support, November 2026

| Engine | Status |
| --- | --- |
| Safari iOS/iPadOS 18.4+ | shipped; Home Screen web apps only[^webkit-184] |
| Safari macOS 18.5+ (macOS 15.5) | shipped[^webkit-185] |
| Chrome / Edge | not shipped; tracked in Chromium's bug tracker[^bcd-window][^bcd-pushevent] |
| Firefox | not shipped; tracked in Bugzilla[^bcd-window]. Mozilla's position is reported "positive" (Feb 2025)[^aimtell] |

Spec status: a normative "Declarative push message" section is in the W3C Push API
Working Draft.[^w3c-push] Notification `navigate` landed separately in Firefox 158 (see
`notification-actions.md`). No shipping date for Chrome was found.

# Limits

- No service worker means no custom logic: no dedupe, no fetch of fresh state.
- Action buttons are not in WebKit's announced member list; Safari has no
  notification actions at all (see `notification-actions.md`).
- Senders must still encrypt with RFC 8291 and sign with VAPID.

# What the kit can take from it

- Always send the declarative JSON shape. Safari shows it natively; Chrome and Firefox
  deliver it to a small service worker that reads the same fields and calls
  `showNotification()`. One payload format serves all browsers.
- It makes iOS more robust: the notification shows even when the worker is evicted.
- Put the board item URL in `navigate` so a tap opens the right page.

[^webkit-dwp]: WebKit blog, Meet Declarative Web Push.
[^webkit-184]: WebKit blog, Safari 18.4 features.
[^webkit-185]: WebKit blog, Safari 18.5 features (confirmed by search listing and press coverage; page body not read).
[^w3c-push]: W3C Push API Working Draft, section 3.3.
[^bcd-window]: MDN compat data, `Window.pushManager` (Chrome and Firefox: not added).
[^bcd-pushevent]: MDN compat data, `PushEvent.notification` (Chrome and Firefox: not added).
[^aimtell]: Aimtell blog, secondary source on Mozilla's position.
