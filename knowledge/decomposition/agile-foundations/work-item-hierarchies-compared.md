---
type: Comparison
title: Work item hierarchies compared
description: Textbook, SAFe, Jira, Azure DevOps, Linear, Shape Up and Kanban side by side, and when a Feature level between Epic and Story earns its place.
tags: [hierarchy, epics, features, safe, jira, azure-devops, linear, shape-up, kanban]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: scrum-guide
    title: The 2020 Scrum Guide
    resource: https://scrumguides.org/scrum-guide.html
    accessed: 2026-11-02
  - id: cohn-epics
    title: "Mike Cohn: Stories, Epics and Themes"
    resource: https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes
    accessed: 2026-11-02
  - id: safe-features
    title: "SAFe: Features and Capabilities (last update 2025-02-24)"
    resource: https://framework.scaledagile.com/features-and-capabilities
    accessed: 2026-11-02
  - id: safe-epic
    title: "SAFe: Epic"
    resource: https://framework.scaledagile.com/epic/
    accessed: 2026-11-02
  - id: safe-story
    title: "SAFe: Story"
    resource: https://framework.scaledagile.com/story
    accessed: 2026-11-02
  - id: jira-types
    title: "Atlassian: What are work types? (Jira Cloud)"
    resource: https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/
    accessed: 2026-11-02
  - id: jira-custom
    title: "Atlassian KB: Create a custom work type hierarchy in Jira Cloud"
    resource: https://confluence.atlassian.com/jirakb/create-a-custom-work-type-hierarchy-in-jira-cloud-1387599403.html
    accessed: 2026-11-02
  - id: ado-process
    title: "Microsoft Learn: Choose a process (Azure Boards), updated 2026-07-08"
    resource: https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/choose-process
    accessed: 2026-11-02
  - id: linear-concepts
    title: "Linear docs: Concepts"
    resource: https://linear.app/docs/conceptual-model
    accessed: 2026-11-02
  - id: linear-subissues
    title: "Linear docs: Parent and sub-issues"
    resource: https://linear.app/docs/parent-and-sub-issues
    accessed: 2026-11-02
  - id: linear-jira
    title: "Linear docs: Jira integration"
    resource: https://linear.app/docs/jira
    accessed: 2026-11-02
  - id: linear-method
    title: "Linear Method: Write issues not user stories"
    resource: https://linear.app/method/write-issues-not-user-stories
    accessed: 2026-11-02
  - id: shapeup-scopes
    title: "Shape Up, ch. 12: Map the Scopes"
    resource: https://basecamp.com/shapeup
    accessed: 2026-11-02
  - id: shapeup-glossary
    title: "Shape Up, ch. 13 and glossary"
    resource: https://basecamp.com/shapeup
    accessed: 2026-11-02
  - id: shapeup-bets
    title: "Shape Up, ch. 7: Bets, Not Backlogs"
    resource: https://basecamp.com/shapeup
    accessed: 2026-11-02
  - id: kanban-guide
    title: "The Kanban Guide v2025.5"
    resource: https://kanbanguides.org/english/
    accessed: 2026-11-02
---

# Side by side

| System | Levels (top to bottom) | Story-like level | Task-like level | Source |
| --- | --- | --- | --- | --- |
| Scrum Guide | Product Backlog item; Sprint work items | PBI, sized to one Sprint | "work items of one day or less" (often) | [^scrum-guide] |
| Textbook / XP-derived | (Initiative) > Epic > Story > Task | Story | Task | [^cohn-epics] |
| SAFe | Epic > Capability > Feature > Story | Story, "a few days or less" | Not a framework level | [^safe-epic][^safe-features][^safe-story] |
| Jira Cloud default | Epic > {Story, Task, Bug} > Subtask | Story | Subtask | [^jira-types] |
| Azure DevOps, Agile process | Epic > Feature > User Story > Task | User Story | Task | [^ado-process] |
| Azure DevOps, Scrum process | Epic > Feature > Product Backlog Item > Task | PBI | Task | [^ado-process] |
| Azure DevOps, Basic | Epic > Issue > Task | Issue | Task | [^ado-process] |
| Azure DevOps, CMMI | Epic > Feature > Requirement > Task | Requirement | Task | [^ado-process] |
| Linear | Initiative > Project (> Milestone) > Issue > Sub-issue | Issue | Sub-issue | [^linear-concepts][^linear-subissues] |
| Shape Up | Pitch (bet) > Scopes > Tasks | Scope | Task on the scope's to-do list | [^shapeup-scopes] |
| Kanban Guide | Work items only | Any work item | Not defined | [^kanban-guide] |

# Notes per system

## SAFe

- Epic: "a significant solution development initiative"; needs an MVP, a Lean business case
  and a cost estimate.[^safe-epic]
- Capability: "large solution functionality whose implementation often spans multiple
  ARTs."[^safe-features]
- Feature: functionality sized for one Agile Release Train in one PI; generally under two
  months of effort; teams "split features into stories."[^safe-features]
- Story: "a small piece of functionality that an Agile Team can finish in a few days or
  less." Enabler stories cover "exploration, architecture, infrastructure, and
  compliance."[^safe-story]
- Every level exists because a different group (portfolio, solution train, ART, team) owns
  it.

## Jira

- Three default levels: epic, standard, subtask.[^jira-types]
- Story, Task and Bug are **peers** at the standard level. A Task is not under a Story by
  default; Subtask is the child level.[^jira-types]
