"""Preprocessing module - cleans the extracted text and collects basic document facts."""
import re

MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|"
          "December")
DATE_PATTERN = re.compile(rf"\b\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}}\b|\b\d{{1,2}}[/-]\d{{1,2}}[/-]\d{{2,4}}\b")
AMOUNT_PATTERN = re.compile(r"(?:INR|Rs\.?|₹)\s?[\d,]+(?:\.\d+)?")
NUMBER_WORDS = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|"
                "thirty|forty|forty-five|sixty|ninety")
# "30 days", "48 hours", "thirty (30) days", "two (2) years"
PERIOD_PATTERN = re.compile(rf"(?:\b(?:{NUMBER_WORDS})\s+)?\(?\b\d+\)?\s*"
                            r"(?:hours?|days?|weeks?|months?|years?)\b", re.I)


def clean_text(raw):
    """Remove extra spaces, page numbers and line breaks that split sentences."""
    text = raw.replace("\r", "\n").replace("\t", " ")
    # page numbers: a line holding only a 1-3 digit number (keeps 6-digit PIN codes)
    text = re.sub(r"\n\s*(?:Page\s+)?\d{1,3}\s*(?:of\s+\d{1,3})?\s*(?=\n)", "", text)
    # join a line to the next one when the sentence clearly continues
    text = re.sub(r"(?<![.:;\n])\n(?=[a-z0-9(])", " ", text)
    text = re.sub(r"[ \u00a0]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return "\n".join(line.strip() for line in text.split("\n")).strip()


def document_facts(text, pages):
    """Rule-based facts used to cross-check the LLM output."""
    return {
        "pages": pages,
        "words": len(text.split()),
        "characters": len(text),
        "dates": list(dict.fromkeys(re.sub(r"\s+", " ", d) for d in DATE_PATTERN.findall(text))),
        "amounts": list(dict.fromkeys(a.strip() for a in AMOUNT_PATTERN.findall(text))),
        "periods": list(dict.fromkeys(p.lower() for p in PERIOD_PATTERN.findall(text))),
    }
