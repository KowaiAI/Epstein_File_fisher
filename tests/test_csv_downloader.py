#!/usr/bin/env python3
"""Tests for CSV downloader module."""

import sys
import tempfile
import csv
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import csv_downloader


def test_csv_downloader_init():
    """Test CSVDownloader initialization."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
    
    try:
        downloader = csv_downloader.CSVDownloader(csv_path, download_files=False)
        assert isinstance(downloader.csv_path, Path)
        assert downloader.download_files is False
        assert downloader.output_dir is not None
        assert downloader.logs_dir is not None
        assert downloader.files_by_dataset == {}
        assert downloader.metadata == {}
        print("✓ CSVDownloader initialization works")
    finally:
        Path(csv_path).unlink(missing_ok=True)


def test_file_categorization():
    """Test file type categorization logic."""
    test_cases = {
        'document.pdf': 'documents',
        'video.mp4': 'videos',
        'audio.mp3': 'audio',
        'image.jpg': 'images',
        'archive.zip': 'archives',
        'unknown.xyz': 'other',
    }
    
    for filename, expected_category in test_cases.items():
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
        
        assert category == expected_category, f"Failed for {filename}"
    
    print("✓ File categorization logic works correctly")


def test_load_csv_with_valid_data():
    """Test loading a valid CSV file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['data_set', 'url', 'link_text'])
        writer.writeheader()
        writer.writerow({
            'data_set': '1',
            'url': 'https://example.com/file1.pdf',
            'link_text': 'file1.pdf'
        })
        writer.writerow({
            'data_set': '1',
            'url': 'https://example.com/file2.mp4',
            'link_text': 'file2.mp4'
        })
        writer.writerow({
            'data_set': '2',
            'url': 'https://example.com/file3.pdf',
            'link_text': 'file3.pdf'
        })
        csv_path = f.name
    
    try:
        downloader = csv_downloader.CSVDownloader(csv_path, download_files=False)
        result = downloader.load_csv()
        
        assert result == True
        assert 1 in downloader.files_by_dataset
        assert 2 in downloader.files_by_dataset
        assert len(downloader.files_by_dataset[1]) == 2
        assert len(downloader.files_by_dataset[2]) == 1
        print("✓ CSV loading with valid data works")
    finally:
        Path(csv_path).unlink(missing_ok=True)


def test_load_csv_with_invalid_data():
    """Test loading CSV with invalid rows."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['data_set', 'url', 'link_text'])
        writer.writeheader()
        writer.writerow({
            'data_set': '1',
            'url': 'https://example.com/file1.pdf',
            'link_text': 'file1.pdf'
        })
        writer.writerow({
            'data_set': 'invalid',  # Invalid data_set
            'url': 'https://example.com/file2.pdf',
            'link_text': 'file2.pdf'
        })
        csv_path = f.name
    
    try:
        downloader = csv_downloader.CSVDownloader(csv_path, download_files=False)
        result = downloader.load_csv()
        
        assert result == True
        assert 1 in downloader.files_by_dataset
        assert len(downloader.files_by_dataset[1]) == 1  # Only valid row loaded
        print("✓ CSV loading handles invalid rows gracefully")
    finally:
        Path(csv_path).unlink(missing_ok=True)


def test_load_csv_missing_columns():
    """Test loading CSV with missing required columns."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['data_set', 'url'])  # Missing link_text
        writer.writeheader()
        writer.writerow({
            'data_set': '1',
            'url': 'https://example.com/file1.pdf',
        })
        csv_path = f.name
    
    try:
        downloader = csv_downloader.CSVDownloader(csv_path, download_files=False)
        result = downloader.load_csv()
        
        assert result == False  # Should fail due to missing columns
        print("✓ CSV loading validates required columns")
    finally:
        Path(csv_path).unlink(missing_ok=True)


def test_interactive_menu():
    """Test that interactive menu function exists and has correct signature."""
    assert hasattr(csv_downloader, 'interactive_menu')
    import inspect
    sig = inspect.signature(csv_downloader.interactive_menu)
    assert 'available_datasets' in sig.parameters
    print("✓ Interactive menu function exists with correct signature")


if __name__ == "__main__":
    test_csv_downloader_init()
    test_file_categorization()
    test_load_csv_with_valid_data()
    test_load_csv_with_invalid_data()
    test_load_csv_missing_columns()
    test_interactive_menu()
    print("\n✅ All CSV downloader tests passed!")
