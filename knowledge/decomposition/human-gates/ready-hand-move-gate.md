---
type: Pattern
title: Ready hand move (Definition of Ready gate)
description: Agents may refine an item up to Ready, but only a person moves it into the column agents pull from; that move is the go-ahead.
tags: [gates, definition-of-ready, board, human-approval]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: applab, title: "AppLab backlog plugin README (v1.3.0)", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/README.md", accessed: 2026-11-02, commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, version: 1.3.0}
  - {id: kit-labels, title: "gtd-board-kit: Labels are signals", resource: "https://github.com/owner/gtd-board-kit/blob/main/knowledge/model/labels-are-signals.md", accessed: 2026-11-02}
  - {id: kit-claims, title: "gtd-board-kit: Claims and leases", resource: "https://github.com/owner/gtd-board-kit/blob/main/knowledge/model/claims-and-leases.md", accessed: 2026-11-02}
  - {id: sk-implement, title: "Spec Kit: implement command (checklist gate)", resource: "https://github.com/github/spec-kit/blob/7370e592f3cd9c06e5b698983957e227c75b30e2/templates/commands/implement.md", accessed: 2026-11-02, commit: 7370e592f3cd9c06e5b698983957e227c75b30e2}
  - {id: gh-projects-access, title: "GitHub Docs: Managing access to your projects", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-access-to-your-projects", accessed: 2026-11-02}
---

# What it is

Two different questions, kept apart:

| Question | Who answers | Signal |
| --- | --- | --- |
| Is the item **ready** (clear enough to build)? | An agent may check and propose | item reaches the Ready column |
| Should it be built **now**? | A person only | person moves it Ready → pickup |

# The source pattern

The AppLab backlog plugin moves tickets along one edge only: Backlog → READY. "Moving a
ticket from ready to the pickup column is your planning decision — that hand-move is what
keeps an overnight run from building every idea on the board."[^applab]

- Refinement promotes a ticket to READY only when six questions are answered: what the user
  sees, the unhappy path, paths touched, out of scope, how to verify, what it ships behind.[^applab]
- The unattended run reads the **pickup** column, not READY. "On a board with no separate
  Ready column the two are the same column and the gate simply isn't there."[^applab]
- A ticket without acceptance criteria is skipped and reported, never guessed at.[^applab]

Spec Kit has a softer version: before implementing, unchecked reviewer-owned checklist items
stop the agent with a yes/no question.[^sk-implement]

# Mapping to the kit

The kit's `agent-ready` label already means "may be pulled"; `agent-proposed` means observe
only.[^kit-labels] An inferred claim needs `agent-ready`, a small Size and no routing label
naming someone else.[^kit-claims] So the hand move is: **a person adds `agent-ready`** (or
moves the card to the column its bridge maps to it).

# Enforceable or conventional?

Conventional. Project roles are whole-project (Read, Write, Admin); there is no per-field or
per-column permission, so any writer, including an agent token with write, can move a
card.[^gh-projects-access] The gate holds only if agents are told never to add `agent-ready`
themselves, and a check flags it when they do. See
[enforceable vs conventional](github-enforceable-vs-conventional.md).

# Why it is cheap

One drag or one label per Story, done in a batch at planning time. It also serves as the
design approval for small Stories: the person read the refined body before moving it.

# Caveats

- The kit source URLs use a placeholder owner; point them at the published kit.

[^applab]: AppLab backlog README, `/refine` and `/nightshift` sections.
[^kit-labels]: Kit model page, label families.
[^kit-claims]: Kit model page, inferred claims.
[^sk-implement]: Spec Kit implement command, step 2.
[^gh-projects-access]: GitHub Docs, project collaborator roles.
