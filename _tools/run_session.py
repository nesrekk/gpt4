"""Run a program in a pseudo-terminal, type scripted answers, and save the full transcript.

Usage: run_session.py <workdir> <out.txt> <command> [<expect-regex> <answer>]...
The transcript includes the typed input exactly as a terminal would echo it.
"""
import os
import re
import sys

import pexpect

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07")


def main():
    workdir, out_path, command, *steps = sys.argv[1:]
    env = dict(os.environ, TERM="dumb", PYTHONUNBUFFERED="1",
               TOKENIZERS_PARALLELISM="false", TRANSFORMERS_VERBOSITY="error",
               HF_HUB_DISABLE_PROGRESS_BARS="1", PYTHONWARNINGS="ignore")
    child = pexpect.spawn("/bin/bash", ["-c", command], cwd=workdir, env=env,
                          encoding="utf-8", timeout=600, dimensions=(60, 140))
    chunks = []
    child.logfile_read = type("Log", (), {"write": lambda self, s: chunks.append(s),
                                          "flush": lambda self: None})()
    for pattern, answer in zip(steps[0::2], steps[1::2]):
        child.expect(pattern)
        child.sendline(answer)
    child.expect(pexpect.EOF)
    text = ANSI.sub("", "".join(chunks)).replace("\r\n", "\n").replace("\r", "")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
