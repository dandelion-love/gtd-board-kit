"""Reference implementation of register records (server-spec/register-records.md), for checks
RR1 to RR4.

Standard library only. A server or repository that writes, reads, folds or shows register
records copies this file and holds its copy to conformance/record_cases.json, so every writer
refuses the same lines, every reader upgrades older lines the same way, and every mirror shows
the same state.

    validate(register, line, prior=None)    -> list of refusal codes ([] = writable)
    upgrade(register, line, timezone=None)  -> the record in the current shape
    fold(register, lines, ...)              -> one item's state
    represent(state, source)                -> labels, Status, open/closed, fields
    stamp(record, by, via, now=None)        -> the record with v, eid and t filled

The schemas are read from server-spec/schemas/register-records/ beside this file's folder; a
copy elsewhere passes `schema_dir` or keeps the three files beside itself.
"""
from __future__ import annotations

import hashlib
import json
import re
import secrets
import sys
import time
from datetime import datetime, timezone as _utc_tz
from pathlib import Path
from typing import Any

VERSION = 1
REGISTERS = ("experiment", "benchmark", "finding")
_HERE = Path(__file__).resolve().parent
_SCHEMA_DIRS = (_HERE.parent / "server-spec" / "schemas" / "register-records", _HERE)
_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_PRINCIPAL = re.compile(r"^[a-z][a-z0-9-]*:\S+$")
_T_UTC = "%Y-%m-%d %H:%M:%S+00:00"
_TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool,
          "object": dict, "array": list, "null": type(None)}
_OBS_KINDS = ("finding", "threat", "precondition", "provenance", "instrument", "sealed", "note")
_PREREG = ("CLEAN", "PARTIAL", "POST-HOC")
_BEFORE = re.compile(r"^(registered|written)\b[^.;]*?\bbefore\b", re.I)
_NOT_CLEAN = re.compile(r"\b(after|not clean|informed|seen|blocked|post-hoc|partial)\b", re.I)
_CONTEXT_REFUSALS = ("verdict-not-in-rule", "rule-hash-differs", "not-registered",
                     "registered-twice", "eid-reused")
_cache: dict[tuple[str, str], dict] = {}


def line_sha256(line: str) -> str:
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def schema(register: str, schema_dir: str | None = None) -> dict:
    if register not in REGISTERS:
        raise ValueError(f"unknown register {register!r}; one of {REGISTERS}")
    dirs = [Path(schema_dir)] if schema_dir else list(_SCHEMA_DIRS)
    key = (register, str(dirs[0]))
    if key not in _cache:
        for d in dirs:
            p = d / f"{register}.schema.json"
            if p.exists():
                _cache[key] = json.loads(p.read_text(encoding="utf-8"))
                break
        else:
            raise FileNotFoundError(f"{register}.schema.json not found in {dirs}")
    return _cache[key]


def events(register: str, schema_dir: str | None = None) -> list[str]:
    return list(schema(register, schema_dir)["x-events"])


# ---------------------------------------------------------------------------
# The schema subset the register schemas use
# ---------------------------------------------------------------------------

def _empty(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}


