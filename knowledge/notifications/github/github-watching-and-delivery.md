---
type: Reference
title: GitHub watching, delivery and the inbox
description: How a person chooses which repositories reach them (watch levels, Custom), and where notifications land (web inbox, email, GitHub Mobile push with working hours).
tags: [github, notifications, mobile, email, watching]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: gh-config, title: "GitHub Docs: Configuring notifications", resource: "https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/setting-up-notifications/configuring-notifications", accessed: 2026-11-05}
  - {id: gh-about, title: "GitHub Docs: About notifications", resource: "https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications", accessed: 2026-11-05}
---

# Watch levels per repository

| Level | What arrives |
| --- | --- |
| Participating and @mentions | only threads you take part in, are mentioned, assigned or asked to review in |
| All activity | every thread in the repository |
| Custom | participating and @mentions, plus every thread of the types you pick: Issues, Pull requests, Releases, Discussions, Security alerts[^gh-config] |
| Ignore | nothing, not even mentions[^gh-config] |

Custom → Issues covers "every issue (including those that existed prior to you
selecting this option)", so it is the native way to hear about every new issue, and
about every comment on every issue too.[^gh-config] You automatically watch repositories
you create under your personal account; that can be turned off.[^gh-about]

# Where they land

| Channel | Notes |
| --- | --- |
| Web inbox | The record. Reasons, filters, Saved (kept), Done; unsaved entries are kept three months[^gh-about] |
| Email | To a verified address; an organisation can route its notifications to a different address[^gh-config] |
| GitHub Mobile | Syncs with the web inbox. Push for direct mentions, assignments, review requests and deployment approvals, each switchable; optional working hours[^gh-config] |

A GitHub Mobile push is an ordinary notification: one banner, no repeat, no
escalation, no Do Not Disturb bypass. It sits in the phone's list beside every other
app's.

# What the kit can take from it

- Recommended person setup: watch work repos at **Participating and @mentions**; turn on
  Mobile push for mentions and review requests; keep inbox filters `reason:mention` and
  `reason:review-requested` as the "needs me" inbox.
- "Every new issue on my phone" is a per-repo opt-in (Custom → Issues), noisy on busy
  repos. The kit should not need it: new issues wait in the board's Inbox view.
- When an ask must be louder than a GitHub push, it needs another channel
  ([push technology](/notifications/push-tech/)).

[^gh-config]: GitHub Docs, Configuring notifications.
[^gh-about]: GitHub Docs, About notifications.
