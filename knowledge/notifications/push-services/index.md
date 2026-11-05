# Push services (prior art)

* [Apprise](apprise.md) - Apprise is a BSD-licensed Python library and CLI that sends one notification to many services through a URL per target (ntfy://, pover://, gotify://, json://), with an optional self-hosted HTTP API server
* [Gotify](gotify.md) - Gotify is a small MIT-licensed self-hosted server that takes messages over REST and pushes them to its Android app and web UI over a WebSocket; it has no iOS app
* [Matrix push gateway (Sygnal)](matrix-push-gateway-sygnal.md) - Matrix splits push into homeserver, push gateway and APNs/FCM; Sygnal is the reference gateway that holds the vendor credentials and turns one small notify call into platform pushes
* [Mozilla autopush](mozilla-autopush.md) - autopush-rs is Mozilla's MPL-licensed Rust Web Push server behind Firefox; it accepts RFC 8030 pushes over HTTP, keeps browsers on WebSockets, and bridges to APNs and FCM for mobile
* [ntfy](ntfy.md) - ntfy is a self-hostable HTTP pub-sub notification server with Android, iOS and web clients; a sender posts plain text to a topic URL and the phone shows it, with five priority levels and action buttons
* [Push services compared](push-services-compared.md) - Side-by-side view of ntfy, Gotify, UnifiedPush, Pushover, Apprise, Sygnal and autopush for notifying one owner; the kit should reuse ntfy as its default channel and Apprise or Pushover as optional adapters rather than build a push server
* [Pushover](pushover.md) - Pushover is a hosted, closed-source push service with apps for iOS, Android and desktop browsers; its emergency priority repeats until the user acknowledges, and its iOS app can send critical alerts that bypass mute
* [UnifiedPush](unifiedpush.md) - UnifiedPush is an open push protocol where the user picks the push server and on-device distributor; it now requires Web Push encryption (RFC 8291) and supports VAPID (RFC 8292), so an app server sends standard Web Push to any distributor
