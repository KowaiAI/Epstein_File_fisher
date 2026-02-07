```
░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄
░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀
░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀
```

# File Fisher - DOJ Epstein Disclosures Downloader

**Download documents from the Department of Justice's Epstein Files Transparency Act disclosure portal.**

![Interactive Menu](docs/images/interactive-menu.png)

## 🌟 Two Download Methods

### Method 1: CSV Downloader (RECOMMENDED) ⭐
- ✅ Direct download links - no bot detection!
- ✅ Reliable and fast (~2 sec/file)
- ✅ 575 files across 12 data sets
- 📖 [CSV Method Guide](docs/CSV_METHOD.txt)

### Method 2: Web Scraper
- ⚠️ May encounter bot detection
- ✅ Auto-discovers new files

## 🚀 Quick Start

```bash
# Setup (run once)
./scripts/setup.sh          # Linux/Mac
scripts\setup.bat           # Windows

# Run
./run.sh                    # Linux/Mac
run.bat                     # Windows

# Or manually
source venv/bin/activate
python src/csv_downloader.py
```

## 🎯 Interactive Menu

The menu allows you to:
- Select individual data sets (1-12)
- Download all data sets at once (option 99)
- Add multiple data sets in one session
- See your download configuration before starting

## 📖 Documentation

- **[Beginner's Guide](docs/BEGINNER_GUIDE.md)** - Step-by-step instructions
- **[CSV Method](docs/CSV_METHOD.txt)** - Recommended download method
- **[Interactive Menu](docs/INTERACTIVE_MENU.txt)** - Menu guide
- **[Quick Reference](docs/QUICK_START.txt)** - All commands

## 📁 Project Structure

```
Epstein_File_fisher/
├── src/                 # Source code
│   ├── csv_downloader.py   # CSV downloader (recommended)
│   ├── scraper.py          # Web scraper
│   └── config.py           # Settings
├── scripts/             # Setup scripts
│   ├── setup.sh
│   └── setup.bat
├── docs/                # Documentation
├── run.sh / run.bat     # Quick run scripts
└── requirements.txt
```

## 💾 Output

Files download to: `~/Documents/Epstein/`

```
Documents/Epstein/
├── data_set_1/
│   ├── documents/  # PDFs
│   ├── videos/     # MP4, MOV
│   ├── audio/      # MP3
│   ├── images/     # JPG, PNG
│   └── archives/   # ZIP
├── data_set_2/
└── ... (12 total)
```

## 🛠️ Requirements

- Python 3.8+
- pip
- ~150 GB free space (for all files)

## 📝 Usage Examples

```bash
# Interactive menu
python src/csv_downloader.py

# Specific data sets
python src/csv_downloader.py --data-sets 1 2 3

# Custom CSV file
python src/csv_downloader.py /path/to/links.csv --data-sets 8

# Metadata only
python src/csv_downloader.py --no-download
```

## ⚠️ Legal Notice

These are public records from the U.S. Department of Justice. Use responsibly for research, journalism, or public interest purposes.

---

**Repository**: https://github.com/KowaiAI/Epstein_File_fisher

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
