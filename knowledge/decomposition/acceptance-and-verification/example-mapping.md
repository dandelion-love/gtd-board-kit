---
type: Practice
title: Example mapping
description: A short card-based conversation that splits a story into rules, examples and open questions before it is built, and tells you when a story is too big or too unclear.
tags: [acceptance-criteria, refinement, bdd]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: wynne-em, title: "Matt Wynne, Introducing Example Mapping (Cucumber blog, 2015-12-08)", resource: "https://cucumber.io/blog/bdd/example-mapping-introduction/", url: "https://cucumber.io/blog/bdd/example-mapping-introduction/", accessed: 2026-11-02 }
---

# What it is

Matt Wynne described it on the Cucumber blog on 8 December 2015.[^wynne-em]

| Card | Holds |
| --- | --- |
| Yellow | the story |
| Blue | a rule (an acceptance criterion or constraint) |
| Green | an example that illustrates a rule |
| Red | a question nobody present can answer |

A well-sized story should map in about 25 minutes, then a thumb vote decides if it is
ready.[^wynne-em]

# The signals (its real value)

| Signal | Meaning |
| --- | --- |
| Many red cards | too uncertain; someone must find answers first |
| Many blue cards | too big; slice it |
| One rule with many green cards | the rule is too complex; split it |
| Cannot map in the time box | too big, too unclear, or the team is still learning |

All from the original post.[^wynne-em] Gherkin is usually written **after** the session,
not during it.[^wynne-em]

# Adapting it for one person and agents

Wynne's version is a group workshop. For a solo owner with agents, a plausible
adaptation (not tested in this research) is:

- The issue body holds the map as text: `## Rules` (each a criterion), examples under each
  rule, and `## Open questions`.
- An open red card means the story is not ready: it waits on a person, not an agent.
- Many rules is the signal to split into more stories.

# Related

- [Specification by Example](specification-by-example.md)
- [Choosing a criteria form](choosing-a-criteria-form.md)
- [Criterion-to-evidence chain](criterion-to-evidence-chain.md)
