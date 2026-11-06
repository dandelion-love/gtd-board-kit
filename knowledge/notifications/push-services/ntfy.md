---
type: Reference
title: ntfy
description: ntfy is a self-hostable HTTP pub-sub notification server with Android, iOS and web clients; a sender posts plain text to a topic URL and the phone shows it, with five priority levels and action buttons.
tags: [notifications, push, self-hosted, ntfy, unifiedpush, web-push]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: ntfy-repo, title: "ntfy on GitHub (README)", resource: "https://github.com/binwiederhier/ntfy", accessed: 2026-11-05}
  - {id: ntfy-publish, title: "ntfy docs: Publishing", resource: "https://docs.ntfy.sh/publish/", accessed: 2026-11-05}
  - {id: ntfy-config, title: "ntfy docs: Configuring the ntfy server", resource: "https://docs.ntfy.sh/config/", accessed: 2026-11-05}
  - {id: ntfy-issues, title: "ntfy docs: Known issues", resource: "https://docs.ntfy.sh/known-issues/", accessed: 2026-11-05}
  - {id: ntfy-releases, title: "ntfy docs: Release notes", resource: "https://docs.ntfy.sh/releases/", accessed: 2026-11-05}
---

# What it is

ntfy ("notify") is a simple HTTP pub-sub service. You "send push notifications to
your phone or desktop using PUT/POST".[^ntfy-repo] It is open source, dual licensed
Apache 2.0 and GPLv2.[^ntfy-repo] A public instance runs at ntfy.sh, with paid plans
from about 5 USD a month; you can also self-host it.[^ntfy-repo]

# How a sender posts

- `PUT` or `POST` a body to `https://<server>/<topic>`. Topics appear on first use.[^ntfy-publish]
- Headers set `Title`, `Priority`, `Tags`, `Click`, `Attach`, `Icon`, `Actions`, `Markdown`.[^ntfy-publish]
- Up to three action buttons: `view` (open URL), `http` (send a request), `broadcast`
  (Android intent), `copy`.[^ntfy-publish]
- Auth: users with ACLs per topic pattern, and access tokens that start with `tk_`.
  The default is open read-write; the docs advise `auth-default-access: deny-all` for a
  private server.[^ntfy-config] Tokens are sent as an `Authorization` header (Bearer);
  the exact header form was not re-read in this pass.

# How the phone receives

| Client | Path |
| --- | --- |
| Android, ntfy.sh | Firebase (FCM)[^ntfy-config] |
| Android, self-hosted | "instant delivery", FCM not involved (a kept-open connection)[^ntfy-config] |
| iOS, self-hosted | server sends a poll request with only the message ID to an upstream (ntfy.sh), which relays via Firebase/APNs; the phone then fetches the message from your server[^ntfy-config] |
| Browser | Web Push with VAPID keys (`web-push-public-key`), HTTPS required[^ntfy-config] |

Without `upstream-base-url`, iOS delivery "can take hours".[^ntfy-config] If the phone
cannot reach your server, iOS shows the placeholder "New message".[^ntfy-issues]

# Priority and urgency

Five levels: 1 min, 2 low, 3 default, 4 high, 5 max/urgent. On Android, max gives
"Really long vibration bursts ... with a pop-over notification".[^ntfy-publish] There is
no built-in repeat-until-acknowledged.

# iOS limits

- Instant iOS delivery from a self-hosted server depends on ntfy.sh as upstream.[^ntfy-config]
- Known issues list notifications not arriving and the app view not refreshing.[^ntfy-issues]
- Safari web push is silent.[^ntfy-issues]

# 2026 status

Active. Server v2.37.2 (3 Nov 2026); iOS app v1.7.0 (30 May 2026).[^ntfy-releases]
2026 added updating and deleting notifications (v2.16.0), PostgreSQL (v2.18.0) and
experimental clustering (v2.30.0, "not production-ready").[^ntfy-releases] ntfy is also
the default UnifiedPush distributor (see [UnifiedPush](unifiedpush.md)).

# What the kit can take from it

- The **send contract**: one HTTP POST, title + body + priority + click URL + action
  buttons. A kit notifier can target this shape directly.
- Reuse rather than build: a self-hosted ntfy (or ntfy.sh with a token and a
  `deny-all` default) covers Android, desktop browser and, via upstream, iOS.
- Action buttons (`view` to the PR, `http` to an answer endpoint) fit "answer the
  agent's question" flows.
- Gap: no escalation or acknowledgement; the kit must add re-notify logic itself.

[^ntfy-repo]: ntfy README on GitHub.
[^ntfy-publish]: ntfy docs, Publishing.
[^ntfy-config]: ntfy docs, Configuring the ntfy server.
[^ntfy-issues]: ntfy docs, Known issues.
[^ntfy-releases]: ntfy docs, Release notes.
