"""Safety module - rule-based red-flag scan and triage (does not depend on the LLM)."""
import re

# (pattern, reason) - any match means the person should get emergency care now
RED_FLAGS = [
    (r"chest (pain|tightness|pressure)", "Chest pain or pressure"),
    (r"(difficulty|trouble|hard) (in )?breathing|short(ness)? of breath|can'?t breathe",
     "Difficulty breathing"),
    (r"faint|passed out|unconscious|loss of consciousness", "Fainting / loss of consciousness"),
    (r"confus|slurred speech|face droop|(one|one-sided|left|right) side weakness|numbness on one side",
     "Possible stroke signs (confusion, slurred speech, one-sided weakness)"),
    (r"seizure|fits|convulsion", "Seizure"),
    (r"stiff neck", "Stiff neck (with fever can mean meningitis)"),
    (r"(vomit|cough)(ing)? (up )?blood|blood in (vomit|stool)|black stool", "Bleeding"),
    (r"worst headache|sudden severe headache|thunderclap", "Sudden severe headache"),
    (r"suicid|kill myself|self[- ]harm", "Thoughts of self-harm"),
    (r"swelling of (the )?(face|lips|tongue|throat)|anaphyla", "Severe allergic reaction"),
]


def high_fever(text):
    match = re.search(r"(\d{2,3}(?:\.\d)?)\s*°?\s*(f|c)\b", text.lower())
    if not match:
        return False
    value, unit = float(match.group(1)), match.group(2)
    return value >= 103 if unit == "f" else value >= 39.5


def assess(data, profile, context):
    """Return {'level', 'advice', 'red_flags'} using fixed rules."""
    text = " ".join([data["symptoms"], data["additional"]]).lower()
    flags = [reason for pattern, reason in RED_FLAGS if re.search(pattern, text)]
    if flags:
        return {"level": "EMERGENCY", "red_flags": flags,
                "advice": "Seek emergency medical care immediately - call 108 or go to the "
                          "nearest hospital. Do not wait for the symptoms to pass."}

    reasons = []
    if context["severity"] == "Severe":
        reasons.append("severity is reported as severe")
    if high_fever(text):
        reasons.append("high fever")
    if context["duration_days"] and context["duration_days"] > 7:
        reasons.append("symptoms have lasted more than a week")
    if context["risk_factors"] and context["severity"] != "Mild":
        reasons.append("risk factors: " + ", ".join(context["risk_factors"]))
    if reasons:
        return {"level": "SEE A DOCTOR WITHIN 24 HOURS", "red_flags": reasons,
                "advice": "Book a consultation with a doctor within the next 24 hours."}
    return {"level": "ROUTINE / SELF-CARE", "red_flags": [],
            "advice": "No warning signs found. Rest, stay hydrated and monitor the symptoms; "
                      "see a doctor if they get worse or do not improve in 2-3 days."}
