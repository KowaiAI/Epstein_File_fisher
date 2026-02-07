"""Configuration for DOJ Epstein Disclosures scraper."""

# Base URLs
BASE_URL = "https://www.justice.gov"
MAIN_PAGE_URL = f"{BASE_URL}/epstein/doj-disclosures"

# Scraping settings
REQUEST_TIMEOUT = 30  # seconds
RATE_LIMIT_DELAY = 2.0  # seconds between requests (slower to avoid detection)
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds

# User agent (appear as regular browser to avoid bot detection)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Output settings (cross-platform defaults)
from pathlib import Path as _Path
OUTPUT_DIR = _Path.home() / "Documents" / "Epstein"  # ~/Documents/Epstein on all platforms
LOGS_DIR = _Path.cwd() / "logs"  # logs directory in current working directory
METADATA_FILE = "metadata.json"
DOWNLOAD_FILES = True  # Set to False to only collect metadata

# Data set configuration
DATA_SETS = list(range(1, 13))  # Data sets 1-12

# Supported file types
SUPPORTED_EXTENSIONS = [
    '.pdf',   # Documents
    '.mp4', '.mov', '.avi', '.wmv', '.flv',  # Video
    '.mp3', '.wav', '.m4a', '.aac', '.ogg',  # Audio
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',  # Images
    '.doc', '.docx', '.txt', '.rtf',  # Text documents
    '.zip', '.rar', '.7z',  # Archives
]

# File naming patterns
FILENAME_PATTERN = r"EFTA\d+"  # Base pattern without extension
