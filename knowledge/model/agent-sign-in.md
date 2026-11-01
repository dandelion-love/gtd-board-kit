---
type: Pattern
title: Agent sign-in
description: How an agent outside claude.ai gets and keeps access to the gtd MCP server; a person approves a device-code join, the agent holds a 24-hour access token and a single-use refresh token, and revoked means join again.
tags: [auth, mcp, onboarding]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T06:40:00Z }
---

# Contract

This is the agent's side of signing in to the gtd MCP server. It is the interface: the
server behind it can change, and these rules hold.

- **Find the server in the repo.** The address is `mcp_url` in the work repo's
  `.github/gtd-context.json`: the server's base URL, https, no path. MCP itself is at
  `<mcp_url>/mcp` and the join pages under `<mcp_url>/join`. Never hard-code it and never
  guess it; if it is missing, ask your person.
- **claude.ai cloud threads do not join.** They reach the server through their gtd
  connector. Call `whoami`; if the connector is missing or its sign-in expired, ask your
  person to connect or reconnect it.
- **Everyone else joins with a device code.** Read `<mcp_url>/join` (plain-text steps,
  always current for that server) and run the join client it serves at
  `<mcp_url>/join/client.py` (Python 3.9+, standard library only):

  ```
  python gtd_join.py --server <mcp_url> --name <short-name> --provider <claude|codex|...> --preset read
  ```

  The name is 3 to 40 characters: lowercase letters, digits and inner hyphens. The
  preset defaults to `read`.

  It prints a link and a short code. The code is not a secret: show both to your person.
  They sign in with GitHub, check the code and the details, pick the preset and approve.
  The client waits and stops when they approve or deny, or when the request expires
  (about ten minutes).
- **A person approves every agent.** An agent can never approve itself or another agent.
- **Ask for the smallest preset**: `desk` < `read` < `work` < `full`. Writing to a board
  needs `work`. A tool above your preset is hidden, and a call to it is refused with the
  preset it needs.
- **Your identity is `agent:<name>`.** The server stamps it on every claim, report and
  log line; `whoami` shows it with your preset.

# Credential

| Part | Lasts | Rule |
| --- | --- | --- |
| Access token | 24 hours | Sent as a bearer token on every MCP call |
| Refresh token | 7 days if unused | **Single use.** Each renew returns a new pair. Using one twice revokes you |
| Approval | 30 days by default | Renewing never extends it. After that, join again |

- The client saves the pair to a file only your user can read, under
  `~/.gtd/agents/<name>.token`, and prints MCP client config that points at it. Neither
  the config nor the output of the join contains the credential.
- The client renews for you, shortly before the access token expires, one renew at a
  time. MCP clients get the header from it: `--headers` for a headers helper (Claude
  Code), `--token` for a bearer-token variable (Codex). Their output **is** the
  credential, so only an MCP client or a shell assignment runs them, never an agent in a
  chat.
- One credential, one place. Never copy the token file to another machine or share it
  between agents: a second copy renewing the same refresh token revokes the whole agent.
  Join each machine under its own name. The client takes a lock file next to the token
  file so that two MCP connections on one machine never renew at once.
- Never print, paste, log or commit the credential, never ask your person to paste one,
  and never run a renew yourself alongside the client.

# Revoked means join again

An unauthorised MCP call on its own does not mean revoked: an expired access token gets
the same answer, and the client renews and the call is retried. **Only a refused renew
ends the credential**: the server answers `invalid_grant`, and `--headers` or `--token`
exits with status 1 and says to run the join again. That covers every way it ends:

- the approval period ran out (both token lifetimes stop at the approval's end, and a
  renew never extends it);
- your person revoked you at `<mcp_url>/join/agents`, or revoked every agent;
- a refresh token was used twice (the server treats it as a leak);
- the refresh token went unused for its whole lifetime.

The answer is always the same: stop, tell your person, and run the join again once they
agree. A new join replaces the old credential. Never retry a refused renew in a loop. If you think your credential leaked, stop using
it and tell your person: they revoke it, and the server's operator holds the wider
switch.

# Wire shape

For anyone writing their own client. Errors are JSON `{error, error_description}` in the
device authorization grant shape of RFC 8628.

| Call | Sends | Gets |
| --- | --- | --- |
| `POST <mcp_url>/join/start` | `name`, `provider`, `machine`, `preset` | `device_code`, `user_code` (`XXXX-XXXX`), `verification_uri`, `verification_uri_complete`, `expires_in` (600), `interval` (5) |
| `POST <mcp_url>/join/token` | `device_code` | `authorization_pending`, `slow_down`, `access_denied` or `expired_token`; or the grant below |
| `POST <mcp_url>/join/token` | `grant_type=refresh_token`, `refresh_token` | a new grant, or `invalid_grant` |

A grant holds `access_token`, `token_type` (`Bearer`), `expires_in`, `expires_at`,
`refresh_token`, `refresh_expires_at`, `agent_expires_at` (the end of the approval),
`principal` and `preset`. Client exit status: 0 joined, 1 denied, expired or renew
refused, 2 usage or server error.

# Flows

```mermaid
sequenceDiagram
    autonumber
    participant A as Agent (join client)
    participant S as gtd MCP server
    participant P as Person (browser)
    A->>S: GET mcp_url/join (steps) and /join/client.py
    A->>S: POST /join/start (name, provider, preset)
    S-->>A: link + short code, device code, poll interval
    A->>P: show the link and the code
    P->>S: sign in with GitHub, check the code, pick preset, approve
    loop every few seconds until approved, denied or expired
        A->>S: POST /join/token (device code)
        S-->>A: authorization_pending
    end
    S-->>A: access token (24 h) + refresh token (7 d, single use)
    A->>A: save to a user-only file
    A->>S: MCP call with bearer token: whoami
    S-->>A: agent:name, preset
```

```mermaid
stateDiagram-v2
    [*] --> Joining: run the join client
    Joining --> Active: person approves
    Joining --> [*]: denied or expired
    Active --> Active: renew before the access token expires (new pair)
    Active --> Active: call refused as unauthorised, renew and retry
    Active --> Revoked: renew refused (approval ran out, person revoked, refresh reused)
    Revoked --> Joining: tell your person, join again
```

How the server keeps tokens and approvals is up to each deployment; this page is only
what an agent may rely on. See [claims and leases](/model/claims-and-leases.md) for what
the stamped identity is used for.
