---
type: Decision
title: Register records have one schema, upgraded on read
description: Experiment, benchmark and finding records carry an envelope and follow per-event JSON Schemas kept in the kit; every writer validates against them, older records are upgraded when read and never rewritten, and every mirror shows an item's state the same way.
tags: [registers, records, schema, experiments]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-14T05:00:00Z }
---

# Context

Record pages fixed where register records live and how a page grows, but not what a record
says. In one lab register measured before this decision, a record's time came in three
formats (local with no zone, UTC with an offset, a local offset) and was missing on some
lines; the author field was missing on most lines and free text on the rest; one event's
`kind` held a free-text headline; the preregistration status was a sentence a reader had to
parse; a registration's spec had nine required keys and about sixty optional ones nobody had
listed; and no record carried a schema version. The same refusal rules were restated by hand
in each tool that wrote records and in the server, so each copy could drift.

Prior art was surveyed in four groups. Experiment trackers (MLflow, DVC, Weights & Biases,
Hydra, Sacred) record that a run happened and what numbers it produced, and none records a
decision rule, a verdict by that rule, or a later reading that changes what a result means;
some allow editing a summary after the fact. Evaluation harnesses (lm-evaluation-harness,
HELM, Inspect AI, OpenAI evals) separate a task definition from its run log and hash the task,
but report numbers, not verdicts. Provenance and preregistration standards (W3C PROV,
RO-Crate, nanopublications, OSF and AsPredicted templates) model immutable assertions,
retraction by a new record, and the fields a preregistration needs, including deviations and
when they were made. Event and record stores (CloudEvents, Inspect's log upgrades, git-native
issue stores, event-sourcing practice) carry a version per record and upgrade old records in
the reader instead of rewriting them.

# Decision

- One JSON Schema per register in `server-spec/schemas/register-records/`, with a definition
  per event, and a standard-library reference implementation that validates, upgrades, folds
  and shows records (`conformance/register_records.py`). Servers and repositories copy it and
  are held to the golden cases, as they are for record pages.
- Every new record carries an envelope: `v`, `eid` (a writer-minted ULID), `t` in UTC with
  its offset, `by` as a principal, `via` naming the writing tool, and optional `for`.
- Closed sets that a fold or a view depends on are enums. New events: `deviation` (a change
  from the registration, with its timing) and `artifact` (a pointer, split from item links).
  A registration answers its baseline, stopping rule, positive control and reference anchor,
  with `none: <reason>` allowed where there is none.
- Older records are never rewritten. A record without `v` is version 0, and the reader
  upgrades it with fixed rules. The line hash stays the citation.
- The fold and what an item shows on GitHub (issue type, kind and state labels, an
  invalid-record label, Status, fields, a body that links to the item's page) are fixed in
  the same section, so a sync and a tool show the same state.

# Consequences

- A rule changes in one place and reaches every writer and mirror through the kit pin.
- A writer that skips the envelope or a required field is refused; a repository's existing
  records stay valid.
- The upgrade is permanent code: each step is a golden case, and a repository adopting it
  checks that its folds do not change.
- Exporting standard formats (an RO-Crate per item, PROV terms for link kinds) is left for
  later; it can be generated from records, and is never the record.
