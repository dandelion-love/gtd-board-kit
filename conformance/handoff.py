"""Reference for the milestone handoff contract (server-spec/milestone-handoff.md), for checks
MH1 to MH8. Standard library only. A server copies this file and holds its copy to
conformance/handoff_cases.json.

    validate(record)            -> list of problems ([] = a valid handoff record)
    run_head(events, roles)     -> {"outcomes": [...], "heads": {milestone: {handoff_id, revision}}}
    route(case)                 -> {"binding": id or None, "rule": refusal or None}
    bind_op(case)               -> {"allowed": bool, "rule": refusal or None}
    may_work(case)              -> {"allowed": bool, "rule": refusal or None}
    run_delivery(case)          -> {"outcomes": [...], "state": ..., "escalated": bool}
    negotiate(case)             -> {"mode": "push" | "poll" | "manual"}
    fold_claims(case)           -> {"outcomes": [...], "holder": ..., "reviewers": [...]}
    delivery_id(...), attempt_offsets(...)

`run_head` replays handoff, verdict and authorize events in comment order: the milestone head
moves only by an accepted handoff, and a verdict is effective only when an authorize event
finds the verdict's handoff and revision current.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
_SCHEMA_PATHS = (_HERE.parent / "server-spec" / "schemas" / "milestone-handoff" / "handoff.schema.json",
                 _HERE / "handoff.schema.json")
_TYPES = {"string": str, "integer": int, "boolean": bool, "object": dict, "array": list, "null": type(None)}
_schema: dict | None = None


def schema() -> dict:
    global _schema
    if _schema is None:
        path = next(p for p in _SCHEMA_PATHS if p.exists())
        _schema = json.loads(path.read_text(encoding="utf-8"))
    return _schema


def _ref(root: dict, ref: str) -> dict:
    node: Any = root
    for part in ref.lstrip("#/").split("/"):
        node = node[part]
    return node


def _check(root: dict, node: dict, value: Any, path: str, out: list[str]) -> None:
    if "$ref" in node:
        return _check(root, _ref(root, node["$ref"]), value, path, out)
    if "const" in node and value != node["const"]:
        out.append(f"{path}: must be {node['const']!r}")
        return
    if "enum" in node and value not in node["enum"]:
        out.append(f"{path}: must be one of {node['enum']}")
        return
    want = node.get("type")
    if want is not None:
        kinds = want if isinstance(want, list) else [want]
        ok = any(isinstance(value, _TYPES[k]) and not (k == "integer" and isinstance(value, bool)) for k in kinds)
        if not ok:
            out.append(f"{path}: must be {'/'.join(kinds)}")
            return
    if isinstance(value, str):
        if "minLength" in node and len(value) < node["minLength"]:
            out.append(f"{path}: too short")
        if "maxLength" in node and len(value) > node["maxLength"]:
            out.append(f"{path}: too long")
        if "pattern" in node and not re.search(node["pattern"], value):
            out.append(f"{path}: does not match {node['pattern']}")
    if isinstance(value, list):
        if "maxItems" in node and len(value) > node["maxItems"]:
            out.append(f"{path}: too many items")
        for i, item in enumerate(value):
            if "items" in node:
                _check(root, node["items"], item, f"{path}[{i}]", out)
    if isinstance(value, dict):
        props = node.get("properties", {})
        for key in node.get("required", []):
            if key not in value:
                out.append(f"{path}.{key}: required")
        if node.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    out.append(f"{path}.{key}: not allowed")
        for key, sub in props.items():
            if key in value:
                _check(root, sub, value[key], f"{path}.{key}", out)


def validate(record: dict) -> list[str]:
    root = schema()
    out: list[str] = []
    _check(root, root["oneOf"][0], record, "$", out)
    return out


def run_head(events: list[dict], roles: dict | None = None) -> dict:
    """Replay handoff, verdict and authorize events. A handoff whose action is
    ``address-findings`` lives on the milestone ``<reviewed>-findings`` (a head of its own, so a
    findings handoff never fights the evidence head), and no other action may use that suffix."""
    heads: dict[str, dict] = {}
    handoffs: dict[str, dict] = {}
    verdicts: dict[str, dict] = {}
    outcomes: list[dict] = []
    roles = roles or {}
    for ev in events:
        kind = ev["event"]
        if kind == "handoff":
            head = heads.get(ev["milestone"])
            sup = ev.get("supersedes")
            findings = ev.get("action") == "address-findings"
            suffix = ev["milestone"].endswith("-findings")
            if findings != suffix:
                rule = "findings-milestone" if findings else "reserved-suffix"
            elif head is None and sup is None:
                rule = None
            elif head is None:
                rule = "unknown-supersedes"
            elif sup is None or sup != head["handoff_id"]:
                rule = "stale-base"
            elif ev["revision"] == head["revision"]:
                rule = "same-revision"
            else:
                rule = None
            if rule is None:
                heads[ev["milestone"]] = {"handoff_id": ev["id"], "revision": ev["revision"]}
                handoffs[ev["id"]] = ev
            outcomes.append({"id": ev["id"], "accepted": rule is None, "rule": rule})
        elif kind == "verdict":
            verdicts[ev["id"]] = ev
        elif kind == "authorize":
            v = verdicts[ev["verdict"]]
            head = heads.get(v.get("milestone") or "")
            if not v.get("milestone"):
                rule = "missing-milestone"
            elif not v.get("revision"):
                rule = "missing-revision"
            elif head is None:
                rule = "no-handoff"
            elif v.get("handoff") != head["handoff_id"] or v["revision"] != head["revision"]:
                rule = "stale-revision"
            else:
                rule = _verdict_author(handoffs[head["handoff_id"]], v, roles)
            outcomes.append({"id": ev["verdict"], "effective": rule is None, "rule": rule})
    return {"outcomes": outcomes, "heads": heads}


def _verdict_author(handoff: dict, verdict: dict, roles: dict) -> str | None:
    """The verdict's author must be the handoff's recipient (the named principal, or a principal
    granted the role) and must hold a live review claim."""
    rec = handoff.get("recipient") or {"role": "reviewer"}
    by = verdict.get("by")
    if rec.get("principal") is not None:
        ok = by == rec["principal"]
    else:
        ok = by in roles.get(rec["role"], [])
    if not ok:
        return "unauthorized-author"
    if verdict.get("claim") != "review":
        return "no-review-claim"
    return None


# ---------------------------------------------------------------------------
# Routing and bindings
# ---------------------------------------------------------------------------

MAX_TTL_MINUTES = 24 * 60


def route(case: dict) -> dict:
    """Resolve a recipient role to one active session binding, or the rule that refuses."""
    h, now = case["handoff"], case["now"]
    role, named = h["recipient"]["role"], h["recipient"].get("principal")
    roles = case.get("roles") or {}
    live = [b for b in case["bindings"]
            if b["role"] == role and (named is None or b["principal"] == named)
            and (b["principal"] in roles.get(role, []) or (role == "worker" and b.get("participant")))
            and not b.get("revoked") and b["expires"] > now]
    if not live:
        return {"binding": None, "rule": "no-binding"}
    if len({b["principal"] for b in live}) > 1:
        return {"binding": None, "rule": "ambiguous-recipient"}
    pick = max(live, key=lambda b: b["expires"])
    if h.get("purpose") == "review" and pick["session"] == h["sender_session"]:
        return {"binding": None, "rule": "self-review"}
    return {"binding": pick["binding_id"], "rule": None}


def bind_op(case: dict) -> dict:
    """May the caller create, replace or revoke this binding?"""
    op, caller, owner, sub = case["op"], case["caller"], case["owner"], case["subject"]
    if op == "revoke":
        ok = caller in (sub["principal"], owner)
        return {"allowed": ok, "rule": None if ok else "not-allowed"}
    if caller != sub["principal"]:
        return {"allowed": False, "rule": "others-binding"}
    if sub["role"] == "owner":
        return {"allowed": False, "rule": "owner-role"}
    granted = caller in (case.get("roles") or {}).get(sub["role"], [])
    if not (granted or (sub["role"] == "worker" and case.get("participant"))):
        return {"allowed": False, "rule": "role-not-authorized"}
    if case.get("ttl_minutes", 0) > MAX_TTL_MINUTES or case.get("ttl_minutes", 1) <= 0:
        return {"allowed": False, "rule": "ttl-out-of-range"}
    return {"allowed": True, "rule": None}


def may_work(case: dict) -> dict:
    """Does a handoff (delivered or acknowledged) let the recipient work? Only a claim does."""
    claim = case.get("claim")
    if case.get("via") in ("comment", "role-name"):
        rule = "no-authority"
    elif claim is None:
        rule = "claim-required"
    elif claim["purpose"] != case["scope_purpose"]:
        rule = "scope-mismatch"
    elif claim["purpose"] == "review" and claim["session"] in case.get("work_sessions", []):
        rule = "self-review"
    else:
        rule = None
    return {"allowed": rule is None, "rule": rule}


# ---------------------------------------------------------------------------
# Delivery
# ---------------------------------------------------------------------------

def delivery_id(handoff_id: str, revision: str, recipient: str) -> str:
    """The stable deduplication key: the same across retries, new for another recipient."""
    return "dl_" + hashlib.sha256(f"{handoff_id}|{revision}|{recipient}".encode()).hexdigest()[:16]


def attempt_offsets(max_attempts: int = 5) -> list[int]:
    """Minutes after the first attempt at which each attempt is made: the delay doubles
    from one minute and stops growing at thirty."""
    out, delay = [0], 1
    for _ in range(max_attempts - 1):
        out.append(out[-1] + delay)
        delay = min(delay * 2, 30)
    return out


TERMINAL = ("acknowledged", "failed", "cancelled")


def run_delivery(case: dict) -> dict:
    h = case["handoff"]
    want_id = delivery_id(h["handoff_id"], h["revision"], h["recipient"])
    state, superseded, escalated = "pending", False, False
    outcomes = []
    for ev in case["events"]:
        kind, out = ev["event"], {"event": ev["event"], "ok": True, "rule": None}
        if kind == "supersede":
            superseded = True
        elif kind == "deliver":
            if state == "pending":
                state = "delivered"
            elif state == "delivered":
                out["unchanged"] = True
            else:
                out.update(ok=False, rule="terminal")
        elif kind == "ack":
            if state in ("cancelled", "failed"):
                out.update(ok=False, rule=state)
            elif ev["by"] != h["recipient"]:
                out.update(ok=False, rule="wrong-recipient")
            elif case.get("mode", "push") == "poll" and not ev.get("granted", True):
                out.update(ok=False, rule="role-not-granted")
            elif case.get("mode", "push") == "push" and not ev.get("binding_active", True):
                out.update(ok=False, rule="revoked-binding")
            elif ev.get("delivery_id") != want_id:
                out.update(ok=False, rule="delivery-mismatch")
            elif ev.get("revision") != h["revision"]:
                out.update(ok=False, rule="revision-mismatch")
            elif state == "acknowledged":
                out["unchanged"] = True
            else:
                state = "acknowledged"
            if out["ok"] and superseded:
                out["stale"] = True
        elif kind == "fail":
            if state == "pending" and ev.get("attempts", 0) >= case.get("max_attempts", 5):
                state, escalated = "failed", True
            else:
                out.update(ok=False, rule="not-exhausted" if state == "pending" else state)
        elif kind == "cancel":
            if state in ("pending", "delivered"):
                state = "cancelled"
            else:
                out.update(ok=False, rule=state)
        if kind != "supersede":
            outcomes.append(out)
    return {"outcomes": outcomes, "state": state, "escalated": escalated}


# ---------------------------------------------------------------------------
# Capability negotiation
# ---------------------------------------------------------------------------

CAPABILITY = "milestone-handoff:1"
PUSH_CAPABILITY = "milestone-handoff-push:1"
CORE_TOOLS = ("handoff_send", "handoff_get", "handoff_list", "handoff_ack", "handoff_cancel")
PUSH_TOOLS = ("handoff_bind", "handoff_unbind", "handoff_bindings")


def negotiate(case: dict) -> dict:
    """How an agent hands a milestone over on this server. The capability name is what is
    trusted; the tools must back it, or the agent falls back and says delivery is manual."""
    caps, tools = set(case.get("capabilities") or []), set(case.get("tools") or [])
    if CAPABILITY not in caps or not all(t in tools for t in CORE_TOOLS):
        return {"mode": "manual"}
    if PUSH_CAPABILITY in caps and all(t in tools for t in PUSH_TOOLS):
        return {"mode": "push"}
    return {"mode": "poll"}


# ---------------------------------------------------------------------------
# A review claim alongside a work claim
# ---------------------------------------------------------------------------

def fold_claims(case: dict) -> dict:
    """The claim fold with review claims that coexist with a live work claim. A review claim is
    accepted beside a live work holder only with ``handoff`` naming the milestone's head, a
    review handoff whose recipient the caller is, and never from the holder's own session."""
    now = case["now"]
    holder = None  # {by, session, purpose, until}
    reviewers: list[dict] = []
    outcomes = []
    heads = case.get("heads", {})
    for ev in case["events"]:
        kind, by, out = ev["event"], ev["by"], {"event": ev["event"], "by": ev["by"], "ok": True, "rule": None}
        live = holder is not None and holder["until"] > now
        if kind == "claim" and ev["purpose"] == "review" and live:
            h = heads.get(ev.get("handoff") or "")
            if holder["by"] == by or holder["session"] == ev.get("session"):
                out.update(ok=False, rule="self-review")
            elif h is None:
                out.update(ok=False, rule="held")
            elif not h.get("head"):
                out.update(ok=False, rule="stale-handoff")
            elif h.get("purpose") != "review" or h.get("recipient") not in (None, by):
                out.update(ok=False, rule="not-recipient")
            else:
                reviewers = [r for r in reviewers if r["by"] != by] + [{"by": by, "handoff": ev["handoff"], "until": ev["until"]}]
        elif kind == "claim":
            if holder is None or not live:
                holder = {"by": by, "session": ev.get("session"), "purpose": ev["purpose"], "until": ev["until"]}
            else:
                out.update(ok=False, rule="held")
        elif kind == "release":
            if holder and holder["by"] == by:
                holder = None
            elif any(r["by"] == by for r in reviewers):
                reviewers = [r for r in reviewers if r["by"] != by]
            else:
                out.update(ok=False, rule="not-holder")
        elif kind == "send":
            ok = (holder and holder["by"] == by) or any(r["by"] == by and r["handoff"] == ev.get("for_handoff") for r in reviewers)
            if not ok:
                out.update(ok=False, rule="no-claim")
        outcomes.append(out)
    return {"outcomes": outcomes, "holder": holder["by"] if holder else None,
            "reviewers": sorted(r["by"] for r in reviewers if r["until"] > now)}
