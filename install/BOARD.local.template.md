# This repo's board layer

Read after `.gtd/kit/BOARD.md`. Where this file differs from the kit, this file wins,
except that it can never relax the kit's rule 1 (board only through the gtd MCP server)
or rule 9 (hard limits), apart from the workflow and merge grants rule 9 allows below. It lives in this repo, not in the public kit, so it is the place
for anything specific to this repo. Delete any section you don't need.

## Board and profile

- Profile: <!-- as in .github/gtd-context.json -->
- Board: <!-- owner/number -->
- Other boards or channels agents here may write to: <!-- e.g. a run-state channel -->
- Knowledge bundle: <!-- folder of this repo's OKF knowledge docs; default docs/knowledge/ -->
- The owner's `needs` value: <!-- the needs:* label that means "only the owner can unblock this" -->
- Standing chore item: <!-- owner/repo#n: a Chore issue agents claim for work with no issue of its own (register lines, upkeep), so pr_open can land it; label it `standing` -->

## Notifications

<!-- Kit rule 7 and knowledge/decisions/notify-only-when-a-person-must-act.md: a person is
     pinged only for an ask, a PR ready for review or work that cannot finish. Who each
     `needs` value pings lives in .github/gtd-context.json under "notify" (the server reads
     it there; see .gtd/kit/server-spec/notifications.md):
       "notify": {"mentions": {"<owner needs value>": "<login>"}, "push": "none", "new_issues": "view"}
     A server with notify_get posts the one ping itself, under its App ([bot]), never as the
     person. Without it, the ask's attention text carries the mention, and only works when
     records are not written as that person: say here if they are. -->

- Pinged for asks: <!-- @login, as in gtd-context.json notify.mentions -->
- Louder channel: none <!-- none | web-push; see knowledge/notifications/ -->
- New issues: view <!-- view (default: they wait in the Inbox view) | digest (one comment a day on the standing chore item) | watch (the owner sets Watch > Custom > Issues) -->

## Labels this repo adds or uses differently

| Label | Meaning here | What an agent does with it |
| --- | --- | --- |
| | | |

## Status per label (only if this repo has no label-to-Status bridge)

| Label | Status column |
| --- | --- |
| agent-running | |
| waiting-for-review | |
| blocked | |
| <!-- the owner's needs:* label --> | <!-- its own column, e.g. Needs owner; not Blocked (see knowledge/model/board-fields.md) --> |

## Fields and columns

<!-- The kit's standard fields and their writers are in .gtd/kit/knowledge/model/board-fields.md.
     Here: renamed or extra fields and who writes them; columns an agent must never set by hand. -->

## Queue and ETA

<!-- The kit's meaning: the queue is the card order of a view with no sort; the ETA is a
     date field a person may overwrite, and then theirs wins. Name the concrete ones here. -->

- Queue view: <!-- view name; each lane may name its own with queue: -->
- ETA field: Target date
- Start field: Start date

## What agents may pick up here

<!-- Tighten or loosen the kit's pickup rule, e.g. which item types an agent may pull. -->

## Procedure differences

<!-- Steps that replace or add to the kit skills. For a bigger change, put a repo-owned
     skill in .claude/skills/<name>/ (a real folder, not a link); one with a kit skill's
     name replaces it. -->

## Standing lanes

<!-- Recurring, pre-approved work (kit skill board-lane). A lane counts only once it is on
     the default branch: a person adds, widens or switches one on by merging a PR. New lanes
     start at switch: observe. Bump policy on every change to a lane. Fast stop, no PR:
     close the lane's item (off) or add any needs:* label to it (hold). Copy the block
     below once per lane, then lint with: python3 .gtd/kit/tools/lanes.py check
     Blocks named example-* are placeholders: lanes.py skips them, so they never lint,
     run or grant anything. Rename a copy to use it. Label the lane's item `standing`. -->

### lane: example-lane

- asked_by: <!-- the owner's handle: who approved this lane -->
- basis: <!-- one line: why this work may run without anyone pointing at each item -->
- grant: <!-- link to the owner's message, comment or PR that approved it -->
- policy: 1
- switch: observe
- item: <!-- owner/repo#n: the lane's own board item; its lease is the heartbeat -->
- queue: <!-- the board view whose card order is this lane's queue -->
- resource: <!-- optional: what only this lane's jobs use, e.g. a machine; delete if none -->
- capacity: <!-- optional, with resource: how many jobs at once; default 1 -->
- busy_check: <!-- optional, with resource: a repo command that exits 0 when it is free -->
- epics: <!-- optional, with resource: the epics it serves (owner/repo#n, ...), read for next steps when it is idle -->
- on_board_down: hold
- every: 1h
- lease: 26h
- may:
  - <!-- what a tick may do, one class of work per line -->
- never:
  - <!-- what a tick must never do, even inside may -->

## Intake

<!-- Where other projects file requests to this repo, and where this repo files its own
     (kit skill board-lane, intake.md). A request is an open issue with the label; it
     stays agent-proposed until a person decides. Delete this section if unused. -->

- label: agent-proposed
- ack_within: 24h
- owner_needs: <!-- the needs value that reaches this repo's owner, e.g. the profile's owner_needs -->

### Files to

<!-- One line per project this repo files requests to: owner/repo, its label, its
     ack_within. Your own lane watches each request filed there for its ack. -->

## Workflow grants

<!-- Kit rule 9 forbids creating or editing .github/workflows/** unless a grant here, on
     the default branch, names the path. Agents still work on a branch and open a PR; a
     workflow file is never under a merge grant. Name each workflow file; a whole-folder grant is refused. With no grant here,
     the default stays "never". Copy the block below once per grant. -->

### grant: example-grant

- paths:
  - .github/workflows/<!-- file.yml -->
- granted_by: <!-- the owner's handle -->
- date: <!-- YYYY-MM-DD -->
- link: <!-- the owner's message, comment or PR -->
- also: <!-- optional: secrets, permissions or triggers the grant also allows; default none -->

## Merge grants

<!-- Kit rule 9 forbids an agent merging unless ONE grant here, on the default branch,
     names every file the PR changes (knowledge/model/grants.md). Name exact files, never
     a folder or pattern; nothing under .github/ or .gtd/ can be granted. With no grant
     here, the default stays "never merge". Copy the block below once per grant. -->

### merge: example-merge

- paths:
  - <!-- an exact file, e.g. a register an agent appends to -->
- granted_by: <!-- the owner's handle -->
- date: <!-- YYYY-MM-DD -->
- link: <!-- the owner's message, comment or PR -->
- also: <!-- optional: extra conditions, e.g. "only PRs opened with pr_open"; default none -->
