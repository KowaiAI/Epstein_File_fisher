#!/bin/bash
# Quick run script for File Fisher

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: ./scripts/setup.sh"
    exit 1
fi

source venv/bin/activate
python src/csv_downloader.py "$@"
