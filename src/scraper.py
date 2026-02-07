#!/usr/bin/env python3
"""
░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄
░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀
░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀

DOJ Epstein Disclosures Web Scraper

Scrapes documents from the Department of Justice's Epstein Files Transparency Act
disclosure portal at https://www.justice.gov/epstein/doj-disclosures

Features:
- Multi-page pagination handling
- Multi-format support (PDF, MP4, MP3, JPG, ZIP, etc.)
- Rate limiting and retry logic
- Metadata collection
- File downloads with resume support
- Progress tracking
- Comprehensive logging
"""

import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

# Check for required dependencies
try:
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm
except ImportError as e:
    print("\n" + "="*70)
    print("❌ ERROR: Missing required dependencies!")
    print("="*70)
    print(f"\nMissing module: {e.name}")
    print("\nPlease install dependencies first:")
    print("\n  1. Create virtual environment:")
    print("     python3 -m venv venv")
    print("\n  2. Activate it:")
    print("     source venv/bin/activate  (Mac/Linux)")
    print("     venv\\Scripts\\activate     (Windows)")
    print("\n  3. Install dependencies:")
    print("     pip install -r requirements.txt")
    print("\n" + "="*70 + "\n")
    sys.exit(1)

import config


class DOJEpsteinScraper:
    """Scraper for DOJ Epstein disclosure documents."""

    def __init__(self, download_files: bool = True):
        """
        Initialize the scraper.

        Args:
            download_files: Whether to download files (vs. metadata only)
        """
        self.download_files = download_files
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": config.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        })

        # Setup directories
        self.output_dir = Path(config.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True, parents=True)

        self.logs_dir = Path(config.LOGS_DIR)
        self.logs_dir.mkdir(exist_ok=True, parents=True)

        # Setup logging
        self._setup_logging()

        # Metadata storage
        self.metadata: Dict[str, List[Dict]] = {}

    def _setup_logging(self):
        """Configure logging to file and console."""
        log_file = self.logs_dir / f"scraper_{time.strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Logging to {log_file}")

    def _make_request(self, url: str, stream: bool = False) -> Optional[requests.Response]:
        """
        Make HTTP request with retry logic.

        Args:
            url: URL to fetch
            stream: Whether to stream the response (for large files)

        Returns:
            Response object or None if failed
        """
        for attempt in range(config.MAX_RETRIES):
            try:
                time.sleep(config.RATE_LIMIT_DELAY)
                response = self.session.get(
                    url,
                    timeout=config.REQUEST_TIMEOUT,
                    stream=stream
                )
                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                self.logger.warning(
                    f"Request failed (attempt {attempt + 1}/{config.MAX_RETRIES}): {e}"
                )
                if attempt < config.MAX_RETRIES - 1:
                    time.sleep(config.RETRY_DELAY)
                else:
                    self.logger.error(f"Failed to fetch {url} after {config.MAX_RETRIES} attempts")
                    return None

    def get_data_set_urls(self) -> Dict[int, str]:
        """Get URLs for all data set pages."""
        self.logger.info(f"Fetching main page: {config.MAIN_PAGE_URL}")
        response = self._make_request(config.MAIN_PAGE_URL)

        if not response:
            self.logger.error("Failed to fetch main page")
            return {}

        soup = BeautifulSoup(response.text, "lxml")
        data_set_urls = {}

        # Find all data set links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            match = re.search(r"data-set-(\d+)-files", href)
            if match:
                data_set_num = int(match.group(1))
                full_url = urljoin(config.BASE_URL, href)
                data_set_urls[data_set_num] = full_url
                self.logger.info(f"Found Data Set {data_set_num}: {full_url}")

        return data_set_urls

    def get_pagination_info(self, soup: BeautifulSoup) -> int:
        """Extract total number of pages from pagination controls.
        
        This function analyzes the pagination navigation in a BeautifulSoup object to
        determine the total number of pages available. It first checks for the
        presence of a pagination nav element. If found, it retrieves all page links
        and identifies the maximum page number by examining both the "Last" button and
        individual page numbers. The function returns the total number of pages based
        on the extracted information.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            int: Total number of pages (1 if no pagination found)
        """
        # Look for pagination nav
        pagination = soup.find("nav", {"aria-label": "Pagination"})
        if not pagination:
            return 1

        # Find all page links
        page_links = pagination.find_all("a")
        max_page = 1

        for link in page_links:
            # Check for "Last" button
            if "Last" in link.get_text():
                href = link.get("href", "")
                match = re.search(r"[?&]page=(\d+)", href)
                if match:
                    # Return page number + 1 (pages in URL are 0-indexed, but we count from 1)
                    return int(match.group(1)) + 1

            # Check for page numbers
            text = link.get_text().strip()
            if text.isdigit():
                max_page = max(max_page, int(text))

        return max_page

    def extract_documents_from_page(self, soup: BeautifulSoup, data_set_num: int) -> List[Dict]:
        """Extract document information from a page.
        
        This function retrieves document metadata from a given BeautifulSoup object
        representing a web page. It identifies all file links, checks their extensions
        against a set of supported types, and categorizes them accordingly. The
        resulting metadata, including filename, URL, dataset number, file type, and
        category, is collected into a list of dictionaries for further processing.
        
        Args:
            soup: BeautifulSoup object of the page
            data_set_num: Data set number
            
        Returns:
            List[Dict]: List of document metadata dictionaries
        """
        documents = []

        # Find all file links
        for link in soup.find_all("a", href=True):
            href = link["href"]

            # Get file extension
            parsed_path = urlparse(href).path
            file_ext = Path(parsed_path).suffix.lower()

            # Check if it's a supported file type with EFTA pattern
            if file_ext in config.SUPPORTED_EXTENSIONS and re.search(config.FILENAME_PATTERN, href, re.IGNORECASE):
                filename = Path(parsed_path).name
                
                # Validate and construct full URL
                try:
                    full_url = urljoin(config.BASE_URL, href)
                    # Basic URL validation
                    parsed_url = urlparse(full_url)
                    if not parsed_url.scheme or not parsed_url.netloc:
                        self.logger.warning(f"Invalid URL constructed: {full_url}")
                        continue
                except Exception as e:
                    self.logger.warning(f"Failed to construct URL from {href}: {e}")
                    continue

                # Determine file category
                if file_ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf']:
                    category = 'documents'
                elif file_ext in ['.mp4', '.mov', '.avi', '.wmv', '.flv']:
                    category = 'videos'
                elif file_ext in ['.mp3', '.wav', '.m4a', '.aac', '.ogg']:
                    category = 'audio'
                elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
                    category = 'images'
                elif file_ext in ['.zip', '.rar', '.7z']:
                    category = 'archives'
                else:
                    category = 'other'

                doc_info = {
                    "filename": filename,
                    "url": full_url,
                    "data_set": data_set_num,
                    "file_type": file_ext,
                    "category": category,
                }

                documents.append(doc_info)

        return documents

    def scrape_data_set(self, data_set_num: int, data_set_url: str) -> List[Dict]:
        """Scrape all documents from a data set.
        
        This function retrieves all documents from a specified data set by first
        determining the total number of pages through a request to the data set URL.
        It then iterates through each page, extracting document metadata using the
        `extract_documents_from_page` method. The results are logged for each page,
        and a comprehensive list of all documents is returned at the end.
        
        Args:
            data_set_num: Data set number.
            data_set_url: URL of the data set page.
            
        Returns:
            List[Dict]: List of all document metadata from the data set
        """
        self.logger.info(f"Scraping Data Set {data_set_num}")

        # Get first page to determine pagination
        response = self._make_request(data_set_url)
        if not response:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        total_pages = self.get_pagination_info(soup)
        self.logger.info(f"Data Set {data_set_num} has {total_pages} pages")

        all_documents = []

        # Scrape all pages
        for page_num in tqdm(range(total_pages), desc=f"Data Set {data_set_num}"):
            if page_num == 0:
                page_soup = soup  # Already have first page
            else:
                page_url = f"{data_set_url}?page={page_num}"
                page_response = self._make_request(page_url)
                if not page_response:
                    continue
                page_soup = BeautifulSoup(page_response.text, "lxml")

            documents = self.extract_documents_from_page(page_soup, data_set_num)
            all_documents.extend(documents)
            self.logger.debug(f"Page {page_num + 1}: Found {len(documents)} documents")

        self.logger.info(f"Data Set {data_set_num}: Found {len(all_documents)} total documents")
        return all_documents

    def download_file(self, doc: Dict, data_set_dir: Path) -> bool:
        """Download a file (any supported type).
        
        This function creates a category subdirectory within the specified
        data_set_dir to store the downloaded file. It checks if the file already
        exists to avoid redundant downloads. If not, it makes a request to the
        provided URL, streams the content, and saves it to the designated path. The
        function also logs the download progress and updates the document metadata
        with the file size.
        
        Args:
            doc: Document metadata dictionary containing 'category',
                'filename', and 'url'.
            data_set_dir: Directory to save the file.
            
        Returns:
            bool: True if download was successful, False otherwise.
        """
        # Create category subdirectory
        category_dir = data_set_dir / doc["category"]
        category_dir.mkdir(exist_ok=True, parents=True)

        file_path = category_dir / doc["filename"]

        # Skip if already downloaded
        if file_path.exists():
            self.logger.debug(f"Already exists: {doc['filename']}")
            return True

        response = self._make_request(doc["url"], stream=True)
        if not response:
            self.logger.error(f"Failed to download {doc['filename']}: request failed")
            return False

        try:
            # Get file size if available (validate header value)
            try:
                total_size = int(response.headers.get('content-length', 0))
            except (ValueError, TypeError):
                total_size = 0
                self.logger.debug(f"Could not parse content-length header for {doc['filename']}")

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Log file size
            file_size = file_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            self.logger.debug(f"Downloaded: {doc['filename']} ({size_mb:.2f} MB)")

            # Add file size to metadata
            doc['file_size_bytes'] = file_size
            doc['file_size_mb'] = round(size_mb, 2)

            return True

        except Exception as e:
            self.logger.error(f"Failed to save {doc['filename']}: {e}")
            if file_path.exists():
                file_path.unlink()
            return False

    def run(self):
        """Run the complete scraping process.
        
        This method initiates the scraping process for the DOJ Epstein Disclosures. It
        retrieves all relevant data set URLs and iterates through the selected data
        sets, scraping metadata and downloading files if enabled. The function also
        logs the progress and any issues encountered during the process, including
        missing data sets and the types of files found.
        """
        self.logger.info("Starting DOJ Epstein Disclosures scraper")

        # Get all data set URLs
        data_set_urls = self.get_data_set_urls()
        if not data_set_urls:
            self.logger.error("No data sets found or failed to retrieve data set URLs. Exiting.")
            return

        # Scrape only the selected data sets
        for data_set_num in sorted(config.DATA_SETS):
            if data_set_num not in data_set_urls:
                self.logger.warning(f"Data Set {data_set_num} not found on website")
                continue

            data_set_url = data_set_urls[data_set_num]

            # Scrape metadata
            documents = self.scrape_data_set(data_set_num, data_set_url)
            self.metadata[f"data_set_{data_set_num}"] = documents

            # Download files if enabled
            if self.download_files and documents:
                data_set_dir = self.output_dir / f"data_set_{data_set_num}"
                data_set_dir.mkdir(exist_ok=True, parents=True)

                self.logger.info(f"Downloading files for Data Set {data_set_num}")
                download_success_count = 0

                # Count files by type
                file_types = {}
                for doc in documents:
                    file_types[doc['category']] = file_types.get(doc['category'], 0) + 1

                self.logger.info(f"File types found: {file_types}")

                for doc in tqdm(documents, desc=f"Downloading Set {data_set_num}"):
                    # Download file
                    if self.download_file(doc, data_set_dir):
                        download_success_count += 1

                self.logger.info(
                    f"Data Set {data_set_num}: Downloaded {download_success_count}/{len(documents)} files"
                )

        # Save metadata
        self._save_metadata()
        self.logger.info("Scraping complete!")

    def _save_metadata(self):
        """Save collected metadata to JSON file."""
        metadata_path = self.output_dir / config.METADATA_FILE

        try:
            with open(metadata_path, "w", encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2)

            self.logger.info(f"Metadata saved to {metadata_path}")

            # Print summary
            total_docs = sum(len(docs) for docs in self.metadata.values())
            self.logger.info(f"Total documents found: {total_docs}")
        except (IOError, OSError) as e:
            self.logger.error(f"Failed to save metadata to {metadata_path}: {e}")


