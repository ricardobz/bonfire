#!/usr/bin/env python3
"""Turns a raw Codex image into the final card background: pixel grid + limited palette.

Codex never hits an exact grid, so we downscale to the "logical" resolution (one art
pixel per block), quantize the colors and upscale without smoothing.

Usage:
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
    parser.add_argument("--block", type=int, default=2, help="art pixel size, in px")
    parser.add_argument("--colors", type=int, default=128)
    args = parser.parse_args()
    pixelize(args.src, args.dst, block=args.block, colors=args.colors)


if __name__ == "__main__":
    main()
