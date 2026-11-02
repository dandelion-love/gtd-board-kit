---
type: Comparison
title: Bug
description: Tools disagree on where a defect sits; Jira and GitHub make it a peer of story and task, Azure DevOps lets each team choose requirement-level or task-level, and practitioners split bugs found in current work from bugs in accepted work.
tags: [work-item-kinds, bug, defect]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - id: jira-overview
    resource: https://www.atlassian.com/software/jira/guides/issues/overview
    title: Atlassian, Jira work items overview
    accessed: 2026-11-02
  - id: ado-manage-bugs
    resource: https://learn.microsoft.com/en-us/Azure/devops/boards/backlogs/manage-bugs?view=azure-devops
    title: Microsoft Learn, Define, capture, triage, and manage software bugs in Azure Boards (updated 2026-04-03)
    accessed: 2026-11-02
  - id: ado-show-bugs
    resource: https://learn.microsoft.com/en-us/azure/devops/organizations/settings/show-bugs-on-backlog
    title: Microsoft Learn, Show bugs on backlogs and boards (updated 2025-12-22)
    accessed: 2026-11-02
  - id: ado-process
    resource: https://github.com/MicrosoftDocs/azure-devops-docs/blob/main/docs/boards/work-items/guidance/choose-process.md
    title: Azure DevOps docs, Choose a process (source file)
    accessed: 2026-11-02
  - id: gh-issue-types
    resource: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization
    title: GitHub Docs, Managing issue types in an organization
    accessed: 2026-11-02
  - id: pivotal-stories
    resource: https://www.pivotaltracker.com/blog/principles-of-effective-story-writing-the-pivotal-labs-way
    title: Pivotal Tracker blog, Principles of effective story writing, the Pivotal Labs way
    accessed: 2026-11-02
  - id: cohn-bugs-backlog
    resource: https://www.mountaingoatsoftware.com/blog/bugs-on-the-product-backlog
    title: Mike Cohn, Bugs on the Product Backlog
    accessed: 2026-11-02
  - id: cohn-bug-points
    resource: https://www.mountaingoatsoftware.com/blog/should-story-points-be-assigned-to-a-bug-fixing-story
    title: Mike Cohn, Should Story Points Be Assigned to a Bug Fixing Story? (updated 26 Sep 2018)
    accessed: 2026-11-02
---

# How tools place a bug

| Tool | Where Bug sits | Source |
| --- | --- | --- |
| Jira | Middle level, a peer of Story and Task under Epic; Sub-task below all three | [^jira-overview] |
| GitHub | Default org issue types are Task, Bug, Feature (peers); up to 25 types | [^gh-issue-types] |
| Azure DevOps | Team setting: bugs as **Requirements**, as **Tasks**, or **not on backlogs or boards** | [^ado-manage-bugs] [^ado-show-bugs] |
| Pivotal Tracker | Its own story type; not pointed | [^pivotal-stories] |

## Azure DevOps "bugs behavior"

- **As requirements:** ranked with stories, estimated, on the board, counted in velocity
  and forecasts, visible on delivery plans.[^ado-manage-bugs]
- **As tasks:** estimated like tasks, on the sprint taskboard, linked as **child items**
  of a story ("the natural parent work item type for Bugs").[^ado-manage-bugs]
- **Not on boards:** managed with queries only.[^ado-manage-bugs]
- The pages read do not state a per-process default. The Basic process has no Bug type
  and uses Issue instead.[^ado-show-bugs] [^ado-process]

# What practitioners say

- Pivotal: "A bug is a defect in a feature that has already been accepted, regardless of
  when it was accepted"; bugs carry no points.[^pivotal-stories]
- Cohn: a bug in the current sprint's work: tell the developer at once ("yell"), a task
  card second; older bugs: "The ideal situation is to put the bugs right onto the product
  backlog."[^cohn-bugs-backlog] On legacy defects he usually assigns points.[^cohn-bug-points]
- The two rules agree: **a defect in unfinished work is part of that work; a defect in
  accepted work is new backlog work.**

# Done

A bug is done when the faulty behaviour no longer occurs and that is shown: a test or
reproduction that failed before the fix passes after it, and the fix is merged. The
definition is the same at either level; only the carrier changes.

# For the kit

- **Default:** Kind `bug` as a **story-level** issue (Azure "as requirements"; Jira and
  GitHub peers). Parent: the epic of the feature it breaks, or none.
- **Bug in work still open** (its PR not merged): fix it in that PR; no new item.
- **Alternative:** bugs as sub-issues of a story (Azure "as tasks"), for a defect found
  while the story is in review. Trade-off: keeps the story open and visible, but hides
  the bug from story-level views and queues.
- See the [mapping](kind-to-level-mapping.md).

# Caveats

- SAFe's treatment of defects was not found in a primary page during this sweep; it is
  left out rather than guessed.
- The Pivotal blog post has no date; Pivotal Tracker itself has been retired, so the page
  may disappear.
