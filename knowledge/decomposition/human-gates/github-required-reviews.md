---
type: Reference
title: GitHub required reviews
description: Branch protection or a ruleset can block a merge until enough write-access reviewers approve; authors cannot approve their own PRs, which shapes how a solo owner's agents must sign in.
tags: [github, branch-protection, rulesets, merge, enforceable]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: gh-protected, title: "GitHub Docs: About protected branches", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", accessed: 2026-11-02}
  - {id: gh-approve, title: "GitHub Docs: Approving a pull request with required reviews", resource: "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews", accessed: 2026-11-02}
  - {id: gh-rulesets, title: "GitHub Docs: About rulesets", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets", accessed: 2026-11-02}
  - {id: dsh-exec, title: "dsh-superagent-prototype: 003 Execution", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 003-execution.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
---

# The settings that matter

| Setting | Effect |
| --- | --- |
| Required approving reviews | a set number of approvals from people with write permission or a code owner[^gh-protected] |
| Dismiss stale approvals | approvals are dismissed when new commits change the diff[^gh-protected] |
| Require approval of the most recent reviewable push | "the most recent reviewable push must be approved by someone other than the person who pushed it"[^gh-protected] |
| Required status checks | must be `successful`, `skipped` or `neutral` before merge[^gh-protected] |
| Require conversation resolution | all PR comments resolved before merge[^gh-protected] |
| Do not allow bypassing | applies the rules to admins too; by default admins are exempt[^gh-protected] |

Rulesets layer with branch protection; all applicable rules apply, the most restrictive
wins.[^gh-rulesets] Rulesets can name bypass actors (roles, teams, GitHub Apps).[^gh-rulesets]

# Who can approve

- "Pull request authors cannot approve their own pull requests."[^gh-approve]
- You also cannot approve a Copilot-raised PR "if it was you who assigned Copilot to the
  issue to which the pull request relates."[^gh-approve] GitHub treats the delegating person
  like the author in that case.
- Only approvals from users with write (or admin) access count.[^gh-approve]

# The solo-owner problem

| Agent signs in as | Required review works? |
| --- | --- |
| the owner's own account | No. The owner is the author; only admin bypass merges |
| a separate bot or App identity | Yes. The owner is a valid reviewer, and "most recent push" approval works because the bot pushed |
| Copilot coding agent, assigned by the owner | No, per the rule above |

So the enforceable merge gate needs agents to push under **their own identity**. dsh-superagent
reaches the same place from the other side: an agent that enables auto-merge as itself is
recorded as the merger, so it never does.[^dsh-exec]

# Plan limits

Protected branches: public repos on Free; public and private on Pro, Team and
Enterprise.[^gh-protected] Rulesets in private repos need Pro, Team or Enterprise Cloud.[^gh-rulesets]
Bypass lists on branch protection need an organisation-owned repo.[^gh-protected]

# Open questions

- Whether GitHub extends the "you assigned it" rule to third-party agent Apps is not
  documented; only Copilot is named.

[^gh-protected]: GitHub Docs, About protected branches.
[^gh-approve]: GitHub Docs, Approving a pull request with required reviews.
[^gh-rulesets]: GitHub Docs, About rulesets.
[^dsh-exec]: dsh-superagent 003 Execution, Merging.
