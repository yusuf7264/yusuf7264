#!/usr/bin/env python3
"""Converts a photo into the ASCII portrait used by the profile README SVGs.

    python3 photo_to_ascii.py portrait.jpg
    python3 photo_to_ascii.py photo.jpg --rotate 90 --crop 0.25,0.1,0.75,0.9

Emits two blocks (dark-mode and light-mode). The SVG draws light text on a dark
background and vice versa, so the two use inverted ramps -- this is why the
upstream repo ships visually different art for each theme.

At 38x24 characters there is very little resolution to work with, so a tight
crop on the face reads far better than a full-frame shot.

--rotate is clockwise degrees, for photos EXIF alone does not set upright.
--crop is left,top,right,bottom as fractions of width/height, applied after
  rotation.

Sized for the layout in gen_svg.py: at most MAX_COLS wide, or the art collides
with the info panel at x=390.
"""
import argparse
import sys
from PIL import Image, ImageOps

MAX_COLS = 38          # (PANEL_X - 15) / CHAR_W, from gen_svg.py
MAX_ROWS = 24
CELL_ASPECT = 20 / 9.667   # SVG line height / character advance width

# Dense -> sparse. Characters chosen to stay inside the ASCII set the upstream
# art uses, so the SVG needs no extra escaping beyond & < >.
RAMP = "@%#*+=-:. "


def to_ascii(img, cols, rows, invert):
    img = img.convert("L")
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
    w, h = img.size
    cols = MAX_COLS
    rows = round(h / w * cols / CELL_ASPECT)
    if rows > MAX_ROWS:
        rows = MAX_ROWS
        cols = min(MAX_COLS, round(w / h * rows * CELL_ASPECT))
    return cols, rows


def prepare(path, rotate, crop):
    img = ImageOps.exif_transpose(Image.open(path))
    if rotate:
        img = img.rotate(-rotate, expand=True)   # PIL rotates counter-clockwise
    if crop:
        l, t, r, b = crop
        w, h = img.size
        img = img.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
    return img


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--rotate", type=int, default=0, choices=[0, 90, 180, 270],
                   help="clockwise degrees to rotate before cropping")
    p.add_argument("--crop", help="left,top,right,bottom as fractions, e.g. 0.25,0.1,0.75,0.9")
    a = p.parse_args()

    crop = None
    if a.crop:
        crop = [float(v) for v in a.crop.split(",")]
        if len(crop) != 4 or not all(0 <= v <= 1 for v in crop) \
                or crop[0] >= crop[2] or crop[1] >= crop[3]:
            sys.exit("--crop needs 4 fractions in 0..1 with left<right and top<bottom")

    img = prepare(a.image, a.rotate, crop)
    cols, rows = fit(img)
    print(f"# {a.image} -> {img.size[0]}x{img.size[1]}px -> {cols} cols x {rows} rows",
          file=sys.stderr)

    # A dense glyph reads as *bright* on a dark background and *dark* on a light
    # one, so dark mode takes the inverted ramp.
    for label, invert in (("DARK MODE (light text on dark bg)", True),
                          ("LIGHT MODE (dark text on light bg)", False)):
        print(f"\n===== {label} =====")
        for line in to_ascii(img, cols, rows, invert):
            print(line)


if __name__ == "__main__":
    main()
