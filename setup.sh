#!/bin/bash
# One-time setup on a new Mac / Linux computer (run from this folder: bash setup.sh)
set -e
cd "$(dirname "$0")"
if ! command -v ollama >/dev/null; then
  echo "Ollama is not installed. Install it from https://ollama.com/download (Mac: brew install ollama), then run this again."
  exit 1
fi
ollama list >/dev/null 2>&1 || { echo "Start Ollama first: open the Ollama app, or run 'ollama serve' in another terminal."; exit 1; }
python3 -c "import sys; sys.exit(0 if (3, 11) <= sys.version_info[:2] <= (3, 13) else 1)" || { echo "Python 3.11 to 3.13 is needed (python3 is $(python3 --version))."; exit 1; }
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
# download only the models that are not on this computer yet
for m in qwen2.5:0.5b qwen2.5:1.5b llama3.2; do
  ollama list | grep -qi "^$m" && echo "Model $m is already installed." || ollama pull "$m"
done
touch .venv/setup_done.txt
echo
echo "Setup done. Run: bash start.sh"
