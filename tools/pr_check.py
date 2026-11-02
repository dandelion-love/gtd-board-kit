#!/usr/bin/env python3
"""pr_check.py: report whether a pull request carries its evidence, and audit agent actions.

  python3 .gtd/kit/tools/pr_check.py [--repo owner/repo] [--pr N]
        check one pull request: the gtd-pr marker, an Evidence row for every acceptance
        criterion of every issue it carries, a Test changes section that names each changed
        test file, and a claim record on each carried issue
  python3 .gtd/kit/tools/pr_check.py --audit [--repo owner/repo] [--since 24h]
        look back over a repo: agent-ready added by an agent or bot, merges and approvals by
        an agent or bot, and pull requests opened without the gtd-pr marker (outside pr_open)

Report-only by default: findings are printed and the exit status is 0. --enforce exits 1
when there is any finding (for when a person makes the check required). A usage or API
error exits 2. The report goes to stdout and, inside GitHub Actions, to the step summary.

Inside Actions, --repo comes from GITHUB_REPOSITORY and --pr from the event. The token is
read from GITHUB_TOKEN (or GH_TOKEN) and is never printed. Optional settings, as flags or
environment variables (comma-separated lists):

  --server-login / GTD_SERVER_LOGIN      the gtd server's GitHub login (its App bot); a
                                         gtd-pr marker on a PR it did not author is flagged
  --agent-login / GTD_AGENT_LOGINS       logins that are agents; every Bot is one already
  --record-author / GTD_RECORD_AUTHORS   logins whose comments may carry claim records
                                         (server-spec claim-records "Which comments count")

Standard library only. Agents never write .github/workflows/**: a person installs the
template in templates/workflows/ once per repo.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

READY_LABEL = "agent-ready"
PR_MARKER = re.compile(r"<!--\s*gtd-pr v1 (\{.*?\})\s*-->", re.S)
DESK_MARKER = re.compile(r"<!--\s*gtd-desk v1 (\{.*?\})\s*-->", re.S)
# Closes / Fixes / Resolves / Works on / Refs, then one or more issue references.
REF_VERB = re.compile(
    r"\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?|works on|refs?)\b:?\s+"
    r"((?:(?:[\w.-]+/[\w.-]+)?#\d+(?:\s*,\s*|\s+and\s+|\s+)?)+)", re.I)
ISSUE_REF = re.compile(r"(?:([\w.-]+/[\w.-]+))?#(\d+)")
AC_ID = re.compile(r"\bAC(\d+)\b", re.I)
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
EMPTY_RESULT = {"", "-", "—", "todo", "tbd", "?", "n/a"}
TEST_PATH = re.compile(
    r"(^|/)(tests?|__tests__|specs?|fixtures?|__snapshots__|testdata|conformance)/"
    r"|(^|/)test_[^/]*\.py$|_test\.(py|go|rb)$|\.(test|spec)\.[cm]?[jt]sx?$"
    r"|(^|/)(pytest\.ini|conftest\.py|jest\.config\.[^/]*|vitest\.config\.[^/]*)$")


@dataclass(frozen=True)
class Finding:
    rule: str
    where: str
    detail: str

    def line(self) -> str:
        return f"- **{self.rule}** ({self.where}): {self.detail}"


# ---------------------------------------------------------------- pure checks

def section(text: str, title: str) -> str | None:
    """The body under the first Markdown heading named `title` (any level, any case),
    up to the next heading of the same or a higher level. None when there is no such heading."""
    lines = (text or "").splitlines()
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m and m.group(2).strip().rstrip(":").lower() == title.lower():
            level, out = len(m.group(1)), []
            for nxt in lines[i + 1:]:
                h = HEADING.match(nxt)
                if h and len(h.group(1)) <= level:
                    break
                out.append(nxt)
            return "\n".join(out)
    return None


def pr_marker(body: str) -> tuple[dict | None, str | None]:
    """(marker, problem). The marker must appear exactly once and hold by and issues."""
    found = PR_MARKER.findall(body or "")
    if not found:
        return None, "no gtd-pr marker: the PR was not opened through pr_open"
    if len(found) > 1:
        return None, f"{len(found)} gtd-pr markers; pr_open writes exactly one"
    try:
        data = json.loads(found[0])
    except ValueError:
        return None, "the gtd-pr marker is not valid JSON"
    if not isinstance(data, dict) or not isinstance(data.get("by"), str) \
            or not isinstance(data.get("issues"), list) \
            or not all(isinstance(n, int) for n in data["issues"]):
        return None, "the gtd-pr marker lacks by or a list of issue numbers"
    return data, None


def carried_issues(body: str, repo: str, marker: dict | None) -> list[tuple[str, int]]:
    """Every (repo, number) the PR says it carries, in first-seen order: closing keywords,
    Works on and Refs lines, and the marker's issues. Text inside the marker block counts
    the same, so the pr_open visible line is read too."""
    out: list[tuple[str, int]] = []

    def add(r: str, n: int) -> None:
        if (r, n) not in out:
            out.append((r, n))

    text = re.sub(r"```.*?```", "", body or "", flags=re.S)
    for m in REF_VERB.finditer(text):
        for r, n in ISSUE_REF.findall(m.group(2)):
            add(r or repo, int(n))
    for n in (marker or {}).get("issues", []):
        add(repo, n)
    return out


def criteria(issue_body: str) -> tuple[list[str], str | None]:
    """(AC ids like 'AC1', problem) from the issue's Acceptance criteria section."""
    sec = section(issue_body, "Acceptance criteria")
    if sec is None:
        return [], "the issue has no Acceptance criteria section"
    items = [ln for ln in sec.splitlines() if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", ln)]
    ids: list[str] = []
    for ln in items:
        m = AC_ID.search(ln)
        if m and f"AC{m.group(1)}" not in ids:
            ids.append(f"AC{m.group(1)}")
    if not items:
        return [], "the Acceptance criteria section lists no criteria"
    if len(ids) < len(items):
        return ids, "some criteria are not numbered AC1, AC2, ... so their rows cannot be matched"
    return ids, None


def table_rows(sec: str) -> list[list[str]]:
    """Cells of each Markdown table row, header and separator rows dropped."""
    rows = []
    for ln in sec.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", s.strip("|"))]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    if rows and rows[0] and rows[0][0].strip("`* ").lower() in ("ac", "criterion", "issue"):
        rows = rows[1:]
    return rows


def evidence(body: str) -> tuple[list[tuple[tuple[str, int] | None, str, str]], str | None]:
    """[(issue or None, AC id, result)] from the Evidence table. The first cell names the
    criterion: `AC1`, or `#<n> AC1` / `owner/repo#<n> AC1` when the PR carries several issues.
    The result is the last cell."""
    sec = section(body, "Evidence")
    if sec is None:
        return [], "no Evidence section"
    out = []
    for cells in table_rows(sec):
        first = cells[0]
        ac = AC_ID.search(first)
        if not ac:
            continue
        ref = ISSUE_REF.search(first)
        issue = (ref.group(1) or "", int(ref.group(2))) if ref else None
        out.append((issue, f"AC{ac.group(1)}", cells[-1] if len(cells) > 1 else ""))
    if not out:
        return [], "the Evidence section has no table rows naming AC1, AC2, ..."
    return out, None


def check_evidence(body: str, repo: str, issues: dict[tuple[str, int], str]) -> list[Finding]:
    """One finding per criterion with no row or an empty result, per issue carried."""
    findings: list[Finding] = []
    rows, problem = evidence(body)
    several = len(issues) > 1
    any_criteria = False
    for (r, n), issue_body in issues.items():
        where = f"{r}#{n}" if r != repo else f"#{n}"
        ids, issue_problem = criteria(issue_body)
        if issue_problem:
            findings.append(Finding("criteria", where, issue_problem))
        if not ids:
            continue
        any_criteria = True
        if problem:
            continue
        for ac in ids:
            mine = [res for (iss, a, res) in rows if a == ac and (
                (iss is not None and (iss[0] or repo, iss[1]) == (r, n)) or
                (iss is None and not several))]
            if not mine:
                hint = f" (with several issues, write `{where} {ac}`)" if several else ""
                findings.append(Finding("evidence", where, f"{ac} has no Evidence row{hint}"))
            elif all(res.strip("`* ").lower() in EMPTY_RESULT for res in mine):
                findings.append(Finding("evidence", where, f"{ac} has an Evidence row with no result"))
    if problem and any_criteria:
        findings.insert(0, Finding("evidence", "PR body", problem))
    return findings


def check_test_changes(body: str, changed: list[str]) -> list[Finding]:
    """A Test changes section exists and names every changed test file (path or file name)."""
    sec = section(body, "Test changes")
    tests = [p for p in changed if TEST_PATH.search(p)]
    if sec is None:
        detail = "no Test changes section"
        if tests:
            detail += f"; the diff changes {len(tests)} test file(s): " + ", ".join(f"`{p}`" for p in tests[:20])
        return [Finding("test-changes", "PR body", detail)]
    missing = [p for p in tests if p not in sec and p.rsplit("/", 1)[-1] not in sec]
    if missing:
        return [Finding("test-changes", "PR body", "changed test files not named in Test changes: "
                        + ", ".join(f"`{p}`" for p in missing[:20]))]
    return []


def claim_records(comments: list[dict], record_authors: set[str]) -> list[dict]:
    """Claim records in an issue's comments (server-spec claim-records), oldest first."""
    out = []
    for c in comments:
        if record_authors and ((c.get("user") or {}).get("login") or "") not in record_authors:
            continue
        found = DESK_MARKER.findall(c.get("body") or "")
        if len(found) != 1:
            continue
        try:
            rec = json.loads(found[0])
        except ValueError:
            continue
        if isinstance(rec, dict) and rec.get("v") == 1 and rec.get("event") == "claim":
            out.append(rec)
    return out


def check_claims(where: str, records: list[dict], by: str | None) -> list[Finding]:
    """The issue has (or had) a claim; when the marker names who asked, a claim by them."""
    if not records:
        return [Finding("claim", where, "no claim record: the story was never claimed")]
    if by and not any(r.get("by") == by for r in records):
        holders = sorted({str(r.get("by")) for r in records})
        return [Finding("claim", where, f"no claim by {by}, who asked for the PR (claims by: "
                        + ", ".join(holders) + ")")]
    return []


def is_agent(user: dict | None, agent_logins: set[str]) -> bool:
    login = (user or {}).get("login") or ""
    return bool(login) and (login in agent_logins or (user or {}).get("type") == "Bot"
                            or login.endswith("[bot]"))


def check_pr(pr: dict, repo: str, changed: list[str], issues: dict[tuple[str, int], str],
             comments: dict[tuple[str, int], list[dict]], *, server_login: str | None = None,
             record_authors: frozenset[str] = frozenset()) -> list[Finding]:
    """Every PR-mode finding for one PR, given what the API returned."""
    body = pr.get("body") or ""
    findings: list[Finding] = []
    marker, problem = pr_marker(body)
    if problem:
        findings.append(Finding("pr_open", "PR body", problem))
    author = (pr.get("user") or {}).get("login")
    if marker and server_login and author != server_login:
        findings.append(Finding("pr_open", "PR author", f"a gtd-pr marker on a PR authored by "
                                f"{author}, not the server ({server_login})"))
    if not issues:
        findings.append(Finding("issues", "PR body", "carries no issue (Closes, Works on or Refs)"))
    findings += check_evidence(body, repo, issues)
    findings += check_test_changes(body, changed)
    for (r, n) in issues:
        where = f"{r}#{n}" if r != repo else f"#{n}"
        findings += check_claims(where, claim_records(comments.get((r, n), []), set(record_authors)),
                                 (marker or {}).get("by"))
    return findings


def parse_since(text: str, now: datetime) -> datetime:
    m = re.fullmatch(r"(\d+)([hd])", text.strip())
    if not m:
        raise ValueError(f"--since must look like 24h or 7d, not {text!r}")
    n = int(m.group(1))
    return now - (timedelta(hours=n) if m.group(2) == "h" else timedelta(days=n))


def ts(text: str | None) -> datetime | None:
    if not text:
        return None
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def audit(events: list[dict], pulls: list[dict], reviews: dict[int, list[dict]], since: datetime,
          *, agent_logins: frozenset[str] = frozenset(), server_login: str | None = None,
          ready_label: str = READY_LABEL) -> list[Finding]:
    """Audit findings in the window. `events` are repo issue events, `pulls` the PRs
    updated in the window, `reviews` each PR's reviews by number."""
    findings: list[Finding] = []
    agents = set(agent_logins)
    note = " (through the gtd server: GitHub does not record which principal asked)"
    for e in events:
        if e.get("event") != "labeled" or (e.get("label") or {}).get("name") != ready_label:
            continue
        if (ts(e.get("created_at")) or since) < since or not is_agent(e.get("actor"), agents):
            continue
        num = (e.get("issue") or {}).get("number")
        login = e["actor"]["login"]
        findings.append(Finding("agent-ready", f"#{num}", f"{ready_label} added by {login}"
                                + (note if login == server_login else "")))
    for p in pulls:
        num = p.get("number")
        merged = ts(p.get("merged_at"))
        if merged and merged >= since and is_agent(p.get("merged_by"), agents):
            findings.append(Finding("merge", f"#{num}", f"merged by {p['merged_by']['login']}"))
        for r in reviews.get(num, []):
            when = ts(r.get("submitted_at"))
            if r.get("state") == "APPROVED" and when and when >= since and is_agent(r.get("user"), agents):
                findings.append(Finding("approval", f"#{num}", f"approved by {r['user']['login']}"))
        created = ts(p.get("created_at"))
        if created and created >= since:
            _, problem = pr_marker(p.get("body") or "")
            author = (p.get("user") or {}).get("login")
            if problem:
                findings.append(Finding("pr_open", f"#{num}", f"opened by {author} without pr_open: {problem}"))
            elif server_login and author != server_login:
                findings.append(Finding("pr_open", f"#{num}", f"gtd-pr marker on a PR authored by {author}, "
                                        f"not the server ({server_login})"))
    return findings


def report(title: str, findings: list[Finding], notes: list[str]) -> str:
    out = [f"## {title}", ""]
    out += [f"_{n}_" for n in notes] + ([""] if notes else [])
    if findings:
        out.append(f"{len(findings)} finding(s):")
        out.append("")
        out += [f.line() for f in findings]
    else:
        out.append("No findings.")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- GitHub API

class Api:
    def __init__(self, token: str | None, base: str):
        self.token, self.base = token, base.rstrip("/")

    def get(self, path: str, params: dict | None = None) -> tuple[object, dict]:
        url = path if path.startswith("http") else self.base + path
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "gtd-board-kit-pr-check"})
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8") or "null"), dict(resp.headers)
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"GitHub API {e.code} on {urllib.parse.urlsplit(url).path}") from None
        except urllib.error.URLError as e:
            raise RuntimeError(f"GitHub API unreachable: {e.reason}") from None

    def pages(self, path: str, params: dict | None = None, stop=None, limit: int = 20) -> list:
        """Follow Link: next for up to `limit` pages; stop(item) True ends the walk early.
        The next page is asked for on the same /repos/ path with the link's query, because
        GitHub's next links may switch to a /repositories/<id>/ path some proxies refuse."""
        out: list = []
        p = dict(params or {}, per_page=100)
        for _ in range(limit):
            data, headers = self.get(path, p)
            for item in data or []:
                if stop and stop(item):
                    return out
                out.append(item)
            m = re.search(r'<([^>]+)>;\s*rel="next"', headers.get("Link", "") or headers.get("link", ""))
            if not m:
                break
            p = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(m.group(1)).query))
        return out


