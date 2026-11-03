"""Build screenshot PNGs for one experiment from its recorded transcripts.

Usage: shots.py <exp-dir> <venv-prompt-name> <spec.json>
spec.json: [{"out": "01_x.png", "title": "...", "parts": [["cmd", "raw.txt", [start, end]?], ...]}]
Each part is shown as "$ <cmd>" followed by that transcript (optionally a 1-based line range).
"""
import json
import os
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))


def main():
    exp_dir, folder, spec_path = sys.argv[1:]
    shots_dir = os.path.join(exp_dir, "screenshots")
    for shot in json.load(open(spec_path)):
        text = []
        for part in shot["parts"]:
            cmd, raw = part[0], part[1]
            lines = open(os.path.join(shots_dir, "raw", raw), encoding="utf-8").read().rstrip("\n").split("\n")
            if len(part) > 2:
                start, end = part[2]
                lines = lines[start - 1:end]
            if cmd:
                text.append(f"$ {cmd}")
            text.extend(lines)
            text.append("")
        tmp = os.path.join(shots_dir, "raw", "_render.txt")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("\n".join(text))
        subprocess.run([sys.executable, os.path.join(TOOLS, "render_terminal.py"), tmp,
                        os.path.join(shots_dir, shot["out"]), shot.get("title", f"Terminal — {folder}")],
                       check=True)
        os.remove(tmp)


if __name__ == "__main__":
    main()
