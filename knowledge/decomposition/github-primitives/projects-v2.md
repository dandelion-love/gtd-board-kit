---
type: Reference
title: GitHub Projects (v2) for an Epic/Story/Task board
description: What Projects offers a hierarchy board as of November 2026 - field types, iteration, parent and sub-issue progress fields, hierarchy view, built-in workflows, limits, and the GraphQL and REST APIs.
tags: [github, projects, board, iteration, hierarchy, epic-story-task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:10:00Z }
sources:
  - {id: cl-2025-04-09, title: "Evolving GitHub Issues and Projects (GA), changelog 2025-04-09", resource: "https://github.blog/changelog/", changelog_entry: "2025-04-09-evolving-github-issues-and-projects", accessed: 2026-11-02}
  - {id: cl-2025-09-11, title: "A REST API for GitHub Projects, sub-issues improvements, and more, changelog 2025-09-11", resource: "https://github.blog/changelog/", changelog_entry: "2025-09-11-a-rest-api-for-github-projects-sub-issues-improvements-and-more", accessed: 2026-11-02}
  - {id: cl-2026-01-15, title: "Hierarchy view now available in GitHub Projects, changelog 2026-01-15", resource: "https://github.blog/changelog/", changelog_entry: "2026-01-15-hierarchy-view-now-available-in-github-projects", accessed: 2026-11-02}
  - {id: cl-2026-03-05, title: "Hierarchy view improvements and file uploads in issue forms, changelog 2026-03-05", resource: "https://github.blog/changelog/", changelog_entry: "2026-03-05-hierarchy-view-improvements-and-file-uploads-in-issue-forms", accessed: 2026-11-02}
  - {id: cl-2026-03-19, title: "Hierarchy view in GitHub Projects is now generally available, changelog 2026-03-19", resource: "https://github.blog/changelog/", changelog_entry: "2026-03-19-hierarchy-view-in-github-projects-is-now-generally-available", accessed: 2026-11-02}
  - {id: cl-2026-04-09, title: "Release information in issue sidebar and default values for project fields, changelog 2026-04-09", resource: "https://github.blog/changelog/", changelog_entry: "2026-04-09-release-info-in-issue-sidebar-and-project-defaults", accessed: 2026-11-02}
  - {id: cl-2026-07-16, title: "Advanced search for Projects is generally available, changelog 2026-07-16", resource: "https://github.blog/changelog/", changelog_entry: "2026-07-16-advanced-search-for-projects-is-generally-available", accessed: 2026-11-02}
  - {id: cl-2026-08-07, title: "Relates to preview and multi-select fields GA, changelog 2026-08-07", resource: "https://github.blog/changelog/", changelog_entry: "2026-08-07-connecting-issues-and-multi-select-field-support", accessed: 2026-11-02}
  - {id: docs-about, title: "About Projects (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects", accessed: 2026-11-02}
  - {id: docs-archive, title: "Archiving items from your project (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/archiving-items-from-your-project", accessed: 2026-11-02}
  - {id: docs-iter, title: "About iteration fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields", accessed: 2026-11-02}
  - {id: docs-progress, title: "About parent issue and sub-issue progress fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-parent-issue-and-sub-issue-progress-fields", accessed: 2026-11-02}
  - {id: docs-builtin, title: "Using the built-in automations (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations", accessed: 2026-11-02}
  - {id: docs-autoadd, title: "Adding items automatically (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically", accessed: 2026-11-02}
  - {id: docs-rest-proj, title: "REST API endpoints for Projects (GitHub Docs)", resource: "https://docs.github.com/en/rest/projects/projects", accessed: 2026-11-02}
  - {id: docs-rest-fields, title: "REST API endpoints for Project fields (GitHub Docs)", resource: "https://docs.github.com/en/rest/projects/fields", accessed: 2026-11-02}
  - {id: docs-rest-items, title: "REST API endpoints for Project items (GitHub Docs)", resource: "https://docs.github.com/en/rest/projects/items", accessed: 2026-11-02}
  - {id: docs-rest-views, title: "REST API endpoints for Project views (GitHub Docs)", resource: "https://docs.github.com/en/rest/projects/views", accessed: 2026-11-02}
  - {id: docs-api-guide, title: "Using the API to manage Projects (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects", accessed: 2026-11-02}
---

# What it is

A Project is a board or table over issues and PRs from many repositories. Its custom
fields live **in the project**, not on the issue. It is the native carrier for Status,
Iteration (Sprint) and planning views. See [issue-fields.md](issue-fields.md) for values
that live on the issue.

# Field types

| Kind | Types | Source |
| --- | --- | --- |
| Custom | text, number, date, single select, iteration; multi-select (GA 2026-08-07) | [^docs-about][^cl-2026-08-07] |
| Built-in | assignees, labels, milestone, repository, reviewers, linked PRs, Type, Parent issue, Sub-issue progress | [^docs-about][^docs-rest-items][^docs-progress] |
| Issue fields | org-level fields added as columns | [^cl-2025-04-09] |
| Defaults | text, number and single-select can have a default applied on add (2026-04-09) | [^cl-2026-04-09] |

# Iteration fields

