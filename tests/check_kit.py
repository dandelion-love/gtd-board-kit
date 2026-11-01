#!/usr/bin/env python3
"""Checks for gtd-board-kit: size budgets, skill frontmatter, versions and local links.

Standard library only. Exit 0 when every check passes, 1 otherwise.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["board-onboard", "board-pickup", "board-claim", "board-report", "board-needs-person", "board-lane", "okf-knowledge"]
BOARD_BUDGET = 3000      # bytes; BOARD.md is read in full by every agent
SKILL_BUDGET = 6000      # bytes per SKILL.md
DESC_BUDGET = 1024       # characters; the Agent Skills limit for description
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out, section = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\S[^:]*:\s*$", line):
            section = line.rstrip(":").strip()
            continue
        k, _, v = line.strip().partition(":")
        key = f"{section}.{k}" if line.startswith(" ") and section else k
        out[key.strip()] = v.strip()
    return out


version = (ROOT / "VERSION").read_text().strip()
if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    fail(f"VERSION is not semver: {version!r}")

board = ROOT / "BOARD.md"
if board.stat().st_size > BOARD_BUDGET:
    fail(f"BOARD.md is {board.stat().st_size} bytes, over {BOARD_BUDGET}")
board_text = board.read_text()
for s in SKILLS:
    if f"`{s}`" not in board_text:
        fail(f"BOARD.md does not list {s}")

found = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
if found != sorted(SKILLS):
    fail(f"skills/ holds {found}, expected {sorted(SKILLS)} (update SKILLS and the installers)")

for s in SKILLS:
    path = ROOT / "skills" / s / "SKILL.md"
    if not path.exists():
        fail(f"{path.relative_to(ROOT)} missing")
        continue
    text = path.read_text()
    fm = frontmatter(text)
    if fm.get("name") != s:
        fail(f"{s}: frontmatter name is {fm.get('name')!r}")
    desc = fm.get("description", "")
    if not desc or len(desc) > DESC_BUDGET or "<" in desc or ">" in desc:
        fail(f"{s}: description missing, too long, or has angle brackets")
    if fm.get("metadata.version") is None:
        fail(f"{s}: no metadata.version")
    if path.stat().st_size > SKILL_BUDGET:
        fail(f"{s}: {path.stat().st_size} bytes, over {SKILL_BUDGET}")
    if "BOARD.md" not in text:
        fail(f"{s}: does not send the agent to BOARD.md")

for script in ("add-to-repo.sh", "add-to-repo.ps1"):
    body = (ROOT / "install" / script).read_text()
    for s in SKILLS:
        if s not in body:
            fail(f"install/{script} does not install {s}")

# PowerShell names are case-insensitive and functions beat executables, so a function
# named git would recurse on its own `& git` call .
for ps1 in (ROOT / "install").glob("*.ps1"):
    if re.search(r"(?im)^\s*function\s+git\b", ps1.read_text()):
        fail(f"install/{ps1.name}: a function named git shadows git.exe")

# okf/SPEC.md is a verbatim upstream copy whose links are examples; code is not a link.
# In the knowledge/ bundle, a link starting with / is bundle-relative (OKF 0.2).
for md in ROOT.rglob("*.md"):
    if md == ROOT / "okf" / "SPEC.md" or ".git" in md.parts:
        continue
    text = re.sub(r"```.*?```|`[^`\n]*`", "", md.read_text(), flags=re.S)
    in_bundle = (ROOT / "knowledge") in md.parents
    for target in re.findall(r"\]\(([^)#\s]+)\)", text):
        if "://" in target:
            continue
        if target.startswith("/") and in_bundle:
            resolved = ROOT / "knowledge" / target.lstrip("/")
        else:
            resolved = md.parent / target
        if not resolved.exists():
            fail(f"{md.relative_to(ROOT)}: broken link {target}")

# The guard must pass on the whole tree: this repo is public.
import subprocess  # noqa: E402
guard = subprocess.run([sys.executable, str(ROOT / "tools" / "public_guard.py"), "--all"],
                       capture_output=True, text=True)
if guard.returncode != 0:
    fail("public_guard --all found private data:\n" + guard.stderr.strip())

# The guard must catch these shapes. Built at run time so the file itself stays clean.
LEAKS = ["tok " + "ghp_" + "a" * 30, "see " + "D:" + "\\work", "fixes " + "#" + "12",
         "board " + "acme/" + "4", "id " + "55" + "60276", "a" + "@" + "b.com",
         "/mnt/" + "project-files/x"]
for leak in LEAKS:
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "public_guard.py"), "--text"],
                       input=leak, capture_output=True, text=True)
    if r.returncode != 1:
        fail(f"public_guard missed a leak shape: {leak[:12]}...")
for trailer in ("Co-Authored-By: " + "ghp_" + "a" * 30,):
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "public_guard.py"), "--text"],
                       input=trailer, capture_output=True, text=True)
    if r.returncode != 1:
        fail("public_guard lets a token through in a trailer")

# lanes.py: a filled lane and a named grant pass; a whole-folder grant and a bad switch fail.
FILLED = """## Standing lanes

