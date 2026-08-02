#!/usr/bin/env python3
"""Regenerates dark_mode.svg and light_mode.svg for the profile README.

Edit FIELDS / ASCII_ART below and run `python3 gen_svg.py` to rebuild both SVGs.
This resets the GitHub stat numbers to 0; the next `today.py` run (or the daily
Action) fills in the real values, so that is harmless.

Rows are padded so every line in the info panel is exactly ROW_WIDTH chars,
which is what makes the dot-leaders line up. Dynamic fields (the ones today.py
rewrites at build time) get an id + a matching *_dots id.
"""
import html

ROW_WIDTH = 70          # widened from upstream's 60 to fit the Languages.Programming row
PANEL_X = 390
# Derived from upstream's proven geometry: a 60-col panel at x=390 in a 985px
# canvas leaves a 15px right margin, i.e. (985 - 390 - 15) / 60.
CHAR_W = 9.667
# Consolas is absent on macOS/Linux, so viewers fall back to a wider monospace.
# Extra right margin absorbs that: the panel still fits at ~10.0px/char.
RIGHT_MARGIN = 33
SVG_W = round(PANEL_X + ROW_WIDTH * CHAR_W + RIGHT_MARGIN)

# --- ASCII art panel -------------------------------------------------------
# Placeholder monogram. Swap for a photo-derived portrait if desired.
# Must stay <= ART_MAX_COLS wide or it will collide with the info panel at PANEL_X.
ASCII_ART = r"""
   __   __                 __
   \ \ / /   _ ___ _   _  / _|
    \ V / | | / __| | | || |_
     | || |_| \__ \ |_| ||  _|
     |_| \__,_|___/\__,_||_|

    _   _
   | | | | __ _ ___ ___  __ _ _ __
   | |_| |/ _` / __/ __|/ _` | '_ \
   |  _  | (_| \__ \__ \ (_| | | | |
   |_| |_|\__,_|___/___/\__,_|_| |_|

   +------------------------------+
   |                              |
   |  $ whoami                    |
   |  > lead software engineer    |
   |  > rise / utdrise.com        |
   |                              |
   |  $ status                    |
   |  > open to internships       |
   |                              |
   +------------------------------+
""".strip("\n").split("\n")


def row(key_parts, value, width=ROW_WIDTH, value_id=None):
    """Builds one dot-leader row, padded to `width` chars.

    key_parts: list of key segments rendered in the key color, joined by '.'
    """
    key_plain = ".".join(key_parts)
    prefix_len = 2 + len(key_plain) + 1          # '. ' + key + ':'
    dots_len = width - prefix_len - len(value)
    if dots_len < 3:
        raise ValueError(f"row too long ({prefix_len + len(value)}): {key_plain}={value}")
    dots = " " + ("." * (dots_len - 2)) + " "

    key_html = ".".join(f'<tspan class="key">{html.escape(k)}</tspan>' for k in key_parts)
    dots_attr = f' id="{value_id}_dots"' if value_id else ""
    val_attr = f' id="{value_id}"' if value_id else ""
    return (f'<tspan class="cc">. </tspan>{key_html}:'
            f'<tspan class="cc"{dots_attr}>{dots}</tspan>'
            f'<tspan class="value"{val_attr}>{html.escape(value)}</tspan>')


def header(title, width=ROW_WIDTH):
    """Section header, e.g. '- Contact -———————...'"""
    text = f"- {title} " if title else ""
    return html.escape(text) + "-" + "—" * (width - len(text) - 4) + "-—-"


# --- content ---------------------------------------------------------------
FIELDS = [
    ("raw", '<tspan class="value">yusuf@hassan</tspan> '
            + "-" + "—" * (ROW_WIDTH - len("yusuf@hassan ") - 4) + "-—-"),
    ("row", (["OS"], "macOS, Ubuntu, Windows 11", None)),
    ("row", (["Uptime"], "21 years, 0 months, 0 days", "age_data")),
    ("row", (["Host"], "Rise (utdrise.com)", None)),
    ("row", (["Kernel"], "Lead Software Engineer", None)),
    ("row", (["Status"], "Open to internships", None)),
    ("row", (["IDE"], "VS Code, Cursor, Claude Code", None)),
    ("blank", None),
    ("row", (["Languages", "Programming"], "Python, JavaScript, TypeScript, C/C++, SQL", None)),
    ("row", (["Languages", "Computer"], "HTML5, CSS3, JSON", None)),
    ("row", (["Languages", "Real"], "English, Arabic", None)),
    ("blank", None),
    ("row", (["Projects"], "Rise", None)),
    ("header", "Contact"),
    ("row", (["Email", "Personal"], "yusufha.2004@gmail.com", None)),
    ("row", (["LinkedIn"], "yusuf-ha", None)),
    ("row", (["GitHub"], "yusuf7264", None)),
    ("header", "GitHub Stats"),
    ("stats1", None),
    ("stats2", None),
    ("stats3", None),
]

