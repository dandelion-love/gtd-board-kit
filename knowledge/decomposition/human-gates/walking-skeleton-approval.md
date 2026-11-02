---
type: Pattern
title: Walking skeleton approval
description: The first, smallest end-to-end slice of an Epic must pass a real check and be approved by a person before the other slices start.
tags: [gates, walking-skeleton, epic, human-approval]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: aidlc-phases, title: "AI-DLC guide: Phases and stages (2.11.2)", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 04-phases-and-stages.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523, version: 2.11.2}
  - {id: aidlc-first, title: "AI-DLC guide: Your first workflow", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 02-your-first-workflow.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523}
---

# What it is

With skeleton-on, AI-DLC makes the first Unit in the dependency graph "the smallest working
integrated slice". Its code must run through a real end-to-end check, and the person
approves the verified skeleton before later Units begin, even in stage-major order.[^aidlc-phases]
"A first design-stage review alone is not a working skeleton."[^aidlc-phases]

# The parts that make it cheap

- **One command, chosen once.** Delivery Planning proposes a Construction Verification
  Command and the person authorizes it; it is reused for every later Unit checkpoint. A
  command picked at verify time does not count.[^aidlc-phases]
- **Proof, not prose.** The approval question shows "Verified with `<command>` (exit 0)",
  and approval needs a tool-written receipt; a hand-written proof file cannot verify a Unit.[^aidlc-phases]
- **Autonomy offered after it.** With skeleton-on, the "Continue automatically / Review each
  checkpoint" offer comes only after the real skeleton checkpoint.[^aidlc-phases]

# Mapping to Epic, Story, Task

| AI-DLC | Board |
| --- | --- |
| Intent | outcome above the Epic |
| first DAG Unit (skeleton) | the Epic's first Story, flagged as skeleton |
| verification command | one command recorded on the Epic |
| skeleton approval | merge of the skeleton Story's PR by a person, after the command passed |

Only the skeleton gets a design-level look at running code. Later Stories ride on the
[merge gate](merge-approval-gate.md).

# Why it matters for one owner

It is a single, early, concrete gate per Epic. It catches a wrong architecture while one
slice is built, not five. It also converts trust into a reusable check, so later gates can
be lighter.

# Caveats

- The walkthrough shows the same pattern on a sample project; it is AWS's own example,
  not an independent evaluation.[^aidlc-first]

[^aidlc-phases]: AI-DLC Phases and stages, "Why Construction works the way it does".
[^aidlc-first]: AI-DLC Your first workflow, Construction section.
