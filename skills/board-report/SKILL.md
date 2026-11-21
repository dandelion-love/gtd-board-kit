---
name: board-report
description: Report progress on a claimed board item, renew or release its claim, or record a failure, through the gtd MCP server. Use at each milestone of work on a claimed issue, before a lease runs out, when work stops for any reason, and when handing an item to someone else.
metadata:
  author: gtd-board-kit
  version: 0.10.0
---

# Report on a claimed item

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file's labels, columns and rules win over anything below. Only the holder reports a
state; check with `item_get(repo, number)` if unsure.

## The report

```
item_report(repo, number, state, note, links, project)
```

| state | When | Label change (`issue_labels`, with `profile`) |
| --- | --- | --- |
| `progress` | a milestone: a step done, a branch pushed, tests green | none |
| `waiting` | waiting on something outside (a run, a dependency, CI) | add `blocked` |
| `blocked` | cannot continue without an outside change | add `blocked` |
| `ready` | PR open, work returned | `waiting-for-review` in, `agent-running` out |
| `failed` | you tried and could not finish | `agent-failed` in, `agent-running` out |
| `dropped` | no longer worth doing (this releases the claim) | `agent-running` out |

- `note`: one or two plain lines: what happened, what is next. No secrets or pasted
  logs; link them.
- `links`: the PR, the run, the doc.
- At `ready`, also keep the evidence on the issue as
  `.gtd/kit/knowledge/model/evidence-places.md` says: a `link` artifact for the PR or a
  published doc, a `generic` one for a report (`issue_artifact_create`, when offered;
  a name has no `#` or `:`). Tick each criterion whose evidence passes, with a link to
  the proof on its line (a permalink at the head commit, plus `PR #n AC2 row`); leave a
  failing one empty with the reason. The `ready` note is for a person: what is
  delivered, the one action asked, what is not done, choices you made
  and their undo. The issue must speak for itself
  (`.gtd/kit/knowledge/model/self-reviewable-items.md`).
- **Name the successor.** A `ready` or closing report links the next item, `capture`s
  it, or says the leg ends.
- Remove `blocked` when you resume. Without `.github/workflows/project-sync.yml`, also
  set Status to the column `.gtd/BOARD.local.md` gives.
- A question for a person is not a state: use `board-needs-person`.
- **Waiting on a lane or its resource** (a run only a lane starts, a card a lane owns):
  `waiting` alone reaches nobody. Also `issue_comment` on that lane's item (its `item` in
  `.gtd/BOARD.local.md`): your item's link and what you wait for. The lane's next tick
  reads it in `activity_since` (`board-lane`) and answers there.

## New activity

At each tick, before each report and before you release: `activity_since(repo,
since=<the read_at you kept>)`. It lists what others wrote since then on items you hold,
PRs opened for you by `pr_open` (comments and reviews) and the repo's channels. Answer
each entry where it was written, or say in your next report why not. While
`has_next_page`, call again with `next_cursor` and the same `since`. Then keep
`read_at` (the same on every page); with none kept, omit `since` (last 24 hours) and skip what you already
answered. Skip only entries whose url your own writes returned. No such tool on the server: read each held
item's `follow_ups` (`item_get`) and each channel (`channel_comments_read`).

## Cadence

- Report at every milestone and at least once per lease.
- `item_renew(repo, number, lease, project)` before the lease ends if you still hold it.
  A standing lane's item is renewed every tick: its lease is the lane's heartbeat.
- When you stop, for any reason, end with `item_release(repo, number, done, left, decided,
  set_aside, next, handoff_to, project)`: the four-part closing note
  (`.gtd/kit/knowledge/model/report-vocabulary.md`): what is done, what is left, what you
  decided (each with its undo) and what you set aside. Write `none` for an empty part.
  On a server whose `item_release` schema has no `left`, pass `remaining` for it. `handoff_to` is a principal, a role, `any`, or omitted.
  An item left held by a session that has ended blocks everyone until the lease expires.
- **A stop.** `stop` in any `item_get`, `item_renew` or `item_report` result is the
  owner's request (`.gtd/kit/knowledge/model/stop-signal.md`): finish the current step,
  start nothing new, write the four parts and release, before `stop.wind_down_until`.
  Never ignore it; never clear it; the server will not take the claim from you.

## Queue order and ETA

The queue is the board's card order and the ETA is `Target date`; a person's edit wins.
Read `queue-and-fields.md` before you move a card, set a date or write a field.

## Long runs on compute hosts

If `.gtd/BOARD.local.md` names a run-state channel, a run also posts there:
`run_state_post(event=start | phase | end | hold | release | spend, host, by, …)`.
Report both the item and the run.

## Board-level reports

Only owners and coordinators post the board's status (`project_report`).
