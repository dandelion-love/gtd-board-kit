---
type: Practice
title: User stories, the 3 Cs, and job stories
description: The Connextra template, Jeffries' Card-Conversation-Confirmation, and the job story as an alternative that names the situation instead of the role.
tags: [user-stories, job-stories, connextra, three-cs, jtbd]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: agile-alliance-story
    title: "Agile Alliance glossary: User Story"
    resource: https://agilealliance.org/glossary/user-story
    accessed: 2026-11-02
  - id: jeffries-3cs
    title: "Ron Jeffries: Essential XP: Card, Conversation, Confirmation (2001-08-30)"
    resource: https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/
    accessed: 2026-11-02
  - id: wake-invest
    title: "Bill Wake: INVEST in Good Stories, and SMART Tasks (2003)"
    resource: https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
    accessed: 2026-11-02
  - id: north-bdd
    title: "Dan North: Introducing BDD (2006-09-20)"
    resource: https://dannorth.net/blog/introducing-bdd/
    accessed: 2026-11-02
  - id: intercom-jobs
    title: "Paul Adams (Intercom): How we accidentally invented Job Stories (2016-06-28)"
    resource: https://www.intercom.com/blog/accidentally-invented-job-stories/
    accessed: 2026-11-02
  - id: cohn-jobs
    title: "Mike Cohn: Job Stories Offer a Viable Alternative to User Stories"
    resource: https://www.mountaingoatsoftware.com/blog/job-stories-offer-a-viable-alternative-to-user-stories
    accessed: 2026-11-02
  - id: linear-method
    title: "Linear Method: Write issues not user stories"
    resource: https://linear.app/method/write-issues-not-user-stories
    accessed: 2026-11-02
  - id: cohn-epics
    title: "Mike Cohn: Stories, Epics and Themes"
    resource: https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes
    accessed: 2026-11-02
---

# The Connextra template

```
As a <role>, I want <capability>, so that <benefit>.
```

The "role-feature-reason" format was invented at Connextra in the UK in 2001.[^agile-alliance-story]
Dan North's 2006 BDD article uses the same three lines and pairs them with Given/When/Then
scenarios.[^north-bdd] See [acceptance criteria, DoD and DoR](acceptance-criteria-dod-dor.md).

The template is a convention, not the definition of a story. A story is "simply something a user
wants"[^cohn-epics]; the sentence is one way to write it down.

# The 3 Cs (Jeffries, 2001)

| C | Jeffries' words | Meaning for a board |
| --- | --- | --- |
| Card | "The card is a token representing the requirement."[^jeffries-3cs] | The issue title and short body. Not a contract. |
| Conversation | "the requirement itself is communicated from customer to programmers through conversation."[^jeffries-3cs] | Comments, clarifying questions, linked notes. |
| Confirmation | "This component is the acceptance test."[^jeffries-3cs] | Acceptance criteria that can be checked. |

Wake's "Negotiable" letter says the same: a story "is not an explicit contract for
features."[^wake-invest]

**Agent note.** An AI builder has no hallway conversation. The Conversation has to be
written down (in the issue, or as answered questions) before it builds, or the agent must
be allowed to ask. This is the strongest reason to make Confirmation explicit.

# Job stories

```
When <situation>, I want to <motivation>, so I can <expected outcome>.
```

- Origin: Intercom. Paul Adams writes that the format "didn't have that name at the time"
  and that "Alan Klement later named it for us."[^intercom-jobs]
- Why: "Personas look at roles and attributes, JTBD looks at situations and
  motivations."[^intercom-jobs] Intercom also found user stories were written from an
  engineering view, describing functions, not motives.[^intercom-jobs]
- Cohn's view: a job story "is focused less on the user performing some function than on
  the job to be done." It is "the better option when your product has users but their needs
  are not very distinct." He suggests mixing both in one backlog.[^cohn-jobs]

# Which to use

| Situation | Format |
| --- | --- |
| Distinct user roles with different needs | User story (Connextra) |
| One kind of user; the trigger or context matters | Job story |
| Internal or technical work with no user (a migration, a CI fix) | Plain task with a clear outcome (Linear style)[^linear-method] |
| Mixed | Allow both; require the "so that" or "so I can" clause either way |

Linear's position is the strongest critique: user stories are "an anti-pattern"; write "a
task with a clear, defined outcome" instead.[^linear-method] The useful part to keep from
both sides: **state the outcome and who or what benefits.** A role sentence with no
checkable outcome adds little.

# Caveats

- Forcing "As a developer, I want ..." onto technical work is a common smell. Cohn's own
  phrasing (a story is "simply something a user wants")[^cohn-epics] does not require the template.
- Job story dates: the Intercom post is from 2016 but describes earlier practice; Klement's
  naming article is commonly dated 2013 (not checked against the original).

[^agile-alliance-story]: Agile Alliance glossary: User Story, <https://agilealliance.org/glossary/user-story>
[^north-bdd]: Dan North: Introducing BDD (2006-09-20), <https://dannorth.net/blog/introducing-bdd/>
[^cohn-epics]: Mike Cohn: Stories, Epics and Themes, <https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes>
[^jeffries-3cs]: Ron Jeffries: Essential XP: Card, Conversation, Confirmation (2001-08-30), <https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/>
[^wake-invest]: Bill Wake: INVEST in Good Stories, and SMART Tasks (2003), <https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/>
[^intercom-jobs]: Paul Adams (Intercom): How we accidentally invented Job Stories (2016-06-28), <https://www.intercom.com/blog/accidentally-invented-job-stories/>
[^cohn-jobs]: Mike Cohn: Job Stories Offer a Viable Alternative to User Stories, <https://www.mountaingoatsoftware.com/blog/job-stories-offer-a-viable-alternative-to-user-stories>
[^linear-method]: Linear Method: Write issues not user stories, <https://linear.app/method/write-issues-not-user-stories>
