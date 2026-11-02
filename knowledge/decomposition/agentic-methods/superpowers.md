---
type: Reference
title: Superpowers (obra/superpowers), v7.0.1
description: Jesse Vincent's skills-based development method for coding agents, verified at v7.0.1; strong execution decomposition (design, plan, task, step), no backlog levels.
resource: https://github.com/obra/superpowers
tags: [reference, agentic-methods, execution-decomposition, tdd, verification]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:00Z }
sources:
  - id: sp-readme
    title: Superpowers README
    resource: https://github.com/obra/superpowers/blob/v7.0.1/README.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/README.md
    accessed: 2026-11-02
    version: v7.0.1
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-notes
    title: Superpowers RELEASE-NOTES.md (entries v6.4.2 and later)
    resource: https://github.com/obra/superpowers/blob/v7.0.1/RELEASE-NOTES.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/RELEASE-NOTES.md
    accessed: 2026-11-02
    version: v7.0.1
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-brainstorming
    title: skills/brainstorming/SKILL.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/brainstorming/SKILL.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/skills/brainstorming/SKILL.md
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-writing-plans
    title: skills/writing-plans/SKILL.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/writing-plans/SKILL.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/skills/writing-plans/SKILL.md
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-writing-plans-old
    title: skills/writing-plans/SKILL.md before v6.4.2 (parent of commit 8ca22db)
    resource: https://github.com/obra/superpowers/blob/8ca22db~1/skills/writing-plans/SKILL.md
    url: https://github.com/obra/superpowers/commit/8ca22db
    accessed: 2026-11-02
    commit: 8ca22db
  - id: sp-sdd
    title: skills/subagent-driven-development/SKILL.md and task-reviewer-prompt.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/subagent-driven-development/SKILL.md
    url: https://github.com/obra/superpowers/tree/v7.0.1/skills/subagent-driven-development
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-executing
    title: skills/executing-plans/SKILL.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/executing-plans/SKILL.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/skills/executing-plans/SKILL.md
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-tdd
    title: skills/test-driven-development/SKILL.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/test-driven-development/SKILL.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/skills/test-driven-development/SKILL.md
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-verify
    title: skills/verification-before-completion/SKILL.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/verification-before-completion/SKILL.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/skills/verification-before-completion/SKILL.md
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-finishing
    title: skills/finishing-a-development-branch/SKILL.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/finishing-a-development-branch/SKILL.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/skills/finishing-a-development-branch/SKILL.md
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-review
    title: skills/requesting-code-review/SKILL.md and skills/receiving-code-review/SKILL.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/requesting-code-review/SKILL.md
    url: https://github.com/obra/superpowers/tree/v7.0.1/skills
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-using
    title: skills/using-superpowers/SKILL.md and hooks/session-start
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/using-superpowers/SKILL.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/hooks/session-start
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: sp-worktrees
    title: skills/using-git-worktrees/SKILL.md
    resource: https://github.com/obra/superpowers/blob/v7.0.1/skills/using-git-worktrees/SKILL.md
    url: https://github.com/obra/superpowers/blob/v7.0.1/skills/using-git-worktrees/SKILL.md
    accessed: 2026-11-02
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
---

# Pin

| Item | Value |
| --- | --- |
| Repository | `obra/superpowers`, MIT, "Copyright (c) 2025 Jesse Vincent" |
| Release | `v7.0.1`, commit `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`, 2026-10-21 (also default-branch head on 2026-11-02) |
| First commit | 2025-10-09 |
| Authors | "built by Jesse Vincent and the rest of the folks at Prime Radiant"[^sp-readme] |

The skills changed a lot in 2026 (see Caveats). Quote the skill files at a pinned commit,
not the README, which lags them.

# What it is

"A complete software development methodology for your coding agents, built on top of a set
of composable skills and some initial instructions that make sure your agent uses
them."[^sp-readme] A session-start hook injects the `using-superpowers` skill, which says:
"IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT."[^sp-using]
It installs as a plugin in many harnesses, including Anthropic's official Claude plugin
marketplace and the official Codex plugin marketplace.[^sp-readme]

# The chain, at v7.0.1

