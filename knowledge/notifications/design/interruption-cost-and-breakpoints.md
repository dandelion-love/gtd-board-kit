---
type: Research Finding
title: Interruption cost and breakpoints
description: Field and lab studies show interruptions raise stress and frustration even when people keep pace, and that holding a notification until the person reaches a task breakpoint cuts frustration at a cost of about a minute and a half of delay.
tags: [notifications, interruption, attention, breakpoints, hci, research]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: iqbal-horvitz-07, title: "Iqbal and Horvitz, Disruption and Recovery of Computing Tasks: Field Study, Analysis, and Directions (CHI 2007)", resource: "https://www.microsoft.com/en-us/research/publication/disruption-recovery-computing-tasks-field-study-analysis-directions/", accessed: 2026-11-05}
  - {id: iqbal-bailey-08, title: "Iqbal and Bailey, Effects of Intelligent Notification Management on Users and Their Tasks (CHI 2008)", resource: "https://www.interruptions.net/literature/Iqbal-CHI08.pdf", accessed: 2026-11-05}
  - {id: mark-08, title: "Mark, Gudith and Klocke, The Cost of Interrupted Work: More Speed and Stress (CHI 2008)", resource: "https://www.interruptions.net/literature/Mark-CHI08.pdf", accessed: 2026-11-05}
---

# What it is

Human-computer interaction research on what an interruption costs and when it costs
least. These papers back the kit's choice to hold most messages rather than push them.

# Findings

**Iqbal and Horvitz, CHI 2007.** A field study logged how computer users suspend and
resume tasks, including incoming email and instant-message alerts.[^iqbal-horvitz-07]
The work fed into systems that estimate the cost of interrupting someone before
alerting them.[^iqbal-horvitz-07] The landing page gives the abstract only; the detailed
numbers are in the paper and were not re-checked here.

**Iqbal and Bailey, CHI 2008.** A lab study held notifications until detected task
breakpoints.

| Measure | Result |
| --- | --- |
| Frustration | lower at coarse breakpoints than fine ones, and lower than immediate delivery, in a diagram task[^iqbal-bailey-08] |
| Reaction time | relevant notifications answered faster at breakpoints than immediately (3.07 s vs 4.08 s)[^iqbal-bailey-08] |
| Resumption time | not significantly changed by scheduling[^iqbal-bailey-08] |
| Cost | mean deferral of 88.6 s[^iqbal-bailey-08] |

The authors suggest relevant notifications can go at finer breakpoints and general
interest ones should wait for coarse breakpoints. "Scheduling notifications at
breakpoints reduces frustration and reaction time."[^iqbal-bailey-08]

**Mark, Gudith and Klocke, CHI 2008.** Interrupted people finished email tasks faster
with no loss of quality, but reported significantly more stress, frustration, time
pressure and effort.[^mark-08] Speed hides the cost: the price is paid in strain.[^mark-08]

# Limits

- Lab tasks and small samples. The kit's owner is a developer switching between deep
  work and reviews, which is close to but not the same as these settings.
- The ACM DOIs for these papers contain long numeric strings that this repo's
  public-content guard blocks. Find them in the ACM Digital Library by title.

# What the kit can take from it

- A short delay is cheap. Holding an ask for minutes to reach a natural break costs
  little and lowers frustration.
- Natural breakpoints for a developer-owner are visible to the system: a PR merged, a
  review submitted, a board session ending. Release held asks then.
- General-interest items ("an agent finished", "CI passed") should wait for coarse
  breaks such as a daily digest.
- Do not judge success by response speed. A fast reply can still mean a costly
  interruption.

[^iqbal-horvitz-07]: Iqbal and Horvitz, Disruption and Recovery of Computing Tasks, CHI 2007.
[^iqbal-bailey-08]: Iqbal and Bailey, Effects of Intelligent Notification Management, CHI 2008.
[^mark-08]: Mark, Gudith and Klocke, The Cost of Interrupted Work, CHI 2008.
