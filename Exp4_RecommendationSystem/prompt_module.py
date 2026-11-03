"""Part C - Prompt construction (Q4)."""


def build_prompt(profile, analysis, feedback=None, previous=None):
    """Q4: build the recommendation prompt from the profile, interests, level, goal and count."""
    prompt = (
        "You are a personalized recommendation assistant.\n\n"
        "User:\n"
        f"Name: {profile['name']}\n"
        f"Age: {profile['age']}\n"
        f"Background: {profile['background']}\n"
        f"Interests: {profile['interests']}\n"
        f"Skill Level: {profile['skill_level']}\n"
        f"Preferred Category: {profile['category']}\n"
        f"Goal: {profile['goal']}\n"
        f"Preference: {profile['preference']}\n"
        f"Constraints: {analysis['Constraints']}\n\n"
        f"Recommend {profile['count']} suitable {profile['category'] or 'learning resources'}.\n"
        "For each recommendation provide:\n"
        "1. Name\n2. Reason\n3. Suitability score"
    )
    if feedback:
        prompt += (
            "\n\nPrevious recommendations: " + ", ".join(previous or []) + "\n"
            f"User feedback: \"{feedback}\"\n"
            "Refine the list using this feedback: drop what the user does not want, keep "
            "what they liked, and add new items that match the feedback."
        )
    return prompt
