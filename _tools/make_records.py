"""Build the lab record (.docx) for every experiment in the teacher's template format.

Usage: make_records.py [REG_NO]
The GitHub and LinkedIn links are written as clickable links; the <REG. NO> placeholder
(when no REG_NO is given) is highlighted in yellow.
"""
import os
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from PIL import Image

GPT4 = os.path.expanduser("~/Desktop/gpt4")
REG_NO = sys.argv[1] if len(sys.argv) > 1 else "<REG. NO>"
GITHUB = "https://github.com/nesrekk/gpt4/tree/main/"
LINKEDIN = {
    "Exp0_Study_Installation_of_LLM": "https://lnkd.in/p/dPsfB6R6",
    "Exp1_ECommerceGPT": "https://lnkd.in/p/dnqtkDq8",
    "Exp2_BlogGenerator": "https://lnkd.in/p/dn9dA3fN",
    "Exp3_EmailAssistant": "https://lnkd.in/p/dN6q59F4",
    "Exp4_RecommendationSystem": "https://lnkd.in/p/dCJ3CSym",
    "Exp5_LegalDocumentAnalyzer": "https://lnkd.in/p/dC3ejhA8",
    "Exp6_MedicalSymptomAssistant": "https://lnkd.in/p/dJe5hke7",
}

VERSIONS = [
    ("Python", "3.13.5"),
    ("Ollama", "0.40.10 (Python client ollama 0.6.3)"),
    ("VS Code", "Not used - programs were run from the macOS Terminal"),
    ("Pandas", "2.2.3"),
    ("Sentence Transformers", "6.2.0"),
]
EXTRA_VERSIONS = {
    "torch": ("PyTorch", "2.14.1"),
    "transformers": ("Transformers (Hugging Face)", "5.20.2"),
    "sklearn": ("scikit-learn", "1.6.1"),
    "pymupdf": ("PyMuPDF (PDF text extraction)", "2.0"),
    "docx": ("python-docx (Word text extraction)", "1.2.0"),
}


# ---------------------------------------------------------------- docx helpers
def set_cell_text(cell, text, bold=False, align=None, size=11):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if align:
        p.alignment = align
    if text.startswith("<") and text.endswith(">"):
        run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return run


def add_page_border(section):
    sect_pr = section._sectPr
    borders = OxmlElement("w:pgBorders")
    borders.set(qn("w:offsetFrom"), "page")
    for side in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "8")
        b.set(qn("w:space"), "24")
        b.set(qn("w:color"), "000000")
        borders.append(b)
    sect_pr.append(borders)


def new_document():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    style.font.size = Pt(12)
    section = doc.sections[0]
    section.left_margin = section.right_margin = Inches(0.9)
    section.top_margin = section.bottom_margin = Inches(0.8)
    add_page_border(section)
    return doc


