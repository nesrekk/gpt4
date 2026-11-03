"""Part I (Q10) - complete personalized recommendation system with continuous interaction."""
from explanation_module import display_explanations, explain_recommendations
from feedback_module import read_feedback, refine_recommendations
from input_module import read_profile
from intent_module import detect_intent
from profile_module import analyze_preferences, display_analysis, display_profile
from prompt_module import build_prompt
from ranking_module import display_ranking, rank_recommendations
from recommendation_module import display_recommendations, generate_recommendations
from save_module import save_recommendations

HOME = """
==================================================
   PERSONALIZED RECOMMENDATION SYSTEM (Ollama)
==================================================
 Ask in your own words, for example:
  - Recommend some AI courses.
  - I prefer AI and don't want Web Development.
  - Why did you recommend these?
  - Show my profile
  - Save the recommendations
  - Exit
=================================================="""


def generate(profile, analysis):
    prompt = build_prompt(profile, analysis)
    print("\nGenerated Prompt")
    print("-" * 44)
    print(prompt)
    print("\nGenerating recommendations...")
    items = rank_recommendations(generate_recommendations(prompt, profile["count"]))
    display_recommendations(items)
    print("\nRecommendation Ranking")
    display_ranking(items)
    return items


def main():
    print(HOME)
    profile = read_profile()
    display_profile(profile)
    analysis = analyze_preferences(profile)
    display_analysis(analysis)

    items, explanations = [], None
    while True:
        request = input("\nWhat would you like to do? : ").strip()
        if not request:
            continue
        intent = detect_intent(request)
        print(f"Detected Intent : {intent}")

        if intent == "EXIT":
            print("\nThank you for using the Personalized Recommendation System. Goodbye!")
            break
        if intent == "SHOW_PROFILE":
            display_profile(profile)
            display_analysis(analysis)
        elif intent == "GENERATE_RECOMMENDATION" or not items:
            items, explanations = generate(profile, analysis), None
        elif intent == "EXPLAIN_RECOMMENDATION":
            explanations = explain_recommendations(profile, items)
            display_explanations(explanations)
        elif intent == "REFINE_RECOMMENDATION":
            # The request itself is the feedback; ask for more only if it is very short
            feedback = request if len(request.split()) > 3 else read_feedback()
            print("\nRefining recommendations using your feedback...")
            items = rank_recommendations(refine_recommendations(profile, analysis, items, feedback))
            explanations = None
            display_recommendations(items, "REFINED RECOMMENDATIONS")
            print("\nRecommendation Ranking")
            display_ranking(items)
        elif intent == "SAVE_RECOMMENDATION":
            path = save_recommendations(profile, items, explanations)
            print("\nRecommendations saved successfully to outputs/" + path.rsplit("/", 1)[-1])


if __name__ == "__main__":
    main()
