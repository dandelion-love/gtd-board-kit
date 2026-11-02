---
type: Reference
title: GitHub CODEOWNERS
description: A file that names owners for paths so they are requested automatically, and, with the matching branch rule, must approve changes to those paths.
tags: [github, codeowners, review, enforceable]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: gh-codeowners, title: "GitHub Docs: About code owners", resource: "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners", accessed: 2026-11-02}
  - {id: gh-protected, title: "GitHub Docs: About protected branches", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", accessed: 2026-11-02}
---

# What it does

- Owners are requested automatically when a PR changes their paths; **not** for draft PRs,
  but they are notified when the draft is marked ready.[^gh-codeowners]
- With "Require review from Code Owners", a PR touching owned code must be approved by an
  owner.[^gh-protected]
- Owners must have write permission.[^gh-codeowners] The file lives in `.github/`, the root
  or `docs/`, first found wins, and must be under 3 MB.[^gh-codeowners]

# Plan limits

Free plans support code owners only in public repos; Pro, Team and Enterprise support both
public and private.[^gh-codeowners]

# Use for one owner with agents

With one human, every path has the same owner, so CODEOWNERS adds little over a plain
[required review](github-required-reviews.md). Its value is **path-scoped strictness**:

| Path | Why own it |
| --- | --- |
| agent rules, CI config, the CODEOWNERS file itself | changes here widen what agents may do |
| policy files that switch lanes or accept modes | a merge here is an authorisation |

Draft PRs do not request owners, which fits the [done check](done-acceptance-gate.md):
the owner is asked only when the agent marks the PR ready.[^gh-codeowners]

# Caveats

- The docs do not say whether an author who is also the only code owner satisfies the
  code-owner rule; with the author-cannot-approve rule, assume not.[^gh-codeowners]

[^gh-codeowners]: GitHub Docs, About code owners.
[^gh-protected]: GitHub Docs, Require review from Code Owners.
