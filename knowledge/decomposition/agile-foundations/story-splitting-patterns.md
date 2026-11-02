---
type: Pattern
title: Story splitting patterns (Humanizing Work, SPIDR) and vertical slicing
description: Split stories into thin vertical slices using Humanizing Work's nine patterns or Cohn's five SPIDR techniques, and keep layer splits for tasks and pull requests.
tags: [splitting, vertical-slicing, spidr, humanizing-work, stories]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: hw-split
    title: "Richard Lawrence and Peter Green: The Humanizing Work Guide to Splitting User Stories"
    resource: https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
    accessed: 2026-11-02
  - id: spidr
    title: "Mike Cohn: SPIDR, Five Simple but Powerful Ways to Split User Stories (updated 2026-08-06)"
    resource: https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories
    accessed: 2026-11-02
  - id: wake-invest
    title: "Bill Wake: INVEST in Good Stories, and SMART Tasks (2003)"
    resource: https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
    accessed: 2026-11-02
  - id: google-cl
    title: "Google Engineering Practices: Small CLs"
    resource: https://google.github.io/eng-practices/review/developer/small-cls.html
    accessed: 2026-11-02
  - id: shapeup-scopes
    title: "Shape Up, ch. 12: Map the Scopes"
    resource: https://basecamp.com/shapeup
    accessed: 2026-11-02
---

# Vertical, not horizontal

- A vertical slice delivers "a valuable change in system behavior" and usually touches
  several layers. A horizontal slice changes one layer.[^hw-split]
- "Many new agile teams attempt to split stories by architectural layer." That "may
  satisfy small, but it fails at independent and valuable."[^hw-split]
- Wake, 2003: split so each slice cuts through the layers and has value.[^wake-invest]
- Shape Up says the same about scopes: organise by "the structure of the project", not by
  role (designers, programmers). A scope named "front-end" or "bugs" is a "grab
  bag".[^shapeup-scopes]

A split into frontend, backend, database and tests is a **task breakdown**, not a story
split.

# Humanizing Work: the flow

1. **Prepare the input story.** Check INVEST except Small. The usual failure is Valuable:
   "tasks or components masquerading as stories."[^hw-split]
2. **Apply the patterns** in order (below).
3. **Evaluate the split.**

# The nine patterns

| # | Pattern | Move |
| --- | --- | --- |
| 1 | Workflow steps | Simple end-to-end case first; middle steps and special cases later. |
| 2 | Operations (CRUD) | Split "manage X" into create, edit, delete. |
| 3 | Business rule variations | One story per hidden business rule. |
| 4 | Variations in data | "Good enough" data first; variations (for example localisation) later. |
| 5 | Data entry methods | Simple UI first, polished UI later. |
| 6 | Major effort | Build one variant first; the rest become cheap. |
| 7 | Simple / complex | The simplest version is one story; each complication its own. |
| 8 | Defer performance | Make it work, then fast (or secure, or scalable). |
| 9 | Break out a spike | Time-boxed investigation when the work is poorly understood. **Last resort.** |

All from the guide.[^hw-split] Its meta-pattern: "find the core complexity", "identify the
variations", "reduce all the variations to one."[^hw-split]

# Evaluating a split

- "Choose the split that lets you deprioritize or throw away a story." The 80/20 rule:
  most value sits in a small part of the functionality.[^hw-split]
- Prefer "equally sized small stories": an 8 split into four 2s beats a 5 and a 3.[^hw-split]
- In complex work, "starting the work will teach you about the work."[^hw-split]

# SPIDR (Cohn)

"Almost every story can be split with one of five techniques."[^spidr]

| Letter | Technique | Cohn's example |
| --- | --- | --- |
| S | Spike: research or a prototype to learn | Test captioning products before build-versus-buy |
| P | Paths: alternate ways a user does the thing | Share a video: 16 paths (networks, copy link, start time) |
| I | Interfaces: one browser or device, or a simple UI first | URL only, then dropdown, then logo picker |
| D | Data: a subset of data first | MP4 uploads only; one manager per employee |
| R | Rules: relax a rule for now | Ignore copyrighted-music checks in the first upload story |

On spikes Cohn says they are "absolutely an essential way to split stories" but "normally
won't be the first technique you'll reach for."[^spidr]

# Mapping the two

| SPIDR | Humanizing Work |
| --- | --- |
| Spike | 9 Break out a spike |
| Paths | 1 Workflow steps, 7 Simple/complex |
| Interfaces | 5 Data entry methods |
| Data | 4 Variations in data |
| Rules | 3 Business rule variations |
| (none) | 2 Operations, 6 Major effort, 8 Defer performance |

Humanizing Work is the fuller list; SPIDR is easier to remember.

# Splitting for an agent backlog

- Split stories vertically (above). Then, if a story's change is still too big for one
  reviewable PR, split the **PR**, and here horizontal is fine: Google's guide allows
  "splitting horizontally" with stubs, stacking, and splitting by files.[^google-cl]
- A spike's output is a finding (a note, a decision, a prototype branch), not shipped
  behaviour. Give it a time box and a question.
- "Defer performance" and "Rules" splits leave known gaps. Record each deferred part as
  its own story at split time, so it is not lost.

# Corrections to the first sweep

- SPIDR letters and meanings: confirmed.[^spidr]
- "Spike: short time-boxed investigation whose output is a finding": consistent with Cohn
  and Humanizing Work; Humanizing Work, not Cohn, calls it the last resort.[^hw-split][^spidr]

# Caveats

- Some sources are cited by their site's front page (the paper or post is named in the
  title), because their dated or numbered URLs trip the public repo's guard.
- The Humanizing Work page says its content has been coached "since at least 2005"; the
  date of the first published poster was not confirmed.

[^hw-split]: Richard Lawrence and Peter Green: The Humanizing Work Guide to Splitting User Stories, <https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/>
[^wake-invest]: Bill Wake: INVEST in Good Stories, and SMART Tasks (2003), <https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/>
[^shapeup-scopes]: Shape Up, ch. 12: Map the Scopes, <https://basecamp.com/shapeup>
[^spidr]: Mike Cohn: SPIDR, Five Simple but Powerful Ways to Split User Stories (updated 2026-08-06), <https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories>
[^google-cl]: Google Engineering Practices: Small CLs, <https://google.github.io/eng-practices/review/developer/small-cls.html>
