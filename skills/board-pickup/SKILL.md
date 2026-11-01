---
name: board-pickup
description: Find a board item this agent may take in the current repo, through the gtd MCP server. Use when a session starts with no task, or when asked "what should I work on", "pick up work", "anything on the board for me". Read-only; it never claims.
metadata:
  author: gtd-board-kit
  version: 0.2.0
---

# Pick up work from the board

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file's labels, columns and rules win over anything below. Everything here goes
through the gtd MCP server; if its tools are missing, stop and say so (BOARD.md rule 1).

## 1. Who and where

1. `whoami`: note your principal (`agent:<name>` or `google:<email>`) and preset. Writes
   need the `work` preset; `read` can only look.
2. Read `.github/gtd-context.json`: `profile`, and `project` if set (pass it as
   `owner/number`). `repo` is this repo's `owner/name` from `git remote get-url origin`.
3. Pointed at a specific issue already? Skip to the `board-claim` skill. Running a
   standing lane? Use `board-lane`; its `may` list replaces the pull filter below.

## 2. List candidates

- Pushed work first: `list_next_actions(repo=…, context="run-agent")`.
- Then pull work: `list_next_actions(repo=…, context="agent-ready")`.
- For Size and Status, page the board with `project_items(project=…)`, or one item with
  `project_item_find`.

## 3. Filter: keep an item only if all hold

- It is open, labelled `run-agent` (you were pushed it) or `agent-ready` (pull).
- No `agent:<x>` label names someone other than you; `agent:any` or none is fine.
  `agent:human` is never yours.
- No `needs:*`, `blocked`, `agent-running`, `waiting-for-review` or `agent-proposed`
  label.
- For a pull (`agent-ready` without `run-agent`): board Size is XS, S or M. No Size, no
  pull.
- Nothing open blocks it: `issue_blocked_by_list`.
- Nobody holds it: `item_get(repo, number)` shows no live claim.

## 4. Choose and hand off

Prefer `run-agent` over `agent-ready`, then higher Priority, then smaller Size, then the
oldest. Tell your person which item you picked and why in one line, then use
`board-claim`. With `run-agent` the basis is `explicit` (`asked_by` is whoever added the
label, or your person); with only `agent-ready` it is `inferred`.

Nothing qualifies? Say so and stop. Do not lower the bar, and do not invent work:
anything new goes in through `capture` with `agent-proposed` (BOARD.md rule 8).