| # | Skill | What it does | Gate |
| --- | --- | --- | --- |
| 1 | brainstorming | Lay out 2-3 approaches, human picks one; size the work (small change: short design; project: full design); write the design doc to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`; a fresh "builder check" subagent reads it first.[^sp-brainstorming] | **HARD-GATE:** "Nothing gets built until your human partner approves the design doc".[^sp-brainstorming] |
| 2 | using-git-worktrees | Asks consent, then an isolated worktree; runs setup and a test baseline. "If tests fail: Report failures, ask whether to proceed or investigate."[^sp-worktrees] | Human consent; baseline. |
| 3 | writing-plans | Plan to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`; self-review; hand to the human.[^sp-writing-plans] | Human reviews the plan and picks Subagent-driven or Native execution. |
| 4a | subagent-driven-development | "a fresh implementer subagent per task, a task review (spec compliance + code quality) after each, and a broad whole-branch review at the end."[^sp-sdd] | Per-task reviewer; no pauses between tasks. |
| 4b | executing-plans | Inline: "no implementer subagent per task, no reviewer per task. One fresh-context review of the whole branch at the end."[^sp-executing] | TDD per task; one final review. |
| 5 | test-driven-development | "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST". "Write code before the test? Delete it. Start over."[^sp-tdd] | Iron law. |
| 6 | requesting / receiving-code-review | Mandatory after each SDD task, after a major feature, before merge. "Fix Critical issues immediately. Fix Important issues before proceeding. Note Minor issues for later."[^sp-review] Receiving: "Verify before implementing. Ask before assuming."[^sp-review] | Critical and Important both block. |
| 7 | finishing-a-development-branch | "Verify tests → Detect environment → Present options → Execute choice → Clean up." Three options: merge locally, push and open a PR, keep as-is. Discard only on explicit request.[^sp-finishing] | Human chooses integration. |
| — | verification-before-completion | "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"[^sp-verify] | Applies to any claim, any time. |

# The plan task format (verified)

Plan header (every plan): **Goal** (one sentence), **Architecture**, **Tech Stack**,
**Spec** (path to the design doc), **Global Constraints** (exact values copied verbatim
from the spec), **Review Focus** (five uncovered input classes or failure modes, each
pinned by a test in its owning task).[^sp-writing-plans]

Each task:

| Field | Content |
| --- | --- |
| `### Task N: [Component Name]` | Title |
| **Files** | Create / Modify (with line ranges) / Test, exact paths |
| **Interfaces** | Consumes (exact signatures from earlier tasks), Produces (names and types later tasks rely on) |
| Steps, as `- [ ]` checkboxes | Write the failing test; run it, expected FAIL; implement the exact signature; run it, expected PASS; commit |

Sizing rules:

- "A task is the smallest unit that carries its own test cycle and is worth a fresh
  reviewer's gate." Split "only where a reviewer could meaningfully reject one task while
  approving its neighbor."[^sp-writing-plans]
- "Each step is one action with a checkable result."[^sp-writing-plans]
- "A plan is the set of decisions the implementer cannot make alone. A plan longer than the
  code it describes has written the code instead."[^sp-writing-plans]
- Lines that decide nothing ("TBD", "handle edge cases") are the opposite
  failure.[^sp-writing-plans]

There is **no per-task "Acceptance Criteria" field and no per-task "Goal"**. The criteria
are the test assertions in the steps; the verification step is a command plus the output
that means it passed.

# Verification before completion (wording)

The gate function, verbatim in substance:[^sp-verify]

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Make the claim

"Skip any step = lying, not verifying." Its table includes "Agent completed | VCS diff
shows changes | Agent reports 'success'" and "Requirements met | Line-by-line checklist |
Tests passing".[^sp-verify]

# Decomposition model

Design → (independent sub-projects, brainstormed one at a time) → plan → task → step.
Brainstorming says: "If this is really several independent projects, say so, agree on an
order, and brainstorm them one at a time."[^sp-brainstorming] Writing-plans adds: one plan
per subsystem, "Each plan should produce working, testable software on its
own."[^sp-writing-plans]

There is no epic, story, backlog, sprint, Definition of Done or issue-tracker concept in
the skills (no match in `skills/` at v7.0.1, except "acceptance criteria" as an input to
the implementer prompt).[^sp-sdd]

