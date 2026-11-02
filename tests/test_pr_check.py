#!/usr/bin/env python3
"""Offline tests for tools/pr_check.py: the pure checks, no network. Standard library only.

Issue references are built at run time (H + number) so this file passes public_guard.
"""
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import pr_check as pc  # noqa: E402

H = "#"
REPO = "owner/repo"
T = "2026-01-01T12:00:00Z"


def marker(by="agent:example", issues=(12,)):
    return "<!-- gtd-pr v1 " + json.dumps({"by": by, "issues": list(issues), "t": T, "v": 1}) + " -->"


def claim(by="agent:example", login="server[bot]"):
    rec = {"by": by, "event": "claim", "lease_until": T, "t": T, "v": 1}
    return {"user": {"login": login}, "body": "### Claimed\n\n<!-- gtd-desk v1 " + json.dumps(rec) + " -->"}


ISSUE = """Some context.

## Acceptance criteria
- [ ] AC1: an empty title is refused.
- [ ] AC2: a saved item shows first.

## Open questions
- none
"""

GOOD = f"""Closes {H}12

## Evidence
| AC | Kind | Check | Result |
| --- | --- | --- | --- |
| AC1 | test | test_empty_title | pass |
| AC2 | test | test_order | pass |

## Test changes
- `tests/test_form.py`: new tests for AC1 and AC2

---
Opened through the gtd MCP server for **agent:example**. Works on {H}12.

{marker()}
"""


class Parsing(unittest.TestCase):
    def test_section_stops_at_same_level(self):
        self.assertIn("AC2", pc.section(ISSUE, "acceptance criteria"))
        self.assertNotIn("none", pc.section(ISSUE, "Acceptance criteria"))
        self.assertIsNone(pc.section(ISSUE, "Evidence"))

    def test_carried_issues(self):
        body = f"Closes {H}12, {H}15 and other/thing{H}3\nRefs {H}7\nsee {H}99 later\n```\nFixes {H}50\n```"
        got = pc.carried_issues(body, REPO, {"issues": [12, 20]})
        self.assertEqual(got, [(REPO, 12), (REPO, 15), ("other/thing", 3), (REPO, 7), (REPO, 20)])

    def test_marker(self):
        self.assertEqual(pc.pr_marker(GOOD)[0]["by"], "agent:example")
        self.assertIn("no gtd-pr marker", pc.pr_marker("Closes")[1])
        self.assertIn("2 gtd-pr", pc.pr_marker(marker() + marker())[1])
        self.assertIn("not valid JSON", pc.pr_marker("<!-- gtd-pr v1 {nope} -->")[1])
        self.assertIn("lacks", pc.pr_marker('<!-- gtd-pr v1 {"by": "x"} -->')[1])

    def test_criteria(self):
        self.assertEqual(pc.criteria(ISSUE), (["AC1", "AC2"], None))
        self.assertIn("no Acceptance", pc.criteria("just text")[1])
        ids, problem = pc.criteria("## Acceptance criteria\n- AC1: x\n- y\n")
        self.assertEqual(ids, ["AC1"])
        self.assertIn("not numbered", problem)


