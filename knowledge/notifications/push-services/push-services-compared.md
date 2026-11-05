---
type: Research Finding
title: Push services compared
description: Side-by-side view of ntfy, Gotify, UnifiedPush, Pushover, Apprise, Sygnal and autopush for notifying one owner; the kit should reuse ntfy as its default channel and Apprise or Pushover as optional adapters rather than build a push server.
tags: [notifications, push, comparison, ntfy, pushover, unifiedpush, apprise]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: ntfy-config, title: "ntfy docs: Configuring the ntfy server", resource: "https://docs.ntfy.sh/config/", accessed: 2026-11-05}
  - {id: ntfy-publish, title: "ntfy docs: Publishing", resource: "https://docs.ntfy.sh/publish/", accessed: 2026-11-05}
  - {id: gotify-android, title: "gotify/android on GitHub", resource: "https://github.com/gotify/android", accessed: 2026-11-05}
  - {id: up-security, title: "UnifiedPush news: Push notifications, security and privacy (2025-05-13)", resource: "https://unifiedpush.org/news/", accessed: 2026-11-05}
  - {id: po-api, title: "Pushover: Message API", resource: "https://pushover.net/api", accessed: 2026-11-05}
  - {id: po-pricing, title: "Pushover: Pricing", resource: "https://pushover.net/pricing", accessed: 2026-11-05}
  - {id: apprise-repo, title: "caronc/apprise on GitHub (README)", resource: "https://github.com/caronc/apprise", accessed: 2026-11-05}
  - {id: mx-pgw, title: "Matrix Specification: Push Gateway API (v1.19)", resource: "https://spec.matrix.org/latest/push-gateway-api/", accessed: 2026-11-05}
  - {id: ap-http, title: "autopush-rs documentation: HTTP Endpoints", resource: "https://mozilla-services.github.io/autopush-rs/http.html", accessed: 2026-11-05}
---

# The table

| | [ntfy](ntfy.md) | [Gotify](gotify.md) | [UnifiedPush](unifiedpush.md) | [Pushover](pushover.md) | [Apprise](apprise.md) | [Sygnal](matrix-push-gateway-sygnal.md) | [autopush](mozilla-autopush.md) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kind | server + apps | server + app | protocol | hosted service | sender library | gateway | Web Push server |
| Self-host? | yes | yes | yes (server side) | no | yes | yes | yes, heavy |
| iOS? | yes, via ntfy.sh upstream relay[^ntfy-config] | no | no | yes, incl. critical alerts | via target | yes, own APNs key | via APNs bridge |
| Android without Google? | yes, kept-open connection[^ntfy-config] | yes[^gotify-android] | yes, its purpose | no (Play app) | via target | no | via Sunup |
| Desktop? | browser Web Push[^ntfy-config] | web UI | Linux (KUnifiedPush) | browser app[^po-pricing] | many targets | no | Firefox |
| Urgency | 5 levels[^ntfy-publish] | 0-10[^gotify-android] | Web Push hints | -2..2, emergency repeats until ack[^po-api] | maps to target | high/low[^mx-pgw] | TTL, Topic[^ap-http] |
| Ack / escalation | no | no | no | receipts + callback[^po-api] | no | no | no |
| Sender auth | user ACL + `tk_` token[^ntfy-config] | app token | VAPID (RFC 8292)[^up-security] | app token + user key[^po-api] | per-target URL secret[^apprise-repo] | none in spec[^mx-pgw] | VAPID[^ap-http] |
| Cost | free self-host; paid hosted tiers | free | free | 4.99 USD per platform once[^po-pricing] | free | free | free |
| Licence | Apache-2.0 / GPLv2 | MIT | spec + Apache-2.0 libs | proprietary | BSD-2-Clause | Apache-2.0 | MPL-2.0 |

# What a kit server could reuse

| Need | Reuse | Why |
| --- | --- | --- |
| Default phone + desktop channel | **ntfy** (ntfy.sh or self-hosted) | one POST, priority, click URL, action buttons, Android/iOS/web clients |
| Many other channels | **Apprise** URLs | one config string per target; no per-service code |
| "Must act now" on iOS | **Pushover** emergency priority | only option here with ack, retry, expiry and critical alerts |
| Browser-only owners | Web Push with VAPID | same wire format as UnifiedPush and autopush |
| Own phone app (later) | gateway split as in Sygnal | keeps APNs/FCM keys out of the kit runtime |

# Finding

No open option gives escalation and acknowledgement; only Pushover does. No
self-hosted option reaches iOS instantly without a vendor relay; ntfy borrows ntfy.sh.
So the kit should **not build a push server**. It should build a thin **notifier**:
decide when the owner must act, dedupe, and re-notify until the GitHub state changes.
It should send through ntfy by default and through Apprise or Pushover as options.

[^ntfy-config]: ntfy docs, Configuring the ntfy server.
[^ntfy-publish]: ntfy docs, Publishing.
[^gotify-android]: gotify/android README.
[^up-security]: UnifiedPush news, security and privacy, 2025-05-13.
[^po-api]: Pushover, Message API.
[^po-pricing]: Pushover, Pricing.
[^apprise-repo]: Apprise README on GitHub.
[^mx-pgw]: Matrix Specification, Push Gateway API.
[^ap-http]: autopush-rs docs, HTTP Endpoints.
