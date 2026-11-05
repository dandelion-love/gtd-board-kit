---
type: Reference
title: Mozilla autopush
description: autopush-rs is Mozilla's MPL-licensed Rust Web Push server behind Firefox; it accepts RFC 8030 pushes over HTTP, keeps browsers on WebSockets, and bridges to APNs and FCM for mobile.
tags: [notifications, push, web-push, mozilla, autopush, vapid, self-hosted]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: ap-repo, title: "mozilla-services/autopush-rs on GitHub", resource: "https://github.com/mozilla-services/autopush-rs", accessed: 2026-11-05}
  - {id: ap-docs, title: "autopush-rs documentation: Introduction", resource: "https://mozilla-services.github.io/autopush-rs/", accessed: 2026-11-05}
  - {id: ap-http, title: "autopush-rs documentation: HTTP Endpoints", resource: "https://mozilla-services.github.io/autopush-rs/http.html", accessed: 2026-11-05}
  - {id: up-distributors, title: "UnifiedPush: Distributors", resource: "https://unifiedpush.org/users/distributors/", accessed: 2026-11-05}
---

# What it is

"The fourth generation of the Mozilla Web Push server", in Rust; production serves
Firefox.[^ap-repo][^ap-docs] Licence: MPL-2.0.[^ap-docs] Two parts:[^ap-docs]

- `autoconnect`: WebSocket server for desktop browsers.
- `autoendpoint`: HTTP server for publishing and for mobile.

Storage examples ship for Bigtable and Redis (compose files).[^ap-repo] Full self-host
guidance was not reviewed here.

# How a sender posts

Standard Web Push (RFC 8030) to the subscription's `/wpush/...` endpoint.[^ap-docs][^ap-http]

- Headers seen: `TTL`, `Topic` (replaces an unread message with the same topic),
  `Authorization: Vapid ...`.[^ap-http]
- Payload up to 4096 bytes; about 2744 when bridged to FCM.[^ap-http]
- Returns 201 on success; 404 invalid and 410 gone mean drop the subscription.[^ap-http]
- With a VAPID key, the endpoint only accepts that app server; the claim needs a `sub`
  contact URI.[^ap-http]
- `Urgency` handling was not confirmed in the page read.

# How the device receives

- Firefox desktop: own WebSocket to autoconnect.[^ap-docs]
- Mobile: a bridge with `gcm`, `fcm` and `apns` types; the app registers its token and
  gets a Web Push endpoint back. Bridge records expire after 60 days without a
  daily-ish check-in.[^ap-http]
- Sunup, a UnifiedPush distributor for Android, uses autopush-rs as its server, and it
  can be self-hosted.[^up-distributors]

# Priority and iOS

Only Web Push hints (TTL, Topic; Urgency unconfirmed). No escalation. iOS reach is via
the APNs bridge, which needs the app owner's Apple credentials.

# 2026 status

Active (repo footer 2026; Mozilla runs it for Firefox).[^ap-repo] Releases not checked.

# What the kit can take from it

- Proof that one Web Push endpoint can front both a browser socket and APNs/FCM
  bridges; a kit server need not invent a protocol.
- `Topic` collapsing suits "PR ready" updates: a newer push replaces the older one.
- Too heavy to embed (Bigtable/Redis, two services). Reuse it indirectly through Sunup
  or browsers, not as the kit's own server.

[^ap-repo]: autopush-rs on GitHub.
[^ap-docs]: autopush-rs docs, Introduction.
[^ap-http]: autopush-rs docs, HTTP Endpoints.
[^up-distributors]: UnifiedPush, Distributors page.
