"""Saving recommendations to outputs/recommendations.txt."""
import os
from datetime import datetime

from utils import OUTPUT_FILE


def save_recommendations(profile, items, explanations=None):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    explained = dict(explanations or [])
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"Personalized Recommendations for {profile['name']}\n")
        f.write(f"Generated on : {datetime.now():%d-%m-%Y %H:%M}\n")
        f.write(f"Interests    : {profile['interests']}\n")
        f.write(f"Skill Level  : {profile['skill_level']}\n")
        f.write(f"Goal         : {profile['goal']}\n")
        f.write("=" * 60 + "\n")
        for rank, item in enumerate(items, 1):
            f.write(f"{rank}. {item['name']}  (Score: {item['score']}%)\n")
            f.write(f"   Reason: {item['reason']}\n")
            if explained.get(item["name"]):
                f.write(f"   Why it suits you: {explained[item['name']]}\n")
            f.write("\n")
    return OUTPUT_FILE
