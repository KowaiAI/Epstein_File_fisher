#!/usr/bin/env python3
"""
░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄
░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀
░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀

CSV-Based DOJ Epstein Files Downloader

Uses a CSV file with direct download links to bypass bot detection.
Much more reliable than web scraping!
"""

import csv
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List

try:
    import requests
    from tqdm import tqdm
except ImportError as e:
    print("\n" + "="*70)
    print("❌ ERROR: Missing required dependencies!")
    print("="*70)
    print(f"\nMissing module: {e.name}")
    print("\nPlease install dependencies first:")
    print("     pip install requests tqdm")
    print("\n" + "="*70 + "\n")
    sys.exit(1)

import config


class CSVDownloader:
    """Download files from CSV link list."""

    def __init__(self, csv_path: str, download_files: bool = True):
        """
        Initialize downloader.

        Args:
            csv_path: Path to CSV file with download links
            download_files: Whether to download files
        """
        self.csv_path = Path(csv_path)
        self.download_files = download_files

        # Setup directories
        self.output_dir = Path(config.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True, parents=True)

        self.logs_dir = Path(config.LOGS_DIR)
        self.logs_dir.mkdir(exist_ok=True, parents=True)

        # Setup logging
        self._setup_logging()

        # Setup session
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": config.USER_AGENT,
        })

        # Storage
        self.files_by_dataset: Dict[int, List[Dict]] = {}
        self.metadata: Dict[str, List[Dict]] = {}

    def _setup_logging(self):
        """Configure logging."""
        log_file = self.logs_dir / f"csv_downloader_{time.strftime('%Y%m%d_%H%M%S')}.log"

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

    def load_csv(self):
        """Load CSV file and organize files by data set."""
        self.logger.info(f"Loading CSV: {self.csv_path}")

        if not self.csv_path.exists():
            self.logger.error(f"CSV file not found: {self.csv_path}")
            return False

        try:
            with open(self.csv_path, 'r') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    try:
                        data_set = int(row['data_set'])
                        url = row['url']
                        filename = row['link_text']

                        # Determine file category
                        file_ext = Path(filename).suffix.lower()
                        if file_ext in ['.pdf', '.doc', '.docx', '.txt']:
                            category = 'documents'
                        elif file_ext in ['.mp4', '.mov', '.avi']:
                            category = 'videos'
                        elif file_ext in ['.mp3', '.wav', '.m4a']:
                            category = 'audio'
                        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                            category = 'images'
                        elif file_ext in ['.zip', '.rar', '.7z']:
                            category = 'archives'
                        else:
                            category = 'other'

                        file_info = {
                            'filename': filename,
                            'url': url,
                            'data_set': data_set,
                            'file_type': file_ext,
                            'category': category
                        }

                        if data_set not in self.files_by_dataset:
                            self.files_by_dataset[data_set] = []

                        self.files_by_dataset[data_set].append(file_info)

                    except (KeyError, ValueError) as e:
                        self.logger.warning(f"Skipping invalid row: {e}")
                        continue

            # Log statistics
            total_files = sum(len(files) for files in self.files_by_dataset.values())
            self.logger.info(f"Loaded {total_files} files across {len(self.files_by_dataset)} data sets")

            for ds_num in sorted(self.files_by_dataset.keys()):
                count = len(self.files_by_dataset[ds_num])
                self.logger.info(f"  Data Set {ds_num}: {count} files")

            return True

        except Exception as e:
            self.logger.error(f"Failed to load CSV: {e}")
            return False

    def download_file(self, file_info: Dict, data_set_dir: Path) -> bool:
        """Download a single file."""
        category_dir = data_set_dir / file_info['category']
        category_dir.mkdir(exist_ok=True, parents=True)

        file_path = category_dir / file_info['filename']

        # Skip if exists
        if file_path.exists():
            self.logger.debug(f"Already exists: {file_info['filename']}")
            return True

        # Download
        try:
            time.sleep(config.RATE_LIMIT_DELAY)
            response = self.session.get(file_info['url'], timeout=30, stream=True)
            response.raise_for_status()

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Get file size
            file_size = file_path.stat().st_size
            file_info['file_size_bytes'] = file_size
            file_info['file_size_mb'] = round(file_size / (1024 * 1024), 2)

            self.logger.debug(f"Downloaded: {file_info['filename']} ({file_info['file_size_mb']} MB)")
            return True

        except Exception as e:
            self.logger.error(f"Failed to download {file_info['filename']}: {e}")
            if file_path.exists():
                file_path.unlink()
            return False

    def download_data_sets(self, data_set_numbers: List[int]):
        """Download selected data sets."""
        for ds_num in sorted(data_set_numbers):
            if ds_num not in self.files_by_dataset:
                self.logger.warning(f"Data Set {ds_num} not found in CSV")
                continue

            files = self.files_by_dataset[ds_num]
            self.logger.info(f"Downloading Data Set {ds_num} ({len(files)} files)")

            if not self.download_files:
                self.metadata[f"data_set_{ds_num}"] = files
                self.logger.info(f"Data Set {ds_num}: Metadata collected (no download)")
                continue

            # Download files
            data_set_dir = self.output_dir / f"data_set_{ds_num}"
            data_set_dir.mkdir(exist_ok=True, parents=True)

            success_count = 0
            for file_info in tqdm(files, desc=f"Data Set {ds_num}"):
                if self.download_file(file_info, data_set_dir):
                    success_count += 1

            self.logger.info(f"Data Set {ds_num}: Downloaded {success_count}/{len(files)} files")
            self.metadata[f"data_set_{ds_num}"] = files

    def save_metadata(self):
        """Save metadata to JSON."""
        metadata_path = self.output_dir / config.METADATA_FILE

        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)

        self.logger.info(f"Metadata saved to {metadata_path}")

        total_files = sum(len(files) for files in self.metadata.values())
        self.logger.info(f"Total files processed: {total_files}")


