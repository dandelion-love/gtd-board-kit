#!/usr/bin/env python3
"""Black-box conformance checks for a gtd MCP server (server-spec/conformance.md).

Standard library only (Python 3.9+). It speaks MCP over Streamable HTTP and plain HTTP to
the join routes, so it works against any implementation, in any language.

    python3 conformance/runner.py --server https://gtd.example.com --token-env GTD_TOKEN \
        --repo owner/sandbox --project owner/number --token-b-env GTD_TOKEN_B

What it needs, and which checks each unlocks:

    nothing                 C13 (the fold fixtures, against the reference fold or --fold-cmd)
    --server                T1, T8, J2, J3 (J2 and J3 only with --join-start: it opens one join
                            request, which expires on its own in ten minutes)
    + a token               T2, T3, T5, T6 (partly), T7, T8 (in full), T9, P1 to P3, P8, J10, X2 (partly)
    + --repo (a sandbox)    P4 to P6, C1, C5 to C9, C11, C14, X1, X3. It CREATES issues there
    + a second token        C2, C3, C6 (as a second principal)
    + --project (a board)   P7, C5 (Size), C12, B1 to B4
    + --preset-token P=ENV  T6 and X2 in full, one token per preset
    profile_updates offered O1 (with a token), O2 (with --repo); O3 is manual
    item_ready offered      R1 (with --ready-cmd), R2 to R8 (with --repo; R2 and R6 in full
                            with --project)
    sub_issue_add offered   K1 (with --kind-cmd), K2 to K4 (with --repo whose owner has the
                            Issue Types Epic, Story, Chore, Spike and Finding)
    no --server             C13, R1 and K1, against the reference fold, ready check and Kind rules

Tokens are read from environment variables, never from the command line, and are never
printed. Checks that need a person (J4 to J9, C4, C10, T4) are listed as manual with what
to do. Exit status: 0 every run check passed, 1 a check failed, 2 usage or connection error.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from enum import Enum
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


class Family(Enum):
    """The check families of server-spec/conformance.md, in report order. A check id is
    the family's prefix and a number (``T1``, ``JC4``, ``C6b``); ``RUN`` is the runner's
    own row when a run stops early."""
    TRANSPORT = "T"         # Transport and identity (Core)
    PROFILES = "P"          # Repo context and labels (Core)
    CLAIMS = "C"            # Claims (Core)
    BOARD = "B"             # Board (Board level)
    CUSTOMIZATION = "O"     # Customization (when profile_updates is offered)
    READINESS = "R"         # Ready check (when item_ready is offered)
    PULL_REQUESTS = "PR"    # Pull requests (when pr_open is offered)
    KINDS = "K"             # Kind and parent rules (when the Issue structure tools are offered)
    JOIN = "J"              # Join (Join level)
    CONNECTOR = "JC"        # Connector entrance (when offered)
    SECURITY = "X"          # Security (all levels)
    RUN = "RUN"             # the runner itself


#: Each family's heading in server-spec/conformance.md (tests/check_kit.py checks them).
HEADINGS = {
    Family.TRANSPORT: "Transport and identity", Family.PROFILES: "Repo context and labels",
    Family.CLAIMS: "Claims", Family.BOARD: "Board", Family.CUSTOMIZATION: "Customization",
    Family.READINESS: "Ready check", Family.PULL_REQUESTS: "Pull requests",
    Family.KINDS: "Kind and parent rules",
    Family.JOIN: "Join", Family.CONNECTOR: "Connector entrance", Family.SECURITY: "Security",
}

#: A check id: a family prefix, a number, and an optional letter.
CHECK_ID = re.compile(r"(?:%s)\d+b?" % "|".join(
    sorted((f.value for f in Family if f is not Family.RUN), key=len, reverse=True)))


class Level(Enum):
    """The conformance levels of server-spec/README.md, lowest first."""
    CORE = "Core"
    JOIN = "Join"
    BOARD = "Board"
    EXTENDED = "Extended"


#: The level each family's checks belong to (Security holds at every level, so Core).
LEVEL_OF = {
    Family.TRANSPORT: Level.CORE, Family.PROFILES: Level.CORE, Family.CLAIMS: Level.CORE,
    Family.SECURITY: Level.CORE, Family.JOIN: Level.JOIN, Family.CONNECTOR: Level.JOIN,
    Family.BOARD: Level.BOARD, Family.CUSTOMIZATION: Level.EXTENDED,
    Family.READINESS: Level.EXTENDED, Family.PULL_REQUESTS: Level.EXTENDED,
    Family.KINDS: Level.EXTENDED,
}

WELL_KNOWN = "/.well-known/gtd-board-kit"
SEMVER = re.compile(r"\d+\.\d+\.\d+")


def family_of(cid: str) -> Family:
    """The family a check id belongs to (the longest matching prefix)."""
    if cid == Family.RUN.value:
        return Family.RUN
    prefix = re.match(r"[A-Z]+", cid)
    return Family(prefix.group(0)) if prefix else Family.RUN


def report_order(cid: str) -> tuple:
    """Family order, then number, then the id: ``T2`` before ``T10`` before ``P1``."""
    families = list(Family)
    return (families.index(family_of(cid)), int(re.sub(r"\D", "", cid) or 0), cid)
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
    "channel_comments_read", "profile_updates", "item_ready"), "read"))
CLASS.update(dict.fromkeys((
    "capture", "issue_comment", "issue_labels", "item_claim", "item_renew", "item_release",
    "item_report", "project_set_status", "project_set_field", "project_item_move",
    "project_add_item", "project_report", "project_item_archive", "project_status_update",
    "project_draft_add", "project_draft_update", "project_draft_convert", "issue_update",
    "issue_close", "issue_reopen", "issue_assign", "issue_milestone", "issue_type_set",
    "sub_issue_add", "sub_issue_remove", "issue_blocked_by_add", "issue_blocked_by_remove",
    "run_state_post", "channel_comment_post", "pr_open"), "work"))
#: Tools the spec classes `full` by name (tools.md, Optional groups), and the families it
#: classes `full` by prefix. A declaration can never lower one of these.
SPEC_FULL = frozenset((
    "project_create", "project_update", "project_template", "project_copy", "project_link_repo",
    "project_views", "project_reconcile", "project_field_update", "project_field_delete",
    "project_item_remove", "project_workflows", "project_workflow_delete",
    "repo_reconcile_labels", "work_items_sync", "actions_run", "actions_rerun", "actions_cancel",
    "org_issue_types", "org_issue_type_set", "repo_variables", "repo_variable_set",
    "repo_variable_delete"))
SPEC_FULL_PREFIXES = ("webhook_",)


def spec_class(name: str) -> str | None:
    """The class the spec gives ``name``, or None for a tool the spec does not name."""
    if name in CLASS:
        return CLASS[name]
    if name in SPEC_FULL or name.startswith(SPEC_FULL_PREFIXES):
        return "full"
    return None


#: Where a server declares the class of a tool of its own (transport-and-identity.md, Presets).
CLASS_META = "gtd-board-kit/class"
#: How long a list read may lag a label write (GitHub's label-filtered lists), P6 and C8.
LIST_LAG_SECONDS, LIST_LAG_STEP = 30, 3


def tool_class(tool: dict) -> tuple[str, str | None]:
    """(class, problem): the spec's class, else the declared one, else ``full``."""
    declared = (tool.get("_meta") or {}).get(CLASS_META)
    spec = spec_class(tool.get("name") or "")
    if declared is not None and declared not in PRESETS:
        return spec or "full", f"declares class {declared!r}, not a preset"
    if spec and declared is not None and declared != spec:
        return spec, f"declares {declared}, the spec gives {spec}"
    return spec or declared or "full", None


def settle(read, ok_when, timeout: float = LIST_LAG_SECONDS, step: float = LIST_LAG_STEP):
    """Call ``read`` until ``ok_when(result)`` or ``timeout`` passes; the last result."""
    deadline = time.monotonic() + timeout
    while True:
        res = read()
        if ok_when(res) or time.monotonic() >= deadline:
            return res
        time.sleep(step)


CORE_TOOLS = ("whoami", "profile_list", "profile_get", "project_get", "project_items",
              "project_item_find", "project_views_list", "list_next_actions", "issue_list",
              "issue_blocked_by_list", "item_get", "item_claim", "item_renew", "item_release",
              "item_report", "capture", "issue_comment", "issue_labels")
WHOAMI_FIELDS = ("principal", "signed_in_by", "preset", "fenced", "provider", "entrance", "expires_at",
                 "join_url", "conformance", "spec_version")
PROFILE_FIELDS = ("name", "labels", "needs", "owner_needs", "pickup_sizes", "status_for_label")
BASE_LABELS = ("run-agent", "agent-running", "waiting-for-review", "agent-failed", "blocked",
               "accepted", "needs:triage", "agent:any", "agent:human", "agent-ready",
               "agent-proposed")


class RetiredKind(Enum):
    """Kinds a profile must not declare (repo-context-and-profiles.md, Kinds; check P8)."""
    TASK = "task"
    QUESTION = "question"
    DECISION = "decision"


