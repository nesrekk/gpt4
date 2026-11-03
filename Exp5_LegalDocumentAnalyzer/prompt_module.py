"""Prompt module - builds the structured analysis prompts for the requested analysis type.

A small local model gives far more complete answers when each part of the analysis is asked
separately, so every analysis type is a list of focused prompt groups.
"""

GROUPS = {
    "overview": (
        "Identify the document type, every party and a plain-English summary.",
        '"document_type": "e.g. Mutual Non-Disclosure Agreement",\n'
        '  "parties": [{"name": "full legal name", "role": "the role or short name the document gives this party"}],\n'
        '  "summary": "5-6 sentence plain-English summary of the whole document"',
    ),
    "clauses": (
        "List the 6-8 most important clauses of the document, in document order.",
        '"key_clauses": [{"clause": "clause number and title as written", '
        '"explanation": "one sentence on what it means in practice"}]',
    ),
    "obligations": (
        "List every obligation (what a party must or must not do). Include obligations of "
        "every party; name the party exactly as the document does.",
        '"obligations": [{"party": "...", "obligation": "one sentence"}]',
    ),
    "money_and_exit": (
        "List every fee, payment, penalty, damages or interest term with exact amounts, and "
        "every way the agreement can end (duration, notice periods, breach, survival).",
        '"payment_terms": ["one item per term; empty list if the document has none"],\n'
        '  "termination": ["one item per condition, as a plain sentence"]',
    ),
    "dates": (
        "List every date and every deadline or time period, with what happens on it.",
        '"important_dates": [{"date": "date or period exactly as written", "event": "what happens"}]',
    ),
}

ANALYSIS_GROUPS = {
    "Summary": ["overview"],
    "Clause": ["overview", "clauses", "money_and_exit"],
    "Obligation": ["overview", "obligations", "dates"],
    "Complete": list(GROUPS),
}


def build_prompts(request, text, facts):
    """Return {group: prompt} for the requested analysis type."""
    hints = []
    if request["doc_type"] != "Auto-detect":
        hints.append(f"The user says this is a {request['doc_type']} document.")
    if request["parties"]:
        hints.append(f"The user lists these parties: {request['parties']}.")
    context = (
        "Use ONLY information written in the legal document below; never invent names, dates "
        "or amounts, and quote amounts and periods exactly. " + " ".join(hints)
        + f"\nDates found in the text: {', '.join(facts['dates']) or 'none'}."
        + f"\nAmounts found in the text: {', '.join(facts['amounts']) or 'none'}.\n"
    )
    prompts = {}
    for group in ANALYSIS_GROUPS[request["analysis"]]:
        task, schema = GROUPS[group]
        prompts[group] = (f"{task}\n{context}\nReturn JSON with exactly these keys:\n{{\n  "
                          f"{schema}\n}}\n\nDOCUMENT:\n{text}")
    return prompts
