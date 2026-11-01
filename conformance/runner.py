#!/usr/bin/env python3
"""Black-box conformance checks for a gtd MCP server (server-spec/conformance.md).

Standard library only (Python 3.9+). It speaks MCP over Streamable HTTP and plain HTTP to
the join routes, so it works against any implementation, in any language.

    python3 conformance/runner.py --server https://gtd.example.com --token-env GTD_TOKEN \
        --repo owner/sandbox --project owner/number --token-b-env GTD_TOKEN_B

What it needs, and which checks each unlocks:

    nothing                 C13 (the fold fixtures, against the reference fold or --fold-cmd)
    --server                T1, J2, J3 (J2 and J3 only with --join-start: it opens one join
                            request, which expires on its own in ten minutes)
    + a token               T2, T3, T5, T6 (partly), T7, P1 to P3, J10, X2 (partly)
    + --repo (a sandbox)    P4 to P6, C1, C5 to C9, C11, X1, X3. It CREATES issues there
    + a second token        C2, C3, C6 (as a second principal)
    + --project (a board)   P7, C5 (Size), C12, B1 to B4
    + --preset-token P=ENV  T6 and X2 in full, one token per preset

Tokens are read from environment variables, never from the command line, and are never
printed. Checks that need a person (J4 to J9, C4, C10, T4) are listed as manual with what
to do. Exit status: 0 every run check passed, 1 a check failed, 2 usage or connection error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PROTOCOL = "2025-06-18"
MARKER = "gtd-desk"
RECORD_RE = re.compile(r"<!--\s*" + MARKER + r"\s+v(\d+)\s+(\{.*?\})\s*-->", re.DOTALL)
PRESETS = ("desk", "read", "work", "full")

# The preset class of every tool the spec classes (transport-and-identity.md, tools.md).
CLASS = {"whoami": "desk"}
CLASS.update(dict.fromkeys((
    "profile_list", "profile_get", "project_get", "project_items", "project_item_find",
    "project_views_list", "list_next_actions", "issue_list", "issue_blocked_by_list",
    "item_get", "issue_parent", "sub_issues_list", "work_items_plan", "actions_workflows",
    "actions_runs", "actions_run_get", "actions_logs", "run_state_read", "channels_list",
    "channel_comments_read"), "read"))
CLASS.update(dict.fromkeys((
    "capture", "issue_comment", "issue_labels", "item_claim", "item_renew", "item_release",
    "item_report", "project_set_status", "project_set_field", "project_item_move",
    "project_add_item", "project_report", "project_item_archive", "project_status_update",
    "project_draft_add", "project_draft_update", "project_draft_convert", "issue_update",
    "issue_close", "issue_reopen", "issue_assign", "issue_milestone", "issue_type_set",
    "sub_issue_add", "sub_issue_remove", "issue_blocked_by_add", "issue_blocked_by_remove",
    "run_state_post", "channel_comment_post"), "work"))
CORE_TOOLS = ("whoami", "profile_list", "profile_get", "project_get", "project_items",
              "project_item_find", "project_views_list", "list_next_actions", "issue_list",
              "issue_blocked_by_list", "item_get", "item_claim", "item_renew", "item_release",
              "item_report", "capture", "issue_comment", "issue_labels")
WHOAMI_FIELDS = ("principal", "signed_in_by", "preset", "fenced", "provider", "expires_at",
                 "join_url", "conformance", "spec_version")
PROFILE_FIELDS = ("name", "labels", "needs", "owner_needs", "pickup_sizes", "status_for_label")
BASE_LABELS = ("run-agent", "agent-running", "waiting-for-review", "agent-failed", "blocked",
               "accepted", "needs:triage", "agent:any", "agent:human", "agent-ready",
               "agent-proposed")
IDENTITY_ARGS = {"principal", "author", "identity", "caller", "as_user", "by", "actor"}
IDENTITY_EXEMPT = {"run_state_post"}  # its `by` is provenance text (tools.md, Run state)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

class Report:
    def __init__(self) -> None:
        self.rows: list[dict[str, str]] = []

    def add(self, cid: str, status: str, note: str = "") -> None:
        self.rows.append({"id": cid, "status": status, "note": note})

    def ok(self, cid: str, note: str = "") -> None:
        self.add(cid, "pass", note)

    def fail(self, cid: str, note: str) -> None:
        self.add(cid, "FAIL", note)

    def skip(self, cid: str, note: str) -> None:
        self.add(cid, "skip", note)

    def manual(self, cid: str, note: str) -> None:
        self.add(cid, "manual", note)

    def check(self, cid: str, cond: bool, note_fail: str, note_ok: str = "") -> bool:
        (self.ok(cid, note_ok) if cond else self.fail(cid, note_fail))
        return cond

    def failed(self) -> bool:
        return any(r["status"] == "FAIL" for r in self.rows)


class CheckError(Exception):
    """A check could not run (the server answered something unusable)."""


# ---------------------------------------------------------------------------
# HTTP and MCP
# ---------------------------------------------------------------------------

def http(method: str, url: str, body: Any = None, headers: dict | None = None,
         form: bool = False, timeout: float = 60) -> tuple[int, dict, str]:
    data = None
    hdrs = dict(headers or {})
    if body is not None:
        if form:
            data = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in body.items()).encode()
            hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")
        else:
            data = json.dumps(body).encode()
            hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read().decode("utf-8", "replace")


class Client:
    """A minimal stateless MCP client: no session id is sent unless the server insists."""

    def __init__(self, base: str, token: str | None, seen: list[str]):
        self.base, self.token, self.seen = base.rstrip("/"), token, seen
        self.session: str | None = None
        self._id = 0

    def _post(self, payload: dict, notification: bool = False) -> tuple[int, dict, Any]:
        headers = {"Accept": "application/json, text/event-stream",
                   "MCP-Protocol-Version": PROTOCOL}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        status, hdrs, text = http("POST", f"{self.base}/mcp", payload, headers)
        self.seen.append(text)
        if notification or not text.strip():
            return status, hdrs, None
        if "text/event-stream" in hdrs.get("content-type", ""):
            msgs = [json.loads(line[5:].strip()) for line in text.splitlines()
                    if line.startswith("data:") and line[5:].strip()]
            msg = next((m for m in msgs if m.get("id") == payload.get("id")), msgs[-1] if msgs else None)
        else:
            try:
                msg = json.loads(text)
            except json.JSONDecodeError:
                msg = None
        return status, hdrs, msg

    def rpc(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}}
        status, _hdrs, msg = self._post(payload)
        if status == 400 and self.session is None and method != "initialize" and \
                "session" in json.dumps(msg or {}).lower():
            raise CheckError("the server requires a session id (not stateless)")
        if status >= 400 or msg is None:
            raise CheckError(f"{method}: HTTP {status}")
        if "error" in msg:
            raise CheckError(f"{method}: {msg['error'].get('message')}")
        return msg["result"]

    def initialize(self) -> dict:
        result = self.rpc("initialize", {"protocolVersion": PROTOCOL, "capabilities": {},
                                         "clientInfo": {"name": "gtd-conformance", "version": "1"}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"}, notification=True)
        return result

    def tools(self) -> list[dict]:
        out, cursor = [], None
        while True:
            res = self.rpc("tools/list", {"cursor": cursor} if cursor else {})
            out += res.get("tools") or []
            cursor = res.get("nextCursor")
            if not cursor:
                return out

    def call(self, name: str, args: dict | None = None) -> tuple[bool, Any, str]:
        """(ok, structured content, text). ok is False for a tool refusal."""
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                   "params": {"name": name, "arguments": args or {}}}
        status, _, msg = self._post(payload)
        if msg is None:
            raise CheckError(f"{name}: HTTP {status}, no JSON-RPC message")
        if "error" in msg:
            return False, None, str(msg["error"].get("message", ""))
        res = msg.get("result") or {}
        text = " ".join(c.get("text", "") for c in res.get("content") or [] if isinstance(c, dict))
        return not res.get("isError"), res.get("structuredContent"), text


# ---------------------------------------------------------------------------
# A small JSON Schema check (type, required, properties, items) for T3
# ---------------------------------------------------------------------------

_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool,
          "integer": int, "number": (int, float), "null": type(None)}


def schema_errors(value: Any, schema: dict, defs: dict | None = None, path: str = "$") -> list[str]:
    defs = defs if defs is not None else (schema.get("$defs") or schema.get("definitions") or {})
    if "$ref" in schema:
        name = schema["$ref"].rsplit("/", 1)[-1]
        return schema_errors(value, defs.get(name, {}), defs, path)
    for key in ("anyOf", "oneOf"):
        if key in schema:
            if any(not schema_errors(value, s, defs, path) for s in schema[key]):
                return []
            return [f"{path}: matches none of {key}"]
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        ok = any(isinstance(value, _TYPES.get(x, object)) and
                 not (x in ("integer", "number") and isinstance(value, bool)) for x in types)
        if not ok:
            return [f"{path}: expected {t}, got {type(value).__name__}"]
    errs: list[str] = []
    if isinstance(value, dict):
        for req in schema.get("required") or []:
            if req not in value:
                errs.append(f"{path}.{req}: required")
        for k, sub in (schema.get("properties") or {}).items():
            if k in value:
                errs += schema_errors(value[k], sub, defs, f"{path}.{k}")
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for i, item in enumerate(value[:20]):
            errs += schema_errors(item, schema["items"], defs, f"{path}[{i}]")
    return errs


# ---------------------------------------------------------------------------
# The reference fold (claim-records.md) and C13
# ---------------------------------------------------------------------------

def parse_record(body: str) -> dict | None:
    found = RECORD_RE.findall(body or "")
    if len(found) != 1 or int(found[0][0]) != 1:
        return None
    try:
        rec = json.loads(found[0][1])
    except json.JSONDecodeError:
        return None
    if not isinstance(rec, dict) or rec.get("event") not in ("claim", "renew", "release", "report"):
        return None
    return rec


def _ts(value: str | None) -> datetime | None:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) if value else None


def reference_fold(comments: list[dict], now: str) -> dict:
    """The fold in server-spec/claim-records.md, over ``[{id, body}]`` in any order."""
    holder = lease = handoff = last_report = attention_by = None
    lost = 0
    for c in sorted(comments, key=lambda c: c["id"]):
        rec = parse_record(c["body"])
        if rec is None:
            continue
        ev, by, at = rec["event"], rec.get("by"), _ts(rec.get("t"))
        if ev == "claim":
            if holder is None or (rec.get("takeover_of") == holder and lease and at and lease < at):
                holder, lease = by, _ts(rec.get("lease_until"))
                handoff = last_report = None
            else:
                lost += 1
        elif ev == "renew" and by == holder:
            lease = _ts(rec.get("lease_until")) or lease
        elif ev == "release" and by == holder:
            holder = lease = last_report = None
            handoff = rec.get("handoff_to")
        elif ev == "report":
            attention_by = by if rec.get("attention") else None
            if by == holder and rec.get("state"):
                last_report = rec["state"]
                if last_report == "dropped":
                    holder = lease = last_report = None
                    handoff = rec.get("handoff_to")
    stamp = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ") if d else None
    return {"holder": holder, "lease_until": stamp(lease),
            "stale": bool(holder and lease and lease < _ts(now)), "last_report": last_report,
            "handoff_to": handoff, "lost_claims": lost, "attention_by": attention_by}


def render_record(rec: dict) -> str:
    raw = json.dumps(rec, sort_keys=True).replace("<", "\\u003c").replace(">", "\\u003e")
    return f"### Record\n\n<!-- {MARKER} v1 {raw} -->"


def fold_inputs(fixtures: dict) -> list[tuple[dict, list[dict], str]]:
    base = _ts(fixtures["base"])
    at = lambda m: (base + timedelta(minutes=m)).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = []
    for case in fixtures["cases"]:
        bodies = list(case.get("raw_comments") or [])
        for r in case["records"]:
            rec = {"v": 1, **r, "t": at(r["t"])}
            if "lease_until" in rec:
                rec["lease_until"] = at(r["lease_until"])
            bodies.append(render_record(rec))
        comments = [{"id": i + 1, "body": b} for i, b in enumerate(bodies)]
        expect = dict(case["expect"])
        if expect.get("lease_until") is not None:
            expect["lease_until"] = at(expect["lease_until"])
        out.append((case, comments, at(fixtures["now"])) + (expect,))
    return out


def check_fold(rep: Report, fold_cmd: str | None) -> None:
    fixtures = json.loads((HERE / "fold_cases.json").read_text())
    bad = []
    for case, comments, now, expect in fold_inputs(fixtures):
        if fold_cmd:
            proc = subprocess.run(fold_cmd, shell=True, input=json.dumps({"now": now, "comments": comments}),
                                  capture_output=True, text=True, timeout=60, check=False)
            try:
                got = json.loads(proc.stdout)
            except json.JSONDecodeError:
                bad.append(f"{case['name']}: no JSON from --fold-cmd")
                continue
        else:
            got = reference_fold(comments, now)
        diff = [k for k, v in expect.items() if got.get(k) != v]
        if diff:
            bad.append(f"{case['name']} ({case['says']}): {', '.join(f'{k}={got.get(k)!r}' for k in diff)}")
    who = "--fold-cmd" if fold_cmd else "the reference fold"
    rep.check("C13", not bad, "; ".join(bad), f"{len(fixtures['cases'])} cases, {who}")


# ---------------------------------------------------------------------------
# Server checks
# ---------------------------------------------------------------------------

def check_t1(rep: Report, base: str) -> None:
    status, hdrs, _ = http("POST", f"{base}/mcp", {"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
                           {"Accept": "application/json, text/event-stream"})
    challenge = hdrs.get("www-authenticate", "")
    m = re.search(r'resource_metadata="([^"]+)"', challenge)
    if status != 401 or not m:
        rep.fail("T1", f"unauthenticated POST /mcp gave {status}, challenge {challenge[:80]!r}")
        return
    s2, _, text = http("GET", m.group(1))
    try:
        meta = json.loads(text)
    except json.JSONDecodeError:
        meta = {}
    rep.check("T1", s2 == 200 and str(meta.get("resource", "")).rstrip("/").endswith("/mcp"),
              f"metadata at {m.group(1)} gave {s2}, resource {meta.get('resource')!r}")


def check_identity(rep: Report, c: Client) -> tuple[dict, dict]:
    try:
        init = c.initialize()
        tools = {t["name"]: t for t in c.tools()}
        ok, who, text = c.call("whoami")
    except CheckError as e:
        rep.fail("T2", str(e))
        raise
    rep.check("T2", ok and isinstance(who, dict) and c.session is None,
              f"whoami: {text[:120]}", f"protocol {init.get('protocolVersion')}")
    no_schema = [n for n, t in tools.items() if not t.get("inputSchema") or not t.get("outputSchema")]
    errs = schema_errors(who or {}, tools.get("whoami", {}).get("outputSchema") or {})
    rep.check("T3", not no_schema and not errs,
              f"no input or output schema: {', '.join(sorted(no_schema)[:12])}; whoami: {'; '.join(errs[:3])}",
              f"{len(tools)} tools")
    missing = [f for f in WHOAMI_FIELDS if f not in (who or {})]
    rep.check("T5", not missing, f"whoami lacks {', '.join(missing)}",
              f"{(who or {}).get('principal')} at {(who or {}).get('preset')}, "
              f"levels {(who or {}).get('conformance')}")
    leaks = sorted(n for n, t in tools.items() if n not in IDENTITY_EXEMPT and
                   IDENTITY_ARGS & set((t.get("inputSchema") or {}).get("properties") or {}))
    rep.check("T7", not leaks, f"identity-like arguments on {', '.join(leaks)}")
    absent = [t for t in CORE_TOOLS if t not in tools]
    if (who or {}).get("preset") in ("full", "work"):
        rep.check("T0", not absent, f"Core tools missing at preset {who.get('preset')}: {', '.join(absent)}",
                  f"all {len(CORE_TOOLS)} Core tools listed")
    else:
        rep.skip("T0", f"needs a work or full token to see every Core tool (have {who.get('preset')})")
    j10 = sorted(n for n in tools if re.search(r"approve|revoke|deny", n))
    rep.check("J10", not j10, f"tools that look like join admin: {', '.join(j10)}")
    return who or {}, tools


def check_presets(rep: Report, base: str, preset_tokens: dict[str, str], seen: list[str]) -> None:
    if not preset_tokens:
        rep.skip("X2", "pass --preset-token PRESET=ENV for each preset")
        return
    bad_t6, bad_x2 = [], []
    for preset, token in preset_tokens.items():
        c = Client(base, token, seen)
        c.initialize()
        names = {t["name"] for t in c.tools()}
        rank = PRESETS.index(preset)
        for n in names:
            cls = CLASS.get(n, "full")
            if PRESETS.index(cls) > rank:
                bad_x2.append(f"{n} ({cls}) visible at {preset}")
        hidden = [n for n, cls in CLASS.items() if PRESETS.index(cls) <= rank and n in CORE_TOOLS
                  and n not in names]
        if hidden:
            bad_t6.append(f"{preset} hides {', '.join(hidden)}")
        above = next((n for n, cls in CLASS.items() if PRESETS.index(cls) == rank + 1), None)
        if above:
            ok, _, text = c.call(above, {})
            if ok or not re.search(PRESETS[rank + 1], text):
                bad_t6.append(f"calling {above} at {preset} did not refuse naming {PRESETS[rank + 1]}")
    rep.check("T6", not bad_t6, "; ".join(bad_t6), f"presets {', '.join(preset_tokens)}")
    rep.check("X2", not bad_x2, "; ".join(bad_x2[:6]))


def check_profiles(rep: Report, c: Client) -> dict:
    ok, lst, text = c.call("profile_list")
    if not ok:
        rep.fail("P1", f"profile_list: {text[:120]}")
        return {}
    names = [p["name"] if isinstance(p, dict) else p for p in (lst or {}).get("profiles") or []]
    profiles, p1, p2, p3 = {}, [], [], []
    for name in names:
        ok, p, text = c.call("profile_get", {"name": name})
        if not ok:
            p1.append(f"{name}: {text[:80]}")
            continue
        profiles[name] = p
        missing = [f for f in PROFILE_FIELDS if f not in p]
        labels = {(lbl.get("name") if isinstance(lbl, dict) else lbl) for lbl in p.get("labels") or []}
        no_base = [b for b in BASE_LABELS if b not in labels]
        if missing or no_base:
            p1.append(f"{name}: lacks {', '.join(missing + no_base)}")
        needs = p.get("needs") or []
        if any(f"needs:{n}" not in labels for n in needs) or p.get("owner_needs") not in needs:
            p2.append(name)
        rules = p.get("status_for_label") or []
        mapped = {r.get("label") for r in rules}
        cols = set(p.get("status") or (p.get("board") or {}).get("status") or [])
        must = ["agent-running", "waiting-for-review", "agent-failed"] + [f"needs:{n}" for n in needs]
        if [m for m in must if m not in mapped] or (cols and {r.get("status") for r in rules} - cols):
            p3.append(name)
    rep.check("P1", names and not p1, "; ".join(p1) or "no profiles", f"{len(names)} profiles")
    rep.check("P2", not p2, f"needs or owner_needs inconsistent in {', '.join(p2)}")
    rep.check("P3", not p3, f"status_for_label incomplete or off-board in {', '.join(p3)}")
    return profiles


class Sandbox:
    """Issues the run creates in the sandbox repo, titled so a person can find them."""

    def __init__(self, c: Client, repo: str, project: str | None, run: str):
        self.c, self.repo, self.project, self.run = c, repo, project, run
        self.made: list[int] = []

    def issue(self, what: str, labels: list[str] | None = None) -> int:
        args = {"title": f"[conformance {self.run}] {what}", "repo": self.repo,
                "note": "Created by the gtd-board-kit conformance runner. Safe to close."}
        if labels:
            args["labels"] = labels
        ok, out, text = self.c.call("capture", args)
        if not ok:
            raise CheckError(f"capture: {text[:160]}")
        self.made.append(int(out["number"]))
        return int(out["number"])

    def args(self, number: int, **more: Any) -> dict:
        a = {"repo": self.repo, "number": number, **more}
        if self.project:
            a.setdefault("project", self.project)
        return a


def check_repo(rep: Report, c: Client, c2: Client | None, sb: Sandbox, profile: dict,
               who: dict | None = None) -> None:
    repo = sb.repo
    owner_needs = profile.get("owner_needs") or "triage"

    # P4 labels
    n = sb.issue("labels")
    ok, out, text = c.call("issue_labels", sb.args(n, add=["blocked", "area:conformance"]))
    ok2, _, t2 = c.call("issue_labels", sb.args(n, add=["conformance-not-a-label"]))
    ok3, _, _t3 = c.call("issue_labels", sb.args(n, add=["run-agent"]))
    ok4, _, _ = c.call("issue_labels", sb.args(n, remove=["blocked"]))
    rep.check("P4", ok and not ok2 and not ok3 and ok4 and "blocked" in (t2 + json.dumps(out or {})),
              f"add {ok} ({text[:60]}), unknown refused {not ok2}, run-agent refused {not ok3}, remove {ok4}")

    # P5 allowlist
    ok, _, text = c.call("item_get", {"repo": "conformance-invalid/never-allowed", "number": 1})
    rep.check("P5", not ok, "item_get on a repo outside the allowlist was not refused",
              "refused (the runner cannot see whether GitHub was called)")

    # P6 next actions
    tag = sb.issue("next action", labels=["agent-ready"])
    ok, out, text = c.call("list_next_actions", {"repo": repo, "context": "agent-ready", "limit": 100})
    rows = out if isinstance(out, list) else (out or {}).get("result") or (out or {}).get("items") or []
    rep.check("P6", ok and any(r.get("number") == tag for r in rows) and
              all("agent-ready" in (r.get("labels") or []) for r in rows),
              f"list_next_actions: {text[:120] if not ok else 'missing or unlabelled rows'}")

    # C1 claim
    n = sb.issue("claim")
    ok_a, _, _ = c.call("item_claim", sb.args(n, basis="explicit"))
    ok, out, text = c.call("item_claim", sb.args(n, basis="explicit", asked_by="conformance", lease="30m"))
    item = (out or {}).get("item") or {}
    rep.check("C1", not ok_a and ok and item.get("holder") and item.get("lease_until") and
              (item.get("mandate") or {}).get("scope"),
              f"no asked_by refused {not ok_a}; claim {ok} {text[:100]}")
    holder = item.get("holder")

    # C2, C6 with a second principal
    if c2:
        ok, _, text = c2.call("item_claim", sb.args(n, basis="explicit", asked_by="conformance"))
        rep.check("C2", not ok and holder and holder in text, f"second claim: ok={ok} {text[:100]}")
        r1, _, _ = c2.call("item_renew", sb.args(n))
        r2, _, _ = c2.call("item_release", sb.args(n, done="a", remaining="b", next="c"))
        r3, _, _ = c2.call("item_report", sb.args(n, state="progress", note="x"))
        rep.check("C6", not (r1 or r2 or r3), f"non-holder renew {r1}, release {r2}, report {r3}")
    else:
        rep.skip("C2", "needs a second token (--token-b-env)")
        rep.skip("C6", "needs a second token (--token-b-env)")

    # C9 follow-ups, C11 marker refusal
    c.call("issue_comment", sb.args(n, body="A follow-up from the conformance runner."))
    ok, out, _ = c.call("item_get", sb.args(n))
    rep.check("C9", ok and ((out or {}).get("item") or {}).get("follow_ups"),
              "a plain comment after the claim is not in follow_ups")
    ok, _, _ = c.call("issue_comment", sb.args(n, body=f"<!-- {MARKER} v1 {{\"event\": \"claim\"}} -->"))
    rep.check("C11", not ok, "a comment carrying a record marker was accepted")

    # C8 attention, X3 over-long
    ok_none, _, _t_none = c.call("item_report", sb.args(n, attention="Which way?"))
    ok, out, text = c.call("item_report", sb.args(n, attention="Which way?", needs=owner_needs))
    ok_lbl, lbl_out, _ = c.call("issue_list", {"repo": repo, "labels": [f"needs:{owner_needs}"], "limit": 100})
    listed = [i.get("number") for i in ((lbl_out or {}).get("issues") or (lbl_out or {}).get("items") or [])]
    rep.check("C8", not ok_none and ok and (n in listed or not ok_lbl),
              f"no needs refused {not ok_none}; with needs {ok} {text[:80]}; labelled {n in listed}")
    ok, _, _ = c.call("item_report", sb.args(n, note="x" * 5000))
    rep.check("X3", not ok, "a 5000-character note was accepted")

    # C7 release
    ok_m, _, _ = c.call("item_release", sb.args(n, done="checked"))
    ok, out, text = c.call("item_release", sb.args(n, done="checked", remaining="none", next="close",
                                                   handoff_to="any"))
    item = (out or {}).get("item") or {}
    rep.check("C7", not ok_m and ok and item.get("holder") is None and item.get("handoff_to") == "any",
              f"missing fields refused {not ok_m}; release {ok} {text[:80]}")

    # C3 race
    if c2:
        n = sb.issue("race")
        results: dict[str, bool] = {}

        def go(cl: Client, key: str) -> None:
            results[key] = cl.call("item_claim", sb.args(n, basis="explicit", asked_by="conformance"))[0]
        ts = [threading.Thread(target=go, args=(c, "a")), threading.Thread(target=go, args=(c2, "b"))]
        [t.start() for t in ts]
        [t.join() for t in ts]
        _, out, _ = c.call("item_get", sb.args(n))
        item = (out or {}).get("item") or {}
        rep.check("C3", sum(results.values()) == 1 and item.get("holder"),
                  f"both claims returned {results}; holder {item.get('holder')}")
    else:
        rep.skip("C3", "needs a second token (--token-b-env)")

    # C5 inferred
    names = {(lbl.get("name") if isinstance(lbl, dict) else lbl) for lbl in profile.get("labels") or []}
    mine = f"agent:{(who or {}).get('provider') or ''}"
    others = sorted(n for n in names if n.startswith("agent:") and n not in ("agent:any", "agent:human", mine))
    bars = {"none": [], "human": ["agent-ready", "agent:human"], "blocked": ["agent-ready", "blocked"],
            "needs": ["agent-ready", f"needs:{owner_needs}"], "proposed": ["agent-ready", "agent-proposed"]}
    if others:
        bars["routed"] = ["agent-ready", others[0]]
    leaked = []
    for what, labels in bars.items():
        num = sb.issue(f"inferred {what}", labels=labels or None)
        ok, _, _ = c.call("item_claim", {"repo": repo, "number": num, "basis": "inferred"})
        if ok:
            leaked.append(what)
    num = sb.issue("inferred ok", labels=["agent-ready", "agent:any"])
    ok, _, text = c.call("item_claim", {"repo": repo, "number": num, "basis": "inferred"})
    rep.check("C5", not leaked and ok, f"accepted: {', '.join(leaked) or '-'}; agent-ready claim {ok} {text[:80]}",
              "Size checked too" if sb.project else "labels only (pass --project for Size)")

    # C6b closed issue: needs issue_close, an optional tool
    rep.manual("C6b", "close a claimed sandbox issue by hand, then item_release must succeed and item_claim refuse")


def check_board(rep: Report, c: Client, sb: Sandbox) -> None:
    proj = sb.project
    ok, out, text = c.call("project_items", {"project": proj, "limit": 2})
    pages = ok and "has_next_page" in (out or {}) and "next_cursor" in (out or {})
    rep.check("P7", pages, f"project_items: {text[:100] or 'no paging fields'}")
    n = sb.issue("board")
    ok, _, text = c.call("project_set_status", {"repo": sb.repo, "number": n, "project": proj,
                                                "status": "Conformance-No-Such-Column"})
    rep.check("B1", not ok and len(text) > 40, "an unknown column was not refused with the live list")
    ok, _, text = c.call("project_set_field", {"repo": sb.repo, "number": n, "project": proj,
                                               "field": "Target date", "value": "2030-01-01"})
    ok2, found, _ = c.call("project_item_find", {"repo": sb.repo, "number": n, "project": proj})
    ok3, _, _ = c.call("project_set_field", {"repo": sb.repo, "number": n, "project": proj,
                                             "field": "Target date", "clear": True})
    rep.check("B4", ok and ok2, f"set_field on an item not yet on the board: {text[:100]}")
    rep.check("B2", ok and ok3 and ((found or {}).get("fields") or {}).get("Target date") == "2030-01-01",
              "date field set/read/clear did not round-trip", "date field only; text, number, select by hand")
    ok, _, text = c.call("project_item_move", {"repo": sb.repo, "number": n, "project": proj})
    ok2, out, _ = c.call("project_items", {"project": proj, "limit": 1})
    first = ((out or {}).get("items") or [{}])[0]
    rep.check("B3", ok and first.get("number") == n, f"move to top: {text[:80]}; first is {first.get('number')}")
    m = sb.issue("mirror")
    c.call("item_claim", sb.args(m, basis="explicit", asked_by="conformance", lease="30m"))
    c.call("item_report", sb.args(m, state="progress", note="mirror check"))
    ok, found, _ = c.call("project_item_find", {"repo": sb.repo, "number": m, "project": proj})
    fields = (found or {}).get("fields") or {}
    rep.check("C12", ok and fields.get("Agent") and "progress" in str(fields.get("Last report", "")),
              f"board fields after claim and report: Agent={fields.get('Agent')!r}, "
              f"Last report={fields.get('Last report')!r}")
    c.call("item_release", sb.args(m, done="mirror", remaining="none", next="close"))


def check_join(rep: Report, base: str, start: bool, claims_join: bool | None) -> None:
    s, _, text = http("POST", f"{base}/join/start", {"name": "X", "provider": "conformance", "preset": "read"})
    if s == 404 and not claims_join:
        rep.skip("J2", "the join routes are off on this server (no Join level)")
        rep.skip("J3", "the join routes are off on this server (no Join level)")
        return
    bad_name = s == 400 and "invalid" in text
    if not start:
        rep.check("J2", bad_name, f"an invalid name gave {s}: {text[:80]}",
                  "invalid name refused; pass --join-start to open one real request")
        rep.skip("J3", "pass --join-start")
        return
    s, _, text = http("POST", f"{base}/join/start", {"name": f"conformance-{int(time.time()) % 100000}",
                                                     "provider": "conformance", "machine": "runner",
                                                     "preset": "read"})
    try:
        grant = json.loads(text)
    except json.JSONDecodeError:
        grant = {}
    fields = ("device_code", "user_code", "verification_uri", "verification_uri_complete", "expires_in", "interval")
    rep.check("J2", bad_name and s == 200 and all(f in grant for f in fields) and
              re.fullmatch(r"[A-Z0-9]{4}-[A-Z0-9]{4}", str(grant.get("user_code", ""))),
              f"start gave {s}: missing {[f for f in fields if f not in grant]}")
    if grant.get("device_code"):
        s, _, text = http("POST", f"{base}/join/token", {"device_code": grant["device_code"]})
        rep.check("J3", "authorization_pending" in text, f"poll gave {s}: {text[:80]}",
                  "pending; the request expires on its own")


MANUAL = {
    "T4": "sign in through the connector as an identity not on the allowlist; every call must be refused",
    "C4": "claim with lease 1m, wait two minutes, claim as a second principal: the record names takeover_of",
    "C10": "with record authors configured, paste a claim record from another account: item_get ignores it",
    "J1": "remove every approver: /join/start and joined tokens are refused",
    "J4": "approve a join at a lower preset: the first poll returns that preset, the second nothing",
    "J5": "inspect the auth store after collection: hashes only",
    "J6": "renew, then renew again with the old refresh token: invalid_grant, and the agent is revoked",
    "J7": "check the grant: expires_at and refresh_expires_at never pass agent_expires_at",
    "J8": "revoke one agent at /join/agents: its next call is 401, its renew invalid_grant, others work",
    "J9": "POST /join/decide and /join/revoke without a session or CSRF token: refused",
}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--server", help="the server's base URL, no path")
    ap.add_argument("--token-env", help="environment variable holding a bearer token (work preset for writes)")
    ap.add_argument("--token-b-env", help="a second principal's token, for C2, C3, C6")
    ap.add_argument("--preset-token", action="append", default=[], metavar="PRESET=ENV",
                    help="a token at that preset, for T6 and X2 (repeatable)")
    ap.add_argument("--repo", help="owner/repo sandbox; the run creates issues there")
    ap.add_argument("--project", help="owner/number board linked to the sandbox repo")
    ap.add_argument("--profile", help="the sandbox repo's profile (default: the first profile_list returns)")
    ap.add_argument("--join-start", action="store_true", help="open one join request for J2 and J3")
    ap.add_argument("--fold-cmd", help="a command that folds {now, comments} from stdin to JSON on stdout")
    ap.add_argument("--json", help="also write the report as JSON to this file")
    a = ap.parse_args(argv)

    rep = Report()
    check_fold(rep, a.fold_cmd)
    seen: list[str] = []
    secrets: list[str] = []

    def token(env: str | None) -> str | None:
        if not env:
            return None
        value = os.environ.get(env)
        if not value:
            print(f"usage: ${env} is empty", file=sys.stderr)
            sys.exit(2)
        secrets.append(value)
        return value

    if a.server:
        base = a.server.rstrip("/")
        try:
            check_t1(rep, base)
        except (urllib.error.URLError, OSError) as e:
            print(f"cannot reach {base}: {e}", file=sys.stderr)
            return 2
        t1 = token(a.token_env)
        claims_join = None
        if t1:
            c = Client(base, t1, seen)
            try:
                who, _tools = check_identity(rep, c)
                claims_join = "Join" in (who.get("conformance") or [])
                profiles = check_profiles(rep, c)
                presets = {}
                for spec in a.preset_token:
                    p, _, env = spec.partition("=")
                    presets[p] = token(env)
                check_presets(rep, base, presets, seen)
                if a.repo:
                    c2 = Client(base, token(a.token_b_env), seen) if a.token_b_env else None
                    if c2:
                        c2.initialize()
                    name = a.profile or next(iter(profiles), None)
                    sb = Sandbox(c, a.repo, a.project, datetime.now(timezone.utc).strftime("%m%d-%H%M"))
                    check_repo(rep, c, c2, sb, profiles.get(name) or {}, who)
                    if a.project:
                        check_board(rep, c, sb)
                    print(f"note: created issues {', '.join('#' + str(x) for x in sb.made)} in {a.repo}",
                          file=sys.stderr)
            except CheckError as e:
                rep.fail("RUN", f"stopped: {e}")
        check_join(rep, base, a.join_start, claims_join)
    for cid, how in MANUAL.items():
        rep.manual(cid, how)
    if secrets:
        leaked = [s for s in secrets if any(s in body for body in seen)]
        rep.check("X1", not leaked, "a token the runner sent came back in a response body",
                  f"{len(seen)} responses scanned")

    order = {k: i for i, k in enumerate("TPCBJXR")}
    rows = sorted(rep.rows, key=lambda r: (order.get(r["id"][0], 9),
                                           int(re.sub(r"\D", "", r["id"]) or 0), r["id"]))
    width = max(len(r["id"]) for r in rows)
    for r in rows:
        print(f"{r['id']:<{width}}  {r['status']:<6}  {r['note']}")
    counts = {s: sum(r["status"] == s for r in rows) for s in ("pass", "FAIL", "skip", "manual")}
    print(", ".join(f"{v} {k}" for k, v in counts.items()))
    if a.json:
        Path(a.json).write_text(json.dumps({"rows": rows, "counts": counts}, indent=2))
    return 1 if rep.failed() else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
