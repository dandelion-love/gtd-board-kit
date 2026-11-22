"""Reference implementation of record pages (server-spec/record-pages.md), for check RP1 to RP3.

Standard library only. A server or repository that writes or checks record pages must give
byte-identical results on conformance/page_cases.json: the readable text of an entry is
checked against what this renderer writes from the entry's own record.
"""
from __future__ import annotations

import hashlib
import json
import re

FORMAT = "okf-register-v1"
FENCE = "```json record"
CLIP = 1500
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,120}$")


def line_sha256(line: str) -> str:
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def item_of(rec: dict) -> str | None:
    """The page a register line belongs to: its `id`, else a link line's `from`."""
    v = rec.get("id") or rec.get("from")
    return v if isinstance(v, str) else None


def _esc(text: str) -> str:
    """Prose-safe text: no raw HTML (a value holding `</details>` would break the page) and no
    line that Markdown would read as a heading, fence or table."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = []
    for ln in text.split("\n"):
        s = ln.lstrip()
        if s.startswith(("#", "```", "~~~", "|", "===")):
            ln = ln[: len(ln) - len(s)] + "\\" + s
        out.append(ln)
    return "\n".join(out)


def _clip(text: str, n: int = CLIP) -> str:
    return text if len(text) <= n else text[:n] + f" … ({len(text) - n} more characters in the record below)"


def _value(v, depth: int = 0) -> str:
    """A value as readable Markdown: strings as text, mappings as nested bullets."""
    if isinstance(v, str):
        return _esc(_clip(v))
    if isinstance(v, (int, float, bool)) or v is None:
        return _esc(json.dumps(v))
    if isinstance(v, list) and all(isinstance(x, (str, int, float)) for x in v):
        return _esc(_clip(", ".join(str(x) for x in v)))
    if isinstance(v, dict) and depth < 2 and len(v) <= 40:
        pad = "  " * depth
        rows = []
        for k, x in v.items():
            inner = _value(x, depth + 1)
            if "\n" in inner and not inner.lstrip().startswith("- "):
                inner = inner.replace("\n", "\n" + pad + "  ")
            rows.append(f"{pad}- **{_esc(str(k))}**: {inner}" if not inner.startswith("\n")
                        else f"{pad}- **{_esc(str(k))}**:{inner}")
        return "\n" + "\n".join(rows)
    return _esc(_clip(json.dumps(v, ensure_ascii=False)))


SUMMARY_FIELDS: dict[str, list[tuple[str, str]]] = {
    "register": [("hypothesis", "Hypothesis"), ("question", "Question"), ("resolves", "Resolves"),
                 ("arms", "Arms"), ("method", "Method"), ("material", "Material"),
                 ("metric", "Metric"), ("decision_rule", "Decision rule"),
                 ("falsified_by", "Falsified by"), ("void_if", "Void if"),
                 ("cannot_answer", "Cannot answer"), ("budget", "Budget"), ("listener", "Listener")],
    "result": [("verdict", "Verdict"), ("judged", "Judged"), ("available", "Available"),
               ("note", "Note"), ("run_dirs", "Files"), ("run_dir", "Files")],
    "reading": [("kind", "Kind"), ("of", "Of"), ("says", "Says"), ("because", "Because"),
                ("changes", "Changes")],
    "fact": [("section", "Section"), ("statement", "Statement"), ("caveat", "Caveat")],
}


def _ref(item, folders: dict | None) -> str:
    """An item id as a relative link to its page when its prefix names a folder, else plain text."""
    if isinstance(item, str) and SAFE_ID.match(item):
        for prefix, target in (folders or {}).items():
            if item.startswith(prefix):
                return f"[{_esc(item)}]({target.replace('{id}', item)})"
    return _esc(str(item))


def summary(rec: dict, folders: dict | None = None) -> str:
    ev = rec.get("event")
    parts: list[str] = []

    def add(label: str, v) -> None:
        if v in (None, "", [], {}):
            return
        parts.append(f"**{label}.** {_value(v)}".rstrip())

    if ev == "register":
        if rec.get("title"):
            add("Title", rec["title"])
        spec = rec.get("spec") if isinstance(rec.get("spec"), dict) else {}
        for k, label in SUMMARY_FIELDS["register"]:
            add(label, spec.get(k, rec.get(k)))
    elif ev == "link":
        to = rec.get("to")
        target = _ref(to, folders) if to else _value(rec.get("url"))
        line = f"**{_esc(str(rec.get('kind')))}** → {target}"
        if rec.get("why") or rec.get("note"):
            line += " — " + _value(rec.get("why") or rec.get("note"))
        parts.append(line)
    elif ev == "fact":
        for k, label in SUMMARY_FIELDS["fact"]:
            add(label, rec.get(k))
        rests = [r.get("id") for r in rec.get("rests_on") or [] if isinstance(r, dict) and r.get("id")]
        if rests:
            parts.append("**Rests on.** " + ", ".join(_ref(i, folders) for i in rests))
    elif ev in SUMMARY_FIELDS:
        for k, label in SUMMARY_FIELDS[ev]:
            add(label, rec.get(k))
    else:
        for k in ("outcome", "instance", "environment", "hours", "verdict", "says", "why", "note"):
            add(k.capitalize(), rec.get(k))
    return "\n\n".join(parts) or "_Nothing to summarise; the record below holds it all._"


def entry_v1(line: str, folders: dict | None = None) -> str:
    rec = json.loads(line)
    head = f"## {_esc(str(rec.get('event')))} · {_esc(str(rec.get('t') or 'no time'))}"
    if rec.get("by"):
        head += f" · {_esc(str(rec['by']))}"
    return (f"\n{head}\n\n{summary(rec, folders)}\n\n<details><summary>Record · sha256 {line_sha256(line)[:16]}"
            f"</summary>\n\n{FENCE}\n{line}\n```\n\n</details>\n")


ENTRY_V2_MARKER = "<!-- okf-entry-v2 -->"
RULE_FIELDS = ("hypothesis", "arms", "metric", "decision_rule", "falsified_by",
               "void_if", "cannot_answer", "n_planned")


def rule_digest(rec: dict) -> str | None:
    """Compute the existing eight-field experiment rule; never infer a missing spec."""
    if (rec.get("event") != "register" or not str(rec.get("id", "")).startswith("EXP-")
            or not isinstance(rec.get("spec"), dict)):
        return None
    spec = rec["spec"]
    payload = json.dumps({k: spec.get(k) for k in RULE_FIELDS}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def full_value(value, depth: int = 0) -> str:
    """Render full structured values as safe, readable Markdown without clipping."""
    if isinstance(value, str):
        return _esc(value)
    if isinstance(value, dict):
        if not value:
            return "{}"
        pad = "  " * depth
        return "\n" + "\n".join(
            f"{pad}- **{_esc(str(key))}**: {full_value(val, depth + 1)}"
            for key, val in value.items()
        )
    if isinstance(value, list):
        if not value:
            return "[]"
        if all(not isinstance(item, (dict, list)) for item in value):
            return ", ".join(full_value(item, depth + 1) for item in value)
        pad = "  " * depth
        return "\n" + "\n".join(f"{pad}- {full_value(item, depth + 1)}" for item in value)
    return _esc(json.dumps(value, ensure_ascii=False))


def summary_v2(rec: dict, folders: dict | None = None) -> str:
    """Expose every field in labelled prose; the sole raw JSON copy stays in details."""
    labels = {
        "rule_hash": "Rule hash prefix (stored)", "prereg": "Preregistration",
        "preregistration_status": "Preregistration status", "n_planned": "Planned",
        "stopping_rule": "Stopping rule", "decision_rule": "Decision rule",
        "cannot_answer": "Cannot answer", "falsified_by": "Falsified by",
        "void_if": "Void if", "review_evidence": "Review evidence",
        "run_dirs": "Run directories", "run_dir": "Run directory",
    }
    parts = []
    def add(key, value):
        if value in (None, "", [], {}):
            return
        label = labels.get(key, key.replace("_", " ").capitalize())
        if key == "rule_hash":
            if isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value):
                label = "Rule SHA-256 (stored)"
            elif not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{16}", value):
                label = "Rule hash (stored; invalid format)"
        rendered = _ref(value, folders) if key == "to" and isinstance(value, str) else full_value(value)
        parts.append(f"**{_esc(label)}.** {rendered}".rstrip())
    for key, value in rec.items():
        if key in ("event", "id", "t", "by"):
            continue
        if key == "spec" and isinstance(value, dict):
            for spec_key, spec_value in value.items():
                add(spec_key, spec_value)
        else:
            add(key, value)
    return "\n\n".join(parts) or "_No additional fields._"


def entry(line: str, folders: dict | None = None) -> str:
    """Render a versioned entry while keeping its fenced record byte-identical."""
    rec = json.loads(line)
    item = item_of(rec)
    if not isinstance(item, str) or not item.startswith("EXP-"):
        return entry_v1(line, folders)
    head = f"## {_esc(str(rec.get('event')))} · {_esc(str(rec.get('t') or 'no time'))}"
    if rec.get("by"):
        head += f" · {_esc(str(rec['by']))}"
    extra = [f"**Record SHA-256.** {line_sha256(line)}"]
    full = rule_digest(rec)
    if full is not None:
        pin = rec.get("rule_hash")
        valid = isinstance(pin, str) and len(pin) in (16, 64) and bool(re.fullmatch(r"[0-9a-f]+", pin))
        if valid and full.startswith(pin):
            extra.append(f"**Rule SHA-256.** {full} (verified against stored pin {pin}; eight registered fields)")
        elif pin is None:
            extra.append(f"**Rule SHA-256.** {full} (computed; no stored pin to verify)")
        else:
            extra.append(f"**Rule SHA-256.** {full} (computed; stored pin {_esc(str(pin))} does not verify)")
    text = "\n\n".join([summary_v2(rec, folders), *extra])
    return (f"\n{head}\n\n{ENTRY_V2_MARKER}\n\n{text}\n\n"
            f"<details><summary>Record · sha256 {line_sha256(line)}</summary>\n\n"
            f"{FENCE}\n{line}\n```\n\n</details>\n")


def header(item: str, kind: str, first_line: str) -> str:
    rec = json.loads(first_line)
    title = rec.get("title") or rec.get("statement") or item
    title = " ".join(str(title).split())
    short = title if len(title) <= 200 else title[:199] + "…"
    return (f"---\ntype: {json.dumps(kind)}\nid: {json.dumps(item)}\ntitle: {json.dumps(short, ensure_ascii=False)}\n"
            f"format: {FORMAT}\nopened: {json.dumps(rec.get('t'))}\n---\n\n# {_esc(item)} — {_esc(short)}\n\n"
            "_Addendum-only record. Nothing above the last entry is ever changed; new information is a new "
            "entry at the end. The JSON in each entry is the record, and the text above it is written from it "
            "by the repository's record-page writer._\n")


def render_page(item: str, kind: str, lines: list[str], folders: dict | None = None) -> str:
    if not lines:
        raise ValueError("a page starts with its first record")
    return header(item, kind, lines[0]) + "".join(entry(ln, folders) for ln in lines)


def parse_page(page: str) -> list[str]:
    """The record lines, in page order: each line between a `json record` fence and its close."""
    out, rows = [], page.split("\n")
    for i, row in enumerate(rows):
        if row == FENCE and i + 2 < len(rows) and rows[i + 2] == "```":
            out.append(rows[i + 1])
    return out


def page_id(page: str) -> str | None:
    m = re.search(r'^id: (".*")$', page.split("\n---\n", 1)[0], re.M)
    try:
        return json.loads(m.group(1)) if m else None
    except Exception:
        return None


def rendered_entries(text: str, folders: dict | None = None) -> list[tuple[str, str]] | None:
    """Parse only complete, byte-exact v1/v2 entries; return original entry bytes."""
    result = []
    seen = {}
    rest = text
    for line in parse_page(text):
        for candidate in (entry(line, folders), entry_v1(line, folders)):
            if rest.startswith(candidate):
                if line in seen and seen[line] != candidate:
                    return None
                seen[line] = candidate
                result.append((line, candidate))
                rest = rest[len(candidate):]
                break
        else:
            return None
    return result if not rest else None


# ---------------------------------------------------------------------------
# The rule
# ---------------------------------------------------------------------------

def check_page(old: str | None, new: str | None, *, item: str, kind: str,
               folders: dict | None = None) -> list[str]:
    """Refusals for one page between two revisions; [] is a pass."""
    if new is None:
        return ["page-removed"] if old is not None else []
    if "\n<<<<<<< " in "\n" + new or "\n>>>>>>> " in "\n" + new:
        return ["conflict-markers"]
    lines = parse_page(new)
    probs: list[str] = []
    for ln in lines:
        try:
            rec = json.loads(ln)
        except Exception:
            probs.append("bad-record-json")
            continue
        if item_of(rec) != item:
            probs.append(f"record-for-another-item:{item_of(rec)}")
    if page_id(new) != item:
        probs.append("front-matter-id-is-not-the-file-name")
    if probs:
        return probs
    if old is None:
        if not lines:
            return ["page-is-not-rendered"]
        prefix = header(item, kind, lines[0])
        return [] if new.startswith(prefix) and rendered_entries(new[len(prefix):], folders) is not None else ["page-is-not-rendered"]
    if not new.startswith(old):
        return ["edits-existing-content"]
    tail = new[len(old):]
    pairs = rendered_entries(tail, folders)
    if pairs is None:
        return ["added-text-is-not-rendered-entries"]
    old_lines = set(parse_page(old))
    for line, rendered in pairs:
        if line in old_lines:
            known = {candidate for candidate in (entry_v1(line, folders), entry(line, folders))
                     if candidate in old}
            if len(known) != 1 or rendered not in known:
                return ["conflicting-record-presentation"]
    return []


def merge_pages(base: str, ours: str, theirs: str, *, item: str, kind: str,
                folders: dict | None = None) -> str | None:
    """Base, then our new entries, then theirs that ours lacks. None if either side broke the rule."""
    if check_page(base, ours, item=item, kind=kind, folders=folders) or \
            check_page(base, theirs, item=item, kind=kind, folders=folders):
        return None
    have, page = set(parse_page(ours)), ours
    base_lines = set(parse_page(base))
    our_pairs = rendered_entries(ours[len(base):], folders) or []
    their_pairs = rendered_entries(theirs[len(base):], folders) or []
    for ln, rendered in our_pairs + their_pairs:
        if ln in base_lines:
            known = [candidate for candidate in (entry_v1(ln, folders), entry(ln, folders))
                     if candidate in base]
            if rendered not in known:
                return None
    our_new = dict(our_pairs)
    for ln, rendered in their_pairs:
        if ln in our_new and our_new[ln] != rendered:
            return None
        if ln not in have:
            page += rendered
            have.add(ln)
    return page