STATS = {
    "stats1": ('<tspan class="cc">. </tspan><tspan class="key">Repos</tspan>:'
               '<tspan class="cc" id="repo_data_dots"> .... </tspan><tspan class="value" id="repo_data">0</tspan>'
               ' {<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">0</tspan>}'
               ' | <tspan class="key">Stars</tspan>:'
               '<tspan class="cc" id="star_data_dots"> ........... </tspan><tspan class="value" id="star_data">0</tspan>'),
    "stats2": ('<tspan class="cc">. </tspan><tspan class="key">Commits</tspan>:'
               '<tspan class="cc" id="commit_data_dots"> .................. </tspan><tspan class="value" id="commit_data">0</tspan>'
               ' | <tspan class="key">Followers</tspan>:'
               '<tspan class="cc" id="follower_data_dots"> ....... </tspan><tspan class="value" id="follower_data">0</tspan>'),
    "stats3": ('<tspan class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:'
               '<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">0</tspan>'
               ' ( <tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>,'
               ' <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">0</tspan>'
               '<tspan class="delColor">--</tspan> )'),
}

THEMES = {
    "dark_mode.svg": dict(bg="#161b22", fg="#c9d1d9", key="#ffa657", value="#a5d6ff",
                          add="#3fb950", dele="#f85149", cc="#616e7f"),
    "light_mode.svg": dict(bg="#f6f8fa", fg="#24292f", key="#953800", value="#0a3069",
                           add="#1a7f37", dele="#cf222e", cc="#c2cfde"),
}


def build(theme):
    lines = []
    y = 30
    for kind, payload in FIELDS:
        if kind == "blank":
            lines.append(f'<tspan x="{PANEL_X}" y="{y}" class="cc">. </tspan>')
        elif kind == "raw":
            lines.append(f'<tspan x="{PANEL_X}" y="{y}">{payload}</tspan>')
        elif kind == "header":
            lines.append(f'<tspan x="{PANEL_X}" y="{y}">{header(payload)}</tspan>')
        elif kind in ("stats1", "stats2", "stats3"):
            lines.append(f'<tspan x="{PANEL_X}" y="{y}">{STATS[kind]}</tspan>')
        else:
            keys, value, vid = payload
            lines.append(f'<tspan x="{PANEL_X}" y="{y}">{row(keys, value, value_id=vid)}</tspan>')
        y += 20
    panel_bottom = y

    art = []
    ay = 30
    for line in ASCII_ART:
        art.append(f'<tspan x="15" y="{ay}">{html.escape(line)}</tspan>')
        ay += 20
    art_bottom = ay

    height = max(panel_bottom, art_bottom) + 10
    return f'''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{SVG_W}px" height="{height}px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {theme["key"]};}}
.value {{fill: {theme["value"]};}}
.addColor {{fill: {theme["add"]};}}
.delColor {{fill: {theme["dele"]};}}
.cc {{fill: {theme["cc"]};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{SVG_W}px" height="{height}px" fill="{theme["bg"]}" rx="15"/>
<text x="15" y="30" fill="{theme["fg"]}" class="ascii">
{chr(10).join(art)}
</text>
<text x="{PANEL_X}" y="30" fill="{theme["fg"]}">
{chr(10).join(lines)}
</text>
</svg>
'''


ART_MAX_COLS = int((PANEL_X - 15) / CHAR_W)   # columns before the art hits the info panel

if __name__ == "__main__":
    import sys, os
    widest = max(len(l.rstrip()) for l in ASCII_ART)
    if widest > ART_MAX_COLS:
        raise SystemExit(f"ASCII art is {widest} cols; max is {ART_MAX_COLS} before it "
                         f"overlaps the info panel at x={PANEL_X}")
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    for name, theme in THEMES.items():
        path = os.path.join(out_dir, name)
        with open(path, "w") as f:
            f.write(build(theme))
        print("wrote", path)
    print(f"\nASCII art: {len(ASCII_ART)} rows, max width {max(len(l) for l in ASCII_ART)} chars")
    print(f"Info panel: {len(FIELDS)} rows")
