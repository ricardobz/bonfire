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

## end-of-day (diário): 📝

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

## captains-log: 📝

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

## bench: 📝

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

## Pendentes: ⬜

Fora da primeira leva (bonfire, end-of-day, captains-log, bench):
`site-of-grace`, `typewriter`, `mountain-campfire`, `save-star`,
`save-crystal`, `sculptors-idol`, `healing-center`, `mdr-terminal`,
`awards-night`, `dnd-table`, `fsociety-terminal`, `ticket-rail`.
