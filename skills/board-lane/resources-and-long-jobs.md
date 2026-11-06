# Long jobs, resources and board outages

Part of the `board-lane` skill. Read `.gtd/kit/BOARD.md` and the skill's `SKILL.md`
first. Optional lane keys used here: `resource`, `capacity`, `epics`, `on_board_down`.

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
  `capacity` counts this lane's jobs only. If anything else can use the resource (a
  person, another lane), the repo names a `busy_check`: a command in the repo that exits
  0 when the resource is free. Run it before each start and start nothing on non-zero.
- A person's direct ask that needs the resource jumps the queue: it starts at the next
  job boundary (when a running job ends), not by killing one, unless the person says to
  stop that job.
- **An idle resource is a question, not an answer.** The lane's `queue` shows only what
  someone already put there, so an empty queue does not prove there is nothing to run.
  A tick that finds the resource idle reads the open items under the epics the lane
  serves (`epics: [owner/repo#n, ...]`; with none, the parents of the items the lane has
  worked) and names, for each one, its next step and what triggers it. An open item
  with neither is a defect: write it up in that tick (`capture` it, or report it on the
  item) instead of reporting the idle as correct. A second idle tick in a row lists the
  items it checked, so a person can see the idle was looked at, not assumed.
- When the job at the head slips, recompute Start and Target dates for the items behind
  it from the head's new ETA. A date a person set stands: report the conflict on that
  item instead of overwriting it.

## When the board is unreachable

Revalidation reads git, so it still runs. What happens next is the lane's
`on_board_down`:

- `hold` (the default): do nothing but check again next tick. Tell your person once.
- `continue`: finish what is running and keep doing local work on items you already
  hold, inside `may`, under the last policy that validated. It starts no new item: no
  new claims, no new items, no new job from the queue, so the resource may idle once the
  running job ends. That is deliberate: a claim the board never recorded could collide
  with another holder. Queue each report
  you would have made, with its original time, and post them in order, times included,
  once the board is back; renew leases first.

## Lane item size

Every renew and report is a comment on the lane item, and a lane runs for weeks. An
hourly renew alone is 24 comments a day, and the item becomes slow to read and fold.

- **Renew only when less than two cadences of the lease remain.** With `every: 1h` and
  `lease: 26h`, that is about one renew a day. The cost: a dead lane shows as a lapsed
  lease up to a day later. A lane whose death must show sooner keeps a shorter lease.
- **Report only on change** (`SKILL.md`, step 6). A quiet tick writes nothing.
- **Roll over at 300 comments.** Open a successor lane item with the same body and
  `standing`, and open a PR that points the lane's `item` at it. Keep ticking on the old
  item until that PR is on the default branch: closing it earlier would stop the lane
  (step 1). Once merged, the next tick claims the successor, `item_release`s the old item
  with `next` naming the successor, and closes it.
