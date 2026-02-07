#!/bin/bash
# Quick setup script for File Fisher

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  ░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄                ║"
echo "║  ░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀                ║"
echo "║  ░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀                ║"
echo "║                                                                    ║"
echo "║                   Quick Setup Script                               ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ Setup Complete!                              ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "To run File Fisher:"
echo ""
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the scraper:"
echo "     python scraper.py"
echo ""
echo "  3. Follow the interactive menu!"
echo ""
echo "📖 Read BEGINNER_GUIDE.md for detailed instructions"
echo ""
