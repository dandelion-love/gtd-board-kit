---
type: Reference
title: iOS interruption levels and Focus
description: iOS ranks notifications as passive, active, time-sensitive or critical; only native apps can set a level, time-sensitive needs a capability and critical needs Apple's approval, so a web app is always "active" under Focus.
tags: [ios, apns, focus, interruption-level, critical-alerts, time-sensitive]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: apple-levels, title: "Apple: UNNotificationInterruptionLevel", resource: "https://developer.apple.com/documentation/usernotifications/unnotificationinterruptionlevel", accessed: 2026-11-05}
  - {id: apple-remote, title: "Apple: Generating a remote notification", resource: "https://developer.apple.com/documentation/usernotifications/generating-a-remote-notification", accessed: 2026-11-05}
  - {id: apple-critical, title: "Apple: Critical Alerts entitlement", resource: "https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.usernotifications.critical-alerts", accessed: 2026-11-05}
  - {id: webkit-ios164, title: "WebKit blog: Web Push for Web Apps on iOS and iPadOS", resource: "https://webkit.org/?p=13878", accessed: 2026-11-05}
  - {id: webkit-dwp, title: "WebKit blog: Meet Declarative Web Push", resource: "https://webkit.org/?p=16535", accessed: 2026-11-05}
---

# The four levels

Available since iOS 15 and macOS 12.[^apple-levels]

| Level | What the system does[^apple-levels] | Who may use it |
| --- | --- | --- |
| passive | adds to the list; no screen wake, no sound | any app |
| active (default) | shows now, lights the screen, may play a sound | any app |
| time-sensitive | as active, and "breaks through system notification controls" (Focus, summary) | native app with the Time Sensitive capability; user can turn it off per app |
| critical | as active, and plays sound through the mute switch and Do Not Disturb | native app with an Apple-granted entitlement plus a separate user grant |

Remote pushes set the level with the `interruption-level` key in `aps`. A critical push
also uses a `sound` dictionary with `critical: 1`.[^apple-remote] `relevance-score`
(0 to 1) orders an app's notifications in the summary.[^apple-remote]

# Critical alerts

Apple grants the entitlement only on request through a form.[^apple-critical] It is
meant for health, safety and security uses (Apple's own framing; the entitlement page
only links the form). A developer tool that asks a human to review a PR does not fit.

# Focus

Focus is the user's filter. Allowed people and apps break through; others wait.
Home Screen web apps "respect Focus", and Focus settings follow the web app by manifest
ID across devices.[^webkit-ios164] The user can add the web app to a Focus's allowed
apps, which is the only break-through a web app gets.

# What a web app can and cannot use

- Can: a normal (active) notification, a badge, and since 18.4 the declarative
  `silent` flag.[^webkit-dwp]
- Cannot: time-sensitive or critical. Neither WebKit article lists any level field,
  and Web Push `Urgency` only affects delivery timing, not display.[^webkit-dwp]
  (Absence confirmed by reading; no Apple statement says "never".)

# What the kit can take from it

- Tell the owner how to allow the kit's web app in their Work Focus; ship this as a
  setup step.
- Do not rely on sound or Focus break-through for "agent blocked". Pair it with a
  repeat or escalation channel instead.
- If a native app is ever built, request only time-sensitive, never critical.

[^apple-levels]: Apple, UNNotificationInterruptionLevel.
[^apple-remote]: Apple, Generating a remote notification.
[^apple-critical]: Apple, Critical Alerts entitlement page.
[^webkit-ios164]: WebKit blog, Web Push for Web Apps on iOS and iPadOS.
[^webkit-dwp]: WebKit blog, Meet Declarative Web Push.
