#!/usr/bin/env python3
"""Regenerates dark_mode.svg and light_mode.svg for the profile README.

Edit FIELDS / ASCII_ART below and run `python3 gen_svg.py` to rebuild both SVGs.
This resets the GitHub stat numbers to 0; the next `today.py` run (or the daily
Action) fills in the real values, so that is harmless.

Rows are padded so every line in the info panel is exactly ROW_WIDTH chars,
which is what makes the dot-leaders line up. Dynamic fields (the ones today.py
rewrites at build time) get an id + a matching *_dots id.
"""
import calendar
import datetime
import html

# Must match BIRTH_* in today.py. Used only for the placeholder Uptime value so
# the SVGs read correctly before the first Action run; today.py rewrites it after.
BIRTH = (2004, 10, 28)


def age_string(birth=BIRTH, today=None):
    """Same output as today.py's daily_readme(), without the dateutil dependency."""
    today = today or datetime.date.today()
    years = today.year - birth[0]
    months = today.month - birth[1]
    days = today.day - birth[2]
    if days < 0:
        months -= 1
        pm = today.month - 1 or 12
        py = today.year if today.month > 1 else today.year - 1
        days += calendar.monthrange(py, pm)[1]
    if months < 0:
        years -= 1
        months += 12
    plural = lambda n: "" if n == 1 else "s"
    return (f"{years} year{plural(years)}, {months} month{plural(months)}, "
            f"{days} day{plural(days)}")

ROW_WIDTH = 70          # widened from upstream's 60 to fit the Languages.Programming row
PANEL_X = 390
# Derived from upstream's proven geometry: a 60-col panel at x=390 in a 985px
# canvas leaves a 15px right margin, i.e. (985 - 390 - 15) / 60.
CHAR_W = 9.667
# Consolas is absent on macOS/Linux, so viewers fall back to a wider monospace.
# Extra right margin absorbs that: the panel still fits at ~10.0px/char.
RIGHT_MARGIN = 33
SVG_W = round(PANEL_X + ROW_WIDTH * CHAR_W + RIGHT_MARGIN)

# The art panel gets its own type size. Braille-block art needs line spacing close
# to the font size to read as solid rather than striped, and a smaller size keeps
# a 39-column block clear of the info panel.
ART_FONT_SIZE = 14
ART_LINE_H = 15
ART_TOP = 26
# Braille comes from a fallback font with a WIDER advance than the Latin
# monospace (0.604 em). Measured empirically: at size 15 a 39-column block
# overran x=390 and struck the info panel, so budget ~0.65 em here.
ART_CHAR_W = ART_FONT_SIZE * 0.65

