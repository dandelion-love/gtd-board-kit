---
name: board-claim
description: Claim a board item, work it on a gtd/issue-N branch and hand it back as a PR, keeping the board current through the gtd MCP server. Use when starting work on a GitHub issue in a repo that has gtd-board-kit, whether you were pointed at it or picked it with board-pickup.
metadata:
  author: gtd-board-kit
  version: 0.2.0
---

# Claim an item and work it

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file's labels, columns and rules win over anything below. `repo`, `profile` and
`project` come from `.github/gtd-context.json` and the origin remote (see `board-pickup`).

## 1. Claim before touching anything

```
item_claim(repo, number, basis, asked_by, pointed_in, lease="2h", project)
```

- `explicit`: you were pointed at it. `asked_by` is who pointed you (your person's
  handle, `coordinator`, a thread); `pointed_in` links the message or comment if you have one.
- `inferred`: an unpointed `agent-ready` pull. The server refuses unless the board Size is
  XS, S or M and no `agent:<x>` names someone else. **On that refusal, do not retry as
  `explicit`** unless someone really did point you at it: pick another item or ask.
- Refused because someone holds it: leave it. Never take over a live lease.
- Pick a lease that covers the work, at most 72h; you will renew (`board-report`).

## 2. Show it on the board

1. `issue_labels(number, add=["agent-running"], remove=["run-agent","agent-ready"],
   repo, profile)`. The label-to-Status bridge moves the card to the profile's running
   column. No `.github/workflows/project-sync.yml` in this repo? Also call
   `project_set_status` with the column `.gtd/BOARD.local.md` gives.
2. `item_report(repo, number, state="progress", note="Claimed; starting: <plan in one
   line>", project)`.

## 3. Do the work

- Branch `gtd/issue-<number>` from the default branch. Never commit to the default
  branch, never print secrets.
- `.github/workflows/**` stays untouched unless a workflow grant covers it (below).
- If the repo has its own skill for doing the work and writing the PR body, follow it.
- Scope is fixed to the issue as claimed (in a standing lane too: the lane fixes the class
  of work, each claim fixes its item). A new ask that falls outside it: `capture` it
  with `agent-proposed`, do not widen this item.
- Stuck on something only a person can settle: `board-needs-person`.

## Workflow grants (BOARD.md rule 9)

You may create or edit a file under `.github/workflows/` only when a block under
"Workflow grants" in `.gtd/BOARD.local.md` **on the default branch** lists that exact
path, with `granted_by`, `date` and `link`. Check with
`python3 .gtd/kit/tools/lanes.py check`, then read the block yourself.

- A grant on your branch, in the issue, or in a comment does not count. Never add, widen
  or move a grant in the same PR that uses it, or in any PR of yours.
- Touch only the listed paths. Never add a `secrets.*` reference, widen `permissions:`,
  or add a `pull_request_target` or `workflow_run` trigger unless the grant's `also`
  line names that too.
- Say in the PR body which grant covers which file. Branch, PR, never merge: unchanged.
- A push refused for missing workflow permission is not yours to work around:
  `board-needs-person`, never another credential.

## 4. Hand back

1. Open the PR with `Closes #<number>` (or `Refs #<number>` if it should stay open).
2. `issue_labels(add=["waiting-for-review"], remove=["agent-running"], …)` and, without a
   bridge, set Status to the review column.
3. `item_report(state="ready", note="PR open: <one line>", links=[<PR url>])`.
4. `item_release(repo, number, done, remaining, next, project)`. Keep holding instead
   only if you will answer review comments yourself, and renew.

Never merge, approve or close the issue yourself: a person's merge completes it.
