---
type: Reference
title: AWS AI-DLC (AI-Driven Development Life Cycle), workflows v2.11.2
description: AWS's AI-DLC method and its open-source workflow engine, verified at release v2.11.2, with what each concept maps to in Epic, Story and Task and where it deliberately does not.
resource: https://github.com/awslabs/aidlc-workflows
tags: [reference, agentic-methods, spec-driven, decomposition, approval-gates]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:50:00Z }
sources:
  - id: aws-blog
    title: "AI-Driven Development Life Cycle: Reimagining Software Engineering (AWS DevOps Blog, Raja SP, 2025-07-31)"
    resource: https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/
    url: https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/
    accessed: 2026-11-02
  - id: aidlc-readme
    title: aidlc-workflows README
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/README.md
    url: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/README.md
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-changelog
    title: aidlc-workflows CHANGELOG, entry 2.11.2 (2026-10-28)
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/CHANGELOG.md
    url: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/CHANGELOG.md
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-phases
    title: "User Guide: Phases and Stages (file 04-phases-and-stages.md in docs, guide folder)"
    resource: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    url: https://awslabs.github.io/aidlc-workflows/
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-glossary
    title: "User Guide: Glossary (docs/guide/glossary.md)"
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/docs/guide/glossary.md
    url: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/docs/guide/glossary.md
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-profiles
    title: "User Guide: Workflow Profiles (docs/guide/workflow-profiles.md)"
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/docs/guide/workflow-profiles.md
    url: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/docs/guide/workflow-profiles.md
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-scopes
    title: "User Guide: Scopes, Depth, and Test Strategy (file 05-scopes-and-depth.md in docs, guide folder)"
    resource: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    url: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-interaction
    title: "User Guide: Interaction Modes (file 07-interaction-modes.md in docs, guide folder)"
    resource: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    url: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-intents
    title: "User Guide: Spaces and Intents (file 03-spaces-and-intents.md in docs, guide folder)"
    resource: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    url: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-audit
    title: "User Guide: State Tracking and Audit Trail (file 10-state-and-audit.md in docs, guide folder)"
    resource: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    url: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/guide
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-units
    title: "Stage 2.7 Units Generation (core/aidlc-common/stages/inception/units-generation.md)"
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/core/aidlc-common/stages/inception/units-generation.md
    url: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/core/aidlc-common/stages/inception/units-generation.md
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-stories
    title: "Stage 2.4 User Stories (core/aidlc-common/stages/inception/user-stories.md)"
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/core/aidlc-common/stages/inception/user-stories.md
    url: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/core/aidlc-common/stages/inception/user-stories.md
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-story-patterns
    title: "Product agent knowledge: User Story Patterns and Requirements Guide (core/knowledge/aidlc-product-agent/)"
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/core/knowledge/aidlc-product-agent/user-story-patterns.md
    url: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/core/knowledge/aidlc-product-agent
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-delivery
    title: "Stage 2.9 Delivery Planning (core/aidlc-common/stages/inception/delivery-planning.md) and the Developer Reference chapter on Inception stages (docs, reference folder)"
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/core/aidlc-common/stages/inception/delivery-planning.md
    url: https://github.com/awslabs/aidlc-workflows/tree/v2.11.2/docs/reference
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
  - id: aidlc-buildtest
    title: "Stage 3.6 Build and Test (core/aidlc-common/stages/construction/build-and-test.md)"
    resource: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/core/aidlc-common/stages/construction/build-and-test.md
    url: https://github.com/awslabs/aidlc-workflows/blob/v2.11.2/core/aidlc-common/stages/construction/build-and-test.md
    accessed: 2026-11-02
    version: v2.11.2
    commit: 10a9bc9d85395a601de2624cf5bdd35292c10db4
---

# Pin

| Item | Value |
| --- | --- |
| Repository | `awslabs/aidlc-workflows`, licence MIT-0[^aidlc-readme] |
| Latest stable release | tag `v2.11.2`, commit `10a9bc9d85395a601de2624cf5bdd35292c10db4`, 2026-10-28[^aidlc-changelog] |
| Newer previews (not used here) | `v2.11.3-preview.20261029.1`, `v2.11.3-preview.20261030.1` |
| Default branch head on 2026-11-02 | `c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523` (newer than the release) |
| Guide site | `awslabs.github.io/aidlc-workflows`, built from `docs/guide/`; the site shows no version number[^aidlc-phases] |

