#!/usr/bin/env python3
"""okf_lint.py: check a knowledge bundle against the OKF version the kit pins.

    python3 okf_lint.py <bundle-dir> [--strict]

Errors (always fail) are the OKF conformance rules (SPEC.md section 11):
  - every non-reserved .md file has a parseable YAML frontmatter block with a non-empty `type`;
  - `index.md` carries no frontmatter, except `okf_version` in the bundle-root index;
  - `log.md` groups entries under `## YYYY-MM-DD` headings, newest first.

Warnings (fail only with --strict) are the SHOULDs and the v0.1 leftovers:
  - the root `index.md` does not declare `okf_version`, or declares another version than
    the kit pins (okf/PIN.json);
  - legacy `timestamp` (now `generated: {by, at}`) or a body `# Citations` list (now
    `sources` plus footnotes);
  - `generated` without `by`, or an actor not in the `human:<id>`, `process:<id>` or
    `<producer>/<version>` form;
  - a datetime without an explicit UTC offset;
  - a footnote label with no matching `sources[].id`;
  - `status` outside draft / stable / deprecated.

Standard library only; uses PyYAML for frontmatter when it is installed.
Exit status: 0 clean, 1 errors (or warnings with --strict).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
RESERVED = {"index.md", "log.md"}
ACTOR = re.compile(r"^(human:[\w.-]+|process:[\w.-]+|[\w.-]+/[\w.+-]+)$")
DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$")
STATUSES = {"draft", "stable", "deprecated"}

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - exercised where PyYAML is absent
    yaml = None


def pinned_version() -> str | None:
    try:
        return json.loads((KIT / "okf" / "PIN.json").read_text())["okf_version"]
    except (OSError, ValueError, KeyError):
        return None


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        end = text.find("\n---", 4)
        if end == -1 or text[end + 4:].strip():
            return None, text
    return text[4:end], text[end + 5:]


def parse(block: str) -> dict | None:
    """Parse frontmatter. With PyYAML: full YAML. Without: top-level keys and simple values."""
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError:
            return None
        return data if isinstance(data, dict) else None
    data: dict = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line[0] in " -\t":
            continue
        key, sep, value = line.partition(":")
        if not sep:
            return None
        data[key.strip()] = value.strip().strip("'\"")
    return data


def as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def datetimes(data: dict) -> list[str]:
    out = []
    gen = data.get("generated")
    if isinstance(gen, dict) and gen.get("at") is not None:
        out.append(str(gen["at"]))
    for v in as_list(data.get("verified")):
        if isinstance(v, dict) and v.get("at") is not None:
            out.append(str(v["at"]))
    if data.get("stale_after") is not None:
        out.append(str(data["stale_after"]))
    return out


def lint(bundle: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    pin = pinned_version()
    for path in sorted(bundle.rglob("*.md")):
        rel = path.relative_to(bundle).as_posix()
        text = path.read_text(encoding="utf-8")
        block, body = split_frontmatter(text)
        if path.name == "index.md":
            if block is not None:
                data = parse(block) or {}
                if path.parent != bundle or set(data) - {"okf_version"}:
                    errors.append(f"{rel}: index.md may carry frontmatter only at the bundle "
                                  "root, and only okf_version")
            if path.parent == bundle:
                declared = (parse(block) or {}).get("okf_version") if block else None
                if declared is None:
                    warns.append(f"{rel}: root index.md does not declare okf_version")
                elif pin and str(declared) != pin:
                    warns.append(f"{rel}: declares okf_version {declared}, the kit pins {pin}")
            continue
        if path.name == "log.md":
            dates = re.findall(r"(?m)^## (\S+)\s*$", body if block is None else text)
            bad = [d for d in dates if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d)]
            if bad:
                errors.append(f"{rel}: log headings must be ## YYYY-MM-DD, found {bad[:3]}")
            elif dates != sorted(dates, reverse=True):
                errors.append(f"{rel}: log entries must be newest first")
            continue
        if block is None:
            errors.append(f"{rel}: no YAML frontmatter block")
            continue
        data = parse(block)
        if data is None:
            errors.append(f"{rel}: frontmatter is not parseable YAML")
            continue
        if not str(data.get("type") or "").strip():
            errors.append(f"{rel}: frontmatter has no type")
        if "timestamp" in data:
            warns.append(f"{rel}: legacy timestamp; use generated: {{by, at}} (OKF 0.2)")
        if re.search(r"(?m)^#\s+Citations\s*$", body):
            warns.append(f"{rel}: legacy # Citations list; use sources plus footnotes (OKF 0.2)")
        if "status" in data and str(data["status"]) not in STATUSES:
            warns.append(f"{rel}: status {data['status']!r} is not draft, stable or deprecated")
        if yaml is None:
            continue  # the nested checks need real YAML
        gen = data.get("generated")
        if gen is not None and not (isinstance(gen, dict) and gen.get("by")):
            warns.append(f"{rel}: generated needs by")
        actors = [gen.get("by")] if isinstance(gen, dict) and gen.get("by") else []
        actors += [v.get("by") for v in as_list(data.get("verified")) if isinstance(v, dict)]
        for actor in actors:
            if not ACTOR.match(str(actor)):
                warns.append(f"{rel}: actor {actor!r} is not human:<id>, process:<id> "
                             "or <producer>/<version>")
        for dt in datetimes(data):
            if not DATETIME.match(dt.replace(" ", "T").replace("+00:00", "Z")):
                warns.append(f"{rel}: datetime {dt!r} needs an explicit UTC offset")
        ids = {str(s.get("id")) for s in as_list(data.get("sources"))
               if isinstance(s, dict) and s.get("id")}
        for label in set(re.findall(r"\[\^([^\]]+)\]", body)):
            if label not in ids:
                warns.append(f"{rel}: footnote [^{label}] has no sources entry with that id")
    return errors, warns


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    strict = "--strict" in argv
    if not args or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    bundle = Path(args[0])
    if not bundle.is_dir():
        print(f"okf_lint: {bundle} is not a directory", file=sys.stderr)
        return 1
    errors, warns = lint(bundle)
    for e in errors:
        print(f"ERROR {e}")
    for w in warns:
        print(f"WARN  {w}")
    note = "" if yaml is not None else " (PyYAML not installed: nested checks skipped)"
    if errors or (strict and warns):
        print(f"okf_lint: {len(errors)} errors, {len(warns)} warnings{note}")
        return 1
    print(f"okf_lint: ok against OKF {pinned_version()}, {len(warns)} warnings{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
