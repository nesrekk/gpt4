"""Part E - Blog summary generator (Q7)."""
from utils import ask_llm


def generate_summary(blog, words=100):
    """Q7: generate a short summary of about 100 words."""
    return ask_llm(
        f"Summarize the following blog in about {words} words as a single paragraph. "
        "Return only the summary.\n\n" + blog,
        temperature=0.3,
    )


if __name__ == "__main__":
    text = input("Paste blog text : ")
    print("\nSummary")
    print(generate_summary(text))
