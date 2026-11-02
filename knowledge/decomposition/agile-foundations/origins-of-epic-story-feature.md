---
type: Reference
title: Where Epic, Story, Theme and Feature come from
description: Story and epic come from Extreme Programming teams, the story template from Connextra, the 3 Cs from Ron Jeffries, and Feature from Feature-Driven Development long before SAFe made it a formal level.
tags: [history, user-stories, epics, features, xp, safe]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: wiki-user-story
    title: "Wikipedia: User story (History section)"
    resource: https://en.wikipedia.org/wiki/User_story
    accessed: 2026-11-02
  - id: agile-alliance-story
    title: "Agile Alliance glossary: User Story"
    resource: https://agilealliance.org/glossary/user-story
    accessed: 2026-11-02
  - id: jeffries-3cs
    title: "Ron Jeffries: Essential XP: Card, Conversation, Confirmation (2001-08-30)"
    resource: https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/
    accessed: 2026-11-02
  - id: cohn-epics
    title: "Mike Cohn: Stories, Epics and Themes"
    resource: https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes
    accessed: 2026-11-02
  - id: fdd
    title: "AgileConnection: Feature-Driven Development, an agile alternative to Extreme Programming"
    resource: https://agileconnection.com/article/feature-driven-development-agile-alternative-extreme-programming
    accessed: 2026-11-02
  - id: safe-features
    title: "SAFe: Features and Capabilities"
    resource: https://framework.scaledagile.com/features-and-capabilities
    accessed: 2026-11-02
  - id: safe-epic
    title: "SAFe: Epic"
    resource: https://framework.scaledagile.com/epic/
    accessed: 2026-11-02
  - id: wake-invest
    title: "Bill Wake: INVEST in Good Stories, and SMART Tasks (2003)"
    resource: https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
    accessed: 2026-11-02
---

# Timeline

| Year | Event | Source quality |
| --- | --- | --- |
| 1997 | Kent Beck uses user stories on the Chrysler C3 project.[^wiki-user-story] | Secondary only |
| 1998 | Alistair Cockburn: "a user story is a promise for a conversation."[^wiki-user-story] Wake credits Cockburn with cards as "tokens promising a future conversation".[^wake-invest] | Secondary, plus Wake |
| 1999 | Beck, *Extreme Programming Explained*: stories in the planning game.[^wiki-user-story] | Secondary only |
| ~1997-1999 | Feature-Driven Development (Coad, De Luca): a feature is "a small, deliverable client-valued piece of functionality", named "action result object".[^fdd] | Secondary |
| 2001 | The role-feature-reason template ("As a ... I want ... so that ...") is "invented at Connextra in the UK".[^agile-alliance-story] | Agile Alliance glossary |
| 2001 | Jeffries: Card, Conversation, Confirmation.[^jeffries-3cs] | Primary |
| 2003 | Wake: INVEST for stories, SMART for tasks.[^wake-invest] See [INVEST and SMART](invest-and-smart.md). | Primary |
| 2004 | Cohn, *User Stories Applied*, generalises stories beyond cards.[^wiki-user-story] | Secondary |
| 2008 | Patton: the story map.[^wiki-user-story] See [user story mapping](user-story-mapping.md). | Primary in that file |
| 2010s | SAFe makes Epic, Capability, Feature, Story formal levels.[^safe-features][^safe-epic] | Primary |

# The original meanings

- **Story.** "Simply something a user wants" (Cohn).[^cohn-epics] Jeffries: the card "is a
  token representing the requirement"; the requirement itself travels by conversation; the
  confirmation "is the acceptance test."[^jeffries-3cs]
- **Epic.** "As defined by the XP teams that invented user stories, an epic is a large user
  story." "There's no magic threshold at which we call a particular story an epic."[^cohn-epics]
  In XP an epic is a size label meaning "split me", not a container type.
- **Theme.** "A collection of user stories." It can be smaller or larger than an
  epic.[^cohn-epics]
- **Feature.** Not an XP term. Cohn uses it for a story big enough to release alone and
  suggests a tag, not a level.[^cohn-epics] FDD used it as its core unit.[^fdd] SAFe defines it
  as functionality sized for one Agile Release Train within a Program Increment.[^safe-features]
- **SAFe Epic.** "A significant solution development initiative" that needs an MVP and a Lean
  business case.[^safe-epic] This is a portfolio investment, much bigger than an XP epic.

# Why this matters

The same word means different things:

| Word | XP / Cohn | SAFe | Jira default |
| --- | --- | --- | --- |
| Epic | A story too big for one iteration | Portfolio investment with a business case | Level above standard items |
| Feature | A tag for a releasable story | Level between Capability and Story, one ART, one PI | Not a default type |
| Story | Something a user wants, small | Team-level item "a few days or less" | A standard item, peer of Task and Bug |

A standard should define its words, not assume them. See
[work item hierarchies compared](work-item-hierarchies-compared.md).

# Corrections to the first sweep

- "Feature is formally defined in SAFe, not in Scrum" is true but incomplete. Feature was a
  defined unit in FDD in the late 1990s, and Azure DevOps ships it as a type. SAFe is one of
  several sources.
- "Epic and Story are conventions from Extreme Programming" is confirmed.[^cohn-epics]

# Open questions

- The Connextra inventor. Cohn credits Rachel Davies; Davies credits the team. The Wikipedia
  line is marked "citation needed".[^wiki-user-story] Credit "the Connextra team".
- FDD dates. Secondary sources say a Singapore bank project in 1997 and the book *Java
  Modeling in Color with UML* in 1999. Not checked against the book.

[^wiki-user-story]: Wikipedia: User story (History section), <https://en.wikipedia.org/wiki/User_story>
[^wake-invest]: Bill Wake: INVEST in Good Stories, and SMART Tasks (2003), <https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/>
[^fdd]: AgileConnection: Feature-Driven Development, an agile alternative to Extreme Programming, <https://agileconnection.com/article/feature-driven-development-agile-alternative-extreme-programming>
[^agile-alliance-story]: Agile Alliance glossary: User Story, <https://agilealliance.org/glossary/user-story>
[^jeffries-3cs]: Ron Jeffries: Essential XP: Card, Conversation, Confirmation (2001-08-30), <https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/>
[^safe-features]: SAFe: Features and Capabilities, <https://framework.scaledagile.com/features-and-capabilities>
[^safe-epic]: SAFe: Epic, <https://framework.scaledagile.com/epic/>
[^cohn-epics]: Mike Cohn: Stories, Epics and Themes, <https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes>
