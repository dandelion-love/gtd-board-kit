---
type: Reference
title: GitHub sub-issues
description: GitHub's native parent/child link between issues, GA since April 2025, with 100 children per parent and eight levels of nesting.
tags: [github, sub-issues, hierarchy, epic-story-task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:50:00Z }
sources:
  - {id: cl-2025-04-09, title: "Evolving GitHub Issues and Projects (GA), changelog 2025-04-09", resource: "https://github.blog/changelog/", changelog_entry: "2025-04-09-evolving-github-issues-and-projects", accessed: 2026-11-02}
  - {id: cl-2025-01-12, title: "Evolving GitHub Issues (public preview), changelog 2025-01-12", resource: "https://github.blog/changelog/", changelog_entry: "2025-01-12-evolving-github-issues-public-preview", accessed: 2026-11-02}
  - {id: cl-2024-12-12, title: "Close issue as a duplicate, REST API for sub-issues, and more, changelog 2024-12-12", resource: "https://github.blog/changelog/", changelog_entry: "2024-12-12-github-issues-projects-close-issue-as-a-duplicate-rest-api-for-sub-issues-and-more", accessed: 2026-11-02}
  - {id: cl-2025-09-11, title: "A REST API for GitHub Projects, sub-issues improvements, and more, changelog 2025-09-11", resource: "https://github.blog/changelog/", changelog_entry: "2025-09-11-a-rest-api-for-github-projects-sub-issues-improvements-and-more", accessed: 2026-11-02}
  - {id: cl-2026-06-10, title: "Manage sub-issues, types, and dependencies from GitHub CLI, changelog 2026-06-10", resource: "https://github.blog/changelog/", changelog_entry: "2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli", accessed: 2026-11-02}
  - {id: docs-add, title: "Adding sub-issues (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues", accessed: 2026-11-02}
  - {id: docs-browse, title: "Browsing sub-issues (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/browsing-sub-issues", accessed: 2026-11-02}
  - {id: docs-rest, title: "REST API endpoints for sub-issues (GitHub Docs)", resource: "https://docs.github.com/en/rest/issues/sub-issues", accessed: 2026-11-02}
  - {id: docs-gql, title: "GraphQL reference: Issues (GitHub Docs)", resource: "https://docs.github.com/en/graphql/reference/issues", accessed: 2026-11-02}
  - {id: blog-eng, title: "Introducing sub-issues: Enhancing issue management on GitHub (GitHub Blog, 2025-04-11)", resource: "https://github.blog/engineering/architecture-optimization/introducing-sub-issues-enhancing-issue-management-on-github/", accessed: 2026-11-02}
---

# What it is

A sub-issue is an ordinary issue linked to one parent issue. The link forms a tree. It is
the only native **hierarchy** carrier on GitHub, so it is the natural carrier for
Epic > Story > Task.

# Timeline

| Date | Event |
| --- | --- |
| 2024-12-12 | REST API for sub-issues announced (preview)[^cl-2024-12-12] |
| 2025-01-12 | Public preview, with issue types and advanced search[^cl-2025-01-12] |
| 2025-04-09 | **Generally available**, with issue types and advanced search[^cl-2025-04-09] |
| 2025-09-11 | Sub-issues inherit parent's Project and Milestone by default; cross-organization sub-issues; REST endpoint to get the parent[^cl-2025-09-11] |
| 2026-06-10 | `gh` v2.94.0 adds `--parent`, `--set-parent`, `--remove-parent`[^cl-2026-06-10] |

# Limits (docs, read 2026-11-02)

| Limit | Value | Source |
| --- | --- | --- |
| Children per parent | 100 | [^docs-add] |
| Nesting depth | 8 levels | [^docs-add] |
| Parents per issue | 1 (a sub-issue has one parent; adding elsewhere needs `replace_parent`) | [^docs-rest] |
| Who can add | triage permission or higher | [^docs-add] |
| List page size | max 100 per page | [^docs-rest] |

The GA changelog itself states no numeric limit[^cl-2025-04-09]. The 100 and 8 figures come
from the current docs page.

# APIs

REST (all under `/repos/{owner}/{repo}/issues/{issue_number}`)[^docs-rest]:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/parent` | parent of this issue |
| GET | `/sub_issues` | list children |
| POST | `/sub_issues` | add a child; body `sub_issue_id`, optional `replace_parent` |
| DELETE | `/sub_issue` | remove a child |
| PATCH | `/sub_issues/priority` | reorder; `after_id` or `before_id` |

- `sub_issue_id` is the issue's numeric **id**, not its number. Agents get this wrong often.
- Fine-grained permission: Issues read (list) or write (change).
- GraphQL mutations `addSubIssue`, `removeSubIssue`, `reprioritizeSubIssue` exist, and a
  `SubIssuesSummary` object[^docs-gql].
- CLI: `gh issue create --parent`, `gh issue edit --add-sub-issue / --remove-sub-issue /
  --set-parent / --remove-parent`; `gh issue view --json parent,subIssues,subIssuesSummary`[^docs-add][^docs-browse][^cl-2026-06-10].

# Progress rollup

- The parent shows a summary such as "Sub-issues · 1/3 (33%)"[^docs-browse].
- GitHub stores completion in a separate rolled-up table, so a parent's progress updates
  when a child closes, without walking the children[^blog-eng].
- In Projects this appears as the *Sub-issue progress* field; see
  [projects-v2.md](projects-v2.md).

# Cross-repository parents

- The UI lets you add existing issues from other repositories as children[^docs-add].
- The 2025-09-11 changelog says sub-issues support cross-organization issues[^cl-2025-09-11].
- The REST docs say for `POST /sub_issues` that the child "must belong to the same
  repository owner as the parent"[^docs-rest]. See Caveats.

# What it does not do

- It does not type the levels. A Story under a Task is allowed. Depth means nothing on its
  own; use [issue types](issue-types.md) to say what each node is.
- It does not close the parent when all children close, and it does not stop a parent
  closing with open children (no doc says otherwise).
- It is not a dependency. Order between siblings is a display order only; use
  [issue dependencies](issue-dependencies.md) for "must happen first".

# Caveats

- Cross-owner rule conflicts: the 2025-09-11 changelog claims cross-organization support,
  while the REST reference still says same repository owner. Test before relying on it.
- Whether progress rolls up across more than one level (a Task closing moving the Epic's
  bar) is not documented. The engineering post describes a per-parent summary only.
- No doc states what happens to children when a parent is transferred or deleted.

[^cl-2025-04-09]: Evolving GitHub Issues and Projects, 2025-04-09.
[^cl-2025-01-12]: Evolving GitHub Issues (public preview), 2025-01-12.
[^cl-2024-12-12]: REST API for sub-issues, 2024-12-12.
[^cl-2025-09-11]: REST API for Projects, sub-issue improvements, 2025-09-11.
[^cl-2026-06-10]: Sub-issues, types and dependencies from GitHub CLI, 2026-06-10.
[^docs-add]: Adding sub-issues, GitHub Docs.
[^docs-browse]: Browsing sub-issues, GitHub Docs.
[^docs-rest]: REST API endpoints for sub-issues, GitHub Docs.
[^docs-gql]: GraphQL reference: Issues, GitHub Docs.
[^blog-eng]: Introducing sub-issues, GitHub Blog, 2025-04-11.
