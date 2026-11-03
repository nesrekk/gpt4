"""Part F - Recommendation explanation (Q7)."""
from utils import ask_llm_json, heading


def explain_recommendations(profile, items):
    """Q7: explain why every recommendation suits this user."""
    names = [item["name"] for item in items]
    data = ask_llm_json(
        f"User: {profile['name']}, {profile['age']} years, {profile['background']}. "
        f"Interests: {profile['interests']}. Skill level: {profile['skill_level']}. "
        f"Goal: {profile['goal']}. Preference: {profile['preference']}.\n\n"
        f"Category: {profile['category']}.\n\n"
        "For each recommendation below, write a 2-sentence explanation of why it suits this "
        "user, referring to their interests, skill level, goal or preference. Refer to the "
        "user by name instead of using pronouns.\n"
        + "\n".join(f"- {n}" for n in names)
        + '\n\nReturn JSON: {"explanations": [{"name": "...", "explanation": "..."}]}',
        temperature=0.4,
    )
    found = {e.get("name", "").strip().lower(): e.get("explanation", "")
             for e in data.get("explanations", [])}
    return [(n, found.get(n.lower()) or next(
        (v for k, v in found.items() if k and (k in n.lower() or n.lower() in k)), ""))
        for n in names]


def display_explanations(explanations):
    heading("RECOMMENDATION EXPLANATION")
    for i, (name, text) in enumerate(explanations, 1):
        print(f"{i}. {name}")
        print(f"   {text}")
