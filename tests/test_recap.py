"""Testes do coletor. Rodar: python3 -m unittest discover tests"""

import io
import json
import os
import sys
import time
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import recap  # noqa: E402

# Tudo que tiver CANARY não pode aparecer no JSON de saída.
CANARY = "CANARY"
SECRET_PROJECT = "/home/someone/CANARY-secret-project"
SESSION = "CANARY-session-0001"
NOW = "2026-10-13T23:00:00+00:00"


def setUpModule():
    # Horas e dias são locais; fixar o fuso deixa o teste igual em qualquer máquina.
    os.environ["TZ"] = "America/Sao_Paulo"
    time.tzset()


def user(ts, text, session=SESSION, **extra):
    return {"type": "user", "timestamp": ts, "sessionId": session,
            "cwd": SECRET_PROJECT, "message": {"role": "user", "content": text}, **extra}


def assistant(ts, msg_id, blocks, session=SESSION, usage=None, **extra):
    return {"type": "assistant", "timestamp": ts, "sessionId": session,
            "requestId": f"req-{msg_id}", "cwd": SECRET_PROJECT,
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
        # Mesma resposta em duas linhas: usage não pode contar duas vezes.
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
        # Pausa longa: 10:06 -> 11:00 não conta como tempo ativo.
        user(t("11:00"), "CANARY again"),
        assistant(t("11:04"), "m3", [tool("t7", "Edit", file_path="/x/CANARY.py")]),
        # Fora da janela de 1 dia, mas conta para o streak.
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
        self.assertEqual(data["sessions"], 1)  # o subagent não vira sessão
        self.assertEqual(data["active_minutes"], 6 + 4)
        self.assertEqual(data["streak_days"], 2)
        self.assertEqual(data["active_days"], 1)
        self.assertEqual(data["tokens"]["output"], 20 * 4)  # m1, m2, m3, s1
        self.assertEqual(data["cache_hit_rate"], 0.959)  # 940 / (10 + 30 + 940)
        self.assertEqual(data["tools"], {"Edit": 2, "Write": 1, "Read": 1, "Bash": 1,
                                         "MCP": 1, "Agent": 1, "Grep": 1})
        self.assertEqual(data["subagents"], 1)
        self.assertEqual(data["files_touched"], 2)
        self.assertEqual(data["languages"], {"Python": 1, "JavaScript": 1})
        self.assertEqual(data["models"], {"claude-opus-5-5": 4})

    def test_paths_filter(self):
        self.assertEqual(json.loads(self.run_cli("--paths", SECRET_PROJECT))["sessions"], 1)
        self.assertEqual(json.loads(self.run_cli("--paths", "/other"))["sessions"], 0)


if __name__ == "__main__":
    unittest.main()
