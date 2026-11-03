"""Profile display (Q2) and Part B user preference analysis (Q3)."""
from utils import ask_llm_json, heading

LABELS = [("name", "Name"), ("age", "Age"), ("background", "Background"),
          ("interests", "Interests"), ("skill_level", "Skill Level"),
          ("category", "Preferred Category"), ("preference", "Preference"),
          ("goal", "Goal"), ("count", "No. of Items")]


def display_profile(profile):
    """Q2: display the collected information neatly."""
    heading("USER PROFILE")
    for key, label in LABELS:
        print(f"{label:<19}: {profile[key]}")


def analyze_preferences(profile):
    """Q3: identify interests, skill level, goal, preferred type and constraints."""
    analysis = ask_llm_json(
        "Analyze this user profile. Return JSON with the keys primary_interest, "
        "secondary_interest and constraints (a short text string). Constraints must come "
        "only from the given details (for example skill level or learning style); never "
        "invent time or budget limits.\n\n"
        + "\n".join(f"{label}: {profile[key]}" for key, label in LABELS),
        temperature=0.1,
    )
    constraints = analysis.get("constraints") or "None"
    if isinstance(constraints, dict):
        constraints = list(constraints.values())
    if isinstance(constraints, list):
        constraints = ", ".join(map(str, constraints))
    # Skill level, goal and preference are taken directly from what the user typed
    return {
        "Primary Interest": analysis.get("primary_interest", ""),
        "Secondary Interest": analysis.get("secondary_interest", ""),
        "Skill Level": profile["skill_level"],
        "Goal": profile["goal"],
        "Preference": profile["preference"],
        "Constraints": constraints,
    }


def display_analysis(analysis):
    heading("Preference Analysis", 30)
    for key, value in analysis.items():
        print(f"{key:<19}: {value}")
