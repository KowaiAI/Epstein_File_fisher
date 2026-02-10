#!/usr/bin/env python3
"""Tests for config module."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import config


def test_base_urls():
    """Test that base URLs are properly configured."""
    assert config.BASE_URL == "https://www.justice.gov"
    assert config.MAIN_PAGE_URL == f"{config.BASE_URL}/epstein/doj-disclosures"
    print("✓ Base URLs configured correctly")


def test_request_settings():
    """Test the validity of request configuration settings."""
    assert config.REQUEST_TIMEOUT > 0
    assert config.RATE_LIMIT_DELAY > 0
    assert config.MAX_RETRIES > 0
    assert config.RETRY_DELAY > 0
    print("✓ Request settings valid")


def test_user_agent():
    """Verify that the user agent is properly configured."""
    assert config.USER_AGENT is not None
    assert len(config.USER_AGENT) > 0
    assert "Mozilla" in config.USER_AGENT
    print("✓ User agent configured")


def test_output_directories():
    """Test output directory configuration."""
    assert config.OUTPUT_DIR is not None
    assert isinstance(config.OUTPUT_DIR, Path)
    assert config.LOGS_DIR is not None
    assert isinstance(config.LOGS_DIR, Path)
    print("✓ Output directories configured")


def test_data_sets():
    """Test data set configuration."""
    assert config.DATA_SETS is not None
    assert len(config.DATA_SETS) == 12
    assert config.DATA_SETS == list(range(1, 13))
    print("✓ Data sets configured correctly")


def test_supported_extensions():
    """Test the supported file extensions."""
    assert config.SUPPORTED_EXTENSIONS is not None
    assert len(config.SUPPORTED_EXTENSIONS) > 0
    assert '.pdf' in config.SUPPORTED_EXTENSIONS
    assert '.mp4' in config.SUPPORTED_EXTENSIONS
    print("✓ Supported file extensions configured")


def test_metadata_file():
    """Test metadata file configuration."""
    assert config.METADATA_FILE is not None
    assert config.METADATA_FILE.endswith('.json')
    print("✓ Metadata file configured")


if __name__ == "__main__":
    test_base_urls()
    test_request_settings()
    test_user_agent()
    test_output_directories()
    test_data_sets()
    test_supported_extensions()
    test_metadata_file()
    print("\n✅ All config tests passed!")
