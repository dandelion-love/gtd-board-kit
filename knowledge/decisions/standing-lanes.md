---
type: Decision
title: Standing lanes are written rules a person switches on
description: Recurring, pre-approved work is declared per repo as a lane with who asked, why, a grant link, a policy version, a switch and may/never lists; a lane counts as pointing.
tags: [lanes, authorization, scheduling]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T06:30:00Z }
---

# Context

Some work recurs: a nightly check, a queue to drain, a run to watch. Pointing an agent at
each instance wastes a person's attention, and an agent that takes unpointed work with no
written rule is the clearest prompt-injection risk on a board. Session schedules are also
fragile: a schedule made inside a session dies with it, and recurring ones expire.

# Decision

- A **standing lane** is a block under "Standing lanes" in the repo's
  `.gtd/BOARD.local.md`, with `asked_by`, `basis`, a `grant` link to the owner's
  approval, a `policy` version, a `switch`, its own board `item`, a cadence, a lease,
  and `may` / `never` lists. It counts only on the default branch, so only a person's
  merge creates, widens or switches one on.
- In the terms of an agent desk's accept rules, a lane is a written rule in mode
  `auto` whose scope is a class of work. Work inside `may` is claimed `explicit` with the
  lane's `asked_by` and its `grant` as `pointed_in` (kit rule 4). **Scope stays fixed**
  on two levels: the lane fixes the class at its policy version, and each claim fixes
  its item. Widening the class is a new policy version a person merges.
- Switches: `auto`, `observe` (report what it would do, change nothing), `hold`, `off`.
  `observe` is the default for a new class of work. A person may merge a lane straight
  at `auto` when its `grant` links an approval that predates the lane and the PR says so.
- Items a lane creates inside `may` carry the lane's mandate and may be claimed in the
  same tick, so a lane that owns a resource never idles on its own output.
- A lane may own a `resource` with a `capacity`; a person's direct ask jumps its queue at
  the next job boundary. When the resource is idle, a tick reads the open items under
  the lane's `epics` for next steps before it calls the idle correct. `on_board_down` (`hold` by default, or `continue`) says what
  a tick does when the board is unreachable. A person stops a lane fast, with no PR, by closing its item
  (`off`) or adding any `needs:*` label to it (`hold`).
- Every tick revalidates the lane from the default branch before acting, so an edit takes
  effect at the next tick and a removed lane stops.
- Questions raised in a lane go on the item they are about; the lane keeps running
  (kit rule 7). Only a question on the lane's own item holds it.
- Scheduled prompts are pointers ("Run lane X as .gtd/BOARD.local.md defines it"), never
  copies of the rules. A resume step (`board-lane`, optionally a SessionStart hook
  running `tools/lanes.py resume`) re-creates schedules after a restart.
- The lane item's **lease is the heartbeat**, renewed every tick and longer than two
  cadences, so a dead lane is visible on the board without a separate monitor.
- Long jobs are checked by their own completion marker, never by exit code alone, and a
  session is never restarted while a lane's long job runs in it.

# Consequences

- Lanes need a board item each, and a person reads `observe` reports before moving a
  lane to `auto`.
- Two sessions under one principal could both resume a lane; the skill makes the second
  ask its person when it can't tell the first has ended.
- The design borrows from [dsh-superagent](/references/dsh-superagent.md): accept
  modes, revalidation against a policy version, the recovery check, and speaking only on
  change.

See [claims and leases](/model/claims-and-leases.md) and
[the per-repo layer](/decisions/per-repo-layer.md).
