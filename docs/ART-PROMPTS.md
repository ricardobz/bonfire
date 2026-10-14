# Art prompts (Codex)

Card backgrounds, generated with the local **Codex CLI** (`codex exec`, same workflow
as `floripa_game`). Every image costs quota: get Ricardo's ok before each batch, and
run generations one at a time, never in parallel.

> **Codex session (bonfire style):** `01a137f3-90b7-7302-a6a6-85a9d4e98daa`
> (continue with `codex exec resume <session-id>`, attaching approved backgrounds
> with `-i` to keep the style).

Status: ⬜ prompt pending · 📝 prompt ready · 🧪 generated · ✅ approved · ❌ rejected

Raw files in `ref/<theme>_raw_full.png`, processed into
`assets/backgrounds/<theme>.png` by `python3 tools/pixelize.py <raw> <final>`
(2x2 grid, 128 colors, 1080x1920); never hand-edit the processed file.

Style: **detailed pixel art** (modern indie, 2x2 pixels, up to 128 colors), not
chunky 16-bit.

## Shared base (prefix of every prompt)

```
Highly detailed modern pixel art, like contemporary atmospheric indie games:
fine pixel detail, rich hand-placed shading, subtle dithering, dramatic lighting.
NOT retro 16-bit, NOT chunky: small pixels and a lot of detail.
Background art for a shareable stats card, 1080x1920 vertical (9:16 phone format).
The scene sits in the UPPER 45% of the image. The CENTER and LOWER 55% is calm,
low-detail negative space (dark gradient, faint dithered fog) so white text and
numbers can be laid over it legibly.

STYLE (mandatory): true pixel art, every pixel is a solid 2x2 px square, hard edges,
NO anti-aliasing, NO blur, NO painterly smoothing, at most 128 colors.
NO text, NO letters, NO logos, NO UI, NO frame, NO visible grid,
no characters' faces, no franchise symbols.
```

## bonfire: ✅

Opened the style session (no attachments):
`codex exec -s workspace-write "<base + scene>"`.

```
[BASE] Scene: a small bonfire with a rusted straight sword thrust into its coiled
ashes, embers drifting upward, a ruined stone archway in the dark behind it with
cracked, textured stones and hanging roots. Warm orange firelight casting soft
volumetric glow on the stones, fading into deep charcoal shadows. Melancholic,
restful, "a safe place after a long fight". A few drifting embers in the negative
space below.

Save the result as ref/bonfire_raw.png in the current directory.
```

**Output (2026-10-13):** Codex generated 941x1672 and reduced it to the 2x2 grid +
128 colors itself, in `ref/bonfire_raw.png` (1080x1920). The untouched original is
`ref/bonfire_raw_full.png`; the final background comes from it via
`tools/pixelize.py`. Approved and integrated as `assets/backgrounds/bonfire.png`.

## end-of-day (daily): ✅

The parchment summary panel is left for the card to draw (step 3), not the art: the
background keeps the same dark negative space as the others.

Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a cozy wooden farmhouse interior at night, a bed with a patchwork quilt,
a small window with moonlight and fireflies outside, a shipping crate by the door,
a lantern glowing warm amber on a shelf, potted plants and hanging herbs. Cozy and
content, "a good day's work, time to sleep". Warm amber lamplight against cool
blue moonlight. The negative space below is a dark, cozy dimness (shadowed
wooden floor fading to near-black), still calm and low-detail.

Save the generated image, unmodified, as ref/end-of-day_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-13):** `ref/end-of-day_raw_full.png`, untouched 941x1672 (the generator ignores the
requested 1080x1920). Approved and integrated as `assets/backgrounds/end-of-day.png` via `tools/pixelize.py`.

## captains-log: ✅

Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: view from a starship bridge through a wide panoramic window toward a
nebula in teal and violet with distant stars, the silhouette of a captain's chair
at the lower edge of the scene seen from behind, faint retro-futuristic console
lights glowing along the window frame. Calm, contemplative, end-of-week log entry
mood. The negative space below is deep space darkness fading to near-black.

