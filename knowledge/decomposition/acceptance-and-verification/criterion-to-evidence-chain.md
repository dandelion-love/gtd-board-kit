---
type: Pattern
title: Criterion-to-evidence chain
description: Draft pattern for the kit; each numbered acceptance criterion in a story issue is answered by one evidence row in the agent's pull request, and a person's merge closes the chain.
tags: [acceptance-criteria, verification, traceability, pattern, draft]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: north-bdd, title: "Dan North, Introducing BDD (2006)", resource: "https://dannorth.net/blog/introducing-bdd/", url: "https://dannorth.net/blog/introducing-bdd/", accessed: 2026-11-02 }
  - { id: wynne-em, title: "Matt Wynne, Introducing Example Mapping (2015)", resource: "https://cucumber.io/blog/bdd/example-mapping-introduction/", url: "https://cucumber.io/blog/bdd/example-mapping-introduction/", accessed: 2026-11-02 }
  - { id: sp-vbc, title: "obra/superpowers, verification-before-completion SKILL.md", resource: "https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md", url: "https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md", accessed: 2026-11-02, version: "plugin 7.0.1" }
  - { id: impossiblebench, title: "ImpossibleBench (arXiv 2510.20270)", resource: "https://arxiv.org/abs/arXiv:2510.20270", url: "https://arxiv.org/abs/arXiv:2510.20270", accessed: 2026-11-02 }
  - { id: gh-protected, title: "GitHub Docs, About protected branches", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", url: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", accessed: 2026-11-02 }
  - { id: cc-best, title: "Claude Code docs, Best practices", resource: "https://code.claude.com/docs/en/best-practices", url: "https://code.claude.com/docs/en/best-practices", accessed: 2026-11-02 }
---

# The chain

```
criterion (issue, human-owned)
  -> check (named test / command / CI job / screenshot / reviewer step)
    -> evidence (fresh output on the final commit, in the PR body)
      -> gate (required checks ran + review)
        -> merge by a person = done
```

A link that is missing breaks the chain, and the PR is not ready.

# 1. In the story issue

```markdown
## Acceptance criteria
- [ ] AC1: When a title is empty, the form shows "Title is required" and does not save.
- [ ] AC2: A saved item appears at the top of the list within 1 s on the fixture data.
- [ ] AC3: The export file has one row per item, with the header `id,title,status`.

## Open questions
- (none) <- an open question means not ready for an agent
```

Rules:
- Numbered, one behaviour each, observable outcome
  ([heuristics](testable-criteria-heuristics.md)). Use rule-list lines by default;
  EARS or Gherkin when a trigger matters ([choosing a form](choosing-a-criteria-form.md)).
- At least one failure case.
- Numbers only where behaviour has a number ([SMART](smart-for-acceptance-criteria.md)).
- A person accepts the criteria before the agent starts. Open questions block, as red
  cards do in example mapping.[^wynne-em]

# 2. In the agent's PR body

```markdown
Closes #<issue>

## Evidence
| AC | Kind | Check | Result |
| --- | --- | --- | --- |
| AC1 | test | test_ac1_empty_title_rejected | pass (output below) |
| AC2 | test | test_ac2_new_item_on_top_under_1s | pass, 0.31 s |
| AC3 | command | `python export.py fixture.db \| head -2` | header and row shown below |

## Test changes
- none   <- or each changed test, fixture or check config with the reason

## Not done / found
- ...    <- out-of-scope findings captured as new items
```

Rules:
- One row per AC. Kind is one of `test`, `check`, `command`, `screenshot`, `review`.
- `review` means a person must look; the agent says what to look at.
- Output is from a fresh run on the final commit, quoted, not paraphrased.[^sp-vbc]
- The agent marks the PR ready only when every row is filled.

# 3. At the gate

- Required checks green **and actually ran**; a `skipped` required check still passes
  the rule.[^gh-protected]
- Reviewer reads the Evidence table against the issue's criteria, then the
  Test changes section, then the diff. A fresh reviewer that did not write the code is
  better than self-review.[^cc-best]
- A person merges. Merge, not "PR opened" and not "ready", is done.

# 4. When the chain cannot close

If a criterion and an existing test conflict, or a criterion cannot be met, the agent
stops and reports `blocked` with the conflict, instead of editing the test. An explicit
stop option cut cheating sharply for some models in ImpossibleBench.[^impossiblebench]

# Why this shape

- North: acceptance criteria should be executable.[^north-bdd] Where they cannot be
  automated, the chain still names a check (`review`, `screenshot`).
- "Requirements met" needs a line-by-line checklist; tests passing is not
  enough.[^sp-vbc] The Evidence table is that checklist, in public.
- Agents game tests ([evidence](agent-test-gaming-evidence.md)); the Test changes
  section and human-owned criteria put the risky part in front of the reviewer
  ([mitigations](test-gaming-mitigations.md)).

# Open questions

- Should an epic's acceptance be "all story ACs merged" or its own outcome check? This
  pattern covers stories only.
- Should the kit lint the PR body (every AC id present) in a check? That needs a workflow,
  which agents may not write; a person would have to add it.
- Is the `Kind` list complete (for example `manual-run`, `metric`)?
- Not tested on real work. Try it on a few stories before making it a standard.

# Related

- [Criterion traceability on GitHub](criterion-traceability-on-github.md)
- [Definition of Done for agent PRs](definition-of-done-for-agent-prs.md)
- [Verification before completion](verification-before-completion.md)