def _errors(value: Any, sch: dict, defs: dict, path: str) -> list[str]:
    if "$ref" in sch:
        return _errors(value, defs[sch["$ref"].rsplit("/", 1)[-1]], defs, path)
    errs: list[str] = []
    for sub in sch.get("allOf") or []:
        errs += _errors(value, sub, defs, path)
    if "anyOf" in sch and not any(not _errors(value, s, defs, path) for s in sch["anyOf"]):
        alts = [s for s in sch["anyOf"] if set(s) == {"required"}]
        if alts:   # "one of these fields": name the first as missing
            errs.append(f"missing:{_join(path, alts[0]['required'][0])}")
        else:
            errs.append(f"bad-value:{path or '$'}")
    if "const" in sch and value != sch["const"]:
        errs.append(f"bad-value:{path or '$'}")
    if "enum" in sch and value not in sch["enum"]:
        errs.append(f"bad-value:{path or '$'}")
    t = sch.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        if not any(isinstance(value, _TYPES[x]) and not (x in ("integer", "number") and isinstance(value, bool))
                   for x in types):
            return errs + [f"bad-type:{path or '$'}"]
    if isinstance(value, str):
        if "pattern" in sch and not re.search(sch["pattern"], value):
            errs.append(f"bad-value:{path or '$'}")
        if len(value) < sch.get("minLength", 0):
            errs.append(f"missing:{path}")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and "minimum" in sch \
            and value < sch["minimum"]:
        errs.append(f"bad-value:{path or '$'}")
    if isinstance(value, dict):
        if len(value) < sch.get("minProperties", 0):
            errs.append(f"missing:{path}")
        for req in sch.get("required") or []:
            if _empty(value.get(req)) and not (req == "of" and req in value):
                errs.append(f"missing:{_join(path, req)}")
        for k, sub in (sch.get("properties") or {}).items():
            if k in value and value[k] is not None:
                errs += _errors(value[k], sub, defs, _join(path, k))
    if isinstance(value, list) and isinstance(sch.get("items"), dict):
        for i, item in enumerate(value):
            errs += _errors(item, sch["items"], defs, f"{path}[{i}]")
    return errs


def _join(path: str, key: str) -> str:
    return f"{path}.{key}" if path else key


def _dedupe(xs: list[str]) -> list[str]:
    out: list[str] = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _parse(line: str | dict) -> dict | None:
    if isinstance(line, dict):
        return line
    try:
        rec = json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return None
    return rec if isinstance(rec, dict) else None


def validate(register: str, line: str | dict, prior: list[str] | None = None,
             schema_dir: str | None = None) -> list[str]:
    """The refusals for writing `line` to `register`; [] means it may be written. `prior` is
    the item's earlier lines (raw), needed for the five checks that read them; None skips
    those checks."""
    rec = _parse(line)
    if rec is None:
        return ["bad-json"]
    sch = schema(register, schema_dir)
    ev = rec.get("event")
    if ev not in sch["x-events"]:
        return ["unknown-event"]
    v = rec.get("v", 0)
    if not isinstance(v, int) or isinstance(v, bool):
        return ["bad-type:v"]
    if v > VERSION:
        return ["version-ahead"]
    errs: list[str] = []
    if v == 0:
        if _empty(rec.get("id")) and _empty(rec.get("from")):
            errs.append("missing:id")
    else:
        errs += _errors(rec, sch["$defs"][ev], sch["$defs"], "")
        errs += _extra_rules(register, rec)
    if prior is not None:
        errs += _context(register, rec, line if isinstance(line, str) else None, prior, schema_dir)
    return _dedupe(errs)


def _extra_rules(register: str, rec: dict) -> list[str]:
    """The rules a schema states in words (x-rules)."""
    if register == "experiment" and rec.get("event") == "register":
        spec = rec.get("spec") if isinstance(rec.get("spec"), dict) else {}
        arms = spec.get("arms")
        if isinstance(arms, (dict, list)) and len(arms) > 1 and _empty(spec.get("stopping_rule")):
            return ["missing:spec.stopping_rule"]
    return []


def _context(register: str, rec: dict, raw: str | None, prior: list[str],
             schema_dir: str | None) -> list[str]:
    errs: list[str] = []
    olds = [(p, upgrade(register, p, schema_dir=schema_dir)) for p in prior]
    first = "fact" if register == "finding" else "register"
    regs = [r for _, r in olds if r.get("event") == first]
    ev = rec.get("event")
    if register == "finding":
        if ev not in ("fact", "open") and not any(r.get("event") in ("fact", "open") for _, r in olds):
            errs.append("not-registered")
    elif ev == "register":
        if regs:
            errs.append("registered-twice")
    elif not regs:
        errs.append("not-registered")
    if ev == "result" and register == "experiment" and regs:
        reg = regs[0]
        rule = (reg.get("spec") or {}).get("decision_rule")
        verdict = rec.get("verdict")
        if verdict != "VOID" and not (isinstance(rule, dict) and verdict in rule):
            errs.append("verdict-not-in-rule")
        if reg.get("rule_hash") and rec.get("rule_hash") != reg.get("rule_hash"):
            errs.append("rule-hash-differs")
    if ev == "result" and register == "benchmark" and regs and rec.get("verdict") is not None:
        rule = (regs[0].get("spec") or {}).get("decision_rule")
        if isinstance(rule, dict) and rec["verdict"] not in rule:
            errs.append("verdict-not-in-rule")
    eid = rec.get("eid")
    if eid:
        for p, _ in olds:
            q = _parse(p) or {}
            if q.get("eid") == eid and p != raw:
                errs.append("eid-reused")
                break
    return errs


