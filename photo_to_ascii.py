#!/usr/bin/env python3
"""Converts a photo into the ASCII portrait used by the profile README SVGs.

    python3 photo_to_ascii.py portrait.jpg

Emits two blocks (dark-mode and light-mode). The SVG draws light text on a dark
background and vice versa, so the two use inverted ramps -- this is why the
upstream repo ships visually different art for each theme.

Sized for the layout in gen_svg.py: at most MAX_COLS wide, or the art collides
with the info panel at x=390.
"""
import sys
from PIL import Image, ImageOps

MAX_COLS = 38          # (PANEL_X - 15) / CHAR_W, from gen_svg.py
MAX_ROWS = 24
CELL_ASPECT = 20 / 9.667   # SVG line height / character advance width

# Dense -> sparse. Characters chosen to stay inside the ASCII set the upstream
# art uses, so the SVG needs no extra escaping beyond & < >.
RAMP = "@%#*+=-:. "


def to_ascii(img, cols, rows, invert):
    img = ImageOps.exif_transpose(img).convert("L")
    img = ImageOps.autocontrast(img)
    img = img.resize((cols, rows), Image.LANCZOS)
    if invert:
        img = ImageOps.invert(img)

    px = img.load()
    lines = []
    for y in range(rows):
        line = "".join(RAMP[min(len(RAMP) - 1, px[x, y] * len(RAMP) // 256)]
                       for x in range(cols))
        lines.append(line.rstrip())
    return lines


def fit(img):
    w, h = ImageOps.exif_transpose(img).size
    cols = MAX_COLS
    rows = round(h / w * cols / CELL_ASPECT)
    if rows > MAX_ROWS:
        rows = MAX_ROWS
        cols = min(MAX_COLS, round(w / h * rows * CELL_ASPECT))
    return cols, rows


def main(path):
    img = Image.open(path)
    cols, rows = fit(img)
    print(f"# source {path}  ->  {cols} cols x {rows} rows", file=sys.stderr)

    # A dense glyph reads as *bright* on a dark background and *dark* on a light
    # one, so dark mode takes the inverted ramp.
    for label, invert in (("DARK MODE (light text on dark bg)", True),
                          ("LIGHT MODE (dark text on light bg)", False)):
        print(f"\n===== {label} =====")
        for line in to_ascii(img, cols, rows, invert):
            print(line)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