KIND_LABEL_PREFIX = "kind:"


def retired_kinds_in(profile: dict) -> list[str]:
    """The retired Kinds a profile declares, as labels or item types (check P8)."""
    retired = {k.value for k in RetiredKind}
    found = []
    for lbl in profile.get("labels") or []:
        name = str(lbl.get("name") if isinstance(lbl, dict) else lbl or "")
        if name.lower().startswith(KIND_LABEL_PREFIX) and \
                name[len(KIND_LABEL_PREFIX):].lower() in retired:
            found.append(f"label {name}")
    for t in profile.get("item_types") or []:
        if not isinstance(t, dict):
            continue
        for key in ("name", "issue_type"):
            if str(t.get(key) or "").lower() in retired:
                found.append(f"item type {t.get('name')} ({key} {t.get(key)})")
    return found


class StandardKind(Enum):
    """The standard Kinds (repo-context-and-profiles.md, Kinds)."""
    EPIC = "epic"
    STORY = "story"
    CHORE = "chore"
    BUG = "bug"
    SPIKE = "spike"
    RESEARCH = "research"
    FINDING = "finding"


class KindRule(Enum):
    """The parent rules, in the order a type write checks them (check K1)."""
    RETIRED = "retired-kind"
    EPIC_TOP = "epic-is-top"
    EPIC_STORIES = "epic-holds-stories"
    HOLDS_STEPS = "holds-steps"
    FINDING_NOTHING = "finding-holds-nothing"


#: Parents whose sub-issues are steps, and the standard Kind each may still hold.
STEP_PARENTS = {StandardKind.STORY: (), StandardKind.CHORE: (), StandardKind.BUG: (),
                StandardKind.SPIKE: (StandardKind.FINDING,)}


def _standard(kind: str | None) -> StandardKind | None:
    try:
        return StandardKind(str(kind or "").strip().lower())
    except ValueError:
        return None


def kind_link_rule(parent: str | None, child: str | None) -> str | None:
    """The rule a sub-issue link from ``parent`` to ``child`` breaks, or None. Kinds are
    Issue Type names or ``kind:`` label values, any case; None is no Kind."""
    p, c = _standard(parent), _standard(child)
    if c is StandardKind.EPIC:
        return KindRule.EPIC_TOP.value
    if p is StandardKind.EPIC and (c is StandardKind.FINDING or not str(child or "").strip()):
        return KindRule.EPIC_STORIES.value
    if p in STEP_PARENTS and c is not None and c not in STEP_PARENTS[p]:
        return KindRule.HOLDS_STEPS.value
    if p is StandardKind.FINDING:
        return KindRule.FINDING_NOTHING.value
    return None


def kind_type_rule(kind: str | None, parent: str | None, children: list) -> str | None:
    """The rule setting ``kind`` (None clears it) on an issue breaks, given its parent's
    Kind (None: no parent; ``""``: a parent with no Kind) and its sub-issues' Kinds."""
    if str(kind or "").strip().lower() in {k.value for k in RetiredKind}:
        return KindRule.RETIRED.value
    if parent is not None:
        rule = kind_link_rule(parent, kind)
        if rule:
            return rule
    for child in children or []:
        rule = kind_link_rule(kind, child)
        if rule:
            return rule
    return None


def reference_kind(case: dict) -> dict:
    """K1: one case of conformance/kind_cases.json, answered by the reference rules."""
    if case.get("op") == "type":
        rule = kind_type_rule(case.get("kind"), case.get("parent"), case.get("children") or [])
    else:
        rule = kind_link_rule(case.get("parent"), case.get("child"))
    return {"allowed": rule is None, "rule": rule}


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

    def na(self, cid: str, note: str) -> None:
        """Not applicable: the server does not offer what the check covers (an optional
        entrance or tool group). Unlike a skip, it does not hold a level back."""
        self.add(cid, "n/a", note)

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
        self.schemas: dict[str, dict] = {}
        self.schema_errs: list[str] = []

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
                self.schemas = {t["name"]: t.get("outputSchema") or {} for t in out}
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
        ok, structured = not res.get("isError"), res.get("structuredContent")
        if ok and self.schemas.get(name):
            errs = schema_errors(structured if structured is not None else {}, self.schemas[name])
            self.schema_errs += [f"{name}: {e}" for e in errs[:2]]
        return ok, structured, text


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
# Ready check (server-spec/ready-check.md)
# ---------------------------------------------------------------------------

#: The ready rules, in the order `missing` lists them.
READY_RULES = ("acceptance-criteria", "open-question", "unlinked-blocker", "blocker-cycle", "size")
READY_VERDICTS = ("ready", "ready-blocked", "needs-refinement")
READY_WALK_LIMIT = 50
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
_LIST_MARKER = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")
_TASK_BOX = re.compile(r"^\[[ xX]\](?:\s+|$)")
_BLOCKER_WORDS = re.compile(r"\b(?:blocked by|depends on)\b", re.IGNORECASE)
_ISSUE_REF = re.compile(
    r"https://github\.com/([\w.-]+/[\w.-]+)/issues/(\d+)|(?<![\w/])([\w.-]+/[\w.-]+)?#(\d+)\b")


def _prose_lines(body: str) -> list[str]:
    """The body's lines outside fenced code blocks."""
    out, fence = [], None  # the open fence's character and length
    for line in (body or "").splitlines():
        m = _FENCE.match(line)
        if fence is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)))
                continue
            out.append(line)
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and not m.group(2).strip():
            fence = None  # a closing fence: same character, at least as long, nothing after
    return out


def _is_criterion(line: str) -> bool:
    """A list item with text: a marker, an optional task box, then something to read."""
    m = _LIST_MARKER.match(line)
    if not m:
        return False
    text = _TASK_BOX.sub("", m.group(1).strip(), count=1)
    return bool(text.strip())


def has_acceptance_criteria(body: str) -> bool:
    """A heading starting "acceptance criteria" with a list item before the next heading
    of the same or a higher level."""
    level = None
    for line in _prose_lines(body):
        h = _HEADING.match(line)
        if h:
            depth = len(h.group(1))
            if level is not None and depth <= level:
                level = None
            if level is None and h.group(2).strip().lower().startswith("acceptance criteria"):
                level = depth
            continue
        if level is not None and _is_criterion(line):
            return True
    return False


def body_blockers(body: str, repo: str) -> list[str]:
    """`owner/repo#N` for every issue reference after "blocked by" or "depends on"."""
    refs = []
    for line in _prose_lines(body):
        m = _BLOCKER_WORDS.search(line)
        if not m:
            continue
        for r in _ISSUE_REF.finditer(line[m.end():]):
            refs.append(f"{r.group(1) or r.group(3) or repo}#{r.group(2) or r.group(4)}".lower())
    return refs


def reference_ready(issue: dict) -> dict:
    """The ready check over a plain description of an issue and its blocker graph.

    ``issue``: ``repo``, ``number``, ``body``, ``labels``, ``board`` (bool), ``size``,
    ``pickup_sizes``, ``blocked_by`` (``owner/repo#N`` of each native blocker) and
    ``issues`` (``owner/repo#N`` to ``{state, blocked_by}`` for every other issue).
    Returns ``verdict``, ``missing`` (rule names) and ``blockers`` (open ones)."""
    me = f"{issue['repo']}#{issue['number']}".lower()
    graph = {k.lower(): v for k, v in (issue.get("issues") or {}).items()}
    graph[me] = {"state": "open", "blocked_by": issue.get("blocked_by") or []}
    is_open = lambda ref: (graph.get(ref.lower()) or {}).get("state", "open") == "open"
    native = [b.lower() for b in issue.get("blocked_by") or []]
    open_blockers = [b for b in native if is_open(b)]
    labels = issue.get("labels") or []
    missing = []
    if not has_acceptance_criteria(issue.get("body") or ""):
        missing.append("acceptance-criteria")
    if any(lbl.startswith("needs:") for lbl in labels):
        missing.append("open-question")
    stray = [r for r in body_blockers(issue.get("body") or "", issue["repo"]) if r != me and r not in native]
    if stray or ("blocked" in labels and not open_blockers):
        missing.append("unlinked-blocker")
    # Walk open blockers; a node met again while still on the path is a cycle.
    state: dict[str, str] = {}
    cycle = too_big = False

    def walk(node: str) -> None:
        nonlocal cycle, too_big
        if cycle or too_big:
            return
        state[node] = "on-path"
        if len(state) >= READY_WALK_LIMIT:
            too_big = True
            return
        for nxt in (graph.get(node) or {}).get("blocked_by") or []:
            nxt = nxt.lower()
            if not is_open(nxt):
                continue
            if state.get(nxt) == "on-path":
                cycle = True
                return
            if nxt not in state:
                walk(nxt)
        state[node] = "done"
    walk(me)
    if cycle or too_big:
        missing.append("blocker-cycle")
    if not issue.get("board", True) or issue.get("size") not in (issue.get("pickup_sizes") or []):
        missing.append("size")
    verdict = "needs-refinement" if missing else "ready-blocked" if open_blockers else "ready"
    return {"verdict": verdict, "missing": missing, "blockers": open_blockers}


