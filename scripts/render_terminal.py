#!/usr/bin/env python3
"""Render the real CLI output as a terminal-style PNG for the README.

Input lines come from a text file (one per line); output is docs/screenshots/quickstart.png.
"""
import sys

from PIL import Image, ImageDraw, ImageFont

LINES_FILE, OUT = sys.argv[1], sys.argv[2]
BG = (30, 30, 46)
FG = (166, 227, 161)
DIM = (137, 140, 156)
GREEN = (166, 227, 161)
BLUE = (137, 180, 250)
TITLE = (49, 50, 68)

lines = [l.rstrip("\n") for l in open(LINES_FILE, encoding="utf-8")]
font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 26)
title_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 24)

pad, lh, header = 36, 40, 56
maxw = max((font.getlength(l) for l in lines), default=600) + pad * 2
W, H = int(min(max(maxw, 900), 1400)), header + lh * len(lines) + pad
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
for i, c in enumerate([(243, 139, 168), (250, 179, 135), (166, 227, 161)]):
    d.ellipse([pad + i * 34 - 8, 20, pad + i * 34 + 8, 36], fill=c)
d.text((pad + 110, 16), "$ zsh — erp-spec-forge", fill=DIM, font=title_font)
d.line([(0, header - 1), (W, header - 1)], fill=TITLE)
y = header + 6
for l in lines:
    color = FG
    if l.startswith("$ "):
        color = BLUE
    elif l.startswith(("OK ", "generated", "26 passed")):
        color = GREEN
    d.text((pad, y), l, fill=color, font=font)
    y += lh
img.save(OUT)
print("saved", OUT, img.size)
