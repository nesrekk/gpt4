@echo off
REM Double-click this after extracting the ZIP. The first time it sets everything up,
REM then it shows a menu to run any experiment.
cd /d "%~dp0"
title GPT-4 Lab Experiments

if not exist .venv\setup_done.txt (
    echo First run: setting up Python packages and models. This happens only once.
    echo.
    call setup.bat nopause || (
        pause
        exit /b 1
    )
)

ollama list >nul 2>nul || (
    echo Ollama is not running. Open the Ollama app from the Start menu and run start.bat again.
    pause
    exit /b 1
)

:menu
cd /d "%~dp0"
echo.
echo ==============================================
echo    24CS2506 - Building Applications with GPT-4
echo ==============================================
echo  0. Study Experiment - Installation of LLM
echo  1. AI-Powered E-Commerce Chatbot
echo  2. AI-Powered Blog Content Generator
echo  3. Intelligent Email Assistant
echo  4. Personalized Recommendation System
echo  5. Automated Legal Document Analyzer
echo  6. AI-Powered Medical Symptom Assistant
echo  Q. Quit
echo ==============================================
set CH=
set /p CH=Choose an experiment (0-6 or Q) :
if /i "%CH%"=="q" exit /b 0
for %%n in (0 1 2 3 4 5 6) do if "%CH%"=="%%n" goto run
echo Please type a number from 0 to 6, or Q.
goto menu

:run
echo.
call run.bat %CH%
echo.
echo ---- Experiment %CH% finished ----
goto menu
