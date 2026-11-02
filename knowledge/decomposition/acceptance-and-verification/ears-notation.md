---
type: Concept
title: EARS notation
description: EARS is a small set of keyword templates (While, When, Where, If/Then, plus a plain "shall") for writing natural-language requirements with less ambiguity.
tags: [acceptance-criteria, requirements, ears]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: mavin-ears, title: "EARS (Alistair Mavin's official page)", resource: "https://alistairmavin.com/ears/", url: "https://alistairmavin.com/ears/", accessed: 2026-11-02 }
  - { id: ears-wiki, title: "Easy Approach to Requirements Syntax (Wikipedia)", resource: "https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax", url: "https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax", accessed: 2026-11-02 }
  - { id: kiro-req, title: "Kiro docs: requirements-first feature specs", resource: "https://kiro.dev/docs/specs/feature-specs/requirements-first/", url: "https://kiro.dev/docs/specs/feature-specs/requirements-first/", accessed: 2026-11-02 }
---

# What it is

EARS (Easy Approach to Requirements Syntax) was developed by Alistair Mavin and
colleagues at Rolls-Royce while analysing airworthiness rules for a jet engine control
system, and published at the IEEE Requirements Engineering conference in
2009 (paper: Mavin et al., "Easy Approach to Requirements Syntax (EARS)", RE'09, DOI 10.1109/RE.2009.9; not read directly).[^ears-wiki] Clauses come in a fixed order: optional preconditions,
an optional trigger, the system name, then one or more responses.[^mavin-ears]

| Pattern | Template |
| --- | --- |
| Ubiquitous | The `<system>` shall `<response>` |
| State-driven | **While** `<precondition>`, the `<system>` shall `<response>` |
| Event-driven | **When** `<trigger>`, the `<system>` shall `<response>` |
| Optional feature | **Where** `<feature is included>`, the `<system>` shall `<response>` |
| Unwanted behaviour | **If** `<trigger>`, **then** the `<system>` shall `<response>` |
| Complex | Keywords combined, e.g. While ... When ... |

Templates as given on the official page and the summary of the paper.[^mavin-ears][^ears-wiki]

# Claimed benefits

Less ambiguity, little training, no tools, easier for non-native English writers.[^mavin-ears]
These are the author's claims; this track found no independent controlled study.

# Use by AI coding tools

Kiro, an AWS spec-driven coding tool, writes `requirements.md` in EARS form
("WHEN ... THE SYSTEM SHALL ...").[^kiro-req] So at least one agent tool treats EARS as
the input an agent builds from.

# When it fits

- One-line criteria for a story, where a full scenario is too heavy.
- Constraints with no event (ubiquitous) and state-dependent rules (While).
- The **If/Then** pattern forces the error case to be written down.

# When it does not fit

- It names one response, not concrete example values. Pair it with examples
  ([Specification by Example](specification-by-example.md)) when values matter.
- "Shall" can still hide vague words ("shall respond quickly"); the
  [testability heuristics](testable-criteria-heuristics.md) still apply.

# Related

- [Gherkin and Given/When/Then](gherkin-given-when-then.md): a `When ... shall` line maps
  to a `When ... Then` scenario.
- [Choosing a criteria form](choosing-a-criteria-form.md)
