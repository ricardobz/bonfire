# Prompts de arte (Codex)

Fundos dos cards, gerados pelo **Codex CLI** local (`codex exec`, mesmo fluxo do
`floripa_game`). Cada imagem gasta cota: pedir o ok do Ricardo antes de cada leva.

> **Sessão Codex (estilo bonfire):** `01a137f3-90b7-7302-a6a6-85a9d4e98daa`
> (continuar com `codex exec resume <session-id>`, anexando com `-i` os fundos já
> aprovados para manter o estilo).

Status: ⬜ prompt pendente · 📝 prompt pronto · 🧪 gerado · ✅ aprovado · ❌ rejeitado

Brutos em `ref/`, processados em `assets/backgrounds/`; nunca editar o
processado à mão.

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

## bonfire: 🧪

Placeholder em SVG (desenhado pelo Claude) em `assets/backgrounds/bonfire.svg` até
chegar a versão do Codex. Abriu a sessão do estilo (sem anexos):
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
em `ref/bonfire_raw_full.png`.

## end-of-day (diário): 📝

```
[BASE, cozier and warmer]
Scene: a wooden farmhouse interior at night, a bed with a patchwork quilt,
moonlight through a small window, a shipping crate by the door, fireflies
outside. Bottom half: a large blank parchment-colored panel with a pixel
wooden frame, empty, ready for a daily summary.
```

## captains-log: 📝

```
[BASE] Scene: view from a starship bridge window toward a nebula in teal and
violet, a captain's chair silhouette in the foreground at the edge, faint
retro-futuristic console glow. Calm, contemplative, end-of-week log entry mood.
```

## bench: 📝

```
[BASE] Scene: a lone wrought-iron park bench inside a vast underground cavern,
soft blue bioluminescent glow, a small hanging lantern above the bench, pale
stalactites and distant ruined architecture fading into blue-black mist,
drifting light motes. Quiet, "rest here before going deeper".
Same visual series as the bonfire image in this conversation.
```

## Pendentes: ⬜

Fora da primeira leva (bonfire, end-of-day, captains-log, bench):
`site-of-grace`, `typewriter`, `mountain-campfire`, `save-star`,
`save-crystal`, `sculptors-idol`, `healing-center`, `mdr-terminal`,
`awards-night`, `dnd-table`, `fsociety-terminal`, `ticket-rail`.
