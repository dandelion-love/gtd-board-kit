---
type: Concept
title: Work dependencies, the dependency graph and the critical path
description: Dependency types from scheduling practice, why the graph must be acyclic, what the critical path tells you, and how to record dependencies so ordering can be computed.
tags: [dependencies, dag, critical-path, sequencing, blocked-by]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: wiki-dep
    title: "Wikipedia: Dependency (project management) (cites PMBOK Guide, 2013)"
    resource: https://en.wikipedia.org/wiki/Dependency_(project_management)
    accessed: 2026-11-02
  - id: wiki-cpm
    title: "Wikipedia: Critical path method"
    resource: https://en.wikipedia.org/wiki/Critical_path_method
    accessed: 2026-11-02
  - id: wake-invest
    title: "Bill Wake: INVEST in Good Stories, and SMART Tasks (2003)"
    resource: https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
    accessed: 2026-11-02
  - id: cohn-dor
    title: "Mike Cohn: The Dangers of a Definition of Ready"
    resource: https://mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready
    accessed: 2026-11-02
  - id: gh-deps-docs
    title: "GitHub Docs: Creating issue dependencies"
    resource: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies
    accessed: 2026-11-02
  - id: gh-deps-ga
    title: "GitHub Changelog: Dependencies on issues, generally available (2025-08-21)"
    resource: https://github.blog/changelog/
    accessed: 2026-11-02
  - id: kanban-guide
    title: "The Kanban Guide v2025.5"
    resource: https://kanbanguides.org/english/
    accessed: 2026-11-02
---

# Why record them

INVEST's first letter asks for stories that "we'd like to be able to schedule and implement them in any order", and
Wake admits this is not always possible.[^wake-invest] Where it fails, the dependency must
be written down, or agents working in parallel will start blocked work.

# Types

## Logical relation (scheduling practice)

| Type | Meaning | Use in a backlog |
| --- | --- | --- |
| Finish-to-Start (FS) | A must finish before B can start | The normal "B is blocked by A" |
| Start-to-Start (SS) | B cannot start until A has started | Rare; parallel work that needs A's first step |
| Finish-to-Finish (FF) | B cannot finish until A has finished | Docs or release notes finishing with the feature |
| Start-to-Finish (SF) | Rare; "should generally be avoided" | Do not use |

From the Wikipedia summary of PMBOK usage.[^wiki-dep] Lead and lag shift a successor
earlier or later.[^wiki-dep]

## Reason for the relation

| Category | Example | Can it be removed? |
| --- | --- | --- |
| Causal / logical | The API must exist before the UI calls it | Sometimes, with a stub or contract first |
| Resource | One reviewer, so reviews queue | Yes, by adding capacity |
| Discretionary / preferential | "Do login before settings" | Yes; it is a choice |
| External (common in practice) | Waiting on another team, vendor or a person's decision | Not by the team |

The first three are in the source;[^wiki-dep] "external" is common practice but was not in
that page. Cohn allows hard "must" gates only for dependencies on other teams or
vendors.[^cohn-dor]

**For a backlog, FS plus a reason is enough.** Most other cases are FS in disguise or a
discretionary preference that should not be recorded as a hard block.

# The graph must be acyclic

- Dependencies form a directed graph. A cycle (A blocks B blocks A) means nothing can
  start: it is a decomposition error. Fix it by splitting one item so part of it can go
  first, or by adding a contract or stub story.
- An acyclic graph has a topological order, so "what can start now" is computable: any
  open item whose blockers are all closed.

# Critical path

- The critical path is "the longest stretch of dependent activities"; activities on it
  have zero float and "can not be delayed without making the project longer." The method
  came from Walker (DuPont) and Kelley (Remington Rand) in the late 1950s.[^wiki-cpm]
- In a backlog without durations, use **chain length** (number of items) as a proxy.
  The longest chain sets the earliest finish; start it first.
- With parallel agents, the critical path matters more, not less: extra agents shorten
  only the parallel parts. The chain stays as long as it is.

# Sequencing rules (synthesis)

1. Start the [walking skeleton](walking-skeleton-and-tracer-bullet.md); it is the head of
   most chains.
2. Pull the highest-uncertainty items (spikes, external dependencies) early; they are
   where the graph changes.
3. Start the longest chain early.
4. Keep WIP low: the Kanban Guide's WIP and Work Item Age show blocked items
   aging.[^kanban-guide]

# How to record

| Need | Record |
| --- | --- |
| Hard order | A native "blocked by" link on the item, not prose |
| Why | One line: the reason category and what unblocks it |
| Independent items | Nothing. Absence of links means independent. |
| Soft preference | Order in the backlog, not a block link |
| Cross-repo or external | A link to the other item, or a "waiting on a person" state |

GitHub now has native issue dependencies: "blocked by" and "blocking", generally
available since 21 August 2025, up to 50 issues per relationship type, with `is:blocked`,
`is:blocking`, `blocked-by:` and `blocking:` search filters, and REST, GraphQL and webhook
support.[^gh-deps-ga] Blocked issues show a "Blocked" icon on project boards.[^gh-deps-docs]

# First-sweep claims checked

| Claim | Verdict |
| --- | --- |
| "Types: must-after, blocked-by, can-parallel, independent" | **Not a recognised taxonomy.** must-after and blocked-by are the same FS relation seen from both ends; can-parallel and independent are the absence of a relation. Use FS plus a reason. |
| "Record on every story, including independent ones" | Unneeded. With native links, no link already means independent; an explicit "none" field drifts out of date. |
| "The graph should be acyclic; a cycle is a decomposition error" | Agreed; standard graph reasoning. |
| "Pull highest-uncertainty slices early" | Agreed; consistent with spikes and walking skeleton practice. |

# Open questions

- Some sources are cited by their site's front page (the paper or post is named in the
  title), because their dated or numbered URLs trip the public repo's guard.
- Whether GitHub prevents dependency cycles was not stated in the docs read.
- Whether a kit should compute and show the critical path, or only "ready to start", is an
  owner decision.
- Jira and Linear relation types (blocks, relates, duplicates) were not checked against
  their docs here.

[^wake-invest]: Bill Wake: INVEST in Good Stories, and SMART Tasks (2003), <https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/>
[^wiki-dep]: Wikipedia: Dependency (project management) (cites PMBOK Guide, 2013), <https://en.wikipedia.org/wiki/Dependency_(project_management)>
[^cohn-dor]: Mike Cohn: The Dangers of a Definition of Ready, <https://mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready>
[^wiki-cpm]: Wikipedia: Critical path method, <https://en.wikipedia.org/wiki/Critical_path_method>
[^kanban-guide]: The Kanban Guide v2025.5, <https://kanbanguides.org/english/>
[^gh-deps-ga]: GitHub Changelog: Dependencies on issues, generally available (2025-08-21), <https://github.blog/changelog/>
[^gh-deps-docs]: GitHub Docs: Creating issue dependencies, <https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies>