class PrMode(unittest.TestCase):
    def run_check(self, body, changed=("tests/test_form.py", "src/form.py"), issues=None,
                  comments=None, author="server[bot]", **kw):
        issues = {(REPO, 12): ISSUE} if issues is None else issues
        comments = {(REPO, 12): [claim()]} if comments is None else comments
        pr = {"body": body, "user": {"login": author}}
        return pc.check_pr(pr, REPO, list(changed), issues, comments, **kw)

    def rules(self, findings):
        return [f.rule for f in findings]

    def test_good_pr_is_clean(self):
        self.assertEqual(self.run_check(GOOD, server_login="server[bot]"), [])

    def test_missing_row_and_empty_result(self):
        body = GOOD.replace("| AC2 | test | test_order | pass |\n", "").replace("| pass |", "| |", 1)
        details = [f.detail for f in self.run_check(body)]
        self.assertIn("AC1 has an Evidence row with no result", details)
        self.assertIn("AC2 has no Evidence row", details)

    def test_no_evidence_section(self):
        body = GOOD.split("## Evidence")[0] + "## Test changes\n- none\n" + marker()
        self.assertTrue(any(f.detail == "no Evidence section" for f in self.run_check(body, changed=[])))

    def test_several_issues_need_prefixed_rows(self):
        issues = {(REPO, 12): ISSUE, (REPO, 15): ISSUE}
        comments = {k: [claim()] for k in issues}
        body = GOOD.replace("Closes ", f"Closes {H}15 ")
        found = self.run_check(body, issues=issues, comments=comments)
        self.assertEqual(sum(f.rule == "evidence" for f in found), 4)
        rows = "".join(f"| {H}{n} AC{a} | test | t | pass |\n" for n in (12, 15) for a in (1, 2))
        body2 = body.replace("| AC1 | test | test_empty_title | pass |\n| AC2 | test | test_order | pass |\n", rows)
        self.assertEqual(self.run_check(body2, issues=issues, comments=comments), [])

    def test_test_changes(self):
        body = GOOD.replace("## Test changes\n- `tests/test_form.py`: new tests for AC1 and AC2\n", "")
        f = self.run_check(body)
        self.assertIn("test-changes", self.rules(f))
        self.assertIn("tests/test_form.py", f[-1].detail if f[-1].rule == "test-changes" else
                      next(x.detail for x in f if x.rule == "test-changes"))
        f2 = self.run_check(GOOD, changed=["tests/test_form.py", "web/app.spec.ts", "conftest.py"])
        detail = next(x.detail for x in f2 if x.rule == "test-changes")
        self.assertIn("web/app.spec.ts", detail)
        self.assertIn("conftest.py", detail)
        self.assertNotIn("tests/test_form.py", detail)

    def test_outside_pr_open_and_forged_marker(self):
        self.assertIn("pr_open", self.rules(self.run_check(GOOD.replace(marker(), ""))))
        forged = self.run_check(GOOD, author="someone", server_login="server[bot]")
        self.assertTrue(any("not the server" in f.detail for f in forged))

    def test_claims(self):
        self.assertIn("never claimed", self.run_check(GOOD, comments={(REPO, 12): []})[0].detail)
        other = self.run_check(GOOD, comments={(REPO, 12): [claim(by="agent:other")]})
        self.assertIn("no claim by agent:example", other[0].detail)
        pasted = self.run_check(GOOD, comments={(REPO, 12): [claim(login="someone")]},
                                record_authors=frozenset({"server[bot]"}))
        self.assertIn("never claimed", pasted[0].detail)

    def test_no_issue(self):
        self.assertIn("issues", self.rules(self.run_check("text", issues={}, comments={})))


class AuditMode(unittest.TestCase):
    since = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def test_audit(self):
        bot = {"login": "server[bot]", "type": "Bot"}
        person = {"login": "owner", "type": "User"}
        events = [
            {"event": "labeled", "label": {"name": "agent-ready"}, "actor": bot, "created_at": T, "issue": {"number": 4}},
            {"event": "labeled", "label": {"name": "agent-ready"}, "actor": person, "created_at": T, "issue": {"number": 5}},
            {"event": "labeled", "label": {"name": "agent-ready"}, "actor": {"login": "codex-runner"},
             "created_at": T, "issue": {"number": 6}},
            {"event": "labeled", "label": {"name": "bug"}, "actor": bot, "created_at": T, "issue": {"number": 7}},
            {"event": "labeled", "label": {"name": "agent-ready"}, "actor": bot, "created_at": "2025-12-01T00:00:00Z",
             "issue": {"number": 8}},
        ]
        pulls = [
            {"number": 1, "created_at": T, "merged_at": T, "merged_by": bot, "body": "x", "user": person},
            {"number": 2, "created_at": T, "merged_at": None, "body": GOOD, "user": bot},
            {"number": 3, "created_at": "2025-12-01T00:00:00Z", "merged_at": T, "merged_by": person,
             "body": "", "user": person},
        ]
        reviews = {2: [{"state": "APPROVED", "submitted_at": T, "user": bot},
                       {"state": "APPROVED", "submitted_at": T, "user": person}]}
        got = pc.audit(events, pulls, reviews, self.since, agent_logins=frozenset({"codex-runner"}),
                       server_login="server[bot]")
        self.assertEqual([(f.rule, f.where) for f in got],
                         [("agent-ready", H + "4"), ("agent-ready", H + "6"), ("merge", H + "1"),
                          ("pr_open", H + "1"), ("approval", H + "2")])
        self.assertIn("through the gtd server", got[0].detail)

    def test_since(self):
        now = datetime(2026, 1, 2, tzinfo=timezone.utc)
        self.assertEqual(pc.parse_since("24h", now), datetime(2026, 1, 1, tzinfo=timezone.utc))
        with self.assertRaises(ValueError):
            pc.parse_since("soon", now)


class Exit(unittest.TestCase):
    def test_usage_error_is_2(self):
        self.assertEqual(pc.main(["--repo", "not a repo"]), 2)


if __name__ == "__main__":
    unittest.main()
