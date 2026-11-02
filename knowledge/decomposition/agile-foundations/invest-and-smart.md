---
type: Reference
title: INVEST for stories, SMART for tasks
description: Bill Wake's 2003 article gave INVEST for stories and SMART for tasks; SMART itself comes from George Doran's 1981 management article with different letter meanings.
tags: [invest, smart, story-quality, task-quality, wake, doran]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: wake-invest
    title: "Bill Wake: INVEST in Good Stories, and SMART Tasks (posted 2003-08-17, postscript 2011)"
    resource: https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
    accessed: 2026-11-02
  - id: doran-wiki
    title: "Wikipedia: SMART criteria (cites Doran, Management Review 70(11):35-36, 1981)"
    resource: https://en.wikipedia.org/wiki/SMART_criteria
    accessed: 2026-11-02
  - id: doran-history
    title: "Duncan Haughey: A Brief History of SMART Goals"
    resource: https://www.projectsmart.co.uk/brief-history-of-smart-goals.php
    accessed: 2026-11-02
  - id: hw-split
    title: "Humanizing Work Guide to Splitting User Stories"
    resource: https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
    accessed: 2026-11-02
  - id: aa-dor
    title: "Agile Alliance glossary: Definition of Ready"
    resource: https://www.agilealliance.org/glossary/definition-of-ready/
    accessed: 2026-11-02
---

# The article

Bill Wake, *INVEST in Good Stories, and SMART Tasks*, posted 17 August 2003 on xp123.com.
"I developed the INVEST acronym, and wrote this article in April and August, 2003." He
thanks Mike Cohn for feedback.[^wake-invest]

# INVEST (stories)

| Letter | Wake's meaning | Key line |
| --- | --- | --- |
| Independent | Stories do not overlap; "we'd like to be able to schedule and implement them in any order." | Wake admits this is not always possible.[^wake-invest] |
| Negotiable | Details are worked out between customer and programmer. | "It is not an explicit contract for features."[^wake-invest] |
| Valuable | Value to the customer. | Split vertically through layers so each slice has value.[^wake-invest] |
| Estimable | Enough to rank and schedule. | "We don't need an exact estimate, but just enough to help the customer rank and schedule."[^wake-invest] |
| Small | "Stories typically represent at most a few person-weeks worth of work." | Some teams use a few person-days.[^wake-invest] |
| Testable | Writing the card means "I understand what I want well enough that I could write a test for it." | Some teams write customer tests first.[^wake-invest] |

Wake's article does not use the phrase "acceptance criteria". Its nearest terms are
Confirmation (from Jeffries) and Testable.[^wake-invest]

Wake's 2011 postscript: he listed attributes, clustered them, and rearranged letters;
he considered VESTIGE and VESTING before INVEST.[^wake-invest]

# SMART (tasks), Wake's version

| Letter | Wake's meaning |
| --- | --- |
| Specific | Everyone understands the work. |
| Measurable | "Can we mark it as done?" The team defines done, which may include tests and refactoring. |
| Achievable | The owner can complete it; anyone may ask for help. |
| Relevant | Each task contributes to the story and can be justified to the customer. |
| Time-boxed | A set duration, so people know when to seek help or split the task. |

All from Wake, who notes that letter meanings vary across sources.[^wake-invest]

# SMART, Doran's original (1981)

George T. Doran, "There's a S.M.A.R.T. way to write management's goals and objectives",
*Management Review* 70(11), 1981.[^doran-wiki]

| Letter | Doran | Wake (2003) |
| --- | --- | --- |
| S | Specific: target a specific area for improvement | Specific |
| M | Measurable: quantify, or at least suggest, an indicator of progress | Measurable |
| A | **Assignable**: specify who will do it | **Achievable** |
| R | **Realistic**: results achievable with available resources | **Relevant** |
| T | **Time-related**: specify when the result can be achieved | **Time-boxed** |

Doran, as quoted: "the suggested acronym doesn't mean that every objective written will
have all five criteria."[^doran-history]

# Using them on a board

- INVEST is a review checklist for a story before it is ready (Agile Alliance: DoR is
  "generally based on the INVEST matrix").[^aa-dor] Humanizing Work checks INVEST *except*
  Small before splitting, and finds Valuable the usual failure: "tasks or components
  masquerading as stories."[^hw-split]
- SMART (Wake's sense) fits tasks well, and fits agent tasks very well: Time-boxed maps to
  a turn or spend cap; Measurable maps to a check command.
- Doran's "Assignable" is worth keeping for agent work: every task has one named owner.
- SMART on each acceptance criterion is a later adaptation. S, M and R work; T rarely
  belongs on a single criterion.

# First-sweep claims checked

| Claim | Verdict |
| --- | --- |
| INVEST is Wake, 2003 | Confirmed.[^wake-invest] |
| Wake paired INVEST for stories with SMART for tasks | Confirmed.[^wake-invest] |
| Wake's SMART = Specific, Measurable, Achievable, Relevant, Time-boxed | Confirmed.[^wake-invest] |
| SMART originated with Doran 1981 for management objectives | Confirmed, but Doran's A, R, T were Assignable, Realistic, Time-related.[^doran-wiki] |
| "A story passes INVEST if a competent team member could build it without a clarifying meeting" | **Not Wake.** It cuts against Negotiable, where details come from conversation. It is a reasonable bar for agent hand-off, but label it as the kit's own rule. |

# Caveats

- Doran's original paper was not read; the quotes come from secondary pages.

[^wake-invest]: Bill Wake: INVEST in Good Stories, and SMART Tasks (posted 2003-08-17, postscript 2011), <https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/>
[^doran-wiki]: Wikipedia: SMART criteria (cites Doran, Management Review 70(11):35-36, 1981), <https://en.wikipedia.org/wiki/SMART_criteria>
[^doran-history]: Duncan Haughey: A Brief History of SMART Goals, <https://www.projectsmart.co.uk/brief-history-of-smart-goals.php>
[^aa-dor]: Agile Alliance glossary: Definition of Ready, <https://www.agilealliance.org/glossary/definition-of-ready/>
[^hw-split]: Humanizing Work Guide to Splitting User Stories, <https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/>
