---
type: Comparison
title: Labels vs issue types vs issue fields vs project fields
description: Which GitHub carrier to use for which kind of work-item metadata, by cardinality, scope, typing, portability and API cost, as of November 2026.
tags: [github, labels, issue-types, issue-fields, projects, comparison, epic-story-task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:20:00Z }
sources:
  - {id: docs-types, title: "Managing issue types in an organization (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization", accessed: 2026-11-02}
  - {id: docs-fields, title: "Managing issue fields in your organization (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-fields-in-your-organization", accessed: 2026-11-02}
  - {id: docs-fields-proj, title: "About issue fields in projects (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-issue-fields", accessed: 2026-11-02}
  - {id: docs-labels, title: "Managing labels (GitHub Docs)", resource: "https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels", accessed: 2026-11-02}
  - {id: docs-about-proj, title: "About Projects (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects", accessed: 2026-11-02}
  - {id: docs-rest-issues, title: "REST API endpoints for issues (GitHub Docs)", resource: "https://docs.github.com/en/rest/issues/issues", accessed: 2026-11-02}
  - {id: cl-2026-03-12, title: "Issue fields public preview, changelog 2026-03-12", resource: "https://github.blog/changelog/", changelog_entry: "2026-03-12-issue-fields-structured-issue-metadata-is-in-public-preview", accessed: 2026-11-02}
  - {id: cl-2026-08-27, title: "Better label management on issues is generally available, changelog 2026-08-27", resource: "https://github.blog/changelog/", changelog_entry: "2026-08-27-label-archiving-is-generally-available", accessed: 2026-11-02}
---

# The four carriers

| Carrier | Cardinality | Defined at | Typed? | Travels with issue? | Works on PRs | Personal repos |
| --- | --- | --- | --- | --- | --- | --- |
| Label | many | repository[^docs-labels] | no (name only) | yes | yes | yes |
| Issue type | exactly 0 or 1 | organization, max 25[^docs-types] | enum | yes | no | no (org only) |
| Issue field | one value per field | organization, max 25[^docs-fields] | text, number, date, single/multi-select | yes, to every project[^docs-fields-proj] | no | no |
| Project field | one value per field per project | the project, max 50 fields[^docs-about-proj] | text, number, date, single/multi-select, iteration | **no**, lost if the item leaves the project | yes | yes |

# When each is right

- **Issue type** for *what the item is*: Epic, Story, Task, Bug, Spike. One value, enforced
  as one; shows in search and Projects.
- **Issue field** for *typed attributes of the item that must survive across boards*:
  priority, size/effort, target date, risk. GitHub itself positions fields as the fix for
  `priority/p0` label hacks[^cl-2026-03-12].
- **Project field** for *board state*: Status, Iteration, rank. Iteration exists only here.
- **Label** for *many-valued flags, cross-cutting tags, and anything that must work on PRs
  or in personal-account repos*: `needs:review`, `agent-proposed`, area tags. Labels are also
  the fallback carrier for type when the repo is not in an organization.

# Practical notes

- Labels are per repository. A multi-repo kit must sync them. Archived labels (GA
  2026-08-27) keep history but leave the picker[^cl-2026-08-27].
- Labels, type and milestone set on issue create by a user without push access are
  **silently dropped**[^docs-rest-issues].
- A label is free text: `Story` and `story` are two labels. Types and select fields avoid
  that drift.
- A project field value disappears with the item; an issue field value does not.

# Caveats

- Issue-field values on PRs: not supported, so a PR's size or priority stays a label or
  project field.
- Whether a kit should mirror type into a label (for personal repos and PRs) is a design
  choice, not a GitHub rule.

[^docs-types]: Managing issue types, GitHub Docs.
[^docs-fields]: Managing issue fields, GitHub Docs.
[^docs-fields-proj]: About issue fields in projects, GitHub Docs.
[^docs-labels]: Managing labels, GitHub Docs.
[^docs-about-proj]: About Projects, GitHub Docs.
[^docs-rest-issues]: REST API endpoints for issues, GitHub Docs.
[^cl-2026-03-12]: Issue fields public preview, 2026-03-12.
[^cl-2026-08-27]: Label management GA, 2026-08-27.
