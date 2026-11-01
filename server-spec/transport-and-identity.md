# 02. Transport and identity

## Endpoint and transport

- The server has one public base URL, `https://...`, with no path. Work repos store it as
  `mcp_url` in `.github/gtd-context.json`.
- MCP is served at `<mcp_url>/mcp` over the **Streamable HTTP** transport. The server
  SHOULD run it stateless (no session affinity, every request authenticated on its own) so
  it can scale to zero and run as several replicas.
- The join routes live under `<mcp_url>/join` ([agent-join](agent-join.md)). They are plain
  HTTP, not MCP.
- The server publishes OAuth protected resource metadata (RFC 9728) at
  `<mcp_url>/.well-known/oauth-protected-resource/mcp`, and answers an unauthenticated MCP
  request with `401` and a `WWW-Authenticate: Bearer resource_metadata="..."` header that
  points at it. That is what lets a hosted MCP connector discover how to sign in.
- Every tool declares an input schema and an **output schema**, and returns structured
  content that matches it. Agents read fields, not prose.
- A server SHOULD support the current MCP protocol revision and the one before it, and
  MUST answer `initialize` with the revision it chose.

## Three kinds of caller

All three arrive as `Authorization: Bearer <token>` on `/mcp`. The server tries the
verifiers in a fixed order and the first that recognises the token decides.

| Caller | How it signs in | Principal | Fenced by a preset |
| --- | --- | --- | --- |
| Hosted connector session (for example a claude.ai cloud thread) | OAuth through the identity provider the operator chose, discovered via RFC 9728 | `<idp>:<stable-id>`, for example `google:<email>` or `github:<login>` | No (MAY be) |
| Joined agent | Device-code join, then its own bearer token ([agent-join](agent-join.md)) | `agent:<name>` | **Yes** |
| Service agent | A signed token (JWT) whose issuer and audience the operator configures | `agent:<subject>` | MAY be |

Rules:

- A joined-agent token has a recognisable prefix so the server checks it against its own
  store first and never passes it to another verifier or identity provider.
- A connector sign-in MUST be gated by an operator allowlist of identities. Signing in with
  the identity provider alone grants nothing.
- The **principal** is the only identity the server uses. It is stamped on every record and
  log line. No tool takes a principal, author or `by` argument.
- `agent:` names are one namespace: the operator keeps joined names and service subjects
  distinct.

## Presets

A preset is a ceiling on which tools a joined agent may see and call. They are ordered:

`desk` < `read` < `work` < `full`

| Class | Meaning | Tools the kit relies on in this class |
| --- | --- | --- |
| `desk` | Identify yourself only (plus any coordination-desk tools a server offers) | `whoami` |
| `read` | Read repos, boards, profiles, claim state | `profile_get`, `profile_list`, `project_get`, `project_items`, `project_item_find`, `project_views_list`, `list_next_actions`, `issue_list`, `issue_blocked_by_list`, `item_get` |
| `work` | Change issues and boards, claim and report | `capture`, `issue_comment`, `issue_labels`, `item_claim`, `item_renew`, `item_release`, `item_report`, `project_set_status`, `project_set_field`, `project_item_move`, `project_add_item`, `project_report` |
| `full` | Anything else: board and view creation, field deletion, webhooks, repo variables, deletes | everything not listed above |

- Every tool belongs to exactly one class. A new tool defaults to `full` until someone
  classes it lower on purpose.
- A tool above the caller's preset is **hidden** from `tools/list` and, if called anyway,
  refused with an error that names the preset it needs.
- Fencing happens in one place (middleware), before the tool runs, never inside tools.

The full class table for every tool in [tools.md](tools.md) is in its "Class" column.

## whoami

Registered in every mode, class `desk`. Takes no arguments. Returns:

| Field | Type | Meaning |
| --- | --- | --- |
| `principal` | string | `agent:<name>`, `<idp>:<id>`, or null when unauthenticated (local stdio) |
| `signed_in_by` | string | `agent-join`, `signed-agent-token`, `<idp>` or `local` |
| `preset` | string | The caller's preset; `full` when not fenced |
| `fenced` | bool | Whether the preset fence applies to this caller |
| `provider` | string or null | The agent runtime the join declared (`claude`, `codex`, ...) |
| `expires_at` | int or null | Unix time the current access token ends |
| `join_url` | string or null | `<mcp_url>/join` when the join is switched on, else null |
| `conformance` | list of strings | The levels from the [README](README.md#conformance-levels) this server meets |
| `spec_version` | string | The kit version of this spec the server implements |

An agent calls `whoami` first in every session (BOARD.md rule 1), so it must be cheap and
must never fail for a valid token.

## Errors

- A tool refusal is an MCP tool result with `isError: true` and a one-line, actionable
  message: what was refused, why, and what to do instead (for example "held by
  agent:other until 2026-01-01T12:00:00Z" or "needs the work preset").
- A refusal never includes a token, a stack trace, or another caller's private data.
- `401` at the HTTP layer means "renew or sign in". It is not a revoke ([agent-join](agent-join.md)).
