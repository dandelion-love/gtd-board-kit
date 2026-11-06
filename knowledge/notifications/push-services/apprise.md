---
type: Reference
title: Apprise
description: Apprise is a BSD-licensed Python library and CLI that sends one notification to many services through a URL per target (ntfy://, pover://, gotify://, json://), with an optional self-hosted HTTP API server.
tags: [notifications, apprise, adapters, python, fan-out]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: apprise-repo, title: "caronc/apprise on GitHub (README)", resource: "https://github.com/caronc/apprise", accessed: 2026-11-05}
  - {id: apprise-api, title: "caronc/apprise-api on GitHub (README)", resource: "https://github.com/caronc/apprise-api", accessed: 2026-11-05}
  - {id: apprise-ntfy, title: "Apprise wiki: Notify_ntfy", resource: "https://github.com/caronc/apprise/wiki/Notify_ntfy", accessed: 2026-11-05}
---

# What it is

A Python library and CLI that covers "almost all of the most popular notification
services": chat, SMS, email, desktop and generic JSON/XML/form webhooks.[^apprise-repo]
Licence: BSD-2-Clause.[^apprise-repo] It is not a push server; it is a sender-side
adapter layer.

# How a sender posts

Each target is one URL. Examples:[^apprise-repo]

| Target | URL |
| --- | --- |
| ntfy | `ntfy://topic/` or `ntfys://` |
| Pushover | `pover://user@token` |
| Gotify | `gotify://hostname/token` |
| Generic webhook | `json://hostname` |
| Apprise API server | `apprise://hostname/Token` |

- Python: `pip install apprise`; `Apprise()`, `.add(url)`, `.notify(body=..., title=...)`.[^apprise-repo]
- CLI: `apprise -t TITLE -b BODY URL...`, also reads stdin; `--attach` for files.[^apprise-repo]
- Config in YAML or text; **tags** select targets with OR or AND logic.[^apprise-repo]

Per-service options ride as query parameters. For ntfy: `priority`
(min..max), `tags`, `click`, and `token` or `auth=token`.[^apprise-ntfy]

# Apprise API (server)

A separate project wraps it in HTTP:[^apprise-api]

- `POST /notify/` stateless, with URLs in the request or an env var.
- `/add/{KEY}` saves a config; `/notify/{KEY}` sends through it, filtered by tag.
- `/status` health and `/metrics` Prometheus.
- Docker image for amd64, arm/v7, arm64. Licence: MIT.
- Auth is built in but **off by default** (`APPRISE_AUTH_REQUIRED=yes`, Basic Auth).

# Phone side, priority, iOS

Apprise does not deliver to phones itself; reach, priority and iOS behaviour are those
of each target service. It maps its own priority words to each service's scale.
The exact mapping per service was not checked here.

# 2026 status

Active; the release number and date were not confirmed in this pass.

# What the kit can take from it

- **Reuse it as the adapter layer** instead of writing per-service clients: the owner
  pastes one Apprise URL (ntfy, Pushover, Matrix, email, Slack...) into config.
- The URL-per-target idea suits a kit secret: one opaque string per channel.
- Tags map well to the kit's three event kinds (question, PR ready, stuck).
- Caveat: it adds a Python dependency, and escalation or acknowledgement is not part of
  its model; the kit would keep that logic.

[^apprise-repo]: Apprise README on GitHub.
[^apprise-api]: Apprise API README on GitHub.
[^apprise-ntfy]: Apprise wiki, ntfy page.
