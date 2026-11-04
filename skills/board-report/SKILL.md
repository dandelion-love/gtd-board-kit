---
name: board-report
description: Report progress on a claimed board item, renew or release its claim, or record a failure, through the gtd MCP server. Use at each milestone of work on a claimed issue, before a lease runs out, when work stops for any reason, and when handing an item to someone else.
metadata:
  author: gtd-board-kit
  version: 0.7.0
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

- `note`: one or two plain lines on what happened and what comes next. No secrets,
  no pasted logs; link them.
- `links`: the PR, the run, the doc.
- At `ready`, also keep the evidence on the issue as
  `.gtd/kit/knowledge/model/evidence-places.md` says: a `link` artifact for the PR or a
  published doc, a `generic` one for a report (`issue_artifact_create`, when offered).
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
`has_next_page`, call again with `next_cursor` and the same `since`. Then keep the last
page's `read_at`; with none kept, omit `since` (last 24 hours) and skip what you already
answered. Skip only entries whose url your own writes returned. No such tool on the server: read each held
item's `follow_ups` (`item_get`) and each channel (`channel_comments_read`).

## Cadence

- Report at every milestone and at least once per lease.
- `item_renew(repo, number, lease, project)` before the lease ends if you still hold it.
  A standing lane's item is renewed every tick: its lease is the lane's heartbeat.
- When you stop, for any reason, end with `item_release(repo, number, done, remaining,
  next, handoff_to, project)`. `handoff_to` is a principal, a role, `any`, or omitted.
  An item left held by a session that has ended blocks everyone until the lease expires.

## Queue order and ETA

Both are native board constructs, so a person changes them in the GitHub UI or API and
you follow on your next read. `.gtd/BOARD.local.md` names the view and fields; the
defaults are below.

- **Queue:** the card order in the queue view (a view with no sort, since a sort hides
  manual order). `project_items` returns items in board order; take the first one you
  may claim. Move a card only to put work you capture or hand back where the repo says,
  with `project_item_move`; never reorder what a person ordered.
- **ETA:** the `Target date` field (start: `Start date`), set with
  `project_set_field(field="Target date", value="YYYY-MM-DD")`. Put the same date in
  the `item_report` note. Before changing it, read it with `project_item_find`: if it
  differs from the date you last reported, a person set it. Keep theirs, and if you
  can't make it, say so in a report instead of moving it.
- **Order between items:** native blocked-by links (`issue_blocked_by_list`), never a
  note in the body.
- **Other fields:** `.gtd/kit/knowledge/model/board-fields.md` says who writes each
  field and when. Waiting on a person's gate: `Gates` names it and the report note is
  the one-line ask; once it passes, update `Gates` and clear the `needs:*` label.
- **Sync-owned fields:** a field a profile sync `owns` (`profile_get`; in ml-lab an
  experiment's Agent, Start date and Last report) is written by the sync from its
  register. Never set it by hand, not even for an ETA or a note: record the event
  (`experiment_record`) and let the sync write the card. A Status stuck after a run
  ended means its register event or PR never landed: land it, never move the card.

## Long runs on compute hosts

If `.gtd/BOARD.local.md` names a run-state channel, a run also posts there:
`run_state_post(event=start | phase | end | hold | release | spend, host, by, …)`.
Report the item and the run; one does not replace the other.

## Board-level reports

Owners and coordinators can post the board's status update with `project_report`
(computed health). An agent working one item does not.
