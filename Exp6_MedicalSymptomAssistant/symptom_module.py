"""Symptom module - turns the free-text description into a list of distinct symptoms."""
from utils import ask_llm_json


def extract_symptoms(description):
    data = ask_llm_json(
        "List each distinct symptom mentioned in this description as a short medical term "
        "(e.g. 'Fever', 'Dry cough', 'Headache'). Do not add symptoms that are not mentioned.\n"
        f"Description: {description}\n"
        'Return JSON: {"symptoms": ["..."]}',
        temperature=0,
    )
    symptoms = [str(s).strip().capitalize() for s in data.get("symptoms", []) if str(s).strip()]
    # fall back to splitting the text if the model returned nothing
    return symptoms or [s.strip().capitalize() for s in description.replace(" and ", ",").split(",")
                        if s.strip()]
