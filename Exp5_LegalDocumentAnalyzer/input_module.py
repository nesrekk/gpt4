"""Input module - reads the legal document and the analysis options from the user."""
import os

from utils import BASE_DIR

DOCUMENT_TYPES = ["Auto-detect", "NDA", "Employment", "Service", "Lease", "Sale", "Other"]
ANALYSIS_TYPES = ["Summary", "Clause", "Obligation", "Complete"]


def choose(label, options):
    print(f"\n{label}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    choice = input("Enter choice : ").strip()
    return options[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= len(options) \
        else options[-1 if label.startswith("Analysis") else 0]


def read_document_request():
    """Legal document (file path or pasted text), document type, parties and analysis type."""
    print("Legal document: enter a file path (.txt / .pdf / .docx) or type PASTE to paste text")
    source = input("Document : ").strip()
    if source.upper() == "PASTE":
        print("Paste the legal text. Finish with a line containing only END.")
        lines = []
        while (line := input()) != "END":
            lines.append(line)
        document = {"path": None, "text": "\n".join(lines)}
    else:
        path = source if os.path.isabs(source) else os.path.join(BASE_DIR, source)
        document = {"path": path, "text": None}

    doc_type = choose("Document Type", DOCUMENT_TYPES)
    parties = input("\nParties (optional, comma separated - press Enter to detect) : ").strip()
    analysis = choose("Analysis Type", ANALYSIS_TYPES)
    return {**document, "doc_type": doc_type, "parties": parties, "analysis": analysis}
