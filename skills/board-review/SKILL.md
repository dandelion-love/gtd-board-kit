---
name: board-review
description: Review a board issue labelled agent-review (by a person, or by an agent asking another session to check its work), against the kit's epic and story shapes and the ready check, and post one comment of findings, through the gtd MCP server. Use when an issue carries agent-review, or a person asks for a review of a ticket.
metadata:
  author: gtd-board-kit
  version: 0.4.0
---

# Review an issue

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file wins. `agent-review` asks for a second look at an issue: a
person's before they approve or build it, or an agent's after it finished the work and
wants another session to check it. It is not `agent-ready` and not `run-agent`.

**Never review your own session's work.** A review is another pair of eyes; the session
that claimed the item to work it cannot be them. A fresh session of the same agent may.
The server enforces this on the claim below.

## Finding the requests (a lane)

Nothing starts a review on its own yet. A standing lane (`board-lane`) whose `may` names
board reviews runs this skill on a schedule: each tick, `issue_list(repo,
labels=["agent-review"], state="open")` for every repo the lane watches, oldest first,
and reviews each one as below, with `asked_by` the lane's. An item someone holds is
skipped until next tick. One comment per request: never review an issue twice for one
label.

## 1. Claim it

`item_claim(repo, number, basis="explicit", asked_by=<who added agent-review, or who
pointed you>, purpose="review", session=<this session's name, as in board-claim>,
lease="1h", project)`. The label is the pointing. Refused because someone holds it:
leave it. Refused because your session worked the item: leave it for another session,
never retry with another `session`. A dispatch run started from the label is already
pointed. A server whose `item_claim` has no `purpose`: claim as before, and skip any
item this session claimed, reported on or opened a PR for.

## 2. Review against the kit

Read the issue, its parent, its sub-issues and its blockers (`item_get`,
`issue_parent`, `sub_issues_list`, `issue_blocked_by_list` when offered). Then check:

- **Shape.** The body has every section of its Kind in
  `.gtd/kit/skills/board-decompose/templates.md`. An epic: Problem, Outcome check,
  Scope, Out of scope, Stories, Decisions, Risks and open questions, Gates. A story: one
  `## Acceptance criteria` heading, `Steps`, `Blocked by` lines.
- **Criteria.** Numbered `AC1`...; each checkable, each naming its evidence; at least one
  error or rejection case. `.gtd/kit/knowledge/decomposition/acceptance-and-verification/`
  has the heuristics.
- **Ready.** `item_ready(repo, number, project)` when offered (not for an epic); quote
  its verdict and `missing`.
- **Board.** The fields `.gtd/kit/knowledge/model/board-fields.md` names; for an epic,
  the Stories table against its sub-issues.
- **Evidence.** For a story with an open or merged PR (a work review): every criterion
  has a passing row in the PR's evidence table, its box is ticked with that pointer, and
  the PR is a `link` artifact on the issue, as
  `.gtd/kit/knowledge/model/evidence-places.md` says. A missing tick, pointer or
  artifact is a finding.

## 3. Post one comment

`issue_comment(repo, number, body)` with:

1. A verdict line that names the stage, then the verdict. `Plan review` (no PR yet: is
   it ready to build?) or `Work review` (a PR exists: is the work done?), then `Looks
   ready`, `Needs changes` or `Needs a person`. E.g. `Work review: Needs changes`.
2. Findings, most important first, each with the section it is about and a suggested
   text a person can paste.
3. What you did not check, and why.

Never edit the person's text, never add `agent-ready` or `run-agent`, never start a
build, never close the issue. A finding that is new work: `capture` it with
`agent-proposed` and link it.

## 4. Hand back

1. `issue_labels(number, remove=["agent-review"], repo, profile)`.
2. `item_report(repo, number, state="ready", note=<verdict and the comment's link>)`.
   A question only the person can answer: `board-needs-person` instead.
3. `item_release(repo, number, done, remaining, next, project)`.
