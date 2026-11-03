"""Save module - writes the structured analysis to outputs/<document>_analysis.txt."""
import os
from datetime import datetime

from utils import OUTPUT_DIR


def save_report(request, lines):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    name = os.path.splitext(os.path.basename(request["path"] or "pasted_document"))[0]
    path = os.path.join(OUTPUT_DIR, f"{name}_{request['analysis'].lower()}_analysis.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("AUTOMATED LEGAL DOCUMENT ANALYSIS\n")
        f.write(f"Generated on  : {datetime.now():%d-%m-%Y %H:%M}\n")
        f.write(f"Source        : {request['path'] or 'Pasted text'}\n")
        f.write(f"Analysis Type : {request['analysis']}\n")
        f.write("\n".join(lines) + "\n")
    return path
