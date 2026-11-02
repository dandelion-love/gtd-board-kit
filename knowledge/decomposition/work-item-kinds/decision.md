---
type: Practice
title: Decision
description: A decision is recorded as a short, numbered, immutable record (an ADR) kept in the repository; the work item that makes the decision links to it, and the record outlives the item.
tags: [work-item-kinds, decision, adr]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:15:00Z }
sources:
  - id: nygard-2011
    resource: "Cognitect blog (cognitect.com), post 'documenting-architecture-decisions', 15 Nov 2011; date-path URL left out because it trips the public guard's number rule"
    title: "Michael Nygard, Documenting Architecture Decisions (15 Nov 2011)"
    accessed: 2026-11-02
  - id: madr
    resource: https://adr.github.io/madr/
    title: MADR, Markdown Architectural Decision Records (4.0.0, 2024-09-17)
    version: 4.0.0
    accessed: 2026-11-02
  - id: adr-org
    resource: https://adr.github.io/
    title: adr.github.io, Architectural Decision Records
    accessed: 2026-11-02
  - id: ado-impediments
    resource: https://learn.microsoft.com/en-my/previous-versions/azure/devops/boards/backlogs/manage-issues-impediments?view=tfs-2018
    title: Microsoft Learn (archived TFS 2018), Manage issues or impediments
    accessed: 2026-11-02
  - id: okf-spec
    resource: "gtd-board-kit: okf/SPEC.md (OKF v0.2, pinned by the kit)"
    title: Open Knowledge Format v0.2
    accessed: 2026-11-02
  - id: arc42-nygard
    resource: https://faq.arc42.org/questions/C-9-3/
    title: arc42 FAQ C-9-3, Nygard's ADR format (links the original post)
    accessed: 2026-11-02
---

# What established practice says

- **Nygard (2011):** keep ADRs "in the project repository"; number them "sequentially
  and monotonically"; a reversed decision is kept and "mark[ed] as superseded"; "one or
  two pages long".[^nygard-2011] Sections: Title, Context, Decision, Status,
  Consequences. Status: proposed, accepted, deprecated, superseded.[^nygard-2011] [^arc42-nygard]
- **MADR 4.0.0:** required sections are Context and Problem Statement, Considered
  Options, Decision Outcome; optional ones include Decision Drivers, Consequences,
  **Confirmation**, Pros and Cons. Optional front matter: `status`, `date`,
  `decision-makers`, `consulted`, `informed`. Files go in `docs/decisions` as
  `NNNN-title-with-dashes.md`.[^madr]
- **Decision log:** "The collection of ADRs created and maintained in a project
  constitute its decision log."[^adr-org]
- **Link to work items:** neither Nygard nor adr.github.io say how an ADR links to a
  ticket.[^nygard-2011] [^adr-org] Azure DevOps, in its archived docs, tracks decisions
  "that require several stakeholders" as Issue/Impediment items.[^ado-impediments]

# Record vs work item

| | Work item (issue) | Decision record (ADR / OKF Decision) |
| --- | --- | --- |
| Life | open → closed | proposed → accepted → superseded; never deleted |
| Lives | on the board | in the repo, versioned |
| Answers | "what must be done" | "what we chose and why" |
| Changes | edited in place | a new record supersedes the old |

The two have different lives, so practice keeps them apart and links them.

# Done

The record is merged with status accepted by the person who owns the decision. MADR's
**Confirmation** section says how compliance will be checked;[^madr] that is the
record's own acceptance test.

# For the kit

- Carrier: an **OKF concept** with `type: Decision` in the knowledge bundle (OKF allows
  any `type` string[^okf-spec]); `status: draft` while proposed, `stable` once accepted,
  `deprecated` when superseded.
- The **making** of a decision is work: when it needs research or a person's call, it
  rides on a story (often a [spike](spike.md) or [question](question-and-blocker.md)),
  and that story's PR adds the record.
- The epic links to its decision records; a superseding record links to the old one.
- A Kind `decision` issue is then optional; see the [mapping](kind-to-level-mapping.md).

# Caveats

- The original Nygard post was read at its cognitect.com address; its URL is not written
  here because its date path trips the public guard. The arc42 FAQ links it.[^arc42-nygard]

- Nygard's ADR scope is architecture; using it for product or process decisions is
  common but is an extension.
- OKF `status` (draft, stable, deprecated) has no "proposed" or "superseded" value; the
  kit would need a convention (for example a `supersedes:` key) to carry them.
