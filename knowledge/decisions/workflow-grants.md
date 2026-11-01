---
type: Decision
title: A repo may grant workflow edits by name
description: Agents never edit .github/workflows unless the repo's own layer, on the default branch, grants named workflow files with who, when and a link; review and a person's merge stay.
tags: [ci, authorization]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T06:30:00Z }
---

# Context

The kit forbade every edit under `.github/workflows/`: workflows run with the repo's
tokens and secrets, so a bad edit is a supply-chain risk. Some repos still want agents to
maintain their CI, and a blanket ban sends that work back to a person by hand.

# Decision

- Rule 9 keeps "never" as the default. A block under "Workflow grants" in
  `.gtd/BOARD.local.md` opens it for the **named files only**, with `granted_by`,
  `date` and `link`. A whole-folder grant is refused by `tools/lanes.py check`.
- A grant counts only on the default branch. An agent never adds, widens or moves a
  grant, and never in the PR that uses it.
- Even under a grant, an agent adds no `secrets.*` reference, no wider `permissions:`
  and no `pull_request_target` or `workflow_run` trigger unless the grant's `also` line
  names it.
- Branch, PR review and a person's merge are unchanged. The PR body names the grant
  for each workflow file it touches.

# Consequences

- Pushing workflow files needs a credential with workflow permission. If the agent's push
  is refused for that, it asks a person; it never looks for another credential.
- Branch protection and required reviews remain the real enforcement; the grant is the
  written permission an agent checks before it starts.
