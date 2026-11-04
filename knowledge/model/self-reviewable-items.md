---
type: Pattern
title: Items that speak for themselves
description: A person judges an item from the issue alone, in about a minute, by following links; ticked criteria with linked evidence, the Status, the labels and one ready report carry it, and a summary table elsewhere never replaces them.
tags: [attention, evidence, acceptance-criteria, review]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-04T15:45:00Z }
---

# Rule

An item is done when a person can verify it **from the issue alone**, without reading a PR
body, a chat or a summary table. The owner's attention is the scarce input
([attention budget](/decomposition/human-gates/attention-budget.md)), so the issue does
the explaining with GitHub's own constructs, and every claim on it is one click from its proof.

| A person asks | The issue answers with | Written by, when |
| --- | --- | --- |
| Where is it? | Status (one column) | the label bridge, or the agent per `.gtd/BOARD.local.md` |
| Who acts next? | the labels: `waiting-for-review` (you review), `needs:*` (you decide), none (no one waits on you) | the holder, at each report |
| Is each criterion met? | its ticked box, and on the same line a **link** to the proof | the worker, at `ready` |
| What came back, and what do I do? | one `ready` report: what was delivered, the one action asked, links | the worker, at `ready` |
| Where is the work? | the PR as a `link` artifact (it stays after the merge); on a server without artifact tools, the PR's evidence row, and the report says so | the worker, at `ready` |
| What changed after a review? | a reply report naming each finding and its commit link | the worker, after the fix |

## Criteria lines

- Tick a box only when its proof passes; leave it empty, with the reason on the line, when
  it does not. Never reword the criterion: add the tick and the link only.
- The link goes to the proof itself, not to a page that holds it: a permalink to the file
  or lines at the head commit, the CI run, the published page. The PR's evidence row is
  named too, because the PR check reads it. The line ends like
  `Evidence: docs/pitch/x.md at the head commit (linked), PR #n AC1 row`.
- A criterion the work no longer meets as written (a review changed the plan) stays
  unticked, and the report asks the person to reword it. The worker never rewords it.

## The ready report

At most three lines: what is delivered (with links), the one thing the person must do
(review and merge, decide, listen), and anything not done. No progress narration, no
pasted logs. A healthy item asks nothing more and takes no more attention.

# Why

A summary table in a PR is useful at merge time, but it makes the person open another page
and hold the mapping in their head. dsh-superagent's rule is to take as little human
attention as possible and give as much value as possible
([reference](/references/dsh-superagent.md)). The issue is where a person starts and where
they come back months later, so each item must stand on its own there. GitHub already
shows Status, labels, checkboxes (with a done count in lists), links and artifacts, so
the kit uses them instead of inventing a format.

# Related

- [Where evidence goes](evidence-places.md)
- [Report vocabulary](report-vocabulary.md)
- [Board fields and who writes them](board-fields.md)
