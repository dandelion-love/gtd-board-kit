---
type: Decision
title: Titles and summaries say what an item delivers
description: Every epic and story title is a verb-first outcome in plain words of 25 to 72 characters with no prefix, subtitle, list or code; every body opens with a short summary of who it helps and what changes; mechanical failures make a story not ready, and writes return warnings, never refusals.
tags: [contract, work-items, writing, readiness]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-13T18:30:00Z }
---

# Context

A board is read by people skimming a list of titles. Titles such as "Part 3: a handoff to a
principal nobody holds surfaces" read like an episode name: they hint at a mechanism and
hide what the item delivers, so every reader opens the item to find out. Bodies that open
with where an item came from ("Part of the epic, gap 2") do the same one level down. The
[titles and summaries research](/decomposition/agile-foundations/titles-and-summaries.md)
shows what the common methods ask for instead.

# Decision

## Titles (epics and stories)

1. **Verb first, one outcome.** An imperative verb, then what a person or agent gains:
   "Show agents the items handed to them that nobody has picked up". Epics too: "Notify the
   owner only when they must act".
2. **No prefix.** Not "Epic:", "Story:", "Server:", "Part 3:" or "[docs]". Kind is the issue
   type, the layer is the repo or a label, and the order is the epic's Stories table.
3. **Outcome, not mechanism.** No tool, function, file, field or label names, no issue
   numbers, no dates.
4. **One outcome.** No subtitle (colon, semicolon, spaced dash, arrow) and no list of three
   or more. An "and" asks whether it is two items.
5. **25 to 72 characters**, so it fits a board card and a list without cutting.
6. **Plain words.** Board terms everyone uses (claim, Size, Status, epic) are fine; words
   only the spec uses are not.

## Bodies

7. **Summary first.** One to three sentences, under 400 characters, before any heading: who
   it helps, what is wrong or missing today, and what they can do once it closes. A story may
   use the job-story form ("When <situation>, <who> can <outcome>, so <benefit>."); it is
   optional, the three facts are not. A chore states its outcome plainly; never
   "As a developer, I want ...".
8. **Provenance last.** Parent epic, origin, evidence links, revisions and approvals go under
   `## Context` at the end. The native parent link already shows the epic.
9. **An epic's summary is its hypothesis**: "For <who>, <outcome>. Today <problem>.", then
   `## Problem` and `## Outcome check`.

## Checks

10. The [prose check](../../server-spec/prose-check.md) fixes which rules are mechanical
    (**fail**) and which are hints for a reviewer (**warn**). A story that fails one is not
    ready: the [ready check](../../server-spec/ready-check.md) gains a `prose` rule.
11. Nothing refuses a write for prose. `capture`, `issue_update` and `organize` return
    `prose_warnings`, and `prose_check` checks a draft before it is written.
12. `board-decompose` writes to this standard, and `board-review` reports each prose finding
    with a suggested rewrite.

# Consequences

- Existing stories with prefixed titles or provenance-first bodies read as
  `needs-refinement` until rewritten. Each repo rewrites its open items when it moves its
  kit pin.
- A verb list cannot tell every verb from a noun, so the verb rule only warns.
