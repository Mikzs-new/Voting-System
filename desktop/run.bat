@echo off
title School Voting System - Staff Desktop
echo ========================================
echo   School Voting System Desktop App
echo ========================================
echo.
echo Starting application...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Run the application
python main.py

pause