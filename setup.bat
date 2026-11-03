@echo off
REM One-time setup on a new Windows computer (double-click, or run: setup.bat)
cd /d "%~dp0"
where ollama >nul 2>nul || (echo Ollama is not installed. Install it from https://ollama.com/download then run this again. & pause & exit /b 1)
ollama list >nul 2>nul || (echo Start the Ollama app first, then run this again. & pause & exit /b 1)
python -m venv .venv || (echo Python 3.10+ is needed: https://www.python.org/downloads/ & pause & exit /b 1)
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
ollama pull qwen2.5:0.5b
ollama pull qwen2.5:1.5b
ollama pull llama3.2
echo.
echo Setup done. Example: cd Exp6_MedicalSymptomAssistant ^&^& ..\.venv\Scripts\python main.py
pause
