"""Part G - User feedback and refinement (Q8)."""
from prompt_module import build_prompt
from recommendation_module import generate_recommendations


def read_feedback():
    print("\nWhich recommendations are useful?")
    return input("Your feedback : ").strip()


def refine_recommendations(profile, analysis, items, feedback):
    """Q8: use the feedback to generate a refined recommendation list."""
    prompt = build_prompt(profile, analysis, feedback=feedback,
                          previous=[item["name"] for item in items])
    return generate_recommendations(prompt, profile["count"])
