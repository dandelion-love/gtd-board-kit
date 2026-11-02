---
type: Pattern
title: Design or spec approval gate
description: A person approves a written design or spec before any agent builds; the cheapest gate to pass and the most expensive one to skip.
tags: [gates, design, spec, human-approval]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: sp-brainstorm, title: "Superpowers: brainstorming skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b, version: 7.0.1}
  - {id: sk-workflow, title: "Spec Kit: default speckit workflow with gates", resource: "https://github.com/github/spec-kit/blob/7370e592f3cd9c06e5b698983957e227c75b30e2/workflows/speckit/workflow.yml", accessed: 2026-11-02, commit: 7370e592f3cd9c06e5b698983957e227c75b30e2, version: 1.2.5}
  - {id: sk-wf-readme, title: "Spec Kit: Workflows README (gate steps)", resource: "https://github.com/github/spec-kit/blob/7370e592f3cd9c06e5b698983957e227c75b30e2/workflows/README.md", accessed: 2026-11-02, commit: 7370e592f3cd9c06e5b698983957e227c75b30e2}
  - {id: sk-catalog, title: "Spec Kit: community workflow catalog", resource: "https://github.com/github/spec-kit/blob/7370e592f3cd9c06e5b698983957e227c75b30e2/workflows/catalog.community.json", accessed: 2026-11-02, commit: 7370e592f3cd9c06e5b698983957e227c75b30e2}
  - {id: kiro-feature, title: "Kiro docs: Feature specs", resource: "https://kiro.dev/docs/specs/feature-specs/", accessed: 2026-11-02}
  - {id: aidlc-phases, title: "AI-DLC guide: Phases and stages (2.11.2)", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 04-phases-and-stages.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523, version: 2.11.2}
  - {id: aidlc-modes, title: "AI-DLC guide: Interaction modes", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 07-interaction-modes.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523}
---

# What it is

A person reads a written design (or spec) and approves it before an agent writes product
code. It sits at the Epic or Story level: it fixes *what* and *why*, not *how*.

# How the methods do it

| Method | The gate | Can it be skipped? |
| --- | --- | --- |
| Superpowers | `HARD-GATE`: nothing is built until the person approves the design doc; building includes scaffolding and installing dependencies[^sp-brainstorm] | Yes, if the person opted out of questions; an approved throwaway spike may be built, and keeping it is a new request[^sp-brainstorm] |
| Spec Kit | Default workflow: `gate` step "Review the generated spec before planning", options approve / reject, `on_reject: abort`[^sk-workflow][^sk-wf-readme] | Yes: a community workflow "Full SDD Cycle - no gates" runs without review gates[^sk-catalog] |
| Kiro | Feature specs move Requirements → Design → Tasks (or Design-first) with approval gates between phases[^kiro-feature] | Yes: Quick Spec "runs all three phases automatically without approval gates"[^kiro-feature] |
| AI-DLC | Every stage outside Initialization ends with an Approve / Request Changes gate[^aidlc-phases] | Only by an explicit machine-wide bypass flag; scope and settings cannot lower a gate that is put to you[^aidlc-phases] |

# Design points worth keeping

- **Approval covers only what was shown.** Superpowers lists "they said 'sounds good' to the
  idea" as a red flag: an unwritten design is not approved.[^sp-brainstorm]
- **Bounded revision.** After three rounds of Request Changes on one stage, AI-DLC adds a
  third option, **Accept as-is**, so the loop cannot run forever.[^aidlc-modes]
- **A skip switch is normal.** Every method except AI-DLC offers a no-gate path for small or
  well-understood work. The gate is a default, not a law.

# For a GitHub board

The design lives in the Epic or Story issue body (or a linked doc). The approval is a
person's act on that issue. See [ready hand move](ready-hand-move-gate.md) for how the same
act can double as the design approval for small Stories.

# Caveats

- Kiro's page does not name which click is the approval; "Continue" between phases is
  inferred from the Quick Spec wording.[^kiro-feature]

[^sp-brainstorm]: Superpowers brainstorming skill, HARD-GATE and Red Flags.
[^sk-workflow]: Spec Kit workflow.yml, gate steps after specify and plan.
[^sk-wf-readme]: Spec Kit Workflows README, Gate Steps.
[^sk-catalog]: Spec Kit community workflow catalog.
[^kiro-feature]: Kiro Feature specs page, Quick Spec tip.
[^aidlc-phases]: AI-DLC Phases and stages, "Which stops you always get".
[^aidlc-modes]: AI-DLC Interaction modes, 3-strike revision escape hatch.
