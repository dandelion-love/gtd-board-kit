---
type: Research Finding
title: Alert fatigue and receptivity
description: Clinicians accept fewer alerts as the number and share of repeats grow, and phone users find even useful notifications disruptive depending on sender, task and presentation, so volume and repetition must be kept low.
tags: [notifications, alert-fatigue, receptivity, mobile, clinical-decision-support, research]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: ancker-17, title: "Ancker et al., Effects of workload, work complexity, and repeated alerts on alert fatigue in a clinical decision support system (BMC Medical Informatics and Decision Making, 2017)", resource: "https://scholar.google.com/scholar?q=%22Effects+of+workload%2C+work+complexity%2C+and+repeated+alerts+on+alert+fatigue%22", doi: 10.1186/s12911-017-0430-8, accessed: 2026-11-05}
  - {id: psnet-ancker, title: "AHRQ PSNet summary of Ancker et al. 2017", resource: "https://psnet.ahrq.gov/issue/effects-workload-work-complexity-and-repeated-alerts-alert-fatigue-clinical-decision-support", accessed: 2026-11-05}
  - {id: mehrotra-16, title: "Mehrotra, Pejovic, Vermeulen, Hendley and Musolesi, My Phone and Me: Understanding People's Receptivity to Mobile Notifications (CHI 2016)", resource: "https://dblp.uni-trier.de/rec/conf/chi/MehrotraPVHM16.html", accessed: 2026-11-05}
---

# What it is

Two research threads on what happens when alerts pile up. Clinical decision support
is the best-studied case of alert fatigue. Mobile notification studies show how people
judge any single interruption.

# Alert fatigue in clinical decision support

Ancker et al. studied alerts and reminders shown to primary care clinicians.[^ancker-17]

| Finding | Figure |
| --- | --- |
| Share of drug alerts that were repeats for the same patient within a year | about one quarter[^ancker-17] |
| Share of clinical reminders that were repeats | about one third[^ancker-17] |
| Drop in reminder acceptance per extra reminder in one encounter | 30%[^ancker-17] |
| Drop per five-point rise in the share of repeated reminders | 10%[^ancker-17] |
| Effect of overall workload | none found[^ancker-17] |

The authors conclude that clinicians "became less likely to accept alerts as they
received more of them, particularly more repeated alerts", and that cutting
within-patient repeats is a promising target.[^ancker-17] A federal patient-safety
summary reads the paper the same way: reduce the number of alerts per patient.[^psnet-ancker]

The point for the kit: fatigue tracked **alerts per decision** and **repeats**, not how
busy the person was.

# Receptivity to mobile notifications

Mehrotra et al. logged 10,372 notifications and 474 questionnaire answers from 20 phone
users.[^mehrotra-16] Response time and felt disruption depended on:

- the sender and the receiver's relationship to them;
- the current task, its type, complexity and how near it was to completion;
- how the notification was presented and what kind of alert it used;
- personality traits.[^mehrotra-16]

Even notifications with important or useful content could be disruptive.[^mehrotra-16]

# Limits

- Clinical alerts are not code-review asks, but both are "accept or override" prompts
  shown to an expert under time pressure.
- The CHI 2016 DOI contains a long numeric string that this repo's public-content guard
  blocks; the source points to its dblp record instead. Abstract figures were taken from
  the university repository copy.

# What the kit can take from it

- Count **asks per item**. If one issue would raise a third ask, bundle them into one.
- Never re-send the same ask. Update the existing one and let its age show urgency.
- Measure the owner's **acceptance rate** of pushes. A falling rate is the fatigue
  signal; respond by pushing less, not louder.
- Usefulness does not license an interruption. "Useful to know" goes to the digest.
- The sender matters: the owner should be able to tell at a glance which agent and which
  issue sent an ask.

[^ancker-17]: Ancker et al., BMC Medical Informatics and Decision Making, 2017.
[^psnet-ancker]: AHRQ PSNet summary of Ancker et al.
[^mehrotra-16]: Mehrotra et al., My Phone and Me, CHI 2016.
