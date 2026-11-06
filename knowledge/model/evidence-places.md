---
type: Pattern
title: Where evidence goes
description: The PR's evidence table stays the gate; issue artifacts keep evidence and plans on the issue after the PR merges; sub-issues are never evidence and comments carry reports.
tags: [evidence, acceptance-criteria, issue-artifacts]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-03T15:30:00Z }
sources:
  - { id: gh-artifacts, title: "GitHub Docs, Using artifacts with issues", resource: "github/docs: content/issues/tracking-your-work-with-issues/using-issues/using-artifacts-with-issues.md", url: "https://github.com/github/docs/blob/main/content/issues/tracking-your-work-with-issues/using-issues/using-artifacts-with-issues.md", accessed: 2026-11-03 }
  - { id: gh-artifacts-rest, title: "GitHub Docs, REST API endpoints for issue artifacts", resource: "https://docs.github.com/en/rest/issues/artifacts", url: "https://docs.github.com/en/rest/issues/artifacts", accessed: 2026-11-03 }
---

# Rule

Each numbered acceptance criterion is answered by evidence a person can open from the
issue, after the PR is merged as well as before. Put each kind in one place:

| Evidence | Where | Who writes it, when |
| --- | --- | --- |
| The answer to each criterion (test, check, command, screenshot, review) | one row per `AC<n>` in the PR body's evidence table | the agent, in the PR; the PR check reads it, so it stays the gate |
| The approved plan | a `plan` artifact on the epic, the plan as the person saw it | the agent that asks for G1; never edited after approval, a new plan is a new artifact |
| Something outside GitHub: the merged PR, a published page, a meeting note, a source | a `link` artifact on the issue the evidence answers | the agent, at its `ready` report |
| A report that is the work itself: a spike's answer, a Finding, a verification run | a `generic` artifact on the issue | the agent, at its `ready` report |
| A diagram or prototype | an `embedded_html` artifact | the agent, when the story calls for one |
| Progress and questions | `item_report` (a comment record) | the holder, at each milestone |

- The issue's criterion line names where its evidence is: `Evidence: PR #n, AC2 row` or
  `Evidence: artifact "<name>"`.
- **Ticking.** At its `ready` report the worker ticks each criterion's box whose evidence
  row passes, and adds that pointer to the line. A box stays empty while its row fails or
  is missing. A work review checks every tick against its row, and the person's merge
  confirms them. The worker edits only the boxes and pointers, never the criterion's text.
  The pointer is a link to the proof itself (a permalink to the file at the head commit,
  the run, the page), as [items that speak for themselves](self-reviewable-items.md) says.
- An artifact name holds only letters, numbers, spaces, periods, hyphens and underscores,
  and starts and ends with a letter or number (GitHub refuses `#` or `:`):
  `PR n evidence`, not `PR #n: evidence`.
- **Evidence is the thing, not a description of it.** When a criterion names a produced
  file (an export, a render, a screenshot, a printout, a recording), that file is committed
  in the PR or attached to the issue, and the evidence row links it. A row that only
  reports what the file showed ("exported to PDF: 2 pages") with nothing to open is a
  missing row, and its box stays empty.
- A **sub-issue is never evidence.** Sub-issues are work: stories under an epic, and
  steps where `.gtd/BOARD.local.md` allows them.
- Artifacts are versioned: update one rather than adding a second of the same name.
  Only a person deletes one, because deleting removes its history.
- Agents write artifacts only through the gtd MCP server's issue artifact tools. A
  server without them: put the link in the PR's evidence row and say so in the report.

# Why

The PR body's table proves the work at merge time, but it lives on the PR. A reader who
starts from the issue, or comes back months later, needs the plan and the evidence
where the criteria are. GitHub's issue artifacts are named, ordered and versioned on the
issue itself, and an API can create and update them[^gh-artifacts][^gh-artifacts-rest],
so they fit that role without inventing a file convention. GitHub calls the feature a
public preview, which is why the PR row, not the artifact, stays the gate.

# Related

- [Criterion-to-evidence chain](/decomposition/acceptance-and-verification/criterion-to-evidence-chain.md)
- [Board fields and who writes them](board-fields.md)
- [Items that speak for themselves](self-reviewable-items.md)
- [Report vocabulary](report-vocabulary.md)
