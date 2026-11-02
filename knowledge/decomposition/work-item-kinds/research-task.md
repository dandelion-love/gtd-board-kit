---
type: Practice
title: Research task
description: Broader investigation than a spike, whose deliverable is a written, sourced knowledge document rather than a go/no-go answer; established practice files it as exploration enabler work.
tags: [work-item-kinds, research, enabler, knowledge]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:00Z }
sources:
  - id: safe-enablers
    resource: https://scaledagileframework.com/enablers/
    title: SAFe, Enablers (last update 13 October 2023)
    accessed: 2026-11-02
  - id: safe-story
    resource: https://scaledagileframework.com/story
    title: SAFe, Story (last update 7 December 2022)
    accessed: 2026-11-02
  - id: cohn-spikes
    resource: https://www.mountaingoatsoftware.com/blog/spikes
    title: "Mike Cohn, Agile Spikes Deliver Knowledge So Teams Can Deliver Products (updated 6 Aug 2024)"
    accessed: 2026-11-02
  - id: ucsf-notebook
    resource: https://mcmanuslab.ucsf.edu/uc-lab-notebook-guidelines
    title: UC lab notebook guidelines (a UCSF lab's page)
    accessed: 2026-11-02
---

# What established practice says

- **No framework defines "research task" as its own type.** The nearest is SAFe's
  **exploration enabler**, one of four enabler types (exploration, architectural,
  infrastructure, compliance), covering research and prototyping.[^safe-enablers]
- Enablers are captured "as a type of Epic, Capability, Feature, or Story" and are
  "written and prioritized according to the same rules" as business items.[^safe-enablers]
  So research can live at **any level**, sized to that level.
- Enabler stories may be "expressed in technical rather than user-centric language" and
  are demonstrated "by showing the knowledge gained, artifacts produced".[^safe-story]
- Cohn calls a spike itself "a time-boxed research activity",[^cohn-spikes] so most
  writers do not separate the two; the difference below is a working convention.

# Spike vs research (working distinction)

| | [Spike](spike.md) | Research task |
| --- | --- | --- |
| Question | one, narrow, blocking a story | a topic; several questions |
| Output | an answer plus a next-step decision | a sourced knowledge document (one or more concepts) |
| Timebox | short, fixed | may be longer; split into stories if over one iteration |
| Code | throwaway | usually none |

# Done

- Done = the knowledge document exists, cites its sources, marks open questions, and a
  person has reviewed it (in the kit: an OKF concept merged by PR, `status: draft` until a
  person marks it reviewed).
- Lab practice sets the record's shape: date, purpose, materials and method, then
  "RESULTS and CONCLUSION", and "Do not change entries; make a new entry".[^ucsf-notebook]

# For the kit

- Small research (one iteration): a **story-level issue**, Kind `research`, under the
  epic it informs. Its PR adds [finding](finding.md) concepts to the bundle.
- Large research: an **epic** whose stories are research tracks, each returning concepts.
- See the [mapping](kind-to-level-mapping.md).

# Caveats

- The spike/research split is not from a primary source; it is proposed here. An owner
  may prefer one Kind with a timebox field.
- The lab notebook source is one lab's guideline page, not a standards body.
