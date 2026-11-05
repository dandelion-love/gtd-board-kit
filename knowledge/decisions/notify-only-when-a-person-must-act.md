---
type: Decision
title: Notify a person only when they must act
description: A push goes to a person only for an ask, a pull request ready for review or work that cannot finish, through GitHub's own mention or review request; everything else, new issues included, waits in views; a repo may add a louder Web Push channel for asks.
tags: [notifications, attention, needs, decision]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T05:00:00Z }
---

# Context

The owner of a board is one busy person, often away from a desk. Agents create asks
(`needs:*`), pull requests and new issues all day. GitHub's Projects send no
notifications, so a card in a "needs owner" column reaches nobody until someone opens the
view ([GitHub's gaps](/notifications/github/github-notification-gaps.md)). Owners asked
to hear about new issues and asks on their phone.

The research ([notifications](/notifications/)) points one way: every notification costs
attention and must be worth more than that
([dsh-superagent](/notifications/design/dsh-superagent-when-to-speak.md),
[attention budget](/decomposition/human-gates/attention-budget.md)); batch what can wait
([batching](/decomposition/human-gates/batching-and-one-question-at-a-time.md)); keep the
record in the system of record and make any push a copy that points at it.

# Decision

1. **Three reasons to push, no others.** An ask (`item_report` with `attention`), a pull
   request ready for review, and work that cannot finish (`blocked` or `failed` that
   needs a person). Never a start, progress, a retry, a renew, a healthy state or an
   explanation.
2. **GitHub carries the push.** An ask's record @mentions the person the repo maps to
   that `needs` value; a ready PR requests that person's review. One push per ask; push
   again only when the ask itself changes.
3. **New issues are not pushed.** They wait in the board's Inbox or triage view, which the
   owner reads in a sitting. A repo may opt in to a daily digest (one comment on a pinned
   item) or tell its owner to watch Custom → Issues.
4. **A louder channel is optional and per repo.** For owners who miss ordinary pushes, a
   repo may name a channel that copies asks only. The kit's reference channel is
   **Web Push** (RFC 8030 with RFC 8291 encryption and VAPID, RFC 8292) in the
   Declarative Web Push shape: one sender reaches browsers, home-screen web apps on iOS
   and Android, and UnifiedPush apps, with no app-store or vendor account
   ([push technology](/notifications/push-tech/push-tech-choice-2026.md)). An ntfy topic
   or Pushover are accepted adapters: ntfy when the owner wants its app, Pushover when an
   ask must repeat until acknowledged
   ([push services](/notifications/push-services/push-services-compared.md)).
5. **The record never moves.** The ask lives on the item. A push carries a one-line
   summary and the item's link, nothing private beyond what the item shows, and losing a
   push loses nothing.
6. **What a louder push carries.** A title, one sentence (at most 100 words), the item's
   link as the tap target, the reason (`ask`, `review`, `stopped`), `Urgency: high` for
   an ask or a stop and `normal` for a review, and the item plus reason as its `Topic` so
   a newer push replaces an unread one. No token, secret or private text beyond what the
   item shows.
7. **Actions only open or defer.** The tap opens the item. Where buttons exist, the kit's
   set is **Open**, **Snooze** (remind at the next sitting) and **Answer**, which opens a
   signed-in page. Picking an option, approving, merging, granting or "not me" never
   happen from a lock screen or a blind tap: they go through a signed-in page with a
   fresh check, and the answer lands on the item as a comment
   ([notification actions](/notifications/push-tech/notification-actions.md)).
8. **At most one reminder.** An ask still open at the owner's next sitting may be pushed
   once more; after that it waits in the needs-me view. Only an adapter the owner chose
   for escalation (Pushover) repeats until acknowledged.
9. **Repo specifics stay in the repo.** Who each `needs` value means, the louder channel
   and the new-issue mode go in `.gtd/BOARD.local.md` under "Notifications".

# Consequences

- Requests from other projects are intake, not pushes
  ([intake and acks](/decisions/intake-and-acks.md)); an overdue one becomes a
  `needs:*` ask on the filer's item, and only then pings.
- Agents gain no new tool: an ask's `attention` text carries the mention today.
- A server can do better later, as server-spec work with its own conformance checks:
  `item_report` adds the mention itself from the repo's map (so agents cannot forget or
  repeat it), `pr_open` requests the owner's review, and an optional notifier sends the
  Web Push copy with `Urgency: high` and the item as its `Topic`, so a re-ask replaces
  the old notification instead of stacking.
- Two tiers only: GitHub's ordinary push, and the repo's louder channel for asks.
  Escalation exists only through an adapter the owner chose; quiet hours belong to the
  phone (Focus, Do Not Disturb, GitHub Mobile working hours), not the kit.
- A reference notifier (sender, subscribe page, signed-in answer page) is a separate
  story; the kit owns its contract, a deployment owns its keys.
- The weekly count of pushes is the measure. If it rises, cut pushes first.
