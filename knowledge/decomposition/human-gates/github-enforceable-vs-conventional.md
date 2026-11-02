---
type: Comparison
title: GitHub gate mechanisms, enforceable vs conventional
description: Which GitHub mechanisms the platform enforces against an agent with write access, which only work if the agent obeys, and what each costs the owner.
tags: [github, gates, enforcement, comparison]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: gh-protected, title: "GitHub Docs: About protected branches", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", accessed: 2026-11-02}
  - {id: gh-approve, title: "GitHub Docs: Approving a pull request with required reviews", resource: "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews", accessed: 2026-11-02}
  - {id: gh-rulesets, title: "GitHub Docs: About rulesets", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets", accessed: 2026-11-02}
  - {id: gh-codeowners, title: "GitHub Docs: About code owners", resource: "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners", accessed: 2026-11-02}
  - {id: gh-env, title: "GitHub Docs: Deployments and environments", resource: "https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments", accessed: 2026-11-02}
  - {id: gh-projects-access, title: "GitHub Docs: Managing access to your projects", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-access-to-your-projects", accessed: 2026-11-02}
  - {id: gh-form-schema, title: "GitHub Docs: Syntax for GitHub's form schema", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema", accessed: 2026-11-02}
  - {id: gh-roles, title: "GitHub Docs: Repository roles for an organization", resource: "https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization", accessed: 2026-11-02}
  - {id: dsh-exec, title: "dsh-superagent-prototype: 003 Execution", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 003-execution.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
---

# Table

"Enforced" means GitHub refuses the action from an agent account with write access that
ignores its instructions.

| Mechanism | Gates | Enforced? | Plan limit (private repo) | Owner cost |
| --- | --- | --- | --- | --- |
| [Required reviews](github-required-reviews.md) + stale dismissal + most-recent-push | merge | **yes**, unless the actor is an admin and bypass is allowed[^gh-protected] | Pro / Team or above[^gh-protected] | one review per PR |
| Required status checks | merge | **yes**[^gh-protected] | same | none (machine) |
| [CODEOWNERS](github-codeowners.md) + code-owner review | merge of owned paths | **yes**[^gh-protected] | Pro or above[^gh-codeowners] | none extra for one owner |
| Rulesets | merge, push | **yes**, with a bypass list[^gh-rulesets] | Pro / Team / Enterprise Cloud[^gh-rulesets] | setup only |
| [Environment reviewers](github-environment-required-reviewers.md) | deploy / outside-effect job | **yes**[^gh-env] | public only on Free, Pro, Team[^gh-env] | one click per run |
| [Issue form required fields](github-issue-forms.md) | issue shape | public repos, web form only[^gh-form-schema] | not enforced | none |
| [Projects status move](github-projects-status-move.md) | ready → pickup | **no**: whole-project roles[^gh-projects-access] | — | one drag |
| [Labels](github-labels-as-signals.md) | ready, hold, needs | **no**: triage and above can label[^gh-roles] | — | one click |
| Agent prompt / skill rule | anything | **no**; dsh: prompt merge rules "govern the agent, not GitHub's merge rules"[^dsh-exec] | — | none |

# Reading it

- **Only merge and deploy can be enforced.** Everything before merge (design, ready, plan)
  is a convention the agent must keep.
- Enforcement needs the agent to have **its own identity**: an author cannot approve their
  own PR.[^gh-approve]
- On a Free private repo none of the enforceable rows are available. The gate set must
  then rest on conventions plus an after-the-fact check (a scheduled audit that flags
  merges or `agent-ready` labels made by agent accounts).

# Make conventions checkable

A conventional gate is acceptable when a violation is **visible and attributable**: labels
(actor in timeline) beat status moves (history unreliable), and a check that compares the
actor to a list of agent accounts turns a silent breach into a flagged one.

[^gh-protected]: GitHub Docs, About protected branches.
[^gh-approve]: GitHub Docs, Approving a pull request with required reviews.
[^gh-rulesets]: GitHub Docs, About rulesets.
[^gh-codeowners]: GitHub Docs, About code owners.
[^gh-env]: GitHub Docs, Deployments and environments.
[^gh-projects-access]: GitHub Docs, project roles.
[^gh-form-schema]: GitHub Docs, form schema validations.
[^gh-roles]: GitHub Docs, repository roles.
[^dsh-exec]: dsh-superagent 003 Execution, Merging.