def header_table(doc, ex_no, title, date):
    table = doc.add_table(rows=2, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = (Inches(1.4), Inches(3.6), Inches(1.6))
    for row in table.rows:
        for cell, w in zip(row.cells, widths):
            cell.width = w
    set_cell_text(table.cell(0, 0), f"Ex. No.:{ex_no}", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(table.cell(1, 0), date, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    title_cell = table.cell(0, 1).merge(table.cell(1, 1))
    set_cell_text(title_cell, title, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13)
    reg_cell = table.cell(0, 2).merge(table.cell(1, 2))
    set_cell_text(reg_cell, REG_NO, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    for cell in (title_cell, reg_cell):
        cell.vertical_alignment = 1  # center
    doc.add_paragraph()


def heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(12.5)
    return p


def para(doc, text, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.italic = italic
    if text.startswith("<") and text.endswith(">"):
        r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return p


def bullets(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def numbered(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Number")


def two_col_table(doc, headers, rows, widths=(2.2, 4.3)):
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell, text in zip(table.rows[0].cells, headers):
        set_cell_text(cell, text, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    for left, right in rows:
        cells = table.add_row().cells
        set_cell_text(cells[0], left, size=11)
        set_cell_text(cells[1], right, size=11)
    for row in table.rows:
        row.cells[0].width, row.cells[1].width = Inches(widths[0]), Inches(widths[1])
    doc.add_paragraph()


def code_block(doc, path, label):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    r = p.add_run(label)
    r.bold = True
    r.font.size = Pt(11)
    code = open(path, encoding="utf-8").read().rstrip("\n")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.0
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:fill"), "F4F4F4")
    p._p.get_or_add_pPr().append(shading)
    lines = code.split("\n")
    for i, line in enumerate(lines):
        run = p.add_run(line)
        run.font.name = "Courier New"
        run.element.rPr.rFonts.set(qn("w:eastAsia"), "Courier New")
        run.font.size = Pt(8.5)
        if i < len(lines) - 1:
            run.add_break()


def image(doc, path, caption, width=6.4, max_height=8.2):
    with Image.open(path) as img:
        w, h = img.size
    width = min(width, max_height * w / h)  # keep tall screenshots on one page
    doc.add_picture(path, width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c.add_run(caption)
    r.italic = True
    r.font.size = Pt(10)


def hyperlink(paragraph, url):
    """Add url to the paragraph as a clickable blue underlined link."""
    rel = paragraph.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                                   is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), rel)
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    props.extend([color, underline])
    run.append(props)
    text = OxmlElement("w:t")
    text.text = url
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def link_line(doc, label, url):
    p = doc.add_paragraph()
    p.add_run(f"{label} : ").bold = True
    hyperlink(p, url)


def software_table(doc, extras):
    rows = VERSIONS + [EXTRA_VERSIONS[e] for e in extras]
    two_col_table(doc, ("Software", "Version"), rows)


def screenshots(doc, folder, shots):
    for title, files in shots:
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.bold = True
        for f in files:
            image(doc, os.path.join(GPT4, folder, "screenshots", f), f"Fig: {title}")


# ---------------------------------------------------------------- record content
def record_ex0():
    folder = "Exp0_Study_Installation_of_LLM"
    doc = new_document()
    header_table(doc, 0, "STUDY EXPERIMENT\nInstallation of LLM (Ollama)", "05-08-2026")

    heading(doc, "Aim:")
    para(doc, "To study and install a Large Language Model (LLM) runtime - Ollama - on a local "
              "computer, download an open-source model (Qwen 2.5) and interact with it from the "
              "command line and from a Python program.")

    heading(doc, "Procedure:")
    numbered(doc, [
        "Download Ollama from https://ollama.com/download and install it (Windows: run "
        "OllamaSetup.exe; macOS: install the app or run 'brew install ollama'; Linux: run the "
        "install script given on the website).",
        "Open a terminal / command prompt and verify the installation with 'ollama --version'.",
        "Start the Ollama server with 'ollama serve' (the desktop app starts it automatically). "
        "It listens on http://localhost:11434.",
        "Download the Qwen model once with 'ollama pull qwen2.5:0.5b'.",
        "List the models available locally with 'ollama list'.",
        "Test the model directly from the terminal with 'ollama run qwen2.5:0.5b \"<question>\"'.",
        "Install the official Python client with 'pip install ollama'.",
        "Write the Python program (qwen_chat.py) that sends the user's question with a system "
        "prompt to the local Qwen model through ollama.Client().chat() and prints the reply.",
        "Run the program with 'python qwen_chat.py', type a question and observe the answer "
        "generated completely offline on the local machine.",
    ])

    heading(doc, "Commands to use Ollama:")
    two_col_table(doc, ("Command", "Purpose"), [
        ("ollama --version", "Check the installed Ollama version"),
        ("ollama serve", "Start the local Ollama server (REST API on port 11434)"),
        ("ollama pull qwen2.5:0.5b", "Download a model from the Ollama library"),
        ("ollama list", "List all models downloaded on this computer"),
        ("ollama run qwen2.5:0.5b", "Chat with a model interactively in the terminal (/bye to quit)"),
        ("ollama run <model> \"prompt\"", "Ask a single question and print the answer"),
        ("ollama show qwen2.5:0.5b", "Show model details (parameters, template, licence)"),
        ("ollama ps", "Show models currently loaded in memory"),
        ("ollama stop <model>", "Unload a running model from memory"),
        ("ollama rm <model>", "Delete a downloaded model"),
        ("pip install ollama", "Install the Python client library"),
    ], widths=(2.6, 3.9))

    heading(doc, "Program:")
    code_block(doc, os.path.join(GPT4, folder, "qwen_chat.py"), "qwen_chat.py")

    heading(doc, "Output Screenshot:")
    screenshots(doc, folder, [
        ("Ollama installation and version", ["01_install_and_version.png"]),
        ("Downloading the Qwen model and listing local models", ["02_pull_model.png"]),
        ("Running the model from the command line", ["03_ollama_run.png"]),
        ("Running the Python program", ["04_python_program.png"]),
    ])

    heading(doc, "Video Link:")
    link_line(doc, "LinkedIn Post (video)", LINKEDIN[folder])
    link_line(doc, "GitHub Link", GITHUB + folder)

    heading(doc, "Result:")
    para(doc, "Thus, the Ollama LLM runtime was successfully installed, the Qwen 2.5 (0.5B) model "
              "was downloaded and executed locally, and a Python program was written to interact "
              "with the local model without using any cloud API.")
    return doc, folder, "Ex0_Record_Study_Installation_of_LLM"


def record_ex1():
    folder = "Exp1_ECommerceGPT"
    doc = new_document()
    header_table(doc, 1, "Building E-commerce Chatbot", "02-09-2026")
    heading(doc, "Aim:")
    para(doc, "To build an AI-powered E-Commerce Chatbot using Retrieval-Augmented Generation (RAG) "
              "with Ollama.")
    heading(doc, "Problem Statement:")
    para(doc, "Design and develop a modular Retrieval-Augmented Generation (RAG) based e-commerce "
              "chatbot using Ollama. The chatbot should answer FAQs, recommend products, answer "
              "product-specific questions, summarize customer reviews, and intelligently route user "
              "queries using an LLM-based intent detector.")
    heading(doc, "Software Requirements:")
    software_table(doc, ["torch", "transformers", "sklearn"])
    para(doc, "Models used: qwen2.5:1.5b via Ollama (LLM), all-mpnet-base-v2 (sentence embeddings), "
              "cardiffnlp/twitter-roberta-base-sentiment-latest (sentiment analysis). The sample "
              "code's qwen2.5:0.5b gave incorrect answers in testing, so the slightly larger model "
              "from the same Qwen 2.5 family was used.", italic=True)
    heading(doc, "Dataset Description")
    two_col_table(doc, ("Dataset", "Purpose"), [
        ("Products\n(100 rows, 7 columns: ProductID, ProductName, Category, Brand, Price, "
         "Description, Rating)",
         "Product catalogue (laptops, mobiles, headphones, smartwatches). Used by the "
         "Recommendation module (TF-IDF Top-3 retrieval) and the Product QA module (retrieved "
         "product becomes the RAG context for Ollama)."),
        ("FAQs\n(20 rows, 3 columns: FAQID, Question, Answer)",
         "Common customer questions with answers. Embedded with sentence-transformers and used "
         "by the FAQ module for semantic search with cosine similarity."),
        ("Reviews\n(199 rows, 5 columns: ReviewID, ProductID, ProductName, Review, Rating)",
         "Customer opinions on products. Used by the Review module for sentiment analysis and "
         "for the Ollama review summary / buying suggestion."),
    ], widths=(2.4, 4.1))
    heading(doc, "System Architecture")
    image(doc, os.path.join(GPT4, folder, "architecture.png"), "Fig: System architecture", 6.2)
    heading(doc, "Module Design")
    two_col_table(doc, ("Module", "Responsibility"), [
        ("FAQ Module\n(faq_module.py)", "Loads the stored FAQ embeddings, finds the best FAQ with "
         "cosine similarity, applies a 0.50 similarity threshold and uses Ollama to phrase a "
         "natural answer; otherwise passes the query to the next module."),
        ("Recommendation Module\n(recommendation_module.py)", "Builds TF-IDF vectors of the product "
         "text, retrieves the Top-3 products (ties broken by rating) and asks Ollama to recommend "
         "the best one with a justification."),
        ("Product Module\n(product_module.py)", "Retrieves the most relevant product, prepares a "
         "structured context and answers only from that context (constrained prompt). Remembers "
         "the current product for follow-up questions such as 'What is its price?'."),
        ("Review Module\n(review_module.py)", "Loads a pre-trained 3-class sentiment model, "
         "classifies every review of the product, counts Positive / Neutral / Negative and asks "
         "Ollama for an overall opinion, strengths, weaknesses and buying suggestion."),
        ("Intent Module\n(intent_module.py)", "Uses Ollama with few-shot examples to classify a "
         "query as FAQ, RECOMMENDATION, PRODUCT or REVIEW (keyword fallback if the reply is "
         "not a valid label)."),
        ("Chatbot\n(chatbot.py)", "Integrates all modules, detects the intent of each message, "
         "routes it to the right module and keeps interacting until the user types exit."),
        ("create_embeddings.py / llm_utils.py", "Dataset loading and display (Part A), FAQ "
         "embedding generation and storage (Part B), shared Ollama helper."),
    ], widths=(2.2, 4.3))
    implementation(doc, folder, ["create_embeddings.py", "faq_module.py", "recommendation_module.py",
                                 "product_module.py", "review_module.py", "intent_module.py",
                                 "chatbot.py", "llm_utils.py"])
    heading(doc, "Output Screenshots:")
    screenshots(doc, folder, [
        ("Dataset Preparation (Part A)", ["01_dataset_preparation.png"]),
        ("FAQ", ["02_faq_semantic_search.png"]),
        ("Recommendation", ["03_product_recommendation.png"]),
        ("Product QA", ["04_product_qa_rag.png"]),
        ("Review Summary", ["05_review_summary.png"]),
        ("Intent Detection", ["06_intent_detection.png"]),
        ("Integrated Chatbot", ["07_chatbot_part1.png", "08_chatbot_part2.png"]),
    ])
    heading(doc, "Result:")
    para(doc, "Thus successfully built a local chatbot system that can answer product-related "
              "questions from a dataset, recommend products based on similarity, analyze sentiment "
              "from user/product reviews, and simulate FAQ responses using Ollama.")
    return doc, folder, "Ex1_Record_ECommerce_Chatbot"


def record_ex2():
    folder = "Exp2_BlogGenerator"
    doc = new_document()
    header_table(doc, 2, "AI-Powered Blog Content Generator", "09-09-2026")
    heading(doc, "Aim:")
    para(doc, "To build an AI-powered Blog Content Generator using Ollama that generates blogs, "
              "titles, summaries, SEO keywords, and meta descriptions based on user prompts.")
    heading(doc, "Problem Statement:")
    para(doc, "Design and develop a modular AI-powered Blog Content Generator using Ollama. The "
              "application should generate high-quality blogs from user-provided topics, writing "
              "styles, and word counts. It should also generate blog titles, summaries, SEO "
              "keywords, and meta descriptions while intelligently routing user requests using an "
              "LLM-based intent detector.")
    heading(doc, "Software Requirements:")
    software_table(doc, [])
    para(doc, "Model used: Llama 3.2 (3B) via Ollama, as specified in the lab question.", italic=True)
    heading(doc, "Input Parameters")
    two_col_table(doc, ("Parameters", "Description"), [
        ("Blog Topic", "Subject of the blog, e.g. 'Artificial Intelligence in Education'."),
        ("Writing Style", "How the blog is written, e.g. Professional, Casual, Technical, "
                          "Storytelling."),
        ("Tone", "Attitude of the writing, e.g. Formal, Friendly, Persuasive, Informative."),
        ("Word count", "Approximate length of the blog in words (default 500)."),
    ])
    heading(doc, "System Architecture")
    image(doc, os.path.join(GPT4, folder, "architecture.png"), "Fig: System architecture", 6.2)
    heading(doc, "Module Design")
    two_col_table(doc, ("Module", "Responsibility"), [
        ("Input Module\n(input_module.py)", "Reads topic, writing style, tone and word count and "
                                             "displays them neatly."),
        ("Blog Module\n(blog_module.py)", "Constructs the prompt from the user inputs and uses "
                                           "Llama 3.2 to generate the complete blog (title, "
                                           "Introduction, sub-headings, Conclusion)."),
        ("Title Module\n(title_module.py)", "Generates five attractive blog titles."),
        ("Summary Module\n(summary_module.py)", "Generates a summary of about 100 words."),
        ("SEO Module\n(keyword_module.py, meta_module.py)", "Generates SEO keywords and a meta "
                                                            "description of at most 160 characters "
                                                            "(retries / trims if longer)."),
        ("Intent Module\n(intent_module.py)", "Uses Ollama to detect the intent of a "
                                               "natural-language request (BLOG_GENERATION, "
                                               "SUMMARY, KEYWORD_GENERATION, META_DESCRIPTION, "
                                               "TITLE_GENERATION, SAVE_BLOG, EXIT) and extracts "
                                               "the topic."),
        ("File Module\n(utils.py - save_blog)", "Saves the blog, titles, keywords, summary and "
                                                 "meta description to outputs/generated_blog.txt."),
        ("Main Module\n(main.py)", "Menu-driven application with continuous interaction until "
                                    "Exit; accepts menu numbers or free-text requests."),
    ])
    implementation(doc, folder, ["main.py", "input_module.py", "blog_module.py", "title_module.py",
                                 "keyword_module.py", "summary_module.py", "meta_module.py",
                                 "intent_module.py", "utils.py"])
    heading(doc, "Output Screenshots:")
    screenshots(doc, folder, [
        ("Home Screen", ["01_home_screen.png"]),
        ("User Input", ["02_user_input.png"]),
        ("Blog Generation", ["03_blog_generation.png"]),
        ("Blog Title Generation", ["04_blog_titles.png"]),
        ("Summary Generation", ["06_summary.png"]),
        ("SEO Keywords", ["05_seo_keywords.png"]),
        ("Meta Description", ["07_meta_description.png"]),
        ("Blog Saved Successfully", ["08_blog_saved.png"]),
        ("Intent Detection", ["09_intent_detection.png", "10_intent_in_app_blog.png",
                              "11_intent_in_app_summary_keywords.png"]),
    ])
    heading(doc, "Result:")
    para(doc, "Thus, an AI-powered Blog Content Generator was successfully developed using Ollama. "
              "The application generates blogs based on user prompts, creates titles, summaries, "
              "SEO keywords, and meta descriptions, saves the generated content to a text file, and "
              "demonstrates the use of local Large Language Models (LLMs) for content generation "
              "without requiring cloud-based APIs.")
    return doc, folder, "Ex2_Record_AI_Blog_Content_Generator"


def record_ex3():
    folder = "Exp3_EmailAssistant"
    doc = new_document()
    header_table(doc, 3, "Intelligent Email Assistant", "07-10-2026")
    heading(doc, "Aim:")
    para(doc, "To develop an Intelligent Email Assistant using Ollama that generates context-aware "
              "customer replies by analyzing previous email interactions.")
    heading(doc, "Problem Statement:")
    para(doc, "Develop an AI-powered Email Assistant capable of understanding customer queries, "
              "retrieving similar historical conversations, generating professional responses, "
              "improving tone, summarizing conversations, and storing generated replies.")
    heading(doc, "Software Requirements:")
    software_table(doc, ["torch"])
    para(doc, "Models used: Llama 3.2 (3B) via Ollama; all-mpnet-base-v2 sentence embeddings for "
              "similar-email retrieval. Dataset: Email_Assistant_Dataset_100.xlsx (100 previous "
              "interactions, saved as data/emails.csv).", italic=True)
    heading(doc, "Input Parameters")
    two_col_table(doc, ("Parameters", "Description"), [
        ("Customer Name", "Name of the customer; used in the greeting of the generated reply."),
        ("Subject", "Subject line of the email; used together with the body for intent "
                    "detection and similar-email retrieval."),
        ("Email", "Body of the customer's email describing the issue."),
    ])
    heading(doc, "System Architecture")
    image(doc, os.path.join(GPT4, folder, "architecture.png"), "Fig: System architecture", 6.2)
    heading(doc, "Module Design")
    two_col_table(doc, ("Module", "Responsibility"), [
        ("Input Module\n(input_module.py)", "Reads customer name, subject and email and displays "
                                             "the entered details."),
        ("Intent Module\n(intent_module.py)", "Uses Ollama to classify the email as Delivery "
                                               "Issue, Refund Request, Product Complaint, Technical "
                                               "Support, Order Cancellation, General Inquiry (plus "
                                               "the dataset's Payment Issue, Warranty, Account "
                                               "Issue, Exchange Request)."),
        ("Retrieval Module\n(retrieval_module.py)", "Loads previous interactions from "
                                                     "data/emails.csv, embeds them and retrieves "
                                                     "the most similar previous email and reply."),
        ("Reply Module\n(reply_module.py)", "Generates a professional reply from the customer "
                                             "email and the previous reply."),
        ("Tone Module\n(tone_module.py)", "Rewrites the reply in Friendly, Formal and Empathetic "
                                           "tones without changing the facts."),
        ("Summary Module\n(summary_module.py)", "Summarizes the customer issue and the promised "
                                                 "action in about 50 words."),
        ("Save Module\n(utils.py - save_reply)", "Saves customer email, generated reply, intent "
                                                  "and date to outputs/generated_reply.txt."),
        ("Main Module\n(main.py)", "Menu-driven integration of all modules until Exit."),
    ])
    implementation(doc, folder, ["main.py", "input_module.py", "intent_module.py",
                                 "retrieval_module.py", "reply_module.py", "tone_module.py",
                                 "summary_module.py", "utils.py"])
    heading(doc, "Output Screenshots:")
    screenshots(doc, folder, [
        ("Home Screen", ["01_home_screen.png"]),
        ("Customer Email", ["02_customer_email.png"]),
        ("Intent Detection", ["03_intent_detection.png"]),
        ("Similar Email Retrieval", ["04_similar_email_retrieval.png"]),
        ("AI Reply", ["05_ai_reply.png"]),
        ("Tone Improvement", ["06_tone_improvement.png"]),
        ("Conversation Summary", ["07_conversation_summary.png"]),
        ("Saved Reply", ["08_saved_reply.png"]),
    ])
    heading(doc, "Result:")
    para(doc, "Thus, an Intelligent Email Assistant was successfully developed using Ollama. The "
              "application understands customer emails, retrieves similar historical "
              "conversations, generates professional responses, rewrites replies in different "
              "tones, summarizes conversations, and saves generated replies locally without "
              "requiring cloud-based APIs.")
    return doc, folder, "Ex3_Record_Intelligent_Email_Assistant"


def record_ex4():
    folder = "Exp4_RecommendationSystem"
    doc = new_document()
    header_table(doc, 4, "PERSONALIZED RECOMMENDATION SYSTEM", "07-10-2026")
    heading(doc, "Aim:")
    para(doc, "To develop a personalized recommendation system using GPT-4 that analyzes user "
              "preferences and generates, ranks and explains suitable recommendations based on the "
              "user's profile, interests, skill level and goals.")
    heading(doc, "Problem Statement:")
    para(doc, "Design and develop an intelligent personalized recommendation system using GPT-4. "
              "The application should collect user information and preferences, analyze the user's "
              "requirements, generate personalized recommendations, rank them according to "
              "suitability, provide explanations for the recommendations and refine the results "
              "based on user feedback.")
    heading(doc, "Software Requirements:")
    software_table(doc, [])
    para(doc, "Model used: Llama 3.2 (3B) running locally through Ollama as the GPT-4 style "
              "language model (no paid API key needed); JSON output mode is used so the "
              "recommendations can be ranked programmatically.", italic=True)
    heading(doc, "Input Parameters")
    two_col_table(doc, ("Parameters", "Description"), [
        ("Name", "User's name, used to personalize explanations."),
        ("Age", "User's age."),
        ("Background", "Educational / professional background, e.g. Computer Science."),
        ("Interests", "Topics the user likes, e.g. Artificial Intelligence, Python."),
        ("Skill Level", "Beginner / Intermediate / Advanced."),
        ("Preferred Category", "Type of item to recommend, e.g. online courses, books, projects."),
        ("Goal", "What the user wants to achieve, e.g. Learn AI."),
        ("Preferences", "How the user likes to learn, e.g. practical learning."),
        ("Number of items", "How many recommendations to generate (default 5)."),
    ])
    heading(doc, "System Architecture")
    image(doc, os.path.join(GPT4, folder, "architecture.png"), "Fig: System architecture", 6.2)
    heading(doc, "Module Design")
    two_col_table(doc, ("Module", "Responsibility"), [
        ("Input Module\n(input_module.py)", "Reads the user profile: name, age, background, "
                                             "interests, skill level, category, preference, goal "
                                             "and number of items."),
        ("Profile Module\n(profile_module.py)", "Displays the collected profile neatly."),
        ("Preference Module\n(profile_module.py)", "Analyzes the profile with the LLM to identify "
                                                    "primary / secondary interest and constraints, "
                                                    "together with skill level, goal and "
                                                    "preference."),
        ("Prompt Module\n(prompt_module.py)", "Constructs the recommendation prompt from the "
                                               "profile (and the feedback when refining)."),
        ("Recommendation Module\n(recommendation_module.py)", "Generates the personalized "
                                                               "recommendations (name, reason, "
                                                               "suitability score) as JSON."),
        ("Ranking Module\n(ranking_module.py)", "Ranks the recommendations by suitability score "
                                                 "and prints the Rank | Recommendation | Score "
                                                 "table."),
        ("Explanation Module\n(explanation_module.py)", "Explains why every recommendation suits "
                                                         "the user."),
        ("Feedback Module\n(feedback_module.py)", "Collects feedback and generates a refined "
                                                   "recommendation list."),
        ("Intent Module\n(intent_module.py)", "Detects GENERATE_RECOMMENDATION, "
                                               "REFINE_RECOMMENDATION, SHOW_PROFILE, "
                                               "EXPLAIN_RECOMMENDATION, SAVE_RECOMMENDATION and "
                                               "EXIT."),
        ("Save Module\n(save_module.py)", "Saves the ranked recommendations (and explanations) to "
                                           "outputs/recommendations.txt."),
        ("Main Module\n(main.py)", "Integrates all modules with continuous interaction until the "
                                    "user exits."),
    ])
    implementation(doc, folder, ["main.py", "input_module.py", "profile_module.py",
                                 "prompt_module.py", "recommendation_module.py",
                                 "ranking_module.py", "explanation_module.py",
                                 "feedback_module.py", "intent_module.py", "save_module.py",
                                 "utils.py"])
    heading(doc, "Output Screenshots:")
    screenshots(doc, folder, [
        ("Home Screen", ["01_home_screen.png"]),
        ("User Profile Input", ["02_user_profile_input.png"]),
        ("Collected User Profile", ["03_collected_user_profile.png"]),
        ("Preference Analysis", ["04_preference_analysis.png"]),
        ("Prompt Generation", ["05_prompt_generation.png"]),
        ("GPT-4 Recommendation", ["06_recommendations.png"]),
        ("Recommendation Ranking", ["07_recommendation_ranking.png"]),
        ("Recommendation Explanation", ["08_recommendation_explanation.png"]),
        ("User Feedback", ["09_user_feedback.png"]),
        ("Refined Recommendations", ["10_refined_recommendations.png"]),
        ("Intent Detection", ["11_intent_detection.png"]),
        ("Recommendation Saved Successfully", ["12_recommendation_saved.png"]),
    ])
    heading(doc, "Result:")
    para(doc, "Thus, a personalized recommendation system using GPT-4 was successfully developed. "
              "The system collects user information, analyzes preferences, generates personalized "
              "recommendations, ranks and explains the recommendations, accepts user feedback and "
              "produces refined recommendations.")
    return doc, folder, "Ex4_Record_Personalized_Recommendation_System"


def record_ex5():
    folder = "Exp5_LegalDocumentAnalyzer"
    doc = new_document()
    header_table(doc, 5, "AUTOMATED LEGAL DOCUMENT ANALYZER USING GPT-4", "08-10-2026")
    heading(doc, "Aim:")
    para(doc, "To develop an automated legal document analyzer using GPT-4 that summarizes legal "
              "documents and extracts important information such as parties, key clauses, "
              "obligations, payment terms, termination conditions and important dates.")
    heading(doc, "Problem Statement:")
    para(doc, "Design and develop an automated legal document analyzer using GPT-4. The "
              "application should accept legal contracts or legal text, analyze the content, "
              "generate a concise summary, identify important clauses and obligations, extract "
              "relevant information and present the results in a structured format.")
    heading(doc, "Software Requirements:")
    software_table(doc, ["pymupdf", "docx"])
    para(doc, "Model used: Llama 3.2 (3B) running locally through Ollama as the GPT-4 style "
              "language model, in JSON output mode. Sample documents: data/nda_agreement.txt "
              "(Mutual NDA) and data/service_agreement.pdf (Software Development Service "
              "Agreement).", italic=True)
    heading(doc, "Input Parameters")
    two_col_table(doc, ("Parameter", "Description"), [
        ("Legal Document", "Contract or legal text - a .txt, .pdf or .docx file path, or text "
                           "pasted directly into the terminal."),
        ("Document Type", "Auto-detect / NDA / Employment / Service / Lease / Sale / Other; "
                          "used as a hint in the prompt."),
        ("Parties", "Parties mentioned in the document (optional - detected automatically "
                    "when left blank)."),
        ("Document Length", "Number of pages, words and characters, measured by the "
                            "Extraction and Preprocessing modules."),
        ("Analysis Type", "Summary / Clause / Obligation / Complete - selects which parts of "
                          "the analysis are generated."),
        ("Output Format", "Structured text report shown on screen and saved to "
                          "outputs/<document>_<type>_analysis.txt."),
    ])
    heading(doc, "System Architecture")
    image(doc, os.path.join(GPT4, folder, "architecture.png"), "Fig: System architecture", 6.2)
    heading(doc, "Module Design")
    two_col_table(doc, ("Module", "Responsibility"), [
        ("Input Module\n(input_module.py)", "Accepts the legal document (file path or pasted "
                                             "text), document type, parties and analysis type "
                                             "from the user."),
        ("Extraction Module\n(extraction_module.py)", "Extracts the raw text and page count from "
                                                       ".pdf (PyMuPDF), .docx (python-docx) and "
                                                       ".txt documents."),
        ("Preprocessing Module\n(preprocessing_module.py)", "Cleans the text (page numbers, "
                                                             "broken lines, extra spaces), counts "
                                                             "words / characters and finds dates, "
                                                             "amounts and time periods with "
                                                             "regular expressions."),
        ("Prompt Module\n(prompt_module.py)", "Builds focused prompts (overview, clauses, "
                                               "obligations, payment & termination, dates) with "
                                               "a JSON schema and the regex facts, for the "
                                               "selected analysis type."),
        ("Summary Module\n(summary_module.py)", "Runs the prompts on Ollama, merges the JSON "
                                                 "answers and presents the summary, parties, key "
                                                 "clauses, obligations, payment terms, "
                                                 "termination conditions and important dates, "
                                                 "plus a rule-based cross-check."),
        ("Save Module\n(save_module.py)", "Saves the structured analysis to the outputs "
                                           "folder."),
        ("Main Module\n(main.py)", "Coordinates all modules and keeps analyzing documents "
                                    "until the user chooses to stop."),
    ])
    implementation(doc, folder, ["main.py", "input_module.py", "extraction_module.py",
                                 "preprocessing_module.py", "prompt_module.py",
                                 "summary_module.py", "save_module.py", "utils.py"])
    heading(doc, "Output Screenshots:")
    screenshots(doc, folder, [
        ("Home Screen and Document Input", ["01_home_and_input.png"]),
        ("Complete Analysis - NDA (.txt)", ["02_complete_analysis_1.png", "03_complete_analysis_2.png"]),
        ("Clause Analysis - Service Agreement (.pdf)", ["04_clause_analysis_1.png",
                                                        "04_clause_analysis_2.png"]),
        ("Obligation Analysis - Service Agreement (.pdf)", ["05_obligation_analysis_1.png",
                                                            "05_obligation_analysis_2.png"]),
        ("Summary Analysis - Pasted Legal Text", ["06_summary_pasted_text.png"]),
        ("Analysis Saved Successfully", ["07_saved_analysis.png"]),
    ])
    heading(doc, "Result:")
    para(doc, "Thus, an automated legal document analyzer using GPT-4 was successfully developed. "
              "The system accepts legal documents, processes the text, generates a concise "
              "summary, identifies important clauses and obligations, extracts relevant "
              "information and produces a structured analysis.")
    return doc, folder, "Ex5_Record_Automated_Legal_Document_Analyzer"


def record_ex6():
    folder = "Exp6_MedicalSymptomAssistant"
    doc = new_document()
    header_table(doc, 6, "AI-POWERED MEDICAL SYMPTOM ASSISTANT USING GPT-4", "19-09-2026")
    heading(doc, "Aim:")
    para(doc, "To develop an AI-powered medical symptom assistant using GPT-4 that analyzes "
              "user-reported symptoms, identifies possible associated conditions, generates "
              "relevant follow-up questions and provides general guidance regarding professional "
              "medical attention.")
    heading(doc, "Problem Statement:")
    para(doc, "Design and develop an AI-powered medical symptom assistant using GPT-4. The "
              "application should collect basic user information and symptoms, analyze the "
              "reported symptoms, identify possible conditions, generate follow-up questions and "
              "present the results in a structured format. The system should include appropriate "
              "safety instructions and clearly state that the generated output is not a medical "
              "diagnosis.")
    heading(doc, "Software Requirements:")
    software_table(doc, [])
    para(doc, "Model used: Llama 3.2 (3B) running locally through Ollama as the GPT-4 style "
              "language model, in JSON output mode. Emergency red flags are checked by fixed "
              "rules, so the safety warning never depends on the LLM.", italic=True)
    heading(doc, "Input Parameters")
    two_col_table(doc, ("Parameters", "Description"), [
        ("Age", "Age in years (1-120); used to place the user in an age group (child, "
                "adolescent, adult, older adult)."),
        ("Sex", "Male / Female / Other."),
        ("Symptoms", "Free-text description of the complaints, e.g. 'fever, dry cough and "
                     "body pain'."),
        ("Duration", "How long the symptoms have lasted, e.g. 3 days, 1 week."),
        ("Severity", "Mild / Moderate / Severe."),
        ("Medical History", "Existing conditions such as asthma, diabetes or hypertension "
                            "(risk factors)."),
        ("Medication", "Medicines currently being taken."),
        ("Allergies", "Known allergies, e.g. penicillin."),
        ("Additional Information", "Temperature, travel, contact with sick people, and the "
                                   "answers to the follow-up questions."),
    ])
    heading(doc, "System Architecture")
    image(doc, os.path.join(GPT4, folder, "architecture.png"), "Fig: System architecture", 6.2)
    heading(doc, "Module Design")
    two_col_table(doc, ("Module", "Responsibility"), [
        ("Input Module\n(input_module.py)", "Collects age, sex, the free-text symptom "
                                             "description and the context fields from the "
                                             "terminal."),
        ("Profile Module\n(profile_module.py)", "Validates the age (1-120) and sex and assigns "
                                                 "the age group."),
        ("Symptom Module\n(symptom_module.py)", "Uses the LLM to turn the free-text description "
                                                 "into a list of distinct symptoms."),
        ("Context Module\n(context_module.py)", "Converts the duration to days, normalises "
                                                 "severity and finds risk factors from the "
                                                 "history and age group."),
        ("Prompt Module\n(prompt_module.py)", "Builds the analysis and follow-up prompts with "
                                               "safety rules (no diagnosis, no prescription "
                                               "drugs, mention uncertainty) and a JSON schema."),
        ("Analysis Module\n(analysis_module.py)", "Gets possible conditions with likelihood and "
                                                   "reasoning, self-care measures, warning signs "
                                                   "and the recommended specialist."),
        ("Question Module\n(question_module.py)", "Generates five follow-up questions; the "
                                                   "user's answers are added to the context and "
                                                   "the analysis is refined."),
        ("Safety Module\n(safety_module.py)", "Rule-based scan for emergency red flags (chest "
                                               "pain, breathing difficulty, stroke signs ...), "
                                               "assigns the triage level and adds the "
                                               "disclaimer."),
        ("Save Module\n(save_module.py)", "Saves each report as timestamped .txt and .json "
                                           "files in the reports folder."),
        ("Main Module\n(main.py)", "Coordinates all modules and allows repeated assessments "
                                    "until the user exits."),
    ])
    implementation(doc, folder, ["main.py", "input_module.py", "profile_module.py",
                                 "symptom_module.py", "context_module.py", "prompt_module.py",
                                 "analysis_module.py", "question_module.py", "safety_module.py",
                                 "save_module.py", "utils.py"])
    heading(doc, "Output Screenshots:")
    screenshots(doc, folder, [
        ("Home Screen and User Input", ["01_home_and_input.png"]),
        ("Symptom Analysis, Triage and Follow-up Questions", ["02_analysis.png"]),
        ("Answering Follow-up Questions", ["03_follow_up_answers.png"]),
        ("Refined Analysis", ["04_refined_analysis.png"]),
        ("Report Saved Successfully", ["05_report_saved.png"]),
        ("Emergency Red-Flag Detection", ["06_emergency_input.png", "07_emergency_report.png"]),
    ])
    heading(doc, "Result:")
    para(doc, "Thus, an AI-powered medical symptom assistant using GPT-4 was successfully "
              "developed. The system accepts user-reported symptoms and relevant contextual "
              "information, performs preliminary symptom analysis, generates possible conditions "
              "and follow-up questions, provides appropriate medical-attention guidance and "
              "produces a structured informational response with a safety disclaimer.")
    return doc, folder, "Ex6_Record_AI_Medical_Symptom_Assistant"


def implementation(doc, folder, files):
    heading(doc, "Implementation")
    link_line(doc, "GitHub Link", GITHUB + folder)
    link_line(doc, "LinkedIn Post Link", LINKEDIN[folder])
    p = doc.add_paragraph()
    p.add_run("Program:").bold = True
    for name in files:
        code_block(doc, os.path.join(GPT4, folder, name), name)


if __name__ == "__main__":
    os.makedirs(os.path.join(GPT4, "Records"), exist_ok=True)
    only = sys.argv[2:]  # optional: build only these record numbers, e.g. "5 6"
    builders = (record_ex0, record_ex1, record_ex2, record_ex3, record_ex4, record_ex5, record_ex6)
    for number, build in enumerate(builders):
        if only and str(number) not in only:
            continue
        doc, folder, name = build()
        path = os.path.join(GPT4, "Records", name + ".docx")
        doc.save(path)
        print(path)
