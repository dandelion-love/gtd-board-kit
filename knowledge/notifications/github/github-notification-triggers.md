---
type: Reference
title: What makes GitHub notify a person
description: GitHub notifies a person when they take part in a thread, are mentioned, assigned or asked to review, or watch the repository; everything else, including board changes, reaches nobody.
tags: [github, notifications, mentions, review-requests]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: gh-about, title: "GitHub Docs: About notifications", resource: "https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications", accessed: 2026-11-05}
  - {id: gh-config, title: "GitHub Docs: Configuring notifications", resource: "https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/setting-up-notifications/configuring-notifications", accessed: 2026-11-05}
  - {id: dsh-deploy, title: "dsh-superagent-prototype: 006 Deployment", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs", file: 006-deployment.md, accessed: 2026-11-05, commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4}
---

# Two ways in

GitHub sends a notification for a **thread** (an issue, a pull request, a discussion) to
the people subscribed to it, and for a **repository** to the people watching it.

| You are subscribed to a thread when you | Inbox reason |
| --- | --- |
| open it, comment on it, or change its state (close, merge)[^gh-about] | `author`, `comment`, `state_change` |
| are @mentioned, or your team is[^gh-about] | `mention`, `team_mention` |
| are assigned to it[^gh-about] | `assign` |
| are asked to review the pull request | `review_requested` |
| click Subscribe on it[^gh-about] | `subscribed` |

Each inbox entry carries its reason as a label, and the inbox filters on it.[^gh-about]
Unsubscribing stops a thread until someone mentions you there again.[^gh-about]

# The levers an agent can pull

An agent writing to GitHub has only three ways to put something in front of a person:

1. **A new comment that @mentions them.** The cheapest, and it lands on the item. A
   mention added by *editing* an issue body does not arrive as a new mention; post a
   new comment instead.[^dsh-deploy]
2. **A review request** on a pull request. It has its own reason, so a person can keep
   a "review requested" filter.
3. **An assignment.** It notifies, but it also changes who the item belongs to, so it
   is a poor way to ask a question.

Labels, Status moves, field edits and closing a sub-issue notify nobody by themselves.
A `needs:*` label is a signal for views and filters, not a notification.

# What the kit can take from it

- An ask (the kit's `attention`) is one new comment with one @mention. That is the
  whole push.
- "PR ready" is a review request, never a separate comment.
- Everything else stays silent on GitHub and waits in the board's views.

[^gh-about]: GitHub Docs, About notifications.
[^dsh-deploy]: dsh-superagent 006 Deployment, Sources setting.