Save the generated image, unmodified, as ref/captains-log_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-13):** `ref/captains-log_raw_full.png`, untouched 941x1672 (the generator ignores the
requested 1080x1920). Approved and integrated as `assets/backgrounds/captains-log.png` via `tools/pixelize.py`.

## bench: ✅

Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a lone wrought-iron park bench inside a vast underground cavern, soft blue
bioluminescent glow, a small hanging lantern above the bench, pale stalactites and
distant ruined architecture fading into blue-black mist, drifting light motes.
Quiet, "rest here before going deeper". The negative space below is blue-black
cavern mist fading to near-black.

Save the generated image, unmodified, as ref/bench_raw_full.png in the current
directory. Do not resize or post-process it.
```

**Output (2026-10-13):** `ref/bench_raw_full.png`, untouched 941x1672 (the generator ignores the
requested 1080x1920). Approved and integrated as `assets/backgrounds/bench.png` via `tools/pixelize.py`.

## site-of-grace: ✅

Reference: Elden Ring: golden beam. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: ancient overgrown ruins on a windswept plain at dusk, a single small point
of soft golden light hovering in the tall grass with a few thin golden threads
rising from it, golden motes drifting. Far on the horizon a colossal glowing tree
of golden light fills the sky. Gold and pale amber against muted grey-green and
dusky blue. Hopeful, "grace found, rest here". The negative space below is dark
grass fading into dusky fog and then near-black.

Save the generated image, unmodified, as ref/site-of-grace_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/site-of-grace_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/site-of-grace.png` via `tools/pixelize.py`.

## typewriter: ✅

Reference: Resident Evil: safe room. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a small quiet safe room in an old mansion: a wooden desk with a vintage
typewriter and a single ink ribbon beside it, a sturdy storage chest against the
wall, a dim green-shaded desk lamp, rain streaking a tall window, a potted plant.
Warm lamplight in a cold, dark house. Calm and safe, "the danger can wait".
No paper with writing. The negative space below is a dark wooden floor fading to
near-black.

Save the generated image, unmodified, as ref/typewriter_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/typewriter_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/typewriter.png` via `tools/pixelize.py`.

## mountain-campfire: ✅

Reference: Celeste: mountain campfire. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a small campfire on a snowy mountain ledge at night, a backpack and a
bedroll beside it, a starry violet sky with a faint aurora, distant jagged peaks,
an abandoned rusty chairlift cable crossing the background. Pink, violet and teal
palette with the warm fire. Quiet pride, "made it this far". The negative space
below is the dark mountainside and drifting snow fog fading to near-black.

Save the generated image, unmodified, as ref/mountain-campfire_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/mountain-campfire_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/mountain-campfire.png` via `tools/pixelize.py`.

## save-star: ✅

Reference: Undertale: save star. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a quiet corridor in ancient purple stone ruins, a single small glowing
yellow four-pointed star hovering in mid-air and twinkling, a patch of golden
flowers in a soft beam of light from a crack in the ceiling, a few fallen leaves.
Purple and gold palette. Gentle and determined, "filled with determination".
The negative space below is dark purple shadow fading to near-black.

Save the generated image, unmodified, as ref/save-star_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/save-star_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/save-star.png` via `tools/pixelize.py`.

## save-crystal: ✅

Reference: Final Fantasy: save crystal. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: an ancient underground chamber with carved stone pillars, a large
faceted blue crystal floating and slowly rotating above a circular stone pedestal,
casting soft blue light and sparkles on the walls, faint glowing runes-like
patterns on the floor ring (abstract shapes, not letters). Blue and silver palette.
Serene, "progress saved". The negative space below is dark stone floor and blue
mist fading to near-black.

Save the generated image, unmodified, as ref/save-crystal_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/save-crystal_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/save-crystal.png` via `tools/pixelize.py`.

## sculptors-idol: ✅

Reference: Sekiro: sculptor's idol. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a small weathered hand-carved wooden idol on a mossy stone in the ruins of
a mountain temple, a thin stream of incense smoke rising, red autumn maple leaves
falling, a broken wooden gate and misty pine-covered mountains behind. Red, ochre
and muted grey palette. Solemn and still, "rest, then rise again". The negative
space below is dark mossy ground and mist fading to near-black.

