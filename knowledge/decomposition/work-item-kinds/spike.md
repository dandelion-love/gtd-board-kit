---
type: Practice
title: Spike
description: A short, time-boxed investigation that buys knowledge to cut risk or firm up an estimate; its output is a demonstrable finding, and its code is usually thrown away.
tags: [work-item-kinds, spike, enabler, timebox]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:50:00Z }
sources:
  - id: c2-spike
    resource: https://c2.com/xp/SpikeSolution.html
    title: Spike Solution (Portland Pattern Repository wiki)
    accessed: 2026-11-02
  - id: xp-rules-spike
    resource: http://www.extremeprogramming.org/rules/spike.html
    title: "Create spike solutions (extremeprogramming.org rules, Don Wells)"
    accessed: 2026-11-02
  - id: safe-spikes
    resource: https://scaledagileframework.com/spikes/
    title: SAFe, Spikes (last update 13 March 2023)
    accessed: 2026-11-02
  - id: safe-story
    resource: https://scaledagileframework.com/story
    title: SAFe, Story (last update 7 December 2022)
    accessed: 2026-11-02
  - id: cohn-spikes
    resource: https://www.mountaingoatsoftware.com/blog/spikes
    title: "Mike Cohn, Agile Spikes Deliver Knowledge So Teams Can Deliver Products (updated 6 Aug 2024)"
    accessed: 2026-11-02
---

# What it is

- **Origin: XP.** Kent Beck named it; Ward Cunningham's pattern: write the smallest code
  that performs the function apart from the existing mechanism.[^c2-spike] Ron Jeffries
  on the C3 project: "We plan to throw away the code, although sometimes something is
  salvaged."[^c2-spike]
- **XP rules page:** "a very simple program to explore potential solutions"; "expect to
  throw it away"; goal is "reducing the risk of a technical problem or increase the
  reliability of a user story's estimate"; a pair for "a week or two".[^xp-rules-spike]
- **SAFe:** "Spikes are a type of SAFe Enabler Story", in two forms, technical and
  functional. They sit in the Team Backlog, are "estimated, and sized to fit in an
  iteration".[^safe-spikes] Enabler stories are demonstrated "by showing the knowledge
  gained, artifacts produced".[^safe-story]
- **Cohn:** "a time-boxed research activity"; because it is time-boxed, "the investment
  is fixed", and the decision at the end may be to spend more time.[^cohn-spikes]

# Output and done

| Source | Output | Done when |
| --- | --- | --- |
| XP | knowledge; throwaway code[^xp-rules-spike] | risk reduced or estimate firm |
| SAFe | "demonstrable" output[^safe-spikes] | Product Owner accepts the demo against its acceptance criteria[^safe-spikes] |
| Cohn | knowledge to estimate or choose a solution[^cohn-spikes] | timebox ends; a decision on next steps is made[^cohn-spikes] |

Common thread: **done = the question is answered (or the timebox is spent) and the answer
is shown**, not "code merged".

# Where it sits

- SAFe: at **story level**, a peer of user stories in the team backlog.[^safe-spikes]
- Cohn reports both habits: a spike story on the product backlog, or a spike treated as
  part of another item and seen only on the sprint backlog.[^cohn-spikes]
- All three say use them **sparingly**: SAFe "The Exception, Not the Rule";[^safe-spikes]
  Cohn "only in cases of extreme or excessive amounts of uncertainty".[^cohn-spikes]

# For the kit

- Carrier: a **story-level issue** (Kind `spike`) under the epic whose risk it reduces.
- Needs a **timebox** in the body or a field; Size XS to M fits the kit's pull rule.
- Output: a [finding](finding.md) concept, linked from the issue; follow-up stories go in
  through capture as `agent-proposed`. Spike code goes on its branch; it is merged only if
  salvaged as part of a normal story.
- Compare [research](research-task.md); see the [mapping](kind-to-level-mapping.md).

# Caveats

- The XP site is quoted from extremeprogramming.org directly; a university mirror carries
  the same text.
- No primary source fixes a standard timebox length; "a week or two" is XP's 1990s
  number, SAFe only says "fit in an iteration".
