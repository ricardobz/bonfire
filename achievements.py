"""bonfire achievements: applies the rules in data/achievements.json to the recap JSON.

To add an achievement, just add an entry to the JSON using one of the checks below.
This file only needs changing when a rule needs a new kind of check.
"""

import json
from datetime import date, timedelta
from pathlib import Path

RULES_FILE = Path(__file__).resolve().parent / "data" / "achievements.json"


def read_metric(recap, path):
    """Reads a value by dotted path, e.g. 'tools.Read'. Missing counts as 0."""
    value = recap
    for key in path.split("."):
        value = value.get(key, 0) if isinstance(value, dict) else 0
    return value


def at_least(recap, metric, value):
    return read_metric(recap, metric) >= value


def greater_than(recap, metric, value):
    return read_metric(recap, metric) > value


def metric_greater_than_sum(recap, metric, others):
    return read_metric(recap, metric) > sum(read_metric(recap, o) for o in others)


def count_keys_at_least(recap, metric, value, ignore=()):
    return len([k for k in read_metric(recap, metric) or {} if k not in ignore]) >= value


def active_between_hours(recap, **hours):
    return any(any(day["hours"][h] for h in hour_range(**hours)) for day in recap["heatmap"])


def session_starts_between_hours(recap, **hours):
    return any(int(s["start"][11:13]) in hour_range(**hours) for s in recap["session_list"])


def quick_session(recap, max_active_minutes, min_edits):
    return any(s["active_minutes"] <= max_active_minutes and s.get("edits", 0) >= min_edits
               for s in recap["session_list"])


def full_weekend(recap):
    active = {date.fromisoformat(d["date"]) for d in recap["heatmap"] if any(d["hours"])}
    return any(d.weekday() == 5 and d + timedelta(days=1) in active for d in active)


def hour_range(**hours):
    return range(hours["from"], hours["to"])


CHECKS = {f.__name__: f for f in (
    at_least, greater_than, metric_greater_than_sum, count_keys_at_least,
    active_between_hours, session_starts_between_hours, quick_session, full_weekend,
)}


def load_rules(path=RULES_FILE):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evaluate(recap, rules=None):
    """Unlocked achievements, in rules-file order."""
    return [{"id": r["id"], "name": r["name"], "description": r["description"]}
            for r in (rules if rules is not None else load_rules())
            if CHECKS[r["check"]](recap, **r["params"])]
