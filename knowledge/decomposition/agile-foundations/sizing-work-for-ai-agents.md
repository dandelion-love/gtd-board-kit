---
type: Concept
title: Sizing work when the builder is an AI agent
description: For agent-built work the useful size limits are reliability at task length, one reviewable pull request, and a checkable done condition; raw context-window size has stopped being the binding limit.
tags: [sizing, ai-agents, pull-requests, code-review, context, metr]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T03:55:45Z }
sources:
  - id: metr-horizon
    title: "Kwa, West, Becker et al. (METR): Measuring AI Ability to Complete Long Software Tasks, arXiv:2503.14499v3 (2026-02-25)"
    resource: https://metr.org/
    accessed: 2026-11-02
  - id: metr-rct
    title: "METR: Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity (2025-07-10)"
    resource: https://metr.org/
    accessed: 2026-11-02
  - id: chroma-rot
    title: "Hong, Troynikov, Huber (Chroma): Context Rot (2025-07-14)"
    resource: https://www.trychroma.com/research/context-rot
    accessed: 2026-11-02
  - id: anthropic-context
    title: "Anthropic: Effective context engineering for AI agents (2025-09-29)"
    resource: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    accessed: 2026-11-02
  - id: cc-bp
    title: "Claude Code docs: Best practices"
    resource: https://code.claude.com/docs/en/best-practices
    accessed: 2026-11-02
  - id: codex-bp
    title: "OpenAI Codex: Best practices"
    resource: https://developers.openai.com/codex/learn/best-practices.md
    accessed: 2026-11-02
  - id: copilot-bp
    title: "GitHub Docs: Best practices for using GitHub Copilot to work on tasks"
    resource: https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results
    accessed: 2026-11-02
  - id: google-cl
    title: "Google Engineering Practices: Small CLs"
    resource: https://google.github.io/eng-practices/review/developer/small-cls.html
    accessed: 2026-11-02
  - id: sadowski
    title: "Sadowski et al.: Modern Code Review, a Case Study at Google (ICSE SEIP 2018), research.google publication page with PDF"
    resource: https://research.google/pubs/modern-code-review-a-case-study-at-google/
    accessed: 2026-11-02
  - id: kudrjavets
    title: "Kudrjavets, Nagappan, Rastogi: Do Small Code Changes Merge Faster? (MSR 2022, arXiv:2203.05045)"
    resource: https://arxiv.org/
    accessed: 2026-11-02
  - id: scrum-guide
    title: The 2020 Scrum Guide
    resource: https://scrumguides.org/scrum-guide.html
    accessed: 2026-11-02
  - id: jeffries-points
    title: "Ron Jeffries: Story Points Revisited (2019)"
    resource: https://ronjeffries.com/
    accessed: 2026-11-02
---

# The question

Story points sized work for a human team's sprint. When the builder is an agent and the
reviewer is one person, the costs move: building is cheap, while **review time and
wrong-direction work** cost the most. What should "small enough" mean?

# What the evidence says

## 1. Agent reliability falls with task length

- METR measures the "50% time horizon": "the time humans typically take to complete
  tasks that AI models can complete with 50% success rate." It "has doubled approximately
  every seven months since 2019" (fit: 207 days).[^metr-horizon]
- At 80% success, horizons are "4-6x shorter" than at 50%.[^metr-horizon]
- Performance is "much lower on less structured, 'messier' tasks", and "realistic tasks
  rarely have automatic scoring."[^metr-horizon]

**Implication:** size for the reliability you need, not the best case. A task near an
agent's 50% horizon fails half the time. Unattended work should sit well inside the 80%
horizon, and a messy, ill-specified task behaves like a longer one.

## 2. Context is a quality limit more than a hard limit

- Chroma tested 18 models: performance "grows increasingly unreliable as input length
  grows", even on simple tasks; models "do not use their context uniformly."[^chroma-rot]
- Anthropic names this context rot and an "attention budget": "Every new token introduced
  depletes this budget by some amount." Remedies: compaction, structured notes outside
  the window, and sub-agents "with clean context windows."[^anthropic-context]
- But Claude Code's current docs retire "the context window is your main constraint" as
  old advice: most current models have a 1M-token window and compaction is automatic, so
  "running out is rare". `/clear` between tasks still helps "because a focused context
  gets you better answers and costs less."[^cc-bp]
- OpenAI: "Keep one thread per coherent unit of work"; one thread per project "leads to
  bloated context and worse results over time."[^codex-bp]

**Implication:** "fits in the context window" is no longer a useful size rule. **"One
coherent unit per session"** is.

## 3. The human review is the bottleneck, and small changes review faster

- Google's guide: aim for "one self-contained change"; "100 lines is usually a reasonable
  size for a CL, and 1000 lines is usually too large." Small CLs are "reviewed more
  quickly", less buggy, easier to merge and roll back. Tests ship with the change.[^google-cl]
- Google data: median change 24 lines modified; median first feedback "under an hour" for
  small changes versus "about 5 hours" for very large ones.[^sadowski]
