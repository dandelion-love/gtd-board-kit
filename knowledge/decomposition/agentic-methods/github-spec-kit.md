---
type: Reference
title: GitHub Spec Kit, v1.2.5
description: GitHub's spec-driven development toolkit, verified at v1.2.5; a feature spec with prioritised user stories, a plan, and a task list grouped by story, with an opt-in task-to-issue converter.
resource: https://github.com/github/spec-kit
tags: [reference, agentic-methods, spec-driven, decomposition]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - id: sk-readme
    title: Spec Kit README
    resource: https://github.com/github/spec-kit/blob/v1.2.5/README.md
    url: https://github.com/github/spec-kit/blob/v1.2.5/README.md
    accessed: 2026-11-02
    version: v1.2.5
    commit: 4572a67fe0e72a6837e2d7bb0fda875bc41482e5
  - id: sk-commands
    title: Spec Kit command templates (templates/commands/*.md)
    resource: https://github.com/github/spec-kit/tree/v1.2.5/templates/commands
    url: https://github.com/github/spec-kit/tree/v1.2.5/templates/commands
    accessed: 2026-11-02
    version: v1.2.5
    commit: 4572a67fe0e72a6837e2d7bb0fda875bc41482e5
  - id: sk-spec-template
    title: templates/spec-template.md
    resource: https://github.com/github/spec-kit/blob/v1.2.5/templates/spec-template.md
    url: https://github.com/github/spec-kit/blob/v1.2.5/templates/spec-template.md
    accessed: 2026-11-02
    version: v1.2.5
    commit: 4572a67fe0e72a6837e2d7bb0fda875bc41482e5
  - id: sk-plan-template
    title: templates/plan-template.md
    resource: https://github.com/github/spec-kit/blob/v1.2.5/templates/plan-template.md
    url: https://github.com/github/spec-kit/blob/v1.2.5/templates/plan-template.md
    accessed: 2026-11-02
    version: v1.2.5
    commit: 4572a67fe0e72a6837e2d7bb0fda875bc41482e5
  - id: sk-tasks-template
    title: templates/tasks-template.md
    resource: https://github.com/github/spec-kit/blob/v1.2.5/templates/tasks-template.md
    url: https://github.com/github/spec-kit/blob/v1.2.5/templates/tasks-template.md
    accessed: 2026-11-02
    version: v1.2.5
    commit: 4572a67fe0e72a6837e2d7bb0fda875bc41482e5
  - id: sk-github-ext
    title: extensions/github README and speckit.github.taskstoissues command
    resource: https://github.com/github/spec-kit/tree/v1.2.5/extensions/github
    url: https://github.com/github/spec-kit/blob/v1.2.5/extensions/github/README.md
    accessed: 2026-11-02
    version: v1.2.5
    commit: 4572a67fe0e72a6837e2d7bb0fda875bc41482e5
---

# Pin

| Item | Value |
| --- | --- |
| Repository | `github/spec-kit`, MIT, "Copyright GitHub, Inc." |
| Release | `v1.2.5`, commit `4572a67fe0e72a6837e2d7bb0fda875bc41482e5`, 2026-10-28 |
| Default-branch head on 2026-11-02 | `7370e592f3cd9c06e5b698983957e227c75b30e2` |

# The flow

Minimal flow: `/speckit-constitution`, `/speckit-specify`, `/speckit-plan`,
`/speckit-tasks`, `/speckit-implement`, `/speckit-converge`. "Repeat implement and
converge until convergence reports `Converged`." The constitution is made once per
project; the rest repeats per feature. The README asks you to review each result before
continuing.[^sk-readme]

| Command | Purpose (from its template) |
| --- | --- |
| constitution | Create or update the project's principles |
| specify | Feature spec from a natural-language description |
| clarify | Up to 5 targeted questions, answers written back into the spec |
| plan | Design artifacts from the plan template |
| checklist | A custom checklist for the feature |
| tasks | "an actionable, dependency-ordered tasks.md" |
| analyze | Non-destructive consistency check across spec, plan and tasks |
| implement | Execute the tasks |
| converge | Compare code with spec, plan and tasks; append unbuilt work as new tasks |
| taskstoissues | **Deprecated** in core; moved to the opt-in `github` extension |

All rows: [^sk-commands]

# What the artifacts hold

- **Spec**: user stories, each with a priority (P1, P2, P3), "Why this priority", an
  **Independent Test**, and Given/When/Then acceptance scenarios; functional
  requirements `FR-001`…; mandatory measurable **Success Criteria** `SC-001`…; at most
  three `[NEEDS CLARIFICATION]` markers.[^sk-spec-template] [^sk-commands]
- **Plan**: a **Constitution Check**, "GATE: Must pass before Phase 0 research. Re-check
  after Phase 1 design."[^sk-plan-template]
- **Tasks**: format `[ID] [P?] [Story] Description`, e.g. `T012 [P] [US1] Create ...`;
  `[P]` means parallel-safe; phases Setup, Foundational ("No user story work can begin
  until this phase is complete"), then one phase per user story with a checkpoint, so
  each story can be "Implemented independently, Tested independently, Delivered as an MVP
  increment". Tests are optional unless the spec asks for them.[^sk-tasks-template]

# GitHub issues

The `github` extension is opt-in (`specify init` does not install it). Its
`speckit.github.taskstoissues` command reads `tasks.md`, stops unless the remote is
GitHub, de-duplicates by task ID against open and closed issues, and creates one issue
per task titled `T001: <description>`.[^sk-github-ext] It creates flat issues; no
sub-issues, story parents, types or Projects fields were found in the command.

# Mapping to Epic, Story, Task

| Spec Kit | Board kit level | Fit |
| --- | --- | --- |
| Constitution | Project rules (repo-level, not an issue) | Good. |
| Feature spec (`specs/NNN-feature/`) | Epic | Good: one feature, many stories. |
| User story with priority and Independent Test | Story | Good: independently testable slice. |
| Acceptance scenario (Given/When/Then) | Story acceptance criteria | Direct. |
| Success criteria `SC-nnn` | Epic or Story outcome measure | Measurable; close to SMART's M. |
| Task `Tnnn [US1]` | Task | Direct, but the issue converter drops the story link. |
| Setup / Foundational phases | Enabler tasks with no story | Partial. |

See [AWS AI-DLC](aws-ai-dlc.md), [Kiro specs](kiro-specs.md) and the comparison
[backlog vs execution decomposition](backlog-vs-execution-decomposition.md).

# Caveats

| First-sweep claim | Finding |
| --- | --- |
| constitution, specify, plan, tasks, implement, with clarify, analyse and checklist | Confirmed; v1.2.5 adds **converge**. |
| "a newer task-to-issues conversion" | Confirmed, but the core command is now **deprecated** in favour of the opt-in `github` extension. |
| "its native unit is a task list from a spec, not Epic, Story, Task with criteria" | **Too strong.** The spec has prioritised user stories with acceptance scenarios, and tasks are grouped and tagged by story. What is missing is the mapping onto GitHub's hierarchy: issues are flat, one per task. |
| Actively maintained | Confirmed (release on 2026-10-28, commits on 2026-10-30). |