def already_written(line: str, prior: list[str]) -> bool:
    """A retry: the same eid on the same bytes. The writer writes nothing and succeeds."""
    rec = _parse(line) or {}
    return bool(rec.get("eid")) and line in prior


# ---------------------------------------------------------------------------
# Writing: the envelope
# ---------------------------------------------------------------------------

def mint_eid(now_ms: int | None = None, rand: bytes | None = None) -> str:
    """A ULID: 48 bits of milliseconds, 80 random bits, Crockford base32."""
    ms = int(time.time() * 1000) if now_ms is None else now_ms
    r = rand if rand is not None else secrets.token_bytes(10)
    n = (ms << 80) | int.from_bytes(r, "big")
    return "".join(_CROCKFORD[(n >> (5 * i)) & 31] for i in range(25, -1, -1))


def stamp(record: dict, by: str, via: str, now: datetime | None = None,
          eid: str | None = None) -> dict:
    """The record with the envelope filled: v, eid, t, by, via. Never overwrites an eid."""
    when = (now or datetime.now(_utc_tz.utc)).astimezone(_utc_tz.utc)
    out = {"event": record["event"], "v": VERSION, "id": record.get("id"),
           "eid": record.get("eid") or eid or mint_eid(int(when.timestamp() * 1000)),
           "t": when.strftime(_T_UTC), "by": by, "via": via}
    out.update({k: v for k, v in record.items() if k not in out})
    return out


