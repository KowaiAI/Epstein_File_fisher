#!/usr/bin/env python3
"""Tests for web scraper module."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import scraper


def test_scraper_init():
    """Test DOJEpsteinScraper initialization."""
    scraper_instance = scraper.DOJEpsteinScraper(download_files=False)
    assert scraper_instance.download_files is False
    assert scraper_instance.session is not None
    assert scraper_instance.output_dir is not None
    assert scraper_instance.logs_dir is not None
    assert scraper_instance.metadata == {}
    print("✓ DOJEpsteinScraper initialization works")


def test_scraper_has_session_headers():
    """Test that scraper sets up proper headers."""
    scraper_instance = scraper.DOJEpsteinScraper(download_files=False)
    headers = scraper_instance.session.headers
    
    assert 'User-Agent' in headers
    assert 'Accept' in headers
    assert 'Accept-Language' in headers
    print("✓ Scraper session headers configured")


def test_scraper_directories_created():
    """Test that scraper creates necessary directories."""
    scraper_instance = scraper.DOJEpsteinScraper(download_files=False)
    
    # Directories should be Path objects
    assert isinstance(scraper_instance.output_dir, Path)
    assert isinstance(scraper_instance.logs_dir, Path)
    
    # Directories should exist after initialization
    assert scraper_instance.output_dir.exists()
    assert scraper_instance.logs_dir.exists()
    print("✓ Scraper creates necessary directories")


def test_scraper_has_required_methods():
    """Test that scraper has all required methods."""
    scraper_instance = scraper.DOJEpsteinScraper(download_files=False)
    
    required_methods = ['_setup_logging']
    for method_name in required_methods:
        assert hasattr(scraper_instance, method_name), f"Missing method: {method_name}"
    
    print("✓ Scraper has required methods")


if __name__ == "__main__":
    test_scraper_init()
    test_scraper_has_session_headers()
    test_scraper_directories_created()
    test_scraper_has_required_methods()
    print("\n✅ All scraper tests passed!")
