---
type: Reference
title: Labels as approval signals
description: A label a person adds is a cheap, visible, attributable go-ahead; anyone with triage or write can add one, so it is a convention that agents must check.
tags: [github, labels, signals, conventional]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: kit-labels, title: "gtd-board-kit: Labels are signals", resource: "https://github.com/owner/gtd-board-kit/blob/main/knowledge/model/labels-are-signals.md", accessed: 2026-11-02}
  - {id: gh-roles, title: "GitHub Docs: Repository roles for an organization", resource: "https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization", accessed: 2026-11-02}
  - {id: gh-forms, title: "GitHub Docs: Syntax for issue forms", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms", accessed: 2026-11-02}
  - {id: dsh-domain, title: "dsh-superagent-prototype: 001 Domain model", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 001-domain.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
---

# What the kit already uses

The kit's label families include "may it be pulled" (`agent-ready` to pull,
`agent-proposed` for observe only) and "whom it waits for" (`needs:<who>`); a bridge turns
labels into Status.[^kit-labels]

# Why labels beat Status for approvals

| Property | Label | Status move |
| --- | --- | --- |
| Visible on the issue | yes | on the board |
| Actor recorded | yes, as a timeline event | unreliable, see [status move](github-projects-status-move.md) |
| Set by an issue form | yes, default labels[^gh-forms] | via project add only |
| Who can set it | triage role and above[^gh-roles] | project write |

# Limits

- **Not enforceable.** Any account with triage or write, including an agent token, can add
  `agent-ready`.[^gh-roles] The gate holds only if agents (a) never add approval labels
  themselves and (b) check the adder is a person before claiming.
- **Inferred is not explicit.** dsh-superagent's lesson: a classification of "waiting on a
  person" must come from structured facts, not from free text.[^dsh-domain] A label is a
  structured fact; a comment saying "go ahead" is not.

# Approval label set (proposal)

| Label | Added by | Means |
| --- | --- | --- |
| `agent-ready` | person | build this Story now |
| `agent-proposed` | agent | I suggest this; do not pull |
| `needs:<who>` | anyone | stop; a person must answer |

# Caveats

- The kit URL uses a placeholder owner.
- The roles table is for organisation repos; a personal repo has owner and collaborators,
  and collaborators with write can label.

[^kit-labels]: Kit model page, label families.
[^gh-roles]: GitHub Docs, repository roles (Triage can apply labels).
[^gh-forms]: GitHub Docs, issue form default labels.
[^dsh-domain]: dsh-superagent 001 Domain model, rejected concepts.