- Counter-evidence: on 826,259 GitHub PRs, "pull request size and composition do not
  relate to time-to-merge" (weak correlation, r = 0.26). The authors point to social and CI
  factors.[^kudrjavets]

**Implication:** small PRs reliably make each review *easier*; they do not by themselves
make merges *faster* on GitHub. A solo owner's attention is the queue, so the review-effort
argument is the one that counts.

## 4. Vendors ask for scoped tasks with a done condition

- GitHub: give "clear, well-scoped tasks" with "complete acceptance criteria" and file
  hints. Keep for humans: "broad-scoped, context-rich refactoring", production-critical
  and security work, and "tasks lacking clear definition."[^copilot-bp]
- OpenAI: a "Done when:" line helps Codex "stay scoped, make fewer assumptions, and
  produce work that's easier to review."[^codex-bp]
- Anthropic, for unattended runs: does it know what done looks like, can it check its own
  work, what may it touch, what stops it, and who signs off.[^cc-bp] Its `/batch` command
  splits one big mechanical change into "5 to 30 units", one worktree and one PR
  each.[^cc-bp]

## 5. Perceived speed is not measured speed

In METR's 2025 trial, 16 experienced developers took 19% longer on 246 real issues with
AI allowed, while believing it sped them up by about 20%. METR has since marked these
results outdated.[^metr-rct] The lasting point: **measure cycle time, do not trust
impressions.**

# A size rule for agent-built stories (synthesis)

A story is small enough for an agent when **all** hold:

| Test | Rule | Grounding |
| --- | --- | --- |
| One PR | It lands as one self-contained PR, with its tests | Google small CLs[^google-cl] |
| Reviewable in one sitting | The owner can review it in one pass (as a starting rule, a few hundred changed lines at most, excluding generated files) | Google size guidance[^google-cl] |
| Checkable | It has a "Done when" condition and a command or test that proves it | OpenAI, Anthropic, GitHub[^codex-bp][^cc-bp][^copilot-bp] |
| One session | One coherent unit of work, no unrelated tasks in the same session | OpenAI, Anthropic[^codex-bp][^cc-bp] |
| Inside the reliable horizon | Well short of the length where the chosen agent fails often; shrink further when the spec is vague | METR[^metr-horizon] |
| Single acceptance focus | Close to Jeffries' "single acceptance test" | Jeffries[^jeffries-points] |

If any test fails, [split the story](story-splitting-patterns.md). This replaces points
with a binary "fits / split it" rule, and lets flow metrics (see
[story points and estimation critiques](story-points-and-estimation-critiques.md)) do the
forecasting.

The Scrum Guide's "one Sprint" test for a PBI and "one day or less" hint for work items
still frame the story and task levels; agent work simply lands far below them in
wall-clock time.[^scrum-guide]

# Story versus PR

A story can need more than one PR (a migration first, then the behaviour). Allowed, as
long as each PR is self-contained and the story stays one user-visible outcome. Google
even allows horizontal PR splits with stubs.[^google-cl] Layer splitting is fine for
**PRs**; it is not fine for **stories**.

# Open questions

- Some sources are cited by their site's front page (the paper or post is named in the
  title), because their dated or numbered URLs trip the public repo's guard.
- No public study yet measures **review time per agent-written PR** by size. The size
  thresholds above are borrowed from human code review.
- METR horizons move fast and depend on the task set; do not hard-code a number of
  minutes into a standard. Pin a rule ("one PR, one check") and let the owner tune it.
- Whether a "few hundred lines" cap holds for agent PRs, where the code is uniform and
  tests are large, is untested.

[^metr-horizon]: Kwa, West, Becker et al. (METR): Measuring AI Ability to Complete Long Software Tasks, arXiv:2503.14499v3 (2026-02-25), <https://metr.org/>
[^chroma-rot]: Hong, Troynikov, Huber (Chroma): Context Rot (2025-07-14), <https://www.trychroma.com/research/context-rot>
[^anthropic-context]: Anthropic: Effective context engineering for AI agents (2025-09-29), <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
[^cc-bp]: Claude Code docs: Best practices, <https://code.claude.com/docs/en/best-practices>
[^codex-bp]: OpenAI Codex: Best practices, <https://developers.openai.com/codex/learn/best-practices.md>
[^google-cl]: Google Engineering Practices: Small CLs, <https://google.github.io/eng-practices/review/developer/small-cls.html>
[^sadowski]: Sadowski et al.: Modern Code Review, a Case Study at Google (ICSE SEIP 2018), research.google publication page with PDF, <https://research.google/pubs/modern-code-review-a-case-study-at-google/>
[^kudrjavets]: Kudrjavets, Nagappan, Rastogi: Do Small Code Changes Merge Faster? (MSR 2022, arXiv:2203.05045), <https://arxiv.org/>
[^copilot-bp]: GitHub Docs: Best practices for using GitHub Copilot to work on tasks, <https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results>
[^metr-rct]: METR: Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity (2025-07-10), <https://metr.org/>
[^jeffries-points]: Ron Jeffries: Story Points Revisited (2019), <https://ronjeffries.com/>
[^scrum-guide]: The 2020 Scrum Guide, <https://scrumguides.org/scrum-guide.html>
