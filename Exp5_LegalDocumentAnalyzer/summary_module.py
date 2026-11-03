"""Summary module - runs the LLM analysis and presents it in a structured format."""
import textwrap

from utils import ask_llm_json, heading


def analyze(prompts):
    """Run every prompt group and merge the JSON answers into one result."""
    result = {}
    for group, prompt in prompts.items():
        print(f"  - {group.replace('_', ' ')}...")
        result.update(ask_llm_json(prompt))
    return result


def _wrap(text, first="   ", rest="   "):
    return textwrap.fill(str(text), 96, initial_indent=first, subsequent_indent=rest)


def _items(value):
    return value if isinstance(value, list) else ([value] if value else [])


def _text(item):
    """Plain text for an item the model returned as a string or a small dict."""
    return "; ".join(str(v) for v in item.values()) if isinstance(item, dict) else str(item)


def format_report(result, facts):
    """Return the structured analysis as a list of printable lines."""
    out = []

    def section(title):
        out.extend(["", title, "-" * 60])

    section("DOCUMENT DETAILS")
    out.append(f"Document Type : {result.get('document_type', 'Not stated')}")
    out.append(f"Length        : {facts['pages']} page(s), {facts['words']} words, "
               f"{facts['characters']} characters")
    for p in _items(result.get("parties")):
        out.append(f"Party         : {p.get('name')} ({p.get('role')})" if isinstance(p, dict)
                   else f"Party         : {p}")
    if result.get("summary"):
        section("SUMMARY")
        out.append(_wrap(result["summary"], "", ""))
    if "key_clauses" in result:
        section("KEY CLAUSES")
        for i, c in enumerate(_items(result["key_clauses"]), 1):
            title = str(c.get("clause") if isinstance(c, dict) else c)
            # the model usually keeps the document's own clause number ("4. OBLIGATIONS ...")
            out.append(title if title[:1].isdigit() else f"{i}. {title}")
            if isinstance(c, dict) and c.get("explanation"):
                out.append(_wrap(c["explanation"]))
    if "obligations" in result:
        section("OBLIGATIONS")
        for o in _items(result["obligations"]):
            out.append(_wrap(f"[{o.get('party')}] {o.get('obligation')}" if isinstance(o, dict)
                             else o, " • "))
    for key, title in (("payment_terms", "PAYMENT TERMS"), ("termination", "TERMINATION CONDITIONS")):
        if key in result:
            section(title)
            # one bullet per term, even when the model joined several with ";"
            terms = [t.strip() for item in _items(result[key]) for t in _text(item).split("; ")]
            terms = [t for t in terms if t] or ["None stated in the document"]
            out.extend(_wrap(t, " • ") for t in terms)
    if "important_dates" in result:
        section("IMPORTANT DATES")
        for d in _items(result["important_dates"]):
            out.append(_wrap(f"{d.get('date')} - {d.get('event')}" if isinstance(d, dict) else d, " • "))
    section("RULE-BASED CHECK (regex on the text)")
    out.append(f"Dates   : {', '.join(facts['dates']) or 'none'}")
    out.append(f"Amounts : {', '.join(facts['amounts']) or 'none'}")
    out.append(f"Periods : {', '.join(facts['periods']) or 'none'}")
    return out


def display_report(lines):
    heading("LEGAL DOCUMENT ANALYSIS (Ollama - Llama 3.2)")
    print("\n".join(lines).lstrip("\n"))
