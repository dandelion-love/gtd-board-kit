# GitHub primitives

* [GitHub issue dependencies and relationships](issue-dependencies.md) - Native blocked-by and blocking links between issues, GA on 2025-08-21 with up to 50 per relationship type, plus the "Relates to" link GA on 2026-09-25
* [GitHub issue fields](issue-fields.md) - Typed, organization-level metadata on issues (single-select, text, number, date, multi-select), GA on 2026-07-02, up to 25 per organization, with REST, GraphQL and field.<name> search
* [Issue forms, templates and PR linking on GitHub](issue-forms-and-templates.md) - How YAML issue forms, Markdown templates, PR templates, closing keywords and the Development sidebar can shape Epic, Story and Task bodies, and where they stop enforcing
* [GitHub issue types](issue-types.md) - Organization-level issue classification (default Task, Bug, Feature), up to 25 per organization, GA since April 2025, settable by API, filterable with type:
* [Labels vs issue types vs issue fields vs project fields](labels-vs-types-vs-fields.md) - Which GitHub carrier to use for which kind of work-item metadata, by cardinality, scope, typing, portability and API cost, as of November 2026
* [Mapping an Epic/Story/Task model onto GitHub primitives](mapping-epic-story-task-onto-github.md) - Which native GitHub primitive carries each part of an Epic/Story/Task model as of November 2026, what GitHub enforces by itself, and what a board kit or agent must enforce
* [GitHub Projects (v2) for an Epic/Story/Task board](projects-v2.md) - What Projects offers a hierarchy board as of November 2026 - field types, iteration, parent and sub-issue progress fields, hierarchy view, built-in workflows, limits, and the GraphQL and REST APIs
* [GitHub search and filter syntax for hierarchy, types, fields and dependencies](search-and-filter-syntax.md) - The issue-search and Projects-filter qualifiers an agent can use to find Epics, Stories, Tasks, blocked work and field values, with which ones the official docs actually confirm
* [GitHub sub-issues](sub-issues.md) - GitHub's native parent/child link between issues, GA since April 2025, with 100 children per parent and eight levels of nesting
