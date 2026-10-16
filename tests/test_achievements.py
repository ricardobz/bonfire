"""Achievement tests. Run: python3 -m unittest discover tests"""

import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import achievements  # noqa: E402


def day(date, *active_hours):
    return {"date": date, "hours": [1 if h in active_hours else 0 for h in range(24)]}


def session(start, active_minutes=30, edits=0, end=None, wall_minutes=None):
    return {"start": start, "end": end or start, "active_minutes": active_minutes,
            "wall_minutes": active_minutes if wall_minutes is None else wall_minutes,
            "edits": edits}


def base_recap(**overrides):
    recap = {
        "streak_days": 1, "longest_session_minutes": 60, "subagents": 0,
        "cache_hit_rate": 0.5, "tools": {"Read": 1, "Edit": 5, "Write": 5},
        "languages": {"Python": 1},
        "heatmap": [day("2026-10-08", 20)],  # Thursday
        "session_list": [session("2026-10-08T20:00-03:00")],
        "period": {"days": 7}, "active_days": 1, "projects": 1,
    }
    recap.update(overrides)
    return recap


def unlocked(recap):
    return {a["id"] for a in achievements.evaluate(recap)}


class AchievementsTest(unittest.TestCase):
    def test_rules_file_is_valid(self):
        for rule in achievements.load_rules():
            self.assertEqual(set(rule), {"id", "name", "description", "check", "params"})
            check = achievements.CHECKS[rule["check"]]
            inspect.signature(check).bind(None, **rule["params"])

    def test_nothing_unlocked_on_a_plain_week(self):
        self.assertEqual(unlocked(base_recap()), set())

    def test_each_achievement(self):
        cases = {
            "night-owl": {"heatmap": [day("2026-10-08", 3)]},
            "early-bird": {"session_list": [session("2026-10-08T05:40-03:00")]},
            "marathon": {"longest_session_minutes": 241},
            "speedrun": {"session_list": [session("2026-10-08T20:00-03:00", 9, edits=1)]},
            "streak-7": {"streak_days": 7},
            "polyglot": {"languages": dict.fromkeys(["Python", "JavaScript", "HTML",
                                                     "CSS", "Shell"], 1)},
            "delegator": {"subagents": 10},
            "cache-lord": {"cache_hit_rate": 0.91},
            "weekend-warrior": {"heatmap": [day("2026-10-10", 15), day("2026-10-11", 15)]},
            "read-the-manual": {"tools": {"Read": 6, "Edit": 3, "Write": 2}},
            "work-life-balance": {"heatmap": [day("2026-10-08", 9, 17)]},
            "midnight-oil": {"heatmap": [day("2026-10-08", 1)]},
            "burst": {"session_list": [session(f"2026-10-08T{h}:00-03:00") for h in range(14, 19)]},
            "unfinished-business": {"session_list": [session(
                "2026-10-08T20:00-03:00", end="2026-10-09T21:00-03:00", wall_minutes=1500)]},
            "surgeon": {"tools": {"Read": 1, "Edit": 9, "Write": 3}},
            "token-tycoon": {"tokens": {"output": 1_000_000}},
            "special": {"tools": dict.fromkeys(["Read", "Edit", "Write", "Bash", "Grep",
                                                "Glob", "Agent"], 1)},
            "lone-wanderer": {"projects": 6},
            "war-never-changes": {"active_days": 7},
        }
        self.assertEqual(set(cases), {r["id"] for r in achievements.load_rules()})
        for achievement_id, overrides in cases.items():
            with self.subTest(achievement_id):
                self.assertEqual(unlocked(base_recap(**overrides)), {achievement_id})

    def test_edge_cases(self):
        # Speedrun needs an edit; a lightning session that changes no code doesn't count.
        self.assertEqual(unlocked(base_recap(session_list=[session("2026-10-08T20:00-03:00", 0)])), set())
        # A Sunday plus the following Saturday is not a full weekend.
        self.assertEqual(unlocked(base_recap(heatmap=[day("2026-10-04", 9), day("2026-10-10", 9)])), set())
        # A one-day card is always "every day"; War Never Changes needs a 7+ day period.
        self.assertEqual(unlocked(base_recap(period={"days": 1})), set())
        # 'Other' doesn't count as a language.
        langs = dict.fromkeys(["Python", "JavaScript", "HTML", "CSS", "Other"], 1)
        self.assertEqual(unlocked(base_recap(languages=langs)), set())
        # Write counts as an edit too.
        self.assertEqual(unlocked(base_recap(tools={"Read": 5, "Edit": 3, "Write": 2})), set())
        # Work-Life Balance: one evening hour or a Saturday breaks it; no activity isn't balance.
        self.assertEqual(unlocked(base_recap(heatmap=[day("2026-10-08", 10, 19)])), set())
        self.assertEqual(unlocked(base_recap(heatmap=[day("2026-10-10", 10)])), set())
        self.assertNotIn("work-life-balance", unlocked(base_recap(heatmap=[day("2026-10-08")])))
        # Crossing midnight in a late session is not "resumed on another day".
        late = session("2026-10-08T23:30-03:00", end="2026-10-09T00:30-03:00", wall_minutes=60)
        self.assertEqual(unlocked(base_recap(session_list=[late])), set())
        # Surgeon needs edits: no tools at all doesn't count.
        self.assertNotIn("surgeon", unlocked(base_recap(tools={})))
        # A missing tool counts as 0.
        self.assertEqual(unlocked(base_recap(tools={"Read": 1})), {"read-the-manual"})


if __name__ == "__main__":
    unittest.main()