Read every number below as true **at v2.11.2**. The project ships previews several times a
week, so pin the release tag, not "v2".

# What it is

Two things share the name:

1. **The method**, from the AWS DevOps Blog post of 2025-07-31 by Raja SP.[^aws-blog] AI
   "creates a plan, asks clarifying questions to seek context, and implements solutions
   only after receiving human validation". The post names three phases: **Inception,
   Construction, Operations**. It names **Mob Elaboration** (Inception) and **Mob
   Construction** (Construction). It states "Epics are replaced by Units of Work" and that
   sprints are replaced by **bolts**, "shorter, more intense work cycles measured in hours
   or days rather than weeks". It reports no measured results.[^aws-blog]
2. **The workflow engine**, `aidlc-workflows` v2: "one harness-neutral core" that runs
   natively in Claude Code, Kiro CLI, Kiro IDE, Codex CLI, Cursor, opencode and GitHub
   Copilot, installed with a native `aidlc` command.[^aidlc-readme]

# Structure at v2.11.2

| Fact | Value | Source |
| --- | --- | --- |
| Phases | 5: Initialization (0), Ideation (1), Inception (2), Construction (3), Operation (4) | [^aidlc-glossary] |
| Stages | 33: 3 + 7 + 9 + 7 + 7 | [^aidlc-phases] |
| Agents | 14: 11 domain experts, 2 reviewers, 1 adaptive composer | [^aidlc-readme] |
| Workflow profiles (engine word: scope) | 11: enterprise, feature, mvp, poc, bugfix, refactor, infra, security-patch, classic, workshop, express | [^aidlc-glossary] |
| Audit | 126 event types in 26 categories, append-only per-clone shards | [^aidlc-audit] |
| Stage topology | 29 inline, 2 subagent, 1 pipeline, 1 mob | [^aidlc-phases] |

The blog's three phases sit inside the engine's five: the engine adds Initialization
(automatic, no gates) and Ideation in front.[^aidlc-phases]