### lane: nightly
- asked_by: owner
- basis: the owner approved a nightly check
- grant: https://example.com/approval
- policy: 1
- switch: observe
- item: owner/repo#N
- every: 24h
- lease: 72h
- may:
  - run the check and report
- never:
  - touch the default branch

## Workflow grants

### grant: ci
- paths:
  - .github/workflows/ci.yml
- granted_by: owner
- date: 2026-01-01
- link: https://example.com/approval
"""
import tempfile  # noqa: E402
BAD = FILLED.replace("switch: observe", "switch: maybe").replace("workflows/ci.yml", "workflows/**")
for body, want in ((FILLED, 0), (BAD, 1)):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write(body)
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "lanes.py"), "check", fh.name],
                       capture_output=True, text=True)
    Path(fh.name).unlink()
    if r.returncode != want:
        fail(f"lanes.py check returned {r.returncode}, wanted {want}: {r.stdout.strip()}")
    if want and not ("switch must be" in r.stdout and "whole-folder" in r.stdout):
        fail("lanes.py check missed a bad switch or a whole-folder grant")

# check --merged reads only the default branch: a grant added on a branch grants nothing.
with tempfile.TemporaryDirectory() as tmp:
    def git(*a, cwd=tmp):
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=" + "t" + "@" + "example.com", *a],
                       cwd=cwd, check=True, capture_output=True)
    origin, work = Path(tmp) / "origin.git", Path(tmp) / "work"
    git("init", "-q", "--bare", str(origin))
    git("clone", "-q", str(origin), str(work))
    (work / ".gtd").mkdir()
    (work / ".gtd" / "BOARD.local.md").write_text(FILLED)
    git("add", "-A", cwd=work); git("commit", "-qm", "base", cwd=work)
    git("push", "-q", "origin", "HEAD", cwd=work)
    git("remote", "set-head", "origin", "-a", cwd=work)
    (work / ".gtd" / "BOARD.local.md").write_text(FILLED.replace("workflows/ci.yml", "workflows/ci.yml\n  - .github/workflows/deploy.yml"))
    lanes = [sys.executable, str(ROOT / "tools" / "lanes.py"), "check", "--merged", "--covers"]
    for path, want in ((".github/workflows/ci.yml", 0), (".github/workflows/deploy.yml", 1)):
        r = subprocess.run(lanes + [path], cwd=work, capture_output=True, text=True)
        if r.returncode != want:
            fail(f"check --merged --covers {path} returned {r.returncode}, wanted {want}")

# OKF: the pinned spec is present, PIN.json agrees with it, and the kit's own bundle lints.
import json  # noqa: E402
pin = json.loads((ROOT / "okf" / "PIN.json").read_text())
spec = ROOT / "okf" / "SPEC.md"
m = re.search(r"^\*\*Version ([\d.]+)\*\*", spec.read_text(), re.M) if spec.exists() else None
if not m or m.group(1) != pin.get("okf_version"):
    fail(f"okf/SPEC.md version {m and m.group(1)} does not match PIN.json {pin.get('okf_version')}")
if not re.fullmatch(r"[0-9a-f]{40}", pin.get("commit", "")):
    fail("okf/PIN.json commit is not a full sha")
lint = subprocess.run([sys.executable, str(ROOT / "tools" / "okf_lint.py"),
                       str(ROOT / "knowledge"), "--strict"], capture_output=True, text=True)
if lint.returncode != 0:
    fail("okf_lint knowledge --strict:\n" + lint.stdout.strip())

# Spec and conformance stay paired. Every check id in server-spec/conformance.md is run or
# listed as manual by the runner, the runner reports no id the spec lacks, and the C13
# fixture table matches fold_cases.json.
sys.path.insert(0, str(ROOT / "conformance"))
sys.dont_write_bytecode = True
from runner import CHECK_ID, HEADINGS, Family, family_of, fingerprint, report_order  # noqa: E402
ID = CHECK_ID.pattern
conf_md = (ROOT / "server-spec" / "conformance.md").read_text()
spec_ids = set(re.findall(rf"^\| ({ID}) \|", conf_md, re.M))
runner_ids = set(re.findall(rf'"({ID})"', (ROOT / "conformance" / "runner.py").read_text()))
for cid in sorted(spec_ids - runner_ids):
    fail(f"conformance check {cid} is in server-spec/conformance.md but not in conformance/runner.py "
         "(run it, or list it as manual)")
for cid in sorted(runner_ids - spec_ids):
    fail(f"conformance/runner.py reports {cid}, which server-spec/conformance.md does not define")
fold_table = set(re.findall(r"^\| ([a-z]) \|", conf_md, re.M))
fold_json = {c["name"] for c in json.loads((ROOT / "conformance" / "fold_cases.json").read_text())["cases"]}
if fold_table != fold_json:
    fail(f"C13 fixture table {sorted(fold_table)} differs from fold_cases.json {sorted(fold_json)}")

# Every check id in the table belongs to a Family, and the report sorts by family order.
for cid in spec_ids:
    try:
        if family_of(cid) is Family.RUN:
            raise ValueError(cid)
    except ValueError:
        fail(f"conformance check {cid} has no Family in conformance/runner.py")
for fam in Family:
    if fam is not Family.RUN and not re.search(rf"^##+ {re.escape(HEADINGS[fam])}\b", conf_md, re.M):
        fail(f"Family.{fam.name}'s heading {HEADINGS.get(fam)!r} is not in server-spec/conformance.md")
if sorted(["X1", "JC2", "T10", "O1", "T2", "J1", "RUN"], key=report_order) != \
        ["T2", "T10", "O1", "J1", "JC2", "X1", "RUN"]:
    fail("conformance/runner.py report_order does not follow Family order")

# The runner's fingerprint gives the golden values server-spec states.
spec_md = (ROOT / "server-spec" / "repo-context-and-profiles.md").read_text()
for item, want in (({"name": "Inbox", "layout": "table", "filter": "status:Inbox"}, "9c5ee7e85d3e"),
                   ({"name": "Engage \u2014 Now", "layout": "board", "fingerprint": "x",
                     "manual": ["advisory, not hashed"]}, "14d526f52c0e")):
    if fingerprint(item) != want or f"`{want}`" not in spec_md:
        fail(f"fingerprint golden value {want} disagrees between the runner and the spec")

# tools/spec_pair.py: a spec change needs a conformance change or a Conformance-unchanged trailer.
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
from spec_pair import verdict  # noqa: E402
for files, msg, want in (
        (["server-spec/tools.md"], "Change a tool", False),
        (["server-spec/tools.md", "server-spec/conformance.md"], "Change a tool", False),
        (["server-spec/tools.md", "conformance/runner.py"], "Change a tool", False),
        (["server-spec/tools.md", "server-spec/conformance.md", "conformance/runner.py"], "Change", True),
        (["server-spec/conformance.md"], "Change a check", False),
        (["server-spec/conformance.md", "conformance/runner.py"], "Change a check", True),
        (["conformance/runner.py"], "Fix the runner", True),
        (["server-spec/tools.md"], "Fix a typo\n\nConformance-unchanged: wording only", True),
        (["skills/board-claim/SKILL.md"], "Skill change", True)):
    if verdict(files, msg)[0] != want:
        fail(f"spec_pair verdict for {files} with {msg!r} was not {want}")

if errors:
    print("\n".join(f"FAIL {e}" for e in errors))
    sys.exit(1)
print(f"ok: gtd-board-kit {version}, {len(SKILLS)} skills, BOARD.md {board.stat().st_size} bytes")
