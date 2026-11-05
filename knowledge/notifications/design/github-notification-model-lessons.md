---
type: Reference
title: GitHub notification model lessons
description: Design lessons only from GitHub's subscription model, where every notification carries a reason and the inbox offers done, save, unsubscribe and custom filters; the mechanics are covered on a separate page.
tags: [notifications, github, inbox, reasons, filters, prior-art]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: gh-about-notif, title: "GitHub Docs: About notifications", resource: "https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications", accessed: 2026-11-05}
---

# What it is

GitHub notifies people about repositories, issues and pull requests. Another page in
this research set covers the mechanics in depth. This page keeps only the design ideas.

# Mechanisms in brief

- **Two ways in.** You are subscribed to a thread by acting in it (commenting, being
  assigned, being mentioned), or you **watch** a whole repository.[^gh-about-notif]
- **Every notification has a reason**, such as `mention`, `subscribed` or
  `review requested`, and you can filter on it, for example
  `reason:review-requested`.[^gh-about-notif]
- **Triage verbs**: **Done** removes an item, **Save** flags it, **Unsubscribe** stops
  the thread (a new mention brings you back).[^gh-about-notif]
- **Custom filters** let you focus the inbox on one project or on mentions only.[^gh-about-notif]
- Unsaved notifications are kept for three months.[^gh-about-notif]

# Design lessons

| Lesson | Why it matters |
| --- | --- |
| Reason is metadata, not prose | a filter on reason beats reading every item |
| Participating beats watching | watching a busy repo floods the inbox; participation is narrow |
| Unsubscribe with a mention escape hatch | quiet by default, still reachable by name |
| Done is not resolved | clearing the inbox does not change the underlying issue |

# What the kit can take from it

- Tag every ask with a machine-readable **reason**, such as `approval`, `decision`,
  `blocked` or `review`. Pushes and digests can then be filtered and tiered by reason.
- A `review requested` reason already exists and owners already filter on it. If an agent
  hands back a PR, request the owner's review so it shows up there.
- Keep the owner off "watching" for agent repos. Address them only through assignment,
  review requests and mentions.
- Expect the owner to triage GitHub mail with filters. Use a stable, predictable title
  prefix so the filters work.

[^gh-about-notif]: GitHub Docs, About notifications.
