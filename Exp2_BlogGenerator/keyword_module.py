"""Part D - SEO keyword generator (Q6)."""
import re

from utils import ask_llm


def generate_keywords(topic, blog, count=8):
    """Q6: generate SEO-friendly keywords for the generated blog."""
    reply = ask_llm(
        f"Read this blog on \"{topic}\" and list {count} SEO-friendly keywords or short "
        "key phrases (1-3 words each) that people would search for. "
        "Return one keyword per line with no numbering, bullets or extra text.\n\n"
        f"Blog:\n{blog[:3000]}",
        temperature=0.3,
    )
    keywords = [re.sub(r"^[\s\-*•\d.)]+", "", k).strip().strip('"') for k in reply.splitlines()]
    return "\n".join(k for k in keywords if k)[:1000]


if __name__ == "__main__":
    topic = input("Blog Topic : ")
    print("\nSEO Keywords")
    print(generate_keywords(topic, topic))
