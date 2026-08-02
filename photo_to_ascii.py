#!/usr/bin/env python3
"""Converts a photo into the ASCII portrait used by the profile README SVGs.

    python3 photo_to_ascii.py portrait.jpg --crop 0.14,0,0.80,0.78

At 32x24 characters there is very little resolution to work with, so this leans
on a tight crop, aggressive contrast, and a short glyph ramp. A loose crop of an
evenly-lit subject reads as static.

The output is a single block used for BOTH themes. Dense glyphs land on the
subject, which reads as dark ink on the light theme and as a bright drawing on
the dark theme. Rendering a tonally-faithful negative for the dark theme instead
only works when the photo's background is darker than the subject -- otherwise
the background lights up and the subject becomes a hole. Pass --invert for such
a photo (dark background, bright subject).

--rotate is clockwise degrees, for photos EXIF alone does not set upright.
--crop is left,top,right,bottom as fractions of width/height, applied after
  rotation.

Sized for the layout in gen_svg.py: at most MAX_COLS wide, or the art collides
with the info panel at x=390.
"""
import argparse
import sys
from PIL import Image, ImageFilter, ImageOps

MAX_COLS = 38          # (PANEL_X - 15) / CHAR_W, from gen_svg.py
MAX_ROWS = 24
CELL_ASPECT = 20 / 9.667   # SVG line height / character advance width

# Dense -> sparse. Short by design: at this size, ten near-identical mid-tones
# blur into noise, while five well-separated levels keep features legible.
RAMP = "@#+-. "


def prepare(path, rotate, crop):
    img = ImageOps.exif_transpose(Image.open(path))
    if rotate:
        img = img.rotate(-rotate, expand=True)   # PIL rotates counter-clockwise
    if crop:
        l, t, r, b = crop
        w, h = img.size
        img = img.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
    return img


def fit(img):
    w, h = img.size
    cols = MAX_COLS
    rows = round(h / w * cols / CELL_ASPECT)
    if rows > MAX_ROWS:
        rows = MAX_ROWS
        cols = min(MAX_COLS, round(w / h * rows * CELL_ASPECT))
    return cols, rows


def to_ascii(img, cols, rows, invert=False, cutoff=8, sharpen=220, ramp=RAMP):
    img = img.convert("L")
    if sharpen:
        # Sharpen before downsampling, or the detail is already gone.
        img = img.filter(ImageFilter.UnsharpMask(radius=max(2, img.width // 60),
                                                 percent=sharpen, threshold=2))
    img = img.resize((cols, rows), Image.LANCZOS)
    # cutoff clips the extreme percentiles so the mid-tones use the full ramp.
    img = ImageOps.autocontrast(img, cutoff=cutoff)
    if invert:
        img = ImageOps.invert(img)

    px = img.load()
    lines = []
    for y in range(rows):
        line = "".join(ramp[min(len(ramp) - 1, px[x, y] * len(ramp) // 256)]
                       for x in range(cols))
        lines.append(line.rstrip())
    return lines


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--rotate", type=int, default=0, choices=[0, 90, 180, 270],
                   help="clockwise degrees to rotate before cropping")
    p.add_argument("--crop", help="left,top,right,bottom as fractions, e.g. 0.14,0,0.80,0.78")
    p.add_argument("--invert", action="store_true",
                   help="for photos whose background is darker than the subject")
    p.add_argument("--cutoff", type=int, default=8, help="autocontrast percentile clip")
    p.add_argument("--sharpen", type=int, default=220, help="unsharp mask percent, 0 to disable")
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

    for line in to_ascii(img, cols, rows, a.invert, a.cutoff, a.sharpen):
        print(line)


if __name__ == "__main__":
    main()