Save the generated image, unmodified, as ref/sculptors-idol_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/sculptors-idol_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/sculptors-idol.png` via `tools/pixelize.py`.

## healing-center: ✅

Reference: Pokémon: healing center / PC. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a cozy small-town healing clinic interior at night, a clean counter with a
round healing machine glowing soft pink, a retro beige desktop computer with a
glowing screen (no text) on a side desk, potted plants, a bench, warm ceiling
lights and a night street seen through the glass door. Pink, white and warm
cream palette. Comforting, "your team is fully healed". No logos, no ball-shaped
icons. The negative space below is a shiny dark floor fading to near-black.

Save the generated image, unmodified, as ref/healing-center_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/healing-center_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/healing-center.png` via `tools/pixelize.py`.

## mdr-terminal: ✅

Reference: Severance: MDR terminal. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a sterile, minimalist corporate office with a low ceiling and fluorescent
light panels, an empty green carpet, a single boxy retro-futuristic computer
terminal on a plain desk, its screen glowing with a field of soft floating cyan
dots (abstract, no numbers, no letters), a long empty white corridor behind.
Cold teal, white and muted green palette. Eerie calm, "work-life balance".
The negative space below is the dim green carpet fading to near-black.

Save the generated image, unmodified, as ref/mdr-terminal_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/mdr-terminal_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/mdr-terminal.png` via `tools/pixelize.py`.

## awards-night: ✅

Reference: The Office: Dundies. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: the back room of a modest family restaurant set up for a small office
awards night: a tiny stage with a microphone stand, a blank paper banner, a table
with cheap shiny gold trophies, string lights, balloons, empty chairs facing the
stage. Warm yellow and gold palette with a cozy, slightly cheesy charm.
Celebratory, "everyone gets a trophy". No text anywhere. The negative space below
is the dark floor and chairs fading to near-black.

Save the generated image, unmodified, as ref/awards-night_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/awards-night_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/awards-night.png` via `tools/pixelize.py`.

## dnd-table: ✅

Reference: Stranger Things: D&D table. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a 1980s suburban basement at night: a round table with a tabletop fantasy
game in progress, polyhedral dice, a hand-drawn dungeon map, a blank game master
screen, snacks and soda cans, walkie-talkies, colorful string lights on
wood-paneled walls, and a faint ominous red glow from a small window near the
ceiling. Warm string-light colors against a creeping red. Nostalgic adventure,
"one more session". No text. The negative space below is the dark carpet fading
to near-black.

Save the generated image, unmodified, as ref/dnd-table_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/dnd-table_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/dnd-table.png` via `tools/pixelize.py`.

## fsociety-terminal: ✅

Reference: Mr. Robot: terminal. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a dim small apartment at night: a cluttered desk with a CRT monitor
glowing with abstract green code-like patterns (no readable text), a keyboard, a
dark hoodie hanging on the chair, cold city lights through window blinds, cables
and an old laptop. Green monitor glow against deep blue-black. Quiet and focused,
"control is an illusion". No masks, no faces, no logos. The negative space below
is the dark floor fading to near-black.

Save the generated image, unmodified, as ref/fsociety-terminal_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/fsociety-terminal_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/fsociety-terminal.png` via `tools/pixelize.py`.

## ticket-rail: ✅

Reference: The Bear: ticket rail. Continue the style session, attaching bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + scene>"`.

```
[BASE] The attached image is a STYLE reference only: match its pixel size, level of
detail, shading and lighting approach. Do NOT copy its content or its orange palette.

Scene: a professional restaurant kitchen line after service: a stainless steel
ticket rail with blank paper tickets, copper and steel pans hanging, the pass with
heat lamps glowing warm orange, a folded blue kitchen towel, a knife on a cutting
board. Steel, warm orange and kitchen blue palette. Tired satisfaction,
"yes, chef". No text on the tickets. The negative space below is the dark steel
counter fading to near-black.

Save the generated image, unmodified, as ref/ticket-rail_raw_full.png in the
current directory. Do not resize or post-process it.
```

**Output (2026-10-14):** `ref/ticket-rail_raw_full.png`, untouched 941x1672. Approved and integrated as
`assets/backgrounds/ticket-rail.png` via `tools/pixelize.py`.
