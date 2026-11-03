@echo off
REM One-time setup on a new Windows computer (double-click it, or run: setup.bat)
cd /d "%~dp0"

where ollama >nul 2>nul || (
    echo Ollama is not installed. Install it from https://ollama.com/download and run this again.
    pause
    exit /b 1
)
ollama list >nul 2>nul || (
    echo Ollama is not running. Open the Ollama app from the Start menu and run this again.
    pause
    exit /b 1
)

REM The packages in requirements.txt have Windows builds for Python 3.11 to 3.13
set PY=
for %%v in (3.13 3.12 3.11) do (
    if not defined PY (
        py -%%v -c "" >nul 2>nul && set "PY=py -%%v"
    )
)
if not defined PY (
    python -c "import sys; sys.exit(0 if (3, 11) <= sys.version_info[:2] <= (3, 13) else 1)" >nul 2>nul && set "PY=python"
)
if not defined PY (
    echo Python 3.11, 3.12 or 3.13 is needed. Install Python 3.12 from https://www.python.org/downloads/
    echo and tick "Add python.exe to PATH" during the install, then run this again.
    pause
    exit /b 1
)
echo Using %PY%

if not exist .venv\Scripts\python.exe %PY% -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt || (
    echo Installing the Python packages failed - see the message above.
    pause
    exit /b 1
)

ollama pull qwen2.5:0.5b
ollama pull qwen2.5:1.5b
ollama pull llama3.2

echo.
echo Setup done. To run an experiment, for example Ex 6:
echo     cd Exp6_MedicalSymptomAssistant
echo     ..\.venv\Scripts\python main.py
pause
