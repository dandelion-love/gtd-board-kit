---
type: Concept
title: Gherkin and Given/When/Then
description: Given/When/Then is a scenario template from BDD for writing executable acceptance criteria; Gherkin is Cucumber's formal grammar for it.
tags: [acceptance-criteria, bdd, gherkin, testing]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: north-bdd, title: "Introducing BDD (Dan North)", resource: "https://dannorth.net/blog/introducing-bdd/", url: "https://dannorth.net/blog/introducing-bdd/", accessed: 2026-11-02 }
  - { id: cucumber-history, title: "History of BDD (Cucumber docs)", resource: "https://cucumber.io/docs/bdd/history", url: "https://cucumber.io/docs/bdd/history", accessed: 2026-11-02 }
  - { id: gherkin-ref, title: "Gherkin reference (Cucumber docs)", resource: "https://cucumber.io/docs/gherkin/reference/", url: "https://cucumber.io/docs/gherkin/reference/", accessed: 2026-11-02 }
  - { id: better-gherkin, title: "Writing better Gherkin (Cucumber docs)", resource: "https://cucumber.io/docs/bdd/better-gherkin/", url: "https://cucumber.io/docs/bdd/better-gherkin/", accessed: 2026-11-02 }
---

# What it is

A scenario names a starting state, one event, and the outcomes to check:

```gherkin
Given some initial context (the givens),
When an event occurs,
Then ensure some outcomes.
```

Dan North and Chris Matts worked out this template while developing BDD. North's
article first ran in *Better Software* in March 2006; its heading is "Acceptance
criteria should be executable".[^north-bdd] He did not invent the "As a / I want / so
that" story form; it was already in use where he worked.[^north-bdd] Cucumber's history
page credits Eric Evans' ubiquitous language and the Connextra story template as
influences.[^cucumber-history]

Gherkin is Cucumber's formal grammar for these scenarios.

# Rules from the primary docs

| Rule | Source |
| --- | --- |
| `Given` puts the system in a known state before any interaction | [^gherkin-ref] |
| `When` is one event or action | [^gherkin-ref] |
| `Then` checks an outcome visible to the user or an external system, not a database row | [^gherkin-ref] |
| `Rule` (Gherkin 6+) groups the scenarios that illustrate one business rule | [^gherkin-ref] |
| `Scenario Outline` + `Examples` runs one template per table row | [^gherkin-ref] |
| 3 to 5 steps per scenario is the recommendation | [^gherkin-ref] |
| Write declaratively (what), not imperatively (clicks and fields); ask "will this wording change if the implementation does?" | [^better-gherkin] |

# When it fits

- Behaviour with a clear trigger and an outcome a user can see.
- Several cases of one rule: use `Rule` plus one scenario each, or an outline with a table.
- Work that will be checked by an automated acceptance test.

# When it does not fit

- Pure constraints with no event ("every page is under 200 KB"): a rule-list line or
  an [EARS](ears-notation.md) ubiquitous requirement reads better.
- Documentation, research or config work with no runtime behaviour.
- Long UI scripts: these are the imperative style the docs warn against.

# Related

- [Choosing a criteria form](choosing-a-criteria-form.md)
- [Example mapping](example-mapping.md) produces the rules and examples that become scenarios.
- [Testable criteria heuristics](testable-criteria-heuristics.md)
