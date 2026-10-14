"""Testes do card (sem Chrome). Rodar: python3 -m unittest discover tests"""

import sys
import unittest
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import render  # noqa: E402


def recap(days=7, kind="week", **overrides):
    data = {
        "period": {"days": days, "kind": kind, "from": "2026-10-08", "to": "2026-10-14"},
        "projects": 1, "sessions": 3, "active_minutes": 125,
        "tokens": {"output": 530_000}, "cache_hit_rate": 0.986,
        "tools": {"Bash": 3, "Read": 2, "Write": 1, "Edit": 1},
        "languages": {"Python": 2},
        "heatmap": [{"date": "2026-10-08", "hours": [0] * 20 + [4, 2, 0, 0]}],
        "achievements": [{"name": f"A{i}"} for i in range(6)],
    }
    data.update(overrides)
    return data


class RenderTest(unittest.TestCase):
    def test_formatting(self):
        self.assertEqual(render.format_minutes(483), "8h03")
        self.assertEqual(render.format_minutes(23), "23m")
        self.assertEqual(render.format_count(530_000), "530k")
        self.assertEqual(render.format_count(1_250_000), "1.2M")
        self.assertEqual(render.format_count(950), "950")
        self.assertEqual(render.format_period({"from": "2026-09-30", "to": "2026-10-06"}, 2),
                         "Sep 30 – Oct 6, 2026 · 2 projects")
        self.assertEqual(render.format_period({"from": "2026-10-14", "to": "2026-10-14"}, 1),
                         "Oct 14, 2026 · 1 project")

    def test_every_theme_builds(self):
        for theme_id, theme in render.load_themes().items():
            with self.subTest(theme_id):
                self.assertTrue((render.ROOT / theme["background"]).is_file())
                html = render.build_html(recap(), theme_id)
                self.assertIn(escape(theme["title"]["week"]), html)
                self.assertNotIn("$", html)  # nenhum placeholder sobrando

    def test_day_title_and_badge_overflow(self):
        html = render.build_html(recap(days=1, kind="day"), "end-of-day")
        self.assertIn("Today&#x27;s harvest is in", html)
        self.assertEqual(html.count('class="badge"'), render.MAX_BADGES + 1)
        self.assertIn("+2", html)

    def test_period_titles(self):
        theme = render.load_themes()["bonfire"]
        self.assertEqual(render.title_for(theme, {"kind": "sprint"}), "Quests of the sprint cleared")
        self.assertEqual(render.title_for(theme, {"kind": "custom"}), theme["title"]["week"])
        self.assertEqual(render.title_for(render.load_themes()["save-star"], {"kind": "all"}),
                         "Filled with determination")

    def test_long_heatmap_collapses_to_weekdays(self):
        days = [{"date": f"2026-10-{d:02d}", "hours": [1] + [0] * 23} for d in range(1, 31)]
        rows = render.heatmap_rows(days)
        self.assertEqual([label for label, _ in rows], list("MTWTFSS"))
        # Out/2026 começa numa quinta: 5 quintas, sextas e sábados; 4 dos outros dias.
        self.assertEqual([hours[0] for _, hours in rows], [4, 4, 4, 5, 5, 4, 4])
        self.assertEqual(len(render.heatmap_rows(days[:7])), 7)

    def test_alias_replaces_project_count(self):
        html = render.build_html(recap(), "bonfire", alias="Floripa <Game>")
        self.assertIn("Floripa &lt;Game&gt;", html)
        self.assertNotIn("1 project", html)

    def test_text_is_escaped(self):
        html = render.build_html(recap(tools={"<script>": 1}), "bonfire")
        self.assertNotIn("<script>", html)


if __name__ == "__main__":
    unittest.main()
