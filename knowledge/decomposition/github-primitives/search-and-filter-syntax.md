---
type: Reference
title: GitHub search and filter syntax for hierarchy, types, fields and dependencies
description: The issue-search and Projects-filter qualifiers an agent can use to find Epics, Stories, Tasks, blocked work and field values, with which ones the official docs actually confirm.
tags: [github, search, filters, projects, epic-story-task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:25:00Z }
sources:
  - {id: docs-filter-issues, title: "Filtering and searching issues and pull requests (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests", accessed: 2026-11-02}
  - {id: docs-search, title: "Searching issues and pull requests (GitHub Docs)", resource: "https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests", accessed: 2026-11-02}
  - {id: docs-filter-proj, title: "Filtering projects (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/filtering-projects", accessed: 2026-11-02}
  - {id: docs-progress, title: "About parent issue and sub-issue progress fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-parent-issue-and-sub-issue-progress-fields", accessed: 2026-11-02}
  - {id: docs-fields-use, title: "Adding and managing issue fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-and-managing-issue-fields", accessed: 2026-11-02}
  - {id: docs-iter, title: "About iteration fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields", accessed: 2026-11-02}
  - {id: cl-2025-04-09, title: "Evolving GitHub Issues and Projects (GA), changelog 2025-04-09", resource: "https://github.blog/changelog/", changelog_entry: "2025-04-09-evolving-github-issues-and-projects", accessed: 2026-11-02}
  - {id: cl-2025-08-21, title: "Dependencies on issues, changelog 2025-08-21", resource: "https://github.blog/changelog/", changelog_entry: "2025-08-21-dependencies-on-issues", accessed: 2026-11-02}
  - {id: cl-2026-03-05, title: "Hierarchy view improvements, changelog 2026-03-05", resource: "https://github.blog/changelog/", changelog_entry: "2026-03-05-hierarchy-view-improvements-and-file-uploads-in-issue-forms", accessed: 2026-11-02}
  - {id: cl-2026-07-16, title: "Advanced search for Projects is generally available, changelog 2026-07-16", resource: "https://github.blog/changelog/", changelog_entry: "2026-07-16-advanced-search-for-projects-is-generally-available", accessed: 2026-11-02}
  - {id: blog-eng, title: "Introducing sub-issues (GitHub Blog, 2025-04-11)", resource: "https://github.blog/engineering/architecture-optimization/introducing-sub-issues-enhancing-issue-management-on-github/", accessed: 2026-11-02}
---

# Operators

- `AND`, `OR`, parentheses in issue search; GA 2025-04-09[^cl-2025-04-09]. Space means AND;
  nesting up to **five** levels[^docs-filter-issues].
- `AND` / `OR` in Projects view filters; GA 2026-07-16[^cl-2026-07-16].
- `-` negates a qualifier, but not `no:` qualifiers in issue search[^docs-search].

# Qualifiers by primitive

| Need | Qualifier | Where | Confirmed by |
| --- | --- | --- | --- |
| All Stories | `type:Story` (or `type:"Story"`) | issues, projects | docs[^docs-filter-issues][^docs-filter-proj] |
| Stories or Tasks | `type:Story OR type:Task` | issues | changelog 2025-04-09[^cl-2025-04-09] |
| Children of an Epic | `parent-issue:owner/repo#N` | projects (and issues, see caveat) | docs[^docs-filter-proj][^docs-progress] |
| Items with a parent | `has:parent-issue` | issues | engineering blog only[^blog-eng] |
| Items with children | `has:sub-issues-progress` | issues | engineering blog only[^blog-eng] |
| Filter on children | `sub-issues.is:open` | projects hierarchy view | changelog 2026-03-05[^cl-2026-03-05] |
| Blocked items | `is:blocked` | issues | changelog 2025-08-21[^cl-2025-08-21] |
| Blocking items | `is:blocking` | issues | changelog 2025-08-21[^cl-2025-08-21] |
| Blocked by X | `blocked-by:<issue>` | issues | changelog 2025-08-21[^cl-2025-08-21] |
| Blocking X | `blocking:<issue>` | issues | changelog 2025-08-21[^cl-2025-08-21] |
| Field value | `field.priority:high`, `field."target date":>=2026-03-01` | issues dashboard, repo issues | docs[^docs-fields-use] |
| Current sprint | `iteration:@current`, `iteration:@current..@current+3` | projects | docs[^docs-iter][^docs-filter-proj] |
| Empty project field | `no:priority`; `has:priority` | projects | docs[^docs-filter-proj] |
| Has a closing PR | `linked:pr`, `-linked:pr` | issues | docs[^docs-search] |

# Useful agent queries

- Ready Stories in an Epic: `parent-issue:owner/repo#N type:Story is:open -is:blocked`.
- Orphan Stories: `type:Story is:open no:parent-issue` (see caveat; may not exist).
- Stories with no PR yet: `type:Story is:open -linked:pr`.

# Caveats

- `parent-issue:` is documented for Projects; its use in plain issue search was not
  confirmed in the pages read.
- `has:sub-issues`, `no:parent-issue` and `has:parent-issue` do not appear in the current
  search docs. Only an engineering blog post names `has:parent-issue` and
  `has:sub-issues-progress`. Test before an agent depends on them.
- Dependency qualifiers come from the GA changelog; the search docs page does not list them.
- In issue search `type:` also means issue vs PR (`type:pr`, `type:issue`)[^docs-search].
  An issue type named `Issue` or `PR` would be ambiguous; do not create one.

[^docs-filter-issues]: Filtering and searching issues and pull requests, GitHub Docs.
[^docs-search]: Searching issues and pull requests, GitHub Docs.
[^docs-filter-proj]: Filtering projects, GitHub Docs.
[^docs-progress]: Parent issue and sub-issue progress fields, GitHub Docs.
[^docs-fields-use]: Adding and managing issue fields, GitHub Docs.
[^docs-iter]: About iteration fields, GitHub Docs.
[^cl-2025-04-09]: Evolving GitHub Issues and Projects, 2025-04-09.
[^cl-2025-08-21]: Dependencies on issues, 2025-08-21.
[^cl-2026-03-05]: Hierarchy view improvements, 2026-03-05.
[^cl-2026-07-16]: Advanced search for Projects GA, 2026-07-16.
[^blog-eng]: Introducing sub-issues, GitHub Blog, 2025-04-11.
