# Plan: bonfire

Ideas and plan from the design session (2026-10-13).

## The idea

- **Daily or weekly** analysis of Claude Code usage: every session on the machine,
  or only the folders the user points to.
- Produces a Strava-style summary for devs to share, with **achievements**.
- **Exposes nothing**: aggregated numbers only.
- Ready-made backgrounds to pick when posting, generated with Codex, referencing
  **video game save points** and **TV series**.

## Shape: thin skill + script

- A **Python script (stdlib only)** reads the logs and emits JSON with **aggregates
  only**. Claude never reads conversation content. This guarantees privacy, is cheap
  and gives deterministic results.
- An **HTML card template**: theme background with the numbers on top, exported to
  PNG via headless Chrome.
- A **`/bonfire` skill** (`/bonfire day`, `/bonfire week --theme bonfire`): runs the
  script, previews the data, asks for the theme, renders the PNG and optionally
  writes a punchline **based on the numbers**.
- For other devs: package as a Claude Code **plugin** (skill + script +
  backgrounds).
- Prior art: `ccusage` does tokens and cost in the terminal, but has no card and no
  achievements. That is the differentiator.

### Data source

`~/.claude/projects/<encoded-folder>/*.jsonl`: one file per session, with
timestamps, tool calls and token usage per message. The folder name is the project
path with `/` replaced by `-` (e.g. `-home-beckert-worktest-bonfire`). Filtering by
folder just means choosing which directories to read.

## Metrics (no content)

- Sessions; active time (only stretches without long pauses); day streak
- Tokens in/out; cache hit rate
- Tool calls by type (Edit, Write, Bash, Read…)
- Number of files touched (count only); languages by extension
- Models used; peak hour; longest session; subagents dispatched
- Weekly heatmap

**Privacy:** project names are **hidden by default** (they become "3 projects"), with
an optional alias. No prompt, path, file name or code ever leaves. The JSON preview
is shown before rendering.

## Achievements

| Achievement | Rule |
|---|---|
| Night Owl | session after 2am |
| Early Bird | session before 6am |
| Marathon | session over 4h |
| Speedrun | task closed in under 10 min |
| Streak 7 | 7 days in a row |
| Polyglot | 5 or more languages |
| Delegator | 10 or more subagents |
| Cache Lord | cache hit above 90% |
| Weekend Warrior | Saturday and Sunday |
| Read the Manual | more Read than Edit + Write |
| Work-Life Balance | only weekdays, 9am to 6pm |
| Midnight Oil | activity between midnight and 2am |
| Burst | 5+ sessions in one day |
| Unfinished Business | a session resumed on another day (12h+ wall time) |
| Surgeon | Edit at least 3× Write |
| Token Tycoon | 1M+ output tokens |

## Background themes

### Games: save points

| # | Theme | Reference | Suggested use |
|---|---|---|---|
| 1 | Bonfire | Dark Souls ("Bonfire Lit") | weekly, main theme |
| 2 | Site of Grace | Elden Ring (golden beam) | |
| 3 | Bench | Hollow Knight (bench in a blue cave) | |
| 4 | Typewriter | Resident Evil (safe room) | |
| 5 | End of day | Stardew Valley (end-of-day summary screen) | ⭐ daily |
| 6 | Mountain campfire | Celeste | |
| 7 | Save star | Undertale ("filled with determination") | |
| 8 | Save crystal | Final Fantasy | |
| 9 | Sculptor's idol | Sekiro | |
| 10 | Healing center / PC | Pokémon ("progress saved") | |

### Series

| # | Theme | Reference | Suggested use |
|---|---|---|---|
| 1 | Captain's Log | Star Trek ("Stardate…") | ⭐ weekly |
| 2 | MDR terminal | Severance (Lumon, "work-life balance") | |
| 3 | Awards night | The Office (Dundies = achievements) | |
| 4 | D&D table | Stranger Things (a nod to Pleceboia) | |
| 5 | fsociety terminal | Mr. Robot | |
| 6 | Ticket rail | The Bear ("Yes, chef") | |

⚠️ **Copyright:** *evoke* rather than copy. No logos, characters or franchise names
in the image. Theme names in the code are generic (`bonfire`, `bench`,
`typewriter`, `captains-log`…).

### Image formats

- 1080x1920 (9:16, phone/stories), base format (2026-10-13)
- 1080x1350 (portrait: Instagram/LinkedIn), optional
- 1200x675 (X/Twitter), optional

Every background needs **negative space** for the text (center and bottom).

## Steps (one commit each)

1. [x] **Collector**: `recap.py --days 1|7 --paths ...` emits the aggregated JSON,
   plus a test that no conversation text leaks.
2. [x] **Achievements**: rules in a data file, easy to extend.
3. [x] **Card**: HTML template with themes (background + palette + font) and PNG via
   headless Chrome. Verify with screenshots.
4. [x] **`/bonfire` skill**: the wrapper, with preview and theme choice.
5. [x] **Backgrounds**: prompts in [ART-PROMPTS.md](ART-PROMPTS.md); generated with
   Codex, Claude integrates.
6. [ ] *(Later)* Package as a plugin, write the README, maybe a static gallery on
   Netlify. Once live, add it to the portfolio (ricardobz.dev).
7. **Periods and project** (2026-10-14): besides day and week, `sprint` (15 days,
   default theme `mdr-terminal`), `month` (last 30 days, `typewriter`) and `all`
   (whatever is left in the logs, `typewriter`); above 7 days the heatmap sums by
   weekday. `--alias` shows a typed name instead of "N projects".
   - [x] A. Collector (`--days 15|30|all`, `period.kind`) + card (titles, heatmap, alias)
   - [x] B. Skill (`/bonfire sprint|month|all`, `--alias`) + README

## Decisions

- ~~Where to start~~: **weekly** first (2026-10-13).
- ~~First batch of themes~~: `bonfire`, `end-of-day`, `captains-log`, `bench`.
- ~~Personal use or plugin for other devs?~~ **Personal use** for now (2026-10-14).
- ~~Name~~: `bonfire` clashes with the `vieko/bonfire` plugin (cross-session memory)
  and `savepoint` is also taken (`KYWAxx/savepoint`). Pick a more distinctive name
  before publishing (checked 2026-10-14).