def listed(flag: list[str] | None, env: str) -> frozenset[str]:
    vals = list(flag or []) + os.environ.get(env, "").split(",")
    return frozenset(v.strip() for v in vals if v.strip())


def event_pr() -> int | None:
    path = os.environ.get("GITHUB_EVENT_PATH")
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            ev = json.load(fh)
    except (OSError, ValueError):
        return None
    return ((ev.get("pull_request") or {}).get("number")) or None


def run_pr(api: Api, repo: str, number: int, a) -> tuple[str, list[Finding]]:
    pr, _ = api.get(f"/repos/{repo}/pulls/{number}")
    changed = [f["filename"] for f in api.pages(f"/repos/{repo}/pulls/{number}/files")]
    marker, _ = pr_marker(pr.get("body") or "")
    issues: dict[tuple[str, int], str] = {}
    comments: dict[tuple[str, int], list[dict]] = {}
    for r, n in carried_issues(pr.get("body") or "", repo, marker):
        try:
            issue, _ = api.get(f"/repos/{r}/issues/{n}")
        except RuntimeError:
            continue  # another repo the token cannot read: reported below as no criteria
        if issue.get("pull_request"):
            continue
        issues[(r, n)] = issue.get("body") or ""
        comments[(r, n)] = api.pages(f"/repos/{r}/issues/{n}/comments")
    findings = check_pr(pr, repo, changed, issues, comments, server_login=a.server_login,
                        record_authors=a.record_authors)
    return f"PR check: {repo} pull request {number}", findings


