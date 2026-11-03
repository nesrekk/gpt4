"""Draw the system architecture diagram (architecture.png) for every experiment."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

GPT4 = os.path.expanduser("~/Desktop/gpt4")
COLORS = {"io": "#E3F2FD", "llm": "#FFF3E0", "proc": "#E8F5E9", "data": "#F3E5F5"}
EDGE = {"io": "#1565C0", "llm": "#E65100", "proc": "#2E7D32", "data": "#6A1B9A"}

# Each layer is a list of (label, kind). Arrows go from every box in one layer to the next.
DIAGRAMS = {
    "Exp1_ECommerceGPT": ("E-Commerce Chatbot - System Architecture", [
        [("User Query\n(chatbot.py - loop until exit)", "io")],
        [("Intent Detection\nOllama qwen2.5 (intent_module)", "llm")],
        [("FAQ Module\nmpnet embeddings\n+ cosine similarity", "proc"),
         ("Recommendation\nTF-IDF Top-3\nretrieval", "proc"),
         ("Product QA (RAG)\nembedding retrieval\n+ structured context", "proc"),
         ("Review Module\nRoBERTa sentiment\n(pos / neu / neg)", "proc")],
        [("faqs.csv", "data"), ("products.csv", "data"), ("products.csv", "data"), ("reviews.csv", "data")],
        [("Ollama - qwen2.5:1.5b\n(constrained prompt with retrieved context)", "llm")],
        [("Natural Language Response", "io")],
    ]),
    "Exp2_BlogGenerator": ("AI Blog Content Generator - System Architecture", [
        [("User Input (input_module)\nTopic | Style | Tone | Word count", "io"),
         ("Natural-language request\n\"Write a blog on ...\"", "io")],
        [("Menu choice", "proc"), ("Intent Detection\nOllama Llama 3.2", "llm")],
        [("Prompt Construction (blog_module)", "proc")],
        [("Ollama - Llama 3.2 (local LLM)", "llm")],
        [("Blog\nGeneration", "proc"), ("Title\nGenerator", "proc"), ("SEO\nKeywords", "proc"),
         ("Summary\n(~100 words)", "proc"), ("Meta Description\n(<=160 chars)", "proc")],
        [("Save to outputs/generated_blog.txt", "data")],
    ]),
    "Exp3_EmailAssistant": ("Intelligent Email Assistant - System Architecture", [
        [("Customer Email Input\nName | Subject | Email", "io")],
        [("Intent Detection\nOllama Llama 3.2", "llm"),
         ("Similar Email Retrieval\nmpnet embeddings over data/emails.csv", "proc")],
        [("AI Reply Generation\ncustomer email + previous reply -> Llama 3.2", "llm")],
        [("Tone Improver\nFriendly | Formal | Empathetic", "proc"),
         ("Conversation Summary\n(~50 words)", "proc")],
        [("Save Reply -> outputs/generated_reply.txt\n(email, reply, intent, date)", "data")],
    ]),
    "Exp4_RecommendationSystem": ("Personalized Recommendation System - System Architecture", [
        [("User Profile Input\nname, age, background, interests,\nskill level, category, goal, count", "io")],
        [("Profile Display", "proc"), ("Preference Analysis\nOllama (JSON)", "llm")],
        [("Prompt Construction", "proc")],
        [("Recommendation Generation\nOllama Llama 3.2 (GPT-4 stand-in)", "llm")],
        [("Ranking\nby suitability score", "proc"), ("Explanation\nwhy it suits the user", "llm"),
         ("Feedback ->\nRefined list", "llm")],
        [("Intent Detection (Ollama) routes every request:\ngenerate | refine | explain | show profile | save | exit", "llm")],
        [("Save -> outputs/recommendations.txt", "data")],
    ]),
    "Exp5_LegalDocumentAnalyzer": ("Automated Legal Document Analyzer - System Architecture", [
        [("Input Module\nlegal document (.txt / .pdf / .docx or pasted text),\n"
          "document type, parties, analysis type", "io")],
        [("Extraction Module\nPyMuPDF / python-docx / text reader", "proc")],
        [("Preprocessing Module\nclean text, word / page counts,\nregex dates, amounts, periods", "proc")],
        [("Prompt Module\nfocused prompt groups + JSON schema", "proc")],
        [("Ollama - Llama 3.2 (GPT-4 stand-in, JSON mode)", "llm")],
        [("Summary &\nParties", "proc"), ("Key\nClauses", "proc"), ("Obligations", "proc"),
         ("Payment &\nTermination", "proc"), ("Important\nDates", "proc")],
        [("Structured report -> outputs/<document>_<type>_analysis.txt", "data")],
    ]),
    "Exp6_MedicalSymptomAssistant": ("AI Medical Symptom Assistant - System Architecture", [
        [("Input Module\nage, sex, symptoms, duration, severity,\nhistory, medication, allergies, notes", "io")],
        [("Profile Module\nvalidate age / sex,\nage group", "proc"),
         ("Symptom Module\nLLM symptom extraction", "llm"),
         ("Context Module\nduration, severity,\nrisk factors", "proc")],
        [("Safety Module\nrule-based red flags + triage\n(works without the LLM)", "proc"),
         ("Prompt Module\nsafety guardrails + JSON schema", "proc")],
        [("Analysis Module\npossible conditions, self-care,\nwhen to see a doctor (Llama 3.2)", "llm"),
         ("Question Module\nfollow-up questions ->\nanswers refine the analysis", "llm")],
        [("Structured report with triage level and disclaimer", "io")],
        [("Save Module -> reports/symptom_report_<time>.txt + .json", "data")],
    ]),
}


def draw(folder, title, layers):
    fig_w, row_h = 13, 1.55
    fig, ax = plt.subplots(figsize=(fig_w, row_h * len(layers) + 1.0))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, row_h * len(layers) + 0.6)
    ax.axis("off")
    ax.text(fig_w / 2, row_h * len(layers) + 0.3, title, ha="center", va="center",
            fontsize=15, fontweight="bold")

    centers = []
    for r, layer in enumerate(layers):
        y = row_h * (len(layers) - r) - row_h / 2
        n = len(layer)
        slot = (fig_w - 0.6) / n
        box_w, box_h = min(slot - 0.35, 7.5), row_h - 0.55
        row = []
        for i, (label, kind) in enumerate(layer):
            x = 0.3 + slot * i + slot / 2
            ax.add_patch(FancyBboxPatch((x - box_w / 2, y - box_h / 2), box_w, box_h,
                                        boxstyle="round,pad=0.02,rounding_size=0.12",
                                        fc=COLORS[kind], ec=EDGE[kind], lw=1.6))
            ax.text(x, y, label, ha="center", va="center", fontsize=9.5)
            row.append((x, y, box_h))
        centers.append(row)

    for upper, lower in zip(centers, centers[1:]):
        pairs = list(zip(upper, lower)) if len(upper) == len(lower) and len(upper) > 1 else \
            [(u, l) for u in upper for l in lower]
        for (x1, y1, h1), (x2, y2, h2) in pairs:
            ax.add_patch(FancyArrowPatch((x1, y1 - h1 / 2), (x2, y2 + h2 / 2),
                                         arrowstyle="-|>", mutation_scale=14, lw=1.2, color="#555"))

    out = os.path.join(GPT4, folder, "architecture.png")
    fig.savefig(out, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(out)


if __name__ == "__main__":
    for folder, (title, layers) in DIAGRAMS.items():
        draw(folder, title, layers)
