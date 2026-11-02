---
type: Pattern
title: Plan approval gate
description: A person reviews the agent's implementation plan, the how, before execution starts; methods disagree on whether it is mandatory.
tags: [gates, planning, human-approval]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: sp-plans, title: "Superpowers: writing-plans skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/writing-plans/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b, version: 7.0.1}
  - {id: sp-sdd, title: "Superpowers: subagent-driven-development skill", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b}
  - {id: aidlc-phases, title: "AI-DLC guide: Phases and stages (2.11.2)", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 04-phases-and-stages.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523, version: 2.11.2}
  - {id: sk-workflow, title: "Spec Kit: default speckit workflow", resource: "https://github.com/github/spec-kit/blob/7370e592f3cd9c06e5b698983957e227c75b30e2/workflows/speckit/workflow.yml", accessed: 2026-11-02, commit: 7370e592f3cd9c06e5b698983957e227c75b30e2}
  - {id: kiro-autopilot, title: "Kiro docs: Autopilot and Supervised modes", resource: "https://kiro.dev/docs/ide/chat/autopilot/", accessed: 2026-11-02}
---

# What it is

The design says what; the plan says how: files, interfaces, tasks, verification. A plan gate
asks the person to read that before code is written.

# How the methods do it

| Method | Plan gate | Notes |
| --- | --- | --- |
| Superpowers | After the plan is saved, ask the person to review it and choose an execution method (subagent-driven or native); wait before implementation[^sp-plans] | Once running, the agent does **not** pause between tasks; it records rulings and stops only for four things[^sp-sdd] |
| AI-DLC | Plan Approval per Unit in Construction; survives "Continue automatically"[^aidlc-phases] | It is a ceremony switch: it can be turned off for the work[^aidlc-phases] |
| Spec Kit | Default workflow gate: "Review the plan before generating tasks"[^sk-workflow] | Same approve / reject / abort shape as the spec gate |
| Kiro | The Tasks phase follows the Design phase; Supervised mode also stops after each turn with file edits, with per-file and per-hunk accept[^kiro-autopilot] | Autopilot (the default) asks for no per-step approval[^kiro-autopilot] |

# Assessment for a solo owner

- A plan is long and technical. It is the gate most likely to be
  [rubber-stamped](approval-fatigue-and-rubber-stamping.md).
- AI-DLC already treats it as optional, while it keeps skeleton approval, the verification
  command choice and failures as non-waivable.[^aidlc-phases] That ordering is a useful hint:
  **a check you can run beats a plan you must read.**
- For a Story-sized change, fold the plan into the PR description and review it at merge.
  Keep a separate plan gate for Epics, or for Stories that touch shared contracts.

# Open questions

- No method in this set measured whether plan review catches defects that merge review
  misses. The recommendation above is judgement, not evidence.

[^sp-plans]: Superpowers writing-plans, Execution Handoff.
[^sp-sdd]: Superpowers subagent-driven-development, "Continuous execution" and "Rulings, not stalls".
[^aidlc-phases]: AI-DLC Phases and stages, "Which stops you always get".
[^sk-workflow]: Spec Kit workflow.yml, gate after plan.
[^kiro-autopilot]: Kiro Autopilot page, Supervised mode.