def ready_inputs(fixtures: dict) -> list[tuple[dict, dict, dict]]:
    """(case, input, expected) with letters turned into `owner/repo#N` and body references."""
    repo = fixtures["repo"]
    out = []
    for case in fixtures["cases"]:
        letters = sorted({"S", *case["blocked_by"], *(x for v in case["blocked_by"].values() for x in v),
                          *re.findall(r"\{(?:full|url)?#([A-Z])\}", case["body"])})
        num = {x: 100 + i for i, x in enumerate(["S"] + [x for x in letters if x != "S"])}
        def ref(x: str, num: dict = num) -> str:
            return f"{repo}#{num[x]}"
        forms = {"full": lambda x: ref(x), "url": lambda x, num=num: f"https://github.com/{repo}/issues/{num[x]}",
                 "": lambda x, num=num: f"#{num[x]}"}
        body = re.sub(r"\{(full|url)?#([A-Z])\}", lambda m, f=forms: f[m.group(1) or ""](m.group(2)), case["body"])
        closed = set(case.get("closed") or [])
        issues = {ref(x): {"state": "closed" if x in closed else "open",
                           "blocked_by": [ref(y) for y in case["blocked_by"].get(x, [])]}
                  for x in letters if x != "S"}
        inp = {"repo": repo, "number": num["S"], "body": body, "labels": case["labels"],
               "board": case.get("board", True), "size": case["size"],
               "pickup_sizes": fixtures["pickup_sizes"],
               "blocked_by": [ref(y) for y in case["blocked_by"].get("S", [])], "issues": issues}
        exp = dict(case["expect"], blockers=[ref(y) for y in case["expect"]["blockers"]])
        out.append((case, inp, exp))
    return out


def check_ready_cases(rep: Report, ready_cmd: str | None) -> None:
    """R1: the golden cases, against the reference or a server's own logic (--ready-cmd)."""
    fixtures = json.loads((HERE / "ready_cases.json").read_text())
    bad = []
    for case, inp, exp in ready_inputs(fixtures):
        if ready_cmd:
            proc = subprocess.run(ready_cmd, shell=True, input=json.dumps(inp),
                                  capture_output=True, text=True, timeout=60, check=False)
            try:
                got = json.loads(proc.stdout)
            except json.JSONDecodeError:
                bad.append(f"{case['name']}: no JSON from --ready-cmd")
                continue
        else:
            got = reference_ready(inp)
        got_missing = [m.get("rule") if isinstance(m, dict) else m for m in got.get("missing") or []]
        got_blockers = sorted(str(b).lower() for b in got.get("blockers") or [])
        if got.get("verdict") != exp["verdict"] or got_missing != exp["missing"] or \
                got_blockers != sorted(b.lower() for b in exp["blockers"]):
            bad.append(f"{case['name']} ({case['what']}): {got.get('verdict')} {got_missing} {got_blockers}")
    who = "--ready-cmd" if ready_cmd else "the reference ready check"
    rep.check("R1", not bad, "; ".join(bad[:4]), f"{len(fixtures['cases'])} cases, {who}")


KIND_CASE_KEYS = ("op", "parent", "child", "kind", "children")


def check_kind_cases(rep: Report, kind_cmd: str | None) -> None:
    """K1: the golden Kind cases, against the reference or a server's own logic (--kind-cmd)."""
    fixtures = json.loads((HERE / "kind_cases.json").read_text())
    bad = []
    for case in fixtures["cases"]:
        inp = {k: case[k] for k in KIND_CASE_KEYS if k in case}
        if kind_cmd:
            proc = subprocess.run(kind_cmd, shell=True, input=json.dumps(inp),
                                  capture_output=True, text=True, timeout=60, check=False)
            try:
                got = json.loads(proc.stdout)
            except json.JSONDecodeError:
                bad.append(f"{case['name']}: no JSON from --kind-cmd")
                continue
        else:
            got = reference_kind(inp)
        exp = case["expect"]
        if bool(got.get("allowed")) != exp["allowed"] or got.get("rule") != exp["rule"]:
            bad.append(f"{case['name']} ({case['what']}): {got.get('allowed')} {got.get('rule')}")
    who = "--kind-cmd" if kind_cmd else "the reference Kind rules"
    rep.check("K1", not bad, "; ".join(bad[:4]), f"{len(fixtures['cases'])} cases, {who}")


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
    c.no_schema = sorted(n for n, t in tools.items() if not t.get("inputSchema") or not t.get("outputSchema"))
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
        listed = c.tools()
        names = {t["name"] for t in listed}
        rank = PRESETS.index(preset)
        for t in listed:
            cls, problem = tool_class(t)
            if problem:
                bad_x2.append(f"{t['name']} {problem}")
            if PRESETS.index(cls) > rank:
                bad_x2.append(f"{t['name']} ({cls}) visible at {preset}")
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


def check_t8(rep: Report, base: str, who: dict | None) -> dict | None:
    """The unauthenticated spec-version document, and that it agrees with whoami."""
    status, _, text = http("GET", base + WELL_KNOWN)
    try:
        doc = json.loads(text) if status == 200 else None
    except json.JSONDecodeError:
        doc = None
    if not isinstance(doc, dict):
        rep.fail("T8", f"GET {WELL_KNOWN} gave {status}, not a JSON object")
        return None
    problems = [f"lacks {f}" for f in ("spec_version", "conformance", "mcp", "join_url") if f not in doc]
    version, levels = doc.get("spec_version"), doc.get("conformance")
    if not (isinstance(version, str) and SEMVER.fullmatch(version)):
        problems.append(f"spec_version {version!r} is not MAJOR.MINOR.PATCH")
    names = {lv.value for lv in Level}
    if not (isinstance(levels, list) and all(isinstance(lv, str) and lv in names for lv in levels)):
        problems.append(f"conformance {levels!r} holds unknown levels")
    elif levels and Level.CORE.value not in levels:
        problems.append(f"conformance {levels} claims a level without Core")
    if who is not None:
        for f in ("spec_version", "conformance"):
            if doc.get(f) != who.get(f):
                problems.append(f"{f} {doc.get(f)!r} differs from whoami's {who.get(f)!r}")
    rep.check("T8", not problems, "; ".join(problems),
              f"spec {version}, levels {levels}" + ("" if who is not None else " (no token: not compared)"))
    return doc


def check_t9(rep: Report, claimed: list | None) -> None:
    """Honest levels: no check of a claimed level, or of Core beneath it, failed this run."""
    if claimed is None:
        rep.skip("T9", "needs whoami or the well-known document to know the claimed levels")
        return
    failed: dict[Level, list[str]] = {}
    for r in rep.rows:
        fam = family_of(r["id"])
        if r["status"] == "FAIL" and fam in LEVEL_OF:
            failed.setdefault(LEVEL_OF[fam], []).append(r["id"])
    dishonest = []
    for name in claimed:
        level = next((lv for lv in Level if lv.value == name), None)
        ids = failed.get(level, []) + ([] if level is Level.CORE else failed.get(Level.CORE, []))
        if ids:
            dishonest.append(f"{name} (failed {', '.join(sorted(set(ids), key=report_order))})")
    rep.check("T9", not dishonest, f"claims levels it fails: {'; '.join(dishonest)}",
              f"claims {claimed or 'nothing'}; no check of those levels failed")


def spec_check_ids() -> list[str]:
    """Every check id in server-spec/conformance.md, the set a certifying run must cover."""
    table = (HERE.parent / "server-spec" / "conformance.md").read_text()
    return re.findall(rf"^\| ({CHECK_ID.pattern}) \|", table, re.M)


def claimable(rep: Report, spec_ids: list[str] | None = None) -> tuple[list[str], dict[str, list[str]]]:
    """The levels this run lets a server claim at this kit version, lowest first, and the
    manual checks a person still has to confirm for each.

    A level is claimable only when the run covered **every** check of it, and of Core
    beneath it, in the spec: each one passed, is manual, or is not applicable because the
    server does not offer that optional part; at least one passed; none failed, was
    skipped, or is missing from the run (a missing prerequisite is not a pass)."""
    ids = [cid for cid in (spec_ids if spec_ids is not None else spec_check_ids()) if cid != "T9"]
    status: dict[str, set[str]] = {}
    for r in rep.rows:
        status.setdefault(r["id"], set()).add(r["status"])
    wanted: dict[Level, list[str]] = {}
    for cid in ids:
        fam = family_of(cid)
        if fam in LEVEL_OF:
            wanted.setdefault(LEVEL_OF[fam], []).append(cid)

    def clean(level: Level) -> bool:
        need = wanted.get(level, [])
        got = [status.get(cid, set()) for cid in need]
        return bool(need) and all(s and s <= {"pass", "manual", "n/a"} for s in got) and \
            any("pass" in s for s in got)
    levels = [lv for lv in Level if clean(lv) and (lv is Level.CORE or clean(Level.CORE))]
    manual = {lv.value: sorted({cid for cid in wanted.get(lv, []) + wanted.get(Level.CORE, [])
                                if "manual" in status.get(cid, set())}, key=report_order)
              for lv in levels}
    return [lv.value for lv in levels], manual


