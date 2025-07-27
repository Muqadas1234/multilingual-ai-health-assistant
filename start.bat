@echo off
echo.
echo ========================================
echo   Multilingual AI Health Assistant
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found. Starting application...
echo.

REM Run the startup script
python run.py

echo.
echo Application stopped.
pause 