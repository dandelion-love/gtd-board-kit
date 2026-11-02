---
type: Reference
title: GitHub issue types
description: Organization-level issue classification (default Task, Bug, Feature), up to 25 per organization, GA since April 2025, settable by API, filterable with type:.
tags: [github, issue-types, epic-story-task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:00Z }
sources:
  - {id: cl-2025-04-09, title: "Evolving GitHub Issues and Projects (GA), changelog 2025-04-09", resource: "https://github.blog/changelog/", changelog_entry: "2025-04-09-evolving-github-issues-and-projects", accessed: 2026-11-02}
  - {id: cl-2026-06-10, title: "Manage sub-issues, types, and dependencies from GitHub CLI, changelog 2026-06-10", resource: "https://github.blog/changelog/", changelog_entry: "2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli", accessed: 2026-11-02}
  - {id: docs-manage, title: "Managing issue types in an organization (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization", accessed: 2026-11-02}
  - {id: docs-rest-types, title: "REST API endpoints for issue types (GitHub Docs)", resource: "https://docs.github.com/en/rest/orgs/issue-types", accessed: 2026-11-02}
  - {id: docs-rest-issues, title: "REST API endpoints for issues (GitHub Docs)", resource: "https://docs.github.com/en/rest/issues/issues", accessed: 2026-11-02}
  - {id: docs-gql, title: "GraphQL reference: Issues (GitHub Docs)", resource: "https://docs.github.com/en/graphql/reference/issues", accessed: 2026-11-02}
  - {id: docs-proj-type, title: "About the issue type field (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-the-issue-type-field", accessed: 2026-11-02}
  - {id: docs-filter-proj, title: "Filtering projects (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/filtering-projects", accessed: 2026-11-02}
  - {id: docs-filter-issues, title: "Filtering and searching issues and pull requests (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests", accessed: 2026-11-02}
  - {id: docs-forms, title: "Syntax for issue forms (GitHub Docs)", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms", accessed: 2026-11-02}
---

# What it is

An issue type is a single, organization-wide classification on an issue. Each issue has at
most one type. It is the native carrier for "what kind of work item is this": Epic,
Story, Task.

# Timeline

| Date | Event |
| --- | --- |
| 2025-01-12 | Public preview (with sub-issues) |
| 2025-04-09 | **Generally available**; search with `type:` and boolean `OR`[^cl-2025-04-09] |
| 2026-06-10 | `gh` v2.94.0 sets and filters types[^cl-2026-06-10] |

# Limits and defaults (docs, read 2026-11-02)

| Item | Value | Source |
| --- | --- | --- |
| Types per organization | up to 25 | [^docs-manage] |
| Defaults | `task`, `bug`, `feature`; can be edited, disabled or deleted | [^docs-manage] |
| Per type | name, description, color | [^docs-manage] |
| Colors | gray, blue, green, yellow, orange, red, pink, purple | [^docs-rest-types] |
| Disable | hidden, cannot be set; re-enabling restores it on old issues | [^docs-manage] |
| Delete | permanent | [^docs-manage] |
| Who manages | organization owners | [^docs-manage] |
| Scope | organization only; types "only work in organizations that have configured them" | [^cl-2026-06-10] |

There is no Epic or Story type by default. A kit must create them.

# APIs

- REST, org admin: `GET/POST /orgs/{org}/issue-types`, `PUT/DELETE
  /orgs/{org}/issue-types/{issue_type_id}`; body `name`, `is_enabled`, `description`,
  `color`. Fine-grained permission "Issue Types" (org)[^docs-rest-types].
- REST, per issue: `type` on create/update is the **type name**. Without push access it is
  "silently dropped"[^docs-rest-issues].
- GraphQL: `createIssueType`, `updateIssueIssueType`, object `IssueType`[^docs-gql].
- Issue forms and Markdown templates can preset `type:`[^docs-forms].

# In Projects and search

- Projects: a hidden *Type* field you turn on in table view[^docs-proj-type]; filter with
  `type:"bug"`[^docs-filter-proj].
- Issues search: `type:"Bug"`, combinable as `type:Bug OR type:Feature`[^docs-filter-issues][^cl-2025-04-09].

# What it does not do

- It does not constrain the tree: a `Task` can parent an `Epic`. Allowed parent/child
  pairs must be checked by the kit.
- It does not require fields per type. Issue fields can be *pinned* to a type, not
  required (see [issue-fields.md](issue-fields.md)).

# Caveats

- Personal-account repositories: no doc found that offers types outside organizations.
  The CLI changelog implies organization only. A kit for personal repos must fall back to
  labels.
- The silent drop on missing push access means a write can "succeed" without setting the
  type. Read back after writing.

[^cl-2025-04-09]: Evolving GitHub Issues and Projects, 2025-04-09.
[^cl-2026-06-10]: GitHub CLI sub-issues, types, dependencies, 2026-06-10.
[^docs-manage]: Managing issue types in an organization, GitHub Docs.
[^docs-rest-types]: REST API endpoints for issue types, GitHub Docs.
[^docs-rest-issues]: REST API endpoints for issues, GitHub Docs.
[^docs-gql]: GraphQL reference: Issues, GitHub Docs.
[^docs-proj-type]: About the issue type field, GitHub Docs.
[^docs-filter-proj]: Filtering projects, GitHub Docs.
[^docs-filter-issues]: Filtering and searching issues and pull requests, GitHub Docs.
[^docs-forms]: Syntax for issue forms, GitHub Docs.
