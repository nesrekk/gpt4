"""Part H - Intelligent intent detection using Ollama (Q10)."""
import re

from utils import ask_llm

INTENTS = ["BLOG_GENERATION", "TITLE_GENERATION", "SUMMARY", "KEYWORD_GENERATION",
           "META_DESCRIPTION", "SAVE_BLOG", "EXIT"]

PROMPT = """Classify the user's request for a blog generator app into exactly one intent:
BLOG_GENERATION - write / generate / create a blog or article
TITLE_GENERATION - suggest titles or headings for the blog
SUMMARY - summarize or shorten the blog
KEYWORD_GENERATION - SEO keywords, tags or key phrases
META_DESCRIPTION - meta description or search snippet
SAVE_BLOG - save, store or export the blog to a file
EXIT - quit, exit or close the app

Examples:
Write a blog on Cyber Security -> BLOG_GENERATION
Summarize this blog -> SUMMARY
Give SEO keywords -> KEYWORD_GENERATION
I need a meta description -> META_DESCRIPTION
Suggest some catchy titles -> TITLE_GENERATION
Save it to a file -> SAVE_BLOG

User request: {text}
Answer with the intent label only."""

FALLBACK = [("META_DESCRIPTION", "meta"), ("KEYWORD_GENERATION", "keyword"),
            ("SUMMARY", "summar"), ("TITLE_GENERATION", "title"), ("SAVE_BLOG", "save"),
            ("EXIT", "exit"), ("BLOG_GENERATION", "blog")]


def detect_intent(text):
    reply = ask_llm(PROMPT.format(text=text), system="You are an intent classifier.",
                    temperature=0).upper()
    for intent in INTENTS:
        if re.search(rf"\b{intent}\b", reply):
            return intent
    lowered = text.lower()
    return next((intent for intent, word in FALLBACK if word in lowered), "BLOG_GENERATION")


def extract_topic(text):
    """'Write a blog on Cyber Security' -> 'Cyber Security' (None if no topic given)."""
    match = re.search(r"\b(?:on|about|regarding)\s+(.+)$", text.strip(), re.I)
    return match.group(1).strip(" .?!") if match else None


if __name__ == "__main__":
    for i, text in enumerate(["Write a blog on Cyber Security", "Summarize this blog",
                              "Give SEO keywords"], 1):
        print(f"Example {i}")
        print("User")
        print(text)
        print("Detected Intent")
        print(detect_intent(text))
        print()
