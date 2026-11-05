---
type: Decision
title: Requests between projects go through an intake and get an ack
description: A project receives other projects' requests as labelled issues in its repo, acknowledges each with a signed ack record, and the filer flags a person when no ack comes in time; an intake lane starts in observe.
tags: [intake, lanes, coordination, liveness]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:30:00Z }
---

# Context

Projects ask each other for work: one project's agent needs a kit change, a server tool
or a decision that another project owns. Before this, a request went wherever the filing
agent thought best, and the receiving project heard of it only when someone relayed it.
The filer could not tell a request that was seen from one that went nowhere, and when the
relay between them died for hours nothing noticed. Every step of discovery,
acknowledgement and liveness was done by hand.

Three shapes were weighed:

- **A new source in `activity_since`.** It lists conversation updated since a cursor. An
  unanswered request is exactly the one that does not change, so a read of what changed
  cannot find what is overdue.
- **A registry of projects and a routing service.** Larger than the problem: the
  intake label and repo already route, and each repo's layer can list where it files.
- **One read and one record on the request issue itself.** Chosen. The board is the
  record, both ends read the same answer, and no session has to stay alive for it.

# Decision

- A project's **intake** is its repo plus a label (`agent-proposed` by default). A
  request is an open issue there with the label. It stays `agent-proposed`: no agent
  builds it until a person says so.
- `intake_list` (read) returns the open requests with each one's latest **ack**, and
  flags `overdue` when there is none after `ack_within`. `intake_ack` (work) writes a
  signed ack record: `received`, `taken`, `parked` or `handed-back`. A repeated ack
  posts nothing, so a lane may repeat a tick.
- **The receiving end** runs an intake lane. Like every new lane it starts in `observe`
  (it reports "would ack" and changes nothing on the request) and goes `auto` only after a
  person reviews what it would have done. It speaks to the owner only when a new
  request needs their call. `taken` and `parked` record the owner's decision, with their
  words and a link, which is the work's mandate.
- **The filing end** tracks each request on its own item and checks for the ack each
  tick. An overdue request puts `needs:<owner>` on that item, so a dead path between the
  projects shows in the owner's "Needs a person" view instead of passing unseen.
- An ack is not consent and widens no lane: it records what a person, or a lane's `may`,
  already decided.

# Consequences

- A project discovers requests without a relay, and the filer sees the answer on the
  board, in the same place for every project.
- Liveness rests on the filer's own lane: if both ends' lanes are down, nothing flags.
  A person's "Needs a person" view still shows each overdue request once a lane resumes.
- A registry of who owns what, and refusing lab-internal requests on public repos, stay
  open; each repo's Intake section is the interim list.
- The optional Intake group, conformance I1 to I5, `board-lane` 0.5.0 (`intake.md`) and
  the template's Intake section carry it.
