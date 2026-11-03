"""Part D - Recommendation generation (Q5)."""
from utils import ask_llm_json, heading

JSON_INSTRUCTIONS = (
    "\n\nReturn JSON only, in this form:\n"
    '{"recommendations": [{"name": "...", "reason": "one sentence", "score": 0-100}]}\n'
    "Every item must be of the requested category (for courses, name the platform, "
    "e.g. 'Machine Learning Specialization (Coursera)'). Scores are integers out of 100."
)


def generate_recommendations(prompt, count):
    """Q5: generate personalized recommendations (name, reason, suitability score)."""
    data = ask_llm_json(prompt + JSON_INSTRUCTIONS)
    items = data.get("recommendations", [])
    cleaned = []
    for item in items:
        try:
            score = int(str(item.get("score", 0)).rstrip("%"))
        except ValueError:
            score = 0
        if item.get("name"):
            cleaned.append({"name": item["name"].strip(), "reason": item.get("reason", "").strip(),
                            "score": max(0, min(score, 100))})
    return cleaned[:count]


def display_recommendations(items, title="PERSONALIZED RECOMMENDATIONS"):
    heading(title)
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['name']}")
        print(f"   Score: {item['score']}%")
        print("   Reason:")
        print(f"   {item['reason']}")
