"""Part I (Q11) - complete AI blog generator with continuous menu-driven interaction."""
from blog_module import generate_blog
from input_module import display_details, read_blog_details
from intent_module import detect_intent, extract_topic
from keyword_module import generate_keywords
from meta_module import generate_meta_description
from summary_module import generate_summary
from title_module import generate_titles
from utils import line, save_blog, word_count

MENU = """
==============================================
      AI BLOG CONTENT GENERATOR (Ollama)
==============================================
 1. Enter Blog Details
 2. Generate Blog
 3. Generate Blog Titles
 4. Generate SEO Keywords
 5. Generate Summary
 6. Generate Meta Description
 7. Save Blog to File
 8. Exit
----------------------------------------------
 Or simply type a request, e.g.
 "Write a blog on Cyber Security"
=============================================="""

OPTION_TO_INTENT = {"2": "BLOG_GENERATION", "3": "TITLE_GENERATION", "4": "KEYWORD_GENERATION",
                    "5": "SUMMARY", "6": "META_DESCRIPTION", "7": "SAVE_BLOG", "8": "EXIT"}


def main():
    details = None
    state = {"blog": "", "titles": "", "keywords": "", "summary": "", "meta": ""}

    while True:
        print(MENU)
        choice = input("Enter your choice : ").strip()
        if not choice:
            continue

        if choice == "1":
            details = read_blog_details()
            display_details(details)
            state = dict.fromkeys(state, "")
            continue

        if choice in OPTION_TO_INTENT:
            intent = OPTION_TO_INTENT[choice]
        else:
            intent = detect_intent(choice)
            print(f"\nDetected Intent\n{intent}")
            topic = extract_topic(choice) if intent == "BLOG_GENERATION" else None
            if topic:
                base = details or {"style": "Professional", "tone": "Formal", "words": 500}
                details = {**base, "topic": topic}
                state = dict.fromkeys(state, "")
                display_details(details)

        if intent == "EXIT":
            print("\nThank you for using the AI Blog Content Generator. Goodbye!")
            break
        if details is None:
            print("\nPlease enter the blog details first (option 1).")
            continue
        if intent != "BLOG_GENERATION" and not state["blog"]:
            print("\nNo blog yet - generating the blog first...")
            intent_queue = ["BLOG_GENERATION", intent]
        else:
            intent_queue = [intent]

        for current in intent_queue:
            if current == "BLOG_GENERATION":
                print("\nGenerating Blog...")
                line()
                state["blog"] = generate_blog(details)
                print(state["blog"])
                line()
                print(f"(Generated {word_count(state['blog'])} words)")
            elif current == "TITLE_GENERATION":
                state["titles"] = generate_titles(details["topic"], state["blog"])
                print("\nSuggested Titles")
                print(state["titles"])
            elif current == "KEYWORD_GENERATION":
                state["keywords"] = generate_keywords(details["topic"], state["blog"])
                print("\nSEO Keywords")
                print(state["keywords"])
            elif current == "SUMMARY":
                state["summary"] = generate_summary(state["blog"])
                print("\nSummary")
                print(state["summary"])
                print(f"({word_count(state['summary'])} words)")
            elif current == "META_DESCRIPTION":
                state["meta"] = generate_meta_description(details["topic"], state["blog"])
                print("\nMeta Description")
                print(state["meta"])
                print(f"({len(state['meta'])} characters)")
            elif current == "SAVE_BLOG":
                path = save_blog(details, **state)
                print("\nBlog Saved Successfully!")
                print("File : outputs/" + path.rsplit("/", 1)[-1])


if __name__ == "__main__":
    main()
