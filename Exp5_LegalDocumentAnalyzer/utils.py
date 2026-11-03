"""Shared helpers for the legal document analyzer.

The lab sheet says GPT-4; the lab runs offline with Ollama (Llama 3.2) as the local stand-in.
"""
import json
import os

import ollama

MODEL = "llama3.2"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

client = ollama.Client()


SYSTEM = "You are a careful legal analyst. Use only the given document."


def ask_llm_json(prompt, temperature=0.1):
    """Ask Ollama for a JSON answer (format='json') and parse it.

    In JSON mode a small model occasionally keeps generating whitespace forever, so the
    answer length is capped and a cut-off / invalid answer is retried at a higher temperature.
    """
    for attempt in range(3):
        response = client.chat(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
            format="json",
            options={"temperature": temperature, "num_ctx": 8192, "num_predict": 1500},
        )
        try:
            return json.loads(response["message"]["content"])
        except json.JSONDecodeError:
            temperature = min(temperature + 0.3, 1.0)
    raise RuntimeError("The model did not return valid JSON after 3 attempts.")


def heading(title, width=60):
    print("\n" + title)
    print("-" * width)