def interactive_menu(available_datasets: List[int]):
    """Interactive menu for selecting data sets."""
    print("\n" + "="*70)
    print("░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄")
    print("░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀")
    print("░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀")
    print("="*70)
    print("\nDOJ Epstein Disclosures - CSV Downloader (Fast & Reliable!)\n")
    print("="*70)

    print("\nAvailable Data Sets:")
    print("-" * 70)
    for ds_num in sorted(available_datasets):
        print(f"  [{ds_num:2d}] Data Set {ds_num}")
    print()
    print("  [99] Download ALL data sets")
    print("  [ 0] Exit without downloading")
    print("-" * 70)

    while True:
        try:
            choice = input("\nEnter your choice (0-12, or 99 for all): ").strip()

            if choice == "0":
                print("\n✓ Exiting. Goodbye!")
                return None

            elif choice == "99":
                confirm = input("\n⚠️  Download ALL data sets? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    return available_datasets
                continue

            elif choice.isdigit() and int(choice) in available_datasets:
                selected = [int(choice)]
                print(f"\n✓ Selected: Data Set {choice}")

                more = input("Add another data set? (yes/no): ").strip().lower()
                if more in ['yes', 'y']:
                    while True:
                        additional = input(f"Enter data set number or 'done': ").strip()
                        if additional.lower() == 'done':
                            break
                        if additional.isdigit() and int(additional) in available_datasets:
                            num = int(additional)
                            if num not in selected:
                                selected.append(num)
                                print(f"✓ Added Data Set {num}")
                        else:
                            print("⚠️  Invalid choice")
                return sorted(selected)
            else:
                print("⚠️  Invalid choice")

        except KeyboardInterrupt:
            print("\n\n✓ Cancelled. Goodbye!")
            return None


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Download DOJ Epstein files from CSV"
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default="/home/hibiscus/Downloads/master_file_links.csv",
        help="Path to CSV file with download links"
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Only collect metadata"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help=f"Output directory (default: {config.OUTPUT_DIR})"
    )
    parser.add_argument(
        "--data-sets",
        type=int,
        nargs="+",
        help="Specific data sets to download"
    )

    args = parser.parse_args()

    # Override output dir if specified
    if args.output_dir:
        config.OUTPUT_DIR = Path(args.output_dir)

    # Create downloader
    downloader = CSVDownloader(args.csv_file, download_files=not args.no_download)

    # Load CSV
    if not downloader.load_csv():
        print("❌ Failed to load CSV file")
        return

    # Get available datasets
    available = sorted(downloader.files_by_dataset.keys())

    # Determine which data sets to download
    if args.data_sets:
        selected = args.data_sets
    elif sys.stdin.isatty():
        selected = interactive_menu(available)
        if selected is None:
            return
    else:
        selected = available

    print(f"\n{'='*70}")
    print(f"Download Configuration:")
    print(f"  Data Sets: {selected}")
    print(f"  Output Directory: {config.OUTPUT_DIR}")
    print(f"  Download Files: {not args.no_download}")
    print(f"{'='*70}\n")

    # Download
    downloader.download_data_sets(selected)
    downloader.save_metadata()

    print(f"\n{'='*70}")
    print("✅ Download complete!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
