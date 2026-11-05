---
name: board-lane
description: Run one tick of a standing lane, or resume every lane's schedule after a session starts, through the gtd MCP server. A lane is recurring, pre-approved work declared in .gtd/BOARD.local.md. Use when a scheduled prompt says "run lane X", at session start in a repo with lanes, or when asked to start, hold, check or stop a lane.
metadata:
  author: gtd-board-kit
  version: 0.5.1
---

# Run a standing lane

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md`, first if you have not this
session. A lane is defined only by its block under "Standing lanes" in
`.gtd/BOARD.local.md` **as it is on the default branch** (`git fetch` it, then read
`origin/<default>:.gtd/BOARD.local.md`); a lane anywhere else is not a lane. Never add,
widen or switch on a lane yourself: a person merges that.

## What a lane grants

The lane's `asked_by`, `basis` and `grant` link are the pointing (rule 4): work inside its
`may` list is claimed `explicit`, with `asked_by` from the lane and `pointed_in` = the
`grant` link. Its scope is a class of work, fixed by `may` and `never` at its `policy`
version. Every item a tick takes still gets its own claim with a fixed scope.

**Items a lane creates.** An item a tick creates for work inside `may` carries the
lane's mandate: its body names the lane, `asked_by`, the `grant` link, the lane item and
the `policy` version. The tick may claim it at once (`explicit`, as above). Anything outside `may` is captured as
`agent-proposed` (rule 8) and not done. Under `observe`, report "would create" instead.

## Resume: at session start, and at least every 6 days

Session schedules die with the session and expire after 7 days. The SessionStart hook
prints the resume list into every new session, so any session resumes:

1. `python3 .gtd/kit/tools/lanes.py resume` lists each lane, its switch and cadence.
2. For each lane with switch `auto`, `observe` or `hold` (held lanes keep renew-only
   ticks, so the heartbeat holds and a person's switch back is seen): check its `item`
   with `item_get`.
   - Held by another principal with a live lease: another session runs it. Skip.
   - Held by your own principal: `item_renew` it only if the session that held it has
     ended (can't tell: ask your person). One runner per lane.
   - Free: `item_claim` it (`explicit`, the lane's `asked_by`, `pointed_in` = `grant`,
     `lease` from the lane).
   Then add `agent-running` and `standing` to the lane item (`issue_labels`) and
   schedule it. `standing`: no ready check, and it stays open.
3. Schedule with whatever your runtime has, with only a pointer as the prompt:
   `Run lane <name> as .gtd/BOARD.local.md defines it.` Never copy the rules in.
4. Tell your person in one line which lanes you resumed and which you skipped.

## The issue is the record

Every lane is an issue: open with `agent-running` and a live lease while it runs;
`blocked` while a long job runs; `needs:*` while held; closed when off. Everything a tick
does lands on an issue.

## One tick

1. **Revalidate.** Re-read the lane from the default branch (git, so it works while the
   board is down: see `on_board_down` in `resources-and-long-jobs.md`). Stop the tick, delete its
   schedule and `item_release` the lane item if the lane is gone, its switch is `off`,
   or the lane item is closed. If the switch is `hold`, or the lane item carries any
   `needs:*` label, do nothing this tick except renew. If `policy` changed since your
   last tick, say so in the tick's report and follow the new text. On `off`, also
   remove `agent-running` from the lane item.
2. **Read, then heartbeat.** `activity_since` (`board-report`, New activity): an entry
   on the lane item is a hand-off from an item waiting on it: answer it there or take
   it on (claim or `capture`). Answer the rest where written. Renew the lane item, and each item whose long
   job it started that has no marker yet, only when under two cadences of lease remain.
   The lease is the heartbeat (`resources-and-long-jobs.md`, Lane item size).
3. **Recover before acting.** Check the repo, git history, the board and any marker
   files before repeating an outside action: a previous tick may have done it.
4. **Work.** Take items in the order of the lane's `queue` view and keep their ETA
   (`board-report`, Queue order and ETA). Do only what `may` lists, never `never`. Each concrete item gets
   its own `item_claim` and the normal `board-claim` path (branch, PR, no merge without a merge grant).
   Under `observe`, read, then `item_report(state="progress", note="would: <what>")` on
   the lane item, and change nothing else.
5. **Questions don't stop the lane** (rule 7): ask on the item the question is about
   (`board-needs-person`) and carry on with the rest. Put `needs:*` on the lane item
   only to ask whether the lane should keep running; that holds it.
6. **Speak only on change.** A tick that found nothing reports nothing.
7. A person's direct ask comes before a tick; with a `resource` it jumps the
   queue (`resources-and-long-jobs.md`).

## Long jobs, resources, board outages, intake

Read `intake.md` for an intake lane or a request filed to another project. Read `resources-and-long-jobs.md` before a lane starts a long job, owns a `resource`,
or finds the board down. In short: a tick never waits on a job; a job is
done only when its own marker says so, never on exit 0 alone; and **never restart or
close a session while a lane's long job runs** in it.

## Switches

| Switch | Effect |
| --- | --- |
| `auto` | ticks run and act within `may` |
| `observe` | ticks report what they would do and change nothing. New lanes start here |
| `hold` | ticks only renew; no new job starts, a running one runs on; a person lifts it |
| `off` | no new job starts; the next tick with no running job deletes the schedule and releases the lane item |

Fast stop for a person, no PR: close the lane item (`off`) or add any `needs:*` label
(`hold`). Never undo either yourself.
