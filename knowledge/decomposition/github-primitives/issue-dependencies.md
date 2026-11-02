---
type: Reference
title: GitHub issue dependencies and relationships
description: Native blocked-by and blocking links between issues, GA on 2025-08-21 with up to 50 per relationship type, plus the "Relates to" link GA on 2026-09-25.
tags: [github, dependencies, blocked-by, relationships, epic-story-task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:05:00Z }
sources:
  - {id: cl-2025-08-21, title: "Dependencies on issues, changelog 2025-08-21", resource: "https://github.blog/changelog/", changelog_entry: "2025-08-21-dependencies-on-issues", accessed: 2026-11-02}
  - {id: cl-2026-06-10, title: "Manage sub-issues, types, and dependencies from GitHub CLI, changelog 2026-06-10", resource: "https://github.blog/changelog/", changelog_entry: "2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli", accessed: 2026-11-02}
  - {id: cl-2026-08-07, title: "Relates to relationship in public preview and multi-select GA, changelog 2026-08-07", resource: "https://github.blog/changelog/", changelog_entry: "2026-08-07-connecting-issues-and-multi-select-field-support", accessed: 2026-11-02}
  - {id: cl-2026-09-25, title: "Private saved views for repository issues and Relates to GA, changelog 2026-09-25", resource: "https://github.blog/changelog/", changelog_entry: "2026-09-25-personal-saved-views-for-repository-issues-and-more", accessed: 2026-11-02}
  - {id: docs-dep, title: "Creating issue dependencies (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies", accessed: 2026-11-02}
  - {id: docs-rest-dep, title: "REST API endpoints for issue dependencies (GitHub Docs)", resource: "https://docs.github.com/en/rest/issues/issue-dependencies", accessed: 2026-11-02}
  - {id: docs-gql, title: "GraphQL reference: Issues (GitHub Docs)", resource: "https://docs.github.com/en/graphql/reference/issues", accessed: 2026-11-02}
---

# What it is

A dependency says one issue is **blocked by** another. Its inverse is **blocking**. It is
the native carrier for ordering between Stories and Tasks. It is separate from
[sub-issues](sub-issues.md): containment is not order.

# Timeline

| Date | Event |
| --- | --- |
| 2025-08-21 | **Generally available**: REST, GraphQL, webhooks, search qualifiers[^cl-2025-08-21] |
| 2026-06-10 | `gh` v2.94.0: `--blocked-by`, `--blocking`, `--add-*`, `--remove-*`[^cl-2026-06-10] |
| 2026-08-07 | "Relates to" link in public preview[^cl-2026-08-07] |
| 2026-09-25 | "Relates to" **GA** in REST, GraphQL, webhooks, timeline, issues and projects search[^cl-2026-09-25] |

# Limits

| Item | Value | Source |
| --- | --- | --- |
| Links per relationship type per issue | up to 50 | changelog 2025-08-21[^cl-2025-08-21] |
| Who can add | triage or higher | [^docs-dep] |
| Plans | Free, Pro, Team, Enterprise Cloud | [^docs-dep] |
| List page size | max 100 | [^docs-rest-dep] |

# APIs

REST under `/repos/{owner}/{repo}/issues/{issue_number}/dependencies`[^docs-rest-dep]:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/blocked_by` | issues blocking this one |
| POST | `/blocked_by` | add; body `{"issue_id": <id>}` (numeric id, not number) |
| DELETE | `/blocked_by/{issue_id}` | remove |
| GET | `/blocking` | issues this one blocks |

- There is no POST on `/blocking`. To say "A blocks B", write on B.
- GraphQL: `addBlockedBy`, `removeBlockedBy`, `Issue.blockedBy`[^docs-gql].
- CLI: `gh issue view --json blockedBy,blocking`[^docs-dep].

# How it shows

- Sidebar "Relationships": "Mark as blocked by" / "Mark as blocking"[^cl-2025-08-21].
- A "Blocked" icon on project boards and the repository issue list[^docs-dep].
- Search: `is:blocked`, `is:blocking`, `blocked-by:<issue>`, `blocking:<issue>`[^cl-2025-08-21].

# What it does not do

- No doc says GitHub rejects a cycle. A kit must check the graph is acyclic.
- No doc says closing a blocker changes anything on the blocked issue except the icon.
  No auto-transition to Ready.
- It does not stop work starting or a PR merging on a blocked issue.
- There is no typed "can-parallel" or "must-after" edge. Only blocked-by and relates-to.

# Caveats

- The 50-per-type limit is from the 2025 changelog; current docs do not restate it.
- Cross-repository dependencies: the CLI accepts URLs, which suggests cross-repo links,
  but no page states the rule.
- "Relates to" API field names were not found in the pages read.

[^cl-2025-08-21]: Dependencies on issues, 2025-08-21.
[^cl-2026-06-10]: GitHub CLI sub-issues, types, dependencies, 2026-06-10.
[^cl-2026-08-07]: Relates to preview, 2026-08-07.
[^cl-2026-09-25]: Relates to GA, 2026-09-25.
[^docs-dep]: Creating issue dependencies, GitHub Docs.
[^docs-rest-dep]: REST API endpoints for issue dependencies, GitHub Docs.
[^docs-gql]: GraphQL reference: Issues, GitHub Docs.