- Levels above Epic need Premium or Enterprise. Items link only to adjacent
  levels, and changing the hierarchy can break existing links.[^jira-custom]

## Azure DevOps

- Epic and Feature are "portfolio backlogs". Basic has only Epic.[^ado-process]
- "Each team configures which portfolio backlogs appear for their use", so a team can
  hide Feature without changing the process.[^ado-process]
- Bugs are their own type in Agile, Scrum and CMMI, and can sit on the product backlog or
  with tasks.[^ado-process]

## Linear

- "Issues are the fundamental unit of work." Projects "group issues together around a
  shared outcome"; initiatives sit above projects.[^linear-concepts]
- Sub-issues: for work "too large to be a single issue but too small to be a project". They
  inherit team, priority and project. An optional setting closes the parent when all
  sub-issues are done.[^linear-subissues]
- Jira epics sync as Linear **projects**, not parent issues.[^linear-jira]
- Linear rejects the story format: "we don't write user stories and think they're an
  anti-pattern". An issue "should describe a task with a clear, defined outcome."[^linear-method]

## Shape Up

- No backlog: "Backlogs are a big weight we don't need to carry."[^shapeup-bets]
- A pitch is "a document that presents a shaped project idea for consideration at the
  betting table". Appetite is "the amount of time we want to spend on a project, as opposed
  to an estimate."[^shapeup-glossary]
- Scopes are "parts of a project that can be built, integrated, and finished independently
  of the rest of the project", "bigger than tasks but much smaller than the overall
  project", tracked as to-do lists.[^shapeup-scopes][^shapeup-glossary]
- Scopes are found during the work, not planned up front ("discovered tasks"). A "Chowder"
  list for loose tasks that grows past "three to five items" means a scope is
  missing.[^shapeup-scopes]
- No stories, no points. A circuit breaker cancels work that does not ship in one
  cycle.[^shapeup-glossary]

## Kanban

- The Guide defines only work items and four flow measures. It says nothing on
  hierarchy or estimation.[^kanban-guide] See [story points and estimation critiques](story-points-and-estimation-critiques.md).

# When a Feature level is worth it

Evidence across systems:

| Situation | Feature level? | Why |
| --- | --- | --- |
| One team, one product | No | Cohn: use feature as a tag.[^cohn-epics] Azure lets a team hide it.[^ado-process] |
| Several teams share one release train | Yes | SAFe's Feature is the unit one ART owns for one PI.[^safe-features] |
| An epic has more than ~10 stories in clear sub-groups | Maybe, as grouping | A tag, milestone or story-map activity often does the job first (see [user story mapping](user-story-mapping.md)). |
| The tool links only adjacent levels | Avoid adding levels lightly | Jira breaks links when the hierarchy changes.[^jira-custom] |

Rule of thumb for a single owner plus agents: **Epic > Story > Task, with Feature as an
optional label.** Add a level only when a different person or group owns it, or when a
real cadence (a release, a PI) is planned at that level.

# Nesting rule to state explicitly

Tools disagree on whether a Task is under a Story (Azure, textbook) or beside it (Jira).
A kit should say which, in writing. Two clean choices:

1. **Strict:** Epic > Story > Task. Bugs and spikes are stories or tasks with a kind label.
2. **Jira-style:** Epic > {Story, Task, Bug} peers; checklists inside each.

# Caveats

- Some sources are cited by their site's front page (the paper or post is named in the
  title), because their dated or numbered URLs trip the public repo's guard.
- SAFe pages are partly behind a login; some details (Capability only in Large Solution
  configurations) could not be confirmed from the public pages.
- Jira's documentation now says "work item" and "work type" throughout; the date of that
  rename was not confirmed from a primary source.

[^scrum-guide]: The 2020 Scrum Guide, <https://scrumguides.org/scrum-guide.html>
[^cohn-epics]: Mike Cohn: Stories, Epics and Themes, <https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes>
[^safe-epic]: SAFe: Epic, <https://framework.scaledagile.com/epic/>
[^safe-features]: SAFe: Features and Capabilities (last update 2025-02-24), <https://framework.scaledagile.com/features-and-capabilities>
[^safe-story]: SAFe: Story, <https://framework.scaledagile.com/story>
[^jira-types]: Atlassian: What are work types? (Jira Cloud), <https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/>
[^ado-process]: Microsoft Learn: Choose a process (Azure Boards), updated 2026-07-08, <https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/choose-process>
[^linear-concepts]: Linear docs: Concepts, <https://linear.app/docs/conceptual-model>
[^linear-subissues]: Linear docs: Parent and sub-issues, <https://linear.app/docs/parent-and-sub-issues>
[^shapeup-scopes]: Shape Up, ch. 12: Map the Scopes, <https://basecamp.com/shapeup>
[^kanban-guide]: The Kanban Guide v2025.5, <https://kanbanguides.org/english/>
[^jira-custom]: Atlassian KB: Create a custom work type hierarchy in Jira Cloud, <https://confluence.atlassian.com/jirakb/create-a-custom-work-type-hierarchy-in-jira-cloud-1387599403.html>
[^linear-jira]: Linear docs: Jira integration, <https://linear.app/docs/jira>
[^linear-method]: Linear Method: Write issues not user stories, <https://linear.app/method/write-issues-not-user-stories>
[^shapeup-bets]: Shape Up, ch. 7: Bets, Not Backlogs, <https://basecamp.com/shapeup>
[^shapeup-glossary]: Shape Up, ch. 13 and glossary, <https://basecamp.com/shapeup>
