---
type: Reference
title: Red Hat agile skill (toddward)
description: A text-only Claude skill that best teaches the split between per-story acceptance criteria and a project-wide Definition of Done, with an advocate-challenger-integrator debate per epic; it has no licence, so only its ideas can be borrowed.
resource: https://github.com/toddward/red-hat-agile-skill/tree/141eb736e4978166cd33287f67ca5a4423973852
tags: [skill, decomposition, acceptance-criteria, definition-of-done, invest]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: rh-skill, title: "SKILL.md at 141eb73", resource: "https://github.com/toddward/red-hat-agile-skill/blob/141eb736e4978166cd33287f67ca5a4423973852/SKILL.md", commit: 141eb736e4978166cd33287f67ca5a4423973852, accessed: 2026-11-02 }
  - { id: rh-decomp, title: "references/decomposition-agents.md at 141eb73", resource: "https://github.com/toddward/red-hat-agile-skill/blob/141eb736e4978166cd33287f67ca5a4423973852/references/decomposition-agents.md", commit: 141eb736e4978166cd33287f67ca5a4423973852, accessed: 2026-11-02 }
  - { id: rh-git, title: "Repository git history (4 commits, 2026-04-15 to 2026-04-23) and file tree", resource: "https://github.com/toddward/red-hat-agile-skill/commits/141eb736e4978166cd33287f67ca5a4423973852", commit: 141eb736e4978166cd33287f67ca5a4423973852, accessed: 2026-11-02 }
  - { id: rh-page, title: "Repository page (stars, licence shown)", resource: "https://github.com/toddward/red-hat-agile-skill", accessed: 2026-11-02 }
---

# Provenance

| Fact | Value |
| --- | --- |
| Author | One person (`toddward`). The name refers to the Six Hats "red hat", not to the company |
| Stars / forks | 3 / 0 on 2026-11-02[^rh-page] |
| Pinned commit | `141eb73`, 2026-04-23; 4 commits in all, the first on 2026-04-15[^rh-git] |
| Licence | **None.** The repo has no LICENSE file and the page shows none[^rh-page] [^rh-git] |
| Bundled files | `SKILL.md`, four reference files, `evals/evals.json`, and a `.skill` zip archive[^rh-git] |

The `.skill` zip dates from 2026-04-15, before the commit that split acceptance criteria
from Definition of Done (2026-04-23). Its `SKILL.md` is 12.8 kB; the live file is 17.0 kB.
So the zip is a stale copy of the skill.[^rh-git] It holds no scripts.

# Process

Three phases, each run as a chain of sub-agents:[^rh-skill]

1. **Discovery (First Principles).** A "Vision Archaeologist" reduces the vision to
   fundamental truths. A "Scope Architect" builds epics from those truths only, without
   seeing the original description, to avoid anchoring. A "Coverage Evaluator" checks the
   gaps.
2. **Elaboration (dialectical, per epic).** A Story Advocate proposes stories. A Story
   Challenger critiques them against INVEST and for gaps in acceptance criteria, DoD fit
   and value. A Story Integrator finalises them. Then tasks are written, each with a
   completion criterion.
3. **Validation (Six Hats, short form).** White, Black, Yellow, Red and Blue hats give
   completeness, risk, value, a gut check and a synthesis.

A scope table scales the process down for small projects. A 1-2 sprint project skips
the Scope Architect and runs only the White and Black hats.[^rh-skill]

# The part worth borrowing: AC versus DoD

| | Acceptance criteria | Definition of Done |
| --- | --- | --- |
| Scope | This story only | Every story |
| Form | Given/When/Then (preferred) or numbered testable statements | Checklist of team standards |
| Changes per story | Yes | No; set once per project |

"A story is **accepted** when its AC pass. A story is **done** when it's accepted AND the
project DoD is satisfied."[^rh-skill]

Rules from the AC quality checklist:[^rh-skill]

- observable behaviour, not implementation;
- happy path, error paths and **at least one boundary case**;
- one interpretation only; a tester can write a test from it directly;
- a criterion that applies only to some stories belongs in AC, not DoD;
- "performance is acceptable" becomes a threshold ("200 ms P95 under 100 concurrent
  requests").

Every Epic, Story and Task also carries an **intrinsic value** statement on one of four
dimensions: user, business, technical or learning impact. A task may inherit its value
from its story.[^rh-skill]

# Gaps

- **No human gate.** Validation is a debate between agents; nothing waits for a person
  to sign off.
- **No Definition of Ready.** INVEST is checked by the Challenger, but there is no
  ready/not-ready verdict.
- **Dependencies** are a per-story field and a per-epic "dependency map" in prose.[^rh-decomp]
- **No tracker.** The output is one markdown plan. Nothing touches GitHub.
- **Sizing by sprint.** Stories fit "a single sprint (1-2 weeks)" and tasks "1-3 days".[^rh-skill]
  For agent work, a smaller unit is more useful (see [BMAD](bmad-method.md)).

# Caveats

- **Licence.** With no licence, the default is all rights reserved. Restate the AC/DoD
  distinction in your own words; do not copy the text. This corrects the first sweep's
  "borrow as template".
- The first sweep said SMART's Time-bound and Achievable are not named. That is right:
  the only measurability rule is the performance-threshold example.

[^rh-skill]: SKILL.md at 141eb73
[^rh-decomp]: references/decomposition-agents.md at 141eb73
[^rh-git]: Repository git history (4 commits, 2026-04-15 to 2026-04-23) and file tree
[^rh-page]: Repository page (stars, licence shown)
