---
type: Comparison
title: Kind-to-level mapping (draft for sign-off)
description: Draft table placing each work-item kind at a level or carrier in an Epic/Story/Task hierarchy, with its done condition, rationale, alternatives and trade-offs; it awaits the owner's sign-off.
tags: [work-item-kinds, mapping, epic, story, task, draft-for-signoff]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - id: safe-enablers
    resource: https://scaledagileframework.com/enablers/
    title: SAFe, Enablers (last update 13 October 2023)
    accessed: 2026-11-02
  - id: safe-spikes
    resource: https://scaledagileframework.com/spikes/
    title: SAFe, Spikes (last update 13 March 2023)
    accessed: 2026-11-02
  - id: jira-overview
    resource: https://www.atlassian.com/software/jira/guides/issues/overview
    title: Atlassian, Jira work items overview
    accessed: 2026-11-02
  - id: ado-manage-bugs
    resource: https://learn.microsoft.com/en-us/Azure/devops/boards/backlogs/manage-bugs?view=azure-devops
    title: Microsoft Learn, Manage software bugs in Azure Boards (updated 2026-04-03)
    accessed: 2026-11-02
  - id: prokanban-blocked
    resource: https://www.prokanban.org/blog/whats-wrong-with-having-a-blocked-column
    title: "Jennifer Steelman, What's Wrong With Having a Blocked Column? (9 Apr 2025)"
    accessed: 2026-11-02
  - id: nygard-2011
    resource: "Cognitect blog (cognitect.com), post 'documenting-architecture-decisions', 15 Nov 2011; date-path URL left out because it trips the public guard's number rule"
    title: "Michael Nygard, Documenting Architecture Decisions (15 Nov 2011)"
    accessed: 2026-11-02
  - id: gtd-defs
    resource: "gettingthingsdone.com, GTD Times post 'some-key-gtd-definitions', 13 Oct 2010; date-path URL left out (public guard)"
    title: GTD Times, Some key GTD definitions
    accessed: 2026-11-02
  - id: kit-reports
    resource: "gtd-board-kit: knowledge/model/report-vocabulary.md"
    title: gtd-board-kit, Report vocabulary (kit 0.12.0)
    version: 0.12.0
    accessed: 2026-11-02
  - id: arc42-nygard
    resource: https://faq.arc42.org/questions/C-9-3/
    title: arc42 FAQ C-9-3, Nygard's ADR format (links the original post)
    accessed: 2026-11-02
---

> **DRAFT. Not signed off.** This is a proposal for the owner. Nothing here is a kit rule
> until a person accepts it, ideally as a Decision record.

# Principle

Split three questions the current Kind list mixes together:

1. **What sort of work is it?** → Kind (epic, story, bug, task/enabler, spike, research).
2. **Which GTD list is it on?** → labels and status (next action, waiting-for,
   someday/maybe).[^gtd-defs] See [GTD categories](gtd-categories.md).
3. **What did it produce that we keep?** → knowledge bundle (finding, decision).

Kinds that answer 2 or 3 (question, finding, decision) are better carried by the
mechanism that already answers that question, with an issue only when there is work.

# The table

| Kind | Level / carrier | Done when | Rationale |
| --- | --- | --- | --- |
| epic | Top issue; GTD project | its outcome is reached: child items closed **and** the epic's outcome check passes | GTD project = multi-step outcome[^gtd-defs] |
| story | Issue under an epic | acceptance criteria met, DoD met, PR merged by a person | the level the hierarchy is built on |
| [bug](bug.md) | **Story-level issue** under the epic of the broken feature (or none) | a failing repro/test now passes; fix merged | Jira and GitHub peers; Azure "bugs as requirements"[^jira-overview] [^ado-manage-bugs] |
| [task / enabler / chore](enabler-and-chore.md) | **Story-level issue** if it has its own PR; else a **checklist item** (or sub-issue) in a story | PR merged and the technical outcome shown; checklist item ticked | SAFe enablers use the same levels and rules as business items[^safe-enablers] |
| [spike](spike.md) | **Story-level issue** under the epic it de-risks; timebox stated | timebox spent or question answered; a **finding** merged; next step decided (follow-ups captured) | SAFe: spikes are enabler stories with demonstrable output[^safe-spikes] |
| [research](research-task.md) | **Story-level issue**; an **epic** if it needs several stories | sourced knowledge concepts merged and reviewed by a person | SAFe exploration enablers exist at every level[^safe-enablers] |
| [question](question-and-blocker.md) | **Not a story by default:** `attention` + `needs:<who>` on the item it is about. Own story-level issue only if answering it is work or several items wait on it, linked **blocked-by** | a person answers; answer recorded on the item (or as a decision); person lifts `needs:*` | Kanban marks blocks in place;[^prokanban-blocked] the kit already has this mechanism[^kit-reports] |
| [decision](decision.md) | **OKF Decision concept** in the bundle, added by the PR of the story that made it; linked from the epic | record merged, status accepted by the owner | ADRs are repo records with their own life (proposed → superseded)[^nygard-2011] [^arc42-nygard] |
| [finding](finding.md) | **OKF Research Finding concept**, added by the spike/research PR; linked from issue and epic | reviewed by a person (draft → stable) | an output, not work; append-only like a lab notebook |

# Alternatives and trade-offs

| Kind | Alternative | Gain | Cost |
| --- | --- | --- | --- |
| bug | Sub-issue of a story (Azure "as tasks")[^ado-manage-bugs] | story stays the unit of review | bug hidden from story-level queues; story cannot close |
| bug | Not on the board; query only | clean board | defects invisible to pickup |
| task | Keep `task` as one Kind at story level only | simple | steps inside a story need another word |
| spike + research | Merge into one Kind with a timebox field | one fewer Kind | loses the narrow-vs-broad signal |
| spike | Inside another story, no own item (Cohn's second habit) | no extra item | no place to report or claim the investigation |
| question | **First sweep:** always a blocked story waiting on a person | every question is listed and countable | duplicates the `needs:*` flag; a "story" with no deliverable; noise in story views |
| decision | Kind `decision` issue that closes when the record merges | decisions visible on the board | two records for one thing; drift risk |
| finding | Kind `finding` issue | visible on the board | an issue with nothing to do; closes at once |

# Changes vs the first sweep

| First-sweep draft | This draft | Why |
| --- | --- | --- |
| spike, research → stories under an epic **when they produce a finding** | spike, research → story-level issues **always**; the finding is their required output | the output is the done condition, not the trigger for the level |
| question → blocked story waiting on a person | question → `needs:*` flag on its item by default; own item only when it is work | in-place flag is mainstream practice and is already in the kit |
| decision → OKF decision record linked from the epic | same | agrees with ADR practice |

# Open questions for the owner

1. Keep Kinds `question`, `finding`, `decision` as issue types at all, or retire them in
   favour of `needs:*` and bundle concepts?
2. Rename or split `task` (enabler story vs step inside a story)?
3. One Kind for spike and research, or two?
4. Default bug placement: story-level (proposed) or sub-issue?
5. Timebox for a spike: a field, a Size cap (XS to M), or free text?
6. How to carry ADR "proposed" and "superseded" in OKF, which only has draft, stable,
   deprecated?
