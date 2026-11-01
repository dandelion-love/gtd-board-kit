---
name: okf-knowledge
description: Write and maintain this repo's knowledge docs (research findings, decisions, references, how-tos) as an Open Knowledge Format bundle at the OKF version the kit pins, and lint them. Use when capturing findings or a decision, adding or editing a concept, migrating older docs to the current OKF, or checking a bundle.
metadata:
  author: gtd-board-kit
  version: 0.1.0
---

# Knowledge docs in OKF

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists. The OKF version and spec
this repo follows are pinned by the kit: `.gtd/kit/okf/PIN.json` and `.gtd/kit/okf/SPEC.md`.
Read the spec's sections 4 to 9 before your first edit in a session.

## Where

The bundle lives where `.gtd/BOARD.local.md` says (its "Knowledge bundle" line), else
`docs/knowledge/`. Plan state never goes in it: work is issues on the board.

## A concept

One concept per file; the path is its identity. `index.md` and `log.md` are reserved.

```yaml
---
type: Decision            # required; e.g. Research Finding, Decision, Pattern, Reference, Open Question, Playbook
title: Short display name
description: One sentence an index or a search result can show.
tags: [area, topic]
status: draft             # draft until a person reviews it, then stable; deprecated keeps links alive
generated: { by: <runtime>/<version>, at: 2026-01-01T00:00:00Z }
sources:
  - { id: spec, resource: https://example.com/spec, title: The spec }
---
```

- `generated.by` is you, as `<runtime>/<version>` (for example `claude-code/<version>` or
  `codex/<version>`); people are `human:<id>`, automations `process:<id>`. Update
  `generated.at` on every meaningful content change. Every datetime carries an offset.
- Never add `verified` for yourself: verification is a person's or a check's act.
  When your person confirms a concept, add `{ by: human:<their id>, at: … }` and set
  `status: stable`.
- Cite with footnotes keyed to `sources[].id` (`text.[^spec]`), not a `# Citations` list.
- Link with bundle-relative paths starting with `/` (`[x](/decisions/x.md)`). A link to a
  concept not yet written is allowed; prefer writing a short draft stub.
- Use `stale_after` when a fact has a known shelf life.
- Put structure in the body (headings, lists, tables, code). Conventional headings:
  `# Schema`, `# Examples`, `# Computation`.

## Indexes and the log

- Each directory's `index.md` lists its concepts and subdirectories, under headings, as
  `* [Title](path) - description`. No frontmatter, except the bundle root's, which carries
  `okf_version` set to the value in `.gtd/kit/okf/PIN.json`.
- The bundle's `log.md` gets a line for each notable change, under `## YYYY-MM-DD`,
  newest first.

## Check

```bash
python3 .gtd/kit/tools/okf_lint.py <bundle-dir> --strict
```

Fix every error and warning before you commit. The lint needs only Python; with PyYAML
installed it also checks actors, datetimes and footnotes.

## Migrating older OKF docs

To move from v0.1: turn `timestamp` into `generated: { by, at }` (the `by` of whoever
wrote it; `human:<id>` if a person did, or your runtime if you can't tell, and say so in
the PR), move a `# Citations` list into `sources` with footnotes, then set `okf_version`
in the root `index.md`. Do it in its own PR.
