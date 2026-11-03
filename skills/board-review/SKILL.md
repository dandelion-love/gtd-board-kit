---
name: board-review
description: Review a board issue a person labelled agent-review, against the kit's epic and story shapes and the ready check, and post one comment of findings, through the gtd MCP server. Use when an issue carries agent-review, or a person asks for a review of a ticket.
metadata:
  author: gtd-board-kit
  version: 0.1.0
---

# Review an issue

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file wins. `agent-review` is a person asking for a second look at
an issue before they approve or build it. It is not `agent-ready` and not `run-agent`.

## 1. Claim it

`item_claim(repo, number, basis="explicit", asked_by=<who added agent-review, or who
pointed you>, lease="1h", project)`. The label is the pointing. Refused: someone holds
it; leave it. A dispatch run started from the label is already pointed.

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
- **Evidence.** For a story with a merged PR: every criterion has its evidence where
  `.gtd/kit/knowledge/model/evidence-places.md` says.

## 3. Post one comment

`issue_comment(repo, number, body)` with:

1. A verdict line: `Looks ready`, `Needs changes` or `Needs a person`.
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
