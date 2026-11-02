---
type: Comparison
title: Questions, blockers and impediments
description: Mainstream practice marks a blocked or waiting item in place (a flag, a sticky, a dependency) rather than moving it or making a new story; separate impediment items exist but sit off the backlog.
tags: [work-item-kinds, question, blocked, waiting-for, impediment]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:10:00Z }
sources:
  - id: scrum-guide
    resource: https://scrumguides.org/scrum-guide.html
    title: The 2020 Scrum Guide
    accessed: 2026-11-02
  - id: ado-impediments
    resource: https://learn.microsoft.com/en-my/previous-versions/azure/devops/boards/backlogs/manage-issues-impediments?view=tfs-2018
    title: Microsoft Learn (archived TFS 2018), Manage issues or impediments
    accessed: 2026-11-02
  - id: ado-process
    resource: https://github.com/MicrosoftDocs/azure-devops-docs/blob/main/docs/boards/work-items/guidance/choose-process.md
    title: Azure DevOps docs, Choose a process (source file)
    accessed: 2026-11-02
  - id: jira-flag
    resource: https://support.atlassian.com/jira-software-cloud/docs/flag-an-issue/
    title: Atlassian Support, Flag a work item
    accessed: 2026-11-02
  - id: prokanban-blocked
    resource: https://www.prokanban.org/blog/whats-wrong-with-having-a-blocked-column
    title: "Jennifer Steelman, What's Wrong With Having a Blocked Column? (ProKanban.org, 9 Apr 2025)"
    accessed: 2026-11-02
  - id: leopold-blockers
    resource: https://www.infoq.com/articles/blockers-defects-process-improvement
    title: "Klaus Leopold and Troy Magennis, blocker clustering (InfoQ, 8 Jun 2015)"
    accessed: 2026-11-02
  - id: gh-deps
    resource: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies
    title: GitHub Docs, Creating issue dependencies
    accessed: 2026-11-02
  - id: gh-deps-changelog
    resource: "github.blog changelog, 'Dependencies on issues' GA, 21 Aug 2025; date-path URL left out (public guard)"
    title: GitHub Changelog, Dependencies on issues GA (2025-08-21)
    accessed: 2026-11-02
  - id: gtd-defs
    resource: "gettingthingsdone.com, GTD Times post 'some-key-gtd-definitions', 13 Oct 2010; date-path URL left out (public guard)"
    title: GTD Times, Some key GTD definitions (2010, modified 2014)
    accessed: 2026-11-02
  - id: kit-reports
    resource: "gtd-board-kit: knowledge/model/report-vocabulary.md"
    title: gtd-board-kit, Report vocabulary (kit 0.12.0)
    version: 0.12.0
    accessed: 2026-11-02
---

# Item or flag?

| Practice | Carrier | Source |
| --- | --- | --- |
| Scrum | Impediments are surfaced at the Daily Scrum; the Scrum Master causes their removal. No item type defined | [^scrum-guide] |
| Azure DevOps | A separate **Impediment** (Scrum) or **Issue** (Agile, CMMI) item, linked "Related" to the stories; **not on the backlog**, tracked by query | [^ado-impediments] [^ado-process] |
| Jira | A **flag** on the item itself; shown yellow on boards and backlogs | [^jira-flag] |
| Kanban | Keep the item **in its column** with a visual cue; a blocked column is an anti-pattern (breaks WIP limits, hides where it stalled) | [^prokanban-blocked] |
| Kanban (Leopold, Magennis) | A red sticky with the reason on the card, a tick per day blocked; keep the stickies and cluster them for improvement | [^leopold-blockers] |
| GitHub | **Blocked by / blocking** relationships between issues; a "Blocked" icon on project boards; up to 50 per relationship type; `is:blocked` filter | [^gh-deps] [^gh-deps-changelog] |
| GTD | **Waiting For**: "items that you are waiting on from someone or something else" | [^gtd-defs] |

Azure's archived page also says impediments may track "decisions that require several
stakeholders or product teams to weigh in on".[^ado-impediments] That is the one source
that makes a stakeholder question its own item.

# Two kinds of "question"

1. **A question about an item** ("which API version?"). Practice: flag the item in place.
   The kit already does this: an `attention` on a report adds `needs:<who>`, moves the
   card to the needs-a-person column, and stops work; only the person removes the
   label.[^kit-reports]
2. **A question that is its own piece of work** (answering it needs research, or many
   items wait on it). Practice: an item of its own (Azure Impediment), with blocking
   links from the items that wait.

# Done

A question is done when a person has answered it, the answer is written where the
waiting work can read it (a comment on the item, or a [decision](decision.md) record if
it sets policy), and the person has lifted the `needs:*` label or closed the blocking
item.

# For the kit

- **Default:** no new story. Raise it as `attention` + `needs:<who>` on the item it is
  about (GTD waiting-for).
- **Own item** (Kind `question`) only for case 2: a story-level issue that **blocks** the
  items waiting on it through GitHub dependencies, so the blocked icon shows on them.
- Keep resolved blockers queryable (closed `question` items, `needs:*` history) so they
  can be clustered later, as Leopold and Magennis advise.[^leopold-blockers]
- See the [mapping](kind-to-level-mapping.md).

# Caveats

- The Azure impediment page is archived (TFS 2018); current docs list the types but were
  not found to restate the off-backlog rule.[^ado-process]
- Two sources (GitHub changelog, GTD Times) are cited by name, not URL, because their
  date paths trip the public guard.
- The Jira support page text fetched was only its summary; that a flag means
  "impediment" is common usage, not confirmed from the page body.
