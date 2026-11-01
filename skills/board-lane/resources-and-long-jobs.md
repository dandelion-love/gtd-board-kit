# Long jobs, resources and board outages

Part of the `board-lane` skill. Read `.gtd/kit/BOARD.md` and the skill's `SKILL.md`
first. Optional lane keys used here: `resource`, `capacity`, `on_board_down`.

## Long jobs

- A tick never waits on a long job. Before starting it, `item_claim` (or keep) the work
  item it serves, then start the job and record it there:
  `item_report(state="waiting", note=…, links=…)`, add `blocked`. Say where its result
  and completion marker will be, and give the ETA (`board-report`, Queue order and ETA).
- Every tick renews the lease of each item whose job it started and whose marker is not
  there yet, so a 10-hour job on a 2-hour lease never looks abandoned. When the marker
  appears, remove `blocked`, report, and carry on with the item.
- A job is done only when its own completion marker or result file says so. An exit code
  of 0 alone proves nothing: background jobs (WSL ones in particular) can die with the
  session and still report 0. A job that has stopped with no marker is `failed`; say so.
- **Never restart or close a session while a lane's long job runs in it.** Set the lane
  to `hold` and let the job finish first. `hold` and `off` stop new starts; they never
  kill a running job.

## Resources

A lane that owns something only one job (or a few) can use at once names it:
`resource: <name>` and `capacity: <n>` (default 1). The lane's queue is then the
resource's queue.

- Start a job only while fewer than `capacity` of the lane's jobs are running.
- A person's direct ask that needs the resource jumps the queue: it starts at the next
  job boundary (when a running job ends), not by killing one, unless the person says to
  stop that job.
- When the job at the head slips, recompute Start and Target dates for the items behind
  it from the head's new ETA. A date a person set stands: report the conflict on that
  item instead of overwriting it.

## When the board is unreachable

Revalidation reads git, so it still runs. What happens next is the lane's
`on_board_down`:

- `hold` (the default): do nothing but check again next tick. Tell your person once.
- `continue`: keep doing local work inside `may`, under the last policy that validated.
  Start nothing that needs the board (no new claims, no new items). Queue each report
  you would have made, with its original time, and post them in order, times included,
  once the board is back; renew leases first.
