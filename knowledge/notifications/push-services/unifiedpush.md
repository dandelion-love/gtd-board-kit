---
type: Reference
title: UnifiedPush
description: UnifiedPush is an open push protocol where the user picks the push server and on-device distributor; it now requires Web Push encryption (RFC 8291) and supports VAPID (RFC 8292), so an app server sends standard Web Push to any distributor.
tags: [notifications, push, unifiedpush, web-push, vapid, android, linux]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: up-home, title: "UnifiedPush home page", resource: "https://unifiedpush.org/", accessed: 2026-11-05}
  - {id: up-defs, title: "UnifiedPush spec: Definitions", resource: "https://unifiedpush.org/developers/spec/definitions/", accessed: 2026-11-05}
  - {id: up-distributors, title: "UnifiedPush: Distributors", resource: "https://unifiedpush.org/users/distributors/", accessed: 2026-11-05}
  - {id: up-security, title: "UnifiedPush news: Push notifications, security and privacy (2025-05-13)", resource: "https://unifiedpush.org/news/", accessed: 2026-11-05}
  - {id: up-triangle, title: "UnifiedPush news: Different ways to receive notifications (2026-09-24)", resource: "https://unifiedpush.org/news/", accessed: 2026-11-05}
  - {id: up-flutter, title: "pub.dev: unifiedpush (Flutter)", resource: "https://pub.dev/packages/unifiedpush", accessed: 2026-11-05}
  - {id: rfc8030, title: "RFC 8030: Generic Event Delivery Using HTTP Push", resource: "https://www.rfc-editor.org/rfc/rfc8030", accessed: 2026-11-05}
---

# What it is

A decentralized push system: the user chooses the push service, it can be
self-hosted, and messages are encrypted.[^up-home] It replaces "send via Google FCM"
with "send to whatever endpoint the user's distributor gave you".

# Roles

| Role | Example |
| --- | --- |
| Application server | sends notifications (e.g. Synapse)[^up-defs] |
| Push gateway (optional) | converts or proxies to the push server[^up-defs] |
| Push server | receives messages, forwards to the distributor (e.g. ntfy server)[^up-defs] |
| Distributor | on-device app holding the connection (e.g. ntfy app)[^up-defs] |
| Connector library | inside the end-user app; registers with the distributor[^up-defs] |
| Endpoint | per-app URL, the Web Push concept from RFC 8030[^up-defs][^rfc8030] |

# Alignment with Web Push

- The app sends its endpoint, a public key and an auth secret to its server; the server
  encrypts per RFC 8291. Messages not encrypted correctly are rejected by the app, so the
  push server cannot forge them.[^up-security]
- Push servers are expected to support VAPID (RFC 8292); distributors may require it, so
  a leaked endpoint alone cannot send.[^up-security]
- So one Web Push sender library (as used for browsers) can also reach UnifiedPush phones.
- Not confirmed here: the exact spec version that made encryption mandatory. A
  2026-01-08 retrospective on F-Droid's blog states the specs were updated to require
  RFC 8291 and handle VAPID (not linked: its URL has date-only path segments).

# Distributors (2026)

| Distributor | Platform | Push server |
| --- | --- | --- |
| ntfy | Android | ntfy server, self-hostable[^up-distributors] |
| Sunup | Android | Mozilla autopush-rs, self-hostable[^up-distributors] |
| NextPush | Android | Nextcloud app, self-hosted only[^up-distributors] |
| Conversations | Android | XMPP account + rewrite proxy[^up-distributors] |
| KUnifiedPush (KDE) | Linux | ntfy, Gotify, autopush-rs or NextPush[^up-distributors] |
| gCompat-UP | Android | Google, mainly for development[^up-distributors] |

# Libraries

Flutter `unifiedpush` 6.2.0 (13 Oct 2025, Apache-2.0) supports Android and Linux,
decrypts RFC 8291 messages itself, and takes an optional VAPID public key at
registration.[^up-flutter] An Android connector library exists[^up-defs]; its current
version was not confirmed here.

# Priority and iOS

UnifiedPush adds no priority scale of its own beyond what Web Push carries; urgency
handling was not confirmed in these pages. There is **no iOS distributor**: iOS apps
must use APNs. The project's 2026 note frames the trade-off as a triangle: instant,
efficient, standalone, pick two; push is instant and efficient but needs a third-party
push service.[^up-triangle]

# What the kit can take from it

- Treat "Web Push endpoint + keys + VAPID" as the one wire format. A kit server that
  speaks RFC 8030, 8291 and 8292 reaches browsers, ntfy, Sunup and NextPush alike.
- Follow its server hygiene list: reject private-IP endpoints, do not follow redirects,
  send a validation push first, drop subscriptions on 404, batch sends.[^up-security]
- iOS still needs a separate APNs path (or a relay such as ntfy.sh upstream).

[^up-home]: UnifiedPush home page.
[^up-defs]: UnifiedPush spec, Definitions.
[^up-distributors]: UnifiedPush, Distributors page.
[^up-security]: UnifiedPush news, Push notifications, security and privacy, 2025-05-13.
[^up-triangle]: UnifiedPush news, Different ways to receive notifications, 2026-09-24.
[^up-flutter]: pub.dev, unifiedpush package page.
[^rfc8030]: RFC 8030, Generic Event Delivery Using HTTP Push.
