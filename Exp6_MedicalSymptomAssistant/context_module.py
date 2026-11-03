"""Context module - evaluates duration, severity, history, medication and allergies."""
import re

UNIT_DAYS = {"hour": 1 / 24, "day": 1, "week": 7, "month": 30, "year": 365}
CHRONIC = ["asthma", "diabetes", "hypertension", "heart", "kidney", "copd", "cancer", "pregnan",
           "hiv", "liver", "immun"]


def duration_in_days(text):
    match = re.search(r"(\d+(?:\.\d+)?)\s*(hour|day|week|month|year)", text.lower())
    return float(match.group(1)) * UNIT_DAYS[match.group(2)] if match else None


def build_context(data, profile):
    severity = data["severity"].capitalize() if data["severity"].lower() in (
        "mild", "moderate", "severe") else "Not stated"
    days = duration_in_days(data["duration"])
    risk_factors = [c for c in CHRONIC if c in data["history"].lower()]
    if profile["age_group"] in ("Child", "Older adult"):
        risk_factors.append(f"age group: {profile['age_group'].lower()}")
    return {
        "duration": data["duration"] or "Not stated",
        "duration_days": days,
        "severity": severity,
        "history": data["history"],
        "medication": data["medication"],
        "allergies": data["allergies"],
        "additional": data["additional"],
        "risk_factors": risk_factors,
    }
