---
type: Reference
title: timos-claude-code-plugins story-readiness gate and refine-issue
description: The most GitHub-native readiness gate found in 2026 is a read-only agent that returns READY or NEEDS_REFINEMENT from four checks, including native and acyclic blocked-by edges; its refine-issue skill walks an epic's native sub-issues with a person present.
resource: https://github.com/timo-jakob/timos-claude-code-plugins/tree/14cbf932262c24c694dde5f3085f3edf8067ae85/development
tags: [plugin, definition-of-ready, github-native, sub-issues, dependencies, human-gate]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: tm-readiness, title: "development/agents/story-readiness.md", resource: "https://github.com/timo-jakob/timos-claude-code-plugins/blob/14cbf932262c24c694dde5f3085f3edf8067ae85/development/agents/story-readiness.md", commit: 14cbf932262c24c694dde5f3085f3edf8067ae85, accessed: 2026-11-02 }
  - { id: tm-refine, title: "development/skills/refine-issue/SKILL.md", resource: "https://github.com/timo-jakob/timos-claude-code-plugins/blob/14cbf932262c24c694dde5f3085f3edf8067ae85/development/skills/refine-issue/SKILL.md", commit: 14cbf932262c24c694dde5f3085f3edf8067ae85, accessed: 2026-11-02 }
  - { id: tm-readme, title: "README.md", resource: "https://github.com/timo-jakob/timos-claude-code-plugins/blob/14cbf932262c24c694dde5f3085f3edf8067ae85/README.md", commit: 14cbf932262c24c694dde5f3085f3edf8067ae85, accessed: 2026-11-02 }
  - { id: tm-approver, title: "docs/explanation/claude-approver.md", resource: "https://github.com/timo-jakob/timos-claude-code-plugins/blob/14cbf932262c24c694dde5f3085f3edf8067ae85/docs/explanation/claude-approver.md", commit: 14cbf932262c24c694dde5f3085f3edf8067ae85, accessed: 2026-11-02 }
  - { id: tm-git, title: "Repository git history (first 2026-02-27, HEAD 2026-11-02, about 900 commits; gate added 2026-07-04)", resource: "https://github.com/timo-jakob/timos-claude-code-plugins/commits/14cbf932262c24c694dde5f3085f3edf8067ae85", commit: 14cbf932262c24c694dde5f3085f3edf8067ae85, accessed: 2026-11-02 }
  - { id: tm-page, title: "Repository page (stars, licence)", resource: "https://github.com/timo-jakob/timos-claude-code-plugins", accessed: 2026-11-02 }
---

# Why it is here

The task asked for newer GitHub-issues-native candidates from 2026. This is the
strongest one found. It reads and writes **native sub-issues** and **native blocked-by
edges**, not labels or checkbox lists.

# Provenance

| Fact | Value |
| --- | --- |
| Author | One person; MIT licence[^tm-page] |
| Stars / forks | 1 / 0 on 2026-11-02[^tm-page] |
| Activity | First commit 2026-02-27; about 900 commits; HEAD `14cbf93` on 2026-11-02. The gate agent was added 2026-07-04 and changed 2026-11-01[^tm-git] |
| Scope | A plugin family that bootstraps, maintains, reviews and ships repos, and pulls in a person "only when human judgment is genuinely required"[^tm-readme] |
| Bundled scripts | Many zsh helpers (about 160) that call `gh`; the repo also has its own CI workflows[^tm-git] |

# The story-readiness gate

It is a **read-only** agent. It returns a JSON verdict and nothing else. It never posts,
labels, branches or edits. The calling skill owns every GitHub write.[^tm-readiness]

`READY` holds only when every check that applies passes. Otherwise the verdict is
`NEEDS_REFINEMENT`, with the concrete questions that would unblock it:[^tm-readiness]

1. **Testable acceptance criteria.** "Improve performance" with no measurable outcome
   fails.
2. **Bounded scope.** One coherent unit with known files, not a programme that should
   be an epic. A size script can stop it by counting declared files.
3. **Dependencies declared natively, graph acyclic.** It fails in exactly two cases: a
   prerequisite mentioned only in prose with no native `blockedBy` edge, or a cycle. The
   check is deterministic.
4. **No contradictions.** No mutually exclusive requirements, and any machine-readable
   `story-spec/v1` block in the issue body must agree with the prose.
5. **Outside-in testability**, only for stories that touch a runtime surface (REST,
   gRPC, web UI, CLI). It needs a concrete use case, plus happy, corner and error test
   cases in that surface's own tool (`curl`, `grpcurl`, `playwright`, a CLI call), each
   filed as a linked `test-case` issue.

**Proportionality:** stories with no runtime surface (docs, chores, refactors) skip
check 5. This "keeps the existing backlog from a mass flip to NEEDS_REFINEMENT".[^tm-readiness]

**Borderline cases:** "lean toward NEEDS_REFINEMENT — a cheap clarifying question now
beats a wrong PR later."[^tm-readiness]

# The key idea: specification versus sequencing

> One fact, one owner.

The gate judges whether a dependency is **declared**. A separate build-time precheck
enforces **sequencing**: it rejects a build while a blocker is open, and on a cycle.
A story whose blockers are declared but still open is "**READY-but-queued**". "Never fail
a story ... solely because a declared blocker is open", because no refinement answer can
close a blocker.[^tm-readiness]

This avoids a common fault: marking well-written stories "not ready" only because the
work they wait on has not landed.

# refine-issue: the human-present loop

- It starts from an issue labelled `needs-refinement`. It runs the gate, then loops a
  refiner agent with a person until **the person approves a rewrite**. Then it writes the
  approved prose plus a provenance-stamped `story-spec` block, re-runs the gate, and
  removes the label **only if READY**.[^tm-refine]
- If a session cannot converge, it parks the issue with a typed reason:
  `needs-decision`, `split-recommended` or `deferred`.[^tm-refine]
- Pointed at an epic, it walks each `needs-refinement` child in native sub-issue order.
  The native sub-issues or the `epic` label decide what counts as an epic. A checkbox that
  only *mentions* an issue is an acceptance criterion, not a child.[^tm-refine]

# Gaps and risks

- No decomposition from a vision. It gates and refines stories that already exist.
- No Definition of Done artefact, and no Gherkin. Criteria are judged on substance:
  "a well-written prose story with no `## Acceptance` header can still be READY".[^tm-readiness]
- **Approval can be loosened.** There is an `--auto-accept <0..1>` threshold (default 1)
  and an unattended `--follow-up` mode.[^tm-refine] A separate "Claude Approver" judges PRs
  through its own GitHub App identities; it is now run locally by the user.[^tm-approver]
  Borrowing the gate text is fine. Do not borrow the auto-accept or Approver patterns
  where a person must merge.
- The skill text cites many of its own issue numbers. Strip them when you copy ideas.

# Caveats

- Adoption is minimal (1 star), and the repo changes daily. Treat it as a source of
  well-argued text, not a dependency.

[^tm-readiness]: development/agents/story-readiness.md
[^tm-refine]: development/skills/refine-issue/SKILL.md
[^tm-readme]: README.md
[^tm-approver]: docs/explanation/claude-approver.md
[^tm-git]: Repository git history (first 2026-02-27, HEAD 2026-11-02, about 900 commits; gate added 2026-07-04)
[^tm-page]: Repository page (stars, licence)
