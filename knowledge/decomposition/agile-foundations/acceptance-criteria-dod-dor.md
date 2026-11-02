---
type: Comparison
title: Acceptance criteria, Definition of Done, Definition of Ready
description: Three different checks with different owners and timing; only the Definition of Done is in Scrum, and a Definition of Ready used as a hard gate is widely criticised.
tags: [acceptance-criteria, definition-of-done, definition-of-ready, quality, gates]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: scrum-guide
    title: The 2020 Scrum Guide
    resource: https://scrumguides.org/scrum-guide.html
    accessed: 2026-11-02
  - id: scrumorg-ac
    title: "Scrum.org: What is the difference between the DoD and acceptance criteria?"
    resource: https://www.scrum.org/resources/what-difference-between-dod-and-acceptance-criteria
    accessed: 2026-11-02
  - id: jeffries-3cs
    title: "Ron Jeffries: Essential XP: Card, Conversation, Confirmation (2001)"
    resource: https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/
    accessed: 2026-11-02
  - id: north-bdd
    title: "Dan North: Introducing BDD (2006-09-20)"
    resource: https://dannorth.net/blog/introducing-bdd/
    accessed: 2026-11-02
  - id: aa-dor
    title: "Agile Alliance glossary: Definition of Ready"
    resource: https://www.agilealliance.org/glossary/definition-of-ready/
    accessed: 2026-11-02
  - id: cohn-dor
    title: "Mike Cohn: The Dangers of a Definition of Ready"
    resource: https://mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready
    accessed: 2026-11-02
  - id: kelly-dor
    title: "Allan Kelly: Definition of Ready considered harmful (2017-09-06)"
    resource: https://www.allankelly.net/archives/category/requirements/
    accessed: 2026-11-02
  - id: codex-bp
    title: "OpenAI Codex: Best practices"
    resource: https://developers.openai.com/codex/learn/best-practices.md
    accessed: 2026-11-02
  - id: copilot-bp
    title: "GitHub Docs: Best practices for using GitHub Copilot to work on tasks"
    resource: https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results
    accessed: 2026-11-02
---

# The three checks

| | Acceptance criteria (AC) | Definition of Done (DoD) | Definition of Ready (DoR) |
| --- | --- | --- | --- |
| Applies to | One item | Every item in the Increment | One item, before work starts |
| Question | Did we build the right thing for this item? | Is it built to the shared quality bar, so it is releasable? | Do we understand it well enough to start? |
| When checked | At acceptance of the item | At completion of every item | At selection / planning |
| Owner (usual) | Product Owner, written with the team (convention, not Scrum) | The Scrum Team; or the organisation's standard[^scrum-guide] | The team (convention) |
| In the Scrum Guide? | No[^scrumorg-ac] | Yes, a commitment of the Increment[^scrum-guide] | No |
| Root | XP Confirmation: "the acceptance test"[^jeffries-3cs] | Scrum | 2008 Scrum training material; ETVX (1985) entry criteria[^aa-dor] |

Scrum.org: DoD describes "characteristics of the Increment"; AC are characteristics of a
PBI. AC are "not technically part of Scrum, but is a valuable complementary
practice."[^scrumorg-ac]

**An item is done when its AC pass and the DoD is met.** The Guide's rule for a miss:
the item "cannot be released or even presented at the Sprint Review" and goes back to
the backlog.[^scrum-guide]

# Writing acceptance criteria

North's 2006 template:[^north-bdd]

```
Given some initial context (the givens),
When an event occurs,
Then ensure some outcomes.
```

North's heading is "Acceptance criteria should be executable": scenario parts are
"fine-grained enough to be represented directly in code."[^north-bdd]

Checks that make a criterion testable (synthesis, not one source):

- observable behaviour, not intent or look;
- one behaviour per criterion;
- concrete inputs and outcomes, with a number and unit where the behaviour has one;
- the happy path, plus at least one edge case and one error case;
- no implementation choice unless the interface is the requirement.

For agents the vendors say the same thing in their own words. OpenAI asks for a
"Done when:" line, because it "helps Codex stay scoped, make fewer assumptions, and
produce work that's easier to review."[^codex-bp] GitHub lists "complete acceptance criteria
on what a good solution looks like" as part of a well-scoped task.[^copilot-bp]

# Definition of Ready, and the case against it

Agile Alliance: the team "makes explicit and visible the criteria" an item must meet
before it enters an iteration, "generally based on the INVEST matrix."[^aa-dor]

Critiques:

| Critic | Argument |
| --- | --- |
| Mike Cohn | A DoR rule that "something must be done before the next thing can start" is "a huge step towards a sequential, stage-gate approach." Teams should practise "concurrent engineering". "Favor guidelines rather than rules on your Definition of Ready."[^cohn-dor] |
| Allan Kelly (2017) | A DoR "reduces agility because it breaks up process flow", adds wait states, and can block the top business priority because it is "not ready". Instead, once an item is prioritised, "the first task is to make it ready"; "the later the story becomes 'ready' the better."[^kelly-dor] |

Cohn allows one exception to "guidelines not rules": dependencies on other teams or
vendors.[^cohn-dor]

# Practical position for an agent board

- Keep **AC per story** and **one DoD per repo** (tests pass, review done, docs updated,
  and so on), inherited by every item.
- Keep DoR **thin and mechanical**: a story is ready to hand to an agent when it has an
  outcome, checkable AC, declared blockers that are closed, and fits one PR. Treat the
  rest as guidelines, per Cohn.
- When an item is top priority but not ready, the first task is to make it ready (Kelly),
  not to skip it.
- An agent cannot hold the "conversation" in a hallway. A thin DoR is more useful for
  agents than for humans, because a missing answer costs a whole wrong PR. That is the
  one real argument for DoR here; it is a synthesis, not a sourced finding.

# Caveats

- Some sources are cited by their site's front page (the paper or post is named in the
  title), because their dated or numbered URLs trip the public repo's guard.
- Who "owns" AC is convention. The Scrum Guide gives the Product Owner accountability for
  the backlog, not for AC by name.
- The Agile Alliance page does not name who wrote the 2008 DoR description. Secondary
  sources often credit Jeff Sutherland and Systematic; not verified here.

[^scrum-guide]: The 2020 Scrum Guide, <https://scrumguides.org/scrum-guide.html>
[^scrumorg-ac]: Scrum.org: What is the difference between the DoD and acceptance criteria?, <https://www.scrum.org/resources/what-difference-between-dod-and-acceptance-criteria>
[^jeffries-3cs]: Ron Jeffries: Essential XP: Card, Conversation, Confirmation (2001), <https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/>
[^aa-dor]: Agile Alliance glossary: Definition of Ready, <https://www.agilealliance.org/glossary/definition-of-ready/>
[^north-bdd]: Dan North: Introducing BDD (2006-09-20), <https://dannorth.net/blog/introducing-bdd/>
[^codex-bp]: OpenAI Codex: Best practices, <https://developers.openai.com/codex/learn/best-practices.md>
[^copilot-bp]: GitHub Docs: Best practices for using GitHub Copilot to work on tasks, <https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results>
[^cohn-dor]: Mike Cohn: The Dangers of a Definition of Ready, <https://mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready>
[^kelly-dor]: Allan Kelly: Definition of Ready considered harmful (2017-09-06), <https://www.allankelly.net/archives/category/requirements/>
