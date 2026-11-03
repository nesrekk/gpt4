"""Make a demo video for one experiment: a code tour in an editor, then a replay of the real
recorded terminal run (the transcripts in screenshots/raw, in the order of spec.json).

Usage: make_video.py <number>...   (0-6; no number = all)
Writes Videos/ExN_Video_<name>.mp4 (1920x1080, 30 fps, no audio).
"""
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont
from pygments.lexers import PythonLexer
from pygments.token import Token

G = os.path.expanduser("~/Desktop/gpt4")
OUT_DIR = os.path.join(G, "Videos")
REG_NO = "URK23CS1081"
W, H, FPS = 1920, 1080, 30

EXPERIMENTS = {
    0: ("Exp0_Study_Installation_of_LLM", "Study Experiment - Installation of LLM (Ollama)",
        "Qwen 2.5 (0.5B) via Ollama", ["qwen_chat.py"]),
    1: ("Exp1_ECommerceGPT", "AI-Powered E-Commerce Chatbot",
        "Qwen 2.5 (1.5B) via Ollama + Sentence-Transformers", ["chatbot.py", "faq_module.py", "llm_utils.py"]),
    2: ("Exp2_BlogGenerator", "AI-Powered Blog Content Generator",
        "Llama 3.2 via Ollama", ["main.py", "blog_module.py", "utils.py"]),
    3: ("Exp3_EmailAssistant", "Intelligent Email Assistant",
        "Llama 3.2 via Ollama + Sentence-Transformers", ["main.py", "retrieval_module.py", "reply_module.py"]),
    4: ("Exp4_RecommendationSystem", "Personalized Recommendation System",
        "Llama 3.2 via Ollama", ["main.py", "recommendation_module.py", "prompt_module.py"]),
    5: ("Exp5_LegalDocumentAnalyzer", "Automated Legal Document Analyzer",
        "Llama 3.2 via Ollama", ["main.py", "extraction_module.py", "prompt_module.py"]),
    6: ("Exp6_MedicalSymptomAssistant", "AI-Powered Medical Symptom Assistant",
        "Llama 3.2 via Ollama", ["main.py", "safety_module.py", "prompt_module.py"]),
}

MENLO = "/System/Library/Fonts/Menlo.ttc"
MONO = ImageFont.truetype(MENLO, 21)
MONO_BOLD = ImageFont.truetype(MENLO, 21, index=1)
CODE = ImageFont.truetype(MENLO, 22)
UI = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
UI_SMALL = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 19)
TITLE_BIG = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 64, index=1)
TITLE_MID = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
# Menlo has no rupee sign, so that character is drawn with SF Mono
FALLBACK = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 21)

BG, SIDEBAR, BAR, TABBAR, BORDER = (30, 30, 30), (37, 37, 38), (50, 50, 52), (45, 45, 45), (60, 60, 60)
FG, DIM, PROMPT, ACCENT = (212, 212, 212), (133, 133, 133), (126, 211, 120), (0, 122, 204)
SYNTAX = {Token.Keyword: (197, 134, 192), Token.Name.Builtin: (220, 220, 170),
          Token.Name.Function: (220, 220, 170), Token.Name.Class: (78, 201, 176),
          Token.Literal.String: (206, 145, 120), Token.Literal.Number: (181, 206, 168),
          Token.Comment: (106, 153, 85), Token.Operator.Word: (197, 134, 192),
          Token.Name.Namespace: (78, 201, 176), Token.Name.Decorator: (220, 220, 170)}

TOP = 46                        # window title bar
CHAR_W = MONO.getlength("M")
LINE_H = 29
CODE_LINE_H = 32
SIDE_W = 330


def color_for(tok):
    while tok is not Token:
        if tok in SYNTAX:
            return SYNTAX[tok]
        tok = tok.parent
    return FG


class Video:
    def __init__(self, path):
        self.proc = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
        self.frames = 0

    def hold(self, img, seconds):
        data = img.tobytes()
        for _ in range(max(1, round(seconds * FPS))):
            self.proc.stdin.write(data)
            self.frames += 1

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


