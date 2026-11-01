---
type: Decision
title: The kit is a public, pinned submodule
description: Every work repo pulls the kit in as a git submodule at .gtd/kit, pinned to a full commit; the kit is public so cloud agents can fetch it.
tags: [distribution]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T04:00:00Z }
---

# Decision

- Work repos add the kit as a submodule at `.gtd/kit`, pinned to a full commit, and link
  its skills into `.claude/skills` and `.codex/skills`. Moving the pin is a PR.
- The kit is **public**: a cloud agent session can fetch its own repo and public repos,
  but not a second private one, so a private kit would be empty in cloud sessions.
- Because it is public, **nothing private enters it**. A guard (`tools/public_guard.py`)
  runs on every commit and push, and in Claude Code before git and GitHub writes.

# Consequences

Repo-specific detail has to live somewhere else: see
[the per-repo layer](/decisions/per-repo-layer.md).
