---
type: Reference
title: What the Scrum Guide 2020 defines, and what it leaves out
description: The 2020 Scrum Guide defines Product Backlog items, the Product Goal, the Sprint Goal and the Definition of Done, but not epics, stories, tasks, features, story points, velocity or a Definition of Ready.
tags: [scrum, backlog, definition-of-done, terminology]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: scrum-guide
    title: The 2020 Scrum Guide (Schwaber and Sutherland)
    resource: https://scrumguides.org/scrum-guide.html
    accessed: 2026-11-02
  - id: cohn-epics
    title: "Mike Cohn: Stories, Epics and Themes"
    resource: https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes
    accessed: 2026-11-02
  - id: scrumorg-ac
    title: "Scrum.org: What is the difference between the DoD and acceptance criteria?"
    resource: https://www.scrum.org/resources/what-difference-between-dod-and-acceptance-criteria
    accessed: 2026-11-02
---

# Summary

Scrum is a framework for the backlog, the cadence and the quality bar. It is not a
requirements format. The Guide names one kind of work item, the **Product Backlog item
(PBI)**, and leaves its shape open. Epic, Story, Task and Feature come from other sources
(see [origins of Epic, Story and Feature](origins-of-epic-story-feature.md)).

# What the Guide defines

| Term | What the Guide says | Note |
| --- | --- | --- |
| Product Backlog | "an emergent, ordered list of what is needed to improve the product"[^scrum-guide] | Ordered, not prioritised by category. |
| Product Backlog item | Has attributes that "often vary with the domain of work"[^scrum-guide] | No template, no required fields. |
| Refinement | "the act of breaking down and further defining Product Backlog items"[^scrum-guide] | Continuous, not a gate. |
| Ready for selection | PBIs "that can be Done by the Scrum Team within one Sprint are deemed ready for selection"[^scrum-guide] | This is the only "ready" wording. It is a size test, not a checklist. |
| Sizing | "The Developers who will be doing the work are responsible for the sizing."[^scrum-guide] | No unit is named. |
| Product Goal | "a future state of the product which can serve as a target for the Scrum Team to plan against"[^scrum-guide] | Commitment of the Product Backlog. |
| Sprint Goal | "the single objective for the Sprint"[^scrum-guide] | Commitment of the Sprint Backlog. |
| Definition of Done | Commitment of the Increment. If not an organisational standard, "the Scrum Team must create a Definition of Done appropriate for the product."[^scrum-guide] | Owned by the whole Scrum Team. |
| Not Done | A PBI that misses the DoD "cannot be released or even presented at the Sprint Review" and "returns to the Product Backlog for future consideration."[^scrum-guide] | Hard rule. |
| Increment | "The moment a Product Backlog item meets the Definition of Done, an Increment is born."[^scrum-guide] | Done is per item, not per Sprint. |
| Sprint Backlog work | Planning "is often done by decomposing Product Backlog items into smaller work items of one day or less."[^scrum-guide] | The nearest thing to a Task. Note "often", not "must". |

Each artifact carries one commitment: Product Goal, Sprint Goal, Definition of Done.[^scrum-guide]

# What the Guide does not define

The 2020 Guide never uses these words:[^scrum-guide]

- user story, epic, theme, feature, task (it says "work items");
- story points, velocity;
- Definition of Ready;
- acceptance criteria. Scrum.org calls acceptance criteria "not technically part of Scrum, but is a valuable complementary practice."[^scrumorg-ac]

Cohn says the same of the hierarchy: "the Scrum framework doesn't say anything about
epics, stories, and themes."[^cohn-epics]

The Guide does mention burn-downs, burn-ups and cumulative flow, as forecasting practices
that "do not replace the importance of empiricism."[^scrum-guide]

# What this means for a board kit

- An honest label: **Scrum for the backlog, goals and Done; agile conventions for the
  hierarchy and story format.**
- "Fits in one Sprint" is the Guide's own size test for a PBI. "One day or less" is its own
  (optional) size hint for a work item inside the Sprint.
- The Definition of Done is a team artifact applied to every item. Acceptance criteria are
  per item and come from outside Scrum (see
  [acceptance criteria, DoD and DoR](acceptance-criteria-dod-dor.md)).
- A kit without Sprints can keep the Product Goal and Definition of Done unchanged; the
  Sprint Goal maps to whatever cadence or milestone the board uses.

# Caveats

- The Guide is short and changes rarely. The 2020 edition is current as of the access
  date; check scrumguides.org for a newer edition before quoting.

[^scrum-guide]: The 2020 Scrum Guide (Schwaber and Sutherland), <https://scrumguides.org/scrum-guide.html>
[^scrumorg-ac]: Scrum.org: What is the difference between the DoD and acceptance criteria?, <https://www.scrum.org/resources/what-difference-between-dod-and-acceptance-criteria>
[^cohn-epics]: Mike Cohn: Stories, Epics and Themes, <https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes>
