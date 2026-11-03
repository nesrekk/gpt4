"""Shared helpers for the recommendation system.

The lab sheet says GPT-4; the lab is run fully offline with Ollama (Llama 3.2) as the
local stand-in, exactly as listed in the record's software requirements.
"""
import json
import os

import ollama

MODEL = "llama3.2"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "outputs", "recommendations.txt")

client = ollama.Client()


def ask_llm(prompt, system="You are a personalized recommendation assistant.", temperature=0.5):
    response = client.chat(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        options={"temperature": temperature},
    )
    return response["message"]["content"].strip()


def ask_llm_json(prompt, system="You are a personalized recommendation assistant.",
                 temperature=0.4):
    """Ask Ollama for a JSON answer (format='json') and parse it."""
    response = client.chat(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        format="json",
        options={"temperature": temperature},
    )
    return json.loads(response["message"]["content"])


def heading(title, width=44):
    print("\n" + title)
    print("-" * width)
