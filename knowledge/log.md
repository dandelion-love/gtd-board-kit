# Update log

## 2026-11-01

* **Added**: per-repo customization (kit 0.10.0). `server-spec/` defines `overrides` (`skip` and `keep`) in `gtd-context.json`, a ledger of what a reconciler created from which declaration, item fingerprints in `profile_get`, and the upstream change notice that `profile_updates` returns when the profile changes an item a repo skipped or reshaped. Conformance gains O1 to O3; `board-onboard` surfaces the notices.
* **Added**: the spec and its checks change together (kit 0.9.0). `tests/check_kit.py` checks that every check id in `server-spec/conformance.md` is in the runner and back, and that the fold table matches its fixtures; `tools/spec_pair.py`, run by the `pre-push` hook, fails a branch that changes `server-spec/` without its checks unless a commit carries `Conformance-unchanged: <reason>`; a PR template asks for both.
* **Added**: the conformance runner drives the connector entrance (J11, JC1 to JC9) as an OAuth client with a loopback redirect; a person approves once in a browser (kit 0.8.0).
* **Changed**: one join, two entrances (kit 0.7.0). Agent sign-in starts with which entrance to use: the connector when the host keeps the sign-in, the device code when it keeps a file, and neither in an ephemeral container. It covers reconnecting the connector, a network policy that blocks the server, and whose name connector work goes under. `server-spec/agent-join.md` defines the connector entrance as a contract, `whoami` gains `entrance`, and conformance gains J11 and JC1 to JC9.
* **Added**: `conformance/`, a standard-library Python runner that checks any server against the spec's numbered checks over HTTP, with the claim-fold golden cases as JSON; the spec gains check T0 and fold cases i and j (kit 0.6.0).
* **Added**: `server-spec/`, an implementation-neutral specification of a compatible gtd MCP server, with conformance checks and a unit-by-unit work plan (kit 0.5.0). Onboarding now reads views with `project_views_list`, the read-only tool.
* **Added**: agent sign-in, the agent-side contract for joining the gtd MCP server, with flow diagrams.
* **Added**: the kit-as-interface decision and the queue and ETA pattern: native GitHub constructs carry the state, and a person's edit wins.
* **Added**: standing lanes and workflow grants (kit 0.4.0), and a reference on DeepSeek's dsh-superagent, which the lane design borrows from.

* **Added**: the kit's knowledge as an OKF 0.2 bundle, with the board model, the kit's design decisions, and the pinned OKF specification.
