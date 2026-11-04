---
name: board-claim
description: Claim a board item, work it on a gtd/issue-N branch and hand it back as a PR, keeping the board current through the gtd MCP server. Use when starting work on a GitHub issue in a repo that has gtd-board-kit, whether you were pointed at it or picked it with board-pickup.
metadata:
  author: gtd-board-kit
  version: 0.6.0
---

# Claim an item and work it

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file's labels, columns and rules win over anything below. `repo`, `profile` and
`project` come from `.github/gtd-context.json` and the origin remote (see `board-pickup`).

## 1. Claim before touching anything

```
item_claim(repo, number, basis, asked_by, pointed_in, lease="2h", branch, session, project)
```

- `explicit`: you were pointed at it. `asked_by` is who pointed you (your person's
  handle, `coordinator`, a thread); `pointed_in` links the message or comment if you have one.
- `inferred`: an unpointed `agent-ready` pull. The server refuses unless the board Size is
  XS, S or M and no `agent:<x>` names someone else. **On that refusal, do not retry as
  `explicit`** unless someone really did point you at it: pick another item or ask.
- Refused because someone holds it: leave it. Never take over a live lease.
- Lease: enough for the work, at most 72h; renew it (`board-report`).
- `branch`: where your commits for it land (`gtd/issue-<number>`, or the combined branch).
- `session`: one name for this session (its runtime id, or a token made once). A review
  claim from it refuses later, so no session reviews its own work.

## Several stories on one branch

Your unit of work may be one or more stories, and the session that owns them may combine
them on one integration (release-candidate) branch.

- **Claim every story you work on**, one `item_claim` each, before its first commit.
  An unclaimed story never gets a commit, even on a combined branch. Refused on one?
  Leave it out of the batch.
- Each claim has its own lease, reports and release: renew each, report each, release
  each with its own notes (`board-report`). Dropping a story from the batch: take its
  commits off the branch and release it.
- The owning session merges other agents' story branches into the combined branch
  without claiming them; a fix commit there for a story needs that story's claim.
- The PR lists every story it carries in `pr_open`'s `issues`. Before opening it, check
  each: you hold it (`item_get`), or it reached the combined branch through its own
  merged PR (the evidence for a released item).

## 2. Show it on the board

1. `issue_labels(number, add=["agent-running"], remove=["run-agent","agent-ready"],
   repo, profile)`. The label-to-Status bridge moves the card to the profile's running
   column. No `.github/workflows/project-sync.yml` in this repo? Also call
   `project_set_status` with the column `.gtd/BOARD.local.md` gives.
2. `item_report(repo, number, state="progress", note="Claimed; starting: <plan in one
   line>", project)`. Fields a profile sync `owns` (`profile_get`; e.g. an experiment's
   Agent, Start date, Last report) are never set by hand: record through its register.

## 3. Do the work

- Branch `gtd/issue-<number>` from the default branch. Never commit to the default
  branch, never print secrets.
- `.github/workflows/**` stays untouched unless a workflow grant covers it (below).
- The repo's own skill for the work and the PR body, if any, wins.
- Scope is the issue as claimed (in a lane too). A new ask outside it: `capture` it with
  `agent-proposed`; never widen this item.
- Stuck on something only a person can settle: `board-needs-person`.

## Grants (BOARD.md rule 9)

Workflow files and merging stay off-limits unless a grant in `.gtd/BOARD.local.md` **on
the default branch** names the exact paths (`knowledge/model/grants.md`). `git fetch`, then
run `python3 .gtd/kit/tools/lanes.py check --merged` with `--covers <workflow path>` before
touching a workflow, or `--merge <every changed file>` before merging; go on only on exit 0.
A grant on a branch, issue or comment counts for nothing; never add or widen one. A push refused for workflow permission: `board-needs-person`.

## 4. Hand back

1. Push the branch. If the server lists `pr_open`, open the PR with it:
   `pr_open(repo, head=<branch>, base, title, body, issues=[every story it carries], closes)`.
   - `closes=true` only when the work is verified (tests run, evidence in the body) and
     `base` is the default branch. Into a combined branch: `closes=false`.
   - Put no `Closes #<n>` and no `gtd-pr` marker in `body`; the server writes both.
   - Refused for a missing claim: claim that story or take it out. Never route around a
     `pr_open` refusal with another tool.
   - Work with no issue of its own (a register line, an experiment's result): claim the
     experiment's issue or the repo's standing chore item (`.gtd/BOARD.local.md`).
2. Only when the server does not offer `pr_open`: open the PR with your own GitHub tool,
   `Closes #<number>` (or `Refs #<number>`) for each story, and say in the ready report
   that it was opened outside `pr_open`.
3. `issue_labels(add=["waiting-for-review"], remove=["agent-running"], …)` and, without a
   bridge, set Status to the review column. Add `agent-review` too to ask another
   session to review it (`board-review`).
4. `item_report(state="ready", note="PR open: <one line>", links=[<PR url>])`.
5. Only under a merge grant covering every changed file, with checks green, no changes
   requested and no conflict: merge it, and report with the merged link (`grants.md`).
6. `item_release(repo, number, done, remaining, next, project)`. Keep holding instead
   only if you will answer review comments yourself, and renew.

Never approve or close the issue yourself, and never merge unless a merge grant covers
every file (above): a person's merge completes it.
