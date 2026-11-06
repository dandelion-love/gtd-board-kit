---
type: Reference
title: Notification action buttons
description: Action buttons work in Web Push on Chrome, Edge and recent Firefox but not Safari or iOS web apps, inline text reply is native-only, so a board ask from a notification must degrade to "open the item" and anything that approves must require unlock.
tags: [notifications, actions, inline-reply, web-push, ios, android, ntfy, pushover, security]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: mdn-shownotif, title: "MDN: ServiceWorkerRegistration.showNotification()", resource: "https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/showNotification", accessed: 2026-11-05}
  - {id: mdn-maxactions, title: "MDN: Notification.maxActions", resource: "https://developer.mozilla.org/en-US/docs/Web/API/Notification/maxActions_static", accessed: 2026-11-05}
  - {id: bcd-swr, title: "MDN browser-compat-data: showNotification options", resource: "https://github.com/mdn/browser-compat-data/blob/main/api/ServiceWorkerRegistration.json", accessed: 2026-11-05}
  - {id: w3c-push, title: "W3C Push API, Working Draft", resource: "https://www.w3.org/TR/push-api/", accessed: 2026-11-05}
  - {id: apple-actopts, title: "Apple: UNNotificationActionOptions", resource: "https://developer.apple.com/documentation/usernotifications/unnotificationactionoptions", accessed: 2026-11-05}
  - {id: apple-remote, title: "Apple: Generating a remote notification", resource: "https://developer.apple.com/documentation/usernotifications/generating-a-remote-notification", accessed: 2026-11-05}
  - {id: android-build, title: "Android Developers: Create a notification", resource: "https://developer.android.com/develop/ui/views/notifications/build-notification", accessed: 2026-11-05}
  - {id: ntfy-publish, title: "ntfy docs: Publishing (action buttons)", resource: "https://docs.ntfy.sh/publish/", accessed: 2026-11-05}
  - {id: pushover-api, title: "Pushover API: message priority", resource: "https://pushover.net/api", accessed: 2026-11-05}
---

# Web Push actions

- `showNotification(title, {actions: [{action, title, icon, navigate}]})`. A click on a
  button fires `notificationclick` with `event.action`; a body click gives `""`. An
  action with `navigate` opens that URL instead of firing the event.[^mdn-shownotif]
- `Notification.maxActions` reports how many buttons the browser shows.[^mdn-maxactions]
- Support: Chrome 48+, Edge 18+, Firefox 152+ (desktop and Android); **Safari and iOS
  web apps: none**.[^bcd-swr]
- Text reply: MDN documents no text-input action.[^mdn-shownotif] No shipped browser
  supports one (an old Chrome experiment was never shipped; not re-verified).
- Declarative Web Push: the draft's members are `web_push`, `notification`, `mutable`;
  no action handling was found in the parts read.[^w3c-push]

# Native iOS

- A push names a `category`; the app registers categories with buttons at launch.[^apple-remote]
- Action options: `authenticationRequired` ("only on an unlocked device"),
  `destructive`, `foreground`.[^apple-actopts]
- Text input uses `UNTextInputNotificationAction` (general knowledge, not re-read).

# Native Android

- Up to three buttons per notification.[^android-build]
- Direct reply with `RemoteInput` since Android 7.0; the text arrives in the app without
  opening it.[^android-build]
- `Action.Builder.setAuthenticationRequired(true)` (Android 12) asks for unlock first
  (general knowledge; the page read did not cover it).

# Ready-made apps

| App | Buttons | Ack |
| --- | --- | --- |
| ntfy | up to 3: `view` (open URL), `http` (send a request), `broadcast` (Android only), `copy`; `clear` after tap[^ntfy-publish] | via an `http` action to the server |
| Pushover | not covered here | priority 2 repeats every 30 s or more for up to 3 hours until acknowledged; a `receipt` and optional `callback` URL report the ack[^pushover-api] |

# What the kit can take from it

| Action for a board ask | Web (Chrome/Edge/Firefox) | iOS web app | Lock-screen safe? |
| --- | --- | --- | --- |
| Open item | body tap or `navigate` | body tap | yes; the page itself asks for sign-in |
| Answer (posted as a comment) | open a reply page; no inline text | open page | no: needs sign-in, it writes as the owner |
| Approve / pick an option | button opens a confirm page | open page | **no**: must require unlock and sign-in, never a blind tap |
| Snooze (remind in 1 h) | button, handled in worker | not available | yes, if it only delays a reminder |
| Not me (reassign) | button opens a confirm page | open page | no: changes ownership |

Rules: buttons may only **navigate** or **defer**. Anything that approves, merges,
answers or grants goes through a signed-in page with a fresh check. Never put a token
in the action URL. Treat every action as optional: on iOS there are no buttons.

[^mdn-shownotif]: MDN, showNotification() actions.
[^mdn-maxactions]: MDN, Notification.maxActions.
[^bcd-swr]: MDN compat data, actions option per browser.
[^w3c-push]: W3C Push API Working Draft, declarative members.
[^apple-actopts]: Apple, UNNotificationActionOptions.
[^apple-remote]: Apple, remote notification payload, `category` key.
[^android-build]: Android Developers, action buttons and direct reply.
[^ntfy-publish]: ntfy docs, action buttons.
[^pushover-api]: Pushover API, emergency priority and receipts.
