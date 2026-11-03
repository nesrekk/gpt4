"""Part C - Blog title generator (Q5)."""
import re

from utils import ask_llm


def generate_titles(topic, blog="", count=5):
    """Q5: generate five attractive blog titles."""
    reply = ask_llm(
        f"Suggest {count} short, attractive blog titles for a blog on \"{topic}\".\n"
        + (f"Blog content (for context):\n{blog[:1500]}\n" if blog else "")
        + f"Return exactly {count} titles as a numbered list, one per line, with no extra text.",
        temperature=0.8,
    )
    titles = [re.sub(r"^\s*\d+[.)]\s*", "", t).strip().strip('"*') for t in reply.splitlines()]
    titles = [t for t in titles if t][:count]
    return "\n".join(f"{i}. {t}" for i, t in enumerate(titles, 1))


if __name__ == "__main__":
    topic = input("Blog Topic : ")
    print("\nSuggested Titles")
    print(generate_titles(topic))
