"""Analysis module - asks the LLM for possible conditions, self-care and warning signs."""
from prompt_module import build_analysis_prompt
from utils import ask_llm_json

LIKELIHOOD_ORDER = {"high": 0, "medium": 1, "low": 2}


def split_items(value):
    """One short item per entry, even if the model packed several sentences into one string."""
    items = value if isinstance(value, list) else [value]
    out = []
    for item in items:
        out.extend(part.strip().rstrip(".") + "." for part in str(item).split(". ") if part.strip())
    return out


def analyze_symptoms(profile, symptoms, context):
    data = ask_llm_json(build_analysis_prompt(profile, symptoms, context))
    conditions = [c for c in data.get("possible_conditions", []) if isinstance(c, dict)]
    conditions.sort(key=lambda c: LIKELIHOOD_ORDER.get(str(c.get("likelihood", "")).lower(), 3))
    return {
        "possible_conditions": conditions,
        "self_care": split_items(data.get("self_care", [])),
        "see_doctor_if": split_items(data.get("see_doctor_if", [])),
        "recommended_specialist": data.get("recommended_specialist", "General Physician"),
    }
