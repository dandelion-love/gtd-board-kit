---
type: Research Finding
title: What GitHub never notifies
description: Board changes, your own actions, mentions added by edit and anything below a phone's normal notification level never reach a person through GitHub; a kit that relies on GitHub alone must design around these gaps.
tags: [github, notifications, projects, gaps]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: gh-config, title: "GitHub Docs: Configuring notifications", resource: "https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/setting-up-notifications/configuring-notifications", accessed: 2026-11-05}
  - {id: gh-proj-auto, title: "GitHub Docs: Using the built-in automations", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations", accessed: 2026-11-05}
  - {id: dsh-deploy, title: "dsh-superagent-prototype: 006 Deployment", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs", file: 006-deployment.md, accessed: 2026-11-05, commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4}
---

# The gaps

| Gap | Effect on a board kit |
| --- | --- |
| **Projects send no notifications.** No one can watch a board; a Status, field or order change alerts nobody. Built-in project workflows only set fields, add or archive items.[^gh-proj-auto] | A card in "Needs owner" is invisible until someone opens the view |
| **Your own actions do not notify you.** Email of your own updates is an opt-in setting; the inbox and Mobile push skip them.[^gh-config] | An ask posted under the owner's own account reaches nobody. Agents must write under their own identity |
| **A mention added by editing** a body does not arrive as a new mention.[^dsh-deploy] | Always post a new comment to ask |
| **No urgency.** Every GitHub push is the same ordinary banner | A blocking ask and a routine review look alike on the phone |
| **No acknowledgement.** GitHub cannot tell the sender whether the person saw it | Nothing to escalate on; the record must stay on the item |
| **Watch is all or by type.** Custom → Issues brings every issue and every comment on them[^gh-config] | "New issues only" needs a filter or a bridge |

# What the kit can take from it

- Pair every board state that needs a person with a GitHub act that notifies: the
  `needs:*` label with one mention comment; ready for review with a review request.
- The comment on the item is the record. Any louder channel is a copy that points at it,
  so a lost or ignored push never loses the ask.
- Urgency, acknowledgement and quiet hours are outside GitHub. If the kit wants them,
  it needs its own notifier ([push technology](/notifications/push-tech/), [push services](/notifications/push-services/)).

[^gh-config]: GitHub Docs, Configuring notifications.
[^gh-proj-auto]: GitHub Docs, Projects built-in automations.
[^dsh-deploy]: dsh-superagent 006 Deployment.
