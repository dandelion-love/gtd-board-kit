---
type: Decision
title: Name three risk levels and make the bot the board steward
description: Every act carries a named risk level that says whether to proceed or ask; one bot owns board hygiene, reckoning and retro notes; sessions run as named personas so a person can follow who did what.
tags: [contract, risk, steward, personas, hygiene]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-15T18:30:00Z }
---

# Context

People were asked to approve changes that were easy to undo and touched nobody outside
the team, which spends their attention for no safety gain. Separately, agents tidied the
board by hand while the periodic bot did the same sweeps, so each undid the other, and
retros and spend reports lived in chat where nobody could pick them up.

# Decision

## Risk levels

Every act has one level. Name it in the claim or report (`risk: R0|R1|R2`).

| Level | Meaning | Rule |
| --- | --- | --- |
| R0 reversible and internal | Undoable, and only the team sees it (branches, drafts, board fields, labels, new issues, PRs). | Proceed. Record the act and its undo. Never wait for a decision. |
| R1 reversible, outward | Undoable but others can see it or it costs something (comments on shared repos, spend above the lane budget, notifications to a person). | Proceed inside a standing grant or budget; otherwise ask once. |
| R2 irreversible or outward | Cannot be undone, or reaches users or money outside the team (production deploy, merge to the default branch, deleting data, public posts, secrets, policy changes). | Ask. Stop that item until a person answers. |

When two levels fit, take the higher. A person may name a standing grant that lowers a
class of act by one level; grants live only in the repo's `.gtd/BOARD.local.md` on the
default branch.

## One steward for board hygiene

The periodic board bot is the only writer of these fields; agents never hand-edit them and
the bot flags an agent edit as a conflict:

- closed items move to Done, Void or Abandoned;
- stale claims expire;
- Start (on first claim) and Target (from the queue) fill in;
- Priority inherits onto stories and blockers;
- items missing Size or Release are flagged;
- finished epics are closed or flagged;
- duplicate candidates are listed for a person, never closed automatically.

Each tick the bot also posts a daily and per-milestone reckoning (spend against budget,
throughput, items over estimate, WIP against the lane cap) on the repo's coordination
issue, and on each merged PR or recorded result it opens or appends a dated retro note
(time, tokens, rework, what to make a default). A retro finding with an action becomes a
captured item marked agent-proposed.

## Personas

`.gtd/BOARD.local.md` names a small roster. Each persona has a role, allowed acts, a lane
and a WIP cap equal to the lane capacity. Starter roster: Coordinator, Builder, Reviewer,
Card keeper, Cloud keeper, Steward (the bot). A session runs as one persona plus a short
handle ("Reviewer · Ren"), and claims, reports, signatures and session titles carry it.

# Consequences

Conformance gains checks: closed sweep leaves nothing outside Done, Void or Abandoned;
the daily reckoning exists; a merged PR yields a retro note; claims and reports show a
persona and handle; an agent edit to a steward-owned field is flagged.
