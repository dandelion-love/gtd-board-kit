---
type: Research Finding
title: Push technology choice for 2026
description: Standard Web Push, sent in the Declarative Web Push format, is still the cheapest single technology that reaches Android, iOS and desktop in 2026, at the cost of an iOS install step and no Focus break-through on iPhone.
tags: [web-push, declarative, decision, android, ios, desktop, notifier]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: rfc8030, title: "RFC 8030: Generic Event Delivery Using HTTP Push", resource: "https://datatracker.ietf.org/doc/html/rfc8030", accessed: 2026-11-05}
  - {id: webkit-ios164, title: "WebKit blog: Web Push for Web Apps on iOS and iPadOS", resource: "https://webkit.org/?p=13878", accessed: 2026-11-05}
  - {id: webkit-dwp, title: "WebKit blog: Meet Declarative Web Push", resource: "https://webkit.org/?p=16535", accessed: 2026-11-05}
  - {id: bcd-pushmanager, title: "MDN browser-compat-data: PushManager", resource: "https://github.com/mdn/browser-compat-data/blob/main/api/PushManager.json", accessed: 2026-11-05}
  - {id: apple-members, title: "Apple: Choosing a Membership", resource: "https://developer.apple.com/support/compare-memberships", accessed: 2026-11-05}
  - {id: apple-levels, title: "Apple: UNNotificationInterruptionLevel", resource: "https://developer.apple.com/documentation/usernotifications/unnotificationinterruptionlevel", accessed: 2026-11-05}
  - {id: fcm-v1, title: "Firebase: Migrate from legacy FCM APIs to HTTP v1", resource: "https://firebase.google.com/docs/cloud-messaging/migrate-v1", accessed: 2026-11-05}
  - {id: apple-tn2277, title: "Apple Technical Note TN2277: Networking and Multitasking", resource: "https://developer.apple.com/library/archive/technotes/tn2277/_index.html", accessed: 2026-11-05}
  - {id: android-fgs14, title: "Android Developers: Foreground service types (required since Android 14)", resource: "https://developer.android.com/develop/background-work/services/fgs/service-types", accessed: 2026-11-05}
---

# Question

Which push technology lets a small self-hosted server alert one owner on Android, iOS
and desktop with the least setup?

# Comparison

| Option | Android | iOS | Desktop | Accounts / cost | Kit effort |
| --- | --- | --- | --- | --- | --- |
| Web Push (VAPID) | yes, browser or PWA | yes, Home Screen app, 16.4+[^webkit-ios164] | yes, browser running[^bcd-pushmanager] | none | one server lib + page + small worker |
| Declarative Web Push | via worker fallback | yes, 18.4+, no worker needed[^webkit-dwp] | Safari 18.5; others via worker | none | same as above |
| Native APNs + FCM | yes | yes | macOS only | Apple program[^apple-members] + Firebase project[^fcm-v1] | two apps, signing, store review |
| Own socket (WS/SSE) | typed foreground service[^android-fgs14] | dies on suspend[^apple-tn2277] | yes | none | native app per OS |
| Third-party app (ntfy, Pushover) | yes | yes, through the vendor's relay | yes | vendor app, sometimes paid | small adapter |

# What Web Push cannot do

- No iOS time-sensitive or critical level; Focus can hold the alert.[^apple-levels]
- iOS needs the owner to install the web app once and tap Enable.[^webkit-ios164]
- Desktop needs the browser or installed web app running.
- Delivery is best effort; the push service may drop expired messages.[^rfc8030]

# Conclusion

**Yes, Web Push is still the best default in 2026.** It is the only option that reaches
all three platforms with no vendor account, no app store and no per-user cost. Sending
the declarative JSON shape makes iOS more robust and costs nothing on other browsers.
Native push adds real value only for iOS Focus break-through, and that requires a paid
Apple account and an app the kit would have to publish. Persistent sockets are ruled out
on phones.

# Design implications

1. Server: one Web Push sender (RFC 8291 + VAPID), one key pair per deployment.
2. Payload: Declarative Web Push JSON with `navigate` to the board item; a small service
   worker for Chrome and Firefox that reads the same JSON.
3. Headers: `Urgency: high` + long `TTL` for "blocked"; `normal` for "PR ready";
   `Topic` per item so updates replace stale alerts.[^rfc8030]
4. Setup guide: install the PWA on iPhone, allow it in Focus; raise the site's Android
   channel to Urgent.
5. Escalation for missed "blocked" alerts: re-send after a delay, then an optional
   adapter (ntfy, Pushover, email). This replaces the critical level Web Push lacks.
6. Buttons only navigate or snooze; approvals happen on a signed-in page.

# Open questions

- Chrome and Firefox timelines for Declarative Web Push: none found.
- Whether Safari revokes subscriptions after invisible pushes: not confirmed.

[^rfc8030]: RFC 8030, Urgency, TTL and Topic.
[^webkit-ios164]: WebKit blog, iOS 16.4 Web Push.
[^webkit-dwp]: WebKit blog, Meet Declarative Web Push.
[^bcd-pushmanager]: MDN compat data, PushManager.
[^apple-members]: Apple, Choosing a Membership.
[^apple-levels]: Apple, interruption levels.
[^fcm-v1]: Firebase, HTTP v1 migration.
[^apple-tn2277]: Apple TN2277.
[^android-fgs14]: Android Developers, FGS types.
