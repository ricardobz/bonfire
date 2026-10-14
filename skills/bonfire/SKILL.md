---
name: bonfire
description: Make a shareable "Strava for devs" card of the user's Claude Code usage (day or week) with pixel-art save-point themes and achievements. Use when the user runs /bonfire or asks for their Claude Code recap, weekly/daily stats card, or usage summary to post.
argument-hint: "[day|week] [--theme THEME_ID] [--paths DIR ...]"
allowed-tools: Bash(python3:*), Read, AskUserQuestion
---

# /bonfire

Turns local Claude Code logs into a 1080x1920 PNG card with aggregated numbers only.

The scripts live in the repository root, two levels above this skill's directory:
`ROOT=<this skill's base directory>/../..`. Resolve it once and use absolute paths.

## Privacy rules (non-negotiable)

- **Never read the session logs** (`~/.claude/projects/**/*.jsonl`) or any conversation
  content. All data comes from `recap.py`, which emits aggregates only.
- Never put project names, paths, file names, prompts or code in the card, the caption
  or your replies. If the user asks for project names, explain they are hidden by design.

## Steps

1. **Parse the arguments.** `day` → `--days 1`; `week` or nothing → `--days 7`.
   Keep `--theme` and `--paths` if given (`--paths` takes real project directories).

2. **Collect.** Run, with a timestamped output in the scratchpad (or `/tmp`):
   ```sh
   python3 "$ROOT/recap.py" --days N [--paths ...] --out <tmp>/recap.json
   ```
   Then read `<tmp>/recap.json`.

3. **Preview before rendering.** Show a compact summary so the user sees exactly what
   will be posted: period, projects (count), sessions, active time, tokens out, cache
   hit, top 3 tools, top 3 languages, streak, unlocked achievements. Mention that the
   JSON has numbers only and offer to show it in full. If there were no sessions in
   the period, say so and stop.

4. **Pick the theme.** If `--theme` was not given, ask with AskUserQuestion (max 4
   options). Put the default first, marked "(Recommended)": `end-of-day` for a day,
   `bonfire` for a week; fill the other 3 slots with different themes from
   `$ROOT/data/themes.json` (vary them between runs). In the question text, list
   every theme id so the user can type any other one via "Other".

5. **Render.**
   ```sh
   mkdir -p ~/Pictures/bonfire
   python3 "$ROOT/render.py" <tmp>/recap.json --theme THEME \
     --out ~/Pictures/bonfire/<YYYY-MM-DD>-<day|week>-<THEME>.png
   ```
   Open the PNG with Read and check it before reporting (text inside the card, nothing
   cut off at the bottom). If it looks wrong, say so instead of reporting success.

6. **Caption (optional).** Offer 2–3 short caption options for the post, written **only
   from the numbers in the JSON** and in the theme's voice (bonfire: weary knight
   resting; end-of-day: cozy farmer; captains-log: "Captain's log, stardate…";
   bench: quiet explorer). No hashtags spam, no project names. Reply in the user's
   language; the caption follows the language they ask for.

7. **Report**: the PNG path, the achievements unlocked, and the captions.
