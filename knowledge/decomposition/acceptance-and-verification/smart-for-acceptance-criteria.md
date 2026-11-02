---
type: Concept
title: SMART for acceptance criteria
description: SMART began as a test for management objectives and was applied to agile tasks by Bill Wake; for acceptance criteria only the Specific and Measurable letters do real work.
tags: [acceptance-criteria, smart, quality]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: smart-wiki, title: "SMART criteria (Wikipedia), citing Doran 1981, Management Review 70(11):35-36", resource: "https://en.wikipedia.org/wiki/SMART_criteria", url: "https://en.wikipedia.org/wiki/SMART_criteria", accessed: 2026-11-02 }
  - { id: wake-invest, title: "Bill Wake, INVEST in Good Stories, and SMART Tasks (2003-08-17)", resource: "https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/", url: "https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/", accessed: 2026-11-02 }
  - { id: gherkin-ref, title: "Gherkin reference (Cucumber docs)", resource: "https://cucumber.io/docs/gherkin/reference/", url: "https://cucumber.io/docs/gherkin/reference/", accessed: 2026-11-02 }
---

# Origin

- George T. Doran, "There's a S.M.A.R.T. way to write management's goals and
  objectives", *Management Review* 70(11), November 1981. His letters were Specific,
  Measurable, **Assignable**, **Realistic**, **Time-related**.[^smart-wiki] (Primary
  article not read; citation via Wikipedia.)
- Bill Wake, 17 August 2003: INVEST for stories, SMART (Specific, Measurable,
  Achievable, Relevant, Time-boxed) for **tasks**.[^wake-invest]
- Wikipedia notes SMART lacks a theoretical or empirical base and that Doran himself
  said quantifying is not always feasible.[^smart-wiki]

# Letter by letter, for one criterion

| Letter | Useful for a criterion? |
| --- | --- |
| Specific | Yes: one behaviour, named system, named outcome |
| Measurable | Yes: a value and unit, or an observable state |
| Achievable | Weak: a feasibility check on the story, not the line |
| Relevant | Some: the line should serve the story's goal |
| Time-bound | No for the line: the deadline belongs to the story or milestone. A **latency** threshold ("within 2 s") is Measurable, not Time-bound |

# Where it helps

Performance and quality criteria, where "fast" or "reliable" must become a number:
"p95 response under 300 ms on the fixture data", "no new lint errors", "bundle under
200 KB".

# Where it does not

Behaviour with no natural number. Forcing one invents a fake threshold. Use an
observable outcome instead: a message shown, a record created, a state reached. This
matches Gherkin's rule that `Then` checks something visible from outside.[^gherkin-ref]

# Is "Gherkin + SMART threshold" real practice?

- The **idea** (a `Then` with a measurable value) is common in tutorials and vendor
  blogs, and is consistent with the Gherkin docs.
- No primary or authoritative source was found that names a "Gherkin + SMART" method.
  The first sweep cited a "2026 best-practice summary" without naming it; it could not be
  found. Treat the synthesis as a reasonable kit choice, not as a recognised standard.
- Wake applied SMART to tasks, not to acceptance criteria. Crediting SMART-for-criteria
  to Wake is wrong.

# Related

- [Testable criteria heuristics](testable-criteria-heuristics.md)
- [Choosing a criteria form](choosing-a-criteria-form.md)
