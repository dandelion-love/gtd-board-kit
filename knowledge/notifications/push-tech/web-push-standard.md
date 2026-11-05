---
type: Reference
title: Web Push standard
description: Web Push is three IETF RFCs (protocol, encryption, VAPID) plus the W3C Push API; any server with a key pair can send an encrypted message to a browser's push service without an account.
tags: [web-push, ietf, rfc8030, rfc8291, rfc8292, vapid, w3c]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: rfc8030, title: "RFC 8030: Generic Event Delivery Using HTTP Push", resource: "https://datatracker.ietf.org/doc/html/rfc8030", accessed: 2026-11-05}
  - {id: rfc8291, title: "RFC 8291: Message Encryption for Web Push", resource: "https://datatracker.ietf.org/doc/html/rfc8291", accessed: 2026-11-05}
  - {id: rfc8292, title: "RFC 8292: VAPID for Web Push", resource: "https://datatracker.ietf.org/doc/html/rfc8292", accessed: 2026-11-05}
  - {id: w3c-push, title: "W3C Push API, Working Draft", resource: "https://www.w3.org/TR/push-api/", accessed: 2026-11-05}
  - {id: ntfy-config, title: "ntfy docs: Configuration (Web Push section)", resource: "https://docs.ntfy.sh/config/", accessed: 2026-11-05}
---

# What it is

A browser subscribes to a **push service** run by its vendor (Google, Mozilla, Apple,
Microsoft). The subscription gives the app server an endpoint URL and two keys. The
server POSTs an encrypted message to that URL; the push service holds it and delivers
it to the browser, which wakes a service worker.[^w3c-push]

| Piece | Role |
| --- | --- |
| RFC 8030 (Dec 2016) | HTTP protocol between server, push service and user agent[^rfc8030] |
| RFC 8291 (Nov 2017) | end-to-end payload encryption; the push service cannot read it[^rfc8291] |
| RFC 8292 (Nov 2017) | VAPID: the server proves its identity with a signed JWT[^rfc8292] |
| W3C Push API | browser side: `subscribe()`, `push` event; a Working Draft dated 5 October 2026[^w3c-push] |

# Headers a sender sets (RFC 8030)

| Header | Meaning |
| --- | --- |
| `TTL` | required; seconds the push service keeps an undelivered message. `0` means deliver now or drop[^rfc8030] |
| `Urgency` | `very-low`, `low`, `normal` (default), `high`. `high` is meant for calls and time-sensitive alerts; a device may ignore lower urgencies to save battery[^rfc8030] |
| `Topic` | up to 32 base64url characters; a new message with the same topic **replaces** an undelivered one[^rfc8030] |
| `Prefer: respond-async` | asks for a delivery receipt[^rfc8030] |

# Encryption and identity

- Payload uses `aes128gcm` with ECDH on P-256 and a 16-byte auth secret from the
  subscription. One record only.[^rfc8291]
- Push services need only accept 4096 bytes, so plaintext tops out at 3993 bytes.[^rfc8291]
- VAPID: an ES256 JWT with `aud` (push service origin), `exp` (at most 24 hours ahead)
  and an optional `sub` contact URI, sent as `Authorization: vapid t=<jwt>, k=<key>`.[^rfc8292]
- The browser binds a subscription to the VAPID public key. Changing the key pair
  strands existing subscribers; ntfy warns against it for this reason.[^ntfy-config]

# Limits

- Delivery is best effort. The push service may shorten the TTL.[^rfc8030]
- The browser decides how the notification looks. The protocol has no "critical" level.
- `userVisibleOnly: true` promises every push shows a notification.[^w3c-push]

# 2026 status

Stable RFCs. The W3C draft is still moving, now with a declarative message format
(see `declarative-web-push.md`).[^w3c-push]

# What the kit can take from it

- No vendor account, no fee: a key pair and an HTTPS page are enough.
- Map "agent is blocked" to `Urgency: high` and a long TTL; "PR ready" to `normal`.
- Use `Topic` per board item so a newer state replaces an older one still queued at the
  push service. `Topic` never reaches the browser, so also set the same key as the
  notification `tag` to replace one already on screen.
- Keep payloads tiny (well under 3993 bytes): title, one line, a link.
- Generate the VAPID key once per deployment and never rotate it casually.

[^rfc8030]: RFC 8030, sections on TTL, Urgency, Topic and receipts.
[^rfc8291]: RFC 8291, Message Encryption for Web Push.
[^rfc8292]: RFC 8292, VAPID.
[^w3c-push]: W3C Push API Working Draft.
[^ntfy-config]: ntfy configuration docs, Web Push section.
