---
type: Pattern
title: Backlog review
description: A named backlog owner role reviews open items by Priority and age on a stated cadence, started by hand, and the owner's promote, park or drop is recorded on the item with its date; the review never closes an idle item.
tags: [board, backlog, review]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-21T23:00:00Z }
---

# Rule

Without a review, work never leaves the backlog on purpose; it only ages. The review makes
leaving a decision somebody takes.

- **The role.** The **backlog owner** holds the review. Proposal: the board steward holds the
  role and a person decides each item. The role does the review, not the deciding.
- **The cadence.** Proposal: once a week. A repo may state another in its `BOARD.local.md`.
- **Started by hand.** The owner or the steward runs `backlog_review`. It is not a lane and
  has no scheduler entry. A scheduled run needs the owner's own grant, as any standing
  work does ([standing lanes](../decisions/standing-lanes.md)).
- **One digest.** `backlog_review` returns the open items grouped by Priority (`P0` to `P3`,
  then `unset`) and age, oldest first. An item with no Priority shows under `unset`; it is
  never dropped from the digest. See [priority levels](board-fields.md#priority-levels).
- **Watch first.** The review only records, in `would`, what it would change. It starts in
  this mode, and an acting mode waits until the owner has reviewed what watch recorded.
- **Three decisions.** The owner promotes, parks or drops an item, and `backlog_decide`
  records it on the item with the date. A decision changes nothing else: the owner sets
  the Priority, the label or the close.
- **Never closed by the review.** An idle item stays open until a person closes it.

# A digest

```json
{"mode": "watch", "counts": {"P0": 0, "P1": 1, "P2": 0, "P3": 0, "unset": 1},
 "digest": {"P1": [{"number": 12, "title": "Fix sign-in redirect", "priority": "P1", "age_days": 9,
                    "last_decision": null}],
            "unset": [{"number": 31, "title": "Tidy old wording", "priority": null, "age_days": 75,
                       "last_decision": null}]},
 "would": ["item 31 would ask for a Priority", "item 31 would ask the owner to promote, park or drop"]}
```

Empty groups are left out of `digest`. The tool pages are in the
[server spec](../../server-spec/tools.md#backlog-review).