def dumps(record: dict) -> str:
    """One register line, as every writer writes it."""
    return json.dumps(record, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Reading: the upgrade
# ---------------------------------------------------------------------------

def _utc_t(t: Any, tz: str | None) -> tuple[Any, bool]:
    """`t` as UTC with its offset; True when a zone had to be assumed."""
    if not isinstance(t, str):
        return t, False
    s = t.strip().replace("T", " ")
    try:
        when = datetime.fromisoformat(s)
    except ValueError:
        return t, False
    assumed = when.tzinfo is None
    if assumed:
        if not tz:
            return t, True
        try:
            from zoneinfo import ZoneInfo
            when = when.replace(tzinfo=ZoneInfo(tz))
        except Exception:  # noqa: BLE001 - an unknown zone leaves the time as written
            return t, True
    return when.astimezone(_utc_tz.utc).strftime(_T_UTC), assumed


def _prereg(text: Any) -> str | None:
    if not isinstance(text, str):
        return None
    u = text.strip().upper()
    if "BLOCKED" in u:
        return None
    tag = next((x for x in _PREREG if u.startswith(x)), None)
    if tag or u.startswith("NOT CLEAN"):
        return tag
    if _BEFORE.match(text.strip()) and not _NOT_CLEAN.search(text):
        return "CLEAN"
    return None


def upgrade(register: str, line: str | dict, timezone: str | None = None,
            schema_dir: str | None = None) -> dict:
    """The record in the current shape, with `_upgraded` listing what was assumed. The line's
    bytes are untouched; take the line hash from the raw line, never from this."""
    rec = _parse(line)
    if rec is None:
        return {"event": None, "_upgraded": ["bad-json"]}
    rec = json.loads(json.dumps(rec))
    up: list[str] = []
    if rec.get("v", 0) == VERSION:
        return rec
    if _empty(rec.get("id")) and isinstance(rec.get("from"), str):
        rec["id"] = rec["from"]
        up.append("id")
    if "t" not in rec or rec.get("t") is None:
        rec["t"] = None
        up.append("t")
    else:
        t, assumed = _utc_t(rec["t"], timezone)
        if t != rec["t"] or assumed:
            rec["t"] = t
            up.append("t")
    if _empty(rec.get("eid")) and isinstance(line, str):
        rec["eid"] = "h:" + line_sha256(line)[:24]
        up.append("eid")
    by = rec.get("by")
    if not (isinstance(by, str) and _PRINCIPAL.match(by)):
        if by is not None:
            rec["by_text"] = by
        rec["by"] = "unknown"
        up.append("by")
    ev = rec.get("event")
    if ev == "link" and _empty(rec.get("to")) and (rec.get("url") or rec.get("local")):
        rec["event"] = "artifact"
        if _empty(rec.get("why")) and rec.get("note"):
            rec["why"] = rec["note"]
        up.append("event")
    if ev == "observation" and rec.get("kind") not in _OBS_KINDS:
        if _empty(rec.get("title")):
            rec["title"] = rec.get("kind")
        rec["kind"] = "note"
        up.append("kind")
    if ev == "reading" and _empty(rec.get("kind")):
        rec["kind"] = "reading"
        up.append("kind")
    if ev == "register" and isinstance(rec.get("spec"), dict):
        spec = rec["spec"]
        if "prereg" not in spec:
            spec["prereg"] = _prereg(spec.get("preregistration_status"))
            if isinstance(spec.get("preregistration_status"), str):
                spec["prereg_note"] = spec["preregistration_status"]
            up.append("spec.prereg")
    if register == "benchmark" and ev == "result" and _empty(rec.get("status")):
        measured = rec.get("measured") if isinstance(rec.get("measured"), dict) else {}
        verdict = rec.get("verdict") or measured.get("verdict_as_registered")
        j, a = rec.get("judged"), rec.get("available")
        counted = all(isinstance(x, int) and not isinstance(x, bool) for x in (j, a))
        if verdict is not None and rec.get("verdict") is None:
            rec["verdict"] = verdict
        rec["status"] = "complete" if verdict is not None or (counted and j >= a) else (
            "partial" if counted else None)
        up.append("status")
    rec["v"] = VERSION
    rec["_upgraded"] = up
    return rec


# ---------------------------------------------------------------------------
# The fold
# ---------------------------------------------------------------------------

#: The events whose note (a reading's says) is an item's latest report.
REPORTING = ("launch", "start", "attempt", "result", "block", "unblock", "retire", "unretire",
             "reading", "deviation")


def _reporting_text(rec: dict) -> str | None:
    if rec.get("event") not in REPORTING:
        return None
    text = rec.get("says") if rec.get("event") == "reading" else rec.get("note")
    return text.strip() if isinstance(text, str) and text.strip() else None


def fold(register: str, lines: list[str], timezone: str | None = None,
         evidence: list[str] | None = None, schema_dir: str | None = None) -> dict:
    """One item's state from its lines in page order. `evidence` (findings only) is every line
    of the registers a finding may cite, for staleness."""
    recs = [(ln, upgrade(register, ln, timezone, schema_dir)) for ln in lines]
    invalid = []
    for ln, r in recs:
        refused = validate(register, ln, schema_dir=schema_dir)
        if refused:
            invalid.append({"line_sha256": line_sha256(ln) if isinstance(ln, str) else None,
                            "event": r.get("event"), "refused": refused})
    if register == "experiment":
        st = _fold_experiment([r for _, r in recs])
    elif register == "benchmark":
        st = _fold_benchmark([r for _, r in recs])
    else:
        st = _fold_finding(recs, evidence or [], timezone, schema_dir)
    st["invalid"] = invalid
    return st


def _base(recs: list[dict]) -> dict:
    return {"id": next((r.get("id") for r in recs if r.get("id")), None), "state": None,
            "verdict": None, "prereg": None, "hours": None, "cost": None, "started": None,
            "agent": None, "last_report": None, "title": None}


def _fold_experiment(recs: list[dict]) -> dict:
    st = _base(recs)
    reg = next((r for r in recs if r.get("event") == "register"), None)
    if reg is None:
        st["state"] = None
        return st
    st["title"] = reg.get("title")
    spec = reg.get("spec") if isinstance(reg.get("spec"), dict) else {}
    st["prereg"] = spec.get("prereg")
    phase, result, block, retire, go = None, None, False, None, None
    for r in recs:
        ev = r.get("event")
        if r is not reg and ev == "register":
            continue
        if _reporting_text(r):
            st["last_report"] = {"event": ev, "t": r.get("t"), "text": _reporting_text(r)}
        if ev in ("launch", "start"):
            st["started"] = st["started"] or r.get("t")
            go = r
            phase = "queued" if ev == "launch" else "started"
        elif ev == "result":
            result = r
        elif ev == "block":
            block = True
        elif ev == "unblock":
            block = False
        elif ev == "retire":
            retire = r
        elif ev == "unretire":
            retire = None
        elif ev == "attempt":
            for key, acc in (("hours", "hours"), ("cost_estimated", "cost")):
                x = r.get(key)
                if isinstance(x, (int, float)) and not isinstance(x, bool):
                    st[acc] = round((st[acc] or 0.0) + x, 6)
    if go:
        who = go.get("by_text") if go.get("by") == "unknown" else go.get("by")
        where = go.get("resource") or ", ".join(str(go[k]) for k in ("env", "gpu") if go.get(k))
        st["agent"] = _clip(" · ".join(str(p).strip() for p in (who, where) if p and str(p).strip())) or None
    fold_state, why = None, None
    if result is not None:
        verdict = str(result.get("verdict") or "")
        rule = spec.get("decision_rule")
        if verdict != "VOID" and not (isinstance(rule, dict) and verdict in rule):
            why = "verdict-not-in-rule"
        elif reg.get("rule_hash") and result.get("rule_hash") != reg.get("rule_hash"):
            why = "rule-hash-differs"
        fold_state = "unvalidated" if why else ("void" if verdict == "VOID" else "verdict")
        st["verdict"] = verdict
    if retire is not None and fold_state in (None, "unvalidated"):
        kind = str(retire.get("kind") or "").lower()
        fold_state = kind if kind in ("void", "abandoned") else "retired"
        st["verdict"] = None
    elif fold_state is None:
        fold_state = "blocked" if block else (phase or "registered")
    st["state"] = fold_state
    st["unvalidated_because"] = why
    return st


def _fold_benchmark(recs: list[dict]) -> dict:
    st = _base(recs)
    reg = next((r for r in recs if r.get("event") == "register"), None)
    if reg is None:
        return st
    st["title"] = reg.get("title")
    last, retire = None, None
    for r in recs:
        ev = r.get("event")
        if _reporting_text(r):
            st["last_report"] = {"event": ev, "t": r.get("t"), "text": _reporting_text(r)}
        if ev == "result":
            last = r
        elif ev == "retire":
            retire = r
        elif ev == "unretire":
            retire = None
    state = "registered"
    if last is not None:
        status = last.get("status")
        state = {"complete": "complete", "partial": "partial", "withdrawn": "registered"}.get(
            status, "unvalidated")
        if status in ("complete", "partial"):
            st["verdict"] = last.get("verdict")
    if retire is not None and state != "complete":
        kind = str(retire.get("kind") or "").lower()
        state = kind if kind in ("void", "abandoned") else "retired"
    st["state"] = state
    return st


#: Link kinds that read evidence: a new one on a cited item, from either end, makes a finding
#: stale. The other kinds say how work was planned or what it measured, and change no result.
EVIDENTIAL_LINKS = ("refines", "contradicts", "corroborates", "supersedes", "shares-listener")


def _moves(e: dict, cid: str) -> bool:
    ev = e.get("event")
    if ev in ("result", "reading", "deviation", "artifact"):
        return e.get("id") == cid
    if ev == "link":
        return e.get("kind") in EVIDENTIAL_LINKS and cid in (e.get("id"), e.get("to"))
    return False


def _fold_finding(recs, evidence, timezone, schema_dir) -> dict:
    st = _base([r for _, r in recs])
    last, retired = None, False
    for _, r in recs:
        if r.get("event") in ("fact", "open"):
            last, retired = r, False
        elif r.get("event") == "retire":
            retired = True
    if last is None:
        return st
    st["title"] = last.get("statement")
    st["state"] = "retired" if retired else last["event"]
    st["cites"] = [c.get("id") for c in last.get("rests_on") or [] if isinstance(c, dict)]
    if not retired and isinstance(last.get("t"), str):
        later = [e for e in (upgrade("experiment", ln, timezone, schema_dir) for ln in evidence)
                 if isinstance(e.get("t"), str) and e["t"] > last["t"]]   # only event, id, to, kind, t are read
        moved = [cid for cid in st["cites"] if any(_moves(e, cid) for e in later)]
        if moved:
            st["state"] = "stale"
            st["moved"] = moved
    return st


# ---------------------------------------------------------------------------
# On GitHub
# ---------------------------------------------------------------------------

def _clip(text: str, n: int = 240) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n - 1] + "\u2026"


