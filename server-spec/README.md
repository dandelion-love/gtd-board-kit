# Building a compatible gtd MCP server

The rest of the kit is written for **agents**: it says what an agent may rely on when it
works a board through "the gtd MCP server". This folder is written for **whoever builds
that server**. It specifies, without naming any deployment, what a server must do so that
the kit's skills, `BOARD.md` and the join client work against it unchanged.

It is a contract, not a design. Hosting, language, storage engine and identity provider are
the builder's choice. Where a choice affects interoperability (a record format, a wire
shape, a fold rule) the spec fixes it; everywhere else it says MUST / SHOULD / MAY in the
sense of RFC 2119 and leaves the how open.

## Reading order

| File | What it fixes |
| --- | --- |
| [architecture.md](architecture.md) | The parts, the roles, where state lives, the trust boundaries |
| [transport-and-identity.md](transport-and-identity.md) | MCP transport, the three kinds of caller, principals, presets, `whoami` |
| [agent-join.md](agent-join.md) | The server side of the device-code join, renew and revoke |
| [repo-context-and-profiles.md](repo-context-and-profiles.md) | `.github/gtd-context.json`, profiles, the label families, the label-to-Status map |
| [claim-records.md](claim-records.md) | The record format on issues and the fold that turns records into claim state |
| [tools.md](tools.md) | Every tool the kit calls: arguments, results, refusals, preset class, side effects |
| [security.md](security.md) | The rules that hold whatever the deployment |
| [conformance.md](conformance.md) | Numbered checks a server must pass, and how to run them |
| [work-plan.md](work-plan.md) | The same spec cut into work units a coding agent can plan and build one at a time |
| [ready-check.md](ready-check.md) | The read-only ready check: its verdicts and the five rules every server applies the same way |
| [record-pages.md](record-pages.md) | Record pages: one addendum-only Markdown page per register item, the rule, the merge, and how a server reads and writes them |
| [typed-links.md](typed-links.md) | Typed links between items: the record, the kinds and their native forms, the fold, the Related section, the graph render |
| [sign-offs.md](sign-offs.md) | The sign-off the server ends every write with: who, in which role, which act, which session |
| [notifications.md](notifications.md) | Who an ask pings, under which identity, once: the map, `notify_get`, the ping comment, review requests, the push copy |

The agent-side halves live elsewhere in the kit and are normative here too:
[agent sign-in](../knowledge/model/agent-sign-in.md) (the join wire shape),
[claims and leases](../knowledge/model/claims-and-leases.md),
[report vocabulary](../knowledge/model/report-vocabulary.md),
[labels are signals](../knowledge/model/labels-are-signals.md) and
[queue and ETA](../knowledge/model/queue-and-eta.md).

## Conformance levels

| Level | A server at this level | Kit skills that work |
| --- | --- | --- |
| **Core** | Transport, identity, presets, `whoami`, repo and board reads, issue labels and comments, the claim tools, sign-offs | `board-pickup`, `board-claim`, `board-report`, `board-needs-person`, `board-lane` (with a bridge in the repo) |
| **Join** | Core, plus the device-code join on its own routes, and optionally the connector entrance | Everything above, for agents with their own `agent:<name>` identity, whatever the host |
| **Board** | Core, plus board writes (Status, fields, card order, drafts) | Everything, in repos without a label bridge too |
| **Extended** | Any of the optional tool groups in [tools.md](tools.md#optional-groups) | Repo-specific procedures in `.gtd/BOARD.local.md` that name them |

A server says which levels it meets, and which spec version it implements, in `whoami` and
at `<mcp_url>/.well-known/gtd-board-kit`, and claims only levels whose checks it passes
([spec version and levels](transport-and-identity.md#spec-version-and-levels)). An agent
runs a kit skill only when the server claims that skill's level
([server version and levels](../knowledge/model/server-version.md)).

## Versioning

This spec carries the kit's `VERSION`. A change that would break an existing conforming
server or an existing agent is a minor bump before 1.0 and a major bump after, and lands
with a line in [the knowledge log](../knowledge/log.md).

**The spec and its checks change together.** A PR that changes a requirement here also
changes its checks in [conformance](conformance.md) and the
[runner](../conformance/README.md), in the same PR. `tests/check_kit.py` fails when a check
id is in the table but not in the runner, or the other way round, and
`tools/spec_pair.py` fails a branch that changes `server-spec/` without changing both the
check table and the runner (or the table without the runner), unless a commit says
`Conformance-unchanged: <reason>`.

## What is deliberately not here

Any deployment's address, accounts, organisation, board numbers, App or installation
numbers, allowlists, people or emergency procedures. A deployment documents those in its
own private repo. Examples in this folder use placeholders: `owner/repo`, `owner/number`,
`https://gtd.example.com`.
