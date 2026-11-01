# This repo's board layer

Read after `.gtd/kit/BOARD.md`. Where this file differs from the kit, this file wins,
except that it can never relax the kit's rule 1 (board only through the gtd MCP server)
or rule 9 (hard limits), apart from the workflow grants rule 9 allows below. It lives in this repo, not in the public kit, so it is the place
for anything specific to this repo. Delete any section you don't need.

## Board and profile

- Profile: <!-- as in .github/gtd-context.json -->
- Board: <!-- owner/number -->
- Other boards or channels agents here may write to: <!-- e.g. a run-state channel -->
- Knowledge bundle: <!-- folder of this repo's OKF knowledge docs; default docs/knowledge/ -->
- The owner's `needs` value: <!-- the needs:* label that means "only the owner can unblock this" -->

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

## Fields and columns

<!-- Fields beyond the profile and who writes them; columns an agent must never set by hand. -->

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
     below once per lane, then lint with: python3 .gtd/kit/tools/lanes.py check -->

### lane: example-lane

- asked_by: <!-- the owner's handle: who approved this lane -->
- basis: <!-- one line: why this work may run without anyone pointing at each item -->
- grant: <!-- link to the owner's message, comment or PR that approved it -->
- policy: 1
- switch: observe
- item: <!-- owner/repo#n: the lane's own board item; its lease is the heartbeat -->
- queue: <!-- the board view whose card order is this lane's queue -->
- every: 1h
- lease: 3h
- may:
  - <!-- what a tick may do, one class of work per line -->
- never:
  - <!-- what a tick must never do, even inside may -->

## Workflow grants

<!-- Kit rule 9 forbids creating or editing .github/workflows/** unless a grant here, on
     the default branch, names the path. Agents still work on a branch, open a PR and never
     merge. Name each workflow file; a whole-folder grant is refused. With no grant here,
     the default stays "never". Copy the block below once per grant. -->

### grant: example-grant

- paths:
  - .github/workflows/<!-- file.yml -->
- granted_by: <!-- the owner's handle -->
- date: <!-- YYYY-MM-DD -->
- link: <!-- the owner's message, comment or PR -->
- also: <!-- optional: secrets, permissions or triggers the grant also allows; default none -->
