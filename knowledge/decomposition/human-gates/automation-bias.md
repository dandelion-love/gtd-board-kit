---
type: Concept
title: Automation bias
description: People over-trust automated output, missing its errors and following its wrong advice; it is worse under time pressure and when the output looks finished.
tags: [automation-bias, complacency, human-factors, code-review]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: skitka1999, title: "Skitka, Mosier, Burdick (1999). Does automation bias decision-making? Int J Human-Computer Studies 51(5):991-1006", resource: "https://scholar.google.com/scholar?q=%22Does+automation+bias+decision-making%22", doi: "10.1006/ijhc.1999.0252", accessed: 2026-11-02}
  - {id: pr1997, title: "Parasuraman, Riley (1997). Humans and automation: use, misuse, disuse, abuse. Human Factors 39(2):230-253", resource: "https://scholar.google.com/scholar?q=%22Humans+and+automation%3A+Use%2C+misuse%2C+disuse%2C+abuse%22", accessed: 2026-11-02}
  - {id: pm2010, title: "Parasuraman, Manzey (2010). Complacency and bias in human use of automation: an attentional integration. Human Factors 52(3):381-410", resource: "https://scholar.google.com/scholar?q=%22Complacency+and+bias+in+human+use+of+automation%22", accessed: 2026-11-02}
  - {id: goddard2012, title: "Goddard, Roudsari, Wyatt (2012). Automation bias: a systematic review of frequency, effect mediators, and mitigators. JAMIA 19(1):121-127", resource: "https://scholar.google.com/scholar?q=%22Automation+bias%3A+a+systematic+review+of+frequency%2C+effect+mediators%2C+and+mitigators%22", doi: "10.1136/amiajnl-2011-000089", accessed: 2026-11-02}
  - {id: perry2023, title: "Perry, Srivastava, Kumar, Boneh (2023). Do users write more insecure code with AI assistants? ACM CCS", resource: "https://scholar.google.com/scholar?q=%22Do+users+write+more+insecure+code+with+AI+assistants%22", accessed: 2026-11-02}
---

# What it is

Two error types, named by Skitka, Mosier and Burdick: **omission** (missing a problem
because the automation did not flag it) and **commission** (following the automation's
wrong advice).[^skitka1999] Parasuraman and Riley call over-reliance "misuse".[^pr1997]
Parasuraman and Manzey tie complacency and bias to attention: both show up when people
share attention between the automation and other tasks, and both affect experts as well
as novices.[^pm2010]

# Evidence

| Finding | Source |
| --- | --- |
| Omission and commission errors appear when an automated aid is present | Skitka et al. 1999[^skitka1999] |
| Review of 74 studies: workload, task complexity and time pressure mediate automation bias; trust and confidence are attitude mediators | Goddard et al. 2012[^goddard2012] |
| Mitigators: training, **emphasising user accountability**, placement of advice, updated confidence levels, giving information rather than recommendations | Goddard et al. 2012[^goddard2012] |
| With an AI code assistant, participants wrote significantly less secure code and were more likely to believe it was secure | Perry et al. 2023[^perry2023] |
| Participants who trusted the AI less and iterated on prompts wrote fewer vulnerabilities | Perry et al. 2023[^perry2023] |

# What it means for gates

- **A polished PR invites commission errors.** The reviewer sees a finished, tested-looking
  diff and approves. Ask for the evidence (command, output, screenshot), not a summary.
- **Information, not recommendation.** An ask that says "Approve?" with the agent's
  recommendation pre-selected pushes toward yes. Showing what changed and what was not
  checked is a known mitigator.[^goddard2012]
- **Accountability helps.** Recording *who* approved and *on what* (AI-DLC's audit,
  a named reviewer on a PR) is a documented mitigator, not just paperwork.[^goddard2012]
- **Time pressure hurts.** Batch gates into a planned sitting rather than interrupting; see
  [batching](batching-and-one-question-at-a-time.md).

# Caveats

- Most of this literature is aviation and clinical decision support. Perry et al. is the
  one software study here, and it measured writing code, not reviewing agent PRs.
- Abstracts of Goddard 2012 and Perry 2023 were read for this page; Skitka 1999 and the two
  Parasuraman papers are cited from prior knowledge of them, so re-check before quoting.
- Source links are title searches, and some DOIs are left out: the public guard flags
  resolver paths and long numeric ids as private-data shapes. Perry et al. is ACM CCS 2023.

[^skitka1999]: Skitka, Mosier and Burdick 1999.
[^pr1997]: Parasuraman and Riley 1997.
[^pm2010]: Parasuraman and Manzey 2010.
[^goddard2012]: Goddard, Roudsari and Wyatt 2012, abstract.
[^perry2023]: Perry et al. 2023, abstract.
