---
type: Practice
title: Testable criteria heuristics
description: Checks and anti-patterns for writing acceptance criteria that a test, a command or a reviewer can decide as pass or fail.
tags: [acceptance-criteria, quality, anti-patterns]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: spec-incose, title: "SPEC Innovations, How to write good requirements (summary of INCOSE Guide to Writing Requirements rules)", resource: "https://specinnovations.com/blog/how-to-ensure-requirements-are-clear-and-unambiguous", url: "https://specinnovations.com/blog/how-to-ensure-requirements-are-clear-and-unambiguous", accessed: 2026-11-02 }
  - { id: gherkin-ref, title: "Gherkin reference (Cucumber docs)", resource: "https://cucumber.io/docs/gherkin/reference/", url: "https://cucumber.io/docs/gherkin/reference/", accessed: 2026-11-02 }
  - { id: better-gherkin, title: "Writing better Gherkin (Cucumber docs)", resource: "https://cucumber.io/docs/bdd/better-gherkin/", url: "https://cucumber.io/docs/bdd/better-gherkin/", accessed: 2026-11-02 }
  - { id: swebv, title: "OpenAI, Introducing SWE-bench Verified (2024-08-13)", resource: "https://openai.com/index/introducing-swe-bench-verified/", url: "https://openai.com/index/introducing-swe-bench-verified/", accessed: 2026-11-02 }
---

# The test for a good criterion

Someone who did not write it can decide pass or fail from the criterion plus the PR,
without asking the author.

# Checks

| Check | Pass looks like |
| --- | --- |
| Observable | the outcome is seen from outside: output, message, file, status[^gherkin-ref] |
| One behaviour | no "and" joining two outcomes |
| Concrete | values with units, named inputs |
| Covers failure | at least one error or rejection case |
| What, not how | survives a change of implementation[^better-gherkin] |
| Decidable by a named check | a test, a command, a CI job, or a reviewer step |

# Anti-patterns

| Anti-pattern | Example | Fix |
| --- | --- | --- |
| Vague words | "fast", "user-friendly", "efficient", "appropriate", "usually"[^spec-incose] | a number, or an observable state |
| Escape clauses | "where possible", "as required", "if necessary"[^spec-incose] | state the condition, or drop it |
| Compound criterion | "exports CSV and emails it" | two lines |
| Implementation prescription | "use a Redis cache" | "second identical request returns in under 50 ms"; prescribe only when the interface is the requirement |
| Unstated detail the check needs | test expects an exact warning text the issue never mentioned | put the detail in the criterion, or loosen the check |
| Intent, not outcome | "the user understands the error" | "the error names the missing field" |
| Database-level `Then` | "a row exists in users" | what the user or caller sees[^gherkin-ref] |

The "unstated detail" row comes from SWE-bench Verified: annotators flagged 61.1% of
sampled tasks for tests that could reject valid solutions, for example a test needing a
deprecation message the issue never mentioned, and 38.3% for underspecified
issues.[^swebv] A criterion and its check must say the same thing.

# Caveats

The vague-word list is a secondary summary of the INCOSE Guide to Writing Requirements;
the guide itself was not read (it is not freely available).

# Related

- [SMART for acceptance criteria](smart-for-acceptance-criteria.md)
- [Agent test-gaming evidence](agent-test-gaming-evidence.md)
- [Criterion traceability on GitHub](criterion-traceability-on-github.md)
