---
type: Reference
title: GitHub environments with required reviewers
description: A deployment environment can hold a workflow job until a named reviewer approves it; enforceable, but on Free, Pro and Team only for public repositories.
tags: [github, environments, deployment, enforceable]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: gh-env, title: "GitHub Docs: Deployments and environments", resource: "https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments", accessed: 2026-11-02}
---

# What it does

| Rule | Effect |
| --- | --- |
| Required reviewers | up to six users or teams; one approval lets the job run[^gh-env] |
| Prevent self-review | the user who started the deployment cannot approve it[^gh-env] |
| Wait timer | delay a job 1 to 43,200 minutes (30 days)[^gh-env] |
| Deployment branches and tags | none, protected branches only, or name patterns[^gh-env] |
| Admin bypass | on by default; can be disallowed[^gh-env] |

# Plan limits

On Free, Pro and Team, required reviewers and wait timers exist **only for public
repositories**.[^gh-env] A private work repo on those plans cannot use this gate.

# Use as a gate

It gates an **action**, not a decision about scope: deploy, publish, release, or any job
with outside effects. That matches the "side effect outside this worktree" class that
should always stop an agent (see [merge gate](merge-approval-gate.md)). It is the one GitHub
gate a person can approve from a phone notification with the evidence (the run) one click
away.

# Caveats

- Creating or editing workflow files is off-limits for agents in many repos; an
  environment gate must be set up by a person.
- Prevent self-review only helps if the agent, not the owner, starts the run.[^gh-env]

[^gh-env]: GitHub Docs, Deployments and environments.
