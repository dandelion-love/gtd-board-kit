---
type: Practice
title: Enabler work, chores and technical debt
description: Work with no direct user value (infrastructure, refactoring, upkeep, debt) is filed as an enabler story at the same level and under the same rules as user stories, or paid down inside the feature work that touches it.
tags: [work-item-kinds, task, enabler, chore, tech-debt]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:05:00Z }
sources:
  - id: safe-enablers
    resource: https://scaledagileframework.com/enablers/
    title: SAFe, Enablers (last update 13 October 2023)
    accessed: 2026-11-02
  - id: safe-story
    resource: https://scaledagileframework.com/story
    title: SAFe, Story (last update 7 December 2022)
    accessed: 2026-11-02
  - id: pivotal-stories
    resource: https://www.pivotaltracker.com/blog/principles-of-effective-story-writing-the-pivotal-labs-way
    title: Pivotal Tracker blog, Principles of effective story writing, the Pivotal Labs way
    accessed: 2026-11-02
  - id: fowler-debt
    resource: https://martinfowler.com/bliki/TechnicalDebt.html
    title: Martin Fowler, TechnicalDebt (bliki, rewritten 21 May 2019)
    accessed: 2026-11-02
  - id: jira-overview
    resource: https://www.atlassian.com/software/jira/guides/issues/overview
    title: Atlassian, Jira work items overview
    accessed: 2026-11-02
  - id: ado-process
    resource: https://github.com/MicrosoftDocs/azure-devops-docs/blob/main/docs/boards/work-items/guidance/choose-process.md
    title: Azure DevOps docs, Choose a process (source file)
    accessed: 2026-11-02
---

# What established practice says

- **SAFe enablers** "extend the architectural runway" and are captured "as a type of
  Epic, Capability, Feature, or Story", prioritized "according to the same rules" as
  business items.[^safe-enablers] Four types: exploration, architectural, infrastructure,
  compliance.[^safe-enablers]
- **Enabler stories** cover refactoring, spikes, build and deploy infrastructure, and
  verifying qualities like performance and security; they may use technical language
  instead of the user-voice form.[^safe-story]
- **Chores (Pivotal):** "a story that is necessary but provides no direct, obvious value
  to the user"; not pointed.[^pivotal-stories] Chores were a story type, a peer of
  features and bugs.
- **Task as a type:** Jira's Task is a peer of Story ("a task that needs to be done");
  Sub-task is the decomposition below.[^jira-overview] Azure's Task is the child of a
  story that carries remaining-work hours.[^ado-process] The word "task" thus names two
  levels in common tools.
- **Technical debt (Fowler):** cruft is internal quality deficiency; interest is the
  extra effort on each change.[^fowler-debt] He favours paying it down "gradually", in the
  areas being modified, and leaving "crufty but stable" areas alone.[^fowler-debt] He does
  not prescribe a separate debt item.

# Done

- Enabler story: demonstrated "by showing the knowledge gained, artifacts produced", or a
  stub or UI.[^safe-story] In the kit: PR merged, checks pass, and the stated technical
  outcome (a measure, a removed warning, a passing job) is shown in the PR.
- Debt paid inside a feature: done with that feature; no separate condition.

# For the kit

- The kit's Kind `task` covers two things that should be told apart:
  1. **Enabler or chore with its own PR** → a **story-level issue** (Kind `task`, or a
     new `enabler`), technical wording allowed, same acceptance-criteria and DoD rules.
  2. **A step inside a story** → a **checklist item** in the story body (or a sub-issue
     when it needs its own claim and PR).
- Technical debt: pay it in the story that touches the area (Fowler); open its own item
  only when it is large or blocks other work.
- See the [mapping](kind-to-level-mapping.md).

# Caveats

- Whether the kit's existing `task` Kind means level 1 or level 2 above is not stated in
  the public kit text read for this note; the owner should pin it.
