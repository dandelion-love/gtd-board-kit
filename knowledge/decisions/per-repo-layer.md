---
type: Decision
title: Each repo customises in its own layer
description: A repo's labels, columns, boards, channels and rules live in its own .gtd/BOARD.local.md and repo-owned skills, which win over the kit except on two rules.
tags: [customisation]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T04:00:00Z }
---

# Decision

- `.gtd/BOARD.local.md` in the work repo is read right after the kit's `BOARD.md` and
  wins where they differ. It can never relax "board only through the MCP server" or the
  hard limits.
- A real folder at `.claude/skills/<name>` replaces the kit skill of that name.
- Onboarding (`ONBOARDING.md`) drafts the layer from the repo and the board at run time,
  so the kit never needs to know any repo's details.
