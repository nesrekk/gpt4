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

## Quick start (Windows)

1. Install once, if the computer doesn't have them: **Python 3.12** from
   https://www.python.org/downloads/ (3.11 or 3.13 also work; tick **"Add python.exe to PATH"**)
   and **Ollama** from https://ollama.com/download. Open the Ollama app.
2. On this page click **Code → Download ZIP**, then extract it.
3. Open the extracted `gpt4-main` folder and double-click **`start.bat`**.

The first time, `start.bat` installs the Python packages and downloads any models that are
missing (needs internet; models already on the computer are not downloaded again). Then it
shows a menu: type `0`–`6` to run an experiment, `Q` to quit. Next time it goes straight to
the menu. Keep the Ollama app running.

Ex 1 and Ex 3 also download small Hugging Face models the first time they run.

You can also run one experiment directly: `run.bat 6`, or by hand
`cd Exp6_MedicalSymptomAssistant` then `..\.venv\Scripts\python main.py`.

If `import torch` fails with a DLL error, install the Microsoft Visual C++ Redistributable
(x64) from https://aka.ms/vs/17/release/vc_redist.x64.exe and start again.

## Mac / Linux

Download the ZIP (or `git clone https://github.com/nesrekk/gpt4.git`), open a terminal in the
folder and run:

```bash
bash start.sh
```

Same as `start.bat`: it sets up the first time, then shows the experiment menu.

`_tools/` holds the helper scripts used to record sessions, render screenshots,
draw the architecture diagrams, make the demo videos (`make_video.py [numbers]`) and build the records into `Records/`
(`make_records.py [REG_NO]`, then convert with `soffice --headless --convert-to pdf`).
