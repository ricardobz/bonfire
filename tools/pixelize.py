#!/usr/bin/env python3
"""Processa o bruto do Codex no fundo final do card: grade de pixels + paleta limitada.

O Codex nunca acerta a grade exata, então reduzimos para a resolução "lógica"
(1 pixel de arte por bloco), quantizamos as cores e ampliamos sem suavizar.

Uso:
    python3 tools/pixelize.py ref/bonfire_raw_full.png assets/backgrounds/bonfire.png
"""

import argparse

from PIL import Image


def pixelize(src, dst, width=1080, height=1920, block=2, colors=128):
    small = Image.open(src).convert("RGB").resize(
        (width // block, height // block), Image.Resampling.BOX)
    small = small.quantize(colors=colors, method=Image.Quantize.MEDIANCUT,
                           dither=Image.Dither.NONE)
    small.resize((width, height), Image.Resampling.NEAREST).save(dst, optimize=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("src")
    parser.add_argument("dst")
    parser.add_argument("--block", type=int, default=2, help="lado do pixel de arte, em px")
    parser.add_argument("--colors", type=int, default=128)
    args = parser.parse_args()
    pixelize(args.src, args.dst, block=args.block, colors=args.colors)


if __name__ == "__main__":
    main()