def _local_date(t: Any, tz: str | None) -> str | None:
    """The day a UTC time falls on in the source's zone (UTC without one)."""
    if not isinstance(t, str) or not re.match(r"\d{4}-\d{2}-\d{2}", t):
        return None
    try:
        when = datetime.fromisoformat(t)
    except ValueError:
        return t[:10]
    if when.tzinfo is None or not tz:
        return t[:10]
    try:
        from zoneinfo import ZoneInfo
        return when.astimezone(ZoneInfo(tz)).date().isoformat()
    except Exception:  # noqa: BLE001
        return t[:10]


def represent(state: dict, source: dict) -> dict:
    """What a sync shows for one folded item: the labels it manages and which of them the item
    carries, the board Status, open or closed, and the board fields that have a value."""
    kind_label = source.get("kind_label")
    state_labels = source.get("state_labels") or {}
    invalid_label = source.get("invalid_label")
    managed = sorted({x for x in [kind_label, invalid_label, *state_labels.values()] if x})
    labels = set()
    if kind_label:
        labels.add(kind_label)
    if state.get("state") in state_labels:
        labels.add(state_labels[state["state"]])
    if invalid_label and state.get("invalid"):
        labels.add(invalid_label)
    status = (source.get("status_map") or {}).get(state.get("state"))
    tz = source.get("timezone")
    names = source.get("fields") or {}
    report = state.get("last_report")
    values = {"verdict": state.get("verdict"), "prereg": state.get("prereg"),
              "gpu_hours": round(state["hours"], 3) if state.get("hours") is not None else None,
              "spend": round(state["cost"], 2) if state.get("cost") is not None else None,
              "started": _local_date(state.get("started"), tz),
              "agent": state.get("agent"),
              "last_report": _clip(f"{_local_date(report.get('t'), tz) or '?'} {report['event']}: "
                                   f"{report['text']}") if report else None}
    fields = {names[k]: v for k, v in values.items() if k in names and v not in (None, "")}
    return {"labels": sorted(labels), "managed_labels": managed, "status": status,
            "closed": status in (source.get("closed") or []), "fields": fields}


# ---------------------------------------------------------------------------
# One conformance case from stdin, as --record-cmd answers it
# ---------------------------------------------------------------------------

def answer(case: dict) -> dict:
    op, reg = case["op"], case["register"]
    if op == "validate":
        return {"refused": validate(reg, case["line"], case.get("prior"))}
    if op == "upgrade":
        return {"record": upgrade(reg, case["line"], case.get("timezone"))}
    if op == "fold":
        st = fold(reg, case["lines"], case.get("timezone"), case.get("evidence"))
        return {"state": st, "shown": represent(st, case["source"]) if case.get("source") else None}
    raise ValueError(f"unknown op {op!r}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--case"]:
        print(json.dumps(answer(json.loads(sys.stdin.read())), ensure_ascii=False))
    else:
        print(__doc__)
