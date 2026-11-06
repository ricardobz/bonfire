"""Collector tests. Run: python3 -m unittest discover tests"""

import io
import json
import os
import sys
import time
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import recap  # noqa: E402

# Nothing containing CANARY may appear in the output JSON.
CANARY = "CANARY"
SECRET_PROJECT = "/home/someone/CANARY-secret-project"
SESSION = "CANARY-session-0001"
NOW = "2026-10-13T23:00:00+00:00"


def setUpModule():
    # Hours and days are local; pinning the timezone makes the test machine-independent.
    os.environ["TZ"] = "America/Sao_Paulo"
    time.tzset()


def user(ts, text, session=SESSION, **extra):
    return {"type": "user", "timestamp": ts, "sessionId": session,
            "cwd": SECRET_PROJECT, "message": {"role": "user", "content": text}, **extra}


def assistant(ts, msg_id, blocks, session=SESSION, usage=None, cwd=SECRET_PROJECT, **extra):
    return {"type": "assistant", "timestamp": ts, "sessionId": session,
            "requestId": f"req-{msg_id}", "cwd": cwd,
            "message": {"id": msg_id, "role": "assistant", "model": "claude-opus-5-5",
                        "content": blocks,
                        "usage": usage or {"input_tokens": 10, "output_tokens": 20,
                                           "cache_creation_input_tokens": 30,
                                           "cache_read_input_tokens": 940}},
            **extra}


def tool(tool_id, name, **tool_input):
    return {"type": "tool_use", "id": tool_id, "name": name, "input": tool_input}


def fixture_lines():
    t = "2026-10-13T{}:00Z".format
    return [
        {"type": "summary", "summary": "CANARY summary of the conversation"},
        user(t("10:00"), "CANARY prompt: please fix the CANARY bug"),
        assistant(t("10:01"), "m1", [{"type": "text", "text": "CANARY answer"}]),
        # Same reply on two lines: usage must not be counted twice.
        assistant(t("10:01"), "m1", [tool("t1", "Edit", file_path="/x/CANARY.py",
                                          old_string="CANARY", new_string="CANARY2")]),
        assistant(t("10:05"), "m2", [tool("t2", "Write", file_path="/x/CANARY.js",
                                          content="CANARY code"),
                                     tool("t3", "Read", file_path="/x/CANARY.md"),
                                     tool("t4", "Bash", command="echo CANARY"),
                                     tool("t5", "mcp__CANARYserver__do", q="CANARY"),
                                     tool("t6", "Agent", prompt="CANARY task")]),
        user(t("10:06"), [{"type": "tool_result", "tool_use_id": "t4",
                           "content": "CANARY output"}]),
        # Long pause: 10:06 -> 11:00 doesn't count as active time.
        user(t("11:00"), "CANARY again"),
        # Not prompts: slash-command echo, meta entry, interruption, IDE context alone.
        user(t("11:01"), "<command-name>/CANARY</command-name>"),
        user(t("11:01"), "CANARY caveat", isMeta=True),
        user(t("11:02"), [{"type": "text", "text": "[Request interrupted by user]"}]),
        user(t("11:02"), [{"type": "text", "text": "<ide_opened_file>CANARY</ide_opened_file>"},
                          {"type": "text", "text": "CANARY typed after IDE context"}]),
        assistant(t("11:04"), "m3", [tool("t7", "Edit", file_path="/x/CANARY.py"),
                                     tool("t8", "Write",
                                          file_path=SECRET_PROJECT + "/CANARY.html")]),
        # Outside the 1-day window, but counts for the streak.
        user("2026-10-12T09:00:00Z", "CANARY yesterday"),
    ]


class RecapTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        project = self.root / recap.encode_project_path(SECRET_PROJECT)
        project.mkdir()
        with (project / f"{SESSION}.jsonl").open("w") as fh:
            for line in fixture_lines():
                fh.write(json.dumps(line) + "\n")
            fh.write("not json CANARY\n")
        sub = project / SESSION / "subagents"
        sub.mkdir(parents=True)
        with (sub / "agent-CANARY.jsonl").open("w") as fh:
            fh.write(json.dumps(assistant("2026-10-13T10:07:00Z", "s1",
                                          [tool("s-t1", "Grep", pattern="CANARY")],
                                          session=SESSION, isSidechain=True)) + "\n")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            recap.main(["--root", str(self.root), "--now", NOW, *args])
        return out.getvalue()

    def test_no_conversation_text_leaks(self):
        for days in ("1", "7"):
            output = self.run_cli("--days", days)
            self.assertNotIn(CANARY.lower(), output.lower())
            self.assertNotIn("/x/", output)
            self.assertNotIn("secret", output)

    def test_aggregates(self):
        data = json.loads(self.run_cli("--days", "1"))
        self.assertEqual(data["projects"], 1)
        self.assertEqual(data["sessions"], 1)  # the subagent is not a session
        self.assertEqual(data["prompts"], 3)  # 10:00, 11:00 and the one after IDE context
        self.assertEqual(data["active_minutes"], 6 + 4)
        self.assertEqual(data["streak_days"], 2)
        self.assertEqual(data["active_days"], 1)
        self.assertEqual(data["tokens"]["output"], 20 * 4)  # m1, m2, m3, s1
        self.assertEqual(data["cache_hit_rate"], 0.959)  # 940 / (10 + 30 + 940)
        self.assertEqual(data["tools"], {"Edit": 2, "Write": 2, "Read": 1, "Bash": 1,
                                         "MCP": 1, "Agent": 1, "Grep": 1})
        self.assertEqual(data["subagents"], 1)
        self.assertEqual(data["files_touched"], 3)
        self.assertEqual(data["languages"], {"Python": 1, "JavaScript": 1, "HTML": 1})
        # /x/ is outside the cwd (like a scratchpad); only the HTML file is in the project.
        self.assertEqual(data["project_files_touched"], 1)
        self.assertEqual(data["project_languages"], {"HTML": 1})
        self.assertEqual(data["models"], {"claude-opus-5-5": 4})

    def test_period_kinds(self):
        week = json.loads(self.run_cli("--days", "7"))["period"]
        self.assertEqual((week["kind"], week["from"]), ("week", "2026-10-07"))
        self.assertEqual(json.loads(self.run_cli("--days", "15"))["period"]["kind"], "sprint")
        self.assertEqual(json.loads(self.run_cli("--days", "30"))["period"]["kind"], "month")
        self.assertEqual(json.loads(self.run_cli("--days", "3"))["period"]["kind"], "custom")

    def test_all_starts_at_first_log_day(self):
        data = json.loads(self.run_cli("--days", "all"))
        self.assertEqual(data["period"], {"days": 2, "kind": "all", "from": "2026-10-12",
                                          "to": "2026-10-13", "timezone": "-0300"})
        self.assertEqual([d["date"] for d in data["heatmap"]], ["2026-10-12", "2026-10-13"])
        self.assertEqual(data["active_days"], 2)

    def test_paths_filter(self):
        self.assertEqual(json.loads(self.run_cli("--paths", SECRET_PROJECT))["sessions"], 1)
        self.assertEqual(json.loads(self.run_cli("--paths", "/other"))["sessions"], 0)

    def test_branch_filter(self):
        project = self.root / recap.encode_project_path(SECRET_PROJECT)
        with (project / "CANARY-task.jsonl").open("w") as fh:
            for ts in ("2026-10-10T12:00:00Z", "2026-10-11T12:00:00Z"):
                fh.write(json.dumps(user(ts, "CANARY task prompt", session="CANARY-task",
                                         gitBranch="fb-CANARY-9999-x")) + "\n")
        out = self.run_cli("--days", "all", "--branch", "CANARY-9999")
        self.assertNotIn(CANARY, out)
        data = json.loads(out)
        self.assertEqual((data["sessions"], data["prompts"]), (1, 2))
        self.assertEqual((data["period"]["kind"], data["period"]["from"]), ("task", "2026-10-10"))
        self.assertEqual(json.loads(self.run_cli("--branch", "OTHER-1"))["sessions"], 0)


class CommitFoldersTest(unittest.TestCase):
    def folders(self, command):
        return list(recap.commit_folders(command, "/work/a"))

    def test_shapes_seen_in_real_sessions(self):
        cases = {
            'git add x && git commit -q -m "msg"': ["/work/a/"],
            "git commit -q -F - <<'E'\nsubject\nE": ["/work/a/"],
            "git commit -F - <<'E'\nsee && git commit\nE\ncd /work/b && git commit -m x": ["/work/a/", "/work/b/"],
            'cd /work/b && git commit -m x': ["/work/b/"],
            'cd ..\ngit -C b commit -q -m x\ngit -C c commit -q -m y': ["/work/a/../b", "/work/a/../c"],
            'FOO=1 git -c user.name=x commit -m y': ["/work/a/"],
            'for r in b; do git -C /work/$r commit -m x; done': ["/work/$r"],
        }
        for command, expected in cases.items():
            with self.subTest(command):
                self.assertEqual(self.folders(command), expected)

    def test_not_new_commits(self):
        for command in ("git commit --amend -q -F -", "git log", "grep 'git commit' notes.md",
                        "cat > notes.md <<'EOF'\ngit commit -m x\nEOF",
                        'echo "git commit -m x"', "git status && git add ."):
            with self.subTest(command):
                self.assertEqual(self.folders(command), [])

    def test_missing_cwd(self):
        self.assertEqual(recap.repo_root(next(recap.commit_folders("git commit -m x", None))), None)


class RepoActivityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "logs"
        self.work = base / "work"
        for repo in ("alpha", "beta", "gamma"):
            (self.work / repo / ".git").mkdir(parents=True)
        (self.work / "plain").mkdir()
        self.project = self.root / "p"
        self.project.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def collect(self, sessions):
        for session, blocks in sessions.items():
            with (self.project / f"{session}.jsonl").open("w") as fh:
                for i, (ts, block) in enumerate(blocks):
                    fh.write(json.dumps(assistant(ts, f"{session}-{i}", [block], session=session,
                                                  cwd=str(self.work / "alpha"))) + "\n")
        return recap.collect(self.root, 3, now=recap.parse_ts(NOW))

    def test_repos_and_commits(self):
        data = self.collect({"one": [
            ("2026-10-13T10:00:00Z", tool("a", "Edit", file_path=f"{self.work}/beta/x.py")),
            ("2026-10-13T10:01:00Z", tool("b", "Bash", command="git commit -m x")),
            ("2026-10-13T10:02:00Z", tool("c", "Bash",
                                          command="cd .. && git -C gamma commit -m y; git -C gamma commit -m z")),
            # Reading, and writing outside any repo, change no repo.
            ("2026-10-13T10:03:00Z", tool("d", "Read", file_path=f"{self.work}/plain/x.py")),
            ("2026-10-13T10:04:00Z", tool("e", "Write", file_path=f"{self.work}/plain/x.py")),
        ]})
        session = data["session_list"][0]
        self.assertEqual((session["repos"], session["commits"]), (3, 3))
        self.assertEqual([d["repos"] for d in data["heatmap"]], [0, 0, 3])
        self.assertEqual([a["id"] for a in data["achievements"] if a["id"] == "fast-travel"],
                         ["fast-travel"])
        self.assertNotIn(self.tmp.name, json.dumps(data))

    def test_projects_join_session_folders_and_changed_repos(self):
        block = ("2026-10-13T10:00:00Z", tool("a", "Edit", file_path=f"{self.work}/beta/x.py"))
        # The log folder "p" holds the session; beta only got changed from there.
        self.assertEqual(self.collect({"one": [block]})["projects"], 2)
        # A planning session with no changes still counts its own folder.
        (self.root / "planning").mkdir()
        with (self.root / "planning" / "two.jsonl").open("w") as fh:
            fh.write(json.dumps(user("2026-10-13T11:00:00Z", "plan", session="two")) + "\n")
        self.assertEqual(recap.collect(self.root, 3, now=recap.parse_ts(NOW))["projects"], 3)

    def test_project_changed_from_its_own_session_counts_once(self):
        self.project.rename(self.root / recap.encode_project_path(self.work / "beta"))
        self.project = self.root / recap.encode_project_path(self.work / "beta")
        block = ("2026-10-13T10:00:00Z", tool("a", "Edit", file_path=f"{self.work}/beta/x.py"))
        self.assertEqual(self.collect({"one": [block]})["projects"], 1)

    def test_day_counts_repos_across_sessions(self):
        edit = lambda i, repo: ("2026-10-13T10:00:00Z", tool(
            i, "Edit", file_path=f"{self.work}/{repo}/x.py"))
        data = self.collect({"one": [edit("a", "alpha"), edit("b", "beta")],
                             "two": [edit("c", "beta"), edit("d", "gamma")]})
        self.assertEqual(sorted(s["repos"] for s in data["session_list"]), [2, 2])
        self.assertEqual(data["heatmap"][-1]["repos"], 3)


class ParseTsTest(unittest.TestCase):
    def test_bad_timestamps_are_skipped(self):
        for value in (None, 123, "", "not a date"):
            with self.subTest(value=value):
                self.assertIsNone(recap.parse_ts(value))

    def test_missing_fromisoformat_is_not_swallowed(self):
        # Python 3.6 has no fromisoformat: that must crash, not yield an empty card.
        with mock.patch.object(recap, "datetime", mock.Mock(spec=[])):
            with self.assertRaises(AttributeError):
                recap.parse_ts(NOW)


if __name__ == "__main__":
    unittest.main()
