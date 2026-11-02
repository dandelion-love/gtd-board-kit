---
type: Pattern
title: Claims and leases
description: Before work starts an agent claims the item through the server, which records who holds it and until when; first claim wins.
tags: [board, claims]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T04:00:00Z }
---

# Rule

- **Claim before work.** The server stamps the claimant's identity; no tool takes an
  identity argument.
- **First claim wins.** A second claim is refused while the first holder's lease runs.
  After the lease ends, a new claim is a takeover that names the old holder.
- **Every claim says why**: `explicit` when a person or coordinator pointed the agent at
  the item, `inferred` when a pull rule allowed it. An inferred claim needs
  `agent-ready`, a small Size, and no routing label naming someone else.
- **Scope is fixed** to the item as claimed. New work becomes a new item. A
  [standing lane](/decisions/standing-lanes.md) fixes a class of work instead, and each
  item it takes is still claimed with its own fixed scope.
- **Claim every item you work.** An agent may work several stories at once, and the
  session that owns them may combine them on one integration branch. Each story still
  has its own claim and lease; no claim covers several items, and no commit lands for
  a story its committer does not hold. A claim may record the `branch` its work lands on.
- A lane's own item is held for as long as the lane runs; its lease is the heartbeat.
- **Renew** before the lease ends; **release** with what is done, what remains and the
  next step.

The states a holder reports are in [report vocabulary](/model/report-vocabulary.md).
