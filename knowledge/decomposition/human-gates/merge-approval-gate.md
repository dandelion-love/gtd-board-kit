---
type: Pattern
title: Merge approval gate
description: A person, never the agent, decides whether a finished branch is merged; it is the one gate GitHub can enforce, with a catch for solo owners.
tags: [gates, merge, pull-request, human-approval]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: sp-finish, title: "Superpowers: finishing-a-development-branch skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/finishing-a-development-branch/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b, version: 7.0.1}
  - {id: sp-sdd, title: "Superpowers: subagent-driven-development skill", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b}
  - {id: applab, title: "AppLab backlog plugin README (v1.3.0)", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/README.md", accessed: 2026-11-02, commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, version: 1.3.0}
  - {id: dsh-exec, title: "dsh-superagent-prototype: 003 Execution", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 003-execution.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
---

# What it is

The agent's work ends as a branch or PR. A person chooses: merge, keep, or discard.

# How the methods do it

| Method | Merge decision |
| --- | --- |
| Superpowers | Present exactly three options: merge locally, push and open a PR, keep as-is; discard only when the person explicitly asks, after confirming[^sp-finish]. A merge or push to a shared branch is one of the four things that stop an executing agent[^sp-sdd] |
| AppLab nightshift | One draft PR per ticket, so each can be shipped, delayed or rejected alone; the preview branch that merges them all gets no PR, "so nobody can merge the whole night in one click"[^applab] |
| dsh-superagent | By default the agent never enables auto-merge as its own account, because GitHub attributes the merge to whoever enabled it; without a named merge account, people merge[^dsh-exec] |
| AI-DLC | PR and merge sit outside the method (team convention) |

# Prompt rule vs host rule

dsh-superagent says it plainly: its merge conditions "govern the agent, not GitHub's merge
rules. To enforce approvals, require them in branch protection and dismiss stale
approvals."[^dsh-exec] A merge gate written only in an agent prompt is conventional. The
enforceable form is [required reviews](github-required-reviews.md).

# The solo-owner catch

A PR author cannot approve their own PR. If the agent pushes and opens PRs **as the owner**,
a required-review rule can never be met except by admin bypass. See
[required reviews](github-required-reviews.md) for the options.

# Keep it cheap

- One PR per Story, small diff, evidence in the body (test output, screenshots). AppLab's
  test plan and dsh's "honest delivery" rules both make the PR self-explaining.[^applab][^dsh-exec]
- Draft until the agent's own [done check](done-acceptance-gate.md) passes, so a person is
  only asked when there is something to accept.

[^sp-finish]: Superpowers finishing-a-development-branch, Step 4.
[^sp-sdd]: Superpowers subagent-driven-development, the four stop reasons.
[^applab]: AppLab backlog README, `/nightshift` section.
[^dsh-exec]: dsh-superagent 003 Execution, Merging.
