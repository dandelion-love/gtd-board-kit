---
type: Pattern
title: Milestone handoff
description: A worker hands a milestone to a reviewer, and the reviewer back, as a compact packet naming an immutable revision and one next action; delivery, the verdict and completion are kept apart, and a verdict counts only for the revision it names.
tags: [board, handoff, review, claims]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-21T21:00:00Z }
---

# Rule

Some work needs an independent look before it goes on: a plan review, a work review, a
question only another session can answer. A **milestone handoff** is the record that says
what to look at, which revision of it, what to do, and who is asked. It is optional: a
server may not offer it ([negotiation](/model/milestone-handoff.md#negotiation)), and work goes on
without it.

- **It is not a release.** You keep your claim. A release lets go of the whole item; a
  handoff asks someone about one milestone of it.
- **The evidence is a fixed revision.** A commit or a digest, never a branch name. New
  evidence is a new handoff that supersedes the old one.
- **One ask.** The packet names one concrete action: `review-plan`, `review-work`,
  `address-findings`, `answer-question` or `continue-work`.
- **Three separate things.** *Delivery* (did the session get it, did it acknowledge it),
  the *verdict* (what the reviewer decided about a revision) and *completion* (is the item
  done) never stand for each other. A delivered handoff authorizes nothing.
- **A verdict names its milestone and revision.** It counts only if that revision is still
  the milestone's current one when it is acted on. Accepting an old revision never
  authorizes a newer one.
- **A claim is still needed.** The reviewer claims the item with `purpose` `review` before
  reviewing; a session never reviews its own work; a comment or a role name grants nothing.

# The packet

```text
Handoff packet
milestone: parser-work
revision: <the 40-hex commit>
evidence: <the PR link>, <the run link>
ask: review-work. Check the acceptance criteria against this revision and reply with a
verdict that names this milestone and revision.
meanwhile: continuing the independent story <link>.
```

At most 1200 characters; links, not pasted logs.

# Negotiation

Read `capabilities` in `whoami`. `milestone-handoff:1` with its tools is a **poll** server:
send with `handoff_send`; the recipient finds it with `handoff_list`. Add
`milestone-handoff-push:1` and the server also delivers to a session the recipient bound
with `handoff_bind`. Without the name, or with a tool missing, hand over **manually**: post
the packet as a signed comment, link it from a report, and tell your person delivery is
manual. Never say a release or a comment will wake a session.

# Why

Today a recorded handoff cannot tell delivery from acknowledgement from acceptance of a
particular revision, and a reviewer's "looks ready" can outlive the code it looked at. The
revision and the head close that gap without a second status system. The contract is
[server-spec/milestone-handoff.md](../../server-spec/milestone-handoff.md).