def window(title):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, TOP], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 26 + i * 28
        d.ellipse([cx - 8, TOP / 2 - 8, cx + 8, TOP / 2 + 8], fill=c)
    tw = d.textlength(title, font=UI)
    d.text(((W - tw) / 2, TOP / 2 - 12), title, font=UI, fill=(200, 200, 200))
    return img, d


# ---------------------------------------------------------------- title / end cards

def card(lines):
    img = Image.new("RGB", (W, H), (18, 24, 38))
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 12, W, H], fill=ACCENT)
    total = sum(f.size + 28 for _, f, _ in lines)
    y = (H - total) / 2
    for text, font, fill in lines:
        tw = d.textlength(text, font=font)
        d.text(((W - tw) / 2, y), text, font=font, fill=fill)
        y += font.size + 28
    return img


# ---------------------------------------------------------------- code tour

def code_frame(folder, files, current, code_lines, scroll):
    img, d = window(f"{current} - {folder}")
    d.rectangle([0, TOP, SIDE_W, H], fill=SIDEBAR)
    d.text((24, TOP + 18), "EXPLORER", font=UI_SMALL, fill=DIM)
    head = folder.upper()
    while d.textlength(head, font=UI_SMALL) > SIDE_W - 40:
        head = head[:-2] + "…"
    d.text((24, TOP + 56), head, font=UI_SMALL, fill=FG)
    y = TOP + 96
    for name in files:
        if name == current:
            d.rectangle([0, y - 4, SIDE_W, y + 28], fill=(55, 55, 61))
        d.text((44, y), name, font=UI_SMALL, fill=FG if name == current else (190, 190, 190))
        y += 34
    # tab bar
    d.rectangle([SIDE_W, TOP, W, TOP + 50], fill=TABBAR)
    tw = d.textlength(current, font=UI_SMALL) + 48
    d.rectangle([SIDE_W, TOP, SIDE_W + tw, TOP + 50], fill=BG)
    d.rectangle([SIDE_W, TOP, SIDE_W + tw, TOP + 3], fill=ACCENT)
    d.text((SIDE_W + 24, TOP + 14), current, font=UI_SMALL, fill=FG)
    # code
    top = TOP + 64
    rows = (H - top - 10) // CODE_LINE_H + 1
    first = int(scroll)
    offset = (scroll - first) * CODE_LINE_H
    cw = CODE.getlength("M")
    for i in range(first, min(first + rows + 1, len(code_lines))):
        y = top + (i - first) * CODE_LINE_H - offset
        num = str(i + 1)
        d.text((SIDE_W + 70 - CODE.getlength(num), y), num, font=CODE, fill=(110, 118, 129))
        x = SIDE_W + 100
        for tok, text in code_lines[i]:
            if x > W:
                break
            d.text((x, y), text, font=CODE, fill=color_for(tok))
            x += cw * len(text)
    d.rectangle([SIDE_W, TOP + 50, W, top - 6], fill=BG)
    return img


def tokenize(path):
    lines = [[]]
    for tok, text in PythonLexer().get_tokens(open(path, encoding="utf-8").read()):
        parts = text.expandtabs(4).split("\n")
        for j, part in enumerate(parts):
            if j:
                lines.append([])
            if part:
                lines[-1].append((tok, part))
    while lines and not lines[-1]:
        lines.pop()
    return lines


def code_tour(video, exp_dir, folder, tour):
    files = sorted(f for f in os.listdir(exp_dir) if f.endswith(".py")) + \
        sorted(f + "/" for f in os.listdir(exp_dir)
               if os.path.isdir(os.path.join(exp_dir, f)) and not f.startswith(("_", ".")) and f != "screenshots")
    rows = (H - TOP - 74) // CODE_LINE_H
    for name in tour:
        lines = tokenize(os.path.join(exp_dir, name))
        max_scroll = max(0, len(lines) - rows + 2)
        video.hold(code_frame(folder, files, name, lines, 0), 2.0)
        if max_scroll:
            steps = int(min(9.0, max(2.0, max_scroll / 9)) * FPS)
            for s in range(1, steps + 1):
                t = s / steps
                ease = t * t * (3 - 2 * t)
                video.hold(code_frame(folder, files, name, lines, ease * max_scroll), 1 / FPS)
            video.hold(code_frame(folder, files, name, lines, max_scroll), 1.2)


