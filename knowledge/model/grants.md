---
type: Pattern
title: Grants that widen rule 9
description: Rule 9 says never merge and never touch workflows; a person may widen it only by a named grant merged into BOARD.local.md, checked by lanes.py against the default branch.
tags: [grants, merge, workflows, rule-9]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-04T00:40:00Z }
---

# Rule

Kit rule 9 has two defaults an agent cannot change: it never merges, and it never creates
or edits `.github/workflows/**`. A repo's owner widens either one only with a **grant**:
a named block in `.gtd/BOARD.local.md` that lists exact paths and says who granted it,
when, and where. A grant counts only once it is on the default branch, so a person has
merged it. A grant on a branch, in an issue or in a comment grants nothing, and an agent
never adds, widens or moves a grant, least of all in the PR that would use it.

`python3 .gtd/kit/tools/lanes.py check --merged ...` is the authority. Run `git fetch`
first; it reads `origin/HEAD` and never the working copy.

## Workflow grants

`### grant: <name>` under `## Workflow grants`, with `paths` (each under
`.github/workflows/`, named, never the whole folder), `granted_by`, `date`, `link` and an
optional `also`. Before touching a workflow file, `lanes.py check --merged --covers <path>`
must exit 0. Never add a `secrets.*` reference, widen `permissions:`, or add a
`pull_request_target` or `workflow_run` trigger unless `also` names it. Say in the PR body
which grant covers which file.

## Merge grants

`### merge: <name>` under `## Merge grants`, with `paths` (exact files, never a folder or
pattern, never under `.github/` or `.gtd/`), `granted_by`, `date`, `link` and an optional
`also` for extra conditions. An agent may merge a PR only when all of these hold:

1. **One** merged merge grant names **every** file the PR changes:
   `lanes.py check --merged --merge $(git diff --name-only --no-renames origin/HEAD...<head>)`
   exits 0. `--no-renames` lists both sides of a rename, so a file moved into a granted
   path from anywhere else is caught. Two grants that each cover part of a PR do not add up.
2. The PR is one the agent opened with `pr_open` for an item it holds, and targets the
   default branch.
3. Every required check is green on the PR's current head, nobody has requested changes,
   and the PR has no merge conflict. Anything the grant's `also` adds holds too.

Then it merges with the repo's usual method, reports `ready` with the merged PR's link,
and releases the item. If any condition fails it leaves the PR for a person, as without a
grant. A merge grant never covers approving a PR, closing an issue by hand, or a force push.

# Why

Some work is mechanical and frequent: an agent appending a line to a register the
owner reviews later. Waiting hours for a person's merge leaves the board stale (a card
says Running long after the run is done). Exact paths keep the grant from covering code
or rules, and the merged-only check keeps an agent from granting itself.

The pull request check's daily audit (`templates/workflows/gtd-pr-check.yml`) still lists
every merge by an agent, so a person sees each granted merge the next day.