def check_profiles(rep: Report, c: Client) -> dict:
    ok, lst, text = c.call("profile_list")
    if not ok:
        rep.fail("P1", f"profile_list: {text[:120]}")
        return {}
    names = [p["name"] if isinstance(p, dict) else p for p in (lst or {}).get("profiles") or []]
    profiles, p1, p2, p3, p8 = {}, [], [], [], []
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
        retired = retired_kinds_in(p)
        if retired:
            p8.append(f"{name}: {', '.join(retired)}")
    rep.check("P1", names and not p1, "; ".join(p1) or "no profiles", f"{len(names)} profiles")
    rep.check("P2", not p2, f"needs or owner_needs inconsistent in {', '.join(p2)}")
    rep.check("P3", not p3, f"status_for_label incomplete or off-board in {', '.join(p3)}")
    rep.check("P8", not p8, f"retired Kinds declared: {'; '.join(p8)}")
    return profiles


def fingerprint(item: dict) -> str:
    """The declaration fingerprint (repo-context-and-profiles.md, Fingerprints)."""
    body = {k: v for k, v in item.items() if k not in ("fingerprint", "manual")}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()[:12]


def profile_items(profile: dict) -> list[tuple[str, dict]]:
    board = profile.get("board") or {}
    out = [("label", x) for x in profile.get("labels") or [] if isinstance(x, dict)]
    out += [("field", x) for x in board.get("fields") or [] if isinstance(x, dict)]
    out += [("view", x) for x in board.get("views") or [] if isinstance(x, dict)]
    return out


NOTICE_FIELDS = ("kind", "name", "mode", "source", "change", "seen", "current", "declaration")


def check_customization(rep: Report, c: Client, tools: dict, profiles: dict,
                        repo: str | None, project: str | None) -> None:
    if "profile_updates" not in tools:
        for cid in ("O1", "O2", "O3"):
            rep.na(cid, "profile_updates is not offered")
        return
    bad = []
    for name, p in profiles.items():
        for kind, item in profile_items(p):
            if item.get("fingerprint") != fingerprint(item):
                bad.append(f"{name} {kind} {item.get('name')}: {item.get('fingerprint')} != {fingerprint(item)}")
    rep.check("O1", profiles and not bad, "; ".join(bad[:4]) or "no profiles",
              f"{sum(len(profile_items(p)) for p in profiles.values())} items fingerprinted")
    rep.manual("O3", "in a scratch repo, set an override with a stale seen and one skip without seen; "
                     "a reconcile plan reports the first as an upstream change, never creates the second, "
                     "and deletes nothing")
    if not repo:
        rep.skip("O2", "needs --repo")
        return
    args = {"repo": repo, **({"project": project} if project else {})}
    ok, out, text = c.call("profile_updates", args)
    if not ok or not isinstance(out, dict):
        rep.fail("O2", f"profile_updates: {text[:120]}")
        return
    missing = [k for k in ("profile", "overrides", "inferred", "updates") if k not in out]
    current = {(k, i.get("name")): i.get("fingerprint")
               for k, i in profile_items(profiles.get(out.get("profile")) or {})}
    probs = []
    for n in out.get("updates") or []:
        lack = [f for f in NOTICE_FIELDS if f not in n]
        if lack:
            probs.append(f"{n.get('name')}: lacks {', '.join(lack)}")
        elif n["mode"] not in ("skip", "keep") or n["change"] not in ("changed", "removed"):
            probs.append(f"{n['name']}: mode {n['mode']!r} or change {n['change']!r} is not allowed")
        elif n["change"] == "changed" and n["current"] != current.get((n["kind"], n["name"])):
            probs.append(f"{n['name']}: current {n['current']} is not profile_get's")
    rep.check("O2", not missing and not probs,
              f"lacks {', '.join(missing)}" if missing else "; ".join(probs[:4]),
              f"{len(out.get('updates') or [])} upstream changes for {repo}")


class Sandbox:
    """Issues the run creates in the sandbox repo, titled so a person can find them."""

    def __init__(self, c: Client, repo: str, project: str | None, run: str):
        self.c, self.repo, self.project, self.run = c, repo, project, run
        self.made: list[int] = []

    def issue(self, what: str, labels: list[str] | None = None, body: str = "") -> int:
        args = {"title": f"[conformance {self.run}] {what}", "repo": self.repo,
                "note": (body + "\n" if body else "")
                + "Created by the gtd-board-kit conformance runner. Safe to close."}
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

    def next_rows(res):
        out = res[1]
        return out if isinstance(out, list) else (out or {}).get("result") or (out or {}).get("items") or []

    ok, out, text = settle(
        lambda: c.call("list_next_actions", {"repo": repo, "context": "agent-ready", "limit": 100}),
        lambda res: not res[0] or any(r.get("number") == tag for r in next_rows(res)))
    rows = next_rows((ok, out, text))
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

    def numbers(res):
        out = res[1] or {}
        return [i.get("number") for i in (out.get("issues") or out.get("items") or [])]

    lbl = settle(lambda: c.call("issue_list", {"repo": repo, "labels": [f"needs:{owner_needs}"], "limit": 100}),
                 lambda res: not ok or not res[0] or n in numbers(res))
    ok_lbl, listed = lbl[0], numbers(lbl)
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

    # C14 several items, one branch: one claim per item, each with its own lease
    branch = f"rc/conformance-{sb.run}"
    a, b = sb.issue("branch a"), sb.issue("branch b")
    ok_bad, _, _ = c.call("item_claim", sb.args(a, basis="explicit", asked_by="conformance",
                                               branch="bad..name"))
    ok_a, out_a, t_a = c.call("item_claim", sb.args(a, basis="explicit", asked_by="conformance",
                                                   lease="30m", branch=branch))
    ok_b, out_b, t_b = c.call("item_claim", sb.args(b, basis="explicit", asked_by="conformance",
                                                   lease="45m", branch=branch))
    # Read both back through item_get: the branch must come from the fold, not the echo.
    reads = [c.call("item_get", sb.args(num))[1] for num in (a, b)]
    holder_me = ((out_a or {}).get("item") or {}).get("holder")
    on_branch = bool(holder_me) and all(
        ((o or {}).get("item") or {}).get("holder") == holder_me and
        (((o or {}).get("item") or {}).get("mandate") or {}).get("branch") == branch
        for o in [out_a, out_b, *reads])
    ok_r, _, _ = c.call("item_release", sb.args(a, done="checked", remaining="none", next="close"))
    _, out, _ = c.call("item_get", sb.args(b))
    left = (out or {}).get("item") or {}
    lease_b = (((out_b or {}).get("item") or {}).get("lease_until"))
    rep.check("C14", not ok_bad and ok_a and ok_b and on_branch and ok_r and
              left.get("holder") and left.get("lease_until") == lease_b,
              f"bad branch refused {not ok_bad}; claims {ok_a} {ok_b} ({(t_a or t_b)[:60]}); "
              f"branch recorded {on_branch}; release {ok_r}; second still held {bool(left.get('holder'))}")
    c.call("item_release", sb.args(b, done="checked", remaining="none", next="close"))

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
    # Without `project` the server checks labels only (the Size part runs in check_board).
    num = sb.issue("inferred ok", labels=["agent-ready", "agent:any"])
    ok, _, text = c.call("item_claim", {"repo": repo, "number": num, "basis": "inferred"})
    rep.check("C5", not leaked and ok, f"accepted: {', '.join(leaked) or '-'}; agent-ready claim {ok} {text[:80]}",
              "labels" if sb.project else "labels only (pass --project for the Size part)")

    # C6b closed issue: needs issue_close, an optional tool
    rep.manual("C6b", "close a claimed sandbox issue by hand, then item_release must succeed and item_claim refuse")


READY_FIELDS = ("repo", "number", "title", "verdict", "missing", "blockers", "kind", "size")
READY_AC = "## Acceptance criteria\n\n- AC1: the conformance runner sees this criterion\n"


