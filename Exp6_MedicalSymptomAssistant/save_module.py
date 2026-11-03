"""Save module - stores the report as timestamped .txt and .json files in reports/."""
import json
import os
from datetime import datetime

from utils import REPORT_DIR


def save_report(report_lines, record):
    os.makedirs(REPORT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.join(REPORT_DIR, f"symptom_report_{stamp}")
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(f"AI MEDICAL SYMPTOM ASSISTANT - REPORT ({datetime.now():%d-%m-%Y %H:%M})\n")
        f.write("\n".join(report_lines) + "\n")
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    return base + ".txt", base + ".json"