# Mapping to Epic, Story, Task

| Superpowers | Board kit level | Fit |
| --- | --- | --- |
| A design doc (project) / independent sub-project | Epic, or one Story for a small change | Partial: one design per sub-project; no hierarchy above it. |
| A plan | The implementation plan of one Story | Good: "working, testable software on its own". |
| A plan task | Task (sub-issue or checklist item) | Good: own test cycle, reviewable alone. |
| A step | Checklist line inside a task | Too small to track as an issue. |
| Review Focus, Global Constraints | Story-level non-functional criteria | Useful as story fields. |
| verification-before-completion | Definition of Done evidence rule | Strong; not a DoD checklist itself. |

# What a board kit can borrow

- Design approval as a hard gate before any building.
- The task-sizing rule (own test cycle, separately rejectable), not a minutes figure.
- The Interfaces block, so parallel workers see only their own task.
- A recovery ledger on disk (`progress.md`), and `Ruling:` lines for decisions made
  without stopping.[^sp-sdd]
- The four stop conditions during execution: irreversible or destructive operation,
  security-sensitive action, side effect outside the worktree (merge, push to a shared
  branch, publish), plan too broken to proceed.[^sp-sdd]
- The evidence table of verification-before-completion.

Do not borrow: the missing backlog levels, or the full loop for a change the brainstorming
skill itself calls "a quick, clear task".[^sp-brainstorming]

See [AWS AI-DLC](aws-ai-dlc.md) and the comparison
[backlog vs execution decomposition](backlog-vs-execution-decomposition.md).

# Caveats

First-sweep claims checked against v7.0.1:

| First-sweep claim | Finding |
| --- | --- |
| MIT, Jesse Vincent with Prime Radiant, created October 2025 | Confirmed (first commit 2025-10-09). |
| Distributed through Anthropic's Claude Code marketplace; supports Codex, Cursor, OpenCode, Gemini CLI | Confirmed (README lists 16 harnesses). |
| Session-start bootstrap makes skills mandatory | Confirmed. |
| "2 to 5 minute tasks" | **Outdated.** Before v6.4.2 the skill sized each **step**, not task, at "2-5 minutes".[^sp-writing-plans-old] v6.4.2 (2026-09-25) replaced it with "one action with a checkable result".[^sp-notes] The README still says "2-5 minutes each".[^sp-readme] |
| Each task has "complete code or signatures" | **Changed in v6.4.2.** Signatures, test assertions and spec values; a body only for an algorithm the signature and tests do not determine.[^sp-notes] The README still says "complete code". |
| Per-task fields "Goal, Files, Acceptance Criteria, Verify step, TDD steps" | **Wrong at v7.0.1.** Goal is plan-level; per task: Files, Interfaces, checkbox steps. No Acceptance Criteria field was found in the skill's history either. |
| Plan must be executable "with no session history and no spec in front of it" | **Changed.** The header now carries the Spec path: "executors read both".[^sp-writing-plans] The old "zero context" wording was dropped in v6.4.2.[^sp-notes] |
| Two-stage review, spec compliance then code quality | **Changed.** Since 2026-06 one task reviewer returns two verdicts (spec, then quality) on one read of the diff.[^sp-sdd] |
| executing-plans as the "cheaper path" | Confirmed; it now has no per-task reviewer, one final review. |
| Finishing offers merge, PR, keep, or discard | **Partly.** The menu has three options; discard happens only if asked.[^sp-finishing] |
| Critical review issues block progress | Confirmed, and Important issues also block.[^sp-review] |
| "If the baseline fails, ask the human" | Confirmed.[^sp-worktrees] |
| Explicit go signal before subagent execution | Confirmed: the human reviews the plan and picks the method.[^sp-writing-plans] |
| No SMART, INVEST or story-level template | Confirmed. |

# Open questions

- The README and the skills disagree on task size and code in plans. Which does the
  author consider current? (The skills are newer, per the release notes.)
- v6.4.2 reports "9/9 against planted-defect probes" for the leaner plans; this is the
  author's own test, not an independent measure.[^sp-notes]
