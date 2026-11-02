---
type: Concept
title: Story points, their critiques, and flow metrics
description: Story points are a relative effort estimate; their likely inventor regrets their misuse, #NoEstimates argues for slicing and counting instead, and the Kanban Guide replaces estimates with four flow measures.
tags: [estimation, story-points, noestimates, flow-metrics, kanban, sizing]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: cohn-points
    title: "Mike Cohn: What Are Story Points? (updated 2023-06-28)"
    resource: https://www.mountaingoatsoftware.com/blog/what-are-story-points
    accessed: 2026-11-02
  - id: cohn-poker
    title: "Mountain Goat Software: Planning Poker"
    resource: https://www.mountaingoatsoftware.com/agile/planning-poker
    accessed: 2026-11-02
  - id: jeffries-points
    title: "Ron Jeffries: Story Points Revisited (2019-05-23)"
    resource: https://ronjeffries.com/
    accessed: 2026-11-02
  - id: jeffries-noest
    title: "Ron Jeffries: The NoEstimates Movement (2013-04-29)"
    resource: https://ronjeffries.com/xprog/articles/the-noestimates-movement/
    accessed: 2026-11-02
  - id: techbeacon-noest
    title: "TechBeacon: The #NoEstimates debate, an unbiased look"
    resource: https://techbeacon.com/noestimates-debate-unbiased-look-origins-arguments-thought-leaders-behind-movement
    accessed: 2026-11-02
  - id: kanban-guide
    title: "The Kanban Guide v2025.5 (2025-05-01)"
    resource: https://kanbanguides.org/english/
    accessed: 2026-11-02
  - id: scrum-guide
    title: The 2020 Scrum Guide
    resource: https://scrumguides.org/scrum-guide.html
    accessed: 2026-11-02
  - id: wibas-safe
    title: "Malte Foegen (wibas): Estimation with Normalized Story Points? Really? (2024-04-09)"
    resource: https://www.wibas.com/en/blog/articles-1/estimation-with-normalized-story-points-really-343
    accessed: 2026-11-02
  - id: shapeup-glossary
    title: "Shape Up glossary (appetite)"
    resource: https://basecamp.com/shapeup
    accessed: 2026-11-02
  - id: hw-split
    title: "Humanizing Work Guide to Splitting User Stories"
    resource: https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
    accessed: 2026-11-02
---

# Story points

- Cohn: "a unit of measure for expressing an estimate of the overall effort that will be
  required." Three inputs: "the amount of work to do", "the complexity of the work", "any
  risk or uncertainty in doing the work". "Ultimately, story points are an estimate of
  effort", not of complexity alone.[^cohn-points]
- Scale: Mountain Goat lists "a typical Planning Poker deck" as 0, 1, 2, 3, 5, 8, 13, 20,
  40, 100.[^cohn-poker]
- Relative and team-internal by default. SAFe is the main exception: it aligns reference
  stories across teams so points are roughly comparable (secondary source; the article
  says "1 point = 1 ideal day" is a misconception).[^wibas-safe]
- The Scrum Guide names no unit. The Developers own sizing.[^scrum-guide]

# The inventor's regret

Ron Jeffries, 2019: "I may have invented story points, and if I did, I'm sorry now." He
is "probably a little sorry now, but not very sorry," and "deplore[s] their misuse."[^jeffries-points]

History he gives: XP estimated in time, then "Ideal Days"; the gap with real days
confused stakeholders, so the unit became "points", and "we really only used the points
to decide how much work to take into an iteration."[^jeffries-points]

What he recommends instead:

- "slice stories down until they just need a single acceptance test";
- "find the most valuable things to do, and to do them quickly";
- "provide small amounts of value frequently";
- drop points if they add no value.[^jeffries-points]

# #NoEstimates

- Origin: Woody Zuill's 2012 blog post and the first #NoEstimates tweet (secondary
  source).[^techbeacon-noest]
- The approach attributed to Zuill: build the most important story in small pieces, count
  stories instead of points, slice until one person can finish one in a sprint, and
  forecast from the count.[^techbeacon-noest]
