---
type: Practice
title: Specification by Example
description: Gojko Adzic's name for the practice of agreeing requirements through concrete key examples that are then automated as checks and kept as living documentation.
tags: [acceptance-criteria, examples, living-documentation]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: sbe-book, title: "Gojko Adzic, Specification by Example (Manning, 2011), table of contents", resource: "ISBN 978-1-61729-008-4 (TOC read on the O'Reilly Learning listing)", url: "https://books.apple.com/us/book/specification-by-example/id1572387893", accessed: 2026-11-02 }
---

# What it is

A book (Manning, June 2011) and a practice. Its seven key process patterns are the
chapter titles of Part 2:[^sbe-book]

1. Deriving scope from goals
2. Specifying collaboratively
3. Illustrating using examples
4. Refining the specification
5. Automating validation without changing specifications
6. Validating frequently
7. Evolving a documentation system

# The idea in one line

Abstract criteria are refined into a few **key examples** (concrete inputs and
outputs); those examples become automated checks run often, and the set becomes the
living documentation.

# Why it matters for agent work

- Pattern 1 puts the goal before the scope. An agent given only a solution to build
  cannot tell if the goal was met.
- Pattern 5 says the automated check must not rewrite the agreed specification. This
  is the human-owned-criteria rule in
  [test-gaming mitigations](test-gaming-mitigations.md), stated a decade earlier.
- Concrete examples are harder to satisfy by accident than prose.

# When it fits

Business rules with values (prices, limits, dates, permissions). Less useful for pure
refactors or docs work.

# Caveats

Only the table of contents was verified here; the summary above is a reading of the
chapter titles plus common knowledge of the book, not a quote.

# Related

- [Example mapping](example-mapping.md): a workshop that produces the key examples.
- [Gherkin and Given/When/Then](gherkin-given-when-then.md): one common way to write them.
