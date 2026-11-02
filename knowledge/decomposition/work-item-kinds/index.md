# Work item kinds

* [Bug](bug.md) - Tools disagree on where a defect sits; Jira and GitHub make it a peer of story and task, Azure DevOps lets each team choose requirement-level or task-level, and practitioners split bugs found in current work from bugs in accepted work
* [Decision](decision.md) - A decision is recorded as a short, numbered, immutable record (an ADR) kept in the repository; the work item that makes the decision links to it, and the record outlives the item
* [Enabler work, chores and technical debt](enabler-and-chore.md) - Work with no direct user value (infrastructure, refactoring, upkeep, debt) is filed as an enabler story at the same level and under the same rules as user stories, or paid down inside the feature work that touches it
* [Finding](finding.md) - A finding is the output of a spike, research task or experiment, not a unit of work; research and ML practice record it as a dated, append-only entry tied to a hypothesis and its evidence
* [GTD categories and work-item kinds](gtd-categories.md) - GTD sorts by commitment and actionability (project, next action, waiting for, someday/maybe, reference), not by kind of work, so each work-item kind maps to a GTD list by its state, and non-actionable outputs map to reference
* [Kind-to-level mapping (draft for sign-off)](kind-to-level-mapping.md) - Draft table placing each work-item kind at a level or carrier in an Epic/Story/Task hierarchy, with its done condition, rationale, alternatives and trade-offs; it awaits the owner's sign-off
* [Questions, blockers and impediments](question-and-blocker.md) - Mainstream practice marks a blocked or waiting item in place (a flag, a sticky, a dependency) rather than moving it or making a new story; separate impediment items exist but sit off the backlog
* [Research task](research-task.md) - Broader investigation than a spike, whose deliverable is a written, sourced knowledge document rather than a go/no-go answer; established practice files it as exploration enabler work
* [Spike](spike.md) - A short, time-boxed investigation that buys knowledge to cut risk or firm up an estimate; its output is a demonstrable finding, and its code is usually thrown away
