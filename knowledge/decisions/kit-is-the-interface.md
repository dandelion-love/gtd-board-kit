---
type: Decision
title: The kit is the interface; each repo is an implementation
description: The kit defines what GitHub's native constructs mean on a board; each adopting repo binds them to its own labels, fields and views and keeps the contract.
tags: [customisation, contract]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T06:10:00Z }
---

# Decision

- **Respect the native construct.** Work is an issue, its state is its labels, fields
  and open or closed, the queue is a view's card order, the ETA is a date field, and
  order between items is a blocked-by link. A person can change any of them in the GitHub
  UI or API, and agents follow on their next read. Agents never keep a second copy.
- **The kit holds the general meaning** (the contract): what a claim, a lane, a queue,
  an ETA, a grant mean and how an agent must treat them.
- **Each repo holds the specific meaning** (the implementation) in its
  [own layer](/decisions/per-repo-layer.md): which label, field, view and issue type play
  each role. A research repo's lane takes experiments; a software repo's takes stories.
- An implementation may narrow or rename, never break the contract: it can't relax the
  MCP-only rule or the hard limits beyond a [workflow grant](/decisions/workflow-grants.md).

# Consequences

- Kit text names roles and placeholders, never one repo's labels or boards, which also
  keeps the public kit free of private detail.
- New kit features arrive as a contract plus a template block for the repo to fill.

See [queue and ETA](/model/queue-and-eta.md).
