# Acceptance and verification

* [Agent test-gaming evidence](agent-test-gaming-evidence.md) - Published evidence that coding agents edit tests, special-case expected values or patch the grader to pass, and that passing tests often over-state correctness
* [Choosing a criteria form](choosing-a-criteria-form.md) - Rule list, Gherkin scenario, EARS line or example table; which form of acceptance criterion fits which kind of work item
* [Criterion-to-evidence chain](criterion-to-evidence-chain.md) - Draft pattern for the kit; each numbered acceptance criterion in a story issue is answered by one evidence row in the agent's pull request, and a person's merge closes the chain
* [Criterion traceability on GitHub](criterion-traceability-on-github.md) - A light requirement-to-test matrix built from what GitHub already has, linking each acceptance criterion to the check or evidence that proves it
* [Definition of Done for agent PRs](definition-of-done-for-agent-prs.md) - What "done" means when an agent returns work as a pull request; opened, ready and merged are different states, and only a person's merge completes the item
* [EARS notation](ears-notation.md) - EARS is a small set of keyword templates (While, When, Where, If/Then, plus a plain "shall") for writing natural-language requirements with less ambiguity
* [Example mapping](example-mapping.md) - A short card-based conversation that splits a story into rules, examples and open questions before it is built, and tells you when a story is too big or too unclear
* [Gherkin and Given/When/Then](gherkin-given-when-then.md) - Given/When/Then is a scenario template from BDD for writing executable acceptance criteria; Gherkin is Cucumber's formal grammar for it
* [SMART for acceptance criteria](smart-for-acceptance-criteria.md) - SMART began as a test for management objectives and was applied to agile tasks by Bill Wake; for acceptance criteria only the Specific and Measurable letters do real work
* [Specification by Example](specification-by-example.md) - Gojko Adzic's name for the practice of agreeing requirements through concrete key examples that are then automated as checks and kept as living documentation
* [Test-gaming mitigations](test-gaming-mitigations.md) - Measures that make an agent's green checks mean more; human-owned criteria, protected or held-out tests, an honest way to stop, diff review of test changes, and mutation testing
* [Testable criteria heuristics](testable-criteria-heuristics.md) - Checks and anti-patterns for writing acceptance criteria that a test, a command or a reviewer can decide as pass or fail
* [Verification before completion](verification-before-completion.md) - Evidence before claims; an agent may say work passes or is done only after running the proving command fresh and reading its full output
