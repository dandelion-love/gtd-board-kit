---
type: Pattern
title: Labels are signals; Status follows
description: Agents change labels on an issue; the repo's label-to-Status bridge moves the board card, so the board never drifts from the issue.
tags: [board, labels, status]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T04:00:00Z }
---

# Rule

An agent changes **labels**, through the gtd MCP server's issue tools. A label-to-Status
bridge in the repo turns labels into the board's Status column, in a fixed precedence.
Only where a repo has no bridge does an agent set Status itself, using the column its
`.gtd/BOARD.local.md` gives for each label.

# Label families

| Family | Says | Examples |
| --- | --- | --- |
| Dispatch | where the agent loop is | `run-agent`, `agent-review`, `agent-running`, `waiting-for-review`, `agent-failed`, `blocked` |
| Whom it waits for | a person's turn | `needs:<who>` |
| Who may take it | routing | `agent:any`, `agent:<runtime>`, `agent:human` |
| May it be pulled | accept mode | `agent-ready` (pull), `agent-proposed` (observe only) |

`run-agent` asks for the work now; `agent-review` asks for a review of the issue only
(the `board-review` skill): it never starts a build and never adds `agent-ready`. Only a
person adds either.

See [claims](/model/claims-and-leases.md) for who holds an item and
[reports](/model/report-vocabulary.md) for what a holder says.
