"""Render a captured terminal transcript as a macOS-Terminal-style PNG.

Usage: render_terminal.py <transcript.txt> <out.png> "<window title>"
Lines starting with "$ " are drawn as the shell prompt/command.
"""
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
FONT_BOLD = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22, index=1)
TITLE_FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
# Menlo has no rupee sign, so those characters are drawn with SF Mono
FALLBACK = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 22)
FALLBACK_CHARS = set("₹")
BG, FG, PROMPT, BAR = (30, 30, 30), (230, 230, 230), (126, 211, 120), (56, 56, 56)
LINE_H, PAD, BAR_H = 30, 24, 44


def split_fallback(text):
    """Split text into runs so fallback-font characters are drawn separately."""
    runs, current = [], ""
    for ch in text:
        if ch in FALLBACK_CHARS:
            if current:
                runs.append(current)
            runs.append(ch)
            current = ""
        else:
            current += ch
    return runs + [current] if current else runs or [""]


def main():
    src, out, title = sys.argv[1:4]
    raw = open(src, encoding="utf-8").read().rstrip("\n").split("\n")
    raw = [line.expandtabs(4).rstrip() for line in raw]
    cols = max(100, min(132, max(len(line) for line in raw)))
    lines = []
    for line in raw:
        kind = "prompt" if line.startswith("$ ") else "text"
        wrapped = textwrap.wrap(line, cols, drop_whitespace=False, replace_whitespace=False) or [""]
        lines.extend((kind, w) for w in wrapped)

    char_w = FONT.getlength("M")
    width = int(PAD * 2 + char_w * cols)
    height = BAR_H + PAD * 2 + LINE_H * len(lines)
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width, BAR_H], fill=BAR)
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 22 + i * 26
        d.ellipse([cx - 8, BAR_H / 2 - 8, cx + 8, BAR_H / 2 + 8], fill=color)
    tw = d.textlength(title, font=TITLE_FONT)
    d.text(((width - tw) / 2, BAR_H / 2 - 12), title, font=TITLE_FONT, fill=(200, 200, 200))

    y = BAR_H + PAD
    for kind, text in lines:
        font = FONT_BOLD if kind == "prompt" else FONT
        fill = PROMPT if kind == "prompt" else FG
        x = PAD
        for segment in split_fallback(text):
            seg_font = FALLBACK if segment[:1] in FALLBACK_CHARS else font
            d.text((x, y), segment, font=seg_font, fill=fill)
            x += char_w * len(segment)
        y += LINE_H
    img.save(out)
    print(f"{out}: {width}x{height}, {len(lines)} lines")


if __name__ == "__main__":
    main()
