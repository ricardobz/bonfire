# Prompts de arte (Codex)

Fundos dos cards, gerados pelo **Codex CLI** local (`codex exec`, mesmo fluxo do
`floripa_game`). Cada imagem gasta cota: pedir o ok do Ricardo antes de cada leva.

> **Sessão Codex (estilo bonfire):** `01a137f3-90b7-7302-a6a6-85a9d4e98daa`
> (continuar com `codex exec resume <session-id>`, anexando com `-i` os fundos já
> aprovados para manter o estilo).

Status: ⬜ prompt pendente · 📝 prompt pronto · 🧪 gerado · ✅ aprovado · ❌ rejeitado

Brutos em `ref/<tema>_raw_full.png`, processados em `assets/backgrounds/<tema>.png`
por `python3 tools/pixelize.py <bruto> <final>` (grade 2x2, 128 cores, 1080x1920);
nunca editar o processado à mão.

Estilo: **pixel art detalhada** (indie moderna, pixels 2x2, até 128 cores), não
16-bit chunky.

## Base comum (prefixo de todos)

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

Abriu a sessão do estilo (sem anexos):
`codex exec -s workspace-write "<base + cena>"`.

```
[BASE] Scene: a small bonfire with a rusted straight sword thrust into its coiled
ashes, embers drifting upward, a ruined stone archway in the dark behind it with
cracked, textured stones and hanging roots. Warm orange firelight casting soft
volumetric glow on the stones, fading into deep charcoal shadows. Melancholic,
restful, "a safe place after a long fight". A few drifting embers in the negative
space below.

Save the result as ref/bonfire_raw.png in the current directory.
```

**Saída (13/10/2026):** o Codex gerou 941x1672 e ele mesmo já reduziu para a grade
2x2 + 128 cores em `ref/bonfire_raw.png` (1080x1920). O original sem tratamento ficou
em `ref/bonfire_raw_full.png`; o fundo final sai dele via `tools/pixelize.py`.
Aprovado e integrado em `assets/backgrounds/bonfire.png`.

## end-of-day (diário): ✅

O painel de pergaminho do resumo fica para o card desenhar (passo 3), não para a
arte: o fundo mantém o mesmo espaço negativo escuro dos outros.

Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (13/10/2026):** `ref/end-of-day_raw_full.png`, 941x1672 sem tratamento (o gerador
ignora o 1080x1920 pedido). Aprovado e integrado em
`assets/backgrounds/end-of-day.png` via `tools/pixelize.py`.

## captains-log: ✅

Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (13/10/2026):** `ref/captains-log_raw_full.png`, 941x1672 sem tratamento (o gerador
ignora o 1080x1920 pedido). Aprovado e integrado em
`assets/backgrounds/captains-log.png` via `tools/pixelize.py`.

## bench: ✅

Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (13/10/2026):** `ref/bench_raw_full.png`, 941x1672 sem tratamento (o gerador
ignora o 1080x1920 pedido). Aprovado e integrado em
`assets/backgrounds/bench.png` via `tools/pixelize.py`.

## site-of-grace: ✅

Referência: Elden Ring: feixe dourado. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/site-of-grace_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/site-of-grace.png` via `tools/pixelize.py`.

## typewriter: ✅

Referência: Resident Evil: safe room. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/typewriter_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/typewriter.png` via `tools/pixelize.py`.

## mountain-campfire: ✅

Referência: Celeste: fogueira na montanha. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/mountain-campfire_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/mountain-campfire.png` via `tools/pixelize.py`.

## save-star: ✅

Referência: Undertale: estrela de save. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/save-star_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/save-star.png` via `tools/pixelize.py`.

## save-crystal: ✅

Referência: Final Fantasy: cristal de save. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/save-crystal_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/save-crystal.png` via `tools/pixelize.py`.

## sculptors-idol: ✅

Referência: Sekiro: ídolo do escultor. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/sculptors-idol_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/sculptors-idol.png` via `tools/pixelize.py`.

## healing-center: ✅

Referência: Pokémon: centro de cura / PC. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/healing-center_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/healing-center.png` via `tools/pixelize.py`.

## mdr-terminal: ✅

Referência: Severance: terminal MDR. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/mdr-terminal_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/mdr-terminal.png` via `tools/pixelize.py`.

## awards-night: ✅

Referência: The Office: Dundies. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/awards-night_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/awards-night.png` via `tools/pixelize.py`.

## dnd-table: ✅

Referência: Stranger Things: mesa de D&D. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/dnd-table_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/dnd-table.png` via `tools/pixelize.py`.

## fsociety-terminal: ✅

Referência: Mr. Robot: terminal. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/fsociety-terminal_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/fsociety-terminal.png` via `tools/pixelize.py`.

## ticket-rail: ✅

Referência: The Bear: trilho de comandas. Continuar a sessão do estilo, anexando o bonfire:
`codex exec resume 01a137f3-90b7-7302-a6a6-85a9d4e98daa -i assets/backgrounds/bonfire.png "<base + cena>"`.

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

**Saída (14/10/2026):** `ref/ticket-rail_raw_full.png`, 941x1672 sem tratamento. Aprovado e
integrado em `assets/backgrounds/ticket-rail.png` via `tools/pixelize.py`.
