@echo off
REM Quick setup script for File Fisher (Windows)

echo ========================================================================
echo   File Fisher - Quick Setup Script (Windows)
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python found: %PYTHON_VERSION%
echo.

REM Create virtual environment
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate and install dependencies
echo [*] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully!
echo.

echo ========================================================================
echo                       Setup Complete!
echo ========================================================================
echo.
echo To run File Fisher:
echo.
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run the CSV downloader or scraper:
echo      python src/csv_downloader.py  (recommended)
echo      python src/scraper.py         (alternative)
echo.
echo   3. Follow the interactive menu!
echo.
echo Read BEGINNER_GUIDE.md for detailed instructions
echo.
pause
