"""Reference for the milestone handoff contract (server-spec/milestone-handoff.md), for checks
MH1 to MH2 (and the later groups). Standard library only. A server copies this file and holds
its copy to conformance/handoff_cases.json.

    validate(record)            -> list of problems ([] = a valid handoff record)
    run_head(events)            -> {"outcomes": [...], "heads": {milestone: {handoff_id, revision}}}

`run_head` replays handoff, verdict and authorize events in comment order: the milestone head
moves only by an accepted handoff, and a verdict is effective only when an authorize event
finds the verdict's handoff and revision current.
"""
from __future__ import annotations

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


def run_head(events: list[dict]) -> dict:
    heads: dict[str, dict] = {}
    handoffs: dict[str, dict] = {}
    verdicts: dict[str, dict] = {}
    outcomes: list[dict] = []
    for ev in events:
        kind = ev["event"]
        if kind == "handoff":
            head = heads.get(ev["milestone"])
            sup = ev.get("supersedes")
            if head is None and sup is None:
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
                rule = None
            outcomes.append({"id": ev["verdict"], "effective": rule is None, "rule": rule})
    return {"outcomes": outcomes, "heads": heads}
