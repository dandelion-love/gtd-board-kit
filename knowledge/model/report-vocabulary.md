---
type: Pattern
title: Report vocabulary
description: A holder reports one of six states; anyone may raise a question for a person, which adds a needs label and stops the work.
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
