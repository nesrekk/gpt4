#!/bin/bash
# Run this after downloading the code (bash start.sh). The first time it sets everything up,
# then it shows a menu to run any experiment.
cd "$(dirname "$0")"
G="$(pwd)"
if [ ! -f .venv/setup_done.txt ]; then
  echo "First run: setting up Python packages and models. This happens only once."
  bash setup.sh || exit 1
fi
ollama list >/dev/null 2>&1 || { echo "Ollama is not running. Open the Ollama app (or run 'ollama serve' in another terminal) and try again."; exit 1; }

PY="$G/.venv/bin/python"
while true; do
  cat <<'MENU'

==============================================
   24CS2506 - Building Applications with GPT-4
==============================================
 0. Study Experiment - Installation of LLM
 1. AI-Powered E-Commerce Chatbot
 2. AI-Powered Blog Content Generator
 3. Intelligent Email Assistant
 4. Personalized Recommendation System
 5. Automated Legal Document Analyzer
 6. AI-Powered Medical Symptom Assistant
 Q. Quit
==============================================
MENU
  read -r -p "Choose an experiment (0-6 or Q) : " ch || exit 0
  echo
  case "$ch" in
    0) (cd "$G/Exp0_Study_Installation_of_LLM" && "$PY" qwen_chat.py) ;;
    1) (cd "$G/Exp1_ECommerceGPT" && "$PY" create_embeddings.py && "$PY" chatbot.py) ;;
    2) (cd "$G/Exp2_BlogGenerator" && "$PY" main.py) ;;
    3) (cd "$G/Exp3_EmailAssistant" && "$PY" main.py) ;;
    4) (cd "$G/Exp4_RecommendationSystem" && "$PY" main.py) ;;
    5) (cd "$G/Exp5_LegalDocumentAnalyzer" && "$PY" main.py) ;;
    6) (cd "$G/Exp6_MedicalSymptomAssistant" && "$PY" main.py) ;;
    q|Q) exit 0 ;;
    *) echo "Please type a number from 0 to 6, or Q."; continue ;;
  esac
  echo; echo "---- Experiment $ch finished ----"
done
