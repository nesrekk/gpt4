"""Shared helpers: Ollama calls, formatting and file saving."""
import os
from datetime import datetime

import ollama

MODEL = "llama3.2"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "outputs", "generated_blog.txt")

client = ollama.Client()


def ask_llm(prompt, system="You are an expert blog writer and SEO specialist.", temperature=0.7):
    response = client.chat(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        options={"temperature": temperature},
    )
    return response["message"]["content"].strip()


def word_count(text):
    return len(text.split())


def line(char="-", width=40):
    print(char * width)


def save_blog(details, blog, titles="", keywords="", summary="", meta=""):
    """Save the generated blog and all generated extras to outputs/generated_blog.txt."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"Generated on : {datetime.now():%d-%m-%Y %H:%M}\n")
        f.write(f"Blog Topic   : {details['topic']}\n")
        f.write(f"Style        : {details['style']}\n")
        f.write(f"Tone         : {details['tone']}\n")
        f.write(f"Words        : {details['words']}\n")
        f.write("=" * 60 + "\n\n")
        f.write(blog + "\n\n")
        for heading, value in (("SUGGESTED TITLES", titles), ("SEO KEYWORDS", keywords),
                               ("SUMMARY", summary), ("META DESCRIPTION", meta)):
            if value:
                f.write("=" * 60 + f"\n{heading}\n" + "=" * 60 + f"\n{value}\n\n")
    return OUTPUT_FILE