- Length in days or weeks; breaks between iterations; three iterations made at creation[^docs-iter].
- Filter `iteration:@current`, `@previous`, `@next`, ranges like `@current..@current+3`[^docs-iter].
- No maximum count or duration is documented[^docs-iter].

# Hierarchy support

| Feature | What it does | Date |
| --- | --- | --- |
| Parent issue field | group by parent; filter `parent-issue:"owner/repo#n"` | docs[^docs-progress] |
| Sub-issue progress field | how many sub-issues are done | docs[^docs-progress] |
| Hierarchy view (preview) | table view expands sub-issues up to 8 levels; group, sort, filter keep the tree | 2026-01-15[^cl-2026-01-15] |
| Improvements | `sub-issues.is:open` style filters; dedupe "in most cases"; saved expand state | 2026-03-05[^cl-2026-03-05] |
| Hierarchy view **GA** | on by default for new views; View menu > Show hierarchy | 2026-03-19[^cl-2026-03-19] |

Sub-issues inherit the parent's project by default (2025-09-11)[^cl-2025-09-11].
*Sub-issues progress* cannot be a group-by field[^docs-rest-views].

# Built-in workflows

- Defaults on: item closed -> Status Done; PR merged -> Status Done[^docs-builtin].
- Others: item added -> set Status; auto-archive; auto-add from a repository by filter[^docs-builtin].
- Auto-add filters: `is`, `label`, `reason`, `assignee`, `no`; it does not add existing
  items[^docs-autoadd].
- Auto-add workflows per project: Free 1, Pro 5, Team 5, Enterprise Cloud 20[^docs-autoadd].
- No doc describes creating built-in workflows through the API.

# Limits

| Limit | Value | Source and date |
| --- | --- | --- |
| Items per project | 50,000 (active plus archived) | raised from 1,200, changelog 2025-04-09[^cl-2025-04-09]; docs[^docs-archive] |
| Fields per project | 50, including built-in and issue fields | docs[^docs-about] |
| Views per project | not documented | - |
| Group-by in a view | one field (horizontal), one vertical for board | REST views docs[^docs-rest-views] |

# APIs

- GraphQL is the main API[^docs-about]: `createProjectV2`, `updateProjectV2`, `addProjectV2ItemById`,
  `addProjectV2DraftIssue`, `updateProjectV2ItemFieldValue` (text, number, date, single select,
  iteration), `deleteProjectV2Item`. Add and update need two calls; labels, assignees and
  milestone are set on the issue, not the item; tokens need the `project` scope[^docs-api-guide].
- REST (announced 2025-09-11)[^cl-2025-09-11]:

| Area | What REST can do | Source |
| --- | --- | --- |
| Projects | list and get only; no create | [^docs-rest-proj] |
| Fields | list, get, **create** (text, number, date, single select, iteration) | [^docs-rest-fields] |
| Items | list, add issue or PR, get, update field values, delete | [^docs-rest-items][^cl-2025-09-11] |
| Views | **create** only (`table`, `board`, `roadmap`; filter, sort, group); create endpoint added 2026-01-15 | [^docs-rest-views][^cl-2026-01-15] |

- User-owned project REST endpoints do not accept GitHub App or fine-grained tokens; the
  org ones do[^docs-rest-proj][^docs-rest-views].
- Item lists return only the title unless `fields=` is passed[^docs-rest-items].

# Filters

- Boolean `AND` / `OR` in view filters GA 2026-07-16[^cl-2026-07-16].
- `type:`, `has:`, `no:`, `is:`, `parent-issue:`, `iteration:`; see
  [search-and-filter-syntax.md](search-and-filter-syntax.md).

# Caveats

- Whether hierarchy view is table-only is not stated in the GA post; the preview post said table.
- Sub-issue progress across several levels is undocumented.
- REST views have no update or delete; view fixes still need the UI or GraphQL.
- The REST fields page lists only `iteration` as a `data_type` value while its examples
  show five types; an org POST also needs `issue_field_id`. Docs look inconsistent.

[^cl-2025-04-09]: Evolving GitHub Issues and Projects, 2025-04-09.
[^cl-2025-09-11]: REST API for Projects, 2025-09-11.
[^cl-2026-01-15]: Hierarchy view preview, 2026-01-15.
[^cl-2026-03-05]: Hierarchy view improvements, 2026-03-05.
[^cl-2026-03-19]: Hierarchy view GA, 2026-03-19.
[^cl-2026-04-09]: Project field defaults, 2026-04-09.
[^cl-2026-07-16]: Advanced search for Projects GA, 2026-07-16.
[^cl-2026-08-07]: Multi-select GA, 2026-08-07.
[^docs-about]: About Projects, GitHub Docs.
[^docs-archive]: Archiving items, GitHub Docs.
[^docs-iter]: About iteration fields, GitHub Docs.
[^docs-progress]: Parent issue and sub-issue progress fields, GitHub Docs.
[^docs-builtin]: Using the built-in automations, GitHub Docs.
[^docs-autoadd]: Adding items automatically, GitHub Docs.
[^docs-rest-proj]: REST Projects, GitHub Docs.
[^docs-rest-fields]: REST Project fields, GitHub Docs.
[^docs-rest-items]: REST Project items, GitHub Docs.
[^docs-rest-views]: REST Project views, GitHub Docs.
[^docs-api-guide]: Using the API to manage Projects, GitHub Docs.
