#!/bin/bash
# One-time setup on a new Mac / Linux computer (run from this folder: bash setup.sh)
set -e
cd "$(dirname "$0")"
if ! command -v ollama >/dev/null; then
  echo "Ollama is not installed. Install it from https://ollama.com/download (Mac: brew install ollama), then run this again."
  exit 1
fi
ollama list >/dev/null 2>&1 || { echo "Start Ollama first: open the Ollama app, or run 'ollama serve' in another terminal."; exit 1; }
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
ollama pull qwen2.5:0.5b
ollama pull qwen2.5:1.5b
ollama pull llama3.2
echo
echo "Setup done. Example: cd Exp6_MedicalSymptomAssistant && ../.venv/bin/python main.py"
