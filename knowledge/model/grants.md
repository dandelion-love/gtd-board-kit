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
when, and where. A grant counts only once it is on the default branch **and the owner
approved the PR that added it**. A grant on a branch, in an issue or in a comment grants
nothing. An agent may *propose* a grant block in a PR, but the proposal never counts
by itself: the only record of the owner's authority is the owner's own approving review
(or the owner authoring and merging the PR), never text an agent wrote. An agent never
merges the PR that adds its own grant, and never widens or moves a grant.

`python3 .gtd/kit/tools/lanes.py check --merged ...` is the authority on *which files a
grant names*. Run `git fetch` first; it reads `origin/HEAD` and never the working copy. It
reads files, not reviews, so it cannot tell whether the owner approved the PR that added
a grant: that proof is checked by a server's `pr_merge` (below), and an agent with no
`pr_merge` does not merge.

### Owner approval of a grant

A grant counts only if the PR that introduced that exact block into the default branch
has an approving review by `granted_by` on its final head, or was authored and merged by
`granted_by`. Editing a block makes it a new grant that needs its own approval. A grant
with no findable introducing PR counts for nothing. A grant merged before this rule
stops counting until a PR re-adds it with the owner's approval; there is no
grandfathering, so the record is clean.

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

4. **The grant counts**: the owner approved the PR that added it (above).

An agent merges only through the server's `pr_merge`
([tools](../../server-spec/tools.md#merging-pull-requests)), which checks 1 to 4 itself,
and reports `ready` with the merged PR's link, then releases the item. If any condition
fails, or the server offers no `pr_merge`, it leaves the PR for a person, as without a
grant. A merge grant never covers approving a PR, closing an issue by hand, or a force push.

# Why

Owner approval closes the hole found on 2026-11-04: a grant whose only record was text
the agent wrote. A server-side checks gate closes the other: a merge went through with
its checks still pending because the agent's own wait returned early.

Some work is mechanical and frequent: an agent appending a line to a register the
owner reviews later. Waiting hours for a person's merge leaves the board stale (a card
says Running long after the run is done). Exact paths keep the grant from covering code
or rules, and the merged-only check keeps an agent from granting itself.

The pull request check's daily audit (`templates/workflows/gtd-pr-check.yml`) still lists
every merge by an agent, so a person sees each granted merge the next day.
