---
type: Reference
title: BMAD Method ticket tree and readiness gate
description: BMAD has moved from sharded epics, story files and a separate readiness check (v6) to a Product Owner agent that keeps an initiative-epic-story tree in TOML and markdown, with human-approval flags per entry; it is the most complete model and the fastest-changing.
resource: https://github.com/bmad-code-org/BMAD-METHOD
tags: [method, decomposition, definition-of-ready, human-gate, dependencies]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: bm-changelog, title: "CHANGELOG.md at bd70c64 (Unreleased, v6.12.0, v6.11.0)", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/CHANGELOG.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-readiness, title: "v6.12.0 bmad-sprint-planning/references/readiness-gate.md", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.0/src/bmm-skills/plan/bmad-sprint-planning/references/readiness-gate.md", version: v6.12.0, commit: 05bfbd46d00766ec88eb9b42e76be2c575d64d7b, accessed: 2026-11-02 }
  - { id: bm-tickets-help, title: "skills/bmod-method/help/ticketing-and-epics.md at bd70c64", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/skills/bmod-method/help/ticketing-and-epics.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-ticket-tpl, title: "skills/bmad-agent-po/assets/ticket-template.md at bd70c64", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/skills/bmad-agent-po/assets/ticket-template.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-tickets-tpl, title: "skills/bmad-agent-po/assets/tickets-template.toml at bd70c64", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/skills/bmad-agent-po/assets/tickets-template.toml", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-slice, title: "skills/bmad-agent-po/references/slice.md and validate-checks.md at bd70c64", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/skills/bmad-agent-po/references/slice.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-setup, title: "skills/bmod-method/help/ticketing-setup.md (trackers) at bd70c64", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/skills/bmod-method/help/ticketing-setup.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-docs-plan, title: "docs/plan/break-work-into-stories-and-track-it.md at bd70c64", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/docs/plan/break-work-into-stories-and-track-it.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-page, title: "Repository page (stars, release status)", resource: "https://github.com/bmad-code-org/BMAD-METHOD", accessed: 2026-11-02 }
---

# Provenance

| Fact | Value |
| --- | --- |
| Owner | BMad Code, LLC; MIT licence, plus a separate TRADEMARK.md |
| Stars / forks | 54.6k / 6.1k on 2026-11-02[^bm-page] |
| Stable release | v6.12.0, 2026-09-03 (commit `05bfbd4`)[^bm-changelog] |
| Main branch | `bd70c64`, 2026-10-31: an "Unreleased" v7 draft with breaking changes[^bm-changelog] |
| Scripts | Python helpers that need `uv` and Python 3.11 or later (since v6.11). The ticket tree uses `tickets.py`, about 1,900 lines, standard library only[^bm-changelog] |

# It changed under the first sweep

The first sweep described v6-era BMAD: "sharding", story files, a separate readiness
gate and a "sprint-status file as contract". Since August 2026 much of that has changed:[^bm-changelog]

| Was | Now |
| --- | --- |
| `bmad-shard-doc` | Retired in v6.11, with no replacement |
| `bmad-create-story` and `bmad-dev-story` | Deprecated in v6.11; Phase 4 is sprint-planning, then build, then code-review |
| `bmad-check-implementation-readiness` | Removed in v6.11 and folded into `bmad-sprint-planning` as a PASS / CONCERNS / FAIL gate |
| `bmad-create-epics-and-stories`, `bmad-sprint-planning` | Listed as retired on main (Unreleased) |
| (new) | The Product Owner agent (`bmad-agent-po`) keeps one ticket tree |

# v6.12.0 readiness gate (stable)

The gate asks one question: "could a developer implement these epics without inventing
decisions nothing records?"[^bm-readiness] Its checks:

- requirements trace forward to stories, and stories trace back; orphans are flagged
  both ways;
- epics deliver user value and have no forward dependencies;
- stories can each be completed on their own;
- architecture and UX decisions are recorded, not assumed;
- conflicts between documents are surfaced, not settled silently.

The verdicts: **PASS** continues. **CONCERNS** asks the person whether to proceed or fix
first. **FAIL** names the skill that fixes each finding.[^bm-readiness]

# Main-branch ticket tree (v7 draft)

An initiative holds epics; each epic's `tickets/tickets.toml` holds ordered entries.[^bm-tickets-help]

Fields on each entry worth borrowing:[^bm-tickets-tpl]

| Field | Meaning |
| --- | --- |
| `id` | Permanent, never reused |
| `description`, `verify` | One sentence each; `verify` is the observable check |
| `covers` | Which requirement ids of the epic this entry serves |
| `after` | **Prerequisites only, not sequence.** Build order is the table order |
| `hitl` | A person does part of the work |
| `unknown` | One question for the user; the entry is blocked until it is removed |
| `plan_checkpoint` | A person reviews the ticket or plan before the build |
| `done_checkpoint` | Pause after the build until a person says continue |
| `refined` | Set true "once the user approves its criteria"[^bm-ticket-tpl] |

Story acceptance criteria are numbered **Given/When/Then** behaviours, each tagged with
the requirement it serves (`R<m>`). Containers have "Done when", three to six end checks
including production delivery.[^bm-ticket-tpl]

**Sizing rule:** a story is "one step toward the epic's Done when, sized for one agent
session". It is too small "when setup outweighs the work".[^bm-slice]

**Set checks before approval:** every `after` is a real prerequisite, not restated order.
`tickets.py status` must show no cycle or drift. "A builder could write each story's
acceptance criteria from the epic, entry, and references".[^bm-slice]

**Status ownership:** "Build stops at `built`; the user or orchestrator marks `done`."
Code review appends findings and never changes status.[^bm-tickets-help] [^bm-docs-plan]

# GitHub fit

The tree can publish to GitHub Issues, Jira, Linear, Notion or Trello. But "the trackers
are lightly tested". The markdown files stay the working copy, and "nothing syncs on its
own".[^bm-setup] GitHub is a mirror here, not the record.

# Caveats

- The v7 layout is on main, not released. Field names may change again. Cite v6.12.0
  for anything stable.
- BMAD is heavy: personas, a layered TOML config and an installer. Borrow the field
  names and gates; do not adopt the method.

[^bm-changelog]: CHANGELOG.md at bd70c64 (Unreleased, v6.12.0, v6.11.0)
[^bm-readiness]: v6.12.0 bmad-sprint-planning/references/readiness-gate.md
[^bm-tickets-help]: skills/bmod-method/help/ticketing-and-epics.md at bd70c64
[^bm-ticket-tpl]: skills/bmad-agent-po/assets/ticket-template.md at bd70c64
[^bm-tickets-tpl]: skills/bmad-agent-po/assets/tickets-template.toml at bd70c64
[^bm-slice]: skills/bmad-agent-po/references/slice.md and validate-checks.md at bd70c64
[^bm-setup]: skills/bmod-method/help/ticketing-setup.md (trackers) at bd70c64
[^bm-docs-plan]: docs/plan/break-work-into-stories-and-track-it.md at bd70c64
[^bm-page]: Repository page (stars, release status)