# --- ASCII art panel -------------------------------------------------------
# Braille-block art (U+2800-U+28FF), one block for both themes. Note that
# Consolas has no Braille coverage, so these glyphs come from the viewer's
# fallback font; ART_FONT_SIZE/ART_LINE_H are tuned so that still lines up.
# Must stay <= ART_MAX_COLS wide or it will collide with the info panel at PANEL_X.
ASCII_ART = [
    '⠀⠀⠀⠀⠀⠀⠀⠀⡀⣠⣴⣶⣶⣿⣿⣷⣶⣶⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⢶⣾⣿⡿⠿⠉⠉⠉⠉⠹⠿⣿⣿⣿⣆⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⢠⣴⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠈⣙⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⣼⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠿⠙⣿⣿⡤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⢰⣿⡇⠀⣀⣀⠀⠀⠀⠀⣰⣦⣤⣠⣤⣤⣤⣄⡘⣿⣷⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⢸⣿⡇⠘⣿⣿⠇⠀⠀⣴⡿⢁⣉⣭⣥⣤⣼⣿⠇⢹⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⢺⣿⣧⠀⠀⠀⢀⣴⡿⢏⣴⣿⠟⢉⣩⣽⠟⠁⠀⠀⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠈⣿⣿⡆⠀⢀⣾⣏⣴⡿⣛⣥⣶⠿⠋⠁⠀⠀⠀⠀⢸⣿⣿⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠘⣿⣷⠀⣾⣿⣿⡿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⢸⣿⣶⣄⡙⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⢸⣿⡍⠛⠿⢿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⢀⣾⣿⠀⠀⠀⠀⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣮⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⣾⣿⣿⠀⠀⠀⠀⠈⢿⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣇⠄⠀⠀⠀⠀⠀⠀⠀',
    '⢐⣿⣿⣿⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀',
    '⢸⣿⠀⣿⣷⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⠀⠀⠀⠀⠀⠀⠀',
    '⢸⣿⠀⠈⠙⢿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡀⠀⠀⠀⠀⠀⠀',
    '⢸⣿⡄⠀⠀⠀⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣷⠀⠀⠀⠀⠀⠀',
    '⠹⣿⣧⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡗⡀⠀⠀⠀⠀',
    '⠀⢻⣿⣆⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡧⡇⠀⠀⠀⠀',
    '⠀⢸⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣇⠃⠀⠀⠀⠀',
    '⠀⠘⣿⣧⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡟⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠙⢿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠋⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠘⠹⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣧⣶⣧⣄⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠈⠈⠻⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣾⣿⣿⡿⡟⣿⣿⣶⣀⠀⠀⡀',
    '⠀⠀⠀⠀⠀⠀⠈⠈⢟⢿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣿⣟⣟⡻⢏⣳⣽⣷⢎⡽⢻⣿⣷⣿⡷',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⠿⣿⣮⡷⣋⢾⡻⣝⣮⣼⣿⣿⡿⠏⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣯⣿⣿⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠉⠻⠿⡿⠾⠿⠿⠿⠟⠋⠁⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⣿⣇⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣄⣀⣀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠁⠋⠟⠛⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠇',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⠿⠿⠿⠿⠿⠿⠻⠛⠋⠁⠀⠀',
]


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
    ("row", (["OS"], "macOS, Windows 11", None)),
    ("row", (["Uptime"], age_string(), "age_data")),
    ("row", (["Kernel"], "Software Engineer", None)),
    ("row", (["Status"], "Open to internships", None)),
    ("row", (["Education"], "UIC - B.S. Computer Science", None)),
    ("row", (["IDE"], "VS Code, Cursor, Claude Code", None)),
    ("blank", None),
    ("row", (["Languages", "Programming"], "Python, JavaScript, TypeScript, C/C++, SQL", None)),
    ("row", (["Languages", "Computer"], "HTML5, CSS3, JSON", None)),
    ("row", (["Languages", "Real"], "English, Somali", None)),
    ("blank", None),
    ("row", (["Frameworks"], "React, Next.js, FastAPI, Flask, Node.js", None)),
    ("row", (["Tools"], "Git, GitHub Actions, Vercel, MySQL, MongoDB", None)),
    ("row", (["Projects"], "AskClip, Pytest AI Generator", None)),
    ("header", "Contact"),
    ("row", (["Email", "Personal"], "yusufha.2004@gmail.com", None)),
    ("row", (["LinkedIn"], "linkedin.com/in/yusuf-ha", None)),
    ("row", (["GitHub"], "github.com/yusuf7264", None)),
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
    ay = ART_TOP
    for line in ASCII_ART:
        art.append(f'<tspan x="15" y="{ay}">{html.escape(line)}</tspan>')
        ay += ART_LINE_H
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
<text x="15" y="{ART_TOP}" fill="{theme["fg"]}" class="ascii" font-size="{ART_FONT_SIZE}px">
{chr(10).join(art)}
</text>
<text x="{PANEL_X}" y="30" fill="{theme["fg"]}">
{chr(10).join(lines)}
</text>
</svg>
'''


ART_MAX_COLS = int((PANEL_X - 15) / ART_CHAR_W)   # columns before the art hits the info panel

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
    rows = len(ASCII_ART)
    print(f"\nASCII art: {rows} rows, max width {widest} chars")
    print(f"Info panel: {len(FIELDS)} rows")