def check_readiness(rep: Report, c: Client, tools: dict, sb: Sandbox | None, profile: dict,
                    ready_cmd: str | None) -> None:
    """R1 to R7: item_ready, when the server offers it (server-spec/ready-check.md)."""
    ids = ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8")
    if "item_ready" not in tools:
        for cid in ids:
            rep.na(cid, "item_ready is not offered")
        return
    if ready_cmd:
        check_ready_cases(rep, ready_cmd)
    else:
        rep.manual("R1", "run the golden cases against the server's own rules: --ready-cmd CMD")
    if sb is None:
        for cid in ids[1:]:
            rep.skip(cid, "needs --repo")
        return
    owner_needs = profile.get("owner_needs") or "triage"
    sizes = profile.get("pickup_sizes") or []

    def ready(n: int) -> tuple[bool, dict, str]:
        ok, out, text = c.call("item_ready", sb.args(n))
        return ok, out if isinstance(out, dict) else {}, text

    def rules(out: dict) -> list[str]:
        return [m.get("rule") if isinstance(m, dict) else m for m in out.get("missing") or []]

    def sized(n: int, size: str | None) -> None:
        if sb.project:
            c.call("project_set_field", sb.args(n, field="Size", **({"value": size} if size else {"clear": True})))

    # R2: shape, and a story with criteria and an allowed Size is ready.
    n = sb.issue("ready", body=READY_AC)
    sized(n, sizes[0] if sizes else None)
    ok, out, text = ready(n)
    shape = [f for f in READY_FIELDS if f not in out]
    bad_rules = [r for r in rules(out) if r not in READY_RULES]
    if not ok or shape or out.get("verdict") not in READY_VERDICTS or bad_rules:
        rep.fail("R2", f"item_ready: {text[:80] if not ok else ''} lacks {shape}, verdict "
                       f"{out.get('verdict')!r}, unknown rules {bad_rules}")
    elif sb.project and sizes:
        rep.check("R2", out["verdict"] == "ready", f"criteria and Size {sizes[0]}: {out['verdict']} {rules(out)}")
    else:
        rep.ok("R2", "shape only (pass --project, with pickup_sizes on its Size field, for the ready case)")

    # R3: it writes nothing. Off-board stays off-board; the claim state is unchanged.
    n = sb.issue("read only", body=READY_AC, labels=["blocked"])
    before = c.call("item_get", sb.args(n))[1]
    on_board = c.call("project_item_find", sb.args(n))[0] if sb.project else None
    ready(n)
    ready(n)
    after = c.call("item_get", sb.args(n))[1]
    still = c.call("project_item_find", sb.args(n))[0] if sb.project else None
    keep = lambda x: {k: v for k, v in ((x or {}).get("item") or {}).items() if k not in ("stale", "now")}
    rep.check("R3", keep(before) == keep(after) and on_board == still,
              f"item_get changed {keep(before) != keep(after)}; board item before {on_board}, after {still}",
              "claim state unchanged" + ("; an off-board issue stayed off the board" if sb.project else ""))

    # R4: missing criteria, and an open question.
    n1 = sb.issue("no criteria", body="Make the thing work.\n")
    n2 = sb.issue("question", body=READY_AC, labels=[f"needs:{owner_needs}"])
    r1, r2 = rules(ready(n1)[1]), rules(ready(n2)[1])
    rep.check("R4", "acceptance-criteria" in r1 and "acceptance-criteria" not in r2 and "open-question" in r2,
              f"no criteria gave {r1}; needs:{owner_needs} gave {r2}")

    # R5: blockers named but not linked, linked, and a cycle.
    b = sb.issue("blocker", body=READY_AC)
    n1 = sb.issue("unlinked", body=READY_AC + f"\nBlocked by #{b}.\n")
    n2 = sb.issue("blocked label", body=READY_AC, labels=["blocked"])
    r1, r2 = rules(ready(n1)[1]), rules(ready(n2)[1])
    probs = [] if "unlinked-blocker" in r1 and "unlinked-blocker" in r2 else [f"unlinked gave {r1}, {r2}"]
    if "issue_blocked_by_add" in tools:
        link = lambda x, y: c.call("issue_blocked_by_add", {"repo": sb.repo, "number": x,
                                                            "blocker": y, "blocker_repo": sb.repo})
        okl, _, tl = link(n1, b)
        _, out, _ = ready(n1)
        listed = [x.get("number") for x in out.get("blockers") or [] if isinstance(x, dict)]
        if not okl or "unlinked-blocker" in rules(out) or b not in listed:
            probs.append(f"linked: {tl[:60] if not okl else ''} rules {rules(out)}, blockers {listed}")
        okc, _, tc = link(b, n1)
        r3 = rules(ready(n1)[1])
        if not okc or "blocker-cycle" not in r3:
            probs.append(f"cycle: {tc[:60] if not okc else ''} rules {r3}")
        rep.check("R5", not probs, "; ".join(probs), "unlinked, linked and cycle")
    elif probs:
        rep.fail("R5", "; ".join(probs))
    else:
        rep.manual("R5", "issue_blocked_by_add is not offered: link a blocker by hand (it is listed and "
                         "the unlinked rule passes), then link back (blocker-cycle)")

    # R6: Size.
    if not sb.project:
        rep.skip("R6", "needs --project")
    else:
        n1 = sb.issue("no size", body=READY_AC)
        sized(n1, None)
        cases = [("no Size", rules(ready(n1)[1]))]
        ok, board, _ = c.call("project_get", {"project": sb.project})
        field = next((f for f in (board or {}).get("fields") or [] if f.get("name") == "Size"), None)
        other = [o.get("name") if isinstance(o, dict) else o for o in (field or {}).get("options") or []]
        other = [o for o in other if o not in sizes]
        if other:
            n2 = sb.issue("large", body=READY_AC)
            sized(n2, other[0])
            cases.append((f"Size {other[0]}", rules(ready(n2)[1])))
        wrong = [f"{what}: {got}" for what, got in cases if "size" not in got]
        rep.check("R6", not wrong, "; ".join(wrong), f"{len(cases)} cases")

    # R7: refusals.
    if "issue_close" in tools:
        n = sb.issue("closed", body=READY_AC)
        c.call("issue_close", {"repo": sb.repo, "number": n, "reason": "not_planned"})
        ok, _, _ = ready(n)
        rep.check("R7", not ok, "a closed issue was not refused", "closed issue refused; PR and epic by hand")
    rep.manual("R7", "item_ready on a pull request number and on an issue of Kind epic: both refuse")

    # R8: the claim returns the same verdict, warns when not ready, and never refuses on it.
    def claim_ready(n: int) -> list[str]:
        _, want, _ = ready(n)
        ok, out, text = c.call("item_claim", sb.args(n, asked_by="conformance", basis="explicit", lease="90m"))
        if not ok:
            return [f"#{n}: claim refused: {text[:80]}"]
        got = (out or {}).get("ready")
        c.call("item_release", sb.args(n, done="conformance R8", remaining="none", next="close"))
        if not isinstance(got, dict):
            return [f"#{n}: no ready in the claim"]
        num = lambda bs: sorted(b.get("number") if isinstance(b, dict) else b for b in bs or [])
        probs = []
        if got.get("verdict") != want.get("verdict") or rules(got) != rules(want) or \
                num(got.get("blockers")) != num(want.get("blockers")):
            probs.append(f"#{n}: claim says {got.get('verdict')} {rules(got)}, "
                         f"item_ready {want.get('verdict')} {rules(want)}")
        warned = any(str(want.get("verdict")) in str(w) for w in (out or {}).get("warnings") or [])
        if want.get("verdict") != "ready" and not warned:
            probs.append(f"#{n}: {want.get('verdict')} but no warning names it")
        if want.get("verdict") == "ready" and any("not ready" in str(w) for w in out.get("warnings") or []):
            probs.append(f"#{n}: ready but warned not ready")
        return probs

    n1 = sb.issue("claim not ready", body="Make the thing work.\n")
    n2 = sb.issue("claim ready", body=READY_AC)
    sized(n2, sizes[0] if sizes else None)
    probs = claim_ready(n1) + claim_ready(n2)
    rep.check("R8", not probs, "; ".join(probs[:3]), "verdict matches item_ready; not ready warns, never refuses")


KIND_TYPES = ("Epic", "Story", "Chore", "Spike", "Finding")


