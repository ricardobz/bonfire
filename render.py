#!/usr/bin/env python3
"""Renders the bonfire card: recap JSON + theme -> 1080x1920 PNG via headless Chrome.

Usage:
    python3 recap.py --days 7 --out recap_week.json
    python3 render.py recap_week.json --theme bonfire --out card.png
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent
CARD_DIR = ROOT / "card"
THEMES_FILE = ROOT / "data" / "themes.json"
WIDTH, HEIGHT = 1080, 1920
MAX_BADGES = 4
CHROME_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")


def load_themes():
    return json.loads(THEMES_FILE.read_text(encoding="utf-8"))


def format_minutes(minutes):
    hours, rest = divmod(minutes, 60)
    return f"{hours}h{rest:02d}" if hours else f"{rest}m"


def format_count(value):
    for limit, suffix in ((1_000_000_000, "B"), (1_000_000, "M"), (1_000, "k")):
        if value >= limit:
            short = value / limit
            return f"{short:.1f}{suffix}" if short < 10 else f"{short:.0f}{suffix}"
    return str(value)


def format_period(period, projects, alias=None):
    start, end = date.fromisoformat(period["from"]), date.fromisoformat(period["to"])
    if start == end:
        span = f"{end:%b} {end.day}, {end.year}"
    elif start.month == end.month:
        span = f"{start:%b} {start.day} – {end.day}, {end.year}"
    else:
        span = f"{start:%b} {start.day} – {end:%b} {end.day}, {end.year}"
    if alias:
        return f"{span} · {alias}"
    noun = "project" if projects == 1 else "projects"
    return f"{span} · {projects} {noun}"


def title_for(theme, period):
    """Title for the period (day/week/sprint/month/all); falls back to the week title."""
    titles = theme["title"]
    return titles.get(period.get("kind")) or titles["week"]


def stats_html(recap):
    # Older JSON without prompts still shows active time.
    first = ((format_count(recap["prompts"]), "prompts") if "prompts" in recap
             else (format_minutes(recap["active_minutes"]), "active"))
    stats = [
        first,
        (str(recap["sessions"]), "sessions"),
        (format_count(recap["tokens"]["output"]), "tokens out"),
        (f"{recap['cache_hit_rate'] * 100:.1f}%", "cache hit"),
    ]
    return "".join(f'<div class="stat"><b>{escape(v)}</b><span>{escape(k)}</span></div>'
                   for v, k in stats)


def heatmap_rows(heatmap):
    """Up to 7 days: one row per day. Longer: summed by weekday (Mon to Sun)."""
    if len(heatmap) <= 7:
        return [(date.fromisoformat(d["date"]).strftime("%a")[0], d["hours"]) for d in heatmap]
    weekdays = [[0] * 24 for _ in range(7)]
    for day in heatmap:
        row = weekdays[date.fromisoformat(day["date"]).weekday()]
        for hour, count in enumerate(day["hours"]):
            row[hour] += count
    return list(zip("MTWTFSS", weekdays))


def heatmap_html(recap):
    rows_data = heatmap_rows(recap["heatmap"])
    peak = max((h for _, hours in rows_data for h in hours), default=0) or 1
    rows = []
    for label, hours in rows_data:
        cells = "".join(
            f'<i class="cell on" style="--level: {0.25 + 0.75 * h / peak:.2f}"></i>' if h
            else '<i class="cell"></i>'
            for h in hours)
        rows.append(f'<span class="day">{label}</span>{cells}')
    return "".join(rows)


def percent(count, total):
    share = round(100 * count / total)
    return f"{share}%" if share else "<1%"


def ranked_line(label, items, limit=3):
    """Top items as a share of the whole, e.g. 'Bash 66% · Read 26%'."""
    total = sum(items.values()) if items else 0
    if not total:
        return ""
    top = " · ".join(f"{escape(name)} {escape(percent(count, total))}"
                     for name, count in list(items.items())[:limit])
    return f'<span class="label">{label}</span> {top}'


def badges_html(recap):
    unlocked = recap.get("achievements", [])
    badges = [f'<span class="badge">{escape(a["name"])}</span>' for a in unlocked[:MAX_BADGES]]
    if len(unlocked) > MAX_BADGES:
        badges.append(f'<span class="badge">+{len(unlocked) - MAX_BADGES}</span>')
    return "".join(badges)


def build_html(recap, theme_id, themes=None, alias=None):
    theme = (themes or load_themes())[theme_id]
    template = Template((CARD_DIR / "card.html").read_text(encoding="utf-8"))
    return template.substitute(
        base=CARD_DIR.as_uri() + "/",
        background=theme["background"],
        accent=theme["accent"],
        accent_soft=theme["accent_soft"],
        title=escape(title_for(theme, recap["period"])),
        period=escape(format_period(recap["period"], recap["projects"], alias)),
        stats=stats_html(recap),
        heatmap=heatmap_html(recap),
        tools=ranked_line("tools", recap["tools"]),
        # Project files only; older JSON without the field falls back to every file.
        languages=ranked_line("langs", recap.get("project_languages") or recap["languages"]),
        badges=badges_html(recap),
    )


def find_chrome():
    for name in ([os.environ["BONFIRE_CHROME"]] if os.environ.get("BONFIRE_CHROME") else []) + list(CHROME_NAMES):
        path = shutil.which(name)
        if path:
            return path
    sys.exit("Chrome/Chromium not found (set BONFIRE_CHROME).")


class DevTools:
    """Minimal Chrome DevTools protocol client over --remote-debugging-pipe (fd 3 and 4).

    Headless --screenshot clips the page (a 1920 window becomes a ~1833 viewport), so
    we set the viewport and the clip directly through the protocol.
    """

    def __init__(self, chrome, profile):
        to_chrome_r, self.to_chrome = os.pipe()
        self.from_chrome, from_chrome_w = os.pipe()
        self.proc = subprocess.Popen(
            [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--remote-debugging-pipe", f"--user-data-dir={profile}", "about:blank"],
            pass_fds=(3, 4),
            preexec_fn=lambda: self._map_pipes(to_chrome_r, from_chrome_w),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.close(to_chrome_r)
        os.close(from_chrome_w)
        self.buffer = b""
        self.next_id = 0

    @staticmethod
    def _map_pipes(read_end, write_end):
        # Chrome reads commands on fd 3 and replies on fd 4. Duplicating first avoids
        # clobbering a pipe that already sits on one of those numbers.
        read_end, write_end = os.dup(read_end), os.dup(write_end)
        os.dup2(read_end, 3)
        os.dup2(write_end, 4)

    def read_message(self):
        while b"\0" not in self.buffer:
            chunk = os.read(self.from_chrome, 65536)
            if not chunk:
                raise RuntimeError("Chrome closed the pipe")
            self.buffer += chunk
        raw, self.buffer = self.buffer.split(b"\0", 1)
        return json.loads(raw)

    def call(self, method, session=None, **params):
        self.next_id += 1
        message = {"id": self.next_id, "method": method, "params": params}
        if session:
            message["sessionId"] = session
        os.write(self.to_chrome, json.dumps(message).encode() + b"\0")
        while True:
            reply = self.read_message()
            if reply.get("id") == self.next_id:
                if "error" in reply:
                    raise RuntimeError(f"{method}: {reply['error']}")
                return reply["result"]

    def wait_event(self, method):
        while self.read_message().get("method") != method:
            pass

    def close(self):
        try:
            self.call("Browser.close")
        finally:
            self.proc.wait(timeout=10)


def render_png(html, out):
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "card.html"
        page.write_text(html, encoding="utf-8")
        chrome = DevTools(find_chrome(), Path(tmp) / "profile")
        try:
            target = chrome.call("Target.createTarget", url="about:blank")["targetId"]
            session = chrome.call("Target.attachToTarget", targetId=target, flatten=True)["sessionId"]
            chrome.call("Emulation.setDeviceMetricsOverride", session,
                        width=WIDTH, height=HEIGHT, deviceScaleFactor=1, mobile=False)
            chrome.call("Page.enable", session)
            chrome.call("Page.navigate", session, url=page.as_uri())
            chrome.wait_event("Page.loadEventFired")
            chrome.call("Runtime.evaluate", session, awaitPromise=True,
                        expression="document.fonts.ready.then(() => true)")
            shot = chrome.call("Page.captureScreenshot", session, format="png",
                               clip={"x": 0, "y": 0, "width": WIDTH, "height": HEIGHT, "scale": 1})
        finally:
            chrome.close()
    Path(out).write_bytes(base64.b64decode(shot["data"]))


def main(argv=None):
    themes = load_themes()
    parser = argparse.ArgumentParser(description="Render the PNG card from the recap JSON.")
    parser.add_argument("recap", type=Path, help="JSON produced by recap.py")
    parser.add_argument("--theme", choices=sorted(themes), default="bonfire")
    parser.add_argument("--out", type=Path, default=Path("card.png"))
    parser.add_argument("--alias", help="name to show instead of 'N projects' (optional)")
    parser.add_argument("--html", action="store_true", help="write the HTML instead of the PNG")
    args = parser.parse_args(argv)

    html = build_html(json.loads(args.recap.read_text(encoding="utf-8")), args.theme, themes, args.alias)
    if args.html:
        args.out.write_text(html, encoding="utf-8")
    else:
        render_png(html, args.out)
    print(args.out)


if __name__ == "__main__":
    main()
