---
type: Practice
title: Titles and summaries that say what an item delivers
description: Sources agree that a work item's title names one outcome in plain words, verb first and short enough to scan in a list, and that its description opens with who benefits and why, with provenance and mechanism further down.
tags: [titles, summaries, user-stories, job-stories, epics, plain-language]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-13T18:30:00Z }
sources:
  - id: linear-method
    title: "Linear Method: Write issues not user stories"
    resource: https://linear.app/method/write-issues-not-user-stories
    accessed: 2026-11-13
  - id: thoughtbot-epics
    title: "thoughtbot: How to write good epics"
    resource: https://thoughtbot.com/blog/how-to-write-good-epics
    accessed: 2026-11-13
  - id: atlassian-ticket
    title: "Atlassian Community: How to write a useful Jira ticket"
    resource: https://community.atlassian.com/
    accessed: 2026-11-13
  - id: intercom-jobs
    title: "Paul Adams (Intercom): How we accidentally invented Job Stories"
    resource: https://www.intercom.com/blog/accidentally-invented-job-stories/
    accessed: 2026-11-02
  - id: cohn-epics
    title: "Mike Cohn: Stories, Epics and Themes"
    resource: https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes
    accessed: 2026-11-02
  - id: hw-split
    title: "Humanizing Work Guide to Splitting User Stories"
    resource: https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
    accessed: 2026-11-02
  - id: tracker-ehs
    title: "Pivotal Tracker blog: Using Tracker to communicate epic hypothesis statements"
    resource: https://www.pivotaltracker.com/blog/using-tracker-to-communicate-epic-hypothesis-statements
    accessed: 2026-11-13
---

# What the sources agree on

1. **Name the outcome, not the mechanism.** "An issue should describe a task with a clear,
   defined outcome", written "in plain language".[^linear-method] For an epic, ask whether
   the name is "focused on functionality / outcome, or is it talking about a technology
   layer?"[^thoughtbot-epics] The usual story failure is "tasks or components masquerading
   as stories".[^hw-split]
2. **A title is read in a list.** "The title should be easy to scan, since most people will
   read it on a list or board in the context of other issues."[^linear-method] "Phrase the
   title as an imperative command starting with a verb"; test it as "To complete this
   ticket, I need to <title>"; "A good title jogs the memory of what needs
   doing."[^atlassian-ticket]
3. **Say who benefits and why.** The user story names a role, the job story a situation
   ("When <situation>, I want to <motivation>, so I can <expected outcome>").[^intercom-jobs]
   A story is "simply something a user wants"[^cohn-epics]: the sentence form is optional,
   the outcome and the beneficiary are not. See
   [user stories and job stories](user-stories-and-job-stories.md).
4. **An epic carries one hypothesis, not a list.** SAFe's epic hypothesis statement reads
   "For <customers> who <do something>, the <solution> is a <how> that <provides this
   value>", followed by a business outcome hypothesis and leading
   indicators.[^tracker-ehs] Names can change as scope clears up.[^thoughtbot-epics]

# Failure patterns seen on boards

| Pattern | Generic example | Better |
| --- | --- | --- |
| Code or part prefix | "Part 3: the export retries on a busy store" | "Retry the export when the store is busy" |
| Layer or Kind prefix | "Server: refuse claims on closed issues" | "Refuse a claim on a closed issue" |
| Mechanism | "export_job gets a backoff parameter" | "Retry the export without flooding the store" |
| Several outcomes | "Lanes get slots, intake rules, and a review label" | One epic outcome; each part its own story |
| Insider words | "A handoff to a principal nobody holds surfaces" | "Show agents the items handed to them that nobody has picked up" |
| Provenance first | Body opens "Part of the epic (gap 2). From the field report ..." | Body opens with who it helps and what changes; provenance last |

# How the kit applies it

The [clear titles and summaries](/decisions/clear-titles-and-summaries.md) decision turns this
into rules, and the [prose check](../../../server-spec/prose-check.md) makes the mechanical
ones checkable.

# Caveats

- A verb list cannot tell a verb from a noun ("merge", "record"), so a missing verb is a
  warning for a reviewer, never a failure.
- Character limits are conventions (commit subjects, board cards), not research results.

[^linear-method]: Linear Method: Write issues not user stories, <https://linear.app/method/write-issues-not-user-stories>
[^thoughtbot-epics]: thoughtbot: How to write good epics, <https://thoughtbot.com/blog/how-to-write-good-epics>
[^atlassian-ticket]: Atlassian Community: How to write a useful Jira ticket, <https://community.atlassian.com/> (search the title)
[^intercom-jobs]: Paul Adams (Intercom): How we accidentally invented Job Stories, <https://www.intercom.com/blog/accidentally-invented-job-stories/>
[^cohn-epics]: Mike Cohn: Stories, Epics and Themes, <https://www.mountaingoatsoftware.com/blog/stories-epics-and-themes>
[^hw-split]: Humanizing Work Guide to Splitting User Stories, <https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/>
[^tracker-ehs]: Pivotal Tracker blog: Using Tracker to communicate epic hypothesis statements, <https://www.pivotaltracker.com/blog/using-tracker-to-communicate-epic-hypothesis-statements>
