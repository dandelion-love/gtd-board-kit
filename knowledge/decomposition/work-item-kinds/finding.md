---
type: Practice
title: Finding
description: A finding is the output of a spike, research task or experiment, not a unit of work; research and ML practice record it as a dated, append-only entry tied to a hypothesis and its evidence.
tags: [work-item-kinds, finding, experiment, hypothesis, knowledge]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:20:00Z }
sources:
  - id: oreilly-hdd
    resource: https://www.thoughtworks.com/insights/blog/how-implement-hypothesis-driven-development
    title: "Barry O'Reilly, How to Implement Hypothesis-Driven Development (Thoughtworks, 18 Oct 2014)"
    accessed: 2026-11-02
  - id: mlflow-tracking
    resource: https://mlflow.org/docs/latest/ml/tracking/
    title: MLflow Tracking documentation
    accessed: 2026-11-02
  - id: ucsf-notebook
    resource: https://mcmanuslab.ucsf.edu/uc-lab-notebook-guidelines
    title: UC lab notebook guidelines (a UCSF lab's page)
    accessed: 2026-11-02
  - id: safe-spikes
    resource: https://scaledagileframework.com/spikes/
    title: SAFe, Spikes (last update 13 March 2023)
    accessed: 2026-11-02
  - id: kit-work-items
    resource: "gtd-board-kit: knowledge/decisions/work-items-live-on-the-board.md"
    title: gtd-board-kit, Work items live on the board (kit 0.12.0)
    version: 0.12.0
    accessed: 2026-11-02
---

# What established practice says

- **Hypothesis-driven development:** a story is written "We believe <this capability>
  will result in <this outcome>. We will know we have succeeded when <we see a
  measurable signal>".[^oreilly-hdd] "The key outcome of an experimental approach is
  measurable evidence and learning"; "we should not say we are done until we have
  measured the value".[^oreilly-hdd] The finding is the measured signal against the
  stated threshold.
- **ML experiment tracking (MLflow):** an *experiment* groups *runs*; each run logs
  parameters, metrics, start and end times, tags, artifacts and code
  version.[^mlflow-tracking] Runs are compared and searched by metric.[^mlflow-tracking]
  A run is evidence; a finding is the conclusion drawn across runs.
- **Lab notebooks:** each entry has date, purpose, materials and method, "RESULTS and
  CONCLUSION", including "whether the experiment was successful and the major finding";
  "Do not change entries; make a new entry".[^ucsf-notebook]
- **Spikes:** "The output of a spike is demonstrable".[^safe-spikes] The finding is that
  output.

# A finding is an output, not a work item

| | Spike / research / experiment | Finding |
| --- | --- | --- |
| Kind of thing | work: claimed, done, closed | knowledge: written, reviewed, kept |
| Done | when the question is answered | n/a; it is *reviewed* (draft → stable) or *superseded* |
| Changes | — | append-only: a new finding, not an edit (lab rule) |

# Shape of a finding

Question or hypothesis · method · evidence (runs, links, sources) · result against the
success signal · conclusion · confidence and open questions · next step.

# For the kit

- Carrier: an **OKF concept** (`type: Research Finding`, as the kit's OKF skill already
  lists) in the bundle, added by the PR of the [spike](spike.md) or
  [research](research-task.md) item, linked from that issue and its epic.
- Raw run records: an append-only experiment log; the kit already allows non-work-item
  records like this to stay files.[^kit-work-items]
- A Kind `finding` issue is not needed for the finding itself. Use an issue only to ask a
  person to **review** or act on it (then it is a story or question).
- See the [mapping](kind-to-level-mapping.md).

# Caveats

- "Learning story" as a named backlog type was not found in a primary source; only
  secondary blog use. It is not relied on here.
- The lab notebook source is one lab's guideline page.
