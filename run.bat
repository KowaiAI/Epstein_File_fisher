@echo off
REM Quick run script for File Fisher (Windows)

cd /d "%~dp0"

if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Run: scripts\setup.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python src\csv_downloader.py %*
