---
type: Comparison
title: "Agentic methods: backlog decomposition vs execution decomposition"
description: What AI-DLC, Superpowers, Spec Kit and Kiro each give a GitHub-native board kit, split into backlog decomposition (Epic, Story) and execution decomposition (Task, step, gates).
tags: [comparison, agentic-methods, decomposition, epic, story, task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:10:00Z }
sources:
  - id: aidlc
    title: awslabs/aidlc-workflows, docs/guide and core/aidlc-common/stages
    resource: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2
    url: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: superpowers
    title: obra/superpowers, skills/
    resource: https://github.com/obra/superpowers/tree/v7.0.1/skills
    url: https://github.com/obra/superpowers/tree/v7.0.1/skills
    accessed: 2026-11-02
    version: v7.0.1
    commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
  - id: speckit
    title: github/spec-kit, templates/ and extensions/github
    resource: https://github.com/github/spec-kit/tree/v1.2.5
    url: https://github.com/github/spec-kit/tree/v1.2.5
    accessed: 2026-11-02
    version: v1.2.5
    commit: 4572a67fe0e72a6837e2d7bb0fda875bc41482e5
  - id: kiro
    title: Kiro docs, Specs and Feature specs
    resource: https://kiro.dev/docs/specs/feature-specs/
    url: https://kiro.dev/docs/specs/feature-specs/
    accessed: 2026-11-02
    version: "page updated 2026-08-04"
---

# Two kinds of decomposition

- **Backlog decomposition** cuts an outcome into items a person can prioritise, accept and
  track: Epic, Story, acceptance criteria, Definition of Done.
- **Execution decomposition** cuts one accepted item into work an agent can do and prove:
  plan, task, step, verification, review, merge.

A board kit needs both. None of the four methods gives both *and* a GitHub mapping.

# Side by side (pinned versions)

| | [AWS AI-DLC](aws-ai-dlc.md) v2.11.2 | [Superpowers](superpowers.md) v7.0.1 | [Spec Kit](github-spec-kit.md) v1.2.5 | [Kiro specs](kiro-specs.md) |
| --- | --- | --- | --- | --- |
| Top unit | Intent (one lifecycle run) | Design doc | Feature spec | Spec |
| Epic level | Replaced by Units of work | None | Feature spec acts as one | Spec acts as one |
| Story level | User stories `USx.y`, INVEST notes, MoSCoW | None | User stories P1..Pn with Independent Test | User stories in `requirements.md` |
| Criteria format | Given/When/Then recommended; `ACx.y.n` IDs | Test assertions in plan steps | Given/When/Then; measurable `SC-nnn` | EARS (WHEN … THE SYSTEM SHALL …) |
| Task level | Not tracked (code plans in the record dir) | Plan tasks with Files, Interfaces, checkbox steps | `Tnnn [P] [USn]` lines | Tasks and sub-tasks |
| Dependencies | Unit DAG as YAML, cycle-free | Interfaces (Consumes, Produces) | `[P]` marker, "depends on" text, phases | "dependencies" per task (not detailed) |
| Human gates | Every stage; plan, skeleton, verification command never waivable | Design HARD-GATE; plan review; integration choice | Review each step; Constitution Check gate | Gates between phases (Quick Spec skips them) |
| Done evidence | Verification command exit 0 + receipt + human approval | Fresh evidence before any claim | converge until `Converged` | Task status in the IDE |
| GitHub Issues | None | None | Opt-in: one flat issue per task | None found |

Sources: [^aidlc] [^superpowers] [^speckit] [^kiro]

# What each gives a board kit

| Method | Backlog decomposition | Execution decomposition |
| --- | --- | --- |
| AI-DLC | **Strong**: requirements → stories → Units with DAG and story map; traceability checked at phase boundaries | **Strong gates**, weak tracking: walking skeleton, one approved verification command, checkpoints, failure stops |
| Superpowers | **None** beyond "several independent projects, one at a time" | **Strongest**: right-sized tasks, Interfaces blocks, TDD iron law, per-task review, evidence rule, ledger |
| Spec Kit | **Good, one level**: feature → prioritised, independently testable stories | **Medium**: story-grouped task list, parallel marker, converge loop; flat issue export |
| Kiro | **Good, one level**: spec → stories with EARS criteria | **Medium**: tasks with sub-tasks, IDE status only |

# Consequences for the kit

1. Take **backlog** structure from AI-DLC and Spec Kit (stories with IDs, priorities,
   independent tests, criteria IDs) and keep the kit's own Epic level. AI-DLC's Unit is a
   build boundary; record it as a field or a dependency edge, not a new issue type.
2. Take **execution** structure from Superpowers (task right-sizing, Interfaces, evidence
   before claims) for the Task level and the agent's own plan.
3. Take **gates** from AI-DLC: design or plan approval, a walking-skeleton story first, one
   human-approved verification command per Epic, and a short list of approvals that
   autonomy never waives.
4. Supply what **none** of them supply: native sub-issues (Epic → Story → Task), issue
   types, Projects fields, and a universal Definition of Done. Spec Kit's converter is the
   only GitHub link, and it produces flat issues.
5. Keep criteria formats open: Given/When/Then (AI-DLC, Spec Kit) and EARS (Kiro) both
   appear; none of the four uses SMART by name.

# Caveats

- Versions move fast: Superpowers changed its task-size rule in 2026-09 and its review
  model in 2026-06; AI-DLC ships previews several times a week. Re-pin before quoting.
- Kiro rows rest on doc pages, not on files a reader can pin to a commit.
