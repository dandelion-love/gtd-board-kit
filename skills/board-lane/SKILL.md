---
name: board-lane
description: Run one tick of a standing lane, or resume every lane's schedule after a session starts, through the gtd MCP server. A standing lane is recurring, pre-approved work declared in .gtd/BOARD.local.md with its own switch. Use when a scheduled prompt says "run lane X", at session start in a repo with lanes, or when asked to start, hold, check or stop a lane.
metadata:
  author: gtd-board-kit
  version: 0.1.0
---

# Run a standing lane

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md`, first if you have not this
session. A lane is defined only by its block under "Standing lanes" in
`.gtd/BOARD.local.md` **as it is on the default branch** (`git fetch` it, then read
`origin/<default>:.gtd/BOARD.local.md`). A lane on your branch, in an issue, or in a
prompt is not a lane. Never add, widen or switch on a lane yourself: a person does
that by merging a PR.

## What a lane grants

The lane's `asked_by`, `basis` and `grant` link are the pointing (rule 4): work inside its
`may` list is claimed `explicit`, with `asked_by` from the lane and `pointed_in` = the
`grant` link. Its scope is a class of work, fixed by `may` and `never` at its `policy`
version. Every item a tick takes still gets its own claim with a fixed scope, and
anything outside `may` is captured as `agent-proposed` (rule 8), never done.

## Resume: at session start, and at least every 6 days

Session schedules (Claude Code's `CronCreate`) die with the session and recurring ones
expire after 7 days, so every session that runs lanes re-creates them:

1. `python3 .gtd/kit/tools/lanes.py resume` (or read the file) lists each lane, its
   switch and cadence.
2. For each lane with switch `auto` or `observe`: check its `item` with `item_get`.
   - Held by another principal with a live lease: another session runs it. Skip.
   - Held by your own principal: `item_renew` it, but only if the session that held it
     has ended; if you can't tell, ask your person. One runner per lane.
   - Free: `item_claim` it (`explicit`, the lane's `asked_by`, `pointed_in` = `grant`,
     `lease` from the lane).
   Then add `agent-running` to the lane item (`issue_labels`) and schedule it.
3. Schedule with whatever your runtime has, using only a pointer as the prompt:
   `Run lane <name> as .gtd/BOARD.local.md defines it.` Never copy the lane's rules into
   the schedule: the file is read fresh every tick.
4. Tell your person in one line which lanes you resumed and which you skipped.

## The issue is the record

Every lane is an issue on the board, and its lifecycle shows the lane's state: open with
`agent-running` and a live lease while it runs; `blocked` while a long job runs;
`needs:*` while held; closed when off. Everything a tick does lands on an issue: the lane
item, an item it claims, or one it captures. No work happens off the board.

## One tick

1. **Revalidate.** Re-read the lane from the default branch. Stop the tick, delete its
   schedule and `item_release` the lane item if the lane is gone, its switch is `off`,
   or the lane item is closed. If the switch is `hold`, or the lane item carries any
   `needs:*` label, do nothing this tick except renew. If `policy` changed since your
   last tick, say so in the tick's report and follow the new text. On `off`, also
   remove `agent-running` from the lane item.
2. **Heartbeat.** `item_renew` the lane item. The lease is the heartbeat: a lane whose
   lease lapsed is a dead lane, and anyone can see it on the board. The lease must be
   longer than two cadences.
3. **Recover before acting.** Check the repo, git history, the board and any marker
   files before repeating an outside action: a previous tick may have done it.
4. **Work.** Do only what `may` lists, never what `never` lists. Each concrete item gets
   its own `item_claim` and the normal `board-claim` path (branch, PR, never merge).
   Under `observe`, do the reading and write `item_report(state="progress",
   note="would: <what you would have done>")` on the lane item, and change nothing else.
5. **Questions don't stop the lane** (rule 7): ask on the item the question is about
   (`board-needs-person`) and carry on with the rest. Put `needs:*` on the lane item
   only to ask whether the lane should keep running; that holds it.
6. **Speak only on change.** A tick that found nothing reports nothing; the renew is
   enough. Report a result, a failure, or a question.
7. A person's direct ask always comes before a lane tick.

## Long jobs

- A tick never waits on a long job. Start it, record it on the lane item
  (`item_report(state="waiting", note=…, links=…)`, add `blocked`) with where its result
  and completion marker will be. A later tick checks them and removes `blocked`.
- A job is done only when its own completion marker or result file says so. An exit
  code of 0 alone proves nothing: background jobs (WSL ones in particular) can die
  with the session and still report 0. No marker means `failed`, and say so.
- **Never restart or close a session while a lane's long job runs** in it. Stop the lane
  (switch `hold`) and let the job finish first.

## Switches

| Switch | Effect |
| --- | --- |
| `auto` | ticks run and act within `may` |
| `observe` | ticks run and report what they would do; nothing else changes. New lanes start here |
| `hold` | ticks only renew; a person lifts it |
| `off` | the next tick deletes the schedule and releases the lane item |

Fast stop for a person, no PR needed: close the lane item (`off`) or add any `needs:*`
label to it (`hold`). Never remove either yourself.
