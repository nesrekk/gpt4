@echo off
REM Run one experiment on Windows: run.bat 0 ... run.bat 6
cd /d "%~dp0"
set PY=%~dp0.venv\Scripts\python.exe
if not exist "%PY%" (
    echo Run setup.bat first.
    pause
    exit /b 1
)
if "%~1"=="0" cd Exp0_Study_Installation_of_LLM & "%PY%" qwen_chat.py & goto :end
if "%~1"=="1" cd Exp1_ECommerceGPT & "%PY%" create_embeddings.py & "%PY%" chatbot.py & goto :end
if "%~1"=="2" cd Exp2_BlogGenerator & "%PY%" main.py & goto :end
if "%~1"=="3" cd Exp3_EmailAssistant & "%PY%" main.py & goto :end
if "%~1"=="4" cd Exp4_RecommendationSystem & "%PY%" main.py & goto :end
if "%~1"=="5" cd Exp5_LegalDocumentAnalyzer & "%PY%" main.py & goto :end
if "%~1"=="6" cd Exp6_MedicalSymptomAssistant & "%PY%" main.py & goto :end
echo Usage: run.bat ^<experiment number 0-6^>    for example: run.bat 6
:end
