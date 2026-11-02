---
type: Reference
title: Keel backlog-refinement skill
description: A refinement skill that runs INVEST as six pass/fail checks, turns each acceptance criterion into an atomic Gherkin test with a measurable Then, and proposes but never sets the ready state; its storage is a SysML engine, not GitHub.
resource: https://github.com/williamweatherholtz/keel/tree/5015c2de05c5709154b8513005e87e5a1fe331d2/.claude/skills/backlog-refinement
tags: [skill, refinement, definition-of-ready, gherkin, invest]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: keel-skill, title: ".claude/skills/backlog-refinement/SKILL.md (v0.2.0)", resource: "https://github.com/williamweatherholtz/keel/blob/5015c2de05c5709154b8513005e87e5a1fe331d2/.claude/skills/backlog-refinement/SKILL.md", commit: 5015c2de05c5709154b8513005e87e5a1fe331d2, accessed: 2026-11-02 }
  - { id: keel-readme, title: "Keel README", resource: "https://github.com/williamweatherholtz/keel/blob/5015c2de05c5709154b8513005e87e5a1fe331d2/README.md", commit: 5015c2de05c5709154b8513005e87e5a1fe331d2, accessed: 2026-11-02 }
  - { id: keel-git, title: "Repository git history (first 2026-06-03, HEAD 2026-10-30; skill last changed 894e394, 2026-08-21)", resource: "https://github.com/williamweatherholtz/keel/commit/894e39460c4cabb6a86fe80254a5ff5d35f6ffc1", commit: 894e39460c4cabb6a86fe80254a5ff5d35f6ffc1, accessed: 2026-11-02 }
  - { id: keel-page, title: "Repository page (stars, licence)", resource: "https://github.com/williamweatherholtz/keel", accessed: 2026-11-02 }
---

# Provenance

| Fact | Value |
| --- | --- |
| Author | One person; MIT licence[^keel-page] |
| Stars / forks | 1 / 0 on 2026-11-02[^keel-page] |
| Activity | About 1,585 commits from 2026-06-03 to 2026-10-30. The skill last changed on 2026-08-21[^keel-git] |
| Pinned commit | `5015c2d` (HEAD, 2026-10-30) |
| Skill version | `metadata.version: 0.2.0`, `writePolicy: pr-only`[^keel-skill] |
| Bundled scripts | None in the skill folder. It drives the `keel` CLI, which you install as a prebuilt binary from releases or build from source[^keel-readme] |

Keel is a "work-tracking engine built on SysML v2 text files", where "the AI drives the
CLI; the human supervises".[^keel-readme]

# What the skill does

It takes one existing Story, Epic or Task and works through these steps:[^keel-skill]

1. **Scan for anti-patterns first.** There are seven: criteria as a text blob, an
   unverifiable Then, a horizontal slice, an epic posing as a story, a hidden dependency,
   "ready" with no size, and a non-Fibonacci estimate.
2. **Six INVEST checks**, each pass or fail, each with a fixed fix:
   - I fails: add a `dependency` edge;
   - E fails: open a spike;
   - S fails: split, or promote to Epic, and stop there instead of forcing ready;
   - V fails: re-slice vertically, or demote to a Task.
3. **One Gherkin scenario per behaviour.** Each becomes an atomic `Test` item, linked to
   the story by a `verify` edge, so coverage is computed rather than claimed.
4. **Measurable Then.** "Every Then is objectively pass/fail with a value + unit
   ('within 60 s', 'HTTP 200', 'row count = 3')."
5. **Story format.** "As a <role>, I want <goal>, so that <benefit>." Fill gaps "by
   asking, not inventing the benefit".
6. **Definition-of-Ready gate.** The output is `dor: PASS | NOT_READY`, a list of
   `dor_misses`, and `recommend_state: ready | stay`.
7. **Emit by PR only.** Computed fields are never written by hand.

The output is a fixed YAML block: the INVEST results, the tests created, the DoR verdict
and any split proposal.[^keel-skill]

# What transfers to GitHub

| Keel concept | GitHub form |
| --- | --- |
| `verify` edge from a Test to a Story | One acceptance-criterion checkbox per scenario, or a linked test-case sub-issue |
| `dependency` edge | Native blocked-by |
| `recommend_state`, never set directly | The agent comments with a verdict; a person moves the card |
| Fibonacci-only points | A number field limited to 1, 2, 3, 5, 8; 13 or more means split |

# Gaps

- The skill says to run the DoR gate per "the Output Format checklist", but the Output
  Format section has only the verdict fields. The DoR checklist itself is not written
  down in this file.[^keel-skill]
- The anti-pattern list numbers "7" twice.[^keel-skill]
- The skill improves items that already exist. It does not decompose a new vision.
- You cannot run it without the engine: its storage is SysML text, not issues.

# Caveats

- The first sweep's description is accurate. The extra point here is that the gate
  **proposes** a state and writes only through PRs. That is a real human-approval
  property, which the sweep did not credit.

[^keel-skill]: .claude/skills/backlog-refinement/SKILL.md (v0.2.0)
[^keel-readme]: Keel README
[^keel-git]: Repository git history (first 2026-06-03, HEAD 2026-10-30; skill last changed 894e394, 2026-08-21)
[^keel-page]: Repository page (stars, licence)