def check_kinds(rep: Report, c: Client, tools: dict, sb: Sandbox | None, kind_cmd: str | None) -> None:
    """K1 to K4: Kind and parent rules, when the server offers the Issue structure tools."""
    ids = ("K1", "K2", "K3", "K4")
    if "sub_issue_add" not in tools and "issue_type_set" not in tools:
        for cid in ids:
            rep.na(cid, "the Issue structure tools are not offered")
        return
    if kind_cmd:
        check_kind_cases(rep, kind_cmd)
    else:
        rep.manual("K1", "run the golden Kind cases against the server's own rules: --kind-cmd CMD")
    if sb is None:
        for cid in ids[1:]:
            rep.skip(cid, "needs --repo")
        return

    def set_type(n: int, name: str | None) -> tuple[bool, str]:
        args = {"repo": sb.repo, "number": n, **({"issue_type": name} if name else {"clear": True})}
        ok, _, text = c.call("issue_type_set", args)
        return ok, text

    def link(parent: int, child: int) -> tuple[bool, str]:
        ok, _, text = c.call("sub_issue_add", {"repo": sb.repo, "parent": parent, "child": child})
        return ok, text

    def children(parent: int) -> list:
        _, out, _ = c.call("sub_issues_list", {"repo": sb.repo, "number": parent})
        return [x.get("number") for x in (out or {}).get("children") or [] if isinstance(x, dict)]

    # K2: a retired Kind refuses, naming the rule, whether or not the owner has that type.
    n = sb.issue("retired kind")
    wrong = []
    for name in ("Task", "question", "DECISION"):
        ok, text = set_type(n, name)
        if ok or "retired-kind" not in text:
            wrong.append(f"{name}: {'set' if ok else text[:60]}")
    rep.check("K2", not wrong, "; ".join(wrong), "Task, question and DECISION refused as retired-kind")

    made = {}
    for name in KIND_TYPES:
        made[name] = sb.issue(f"kind {name.lower()}")
        ok, text = set_type(made[name], name)
        if not ok:
            for cid in ids[2:]:
                rep.skip(cid, f"the sandbox owner has no Issue Type {name} ({text[:60]}); "
                              f"K3 and K4 need {', '.join(KIND_TYPES)}")
            return
    epic, story, chore, finding = made["Epic"], made["Story"], made["Chore"], made["Finding"]
    step, step2 = sb.issue("step"), sb.issue("step 2")

    # K3: allowed links succeed; each forbidden one refuses, names its rule, links nothing.
    probs = []
    for parent, child, rule in ((epic, story, None), (epic, step, "epic-holds-stories"),
                                (story, chore, "holds-steps"), (story, step, None),
                                (story, epic, "epic-is-top"), (finding, step2, "finding-holds-nothing")):
        ok, text = link(parent, child)
        if rule is None and not ok:
            probs.append(f"#{parent} > #{child} refused: {text[:60]}")
        elif rule and (ok or rule not in text or child in children(parent)):
            probs.append(f"#{parent} > #{child}: wanted {rule}, got {'a link' if ok else text[:60]}")
    rep.check("K3", not probs, "; ".join(probs[:3]), "two links made; four refused, each naming its rule")

    # K4: issue_type_set checks the new Kind against the parent and the sub-issues.
    probs = []
    for n, name, rule in ((story, "Finding", "epic-holds-stories"), (step, "Chore", "holds-steps"),
                          (story, "Epic", "epic-is-top")):
        ok, text = set_type(n, name)
        if ok or rule not in text:
            probs.append(f"#{n} to {name}: wanted {rule}, got {'set' if ok else text[:60]}")
    if "item_ready" in tools:
        _, out, _ = c.call("item_ready", sb.args(story))
        if isinstance(out, dict) and out.get("kind") not in (None, "story"):
            probs.append(f"a refused write changed #{story}'s Kind to {out.get('kind')}")
    rep.check("K4", not probs, "; ".join(probs[:3]), "three type changes refused, each naming its rule")


def check_size(rep: Report, c: Client, sb: Sandbox, profile: dict) -> None:
    """C5, Size part: with `project`, an inferred claim needs a Size in the profile's pickup_sizes."""
    ok, board, _text = c.call("project_get", {"project": sb.project})
    size = next((f for f in (board or {}).get("fields") or [] if f.get("name") == "Size"), None)
    options = [o.get("name") if isinstance(o, dict) else o for o in (size or {}).get("options") or []]
    allowed = [o for o in options if o in (profile.get("pickup_sizes") or [])]
    other = [o for o in options if o not in allowed]
    if not ok or not allowed:
        rep.skip("C5", f"Size part: the board has no Size option in pickup_sizes {profile.get('pickup_sizes')}")
        return
    cases = [("no Size", None, False), ("allowed Size", allowed[0], True)]
    if other:
        cases.append((f"Size {other[0]}", other[0], False))
    wrong = []
    for what, value, want in cases:
        n = sb.issue(f"inferred {what}", labels=["agent-ready", "agent:any"])
        if value is None:
            c.call("project_set_field", sb.args(n, field="Size", clear=True))
        else:
            c.call("project_set_field", sb.args(n, field="Size", value=value))
        got, _, msg = c.call("item_claim", sb.args(n, basis="inferred"))
        if got != want:
            wrong.append(f"{what}: {'accepted' if got else 'refused ' + msg[:60]}")
        if got:
            c.call("item_release", sb.args(n, done="size check", remaining="none", next="close"))
    rep.check("C5", not wrong, f"Size part: {'; '.join(wrong)}", f"Size part: {len(cases)} cases")


def check_board(rep: Report, c: Client, sb: Sandbox, profile: dict) -> None:
    proj = sb.project
    check_size(rep, c, sb, profile)
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


#: The provenance marker ``pr_open`` writes at the end of a PR body (tools.md).
PR_MARKER_RE = re.compile(r"<!--\s*gtd-pr\s+v1\s+(\{.*?\})\s*-->", re.DOTALL)


def check_prs(rep: Report, c: Client, sb: Sandbox, tools: dict, who: dict | None,
              head: str | None) -> None:
    """PR1 to PR3: ``pr_open`` refusals, then (with a pushed ``head``) one real PR."""
    if "pr_open" not in tools:
        for cid in ("PR1", "PR2", "PR3"):
            rep.na(cid, "pr_open is not offered")
        return
    owner = sb.repo.split("/")[0]
    n = sb.issue("pr_open")
    ok, _, text = c.call("item_claim", sb.args(n, basis="explicit", asked_by="conformance", lease="30m"))
    if not ok:
        for cid in ("PR1", "PR2", "PR3"):
            rep.skip(cid, f"could not claim the sandbox issue: {text[:100]}")
        return

    def pr(**more: Any) -> tuple[bool, Any, str]:
        args = {"repo": sb.repo, "title": f"[conformance {sb.run}] pr_open",
                "body": "Opened by the gtd-board-kit conformance runner. Safe to close.",
                "issues": [n], **more}
        return c.call("pr_open", args)

    missing = f"gtd-conformance-no-such-branch-{sb.run}"
    bad = []
    for label, args in (("cross-repository head", {"head": f"{owner}-other:{missing}"}),
                        ("head equal to base", {"head": "main", "base": "main"}),
                        ("missing branch", {"head": missing})):
        ok, _, _ = pr(**args)
        if ok:
            bad.append(label)
    rep.check("PR1", not bad, f"not refused: {', '.join(bad)}", "three bad heads refused")

    other = sb.issue("pr_open unclaimed")
    bad = []
    # A refusal counts only when it gives the reason PR2 checks: every probe uses a missing
    # branch, so a server without these checks would otherwise pass on the branch alone.
    ok, _, text = pr(head=missing, issues=[])
    if ok or "issues" not in text:
        bad.append("empty issues was not refused for its issues")
    ok, _, text = pr(head=missing, issues=[n, other])
    if ok or str(other) not in text:
        bad.append(f"an unclaimed issue (#{other}) was not refused by name")
    ok, _, text = pr(head=missing, body='x <!-- gtd-pr v1 {"by": "agent:x", "issues": [1], "v": 1} -->')
    if ok or "gtd-pr" not in text:
        bad.append("a body with a gtd-pr marker was not refused for the marker")
    rep.check("PR2", not bad, "; ".join(bad), "empty issues, an unclaimed issue and a marker refused")

    if not head:
        rep.manual("PR3", "push a branch to the sandbox repo and run again with --pr-head BRANCH")
    else:
        ok, out, text = pr(head=head)
        out = out if isinstance(out, dict) else {}
        principal = (who or {}).get("principal")
        probs = []
        if not ok:
            probs.append(f"pr_open: {text[:120]}")
        else:
            author = str(out.get("author") or "")
            if not author.endswith("[bot]"):
                probs.append(f"author {author!r} is not an App")
            if out.get("by") != principal:
                probs.append(f"by {out.get('by')!r} is not {principal!r}")
            ok2, _, text2 = c.call("pr_open", {"repo": sb.repo, "head": head, "title": "again",
                                               "body": "second", "issues": [n]})
            if ok2:
                probs.append("a second pr_open for the same head was not refused")
            elif out.get("url") and out["url"] not in text2:
                probs.append("the second refusal does not give the open PR's URL")
            body = str(out.get("body") or "")
            marks = PR_MARKER_RE.findall(body)
            try:
                got = json.loads(marks[0]) if len(marks) == 1 else None
            except json.JSONDecodeError:
                got = None
            if not got or not body.rstrip().endswith("-->"):
                probs.append("the body does not end with exactly one gtd-pr marker")
            elif got.get("by") != principal or got.get("issues") != [n]:
                probs.append(f"marker by/issues {got.get('by')!r}/{got.get('issues')!r}")
            if out.get("closes") is not False or "Closes #" in body:
                probs.append("a PR opened without closes would close its issues")
            print(f"note: close PR {out.get('url')} by hand", file=sys.stderr)
        rep.check("PR3", not probs, "; ".join(probs), f"opened {out.get('url')} as {out.get('author')}")
    c.call("item_release", sb.args(n, done="pr_open checks", remaining="none", next="close"))


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
        wait = int(grant.get("interval") or 5)
        for _ in range(3):
            time.sleep(wait)
            s, _, text = http("POST", f"{base}/join/token", {"device_code": grant["device_code"]})
            if "slow_down" not in text:
                break
            wait += 5  # RFC 8628: slow_down adds five seconds to the interval
        rep.check("J3", "authorization_pending" in text, f"poll gave {s}: {text[:80]}",
                  "pending; the request expires on its own")