# ---------------------------------------------------------------- terminal replay

def input_patterns(exp_dir):
    """Regexes for every input() prompt in the experiment, to know which text was typed."""
    same_line, next_line = [], []
    src = "".join(open(os.path.join(exp_dir, f), encoding="utf-8").read()
                  for f in os.listdir(exp_dir) if f.endswith(".py"))
    for m in re.finditer(r'input\((f?)"((?:[^"\\]|\\.)*)"', src):
        prompt = m.group(2).encode().decode("unicode_escape")
        parts = prompt.split("\n")
        last, before = parts[-1], [p for p in parts[:-1] if p.strip()]

        def rx(text):
            pieces = re.split(r"\{[^}]*\}", text) if m.group(1) else [text]
            return ".*?".join(re.escape(p) for p in pieces)

        if last.strip():
            same_line.append(re.compile(r"^(" + rx(last.rstrip()) + r" ?)(.*)$"))
        elif before:
            next_line.append(re.compile(r"^\s*" + rx(before[-1].strip()) + r"\s*$"))
    return same_line, next_line


def program_order(parts):
    """Commands that the screenshots slot into the middle of a program run (like "ls outputs")
    are moved to after that run ends, so the replay looks like one terminal session."""
    parts = list(parts)
    i = 0
    while i < len(parts):
        cmd, raw = parts[i][0], parts[i][1]
        if cmd:
            open_runs = {p[1] for p in parts[:i]}
            later = [j for j in range(i + 1, len(parts)) if not parts[j][0] and parts[j][1] in open_runs
                     and parts[j][1] != raw]
            if later:
                parts.insert(later[-1] + 1, parts.pop(i))
                continue
        i += 1
    return parts


def script_lines(exp_dir):
    """[(kind, text)] where kind is 'cmd', 'out', ('prompt', typed) or 'typed'."""
    raw_dir = os.path.join(exp_dir, "screenshots", "raw")
    same_line, next_line = input_patterns(exp_dir)
    parts = [part for shot in json.load(open(os.path.join(raw_dir, "spec.json"))) for part in shot["parts"]]
    items, last = [], {}
    for part in program_order(parts):
        cmd, raw = part[0], part[1]
        lines = open(os.path.join(raw_dir, raw), encoding="utf-8").read().rstrip("\n").split("\n")
        start, end = (part[2] if len(part) > 2 else (1, len(lines)))
        if not cmd and raw in last:
            start = last[raw] + 1        # continue the same run without skipping lines
        last[raw] = end
        if cmd:
            if items:
                items.append(("out", ""))
            items.append(("cmd", cmd))
        typed_next, pasting = False, False
        for line in lines[start - 1:end]:
            line = line.expandtabs(4).rstrip()
            if pasting:
                items.append(("typed", line))
                pasting = line.strip() != "END"
                continue
            if typed_next:
                items.append(("typed", line))
                typed_next = False
                continue
            match = next((p.match(line) for p in same_line if p.match(line)), None)
            if match:
                items.append((("prompt", match.group(2)), match.group(1)))
            elif any(p.match(line) for p in next_line):
                items.append(("out", line))
                typed_next = True
            else:
                items.append(("out", line))
                pasting = line.startswith("Paste the legal text")
    return items


