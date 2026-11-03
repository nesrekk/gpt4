"""Part A - User input collection (Q1, Q2)."""


def read_blog_details():
    """Q1: read topic, writing style, tone and approximate word count."""
    topic = input("Enter Blog Topic :\n").strip()
    style = input("Writing Style :\n").strip() or "Professional"
    tone = input("Tone :\n").strip() or "Formal"
    words = input("Word Count :\n").strip()
    words = int(words) if words.isdigit() else 500
    return {"topic": topic, "style": style, "tone": tone, "words": words}


def display_details(details):
    """Q2: display the collected information neatly."""
    print("-" * 34)
    print(f"Blog Topic : {details['topic']}")
    print(f"Style      : {details['style']}")
    print(f"Tone       : {details['tone']}")
    print(f"Words      : {details['words']}")


if __name__ == "__main__":
    display_details(read_blog_details())
