"""Part F - SEO meta description generator (Q8)."""
from utils import ask_llm

MAX_CHARS = 160


def generate_meta_description(topic, blog):
    """Q8: SEO meta description within 160 characters (retries, then trims at a word)."""
    meta = ""
    for _ in range(3):
        meta = ask_llm(
            f"Write one SEO meta description for a blog on \"{topic}\". It must be under "
            f"{MAX_CHARS} characters, include the main keyword and invite the reader to "
            "click. Return only the sentence, without quotes.\n\n"
            f"Blog:\n{blog[:2000]}",
            temperature=0.5,
        ).strip().strip('"')
        if len(meta) <= MAX_CHARS:
            return meta
    return meta[:MAX_CHARS].rsplit(" ", 1)[0].rstrip(",;:") + "."


if __name__ == "__main__":
    topic = input("Blog Topic : ")
    meta = generate_meta_description(topic, topic)
    print("\nMeta Description")
    print(meta)
    print(f"({len(meta)} characters)")