# ---------------------------------------------------------------------------
# Join: entrances (J11) and the connector entrance (JC1 to JC9)
# ---------------------------------------------------------------------------

def join_entrances(base: str) -> set[str] | None:
    """The entrances /join lists on its `Entrances:` line, or None when there is no such line."""
    s, _, text = http("GET", f"{base}/join")
    lines = re.findall(r"^\s*Entrances:\s*(.+)$", text, re.MULTILINE) if s == 200 else []
    if len(lines) != 1:
        return None  # J11 wants exactly one such line
    return {e.strip().lower() for e in lines[0].split(",") if e.strip()}


def check_j11(rep: Report, entrances: set[str] | None, claims_join: bool | None, who: dict | None) -> None:
    if entrances is None and not claims_join:
        rep.skip("J11", "the join routes are off on this server (no Join level)")
        return
    joined = (who or {}).get("signed_in_by") == "joined"
    entrance_ok = not joined or (who or {}).get("entrance") in (entrances or set())
    rep.check("J11", bool(entrances) and "device-code" in entrances and entrance_ok,
              f"/join entrances {sorted(entrances) if entrances else 'not listed'}; "
              f"whoami entrance {(who or {}).get('entrance')!r}",
              f"entrances {', '.join(sorted(entrances or ()))}"
              + (f"; whoami entrance {who.get('entrance')}" if joined else ""))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def http_noredirect(url: str, form: dict | None = None) -> tuple[int, dict]:
    """GET (or a form POST) that reports a redirect instead of following it."""
    data = urllib.parse.urlencode(form).encode() if form is not None else None
    try:
        with urllib.request.build_opener(_NoRedirect).open(url, data=data, timeout=60) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


class Loopback:
    """A one-shot redirect target on localhost (RFC 8252) that keeps the query it receives."""

    def __init__(self) -> None:
        got: queue.Queue = queue.Queue()

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a: Any) -> None:
                pass

            def do_GET(self) -> None:
                got.put(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query))
                body = b"The conformance runner has the answer. You can close this tab."
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self.server = HTTPServer(("localhost", 0), H)
        self.uri = f"http://localhost:{self.server.server_address[1]}/callback"
        self.got = got
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def wait(self, seconds: float) -> dict | None:
        try:
            return self.got.get(timeout=seconds)
        except queue.Empty:
            return None

    def close(self) -> None:
        self.server.shutdown()


def oauth_metadata(base: str) -> dict:
    """RFC 9728 resource metadata, then RFC 8414 authorization-server metadata."""
    res = {}
    for url in (f"{base}/.well-known/oauth-protected-resource/mcp", f"{base}/.well-known/oauth-protected-resource"):
        s, _, text = http("GET", url)
        if s == 200:
            res = json.loads(text)
            break
    issuer = ((res.get("authorization_servers") or [base])[0]).rstrip("/")
    for url in (f"{issuer}/.well-known/oauth-authorization-server", f"{base}/.well-known/oauth-authorization-server"):
        s, _, text = http("GET", url)
        if s == 200:
            return json.loads(text)
    raise CheckError("no OAuth authorization-server metadata")


def token_call(meta: dict, form: dict) -> tuple[int, dict]:
    s, _, text = http("POST", meta["token_endpoint"], form, form=True)
    try:
        return s, json.loads(text)
    except json.JSONDecodeError:
        return s, {"error": text[:80]}


JC_MANUAL = {
    "JC2": "deny a second connector sign-in: the client gets error=access_denied with its state, and no agent appears",
    "JC3": "leave a code unredeemed for more than 5 minutes: the token endpoint refuses it",
    "JC5": "open /join/agents as an approver: the connector agent is listed with entrance connector",
    "JC6": "present a replaced connector refresh token after the grace window: invalid_grant and the agent is "
           "revoked; a day later (access token ended), a refresh returns a new access token that works",
    "JC7": "after the approval's end the connector refresh answers invalid_grant",
    "JC8": "re-join the same name with the device code: the connector agent's token and refresh stop working; "
           "and the reverse",
    "JC9": "sign in as a non-approver account and POST /join/decide for a connect id: refused",
}
JC_IDS = [f"JC{i}" for i in range(1, 10)]


def check_connector(rep: Report, base: str, entrances: set[str] | None, name: str | None,
                    wait: float, seen: list[str], secrets: list[str]) -> None:
    if not entrances or "connector" not in entrances:
        for cid in JC_IDS:
            rep.na(cid, "the connector entrance is not offered on /join")
        return
    if not name:
        for cid in JC_IDS:
            rep.skip(cid, "pass --connector NAME (a person approves one sign-in in a browser)")
        return
    for cid, how in JC_MANUAL.items():
        rep.manual(cid, how)
    meta = oauth_metadata(base)
    if not meta.get("registration_endpoint"):
        rep.fail("JC1", "the authorization server offers no dynamic registration")
        return
    cb = Loopback()
    try:
        _connector_run(rep, base, meta, cb, name, wait, seen, secrets)
    finally:
        cb.close()


def _register(meta: dict, redirect: str, label: str) -> str:
    s, _, text = http("POST", meta["registration_endpoint"], {
        "client_name": f"gtd-conformance {label}", "redirect_uris": [redirect],
        "grant_types": ["authorization_code", "refresh_token"], "response_types": ["code"],
        "token_endpoint_auth_method": "none"})
    if s not in (200, 201):
        raise CheckError(f"registration with a loopback redirect refused: {s} {text[:100]}")
    return json.loads(text)["client_id"]


