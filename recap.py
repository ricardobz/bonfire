#!/usr/bin/env python3
# /// script
# requires-python = ">=3.7"
# dependencies = []
# ///
"""bonfire collector: reads Claude Code logs and prints JSON with aggregates only.

Privacy: no prompt, reply, path, file name or project name ever leaves this script.
The JSON is built only from numbers and from values in closed lists (tool, model and
language names).

Usage:
    python3 recap.py --days 7
    python3 recap.py --days 1 --paths ~/worktest/bonfire ~/worktest/manezinho-game
"""

import argparse
import json

import achievements
import re
import sys
from collections import Counter
from datetime import datetime, time, timedelta
from pathlib import Path

if sys.version_info < (3, 7):
    sys.exit("bonfire needs Python 3.7+")

DEFAULT_ROOT = Path.home() / ".claude" / "projects"
SUBAGENT_TOOLS = {"Task", "Agent"}
FILE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
PERIOD_KINDS = {1: "day", 7: "week", 15: "sprint", 30: "month"}
LANGUAGES = {
    ".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".html": "HTML", ".htm": "HTML", ".css": "CSS", ".scss": "CSS",
    ".json": "JSON", ".md": "Markdown", ".sh": "Shell", ".bash": "Shell",
    ".go": "Go", ".rs": "Rust", ".java": "Java", ".kt": "Kotlin", ".rb": "Ruby",
    ".php": "PHP", ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++", ".cs": "C#",
    ".swift": "Swift", ".lua": "Lua", ".sql": "SQL", ".yml": "YAML", ".yaml": "YAML",
    ".toml": "TOML", ".ipynb": "Jupyter", ".svg": "SVG",
}