Profile sizes (stages after Initialization's three, out of 30): feature 30, enterprise 30,
workshop 23, mvp 20, classic 15, infra 10, express 7, refactor 7, security-patch 7,
bugfix 6, poc 5.[^aidlc-profiles] Inside Ideation, `poc` runs only Intent Capture; it still
runs other stages after Ideation.[^aidlc-phases]

# Key concepts, verified

| Concept | What v2.11.2 says | Source |
| --- | --- | --- |
| **Intent** | "A single run of the AI-DLC lifecycle, scoped to one task." A row in `intents.json` (`uuid, slug, dirName, scope, repos, status`) plus a record dir holding state, audit trail and artifacts. Status: `in-flight`, `complete`, `archived`. | [^aidlc-intents] |
| **Unit of work** | "The WHAT: an independently implementable piece of the solution", made in stage 2.7. Each Unit has a name, boundaries, responsibilities, deployment model, size S/M/L/XL and a kind (`service`, `spec`, `ui`, `packaging`, `library`), in a cycle-free dependency graph (a fenced YAML edge block) with integration points. | [^aidlc-glossary] [^aidlc-units] |
| **Bolt** | "A planned Construction delivery slice over one or more dependency-linked Units", with a Definition of Done, a confidence hypothesis and ownership. "Runtime order follows the Unit DAG"; `bolt-plan.md` does not replace it. "Bolt ≠ sprint ≠ MMF." No duration is set in the engine. | [^aidlc-glossary] [^aidlc-delivery] |
| **Walking skeleton** | "The smallest working integrated slice, planned as the first DAG Unit when skeleton-on." It must pass the recorded, human-authorised verification command and get human approval before later Units begin. | [^aidlc-glossary] [^aidlc-phases] |
| **Construction Verification Command** | One intent-level check, proposed in Delivery Planning, approved by the human, reused at every Unit or batch checkpoint. A tool-owned receipt binds the approval to the command's SHA-256. | [^aidlc-glossary] [^aidlc-phases] |
| **Mob elaboration** | Stage 2.4 User Stories is the one shipped mob: the lead drafts, "mutually blind collaborators" write contribution files in parallel, the lead integrates, in bounded rounds. **With collaborators off, which is every shipped scope except `enterprise`, the lead runs alone, with no mob round.** | [^aidlc-glossary] [^aidlc-stories] |
| **Mob construction** | Named in the blog only. No v2.11.2 stage is a construction mob; parallel Construction is "swarm" (stage-major, dependency-ready Units in worktrees) or team mode (each person claims a Unit). | [^aws-blog] [^aidlc-phases] |
| **Approval gates** | "Every stage your scope runs, outside Initialization, ends with an approval gate." Options: Approve or Request Changes; after three rounds of changes a third option, **Accept as-is** ("Archive current version and move on"), appears. | [^aidlc-phases] [^aidlc-interaction] |
| **What autonomy cannot waive** | "Continue automatically" waives ordinary Construction checkpoints, but Plan Approval, an enabled summary confirmation, the verification command choice, skeleton approval and failures still need the human. | [^aidlc-phases] [^aidlc-glossary] |
| **Phase boundary verification** | At Ideation→Inception, Inception→Construction and Construction→Operation, automated checks for missing artifacts, broken traceability links, orphans and inconsistency. | [^aidlc-phases] |
| **Depth** | Minimal, Standard, Comprehensive: how much detail each stage writes. | [^aidlc-glossary] |
| **Test strategy** | Minimal ("Nyquist model", one test per requirement, about 5-15 tests), Standard (5-8 tests per component, unit and integration), Comprehensive (10-15 tests per component, all types). Independent of depth; "soft guideline". | [^aidlc-scopes] |
| **Traceability** | Three artifacts: a requirements traceability matrix (Req ID, Design Ref, Unit Ref, Test Ref; empty cell = gap) in the product agent's knowledge; `traceability.json` in stage 2.7 (each story or FR mapped `OK` to one Unit, or `GAP`); and a **Target Verification Matrix** in stage 3.6 (Target ID, Source, Expected, Actual, Evidence, Owning Stage, Verdict). | [^aidlc-story-patterns] [^aidlc-units] [^aidlc-buildtest] |

## Stories and acceptance criteria inside AI-DLC

- Stories use "As a [persona], I want [goal], so that [benefit]", with IDs `US{group}.{seq}`
  and criteria IDs `AC{group}.{seq}.{n}`, MoSCoW priority and "INVEST compliance notes".[^aidlc-stories]
- The story plan offers "Breakdown approach options — By feature, by persona, by
  workflow, by domain area, **by epic**".[^aidlc-stories]
- The product agent's knowledge lists the six **INVEST** criteria, recommends
  Given/When/Then, "3-6 acceptance criteria per story", the sad path, and names the
  anti-pattern "Too Large (Epic in Disguise)".[^aidlc-story-patterns]
- SMART is not used by name (no match in the repo at this tag).

# Mapping to Epic, Story, Task

| AI-DLC | Board kit level | Fit |
| --- | --- | --- |
| Intent | Outcome above Epic, or an Epic for a single-feature run | Partial. An Intent is one lifecycle run with its own record and audit, not a backlog item. |
| Unit of work | Epic-sized or Story-sized slice, cut by build and test boundary | **Deliberate non-map.** The blog replaces Epics with Units. A Unit is a bounded build target, not a theme. One Epic theme usually becomes several Units. |
| User story (`USx.y`) | Story | Direct. Each story traces to one Unit in `traceability.json`; the story map also allows rows that span several Units (cross-cutting). |
| Acceptance criterion (`ACx.y.n`) | Story acceptance criteria | Direct. |
| Bolt | Delivery cycle or milestone, not an issue type | Partial. A Bolt groups Units with a DoD; the DAG, not the Bolt, sets order. |
| Walking skeleton | First Story or first Unit, gated | Direct as a rule: first slice is end-to-end and human-approved. |
| Code-plan steps in 3.5 Code Generation | Task | **No tracked Task level.** Plans live in the record dir; nothing becomes a tracked item. |
| Construction Verification Command and checkpoint receipt | Definition of Done check per Story | Partial. One command for the whole intent, plus human approval. |

# What it does not supply

- No issue tracker, board or GitHub Issues stage. Artifacts "travel with the code, in the
  same repo and the same pull requests".[^aidlc-intents] There is no PR step in the method.
- No universal Definition of Done checklist. Done is layered: Bolt DoD, Unit checkpoint
  (command exit 0 plus human approval), phase boundary verification.[^aidlc-delivery] [^aidlc-phases]
- No tracked Task level below Units and stories.

# What a board kit can borrow

- The **dependency graph as data** (a YAML edge block, cycle-free), kept separate from the
  delivery order.[^aidlc-units]
- The **walking-skeleton gate** before parallel work.
- One **human-authorised verification command**, reused at every checkpoint.
- The **list of decisions autonomy cannot waive**.
- The **3-strike Accept as-is** escape hatch against endless revision.
- Story and criterion **IDs** that traceability can check mechanically.

See [Superpowers](superpowers.md), [GitHub Spec Kit](github-spec-kit.md),
[Kiro specs](kiro-specs.md) and the comparison
[backlog vs execution decomposition](backlog-vs-execution-decomposition.md).

# Caveats

First-sweep claims checked against v2.11.2 and the blog:

| First-sweep claim | Finding |
| --- | --- |
| "2.11 engine line in October 2026" | Confirmed: v2.11.2 released 2026-10-28; README badge 2.11.2. Was "secondary sources" only; now primary. |
| 5 phases, 33 stages; AWS method names 3 | Confirmed. |
| "proof of concept running only Intent Capture" | **Imprecise.** `poc` runs only Intent Capture *within Ideation*; it runs 5 stages after Initialization. |
| Intent is "an outcome in the requester's own words" | **Not how v2.11.2 defines it.** An Intent is one lifecycle run scoped to one task. The engine does keep the request "in your own words" in the record (CHANGELOG 2.11.2), which may be the source of the phrase. |
| Unit of work at stage 2.7, fields, S-XL, kind, DAG | Confirmed. |
| "An Epic, in AI-DLC's critique, is a theme bucket" | **Not found.** The blog says only "Epics are replaced by Units of Work". "Theme bucket" is the first sweep's wording. |
| Bolt "hours or days" | Blog only. The v2 engine sets no duration. |
| "two-week sprint becomes a reporting calendar only" | **Not found** in the blog or the repo. |
| Bolt "expected demo" | Confirmed for the skeleton Bolt; each Bolt has DoD and confidence hypothesis. |
| Mob elaboration "the whole team ... in one sitting" | **Overstated for v2.** It is a parallel agent round; off in every shipped scope except enterprise. |
| "Solo Mob exists, with the single human as arbiter" | **Not found** in v2.11.2. |
| Mob construction | Blog only; not a v2 stage. |
| Approval gate, "recorded in the approver's own words as an audit shard" | Confirmed in substance (reply read in own words; audit shards per clone). |
| Archive-and-move-on after three revision rounds | Confirmed ("Accept as-is"). |
| Waiver does not remove plan approval, skeleton approval, verification command, failure handling | Confirmed. |
| Test volume Minimal / Standard / Comprehensive | Confirmed. |
| "Target Verification Matrix showing which test proves which requirement" | **Partly.** The 3.6 matrix is per *target* (Expected vs Actual with Evidence); requirement-to-test mapping is the separate traceability matrix and `traceability.json`. |
| "each story maps to exactly one Unit" | Confirmed for `traceability.json`; the story map also allows cross-cutting rows. |
| v2 "does not use INVEST by name" | **Wrong.** Stage 2.4 asks for "INVEST compliance notes"; the product knowledge lists all six INVEST criteria. |
| v2 "does not mandate one format" for criteria | Confirmed: Given/When/Then is recommended in knowledge files, not enforced by a sensor found here. |
| Does not use SMART by name | Confirmed. |
| Gartner's term "AI-native software engineering" | Not checked: no primary source in scope for this track. |

# Open questions

- Is the blog's "Mob Construction" still part of the method AWS teaches, or only of the
  original post? The v2 repo has no stage of that name.
- The README links an "AI-DLC Workflows 2.0 Specification" PDF in `assets/`; it was not
  read for this note.
