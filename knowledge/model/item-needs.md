---
type: Pattern
title: Item needs
description: A story declares the graphics memory, tools and longest run a machine needs, and anything left out means it runs anywhere; a Size supplies the default longest run.
tags: [board, matching, needs]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-22T08:00:00Z }
---

# Rule

An item that cannot say what it needs can land on a machine that cannot finish it. A story
says so in a `## Needs` section of its body, with up to three lines: `Graphics memory` (GB),
`Tools` (names) and `Longest run` (a number and a unit). Nothing declared means the item
runs anywhere, and nothing is ever hidden or refused for lacking a declaration.

- **Default run from Size.** With no `Longest run` the board Size gives one: `XS` 15 minutes,
  `S` 1 hour, `M` 4 hours, `L` 1 day, `XL` 3 days. This is a proposal; change the table in a
  pull request.
- **Invalid needs are refused when written.** A body whose section has a value that is not
  a number or a tool name is refused by the server on `issue_update` and `issue_create`, and
  the refusal names the value.
- **Read back.** `item_get` returns `needs`, including `runs_anywhere`.
- **Matching is a later story.** Offering an agent only the items its machine can finish
  waits for the machine card; this page only says how an item states its needs.

The exact grammar, the reply shape and the check (R12) are in the
[server spec](../../server-spec/tools.md#claims-and-reports).