class Terminal:
    def __init__(self, folder):
        self.folder = folder
        self.cols = int((W - 60) // CHAR_W)
        self.rows = (H - TOP - 70) // LINE_H
        self.lines = []           # (color, text) per screen row

    def add(self, text, color=FG, bold=False):
        text = text or ""
        chunks = [text[i:i + self.cols] for i in range(0, len(text), self.cols)] or [""]
        for c in chunks:
            self.lines.append([(c, color, bold)])

    def frame(self):
        img, d = window(f"{self.folder} - Terminal")
        d.rectangle([0, TOP, W, TOP + 48], fill=TABBAR)
        d.text((30, TOP + 13), "TERMINAL", font=UI_SMALL, fill=FG)
        d.rectangle([30, TOP + 44, 30 + d.textlength("TERMINAL", font=UI_SMALL), TOP + 47], fill=ACCENT)
        d.text((170, TOP + 13), "zsh", font=UI_SMALL, fill=DIM)
        y = TOP + 62
        for row in self.lines[-self.rows:]:
            x = 30
            for text, color, bold in row:
                font = MONO_BOLD if bold else MONO
                for ch_run in re.split(r"(₹)", text):
                    if not ch_run:
                        continue
                    d.text((x, y), ch_run, font=FALLBACK if ch_run == "₹" else font, fill=color)
                    x += CHAR_W * len(ch_run)
            y += LINE_H
        return img


def replay(video, exp_dir, folder):
    term = Terminal(folder)
    prompt = f"{folder} $ "
    items = script_lines(exp_dir)
    for kind, text in items:
        if kind == "cmd":
            video.hold(term.frame(), 0.6)
            term.lines.append([(prompt, PROMPT, True), ("", FG, False)])
            type_into(video, term, text, FG)
            video.hold(term.frame(), 0.4)
        elif kind == "typed":
            term.lines.append([("", FG, False)])
            video.hold(term.frame(), 0.3)
            type_into(video, term, text, (255, 255, 255))
        elif isinstance(kind, tuple):
            term.add(text)
            video.hold(term.frame(), 0.5)
            type_into(video, term, kind[1], (255, 255, 255))
            video.hold(term.frame(), 0.25)
        else:
            term.add(text)
            video.hold(term.frame(), 2 / FPS)        # about 15 lines per second
            if text.strip().endswith("..."):
                video.hold(term.frame(), 1.5)       # the model is working
    term.lines.append([(prompt, PROMPT, True)])
    video.hold(term.frame(), 3.0)


def type_into(video, term, text, color):
    """Type text into the last screen row (wrapping), a few characters per frame."""
    per_frame = max(1, len(text) // 60)       # long inputs are typed faster (~2 s max)
    for i in range(0, len(text), per_frame):
        piece = text[i:i + per_frame]
        row = term.lines[-1]
        used = sum(len(t) for t, _, _ in row)
        if used + len(piece) > term.cols:
            term.lines.append([("", color, False)])
            row = term.lines[-1]
        if row[-1][1] == color and not row[-1][2]:
            row[-1] = (row[-1][0] + piece, color, False)
        else:
            row.append((piece, color, False))
        video.hold(term.frame(), 1 / FPS)


# ---------------------------------------------------------------- main

def make(n):
    folder, title, model, tour = EXPERIMENTS[n]
    exp_dir = os.path.join(G, folder)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"Ex{n}_Video_{folder.split('_', 1)[1]}.mp4")
    video = Video(out)
    label = "Study Experiment" if n == 0 else f"Ex. No. {n}"
    video.hold(card([(label, TITLE_MID, (150, 180, 230)),
                     (title.replace("Study Experiment - ", ""), TITLE_BIG, (255, 255, 255)),
                     ("24CS2506 - Building Applications with GPT-4", TITLE_MID, (200, 200, 200)),
                     (f"{REG_NO}   |   {model}", TITLE_MID, (170, 170, 170))]), 3.5)
    code_tour(video, exp_dir, folder, tour)
    video.hold(card([("Demo", TITLE_BIG, (255, 255, 255)),
                     ("Running the program", TITLE_MID, (200, 200, 200))]), 1.5)
    replay(video, exp_dir, folder)
    video.hold(card([(title.replace("Study Experiment - ", ""), TITLE_MID, (255, 255, 255)),
                     ("Thank you", TITLE_BIG, (255, 255, 255)),
                     (REG_NO, TITLE_MID, (170, 170, 170))]), 2.5)
    video.close()
    print(f"{out}: {video.frames / FPS:.1f} s")


if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(EXPERIMENTS):
        make(n)
