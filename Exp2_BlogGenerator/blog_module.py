"""Part B - AI blog generation (Q3, Q4)."""
from utils import ask_llm, line, word_count


def build_prompt(details):
    """Q3: construct the prompt from the user inputs."""
    return (
        f"Write a {details['words']}-word {details['style'].lower()} blog on "
        f"\"{details['topic']}\" in a {details['tone'].lower()} tone for general readers. "
        "Use simple English. Structure:\n"
        "Line 1: the blog title\n"
        "Then a heading line 'Introduction' followed by a paragraph,\n"
        "then 2-3 short sub-headings, each on its own line followed by a paragraph,\n"
        "then a heading line 'Conclusion' followed by a paragraph.\n"
        "Use plain text only (no markdown symbols such as # or **)."
    )


def generate_blog(details):
    """Q4: use Ollama (Llama 3.2) to generate the complete blog."""
    return ask_llm(build_prompt(details))


if __name__ == "__main__":
    from input_module import display_details, read_blog_details

    details = read_blog_details()
    display_details(details)
    print("\nPrompt :\n" + build_prompt(details))
    print("\nGenerating Blog...")
    line()
    blog = generate_blog(details)
    print(blog)
    line()
    print(f"(Generated {word_count(blog)} words)")