- Jeffries in 2013: "a darn good idea. Working in continuous flow, without story
  estimates, is a great way to work." Also: "Estimates are often used as a bludgeon to try
  to get programmers to work faster." He asks how to serve customers who need cost or
  date answers.[^jeffries-noest]
- Critics say the stance drifted from "no estimates, period" to "estimates are fine if and
  when they work" (Peter Kretzman, quoted).[^techbeacon-noest]

Shape Up takes the other side of the same coin: fix the time as **appetite**, "as opposed
to an estimate", and cut scope to fit.[^shapeup-glossary]

# Flow metrics instead of estimates

The Kanban Guide's four required measures:[^kanban-guide]

| Measure | Definition |
| --- | --- |
| WIP | "The number of work items started but not finished." |
| Throughput | "The number of work items finished per unit of time." It is "the exact count of work items." |
| Work Item Age | "The elapsed time between when a work item started and the current date." |
| Cycle Time | "The elapsed time between when a work item started and when a work item finished." |

These need no estimate. They work best when items are of **similar small size**, which
is also what Humanizing Work's split rule aims at ("equally sized small
stories").[^hw-split]

# A size scale for a board

| Option | Good for | Cost |
| --- | --- | --- |
| Points (Fibonacci) | Teams with a stable velocity | Ceremony; misuse as a productivity target |
| T-shirt (S, M, L, XL) | Rough epic-level triage | Not additive |
| "Fits the size rule or split it" (binary) | Agent-built work, flow metrics | Needs a written size rule (see [sizing for AI agents](sizing-work-for-ai-agents.md)) |
| Appetite (time cap) | Fixed-time bets | Needs a person willing to cut scope |

For one owner and agents, the evidence points to the binary rule plus flow metrics.
Points add little when there is no team velocity to protect.

# First-sweep claims checked

| Claim | Verdict |
| --- | --- |
| Points combine effort, complexity, risk and uncertainty, not hours | Confirmed (Cohn).[^cohn-points] |
| Modified Fibonacci 1, 2, 3, 5, 8, 13, 20, 40, 100 | Confirmed, with 0 also on the deck.[^cohn-poker] |
| Points are not cross-team | True by default; SAFe normalises across teams.[^wibas-safe] |
| An estimate of 13 or more is a strong split signal | **Not found in a primary source.** A common team convention; label it as the kit's rule. |

# Caveats

- Some sources are cited by their site's front page (the paper or post is named in the
  title), because their dated or numbered URLs trip the public repo's guard.
- Zuill's own 2012 post was not located; origin details are from a secondary article.

[^cohn-points]: Mike Cohn: What Are Story Points? (updated 2023-06-28), <https://www.mountaingoatsoftware.com/blog/what-are-story-points>
[^cohn-poker]: Mountain Goat Software: Planning Poker, <https://www.mountaingoatsoftware.com/agile/planning-poker>
[^wibas-safe]: Malte Foegen (wibas): Estimation with Normalized Story Points? Really? (2024-04-09), <https://www.wibas.com/en/blog/articles-1/estimation-with-normalized-story-points-really-343>
[^scrum-guide]: The 2020 Scrum Guide, <https://scrumguides.org/scrum-guide.html>
[^jeffries-points]: Ron Jeffries: Story Points Revisited (2019-05-23), <https://ronjeffries.com/>
[^techbeacon-noest]: TechBeacon: The #NoEstimates debate, an unbiased look, <https://techbeacon.com/noestimates-debate-unbiased-look-origins-arguments-thought-leaders-behind-movement>
[^jeffries-noest]: Ron Jeffries: The NoEstimates Movement (2013-04-29), <https://ronjeffries.com/xprog/articles/the-noestimates-movement/>
[^shapeup-glossary]: Shape Up glossary (appetite), <https://basecamp.com/shapeup>
[^kanban-guide]: The Kanban Guide v2025.5 (2025-05-01), <https://kanbanguides.org/english/>
[^hw-split]: Humanizing Work Guide to Splitting User Stories, <https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/>
