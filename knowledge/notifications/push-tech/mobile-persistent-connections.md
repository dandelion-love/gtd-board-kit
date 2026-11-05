---
type: Reference
title: Persistent connections on mobile
description: Holding a WebSocket, SSE or long-poll open from a phone works on Android only inside a typed foreground service with a visible notification, and does not work on iOS at all once the app is suspended.
tags: [android, ios, websocket, sse, foreground-service, background-limits]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: android-fgs14, title: "Android Developers: Foreground service types (required since Android 14)", resource: "https://developer.android.com/develop/background-work/services/fgs/service-types", accessed: 2026-11-05}
  - {id: android-fgs-timeout, title: "Android Developers: Foreground service timeouts", resource: "https://developer.android.com/develop/background-work/services/fg-service-timeout", accessed: 2026-11-05}
  - {id: play-fgs, title: "Play Console Help: Understanding foreground service and full-screen intent requirements (found by title search)", resource: "https://support.google.com/googleplay/android-developer/search?q=foreground+service+and+full-screen+intent+requirements", accessed: 2026-11-05}
  - {id: apple-tn2277, title: "Apple Technical Note TN2277: Networking and Multitasking (archived)", resource: "https://developer.apple.com/library/archive/technotes/tn2277/_index.html", accessed: 2026-11-05}
  - {id: apple-bg, title: "Apple: Pushing background updates to your App", resource: "https://developer.apple.com/documentation/usernotifications/pushing-background-updates-to-your-app", accessed: 2026-11-05}
  - {id: ntfy-config, title: "ntfy docs: Configuration", resource: "https://docs.ntfy.sh/config/", accessed: 2026-11-05}
---

# The idea

Skip the vendor push service: the phone keeps a socket to the kit's server and the
server writes to it. This is how self-hosted tools avoid Google and Apple. Mobile
operating systems fight it to save battery.

# Android

- Without FCM, an app must run a **foreground service** to receive messages; ntfy says
  FCM is the only way to receive without one.[^ntfy-config]
- Apps targeting Android 14 must declare a service type. None fits "listen for
  notifications" well: `remoteMessaging` is for moving text messages between a user's
  devices; `specialUse` is the catch-all and needs a written justification that Play
  reviews.[^android-fgs14]
- Play requires a per-type declaration with a description and a demo video.[^play-fgs]
- Android 15 caps `dataSync` and `mediaProcessing` services at 6 hours per 24 hours in
  the background; at the limit the service must stop or the app crashes.[^android-fgs-timeout]
  Picking `dataSync` for a socket would break after 6 hours.
- The service shows a permanent notification. Since Android 14 users can swipe it away
  (general Android 14 change, not re-read here).

# iOS

- When an app is suspended "no code within the app's process executes", and the system
  may reclaim its sockets.[^apple-tn2277] A WebSocket or SSE stream dies within seconds
  of backgrounding.
- Silent background pushes are throttled to "two or three per hour" and are not
  guaranteed.[^apple-bg] They cannot replace a socket.
- The only reliable wake-up for an iOS app is a visible APNs push.

# Comparison

| Method | Android | iOS | Desktop |
| --- | --- | --- | --- |
| WebSocket / SSE / long-poll | foreground service, typed, visible, Play-reviewed | foreground only | fine while app runs |
| Vendor push (Web Push, FCM, APNs) | yes, no service needed | yes | yes, browser running |

# What the kit can take from it

- Use sockets only for the open web page (live board view), never as the alert path.
- The alert path must be vendor push: Web Push in the browser or PWA.
- Users who want no Google at all can use a UnifiedPush or ntfy app on Android; that is
  their choice, and the kit can support it as an extra target.

[^android-fgs14]: Android Developers, FGS types required.
[^android-fgs-timeout]: Android Developers, FGS timeouts.
[^play-fgs]: Play Console Help, FGS declaration.
[^apple-tn2277]: Apple TN2277 (2011, archived, still describes suspension).
[^apple-bg]: Apple, Pushing background updates.
[^ntfy-config]: ntfy configuration docs, Firebase section.