def interactive_menu():
    """Interactive menu for selecting data sets."""
    print("\n" + "="*70)
    print("░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄")
    print("░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀")
    print("░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀")
    print("="*70)
    print("\nDOJ Epstein Disclosures - Interactive Download Menu\n")
    print("="*70)

    # Show data set options
    print("\nAvailable Data Sets:")
    print("-" * 70)
    for i in range(1, 13):
        print(f"  [{i:2d}] Data Set {i}")
    print()
    print("  [99] Download ALL data sets (1-12)")
    print("  [ 0] Exit without downloading")
    print("-" * 70)

    while True:
        try:
            choice = input("\nEnter your choice (0-12, or 99 for all): ").strip()

            if choice == "0":
                print("\n✓ Exiting without downloading. Goodbye!")
                return None

            elif choice == "99":
                confirm = input("\n⚠️  Download ALL 12 data sets? This may take several hours! (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    return list(range(1, 13))
                else:
                    print("Cancelled. Please choose again.")
                    continue

            elif choice.isdigit() and 1 <= int(choice) <= 12:
                data_set = int(choice)
                print(f"\n✓ Selected: Data Set {data_set}")

                # Ask if they want to add more
                more = input("Add another data set? (yes/no): ").strip().lower()
                if more in ['yes', 'y']:
                    selected = [data_set]
                    while True:
                        additional = input(f"Enter another data set number (1-12), or 'done' to finish: ").strip()
                        if additional.lower() == 'done':
                            break
                        if additional.isdigit() and 1 <= int(additional) <= 12:
                            num = int(additional)
                            if num not in selected:
                                selected.append(num)
                                print(f"✓ Added Data Set {num}")
                            else:
                                print(f"⚠️  Data Set {num} already selected")
                        else:
                            print("⚠️  Invalid choice. Enter a number 1-12 or 'done'")
                    return sorted(selected)
                else:
                    return [data_set]

            else:
                print("⚠️  Invalid choice. Please enter a number between 0-12, or 99 for all.")

        except KeyboardInterrupt:
            print("\n\n✓ Cancelled by user. Goodbye!")
            return None
        except Exception as e:
            print(f"⚠️  Error: {e}")


def main():
    """Main entry point for scraping DOJ Epstein disclosure documents.
    
    This function sets up the command-line interface using argparse, allowing users
    to specify options such as whether to download files, the output directory, and
    specific data sets to scrape. It handles both interactive and non-interactive
    modes for selecting data sets and confirms large downloads before proceeding.
    The function then initializes the DOJEpsteinScraper with the specified options
    and starts the scraping process.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Scrape DOJ Epstein disclosure documents"
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Only collect metadata, don't download files"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help=f"Output directory for downloads (default: {config.OUTPUT_DIR})"
    )
    parser.add_argument(
        "--data-sets",
        type=int,
        nargs="+",
        help="Specific data sets to scrape (default: interactive menu)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Use interactive menu to select data sets"
    )

    args = parser.parse_args()

    # Override output directory if specified (use local variable to avoid mutating config)
    output_dir = Path(args.output_dir) if args.output_dir else config.OUTPUT_DIR

    # Determine which data sets to download
    data_sets_to_scrape = []
    if args.data_sets:
        # Command line arguments provided
        data_sets_to_scrape = args.data_sets
    elif args.interactive or (not args.data_sets and sys.stdin.isatty()):
        # Interactive mode (default when run without arguments)
        selected_sets = interactive_menu()
        if selected_sets is None:
            return  # User cancelled
        data_sets_to_scrape = selected_sets
    else:
        # Non-interactive (all sets) - for scripts/automation
        data_sets_to_scrape = list(range(1, 13))

    print(f"\n{'='*70}")
    print(f"Download Configuration:")
    print(f"  Data Sets: {data_sets_to_scrape}")
    print(f"  Output Directory: {output_dir}")
    print(f"  Download Files: {not args.no_download}")
    print(f"{'='*70}\n")

    # Final confirmation for large downloads
    if len(data_sets_to_scrape) > 3 and not args.no_download:
        try:
            confirm = input("⚠️  You're about to download multiple data sets. Continue? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("\n✓ Download cancelled. Goodbye!")
                return
        except KeyboardInterrupt:
            print("\n\n✓ Cancelled by user. Goodbye!")
            return

    scraper = DOJEpsteinScraper(download_files=not args.no_download)
    
    # Override output directory if specified
    if args.output_dir:
        scraper.output_dir = output_dir
    
    # Set data sets to scrape by directly using the local variable
    # Store in config for backward compatibility with scraper.run() 
    config.DATA_SETS = data_sets_to_scrape
    
    scraper.run()


if __name__ == "__main__":
    main()
