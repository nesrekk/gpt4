"""Main module - Automated Legal Document Analyzer with continuous interaction until Exit."""
import os

from extraction_module import extract_text
from input_module import read_document_request
from preprocessing_module import clean_text, document_facts
from prompt_module import build_prompts
from save_module import save_report
from summary_module import analyze, display_report, format_report

BANNER = """
==========================================================
     AUTOMATED LEGAL DOCUMENT ANALYZER (Ollama)
==========================================================
 Summarizes contracts and extracts parties, key clauses,
 obligations, payment terms, termination and dates.
 Sample documents: data/nda_agreement.txt
                   data/service_agreement.pdf
=========================================================="""


def run_once():
    request = read_document_request()
    if request["path"]:
        raw, pages = extract_text(request["path"])
        print(f"\nExtracted text from {os.path.basename(request['path'])} "
              f"({pages} page(s), {len(raw)} raw characters)")
    else:
        raw, pages = request["text"], max(1, len(request["text"]) // 3000 + 1)

    text = clean_text(raw)
    facts = document_facts(text, pages)
    print(f"Preprocessed text: {facts['words']} words, {facts['characters']} characters")
    print(f"Analysing ({request['analysis']} analysis)...")

    result = analyze(build_prompts(request, text, facts))
    lines = format_report(result, facts)
    display_report(lines)

    if input("\nSave this analysis? (y/n) : ").strip().lower().startswith("y"):
        path = save_report(request, lines)
        print("Analysis saved successfully to outputs/" + os.path.basename(path))


def main():
    print(BANNER)
    while True:
        try:
            run_once()
        except FileNotFoundError as error:
            print(f"\n{error}")
        if not input("\nAnalyze another document? (y/n) : ").strip().lower().startswith("y"):
            print("\nThank you for using the Legal Document Analyzer. Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
