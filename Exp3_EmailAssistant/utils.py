"""Shared helpers: Ollama calls and saving replies (Save module)."""
import logging
import os
import sys
from datetime import datetime

# Only show real errors from Hugging Face downloads (must be set before the import)
os.environ.setdefault("HF_HUB_VERBOSITY", "error")

import ollama

# Windows terminals may not use UTF-8, so print characters like ₹ and • safely there too
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

# Hide a harmless macOS-only torch log line printed while importing sentence-transformers
logging.getLogger("torch.distributed.elastic.multiprocessing.redirects").setLevel(logging.ERROR)

MODEL = "llama3.2"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "emails.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "outputs", "generated_reply.txt")

client = ollama.Client()


def ask_llm(prompt, system="You are a professional customer support email assistant.",
            temperature=0.4):
    response = client.chat(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        options={"temperature": temperature},
    )
    return response["message"]["content"].strip()


def clean_email(text):
    """Drop any chatty preamble ("Here is the email:") before the greeting line."""
    lines = text.strip().splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower().startswith(("dear", "hi ", "hi,", "hello")):
            return "\n".join(lines[i:]).strip()
    return text.strip()


def save_reply(email, reply, intent):
    """Part G (Q9): append customer email, generated reply, intent and date to the file."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Date           : {datetime.now():%d-%m-%Y %H:%M}\n")
        f.write(f"Customer Name  : {email['name']}\n")
        f.write(f"Subject        : {email['subject']}\n")
        f.write(f"Intent         : {intent}\n")
        f.write(f"Customer Email :\n{email['body']}\n\n")
        f.write(f"Generated Reply:\n{reply}\n\n")
    return OUTPUT_FILE
