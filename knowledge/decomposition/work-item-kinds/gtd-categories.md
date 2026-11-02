---
type: Comparison
title: GTD categories and work-item kinds
description: GTD sorts by commitment and actionability (project, next action, waiting for, someday/maybe, reference), not by kind of work, so each work-item kind maps to a GTD list by its state, and non-actionable outputs map to reference.
tags: [work-item-kinds, gtd]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:25:00Z }
sources:
  - id: gtd-what
    resource: https://gettingthingsdone.com/what-is-gtd/
    title: David Allen Company, What is GTD
    accessed: 2026-11-02
  - id: gtd-defs
    resource: "gettingthingsdone.com, GTD Times post 'some-key-gtd-definitions', 13 Oct 2010; date-path URL left out (public guard)"
    title: GTD Times, Some key GTD definitions (2010, modified 2014)
    accessed: 2026-11-02
  - id: gtd-map
    resource: "gettingthingsdone.com uploads, GTD_workflow_map.pdf (David Allen Company, 2008); date-path URL left out (public guard)"
    title: David Allen Company, GTD Workflow map (2008)
    accessed: 2026-11-02
  - id: kit-board
    resource: "gtd-board-kit: BOARD.md (kit 0.12.0)"
    title: gtd-board-kit, Working this repo's board
    version: 0.12.0
    accessed: 2026-11-02
---

# GTD's own definitions

- **Project:** "any outcome that will take more than one action step to complete."[^gtd-defs]
- **Next Action:** "your physical, visible next step."[^gtd-defs]
- **Waiting For:** "items that you are waiting on from someone or something else."[^gtd-defs]
- **Someday/Maybe:** "you are not currently committed to complete it".[^gtd-defs]
- Five steps: Capture, Clarify ("Is it actionable?"; non-actionable items are trash,
  reference, or on hold), Organize, Reflect, Engage.[^gtd-what]
- The workflow map first asks **"Is it actionable?"**; no → "TRASH" or "INCUBATE"
  ("Someday Maybe lists/ folders"), or kept as reference (see Caveats); yes and multi-step → "What's the desired outcome?" (a
  project); then do, track on Waiting For, or defer to calendar.[^gtd-map]

# Key point

GTD buckets are about **commitment and next step**, not about the **kind** of work.
A spike, a bug and a story can each be a next action, waiting-for or someday/maybe.
Only outputs (findings, decisions) are non-actionable, which GTD calls reference.

# Mapping

| GTD | Kit construct | Kinds that land here |
| --- | --- | --- |
| Inbox (captured, unclarified) | `capture`, `agent-proposed`[^kit-board] | any new item |
| Project | epic (and a story with several steps) | epic |
| Next action | a claimable item: `agent-ready`, small[^kit-board] | story, bug, task, spike, research |
| Waiting for | `needs:<who>`, `blocked`, blocked-by link | any item; a `question` item |
| Someday/Maybe | open, not committed (backlog, no `agent-ready`) | any |
| Reference | OKF knowledge bundle | finding, decision |
| Trash | closed as not planned; report `dropped` | any |
| Calendar / tickler | dates on the item or milestone | any dated item |

# For the kit

- Kind answers "what sort of work"; labels and status answer "which GTD list". Keep them
  separate so one item can move through the lists without changing Kind.
- This argues for **fewer Kinds**: question and finding are GTD *states/outputs*
  (waiting-for, reference), not kinds of work. See the [mapping](kind-to-level-mapping.md).

# Caveats

- **Reference** is named on the official "What is GTD" page as a home for non-actionable
  items,[^gtd-what] but the definitions page does not define it and the 2008 map's
  extracted text shows no "Reference" box.[^gtd-map]
- Two GTD sources live at date-path URLs that trip the public guard; they are cited by
  site and post name instead of URL.
- "Someday/Maybe = open but not `agent-ready`" is a proposal; the kit may want an explicit
  label for it.
