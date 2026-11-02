---
type: Practice
title: User story mapping (Patton)
description: A two-dimensional backlog where user activities form a left-to-right backbone, stories hang below them, and horizontal slices mark releases, the first slice being a walking skeleton.
tags: [story-mapping, backlog, release-planning, walking-skeleton]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: patton-map
    title: "Jeff Patton: The New User Story Backlog is a Map (2008-10-08, updated 2023-04-12)"
    resource: https://jpattonassociates.com/the-new-backlog/
    accessed: 2026-11-02
  - id: wiki-user-story
    title: "Wikipedia: User story (History section)"
    resource: https://en.wikipedia.org/wiki/User_story
    accessed: 2026-11-02
---

# The problem it solves

A flat, ordered backlog shows build order but not what the system does. Patton: "Arranging
user stories in the order you'll build them doesn't help me explain to others what the
system does." A flat backlog is "a bag of context-free mulch."[^patton-map]

# The shape

```
time / narrative flow  ->
+-----------+-----------+-----------+    <- backbone: user activities ("big stories")
| Activity A| Activity B| Activity C|
+-----------+-----------+-----------+
| task      | task      | task      |    <- user tasks, left to right
| story     | story     | story     |  --- release 1 (walking skeleton) ---
| story     | story     |           |  --- release 2 ---
| story     |           | story     |
```

| Part | Patton's words |
| --- | --- |
| Activities | "At the top of the map are 'big stories.' I call them user activities."[^patton-map] |
| Backbone | The top row "look[s] a little like vertebrae"; these are "often the essential capabilities the system needs to have."[^patton-map] |
| User task | "what users do to reach their goals"[^patton-map] |
| Flow | "I'm always imagining time moving left to right." "Build the map in a way that helps you tell the story."[^patton-map] |
| Release slices | Masking tape lines make "horizontal swim lanes for each release."[^patton-map] |
| Walking skeleton | The stories placed highest "describe the smallest possible system you could build that would give you end to end functionality."[^patton-map] |

Patton's book on the method followed in 2014.[^wiki-user-story]

# Mapping to Epic, Story, Task

| Map element | Hierarchy element |
| --- | --- |
| Activity (backbone column) | Epic, or a Feature-style grouping |
| User task | Coarse story, often still too big |
| Card under a task | Story |
| Horizontal slice | Release, milestone, or "first slice" set of stories |
| First slice | [Walking skeleton](walking-skeleton-and-tracer-bullet.md) |

The map gives a second axis that a tree cannot: **across** epics (one thin slice through
every activity) instead of **down** one epic at a time. That is why it is a planning view,
not a replacement for the hierarchy.

# Use for an agent-built backlog

- Build the map once per epic group, then cut the first slice. Every story in that slice
  should be end to end (see [story splitting patterns](story-splitting-patterns.md)).
- A board can model slices with a milestone or an iteration field; activities with the
  parent epic. No new issue type is needed.
- The map is good for a human owner to review the plan as one picture before agents start.

# Caveats

- Only the 2008 blog post was read here, not the 2014 book.
- The post has no byline; the site is Jeff Patton's and the voice is first person.

[^patton-map]: Jeff Patton: The New User Story Backlog is a Map (2008-10-08, updated 2023-04-12), <https://jpattonassociates.com/the-new-backlog/>
[^wiki-user-story]: Wikipedia: User story (History section), <https://en.wikipedia.org/wiki/User_story>
