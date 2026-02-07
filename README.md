```
░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄
░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀
░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀
```

# DOJ Epstein Disclosures Scraper

A Python web scraper for the Department of Justice's Epstein Files Transparency Act (EFTA) disclosure portal.

## 🔰 **NEW: [Complete Beginner's Guide](BEGINNER_GUIDE.md)**

**Not tech-savvy? No problem!** We've created a detailed step-by-step guide with simple instructions for everyone. [Click here to read the Beginner's Guide →](BEGINNER_GUIDE.md)

## Overview

This scraper collects documents from all 12 data sets published at:
https://www.justice.gov/epstein/doj-disclosures

### Features

- ✅ **Comprehensive Coverage**: Scrapes all 12 data sets
- ✅ **Pagination Handling**: Automatically navigates through all pages
- ✅ **Metadata Collection**: Saves document URLs and filenames
- ✅ **PDF Download**: Optional bulk download of all documents
- ✅ **Rate Limiting**: Respectful scraping with configurable delays
- ✅ **Retry Logic**: Automatic retries for failed requests
- ✅ **Progress Tracking**: Real-time progress bars
- ✅ **Logging**: Comprehensive logs for debugging
- ✅ **Resume Support**: Skips already downloaded files

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

**Linux/Mac:**
```bash
cd scrapers/doj-epstein

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Windows (Command Prompt):**
```cmd
cd scrapers\doj-epstein

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
cd scrapers\doj-epstein

# Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Download all files from all data sets
python scraper.py

# Only collect metadata (no downloads)
python scraper.py --no-download

# Scrape specific data sets
python scraper.py --data-sets 1 2 3

# Custom output directory
python scraper.py --output-dir /path/to/output

# Recommended for testing
python scraper.py --data-sets 1
```

**Default download location:**
- **Linux/Mac**: `~/Documents/Epstein/`
- **Windows**: `C:\Users\YourName\Documents\Epstein\`

### Configuration

Edit `config.py` to customize:

```python
# Rate limiting (be respectful!)
RATE_LIMIT_DELAY = 1.0  # seconds between requests

# Download settings
DOWNLOAD_PDFS = True    # Set to False for metadata only

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5         # seconds
```

## Output Structure

```
~/Documents/Epstein/            # Or C:\Users\YourName\Documents\Epstein on Windows
├── metadata.json               # Complete metadata with file info
├── data_set_1/
│   ├── documents/              # PDFs, DOCs, TXT
│   │   ├── EFTA00000001.pdf
│   │   ├── EFTA00000002.pdf
│   │   └── ...
│   ├── videos/                 # MP4, MOV, AVI
│   │   └── EFTA00000050.mp4
│   ├── audio/                  # MP3, WAV, M4A
│   │   └── EFTA00000075.mp3
│   ├── images/                 # JPG, PNG, GIF
│   │   └── EFTA00000100.jpg
│   └── archives/               # ZIP, RAR, 7Z
│       └── EFTA00000125.zip
├── data_set_2/
│   └── ...
└── data_set_12/
    └── ...

scrapers/doj-epstein/logs/     # Scraper logs (in scraper directory)
└── scraper_20260206_*.log
```

## Metadata Format

The `metadata.json` file contains structured information:

```json
{
  "data_set_1": [
    {
      "filename": "EFTA00000001.pdf",
      "url": "https://www.justice.gov/epstein/files/DataSet%201/EFTA00000001.pdf",
      "data_set": 1,
      "file_type": ".pdf",
      "category": "documents",
      "file_size_bytes": 2458120,
      "file_size_mb": 2.34
    },
    {
      "filename": "EFTA00000050.mp4",
      "url": "https://www.justice.gov/epstein/files/DataSet%201/EFTA00000050.mp4",
      "data_set": 1,
      "file_type": ".mp4",
      "category": "videos",
      "file_size_bytes": 45821900,
      "file_size_mb": 43.68
    }
  ]
}
```

## Legal & Ethical Considerations

### Important Notes

⚠️ **Content Warning**: These documents may contain sensitive material related to crimes and victims, even with redactions applied.

⚠️ **Age Restriction**: The DOJ site requires users to be 18+ years old.

⚠️ **Respectful Usage**:
- This scraper implements rate limiting to avoid overloading DOJ servers
- The User-Agent identifies itself as a bot for transparency
- Please use this tool responsibly and ethically

⚠️ **Privacy**:
- The DOJ has redacted victim names and identifying information
- Do not attempt to de-anonymize or identify victims
- Report any improperly posted sensitive content to EFTA@usdoj.gov

### Legal Compliance

This scraper is designed for:
- ✅ Academic research
- ✅ Journalism
- ✅ Public interest investigations
- ✅ Data archival

The documents are publicly available, but users should:
- Respect victim privacy
- Comply with terms of use
- Use data responsibly
- Follow ethical research standards

## Technical Details

### Architecture

```
scraper.py
├── DOJEpsteinScraper (main class)
│   ├── get_data_set_urls()       # Find all data set pages
│   ├── scrape_data_set()         # Scrape one data set
│   ├── get_pagination_info()     # Count total pages
│   ├── extract_documents_from_page()  # Parse document links
│   └── download_pdf()            # Download individual files
```

### Rate Limiting

Default: 1 second between requests
- Prevents server overload
- Mimics human browsing patterns
- Configurable in `config.py`

### Error Handling

- Automatic retry with exponential backoff
- Comprehensive logging
- Graceful degradation (continues on errors)
- Resume support (skips existing files)

## Troubleshooting

### Common Issues

**Rate limiting errors (429)**
```python
# Increase delay in config.py
RATE_LIMIT_DELAY = 2.0  # Slower is safer
```

**Timeout errors**
```python
# Increase timeout in config.py
REQUEST_TIMEOUT = 60
```

**Memory issues with large downloads**
- Use `--no-download` to collect metadata first
- Download specific data sets: `--data-sets 1 2`
- The scraper streams large files to avoid memory issues

## Statistics

As of the scraper's design:
- **Data Sets**: 12
- **Example Set 1**: ~3,200 documents (64 pages × 50 per page)
- **Estimated Total**: ~38,000+ documents across all sets
- **File Format**: PDF
- **Naming Pattern**: EFTA[8-digit-number].pdf

## Contributing

Improvements welcome:
- Better metadata extraction
- Document text extraction (OCR/parsing)
- Database integration
- Search functionality
- Analysis tools

## License

This scraper is provided for educational and research purposes. The scraped documents are public records published by the U.S. Department of Justice.

## Contact

For issues with the scraper: [Create an issue]

For improperly posted sensitive content: EFTA@usdoj.gov (DOJ)

## Disclaimer

This tool is for legitimate research and public interest purposes. Users are responsible for complying with all applicable laws and ethical standards when accessing and using these documents.
