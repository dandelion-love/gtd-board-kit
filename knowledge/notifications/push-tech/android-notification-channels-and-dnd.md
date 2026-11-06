---
type: Reference
title: Android notification channels and limits
description: On Android every notification belongs to a channel whose importance the user controls; Do Not Disturb bypass and full-screen intents exist but are user-gated, and since Android 14 full-screen intents are reserved for calls and alarms.
tags: [android, channels, importance, do-not-disturb, full-screen-intent, play-policy]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: android-channels, title: "Android Developers: Create and manage notification channels", resource: "https://developer.android.com/develop/ui/views/notifications/channels", accessed: 2026-11-05}
  - {id: aosp-fsi, title: "Android Open Source Project: Full-screen intent limits", resource: "https://source.android.com/docs/core/permissions/fsi-limits", accessed: 2026-11-05}
  - {id: play-fsi, title: "Play Console Help: Understanding foreground service and full-screen intent requirements (found by title search)", resource: "https://support.google.com/googleplay/android-developer/search?q=foreground+service+and+full-screen+intent+requirements", accessed: 2026-11-05}
  - {id: bcd-swr, title: "MDN browser-compat-data: showNotification options", resource: "https://github.com/mdn/browser-compat-data/blob/main/api/ServiceWorkerRegistration.json", accessed: 2026-11-05}
---

# Channels and importance

Since Android 8.0 every notification must name a channel.[^android-channels]

| User-visible level | Constant | Behaviour[^android-channels] |
| --- | --- | --- |
| Urgent | `IMPORTANCE_HIGH` | sound and heads-up banner |
| High | `IMPORTANCE_DEFAULT` | sound |
| Medium | `IMPORTANCE_LOW` | no sound |
| Low | `IMPORTANCE_MIN` | no sound, not in status bar |

An app cannot change a channel's importance after creating it; the user can, at any
time.[^android-channels] So the first channel design sticks.

# Do Not Disturb

A channel can be flagged to bypass DND (`setBypassDnd`), but the user decides in system
settings which apps may interrupt. The exact conditions under which the flag is honoured
were not confirmed from the API reference in this pass.

# Full-screen intents (FSI)

- Android 14+ limits `USE_FULL_SCREEN_INTENT`. Google Play revokes it at install for
  apps without calling or alarm features; apps check `canUseFullScreenIntent()` and
  may send the user to a settings page to ask.[^aosp-fsi]
- Play policy: declaration required from 31 May 2024; from 22 January 2025 the
  default grant applies only to alarm and calling apps targeting Android 14+.[^play-fsi]
- A review notifier is neither, so FSI is effectively closed to it.

# Web apps on Android

Chrome and Firefox on Android post Web Push notifications into a channel the browser
owns (one per site, general knowledge, not re-verified). The site cannot pick
importance or DND bypass; the user can raise that site's channel to Urgent. Chrome
supports `requireInteraction`, `renotify` and actions; `vibrate` is not supported on
Chrome Android.[^bcd-swr]

# 2026 status

No relaxation of these rules was found in the pages read. The AOSP FSI page was last
updated October 2026.[^aosp-fsi]

# What the kit can take from it

- For the web path: tell the owner to set the kit site's notification channel to
  "Urgent" (or allow it in DND) once, in Android settings.
- If a native app ever exists: two channels, "Needs you" (high) and "FYI" (low), fixed
  at first launch; no FSI.
- Never design around a full-screen takeover; it is policy-blocked.

[^android-channels]: Android Developers, notification channels.
[^aosp-fsi]: AOSP, Full-screen intent limits.
[^play-fsi]: Play Console Help, foreground service and full-screen intent requirements.
[^bcd-swr]: MDN compat data, showNotification options.
