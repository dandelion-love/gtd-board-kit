---
type: Reference
title: GitHub issue fields
description: Typed, organization-level metadata on issues (single-select, text, number, date, multi-select), GA on 2026-07-02, up to 25 per organization, with REST, GraphQL and field.<name> search.
tags: [github, issue-fields, custom-fields, epic-story-task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - {id: cl-2026-03-12, title: "Issue fields: Structured issue metadata is in public preview, changelog 2026-03-12", resource: "https://github.blog/changelog/", changelog_entry: "2026-03-12-issue-fields-structured-issue-metadata-is-in-public-preview", accessed: 2026-11-02}
  - {id: cl-2026-05-21, title: "Issue fields are now in public preview for all organizations, changelog 2026-05-21", resource: "https://github.blog/changelog/", changelog_entry: "2026-05-21-issue-fields-are-now-in-public-preview-for-all-organizations", accessed: 2026-11-02}
  - {id: cl-2026-07-02, title: "Issue fields are now generally available, changelog 2026-07-02", resource: "https://github.blog/changelog/", changelog_entry: "2026-07-02-issue-fields-are-now-generally-available", accessed: 2026-11-02}
  - {id: cl-2026-07-23, title: "Multi-select fields for Projects and Issues in public preview, changelog 2026-07-23", resource: "https://github.blog/changelog/", changelog_entry: "2026-07-23-multi-select-fields-for-projects-and-issues-in-public-preview", accessed: 2026-11-02}
  - {id: cl-2026-08-07, title: "Relates to relationship in public preview and multi-select fields GA, changelog 2026-08-07", resource: "https://github.blog/changelog/", changelog_entry: "2026-08-07-connecting-issues-and-multi-select-field-support", accessed: 2026-11-02}
  - {id: docs-org, title: "Managing issue fields in your organization (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-fields-in-your-organization", accessed: 2026-11-02}
  - {id: docs-use, title: "Adding and managing issue fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-and-managing-issue-fields", accessed: 2026-11-02}
  - {id: docs-proj, title: "About issue fields in projects (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-issue-fields", accessed: 2026-11-02}
  - {id: docs-rest-fields, title: "REST API endpoints for issue fields (GitHub Docs)", resource: "https://docs.github.com/en/rest/orgs/issue-fields", accessed: 2026-11-02}
  - {id: docs-rest-values, title: "REST API endpoints for issue field values (GitHub Docs)", resource: "https://docs.github.com/en/rest/issues/issue-field-values", accessed: 2026-11-02}
  - {id: docs-rest-issues, title: "REST API endpoints for issues (GitHub Docs)", resource: "https://docs.github.com/en/rest/issues/issues", accessed: 2026-11-02}
---

# What it is

Issue fields are typed values stored **on the issue itself**, defined once per
organization. Unlike Project custom fields, they travel with the issue to every project
and to repository issue lists[^docs-proj]. They replace label hacks like `priority/p0`[^cl-2026-03-12].

# Timeline (the "GA July 2026" claim is correct)

| Date | Event |
| --- | --- |
| 2026-03-12 | Public preview for select organizations; 4 types; up to 25 per org[^cl-2026-03-12] |
| 2026-05-21 | Public preview for all organizations; REST can set values on issue create[^cl-2026-05-21] |
| 2026-07-02 | **Generally available** on Free, Team, Enterprise Cloud; GHES 3.23 to follow[^cl-2026-07-02] |
| 2026-07-23 | Multi-select type in public preview (issue fields and project fields)[^cl-2026-07-23] |
| 2026-08-07 | Multi-select **GA**[^cl-2026-08-07] |

# Types and limits (docs, read 2026-11-02)

| Item | Value | Source |
| --- | --- | --- |
| Types | single-select, text, number, date; multi-select via API and changelog | [^docs-org][^docs-rest-fields][^cl-2026-08-07] |
| Fields per organization | up to 25 | [^docs-org] |
| Options per single-select | 100 | [^docs-org] |
| Pinned fields per issue type | 10 | [^docs-org] |
| Default fields | Priority (Urgent/High/Medium/Low), Effort (High/Medium/Low), Start date, Target date | [^docs-org] |
| Scope | organization only; apply to all repos in the org | [^docs-org] |
| Visibility | "Organization only" (default) or "Public" | [^docs-org] |
| Who defines | organization owners | [^docs-org] |
| Who sets values | triage or higher in UI; REST says push access | [^docs-use][^docs-rest-values] |
| Pull requests | not supported | [^docs-use] |
| Deleting a field | permanently removes every value | [^docs-org] |

# Pinning, not requiring

- An admin pins fields to an issue type, so they show when that type is chosen[^docs-org].
- No doc offers a **required** field. Unset, unpinned fields are hidden[^docs-org].
- Fields "cannot currently be pre-filled via URL query parameters or set through issue
  templates"[^docs-use]. An issue form cannot fill them.

# APIs

- Definitions (org admin): `GET/POST /orgs/{org}/issue-fields`, `PATCH/DELETE
  /orgs/{org}/issue-fields/{id}`; `data_type` is `text`, `date`, `single_select`,
  `multi_select` or `number`. Updating `options` without option `id`s may delete and
  recreate options[^docs-rest-fields].
- Values: `GET/POST/PUT /repos/{owner}/{repo}/issues/{n}/issue-field-values`, `DELETE
  .../issue-field-values/{field_id}`. Body `{"issue_field_values":[{"field_id":..,"value":..}]}`.
  `PUT` replaces all; `POST []` clears all[^docs-rest-values].
- Create issue accepts `issue_field_values` too[^docs-rest-issues].
- GraphQL: `createIssueField`, `updateIssueField`, `setIssueFieldValue`; Actions `issues`
  event fires `field_added` / `field_removed`[^docs-use].

# Search and Projects

- Search: `field.priority:high`, `field."target date":>=2026-03-01`, `field.priority:high,medium`[^docs-use].
- Projects: added manually as a column; editable in table view; group, filter, sort and
  chart; count toward the 50-field project limit[^docs-proj].
- Issues from another organization, PRs and drafts show empty cells[^docs-proj].

# Caveats

- The docs field-type list (4 types) lags the API and changelog (5, with multi-select).
- UI says triage can set values; REST says push access. Test with the agent's token.
- `POST` with an empty array clears every value. An agent must never send `[]` by mistake.
- Org-only: a personal-account repo cannot use issue fields.

[^cl-2026-03-12]: Issue fields public preview, 2026-03-12.
[^cl-2026-05-21]: Issue fields preview for all orgs, 2026-05-21.
[^cl-2026-07-02]: Issue fields GA, 2026-07-02.
[^cl-2026-07-23]: Multi-select preview, 2026-07-23.
[^cl-2026-08-07]: Relates to preview, multi-select GA, 2026-08-07.
[^docs-org]: Managing issue fields in your organization, GitHub Docs.
[^docs-use]: Adding and managing issue fields, GitHub Docs.
[^docs-proj]: About issue fields in projects, GitHub Docs.
[^docs-rest-fields]: REST API endpoints for issue fields, GitHub Docs.
[^docs-rest-values]: REST API endpoints for issue field values, GitHub Docs.
[^docs-rest-issues]: REST API endpoints for issues, GitHub Docs.
