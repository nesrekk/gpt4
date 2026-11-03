"""Extraction module - pulls raw text out of .txt, .pdf and .docx legal documents."""
import os

import pymupdf
from docx import Document


def extract_text(path):
    """Return (raw_text, page_count) for the given document."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Document not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        with pymupdf.open(path) as pdf:
            return "\n".join(page.get_text() for page in pdf), pdf.page_count
    if ext == ".docx":
        text = "\n".join(p.text for p in Document(path).paragraphs)
        return text, max(1, len(text) // 3000 + 1)
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return text, max(1, len(text) // 3000 + 1)  # ~3000 characters per printed page
