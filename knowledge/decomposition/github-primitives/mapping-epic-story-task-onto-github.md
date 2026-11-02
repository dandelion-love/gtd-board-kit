---
type: Pattern
title: Mapping an Epic/Story/Task model onto GitHub primitives
description: Which native GitHub primitive carries each part of an Epic/Story/Task model as of November 2026, what GitHub enforces by itself, and what a board kit or agent must enforce.
tags: [github, epic-story-task, synthesis, mapping, enforcement]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - {id: docs-sub-add, title: "Adding sub-issues (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues", accessed: 2026-11-02}
  - {id: cl-2025-04-09, title: "Evolving GitHub Issues and Projects (GA), changelog 2025-04-09", resource: "https://github.blog/changelog/", changelog_entry: "2025-04-09-evolving-github-issues-and-projects", accessed: 2026-11-02}
  - {id: docs-types, title: "Managing issue types in an organization (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization", accessed: 2026-11-02}
  - {id: cl-2026-07-02, title: "Issue fields are now generally available, changelog 2026-07-02", resource: "https://github.blog/changelog/", changelog_entry: "2026-07-02-issue-fields-are-now-generally-available", accessed: 2026-11-02}
  - {id: docs-fields, title: "Managing issue fields in your organization (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-fields-in-your-organization", accessed: 2026-11-02}
  - {id: docs-fields-use, title: "Adding and managing issue fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-and-managing-issue-fields", accessed: 2026-11-02}
  - {id: cl-2025-08-21, title: "Dependencies on issues, changelog 2025-08-21", resource: "https://github.blog/changelog/", changelog_entry: "2025-08-21-dependencies-on-issues", accessed: 2026-11-02}
  - {id: cl-2026-03-19, title: "Hierarchy view in GitHub Projects is now generally available, changelog 2026-03-19", resource: "https://github.blog/changelog/", changelog_entry: "2026-03-19-hierarchy-view-in-github-projects-is-now-generally-available", accessed: 2026-11-02}
  - {id: docs-about-proj, title: "About Projects (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects", accessed: 2026-11-02}
  - {id: docs-iter, title: "About iteration fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields", accessed: 2026-11-02}
  - {id: docs-builtin, title: "Using the built-in automations (GitHub Docs)", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations", accessed: 2026-11-02}
  - {id: docs-form-schema, title: "Syntax for GitHub's form schema (GitHub Docs)", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema", accessed: 2026-11-02}
  - {id: docs-link-pr, title: "Linking a pull request to an issue (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue", accessed: 2026-11-02}
  - {id: docs-rest-issues, title: "REST API endpoints for issues (GitHub Docs)", resource: "https://docs.github.com/en/rest/issues/issues", accessed: 2026-11-02}
  - {id: cl-2026-10-28, title: "Issue artifacts are now in public preview, changelog 2026-10-28", resource: "https://github.blog/changelog/", changelog_entry: "2026-10-28-issue-artifacts-are-now-in-public-preview", accessed: 2026-11-02}
---

# Summary

GitHub now has a native part for every structural piece of Epic/Story/Task: **types**
say what a node is, **sub-issues** give the tree, **dependencies** give order, **issue
fields** hold typed attributes, **Projects** hold board state and sprints. What GitHub
does **not** do is *validate* the model: it never checks that a Story sits under an Epic,
that acceptance criteria exist, that the dependency graph has no cycle, or that a parent
closes only when its children are done. That is the kit's job.

Details per primitive: [sub-issues](sub-issues.md), [issue types](issue-types.md),
[issue fields](issue-fields.md), [dependencies](issue-dependencies.md),
[Projects](projects-v2.md), [forms and templates](issue-forms-and-templates.md),
[labels vs types vs fields](labels-vs-types-vs-fields.md),
[search syntax](search-and-filter-syntax.md).

# Mapping table

| Concept | Native carrier | Enforceable natively? | What the kit or agent must enforce |
| --- | --- | --- | --- |
| Level (Epic / Story / Task) | Issue type, created by the kit (defaults are Task, Bug, Feature)[^docs-types] | Partly: one type per issue; only listed types can be set | Create Epic and Story types; read back after write (type is silently dropped without push access)[^docs-rest-issues]; fall back to a label in personal-account repos |
| Epic contains Story contains Task | Sub-issues, 100 children, 8 levels[^docs-sub-add] | Partly: one parent, limits | Allowed parent/child pairs (no Task over Story, no Story without Epic if required); depth used = 3 |
| Task as a checklist inside a Story (alternative) | Task list in the Story body | No | Parse the checklist; decide when a Task is promoted to a sub-issue |
| Ordering / blocked-by | Issue dependencies, 50 per type (2025-08-21)[^cl-2025-08-21] | Partly: links and a Blocked icon | Acyclic graph; "independent" and "can-parallel" have no native edge; do not start blocked work |
| Loose link | "Relates to" (GA 2026-09-25) | Yes, as a link | Nothing beyond use |
| Story body: user story, AC, out of scope | Issue form (YAML) | **Only in public repos, only in the web UI**[^docs-form-schema] | Validate sections on every issue, including API-created ones |
| Definition of Done | PR template + review gates | No (template is text) | Check the checklist and evidence before review is requested |
| Size / effort / priority / target date | Issue fields (GA 2026-07-02; 25 per org)[^cl-2026-07-02][^docs-fields] | Typed, yes; required, **no** | Require values per type; forms cannot fill them[^docs-fields-use], so set by API after create |
| Status (Backlog, Ready, In progress, Review, Done) | Project single-select field | Partly: built-in workflows set Done on close/merge[^docs-builtin] | All other transitions; Ready = AC present + not blocked |
| Sprint / Bolt | Project iteration field[^docs-iter] | Yes, as a field | Keep a Story within one iteration; carry-over rules |
| Epic progress | Sub-issue progress field and hierarchy view (GA 2026-03-19)[^cl-2026-03-19] | Yes, display only | Multi-level rollup if needed (not documented); weighting by size |
| Epic done | Closing the Epic issue | No | Close only when all children are closed and epic-level AC are met |
| Story done via PR | Closing keyword or Development sidebar[^docs-link-pr] | Yes, on merge to default branch | Close the issue when the PR targets another branch; never auto-close the parent |
| One Story per branch and PR | Linked PR | No | Branch naming, one-to-one check |
| Plan, research, design notes | Issue body or issue artifacts (preview 2026-10-28)[^cl-2026-10-28] | No | Choose one place; keep it current |
| Cross-cutting tags, PR flags | Labels | Yes, as free text | Sync labels across repos; prevent case drift |

# Limits a kit must design around

| Limit | Value | Source date |
| --- | --- | --- |
| Sub-issues per parent | 100 | docs, read 2026-11-02[^docs-sub-add] |
| Sub-issue depth | 8 | docs, read 2026-11-02[^docs-sub-add] |
| Issue types per org | 25 | docs, read 2026-11-02[^docs-types] |
| Issue fields per org | 25 | docs, read 2026-11-02[^docs-fields] |
| Options per single-select issue field | 100 | docs, read 2026-11-02[^docs-fields] |
| Pinned fields per type | 10 | docs, read 2026-11-02[^docs-fields] |
| Dependencies per relationship type | 50 | changelog 2025-08-21[^cl-2025-08-21] |
| Project items | 50,000 | changelog 2025-04-09[^cl-2025-04-09] |
| Project fields | 50 (issue fields count) | docs, read 2026-11-02[^docs-about-proj] |
| Issues linked to a PR by hand | 10 | docs, read 2026-11-02[^docs-link-pr] |
| Search nesting | 5 levels | docs, read 2026-11-02 |

# Design consequences

1. **Organization repos get the full native model; personal repos do not.** Types and issue
   fields are organization-only. A kit needs a label fallback (`kind:epic`, `kind:story`).
2. **Validation must run on write, not on form submit.** Agents use the API, where no form
   applies, and private repos ignore `required`.
3. **Ids, not numbers.** Sub-issue and dependency REST calls take the issue's numeric `id`.
4. **Read back every write.** Type, labels and milestone are silently dropped without
   push access.
5. **Close parents explicitly.** No native rule closes or blocks closing a parent.

# Caveats

- Cross-owner sub-issues: changelog (2025-09-11) and REST docs disagree; see
  [sub-issues.md](sub-issues.md).
- Several search qualifiers are confirmed only by changelog or blog, not docs; see
  [search-and-filter-syntax.md](search-and-filter-syntax.md).
- Docs pages are undated living pages; limits marked "docs, read 2026-11-02" may change.

[^docs-sub-add]: Adding sub-issues, GitHub Docs.
[^cl-2025-04-09]: Evolving GitHub Issues and Projects, 2025-04-09.
[^docs-types]: Managing issue types, GitHub Docs.
[^cl-2026-07-02]: Issue fields GA, 2026-07-02.
[^docs-fields]: Managing issue fields, GitHub Docs.
[^docs-fields-use]: Adding and managing issue fields, GitHub Docs.
[^cl-2025-08-21]: Dependencies on issues, 2025-08-21.
[^cl-2026-03-19]: Hierarchy view GA, 2026-03-19.
[^docs-about-proj]: About Projects, GitHub Docs.
[^docs-iter]: About iteration fields, GitHub Docs.
[^docs-builtin]: Using the built-in automations, GitHub Docs.
[^docs-form-schema]: Syntax for GitHub's form schema, GitHub Docs.
[^docs-link-pr]: Linking a pull request to an issue, GitHub Docs.
[^docs-rest-issues]: REST API endpoints for issues, GitHub Docs.
[^cl-2026-10-28]: Issue artifacts preview, 2026-10-28.