def encode_project_path(path):
    """Same scheme as Claude Code: anything non-alphanumeric becomes '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(Path(path).expanduser().resolve()))


def parse_ts(value):
    # Only bad timestamps become None; anything else (e.g. Python < 3.7) must fail loudly.
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone()
    except ValueError:
        return None


def iter_entries(project_dirs):
    """Yields (project dir, is_subagent, entry) for every valid line."""
    for project_dir in project_dirs:
        for log in sorted(project_dir.rglob("*.jsonl")):
            in_subagents = "subagents" in log.relative_to(project_dir).parts
            with log.open(encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(entry, dict):
                        yield project_dir, in_subagents or bool(entry.get("isSidechain")), entry


def tool_label(name):
    # MCP tool names carry the server name; grouping them avoids leaking it.
    return "MCP" if name.startswith("mcp__") else name


def is_prompt(entry):
    """A message the user typed: not a tool result, slash-command echo, IDE context
    or interruption notice. Only checks how the text starts, never stores it."""
    if entry.get("isMeta"):
        return False
    content = (entry.get("message") or {}).get("content")
    texts = [content] if isinstance(content, str) else [
        b.get("text") for b in content if isinstance(b, dict) and b.get("type") == "text"
    ] if isinstance(content, list) else []
    return any(isinstance(t, str) and t.strip()
               and not t.startswith(("<", "[Request interrupted")) for t in texts)


def active_minutes(times, idle_gap):
    times = sorted(times)
    total = sum((b - a for a, b in zip(times, times[1:]) if b - a <= idle_gap), timedelta())
    return round(total.total_seconds() / 60)


def streak_until(days, last_day):
    streak, day = 0, last_day
    while day in days:
        streak += 1
        day -= timedelta(days=1)
    return streak


def collect(root, days, paths=None, now=None, idle_minutes=15):
    """days: number of days including today, or "all" for everything still in the logs."""
    now = now or datetime.now().astimezone()
    kind = "all" if days == "all" else PERIOD_KINDS.get(days, "custom")
    start = None if days == "all" else (now - timedelta(days=days - 1)).replace(
        hour=0, minute=0, second=0, microsecond=0)
    idle_gap = timedelta(minutes=idle_minutes)

    if paths:
        project_dirs = [root / encode_project_path(p) for p in paths]
    else:
        project_dirs = [d for d in sorted(root.iterdir()) if d.is_dir()] if root.is_dir() else []
    project_dirs = [d for d in project_dirs if d.is_dir()]

    all_days = set()
    session_times = {}
    session_edits = Counter()
    projects = set()
    tokens = Counter()
    tools = Counter()
    models = Counter()
    hours = Counter()
    heatmap = {}
    seen_messages, seen_tools = set(), set()
    files_touched, project_files = set(), set()
    languages, project_languages = Counter(), Counter()
    subagents = 0
    prompts = 0

    for project_dir, sidechain, entry in iter_entries(project_dirs):
        if entry.get("type") not in ("user", "assistant"):
            continue
        ts = parse_ts(entry.get("timestamp"))
        if ts is None:
            continue
        all_days.add(ts.date())
        if ts > now or (start and ts < start):
            continue

        projects.add(project_dir.name)
        heatmap.setdefault(ts.date(), [0] * 24)[ts.hour] += 1
        hours[ts.hour] += 1
        if not sidechain and entry.get("sessionId"):
            session_times.setdefault(entry["sessionId"], []).append(ts)
        if entry["type"] == "user" and not sidechain and is_prompt(entry):
            prompts += 1

        message = entry.get("message")
        if entry["type"] != "assistant" or not isinstance(message, dict):
            continue

        # One reply can span several lines with the same id and the same usage.
        message_key = (message.get("id"), entry.get("requestId"))
        if message_key == (None, None) or message_key not in seen_messages:
            seen_messages.add(message_key)
            usage = message.get("usage") or {}
            for field in ("input_tokens", "output_tokens",
                          "cache_creation_input_tokens", "cache_read_input_tokens"):
                value = usage.get(field)
                if isinstance(value, int):
                    tokens[field] += value
            model = message.get("model")
            if isinstance(model, str) and model.startswith("claude"):
                models[model] += 1

        content = message.get("content")
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            if block.get("id") in seen_tools:
                continue
            seen_tools.add(block.get("id"))
            name = str(block.get("name", "?"))
            tools[tool_label(name)] += 1
            if name in SUBAGENT_TOOLS:
                subagents += 1
            if name in FILE_TOOLS:
                session_edits[entry.get("sessionId")] += 1
            tool_input = block.get("input") or {}
            file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
            if name in FILE_TOOLS and isinstance(file_path, str):
                language = LANGUAGES.get(Path(file_path).suffix.lower(), "Other")
                if file_path not in files_touched:
                    files_touched.add(file_path)
                    languages[language] += 1
                # Project-only view: skips scratchpad, /tmp and other files outside the cwd.
                cwd = entry.get("cwd")
                if (file_path not in project_files and isinstance(cwd, str)
                        and Path(file_path).is_relative_to(cwd)):
                    project_files.add(file_path)
                    project_languages[language] += 1

    if start is None:
        first_day = min(all_days, default=now.date())
        start = datetime.combine(first_day, time.min, tzinfo=now.tzinfo)
        days = (now.date() - first_day).days + 1
    for i in range(days):
        heatmap.setdefault((start + timedelta(days=i)).date(), [0] * 24)

    sessions = []
    for session_id, times in session_times.items():
        times.sort()
        sessions.append({
            "start": times[0].isoformat(timespec="minutes"),
            "end": times[-1].isoformat(timespec="minutes"),
            "active_minutes": active_minutes(times, idle_gap),
            "wall_minutes": round((times[-1] - times[0]).total_seconds() / 60),
            "edits": session_edits[session_id],
        })
    sessions.sort(key=lambda s: s["start"])

    cache_read = tokens["cache_read_input_tokens"]
    prompt_total = tokens["input_tokens"] + cache_read + tokens["cache_creation_input_tokens"]
    active_days = sorted(d for d in all_days if start.date() <= d <= now.date())

    recap = {
        "version": 1,
        "period": {
            "days": days,
            "kind": kind,
            "from": start.date().isoformat(),
            "to": now.date().isoformat(),
            "timezone": now.strftime("%z"),
        },
        "projects": len(projects),
        "sessions": len(sessions),
        "prompts": prompts,
        "active_minutes": sum(s["active_minutes"] for s in sessions),
        "active_days": len(active_days),
        "streak_days": streak_until(all_days, active_days[-1]) if active_days else 0,
        "longest_session_minutes": max((s["active_minutes"] for s in sessions), default=0),
        "tokens": {
            "input": tokens["input_tokens"],
            "output": tokens["output_tokens"],
            "cache_read": cache_read,
            "cache_creation": tokens["cache_creation_input_tokens"],
        },
        "cache_hit_rate": round(cache_read / prompt_total, 3) if prompt_total else 0.0,
        "tools": dict(tools.most_common()),
        "subagents": subagents,
        "files_touched": len(files_touched),
        "languages": dict(languages.most_common()),
        "project_files_touched": len(project_files),
        "project_languages": dict(project_languages.most_common()),
        "models": dict(models.most_common()),
        "peak_hour": hours.most_common(1)[0][0] if hours else None,
        "heatmap": [{"date": d.isoformat(), "weekday": d.strftime("%a"), "hours": h}
                    for d, h in sorted(heatmap.items())],
        "session_list": sessions,
    }
    recap["achievements"] = achievements.evaluate(recap)
    return recap


def main(argv=None):
    parser = argparse.ArgumentParser(description="Aggregated summary of Claude Code usage.")
    parser.add_argument("--days", type=lambda v: v if v == "all" else int(v), default=7,
                        help='window in days including today (1 = today, 7, 15, 30) or "all"')
    parser.add_argument("--paths", nargs="+", help="only these project folders (default: all)")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--now", help=argparse.SUPPRESS)  # ISO, for tests
    parser.add_argument("--idle-minutes", type=int, default=15,
                        help="pauses longer than this don't count as active time")
    parser.add_argument("--out", type=Path, help="write the JSON here instead of stdout")
    args = parser.parse_args(argv)
    if args.days != "all" and args.days < 1:
        parser.error("--days must be >= 1")

    now = parse_ts(args.now) if args.now else None
    recap = collect(args.root, args.days, args.paths, now, args.idle_minutes)
    text = json.dumps(recap, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
