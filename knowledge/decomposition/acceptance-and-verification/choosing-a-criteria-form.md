---
type: Comparison
title: Choosing a criteria form
description: Rule list, Gherkin scenario, EARS line or example table; which form of acceptance criterion fits which kind of work item.
tags: [acceptance-criteria, comparison]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: gherkin-ref, title: "Gherkin reference (Cucumber docs)", resource: "https://cucumber.io/docs/gherkin/reference/", url: "https://cucumber.io/docs/gherkin/reference/", accessed: 2026-11-02 }
  - { id: mavin-ears, title: "EARS (Alistair Mavin's official page)", resource: "https://alistairmavin.com/ears/", url: "https://alistairmavin.com/ears/", accessed: 2026-11-02 }
  - { id: wynne-em, title: "Matt Wynne, Introducing Example Mapping", resource: "https://cucumber.io/blog/bdd/example-mapping-introduction/", url: "https://cucumber.io/blog/bdd/example-mapping-introduction/", accessed: 2026-11-02 }
  - { id: wake-invest, title: "Bill Wake, INVEST in Good Stories, and SMART Tasks (2003)", resource: "https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/", url: "https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/", accessed: 2026-11-02 }
---

# The forms

| Form | Shape | Best for | Weak at |
| --- | --- | --- | --- |
| Rule list | `- [ ] <one checkable statement>` | small stories, constraints, docs/config work | hides the trigger; drifts into vague prose |
| Gherkin scenario | Given / When / Then | behaviour with a trigger and visible outcome[^gherkin-ref] | constraints with no event; verbose |
| EARS line | When / While / If-then ... shall ...[^mavin-ears] | one-line behaviour and error cases | no concrete values |
| Example table | rule plus rows of inputs and outputs | business rules with values | prose context |

All four are ways to write the "Testable" in INVEST: a story is testable when you
understand it well enough to write a test for it.[^wake-invest]

# A simple choice rule (draft)

1. Default to a **rule list**: one line per criterion, each line checkable.
2. If a line needs "when X happens", write it as an **EARS** event line, or a short
   **Gherkin** scenario if it will be an automated acceptance test.
3. If a rule has several value cases, add an **example table** under it.
4. Always include at least one error or rejection case (EARS **If/Then**, or a
   scenario whose `When` is bad input).

These are compatible: example mapping's blue cards are rule-list lines and its green
cards are examples or scenarios.[^wynne-em]

# Caveats

- No study found here compares these forms for agent-built work. The choice rule above
  is a draft for the kit, not established practice.
- The first sweep said "the newest skills default to Gherkin". That is a survey of a few
  third-party skills, not a measured trend; treat as anecdotal.

# Related

- [Gherkin and Given/When/Then](gherkin-given-when-then.md)
- [EARS notation](ears-notation.md)
- [Specification by Example](specification-by-example.md)
- [Example mapping](example-mapping.md)
- [SMART for acceptance criteria](smart-for-acceptance-criteria.md)
