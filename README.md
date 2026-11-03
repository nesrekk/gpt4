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

## Windows (lab computer)

1. Install **Python 3.12** from https://www.python.org/downloads/ (3.11 or 3.13 also work;
   tick **"Add python.exe to PATH"**), **Git** from https://git-scm.com/download/win and
   **Ollama** from https://ollama.com/download. Open the Ollama app once.
2. In Command Prompt:

   ```bat
   git clone https://github.com/nesrekk/gpt4.git
   cd gpt4
   setup.bat
   ```

   This makes `.venv`, installs `requirements.txt` and downloads the three models
   (about 3.4 GB). Exp 1 and Exp 3 also download small Hugging Face models on their first run.
3. Run an experiment by its number (keep the Ollama app running):

   ```bat
   run.bat 6
   ```

   `run.bat 0` ... `run.bat 6`. Or by hand: `cd Exp6_MedicalSymptomAssistant` then
   `..\.venv\Scripts\python main.py`.

If `import torch` fails with a DLL error, install the Microsoft Visual C++ Redistributable
(x64) from https://aka.ms/vs/17/release/vc_redist.x64.exe and run `run.bat` again.

## Mac / Linux

```bash
git clone https://github.com/nesrekk/gpt4.git
cd gpt4
bash setup.sh
cd Exp6_MedicalSymptomAssistant && ../.venv/bin/python main.py
```

Other experiments: `Exp0` runs `qwen_chat.py`; `Exp1` runs `create_embeddings.py` and then
`chatbot.py`; `Exp2` to `Exp6` run `main.py`.

`_tools/` holds the helper scripts used to record sessions, render screenshots,
draw the architecture diagrams, make the demo videos (`make_video.py [numbers]`) and build the records into `Records/`
(`make_records.py [REG_NO]`, then convert with `soffice --headless --convert-to pdf`).
