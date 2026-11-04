# Conformance runner

A ready-to-run, implementation-agnostic check of a gtd MCP server against
[server-spec/conformance.md](../server-spec/conformance.md). It talks to the server only
over HTTP, the way an agent does, so it works whatever the server is written in.

It needs Python 3.10 or later and nothing else (standard library only).

## Quick start

```bash
# 1. Offline: the claim-fold (C13), ready-check (R1) and Kind-rule (K1) golden cases, against the references.
python3 conformance/runner.py

# 2. Unauthenticated: the 401 challenge and resource metadata (T1).
python3 conformance/runner.py --server https://gtd.example.com

# 3. Full run against a scratch repo and board.
export GTD_TOKEN=...      # a joined agent at the work preset
export GTD_TOKEN_B=...    # a second agent, for the race and non-holder checks
python3 conformance/runner.py --server https://gtd.example.com \
  --token-env GTD_TOKEN --token-b-env GTD_TOKEN_B \
  --repo owner/scratch-repo --project owner/number \
  --json conformance-report.json
```

Tokens are read from the environment variables you name, never from the command line, and
the runner never prints them. Check X1 fails if a token it sent comes back in any response.

## Certifying a server (for an agent)

A server claims a level only after a run like this has made it claimable
([spec version and levels](../server-spec/transport-and-identity.md#spec-version-and-levels)).
An agent asked to "run conformance" or "certify the server" does this, in order:

1. **Use the latest kit.** Fetch the kit's default branch (`git -C .gtd/kit fetch origin`
   then check out `origin/main` in a scratch copy, or clone the kit fresh). Do not move the
   repo's pin to do it. Note the kit's `VERSION`: that is the version being certified.
2. **Run every check you can**, with `--json`: a token at `work`, a second principal, a
   scratch repo and board, `--join-start`, and `--connector NAME` if the server offers the
   connector entrance. A skipped check, or one the run never reached because an option was missing, keeps its level unclaimable; a check of an optional part the server does not offer is `n/a` and does not.
3. **Do the manual checks with your person.** The run prints them under each claimable
   level ("confirm by hand"). Never mark one done yourself.
4. **Read the verdict.** The last line names the levels claimable at this kit version.
   Nothing claimable: report the failures and stop.
5. **Propose the claim**, in the server's own repository, as a change a person merges:
   set the server's spec version to the kit `VERSION` you ran and its recorded levels to
   the claimable ones (minus any whose manual checks your person did not confirm), with
   the JSON report attached or linked. Never claim a level the run did not make
   claimable, and never edit the report.
6. **After the deploy, re-run** without the sandbox options: T8 shows the new version and
   levels, and T9 confirms the claim is honest.

## What a run needs, and what it touches

| Option | Unlocks | Side effects |
| --- | --- | --- |
| none | C13, R1, K1 | none |
| `--server` | T1, T8, T9 (from the well-known document's levels); J2 and J3 skip unless the server claims Join | none |
| `--token-env` | T0, T2, T3, T5, T7, T8 compared with `whoami`, J10, P1 to P3, P8, P9, X1 | none (reads only) |
| `--preset-token PRESET=ENV` (repeat) | T6, X2 for each preset you pass | none |
| `--repo owner/repo` | P4 to P6, C1, C2, C5 to C9, C11, C14 to C17, X3; R2 to R8 when `item_ready` is offered; K2 to K4 when `sub_issue_add` or `issue_type_set` is offered (K3 and K4 need the Issue Types `Epic`, `Story`, `Chore`, `Spike` and `Finding` on the repo's owner) | **creates issues** titled `[conformance <run>] ...`, adds labels and comments, claims and releases them; for R5 and R7, links one issue as another's blocker, tries the reverse link (GitHub normally refuses the cycle) and closes one, when `issue_blocked_by_add` and `issue_close` are offered; for K3 and K4, sets Issue Types and links sub-issues |
| `--token-b-env` | C2, C3, C6 with a second principal | as above |
| `--project owner/number` | P7, B1 to B4, C12, and the Size part of C5 | adds the sandbox issues to the board and writes fields on them |
| `--pr-head BRANCH` | PR3, when the server offers `pr_open` (PR1 and PR2 need only `--repo`) | **opens one pull request** from that branch, already pushed to the sandbox repo; close it by hand afterwards |
| `--join-start` | J2 and J3 with a real request | opens one join request; it expires unapproved after ten minutes |
| `--connector NAME` | JC1 to JC9, when `/join` lists the connector entrance | registers two OAuth clients with a loopback redirect, joins agent `NAME` at `desk` after a person approves it in a browser, and revokes it at the end when the server advertises `revocation_endpoint` (otherwise revoke it at `/join/agents`) |
| `--fold-cmd CMD` | C13 against **your** fold instead of the reference | runs `CMD` locally |
| `--ready-cmd CMD` | R1 against **your** ready check; without `--server`, R1 runs against the reference | runs `CMD` locally |
| `--kind-cmd CMD` | K1 against **your** Kind rules; without `--server`, K1 runs against the reference | runs `CMD` locally |

Use a **scratch repo and board** that nothing else watches. The runner lists the issues it
made at the end; close or delete them afterwards.

The repo token must be at the `work` preset or higher, because the claim checks write.
`--profile` names the sandbox repo's profile when the runner should not take the first
one `profile_list` returns.

## The connector entrance

With `--connector NAME` the runner acts as an OAuth client: it registers with a loopback
redirect, opens `/authorize` with PKCE and `resource=<server>/mcp?agent=NAME`, checks
that it lands on `/join/approve?connect=...`, and prints that link. **A person opens it,
signs in as an approver, chooses to sign in as an agent, and approves at preset `desk`.**
The runner catches the redirect on localhost (it waits `--connector-wait` seconds, 600 by
default), then redeems the code, calls `whoami`, races two refreshes and checks the client
binding without further help. Run it on the machine whose browser does the approval.

## Reading the result

Each check id prints one line: `pass`, `FAIL` with the reason, `skip` with what it needs,
or `manual` with the steps a person takes. Manual checks (T4, C4, C6b, C10, J1, J4 to J9,
and parts of JC2, JC3 and JC5 to JC9) need a person, a second account or a wait the runner should not take; run them by hand
from their description.

A server meets a level when every check of that level and the levels below it passes,
manual ones included. The runner prints the levels the server claims in `whoami` (T5) and
at `/.well-known/gtd-board-kit` (T8), and T9 fails when a claimed level, or Core beneath it,
has a failing check in the same run. Checks a run skipped or left manual do not count
against T9, so a full claim still needs the manual ones.

Exit code: `0` when nothing failed, `1` when a check failed, `2` when the server could not
be reached or the arguments were wrong. `--json FILE` writes the same rows for CI.

## Testing your fold offline

C13 feeds each case in [fold_cases.json](fold_cases.json) to a command on stdin and reads
JSON from its stdout:

```json
{"now": "2026-01-01T03:20:00Z",
 "comments": [{"id": 1, "body": "<!-- gtd-desk v1 {...} -->"}, {"id": 2, "body": "plain text"}]}
```

The command answers with at least `holder`, `lease_until`, `stale`, `last_report`,
`handoff_to` and `lost_claims` (a count), plus `attention_by` where a case expects it. Wrap
your server's fold in a few lines of glue and pass it as `--fold-cmd "python3 my_fold.py"`.
The runner's own `reference_fold` is a readable statement of the rules in
[claim-records](../server-spec/claim-records.md).

## Testing your ready check offline

R1 feeds each case in [ready_cases.json](ready_cases.json) to a command on stdin, with the
case's letters already turned into issue numbers:

```json
{"repo": "owner/repo", "number": N, "body": "## Acceptance criteria\n\n- AC1 ...",
 "labels": [], "board": true, "size": "S", "pickup_sizes": ["XS", "S", "M"],
 "blocked_by": ["owner/repo#M"],
 "issues": {"owner/repo#M": {"state": "open", "blocked_by": []}}}
```

The command answers with `verdict`, `missing` (rule names, or `{rule, detail}` objects) and
`blockers` (`owner/repo#N` of the open ones). The runner's `reference_ready` is a readable
statement of the rules in [ready check](../server-spec/ready-check.md). If the server
offers `item_ready` and you give no `--ready-cmd`, R1 is listed as manual.

## Testing your Kind rules offline

K1 feeds each case in [kind_cases.json](kind_cases.json) to a command on stdin. A link case
asks whether `parent` may hold `child`; a type case asks whether an issue with that
`parent` and those `children` may take `kind` (null clears the type). Each Kind is an Issue
Type name or a `kind:` label value, any case, or null for none. In a type case `parent` is
null when the issue has no parent and `""` when its parent has no Kind:

```json
{"op": "link", "parent": "Epic", "child": "Story"}
{"op": "type", "kind": "Finding", "parent": "Epic", "children": [null]}
```

The command answers `{"allowed": true|false, "rule": null|"<rule>"}`, with the first rule
broken in the order `retired-kind`, then the issue as a child, then each sub-issue in
order. The runner's `kind_link_rule` and `kind_type_rule` are a readable statement of the
[parent rules](../server-spec/repo-context-and-profiles.md#kinds). If the server offers the
Issue structure tools and you give no `--kind-cmd`, K1 is listed as manual.

## Limits

- It is black-box. It cannot see your logs (X1 covers response bodies only) or whether a
  refused call reached GitHub (P5 checks the refusal only).
- Optional tool groups are not checked beyond their class (X2), except Customization (O1 to O3) and Readiness (R1 to R8) and the Kind and parent rules (K1 to K4).
- A server's own tools, outside the spec, are checked by the class they declare in `_meta` `gtd-board-kit/class`, else as `full` (X2).
- P6 and C8 re-read a label-filtered list, and B3 the board's order, for up to 30 seconds after a write, because those reads can lag.
- It does not clean up after itself; it never deletes issues, and closes only the one R7 makes.
