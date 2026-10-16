---
name: bonfire
description: Make a shareable "Strava for devs" card of the user's Claude Code usage (day, week, sprint, month or all time) with pixel-art save-point themes and achievements. Use when the user runs /bonfire or asks for their Claude Code recap, weekly/daily stats card, or usage summary to post.
argument-hint: "[day|week|sprint|month|all] [--theme THEME_ID] [--paths DIR ...] [--alias NAME]"
allowed-tools: Bash(uv run:*), Bash(uv --version), Read, AskUserQuestion
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
- The only exception is `--alias`: a name the user typed themselves is shown on the card
  instead of the project count. Never derive it from a path; if the user wants a name
  shown, ask them to type it.

## Steps

0. **Check uv.** Run `uv --version`. If it fails, stop and tell the user bonfire needs
   [uv](https://docs.astral.sh/uv/) (it provides a suitable Python), with the install
   command: `curl -LsSf https://astral.sh/uv/install.sh | sh`.

1. **Parse the arguments.** The period maps to `--days` and a default theme:

   | Period | `--days` | Default theme |
   |---|---|---|
   | `day` | `1` | `end-of-day` |
   | `week` (or nothing) | `7` | `bonfire` |
   | `sprint` | `15` | `mdr-terminal` |
   | `month` | `30` | `typewriter` |
   | `all` | `all` | `typewriter` |

   Keep `--theme`, `--paths` (real project directories) and `--alias` if given.

2. **Collect.** Run, with a timestamped output in the scratchpad (or `/tmp`):
   ```sh
   uv run "$ROOT/recap.py" --days N [--paths ...] --out <tmp>/recap.json
   ```
   Then read `<tmp>/recap.json`.

3. **Preview before rendering.** Show a compact summary so the user sees exactly what
   will be posted: period, projects (count), sessions, prompts, tokens out, cache
   hit, top 3 tools, top 3 languages, streak, unlocked achievements. Mention that the
   JSON has numbers only and offer to show it in full. If there were no sessions in
   the period, say so and stop.

4. **Pick the theme.** If `--theme` was not given, ask with AskUserQuestion (max 4
   options). Put the period's default (table above) first, marked "(Recommended)";
   fill the other 3 slots with different themes from
   `$ROOT/data/themes.json` (vary them between runs). In the question text, list
   every theme id so the user can type any other one via "Other".

5. **Render.**
   ```sh
   mkdir -p ~/Pictures/bonfire
   uv run "$ROOT/render.py" <tmp>/recap.json --theme THEME [--alias "NAME"] \
     --out ~/Pictures/bonfire/<YYYY-MM-DD>-<PERIOD>-<THEME>.png
   ```
   Open the PNG with Read and check it before reporting (text inside the card, nothing
   cut off at the bottom). If it looks wrong, say so instead of reporting success.

6. **Caption (optional).** Offer 2–3 short caption options for the post, written **only
   from the numbers in the JSON** and in the theme's voice (bonfire: weary knight
   resting; end-of-day: cozy farmer; captains-log: "Captain's log, stardate…";
   bench: quiet explorer; for other themes, the voice of the game or series they
   evoke, without naming the franchise). No hashtags spam, no project names. Reply in the user's
   language; the caption follows the language they ask for.

7. **Report**: the PNG path, the achievements unlocked, and the captions.
