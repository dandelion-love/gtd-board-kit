---
type: Reference
title: Desktop notification delivery
description: On Windows, macOS and Linux the cheapest path is browser Web Push, which needs the browser or installed web app running; native OS notification APIs need an app, and Flutter's FCM plugin has no Windows or Linux support.
tags: [desktop, windows, macos, linux, web-push, flutter]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: ntfy-pwa, title: "ntfy docs: Using the web app as a PWA", resource: "https://docs.ntfy.sh/subscribe/pwa/", accessed: 2026-11-05}
  - {id: bcd-pushmanager, title: "MDN browser-compat-data: PushManager", resource: "https://github.com/mdn/browser-compat-data/blob/main/api/PushManager.json", accessed: 2026-11-05}
  - {id: webkit-185, title: "WebKit blog: WebKit Features in Safari 18.5", resource: "https://webkit.org/?p=16923", accessed: 2026-11-05}
  - {id: pub-fcm, title: "pub.dev: firebase_messaging", resource: "https://pub.dev/packages/firebase_messaging", accessed: 2026-11-05}
  - {id: freedesktop, title: "freedesktop.org: Desktop Notifications Specification 1.3", resource: "https://specifications.freedesktop.org/notification-spec/latest/", accessed: 2026-11-05}
  - {id: apple-levels, title: "Apple: UNNotificationInterruptionLevel", resource: "https://developer.apple.com/documentation/usernotifications/unnotificationinterruptionlevel", accessed: 2026-11-05}
---

# Browser Web Push on desktop

| Browser | Push support | Install as app |
| --- | --- | --- |
| Chrome | since 42[^bcd-pushmanager] | Windows, macOS, Linux[^ntfy-pwa] |
| Edge | since 17[^bcd-pushmanager] | Windows[^ntfy-pwa] |
| Firefox | since 44[^bcd-pushmanager] | needs an extension on Windows and Linux[^ntfy-pwa] |
| Safari (macOS) | since 16, macOS Ventura+[^bcd-pushmanager]; declarative since 18.5[^webkit-185] | macOS 14+ "Add to Dock"[^ntfy-pwa] |

- On desktop "you generally need either your browser or the web app open" to receive;
  the tab itself need not be open.[^ntfy-pwa]
- The browser hands notifications to the OS notification centre, so OS Focus or Do Not
  Disturb applies.
- Chrome and Edge show action buttons and honour `requireInteraction`
  (see `notification-actions.md`).

# OS notification APIs (native apps)

| OS | API | Notes |
| --- | --- | --- |
| macOS | UserNotifications | same four interruption levels as iOS, macOS 12+[^apple-levels]; remote push via APNs |
| Linux | `org.freedesktop.Notifications` over D-Bus | spec 1.3 (Aug 2024) with urgency levels low, normal, critical[^freedesktop]; local only, no push service |
| Windows | app notifications (toasts) | remote push via Windows Push Notification Services for packaged apps (general knowledge, not re-verified) |

A native desktop app still needs a channel to the server: a socket (fine on desktop,
since apps are not suspended like on phones) or a vendor push.

# Flutter desktop

The official `firebase_messaging` plugin lists Android, iOS, macOS and web only, not
Windows or Linux.[^pub-fcm] A Flutter desktop client would need its own socket or a
third-party plugin.

# What the kit can take from it

- Desktop is free with Web Push: the same subscription code as mobile.
- Tell the owner to install the web app (Chrome/Edge) or add it to the Dock (Safari) and
  let the browser start at login, so pushes are not missed while it is closed.
- A tiny native tray app or CLI watcher holding a socket is a fine optional extra for
  Linux power users; no vendor account needed on desktop.

[^ntfy-pwa]: ntfy docs, PWA page.
[^bcd-pushmanager]: MDN compat data, PushManager.
[^webkit-185]: WebKit blog, Safari 18.5 features (title seen via search; body not read).
[^pub-fcm]: pub.dev, firebase_messaging platform list.
[^freedesktop]: freedesktop.org Desktop Notifications Specification.
[^apple-levels]: Apple, UNNotificationInterruptionLevel availability.