def run_audit(api: Api, repo: str, a) -> tuple[str, list[Finding]]:
    now = datetime.now(timezone.utc)
    since = parse_since(a.since, now)

    def older(key):
        return lambda item: (ts(item.get(key)) or now) < since

    events = api.pages(f"/repos/{repo}/issues/events", stop=older("created_at"))
    pulls = api.pages(f"/repos/{repo}/pulls", {"state": "all", "sort": "updated", "direction": "desc"},
                      stop=older("updated_at"))
    reviews = {p["number"]: api.pages(f"/repos/{repo}/pulls/{p['number']}/reviews") for p in pulls}
    findings = audit(events, pulls, reviews, since, agent_logins=a.agent_logins,
                     server_login=a.server_login)
    return f"Agent audit: {repo} since {since.strftime('%Y-%m-%dT%H:%M:%SZ')}", findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    ap.add_argument("--pr", type=int)
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--since", default="24h")
    ap.add_argument("--enforce", action="store_true", help="exit 1 when there is any finding")
    ap.add_argument("--server-login", default=os.environ.get("GTD_SERVER_LOGIN") or None)
    ap.add_argument("--agent-login", action="append")
    ap.add_argument("--record-author", action="append")
    a = ap.parse_args(argv)
    a.agent_logins = listed(a.agent_login, "GTD_AGENT_LOGINS")
    a.record_authors = listed(a.record_author, "GTD_RECORD_AUTHORS")
    if not a.repo or not re.fullmatch(r"[\w.-]+/[\w.-]+", a.repo):
        print("pr_check: --repo owner/repo is required (or GITHUB_REPOSITORY)", file=sys.stderr)
        return 2
    api = Api(os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"),
              os.environ.get("GITHUB_API_URL", "https://api.github.com"))
    try:
        if a.audit:
            title, findings = run_audit(api, a.repo, a)
        else:
            number = a.pr or event_pr()
            if not number:
                print("pr_check: --pr N is required outside a pull_request event", file=sys.stderr)
                return 2
            title, findings = run_pr(api, a.repo, number, a)
    except (RuntimeError, ValueError) as e:
        print(f"pr_check: {e}", file=sys.stderr)
        return 2
    mode = "enforcing" if a.enforce else "report-only: findings do not fail the check"
    text = report(title, findings, [mode])
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        try:
            with open(summary, "a", encoding="utf-8") as fh:
                fh.write(text)
        except OSError:
            pass
    return 1 if (a.enforce and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
