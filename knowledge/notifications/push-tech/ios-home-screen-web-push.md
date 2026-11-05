---
type: Reference
title: Web Push on iOS Home Screen web apps
description: Since iOS 16.4 a web app added to the Home Screen can receive standard Web Push through APNs with no Apple developer account, but only after install and a user tap, and with fewer options than native apps.
tags: [ios, web-push, pwa, safari, apns, eu, dma]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: webkit-ios164, title: "WebKit blog: Web Push for Web Apps on iOS and iPadOS (2023-02-16)", resource: "https://webkit.org/?p=13878", accessed: 2026-11-05}
  - {id: bcd-pushmanager, title: "MDN browser-compat-data: PushManager", resource: "https://github.com/mdn/browser-compat-data/blob/main/api/PushManager.json", accessed: 2026-11-05}
  - {id: bcd-swr, title: "MDN browser-compat-data: showNotification options", resource: "https://github.com/mdn/browser-compat-data/blob/main/api/ServiceWorkerRegistration.json", accessed: 2026-11-05}
  - {id: silicon-dma, title: "Silicon UK: Apple Reverses Course Over EU Ban On Web Apps (2024-03-04)", resource: "https://www.silicon.co.uk/mobility/smartphones/apple-dma-web-apps-552741", accessed: 2026-11-05}
  - {id: ntfy-pwa, title: "ntfy docs: Using the web app as a PWA", resource: "https://docs.ntfy.sh/subscribe/pwa/", accessed: 2026-11-05}
---

# What it is

iOS and iPadOS 16.4 (announced February 2023) added the Push API, Notifications API
and Badging API to web apps saved to the Home Screen.[^webkit-ios164] Safari tabs on
iOS still cannot subscribe; compat data notes notifications work only "in web apps
saved to the home screen".[^bcd-pushmanager]

# Requirements

| Requirement | Detail |
| --- | --- |
| Install | user adds the site via Share, Add to Home Screen[^webkit-ios164] |
| Manifest | `display` must be `standalone` or `fullscreen`[^webkit-ios164] |
| Permission | requested in response to a direct user action, such as a tap[^webkit-ios164] |
| Account | no paid Apple Developer Program membership needed[^webkit-ios164] |
| Network | the push endpoint is on `*.push.apple.com`; allow it if you filter egress[^webkit-ios164] |
| Server | standard Web Push: VAPID plus RFC 8291 encryption (see `web-push-standard.md`) |

Notifications appear on the Lock Screen, in Notification Center and on a paired
Apple Watch, and they obey Focus. Focus settings follow the web app across the
user's devices by its manifest ID.[^webkit-ios164] Badges can update during push
handling.[^webkit-ios164] The web app does not need to be open.[^ntfy-pwa]

# Reliability limits

- The user must install first. Many users never do; onboarding has to teach it.
- No action buttons, no `requireInteraction`, no `renotify`, no images: Safari has
  none of these `showNotification()` options.[^bcd-swr]
- No interruption level: a web app cannot mark a push time-sensitive or critical
  (see `ios-interruption-levels-and-focus.md`). Not found in any WebKit doc.
- Not confirmed from a primary source: reports that Safari revokes a subscription when
  pushes arrive without a visible notification. Declarative Web Push (18.4+) reduces
  this risk because the system shows the notification itself.
- Deleting the Home Screen icon removes the app and, by implication, its subscription
  (not confirmed in WebKit docs).

# EU and the DMA

In February 2024 Apple's iOS 17.4 betas removed Home Screen web apps in the EU, citing
DMA compliance. In early March 2024 Apple reversed this and kept them, still built on
WebKit, in the final 17.4 release.[^silicon-dma] No later change was found.

# What the kit can take from it

- iOS is reachable with the same Web Push server as Android and desktop, at no cost.
- Ship a manifest with `display: standalone` and a clear "Install, then tap Enable"
  step; test the flow on a real iPhone.
- Design for no buttons on iOS: the notification is a link into the board page.
- Do not promise Focus break-through on iOS for the web path.

[^webkit-ios164]: WebKit blog, Web Push for Web Apps on iOS and iPadOS.
[^bcd-pushmanager]: MDN compat data, PushManager, Safari iOS note.
[^bcd-swr]: MDN compat data, showNotification options (Safari: actions, requireInteraction, renotify, image not supported).
[^silicon-dma]: Silicon UK, March 2024 report quoting Apple's updated developer note.
[^ntfy-pwa]: ntfy docs, PWA page.
