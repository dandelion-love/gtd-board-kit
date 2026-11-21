---
name: board-claim
description: Claim a board item, work it on a gtd/issue-N branch and hand it back as a PR, keeping the board current through the gtd MCP server. Use when starting work on a GitHub issue in a repo that has gtd-board-kit, whether you were pointed at it or picked it with board-pickup.
metadata:
  author: gtd-board-kit
  version: 0.11.0
---

# Claim an item and work it

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file wins over anything below. `repo`, `profile` and
`project` come from `.github/gtd-context.json` and the origin remote (see `board-pickup`).

## 1. Claim before touching anything

```
item_claim(repo, number, basis, asked_by, pointed_in, lease="2h", branch, session, model, reasoning, project)
```

- `explicit`: you were pointed at it. `asked_by` is who pointed you (your person's
  handle, `coordinator`, a thread); `pointed_in` links the message or comment if you have one.
- `inferred`: an unpointed `agent-ready` pull. The server refuses unless the board Size is
  XS, S or M and no `agent:<x>` names someone else. **On refusal, do not retry as
  `explicit`** unless someone really pointed you at it: pick another item or ask.
- Held: leave it.
- Lease: enough for the work, up to 72h; renew it.
- `branch`: where its commits land (`gtd/issue-<number>`, or the combined branch).
- `session`: one name for this session; no session reviews its own work.
- `model`, `reasoning`: self-reported, unverified; omit when unknown.
- **Taking over** (`previous_holder` set, or `interruptions` above 0): read `closing_note`
  (done, left, decided, set_aside) and `interruptions` in `item_get` first. Start from `left`,
  keep `decided`, skip `set_aside`; `none recorded`: read its reports and commits.
- A `stop` in any result: finish the step, write the note, release (`board-report`).

## Several stories on one branch

Claim every story you work, one `item_claim` each, before its first commit; each has its
own lease, reports and release. The PR lists them all in `pr_open`'s `issues`. Details in
`branches.md`; read it before combining stories.

## 2. Show it on the board

1. `issue_labels(number, add=["agent-running"], remove=["run-agent","agent-ready"],
   repo, profile)`. The label-to-Status bridge moves the card to the profile's running
   column. No `.github/workflows/project-sync.yml` in this repo? Also call
   `project_set_status` with the column `.gtd/BOARD.local.md` gives.
2. `item_report(repo, number, state="progress", note="Claimed; starting: <plan>", project)`. Fields a profile sync `owns` (`profile_get`; e.g. an experiment's
   Agent, Start date, Last report) are never set by hand: record through its register.

## 3. Do the work

- Branch `gtd/issue-<number>` from the default branch; never commit to it or print
  secrets.
- `.github/workflows/**` stays untouched unless a workflow grant covers it (below).
- The repo's own skill for the work and the PR body, if any, wins.
- Scope is the issue as claimed. A new ask outside it: `capture` it with
  `agent-proposed`; never widen this item.
- Stuck on something only a person can settle: `board-needs-person`.

## Grants (BOARD.md rule 9)

Workflow files and merging stay off-limits unless a grant in `.gtd/BOARD.local.md` **on
the default branch** names the paths (`knowledge/model/grants.md`). `git fetch`, then
run `python3 .gtd/kit/tools/lanes.py check --merged` with `--covers <workflow path>` before
touching a workflow, or `--head <branch> --merge <every changed file>` before merging; go on only on exit 0.
A grant on a branch, issue or comment counts for nothing; never add or widen one. A push refused for workflow permission: `board-needs-person`.

## 4. Hand back

1. Push the branch. If the server lists `pr_open`, open the PR with it:
   `pr_open(repo, head=<branch>, base, title, body, issues=[every story it carries], closes)`.
   - `closes=true` only when the work is verified (tests run, evidence in the body) and
     `base` is the default branch. Into a combined branch: `closes=false`.
   - No `gtd-pr` marker, and no closing keyword before an issue (`close`, `fix`,
     `resolve`, any form) in `body` or commits, even in a rollback note ("release #n").
     Merging would close it.
   - Refused for a missing claim: claim it or take it out. Never route around a refusal.
   - Work with no issue of its own (a register line): claim the experiment's issue or the
     repo's standing chore item (`.gtd/BOARD.local.md`).
2. No `pr_open` on the server: open it with your own GitHub tool, `Refs #<number>` for
   each story (`Closes` only if `closes=true`), and say so in the ready report.
3. `issue_labels(add=["waiting-for-review"], remove=["agent-running"], …)` and, without a
   bridge, set Status to the review column. Add `agent-review` too to ask another
   session to review it (`board-review`).
4. `item_report(state="ready", note="PR open: <one line>", links=[<PR url>])`.
5. Only under an owner-approved merge grant covering every changed file: `pr_merge`
   (refuses on pending checks, requested changes or conflict). No `pr_merge`, no merge.
   Report with the merged link (`grants.md`).
6. `item_release(repo, number, done, left, decided, set_aside, next, project)` (no `left` in the
   server's schema? pass `remaining`), or keep holding (renew)
   to answer review comments yourself (`activity_since`): each finding with
   `pr_review_reply(…, resolve=true)` (what changed, the commit), a PR note with
   `issue_comment`. Your own GitHub tool only if neither is offered: it is unsigned.

## 5. After it merges

Your PR merged into any branch, the server lists `item_close_done`, and `.gtd/BOARD.local.md`
has no `## Stale done` with `sweep: off`: `stale_done(repo, number, branches=<landed_branches>)`.
`close`: `item_close_done(repo, number, session)`. `keep`: leave it open and report the
reasons. Never close any other way, never approve, never merge outside Hand back step 5.
