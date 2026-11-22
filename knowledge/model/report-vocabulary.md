---
type: Pattern
title: Report vocabulary
description: A holder reports one of six states and leaves a four-part closing note; anyone may raise a question for a person, which adds a needs label and stops the work.
tags: [board, reports]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T04:00:00Z }
---

# States

| State | Meaning |
| --- | --- |
| `progress` | a milestone was reached |
| `waiting` | waiting on something outside the item |
| `blocked` | cannot continue without an outside change |
| `ready` | work returned, usually as a PR |
| `failed` | tried and could not finish |
| `dropped` | no longer worth doing; releases the claim |

# Attention

A question only a person can answer is an `attention` on the report, with a `needs`
value saying whom it waits for. The server adds `needs:<value>`, the card moves to the
profile's needs-a-person column, and work on the item stops until the person answers.
Taking the label off is the person's call.

When a person answers, the question closes with a report that says which question it
answers (`answering`, the question's comment id) and quotes the answer with its time and
where it was said. The item then reads the Status it would have had without the question,
not "needs a person" until the holder reports again. The record is the reporter's quote,
not the person's own act, so it names where the person said it. The answer page records
the same thing for the person who answered there.

# Closing note

A release, and a report that closes a leg of work, carries four short parts, so the next
worker and the owner read what happened without the transcript:

| Part | Holds |
| --- | --- |
| `done` | what was finished, with links to the proof |
| `left` | what remains to do (the old release field `remaining` is the same part) |
| `decided` | choices made on the way, each with how to undo it |
| `set_aside` | what was considered and deliberately not done, and why |

Write all four. An empty part is written `none`, not left out: a reader then knows the
worker thought about it. A part you cannot fill is a decision to explain, not a gap. The
server accepts a release without them for now (with a warning naming what is missing) and
reads an absent part as `none`; with no note at all it reads `none recorded`. The next
worker reads them, and how often the item was interrupted, before working
([claims and leases](claims-and-leases.md)).
