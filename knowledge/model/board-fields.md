---
type: Pattern
title: Board fields and who writes them
description: Every standard board field has a writer and a moment; an agent that creates, plans, claims or reports an item fills its fields then, and a card waiting on a person says which gate and what is asked.
tags: [board, fields, gates]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-03T15:10:00Z }
---

# Rule

A field left empty reads as "nobody knows". Each standard field below has one writer and
one moment. Write it then, through the server (`project_set_field`); never through a
token or GraphQL. A field the board does not have is skipped without comment. The
profile names the fields; `.gtd/BOARD.local.md` may rename one or add its own, and says
who writes those.

| Field | Holds | Written by | When |
| --- | --- | --- | --- |
| `Epic` | the parent epic as `#n`; on an epic, its own number, so a view grouped by Epic shows the epic with its stories | the agent that links it | `board-decompose` step 5, or whenever a parent changes |
| `Size` | XS to XL; an epic is the size of its whole plan (usually L or XL) | an agent suggests once | when it creates or plans the item |
| `Priority` | one of `P0`, `P1`, `P2`, `P3` ([levels](#priority-levels)) | a person; an agent may suggest once, into an empty field, from a date or a stated deadline, and says so in its report | when it creates or plans the item |
| `Lane` | the batch the work rides: the integration branch's short name, e.g. `pitch` for `rc/pitch`; `(person)` for an item only a person works | the session that plans or orchestrates the batch | when it plans the batch or first claims an item for it |
| `Owns` | the paths the item's PR will change, taken from its acceptance criteria; an epic names its folder | the agent that writes the item | `board-decompose` step 5 |
| `Gates` | which [human gates](/decomposition/human-gates/minimum-gate-set-solo-owner.md) apply and which one is open, e.g. `G1 open: add agent-ready to approve the plan` or `G2, G4` | the agent that plans the item; whoever sees a gate pass | at planning, and when a gate passes |
| `Agent` | who holds the item | the server's mirror | on every claim, renew and release |
| `Last report` | the latest report word and note | the server's mirror | on every `item_report` |
| `Start date` | the day work started (an epic: the day its plan was approved) | the agent | its first claim of the item |
| `Target date` | the ETA | the agent; a person's date wins ([queue and ETA](queue-and-eta.md)) | when it can commit to one, and in the report note |

A person's value always wins: read a field before changing it, and never overwrite one
you did not write.

# Priority levels

Four levels, each with one meaning, so two people (or an agent and a person) reading `P1`
mean the same thing. Lower is more urgent. The set is closed: a board's `Priority` options
are exactly these four, and a server accepts exactly these four.

| Level | Meaning | Example |
| --- | --- | --- |
| `P0` | Drop other work: something is broken for users now, or a hard deadline passes today. | a release is down and users cannot sign in |
| `P1` | Do next: needed this week, or it blocks other planned work. | a fix a launch on Friday depends on |
| `P2` | Normal: do it in board order, with no date pressure. | a planned feature with no deadline |
| `P3` | When idle: worth keeping, never worth interrupting other work. | a tidy-up of old wording |

An item with no `Priority` is unranked, not `P2`: pickup treats it after `P3`.

**Who may set a level.** A person: the board's owner, or someone the owner named in the
profile. An agent may **suggest** a level once, only when the field is empty, from a date
or a stated deadline in the item, and says so in its report (`Priority suggested: P1,
because the item names a Friday deadline`). A suggestion is not a decision: a person
confirms it by leaving it, or changes it. An agent never overwrites a value that is
already set, whoever set it, and never suggests twice on one item; a refusal for that
reason says the field is set.

**A level outside the four is refused.** The refusal lists the allowed levels
(`P0, P1, P2, P3`). Writing `P4`, `p1 ` or `high` changes nothing. Existing boards keep
working: a board that has only `P1` to `P3` accepts them unchanged, and adding `P0` to
its options is a person's change to the board.

# A card waiting on a person

When the only thing in the way is a person (a gate such as plan approval, or a question
with `needs:<who>`), the card must say so without a click:

- `Gates` names the open gate, and `Last report` holds the one-line ask, e.g.
  `waiting: plan approval (G1). Add agent-ready to this epic, or comment changes`.
- A profile should give the owner's `needs:*` label its own Status column, such as
  `Needs owner`, kept apart from `Blocked`. `Blocked` means an open blocker link;
  mixing the two hides which items a person can unblock in one click.
- When the gate passes (the person adds `agent-ready` to the epic, or answers), the next
  agent to touch the item clears the `needs:*` label if the person has not, updates
  `Gates` and `Last report`, and moves the card on.

# Closed is Done

Closing an issue, or merging the PR that closes it, is the decision; the Status column only
records it. So something must move a closed item out of the open columns, and it must be
named, or closed items sit in In Review and In Progress for good:

- **A repo with a sync that owns Status on close** (`project-sync.yml` with a profile map,
  which may use its own closed columns such as Abandoned): the sync writes it.
- **Any other repo: the server's bot.** The server's GitHub App receives the `issues`
  closed and `pull_request` closed (merged) events and sets each board's Status to the
  profile's closed column (`Done` by default), as the App, within a minute. A pull request
  closed without merging changes nothing. A periodic sweep on the same App records the
  closed column for any closed item still in an open column, so a lost event is caught.
- The board's built-in Item closed and Pull request merged workflows are optional. Free
  plans limit how many a board may have, and GitHub has no API to set them, so the kit does
  not rely on them. Where a sync owns close they stay off, so the two never fight.
- An agent that finds a closed item outside a closed column, on a repo the server's bot
  serves, records the profile's closed column once with `project_set_status` (the close
  already happened, so this only writes it down) and reports the gap. On a repo whose sync
  owns close, it leaves the column to the sync and reports the gap instead. It never sets a
  closed column on an open item.

# Why

Board views group and filter by these fields (Epic rollup, In flight by Lane, Needs a
person). An item that skips them falls out of every view built on them, and the
person sees empty boxes instead of the state.
