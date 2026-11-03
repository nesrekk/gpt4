# 24CS2506 – Building Applications using GPT-4 (Lab)

All lab experiments from the Google Classroom (Batch 1), built and run locally with **Ollama**.

| Folder | Experiment | Model |
|---|---|---|
| `Exp0_Study_Installation_of_LLM` | Study experiment – Installation of LLM (Ollama) | qwen2.5:0.5b |
| `Exp1_ECommerceGPT` | Ex 1 – AI-Powered E-Commerce Chatbot (RAG) | qwen2.5:1.5b + all-mpnet-base-v2 + RoBERTa sentiment |
| `Exp2_BlogGenerator` | Ex 2 – AI-Powered Blog Content Generator | llama3.2 |
| `Exp3_EmailAssistant` | Ex 3 – Intelligent Email Assistant | llama3.2 + all-mpnet-base-v2 |
| `Exp4_RecommendationSystem` | Ex 4 – Personalized Recommendation System | llama3.2 (GPT-4 stand-in) |
| `Exp5_LegalDocumentAnalyzer` | Ex 5 – Automated Legal Document Analyzer | llama3.2 (GPT-4 stand-in) |
| `Exp6_MedicalSymptomAssistant` | Ex 6 – AI-Powered Medical Symptom Assistant | llama3.2 (GPT-4 stand-in) |

Each experiment folder has the program, the data, `architecture.png`, `screenshots/`
(rendered from real runs; the raw terminal transcripts are in `screenshots/raw/`),
and the generated output files. Lab records (`Records/`) and demo videos (`Videos/`)
are kept on the original computer and are not in this repository.

## Get it on another computer

You need **Python 3.10+**, **Git** and **Ollama** (https://ollama.com/download).
Open the Ollama app (or run `ollama serve` in its own terminal), then:

```bash
git clone https://github.com/nesrekk/gpt4.git
cd gpt4
bash setup.sh          # Windows: setup.bat
```

The setup script makes a `.venv`, installs `requirements.txt` and downloads the three
models (about 3.4 GB in total). Exp 1 also downloads two small Hugging Face models
the first time it runs.

## Run

Mac / Linux:

```bash
cd Exp0_Study_Installation_of_LLM && ../.venv/bin/python qwen_chat.py
cd Exp1_ECommerceGPT && ../.venv/bin/python create_embeddings.py && ../.venv/bin/python chatbot.py
cd Exp2_BlogGenerator && ../.venv/bin/python main.py
cd Exp3_EmailAssistant && ../.venv/bin/python main.py
cd Exp4_RecommendationSystem && ../.venv/bin/python main.py
cd Exp5_LegalDocumentAnalyzer && ../.venv/bin/python main.py
cd Exp6_MedicalSymptomAssistant && ../.venv/bin/python main.py
```

Windows (Command Prompt): the same, with `..\.venv\Scripts\python` instead of
`../.venv/bin/python`, for example `cd Exp6_MedicalSymptomAssistant` then
`..\.venv\Scripts\python main.py`.

Run each command from the `gpt4` folder (each `cd` goes into one experiment).

`_tools/` holds the helper scripts used to record sessions, render screenshots,
draw the architecture diagrams, make the demo videos (`make_video.py [numbers]`) and build the records into `Records/`
(`make_records.py [REG_NO]`, then convert with `soffice --headless --convert-to pdf`).
