---
type: Reference
title: APNs and FCM native push
description: Native apps receive push only through Apple's APNs and Google's FCM; both are free to send, but each needs a vendor account, a signed app and server credentials, which is heavy for a small open-source kit.
tags: [apns, fcm, ios, android, native, accounts]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: apple-remote, title: "Apple: Generating a remote notification", resource: "https://developer.apple.com/documentation/usernotifications/generating-a-remote-notification", accessed: 2026-11-05}
  - {id: apple-bg, title: "Apple: Pushing background updates to your App", resource: "https://developer.apple.com/documentation/usernotifications/pushing-background-updates-to-your-app", accessed: 2026-11-05}
  - {id: apple-members, title: "Apple: Choosing a Membership", resource: "https://developer.apple.com/support/compare-memberships", accessed: 2026-11-05}
  - {id: fcm-v1, title: "Firebase: Migrate from legacy FCM APIs to HTTP v1", resource: "https://firebase.google.com/docs/cloud-messaging/migrate-v1", accessed: 2026-11-05}
  - {id: ntfy-config, title: "ntfy docs: Configuration (iOS and Firebase sections)", resource: "https://docs.ntfy.sh/config/", accessed: 2026-11-05}
---

# What they are

**APNs** (Apple Push Notification service) is the only route to wake an iOS app.
**FCM** (Firebase Cloud Messaging) is the standard route on Android with Google Play
services. Both sit between your server and the device.

# APNs

- Payload is JSON with an `aps` dictionary: `alert`, `sound`, `badge`, `thread-id`,
  `category` (action buttons), `interruption-level`, `relevance-score`.[^apple-remote]
- Size limit 4 KB (5 KB for VoIP).[^apple-remote]
- Silent `content-available` pushes are low priority, throttled ("not more than two
  or three per hour"), and dropped if the user force-quit the app.[^apple-bg]
- Needs a paid Apple Developer Program membership: certificates, identifiers and
  App Store Connect are program-only.[^apple-members] The fee has long been 99 USD a
  year; the page read did not state it (not confirmed here).
- Server auth is a token key (.p8) or a certificate (general knowledge, not re-read).

# FCM HTTP v1

- Legacy HTTP and XMPP APIs were deprecated 20 June 2023; shutdown began 22 July
  2024.[^fcm-v1]
- Endpoint: `https://fcm.googleapis.com/v1/projects/<project-id>/messages:send`.[^fcm-v1]
- Auth: short-lived OAuth 2.0 tokens (about one hour) minted from a service account,
  scope `firebase.messaging`.[^fcm-v1]
- FCM can also forward to APNs for iOS apps, but the app still needs Apple signing.
- Sending is free (Firebase pricing; not re-checked for this page).

# What a small project needs

| Path | Accounts | Build | Per-user setup |
| --- | --- | --- | --- |
| Own iOS app | Apple Developer Program | Xcode, signing, TestFlight or App Store | install app |
| Own Android app | Firebase project (+ Play Console to publish) | Android build with `google-services` | install app |
| Self-host with relay | none for iOS; ntfy-style relay | none | install relay's app |

The ntfy project shows the relay pattern: a self-hosted server forwards only a message
ID to the public ntfy service, which pushes via Firebase to APNs; the phone then fetches
the real message from the self-hosted server.[^ntfy-config] An open-source kit cannot
ship its own APNs credentials to every self-hoster, so a relay or an existing app is the
only practical native path.

# What the kit can take from it

- Do not build or publish native apps for the first version.
- If a native path is ever needed, borrow the relay design: push an opaque ID, fetch the
  content from the owner's server, keep secrets off the relay.
- Native push is the only way to get iOS time-sensitive or critical levels.

[^apple-remote]: Apple, Generating a remote notification, payload key reference.
[^apple-bg]: Apple, Pushing background updates.
[^apple-members]: Apple, Choosing a Membership.
[^fcm-v1]: Firebase, Migrate to HTTP v1.
[^ntfy-config]: ntfy configuration docs, iOS instant notifications.
