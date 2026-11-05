---
type: Reference
title: Gotify
description: Gotify is a small MIT-licensed self-hosted server that takes messages over REST and pushes them to its Android app and web UI over a WebSocket; it has no iOS app.
tags: [notifications, push, self-hosted, gotify, websocket]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: gotify-docs, title: "Gotify docs: Intro", resource: "https://gotify.net/docs/", accessed: 2026-11-05}
  - {id: gotify-push, title: "Gotify docs: Push messages", resource: "https://gotify.net/docs/pushmsg", accessed: 2026-11-05}
  - {id: gotify-extras, title: "Gotify docs: Message extras", resource: "https://gotify.net/docs/msgextras", accessed: 2026-11-05}
  - {id: gotify-server, title: "gotify/server on GitHub", resource: "https://github.com/gotify/server", accessed: 2026-11-05}
  - {id: gotify-android, title: "gotify/android on GitHub", resource: "https://github.com/gotify/android", accessed: 2026-11-05}
  - {id: up-distributors, title: "UnifiedPush: Distributors", resource: "https://unifiedpush.org/users/distributors/", accessed: 2026-11-05}
---

# What it is

"A simple server for sending and receiving messages in real-time per
WebSocket", with a web UI.[^gotify-server] Licence: MIT.[^gotify-server] Written in Go.

Its model has two token kinds: **applications** can only send; **clients** can only
receive and manage.[^gotify-docs] That split is a clean least-privilege pattern.

# How a sender posts

`POST /message` with the app token in the `X-Gotify-Key` header. Fields: `message`
(required), `title`, `priority`, `extras`.[^gotify-push] Tokens are shown only once, at
creation or rotation.[^gotify-push]

Extras (JSON only) add behaviour:[^gotify-extras]

- `client::display` `contentType: text/markdown`
- `client::notification` `click.url` (open a link on tap) and `bigImageUrl`
- `android::action` `onReceive.intentUrl`

# How the phone receives

The Android app holds a connection to the server; a persistent notification shows its
status.[^gotify-android] The server delivers over WebSocket.[^gotify-server] No FCM is
involved, so it works on phones without Google services, at a battery cost.
There is no official iOS client; neither repo mentions one.[^gotify-server][^gotify-android]

# Priority

Android maps priority to style:[^gotify-android]

| Priority | Effect |
| --- | --- |
| 0 | no notification |
| 1-3 | icon in the bar |
| 4-7 | icon and sound |
| 8-10 | icon, sound and vibration |

No repeat, no acknowledgement, no critical-alert path.

# 2026 status

Maintained; the docs show 2.x Android features (bigImageUrl from v2.3.0).[^gotify-extras]
The latest release number and date were not confirmed in this pass. KUnifiedPush on
Linux can use a Gotify server.[^up-distributors]

# What the kit can take from it

- The **send-only vs receive-only token split**: an agent gets a send token that cannot
  read history; the owner's devices get receive tokens.
- Priority as a number the client maps to sound and vibration.
- Not a fit as the kit's main path: no iOS, and Android relies on a kept-open socket.

[^gotify-docs]: Gotify docs, Intro.
[^gotify-push]: Gotify docs, Push messages.
[^gotify-extras]: Gotify docs, Message extras.
[^gotify-server]: gotify/server README.
[^gotify-android]: gotify/android README.
[^up-distributors]: UnifiedPush, Distributors page.
