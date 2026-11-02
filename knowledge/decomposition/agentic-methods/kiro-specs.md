---
type: Reference
title: Kiro specs (requirements, design, tasks)
description: Kiro's spec-driven workflow, three files per spec with EARS-notation requirements, verified from the official Kiro docs pages as updated in 2025-2026.
resource: https://kiro.dev/docs/specs/
tags: [reference, agentic-methods, spec-driven, ears, decomposition]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:05:00Z }
sources:
  - id: kiro-specs
    title: Kiro docs, Specs (overview, markdown index)
    resource: https://kiro.dev/docs/specs.md
    url: https://kiro.dev/docs/specs.md
    accessed: 2026-11-02
  - id: kiro-concepts
    title: Kiro docs, Specs concepts
    resource: https://kiro.dev/docs/specs/concepts
    url: https://kiro.dev/docs/specs/concepts
    accessed: 2026-11-02
    version: "page updated 2025-11-10"
  - id: kiro-feature
    title: Kiro docs, Feature specs
    resource: https://kiro.dev/docs/specs/feature-specs/
    url: https://kiro.dev/docs/specs/feature-specs/
    accessed: 2026-11-02
    version: "page updated 2026-08-04"
---

# Pin

Kiro is a closed-source product; its spec workflow is documented only on `kiro.dev`. Pin by
page date: concepts page updated 2025-11-10,[^kiro-concepts] feature-specs page updated
2026-08-04.[^kiro-feature] Pages were read through a fetch tool that summarises; quotes
below are short phrases it returned verbatim.

# What it is

"Specs or specifications are structured artifacts that formalize the development
process" for features and bug fixes.[^kiro-specs] Each spec has three files:[^kiro-specs] [^kiro-concepts]

| File | Holds |
| --- | --- |
| `requirements.md` (`bugfix.md` for a bugfix spec) | "user stories and acceptance criteria in structured EARS notation" |
| `design.md` | "technical architecture, sequence diagrams, and implementation considerations" |
| `tasks.md` | "a detailed implementation plan with discrete, trackable tasks" |

# Spec types and variants

- **Feature specs** and **Bugfix specs**.[^kiro-specs]
- Feature specs run **Requirements-First** (Requirements → Design → Tasks) or
  **Design-First** (Design → Requirements → Tasks).[^kiro-feature]
- **Quick Spec** generates all three files "without approval gates" between
  phases,[^kiro-specs] which implies the normal flow has them; the pages do not say how
  they work.

# EARS

EARS is "Easy Approach to Requirements Syntax". Kiro's pattern: "WHEN [condition/event]
THE SYSTEM SHALL [expected behavior]".[^kiro-feature] EARS itself is an older
requirements-engineering notation, not Kiro's invention (no primary EARS source was read
for this note).

# Tasks

Tasks have sub-tasks, each with "a clear description, expected outcome, and any necessary
resources or dependencies"; the IDE shows them as in-progress or completed.[^kiro-concepts]
The pages read do not show how a task links back to a requirement.

# Mapping to Epic, Story, Task

| Kiro | Board kit level | Fit |
| --- | --- | --- |
| A spec (feature) | Epic or large Story | Good. |
| User story with EARS criteria | Story with acceptance criteria | Direct; EARS is an alternative to Given/When/Then. |
| Task and sub-task in `tasks.md` | Task and checklist item | Direct, but tracked in the IDE, not in an issue tracker. |

AI-DLC also ships a Kiro harness, so the two can run together: see
[AWS AI-DLC](aws-ai-dlc.md). Comparison:
[backlog vs execution decomposition](backlog-vs-execution-decomposition.md).

# Caveats

- No GitHub Issues export was found in the pages read.
- The first sweep did not cover Kiro specs; nothing to confirm or refute.

# Open questions

- What does a Kiro `tasks.md` look like on disk (requirement references, optional tasks)?
  A sample generated spec would answer it.
