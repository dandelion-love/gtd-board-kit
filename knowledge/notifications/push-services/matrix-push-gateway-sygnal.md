---
type: Reference
title: Matrix push gateway (Sygnal)
description: Matrix splits push into homeserver, push gateway and APNs/FCM; Sygnal is the reference gateway that holds the vendor credentials and turns one small notify call into platform pushes.
tags: [notifications, push, matrix, sygnal, apns, fcm, architecture]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: mx-pgw, title: "Matrix Specification: Push Gateway API (v1.19)", resource: "https://spec.matrix.org/latest/push-gateway-api/", accessed: 2026-11-05}
  - {id: sygnal-repo, title: "Sygnal on GitHub (README)", resource: "https://github.com/matrix-org/sygnal", accessed: 2026-11-05}
  - {id: up-defs, title: "UnifiedPush spec: Definitions", resource: "https://unifiedpush.org/developers/spec/definitions/", accessed: 2026-11-05}
---

# The split

The homeserver forwards event info to a **push gateway**; the gateway sends to a push
provider such as APNs or GCM/FCM; the provider delivers to the device.[^mx-pgw]

```
app server  ->  push gateway  ->  APNs / FCM  ->  phone app
(knows events)  (holds vendor keys)  (vendor)
```

Why: only whoever ships the phone app holds its APNs key or FCM service account. The
app server stays generic and never needs those secrets. UnifiedPush uses the same
term for the same role.[^up-defs]

# The notify call

- One required endpoint: `POST /_matrix/push/v1/notify`.[^mx-pgw]
- Body: a `notification` with `devices` (each with `app_id`, `pushkey`, `data`), and
  optional `event_id`, `room_id`, `sender`, `content`, `counts`.[^mx-pgw]
- `prio`: `high` (default) or `low`, so gateways can save battery.[^mx-pgw]
- `event_id_only` format sends just ids and counts; the app then fetches the content
  itself, which keeps message text away from Apple and Google.[^mx-pgw]
- The response lists `rejected` pushkeys; the homeserver must remove them.[^mx-pgw]
- Retry with exponential backoff; dedupe by `event_id`.[^mx-pgw]
- The spec marks the endpoint "Requires authentication: No".[^mx-pgw]

# Sygnal

The reference gateway. Licence Apache-2.0. Built by the Matrix.org Foundation
2019-2025; Element now maintains it.[^sygnal-repo] A YAML file lists `apps:` keyed by
`app_id`; each is `apns` (certificate or token auth with key id, team id, topic) or
`gcm` (FCM API v1 with a service account).[^sygnal-repo] Web Push support is not
mentioned in the README.[^sygnal-repo] Latest release not confirmed here.

# iOS and urgency

iOS works because the gateway owner holds an APNs key for their own app. Urgency is a
two-level hint (`high`/`low`); there is no repeat or acknowledgement.

# What the kit can take from it

- If the kit ever ships its own phone app, keep the same split: kit runtime sends a
  tiny notify call; a separate gateway holds APNs/FCM keys.
- Copy the **ids-only payload** idea: push "issue N needs you" plus a link, and let
  the app or browser fetch details from GitHub; secrets and code never transit vendors.
- Copy `rejected` keys and backoff rules for stale devices.
- Do not copy the unauthenticated endpoint; a public kit server needs a sender token.

[^mx-pgw]: Matrix Specification, Push Gateway API.
[^sygnal-repo]: Sygnal README on GitHub.
[^up-defs]: UnifiedPush spec, Definitions.
