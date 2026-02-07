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

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

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
        """Make an HTTP request with retry logic."""
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
        # Look for pagination nav
        """def get_pagination_info(self, soup: BeautifulSoup) -> int:
        Extract total number of pages from pagination controls.  This function searches
        for the pagination navigation in the provided  BeautifulSoup object. It
        identifies the maximum page number by checking  for "Last" buttons and page
        number links. If no pagination is found,  it defaults to returning 1,
        indicating a single page. The function  ensures that the page count is
        accurately derived from the links present.
        
        Args:
            soup: BeautifulSoup object of the page"""
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
                    return int(match.group(1)) + 1  # Pages are 0-indexed

            # Check for page numbers
            text = link.get_text().strip()
            if text.isdigit():
                max_page = max(max_page, int(text))

        return max_page

    def extract_documents_from_page(self, soup: BeautifulSoup, data_set_num: int) -> List[Dict]:
        """Extract document information from a page.
        
        This function retrieves document metadata from a given BeautifulSoup object
        representing a webpage. It identifies all file links, checks their extensions
        against supported types, and categorizes them accordingly. The resulting
        metadata, including filename, URL, dataset number, file type, and category,  is
        collected into a list of dictionaries for further processing.
        
        Args:
            soup: BeautifulSoup object of the page
            data_set_num: Data set number
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
                full_url = urljoin(config.BASE_URL, href)

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
        determining the total number of pages through a request to the data set  URL.
        It then iterates through each page, extracting document metadata  using the
        `extract_documents_from_page` method. The results are logged  for each page,
        and a final count of all documents found is reported.
        
        Args:
            data_set_num (int): Data set number.
            data_set_url (str): URL of the data set page.
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
        # Create category subdirectory
        """Download a file (any supported type).
        
        This function creates a category subdirectory within the specified
        data_set_dir to store the downloaded file. It checks if the file  already
        exists to avoid redundant downloads. If not, it makes a  request to retrieve
        the file, writes it to disk in chunks, and logs  the download progress.
        Additionally, it updates the document metadata  with the file size in both
        bytes and megabytes.
        
        Args:
            doc: Document metadata dictionary.
            data_set_dir: Directory to save the file.
        """
        category_dir = data_set_dir / doc["category"]
        category_dir.mkdir(exist_ok=True, parents=True)

        file_path = category_dir / doc["filename"]

        # Skip if already downloaded
        if file_path.exists():
            self.logger.debug(f"Already exists: {doc['filename']}")
            return True

        response = self._make_request(doc["url"], stream=True)
        if not response:
            return False

        try:
            # Get file size if available
            total_size = int(response.headers.get('content-length', 0))

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
        
        This method initiates the scraping of DOJ Epstein Disclosures by first
        retrieving all relevant data set URLs. If no data sets are found, it logs  an
        error and exits. For each data set, it scrapes the metadata and, if  file
        downloading is enabled, creates a directory for the data set and  downloads the
        associated files while logging the progress and success  count. Finally, it
        saves the metadata after the scraping process is  complete.
        """
        self.logger.info("Starting DOJ Epstein Disclosures scraper")

        # Get all data set URLs
        data_set_urls = self.get_data_set_urls()
        if not data_set_urls:
            self.logger.error("No data sets found. Exiting.")
            return

        # Scrape each data set
        for data_set_num in sorted(data_set_urls.keys()):
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
        """Save collected metadata to a JSON file."""
        metadata_path = self.output_dir / config.METADATA_FILE

        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

        self.logger.info(f"Metadata saved to {metadata_path}")

        # Print summary
        total_docs = sum(len(docs) for docs in self.metadata.values())
        self.logger.info(f"Total documents found: {total_docs}")


def main():
    """Main entry point."""
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
        help="Specific data sets to scrape (default: all)"
    )

    args = parser.parse_args()

    # Override config if specific data sets requested
    if args.data_sets:
        config.DATA_SETS = args.data_sets

    # Override output directory if specified
    if args.output_dir:
        config.OUTPUT_DIR = Path(args.output_dir)

    scraper = DOJEpsteinScraper(download_files=not args.no_download)
    scraper.run()


if __name__ == "__main__":
    main()