def _connector_run(rep: Report, base: str, meta: dict, cb: Loopback, name: str, wait: float,
                   seen: list[str], secrets: list[str]) -> None:
    client_a = _register(meta, cb.uri, "a")
    client_b = _register(meta, cb.uri, "b")
    verifier = _b64url(os.urandom(48))
    state = _b64url(os.urandom(12))
    query = {"response_type": "code", "client_id": client_a, "redirect_uri": cb.uri, "state": state,
             "code_challenge": _b64url(hashlib.sha256(verifier.encode()).digest()),
             "code_challenge_method": "S256", "resource": f"{base}/mcp?agent={name}"}
    if meta.get("scopes_supported"):
        query["scope"] = " ".join(meta["scopes_supported"])
    s, hdrs = http_noredirect(f"{meta['authorization_endpoint']}?{urllib.parse.urlencode(query)}")
    location = urllib.parse.urljoin(base + "/", hdrs.get("location", ""))
    loc = urllib.parse.urlparse(location)
    connect = (urllib.parse.parse_qs(loc.query).get("connect") or [""])[0]
    _, _, page = http("GET", location) if connect else (0, {}, "")
    # The page may sign the approver in first (agent-join.md), so the name is checked only
    # when it is shown before sign-in; otherwise the approving person checks it.
    shown = "agent name shown before sign-in" if name in page else "approver checks the prefilled name"
    rep.check("JC1", s in (302, 303, 307) and loc.path.endswith("/join/approve") and bool(connect),
              f"/authorize gave {s} to {loc.path or '-'}; connect id {'present' if connect else 'missing'}",
              f"loopback registered; to /join/approve?connect=...; {shown}")
    if not connect:
        return

    # JC9 (automated part): no session, no CSRF token, or a forged one.
    refused = []
    for form in ({"connect": connect, "decision": "approve", "name": name, "preset": "desk"},
                 {"connect": connect, "decision": "approve", "name": name, "preset": "desk", "csrf": "forged"}):
        s9, h9 = http_noredirect(f"{base}/join/decide", form)
        to_client = h9.get("location", "").startswith(cb.uri)
        refused.append(s9 >= 400 or (s9 in (302, 303) and not to_client))
    early = cb.wait(0.5)
    rep.check("JC9", all(refused) and early is None, "a decide without an approver session was not refused",
              "no session and forged CSRF refused (non-approver: by hand)")

    print(f"\nACTION: open this link in a browser, sign in as an approver, choose to sign in as an agent,\n"
          f"and approve '{name}' at preset desk; check that the card shows that name. The runner waits {int(wait)} s.\n\n  {location}\n",
          file=sys.stderr, flush=True)
    answer = cb.wait(wait)
    if answer is None:
        for cid in ("JC2", "JC3", "JC4", "JC6", "JC7"):
            rep.fail(cid, "no approval reached the loopback redirect in time")
        return
    code = (answer.get("code") or [""])[0]
    rep.check("JC2", bool(code) and answer.get("state") == [state],
              f"redirect gave {sorted(answer)}; state {'unchanged' if answer.get('state') == [state] else 'changed'}",
              "code and state unchanged (deny: by hand)")
    if not code:
        return

    form = {"grant_type": "authorization_code", "code": code, "redirect_uri": cb.uri}
    s_other, _ = token_call(meta, {**form, "client_id": client_b, "code_verifier": verifier})
    s_bad, _ = token_call(meta, {**form, "client_id": client_a, "code_verifier": verifier[::-1]})
    s_ok, grant = token_call(meta, {**form, "client_id": client_a, "code_verifier": verifier})
    s_again, _ = token_call(meta, {**form, "client_id": client_a, "code_verifier": verifier})
    rep.check("JC3", s_other >= 400 and s_bad >= 400 and s_ok == 200 and s_again >= 400,
              f"other client {s_other}, wrong verifier {s_bad}, right {s_ok}, again {s_again}",
              "once, own client, right verifier (expiry: by hand)")
    access, refresh = grant.get("access_token"), grant.get("refresh_token")
    if s_ok != 200 or not access or not refresh:
        return
    secrets += [access, refresh]
    extra = [k for k in grant if "token" in k and k not in ("access_token", "refresh_token", "token_type")]
    c = Client(base, access, seen)
    c.initialize()
    ok, who, text = c.call("whoami")
    tools = {t["name"] for t in c.tools()}
    who = who or {}
    rep.check("JC4", ok and not extra and who.get("principal") == f"agent:{name}"
              and who.get("entrance") == "connector" and who.get("preset") == "desk"
              and who.get("fenced") is True and "item_claim" not in tools,
              f"extra token fields {extra}; whoami {who.get('principal')} entrance {who.get('entrance')} "
              f"preset {who.get('preset')} fenced {who.get('fenced')}; work tools listed {'item_claim' in tools}"
              f"{'' if ok else '; ' + text[:60]}",
              f"agent:{name} at desk, entrance connector, fenced")

    # JC6 (automated part): a refresh rotates the connector refresh token; two racing
    # refreshes with the same token get the same answer and the agent stays live.
    rform = {"grant_type": "refresh_token", "refresh_token": refresh, "client_id": client_a}
    results: list[tuple[int, dict]] = []
    threads = [threading.Thread(target=lambda: results.append(token_call(meta, rform))) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    grants = [g for s6, g in results if s6 == 200]
    fresh = [g.get("access_token") for g in grants]
    new_refresh = [g.get("refresh_token") for g in grants]
    secrets += [t for t in fresh + new_refresh if t]
    same = len(grants) == 2 and fresh[0] == fresh[1] and new_refresh[0] == new_refresh[1]
    rotated = bool(new_refresh) and all(r and r != refresh for r in new_refresh)
    live = []
    for t in set(filter(None, fresh)):
        try:
            cl = Client(base, t, seen)
            cl.initialize()
            live.append(cl.call("whoami")[0])
        except CheckError:
            live.append(False)
    rep.check("JC6", same and rotated and bool(live) and all(live),
              f"racing refreshes gave {[s6 for s6, _ in results]}; same answer {same}; "
              f"refresh token rotated {rotated}; access working {live}",
              "rotates, racing refreshes agree, agent live (grace-window replay, after 24 h: by hand)")
    if grants:
        access, refresh = fresh[0] or access, new_refresh[0] or refresh
    rform = {**rform, "refresh_token": refresh}  # chain with the latest token

    # JC7 (automated part): client binding, then RFC 7009 revocation ends the agent.
    s_b, g_b = token_call(meta, {**rform, "client_id": client_b})
    if not meta.get("revocation_endpoint"):
        rep.check("JC7", s_b >= 400, f"another client's refresh gave {s_b}",
                  "bound to its client; no revocation endpoint, so revoke at /join/agents by hand")
        print(f"note: revoke agent:{name} at {base}/join/agents", file=sys.stderr)
        return
    http("POST", meta["revocation_endpoint"],
         {"token": refresh, "token_type_hint": "refresh_token", "client_id": client_a}, form=True)
    s_after, g_after = token_call(meta, rform)
    try:
        cl = Client(base, access, seen)
        cl.initialize()
        still = cl.call("whoami")[0]
    except CheckError:
        still = False
    rep.check("JC7", s_b >= 400 and s_after >= 400 and g_after.get("error") == "invalid_grant" and not still,
              f"other client {s_b} {g_b.get('error')}; after revoke refresh {s_after} {g_after.get('error')}, "
              f"access token {'still works' if still else 'refused'}",
              "bound to its client; revoked via RFC 7009 (approval end: by hand)")


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
    ap.add_argument("--pr-head", help="a branch pushed to the sandbox repo, for PR3 (opens one PR)")
    ap.add_argument("--join-start", action="store_true", help="open one join request for J2 and J3")
    ap.add_argument("--connector", metavar="NAME",
                    help="join agent NAME through the connector entrance for JC1 to JC9; "
                         "a person approves once in a browser")
    ap.add_argument("--connector-wait", type=float, default=600,
                    help="seconds to wait for that approval (default 600)")
    ap.add_argument("--fold-cmd", help="a command that folds {now, comments} from stdin to JSON on stdout")
    ap.add_argument("--ready-cmd", help="a command that runs the ready check on one case from stdin (R1)")
    ap.add_argument("--kind-cmd", help="a command that answers one Kind rule case from stdin (K1)")
    ap.add_argument("--json", help="also write the report as JSON to this file")
    a = ap.parse_args(argv)

    rep = Report()
    check_fold(rep, a.fold_cmd)
    if not a.server:
        check_ready_cases(rep, a.ready_cmd)
        check_kind_cases(rep, a.kind_cmd)
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
        who = None
        if t1:
            c = Client(base, t1, seen)
            try:
                who, _tools = check_identity(rep, c)
                claims_join = Level.JOIN.value in (who.get("conformance") or [])
                profiles = check_profiles(rep, c)
                check_customization(rep, c, _tools, profiles, a.repo, a.project)
                presets = {}
                for spec in a.preset_token:
                    p, _, env = spec.partition("=")
                    presets[p] = token(env)
                check_presets(rep, base, presets, seen)
                name = a.profile or next(iter(profiles), None)
                sb = None
                if a.repo:
                    c2 = Client(base, token(a.token_b_env), seen) if a.token_b_env else None
                    if c2:
                        c2.initialize()
                    sb = Sandbox(c, a.repo, a.project, datetime.now(timezone.utc).strftime("%m%d-%H%M"))
                    check_repo(rep, c, c2, sb, profiles.get(name) or {}, who)
                    if a.project:
                        check_board(rep, c, sb, profiles.get(name) or {})
                    check_prs(rep, c, sb, _tools, who, a.pr_head)
                check_readiness(rep, c, _tools, sb, profiles.get(name) or {}, a.ready_cmd)
                check_kinds(rep, c, _tools, sb, a.kind_cmd)
                if sb:
                    print(f"note: created issues {', '.join('#' + str(x) for x in sb.made)} in {a.repo}",
                          file=sys.stderr)
            except CheckError as e:
                rep.fail(Family.RUN.value, f"stopped: {e}")
            # T3 last, so every structured result of the run has been validated.
            if c.schemas:
                ns = getattr(c, "no_schema", [])
                rep.check("T3", not ns and not c.schema_errs,
                          f"no input or output schema: {', '.join(ns[:12]) or '-'}; "
                          f"invalid results: {'; '.join(c.schema_errs[:4]) or '-'}",
                          f"{len(c.schemas)} tools; every structured result of the run validated")
        doc = check_t8(rep, base, who)
        if claims_join is None and doc is not None and isinstance(doc.get("conformance"), list):
            claims_join = Level.JOIN.value in doc["conformance"]
        check_join(rep, base, a.join_start, claims_join)
        entrances = join_entrances(base)
        check_j11(rep, entrances, claims_join, who)
        try:
            check_connector(rep, base, entrances, a.connector, a.connector_wait, seen, secrets)
        except CheckError as e:
            rep.fail("JC1", f"stopped: {e}")
    for cid, how in MANUAL.items():
        rep.manual(cid, how)
    if secrets:
        leaked = [s for s in secrets if any(s in body for body in seen)]
        rep.check("X1", not leaked, "a token the runner sent came back in a response body",
                  f"{len(seen)} responses scanned")

    if a.server:
        claimed = (who or {}).get("conformance") if who else (doc or {}).get("conformance")
        check_t9(rep, claimed if isinstance(claimed, list) else None)

    rows = sorted(rep.rows, key=lambda r: report_order(r["id"]))
    width = max(len(r["id"]) for r in rows)
    for r in rows:
        print(f"{r['id']:<{width}}  {r['status']:<6}  {r['note']}")
    counts = {s: sum(r["status"] == s for r in rows) for s in ("pass", "FAIL", "skip", "manual", "n/a")}
    print(", ".join(f"{v} {k}" for k, v in counts.items()))
    kit_version = (HERE.parent / "VERSION").read_text().strip()
    levels, manual = claimable(rep)
    print(f"claimable at kit {kit_version}: {', '.join(levels) or 'nothing'}"
          + "".join(f"\n  {lv}: confirm by hand {', '.join(ids)}" for lv, ids in manual.items() if ids))
    if a.json:
        Path(a.json).write_text(json.dumps({"rows": rows, "counts": counts, "kit_version": kit_version,
                                           "claimable": levels, "manual": manual}, indent=2))
    return 1 if rep.failed() else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
