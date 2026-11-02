---
type: Pattern
title: Walking skeleton and tracer bullet
description: Build the thinnest end-to-end slice first, linking the main parts of the system, then thicken it; the first story of a new epic should usually be this slice.
tags: [walking-skeleton, tracer-bullet, vertical-slicing, sequencing]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: bensguide
    title: "Ben's Guide: Walking Skeleton (quotes Cockburn's definition)"
    resource: https://bensguide.substack.com/p/walking-skeleton
    accessed: 2026-11-02
  - id: dolfing
    title: "Henrico Dolfing: Start your project with a walking skeleton (2018)"
    resource: https://henricodolfing.com/
    accessed: 2026-11-02
  - id: adzic
    title: "Gojko Adzic: Forget the walking skeleton, put it on crutches (2014-06-09)"
    resource: https://gojko.net/
    accessed: 2026-11-02
  - id: patton-map
    title: "Jeff Patton: The New User Story Backlog is a Map (2008)"
    resource: https://jpattonassociates.com/the-new-backlog/
    accessed: 2026-11-02
  - id: hw-split
    title: "Humanizing Work Guide to Splitting User Stories"
    resource: https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
    accessed: 2026-11-02
---

# Definitions

| Term | Definition | Source |
| --- | --- | --- |
| Walking skeleton (Cockburn) | "a tiny implementation of the system that performs a small end-to-end function." "It need not use the final architecture, but it should link together the main architectural components." "The architecture and the functionality can then evolve in parallel." | Quoted by three secondary authors[^bensguide][^dolfing][^adzic] |
| Tracer bullet | A similar idea from *The Pragmatic Programmer*: thin working code through all layers, kept and grown, unlike a throwaway prototype | Mentioned by Dolfing[^dolfing]; book not checked |
| Skeleton on crutches (Adzic) | Ship the user-facing part early on a simple stand-in back end, then replace the back end in steps | Adzic[^adzic] |
| Story-map first slice (Patton) | The stories placed highest "describe the smallest possible system you could build that would give you end to end functionality" | Patton[^patton-map] |

Adzic: "don't worry about making the skeleton walk, put it on crutches and ship out."
With a good pipeline, "back-ends can be updated and reconfigured without even interrupting
user flow."[^adzic]

# Why it comes first

- It proves the parts connect before anyone invests in one part.
- It turns integration risk into an early, small story instead of a late, large one.
- It is the natural first output of the "workflow steps" split: "simple end-to-end case
  first".[^hw-split]
- Every later story is a vertical slice that thickens the skeleton.

# On a board

- The first story of a new epic (or a new repo) is the skeleton. Its acceptance criteria
  are one end-to-end check that runs.
- Other stories in the epic are **blocked by** it (see [work dependencies](work-dependencies.md)).
  That makes the skeleton the head of the dependency graph.
- For agent-built work the skeleton is also where the human owner checks direction once,
  before agents fan out in parallel. That single early review is cheap and catches the
  most expensive mistake: building many slices on a wrong base.

# Skeleton versus spike

| | Walking skeleton | Spike |
| --- | --- | --- |
| Output | Running code that stays | A finding; code may be thrown away |
| Question | Do the parts connect end to end? | What should we build, or can we? |
| Done when | The end-to-end check passes | The question is answered |

# Caveats

- Cockburn's own definition page could not be fetched; the definition is quoted through
  three secondary authors who agree word for word. One says he wrote it up on his site in
  2008, having coined it in the 1990s.[^bensguide]
- Dolfing's and Adzic's posts are cited by site, because their dated URLs trip the public
  guard: Dolfing, "Start your project with a walking skeleton" (April 2018); Adzic,
  "Forget the walking skeleton, put it on crutches" (9 June 2014).
- *The Pragmatic Programmer* (Hunt and Thomas) was not checked directly.

[^bensguide]: Ben's Guide: Walking Skeleton (quotes Cockburn's definition), <https://bensguide.substack.com/p/walking-skeleton>
[^dolfing]: Henrico Dolfing: Start your project with a walking skeleton (2018), <https://henricodolfing.com/>
[^adzic]: Gojko Adzic: Forget the walking skeleton, put it on crutches (2014-06-09), <https://gojko.net/>
[^patton-map]: Jeff Patton: The New User Story Backlog is a Map (2008), <https://jpattonassociates.com/the-new-backlog/>
[^hw-split]: Humanizing Work Guide to Splitting User Stories, <https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/>
