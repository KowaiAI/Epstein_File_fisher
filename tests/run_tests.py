#!/usr/bin/env python3
"""Run all tests for the File Fisher project."""

import sys
import subprocess
from pathlib import Path


def run_test_file(test_file):
    """Run a single test file and return the result."""
    print(f"\n{'='*70}")
    print(f"Running {test_file.name}...")
    print('='*70)
    
    result = subprocess.run(
        [sys.executable, str(test_file)],
        capture_output=False,
        cwd=test_file.parent.parent
    )
    
    return result.returncode == 0


def main():
    """Run all tests."""
    tests_dir = Path(__file__).parent
    test_files = sorted(tests_dir.glob('test_*.py'))
    
    if not test_files:
        print("❌ No test files found!")
        return 1
    
    print(f"\nFound {len(test_files)} test file(s)")
    
    results = []
    for test_file in test_files:
        success = run_test_file(test_file)
        results.append((test_file.name, success))
    
    # Summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print('='*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to ship!")
        return 0
    else:
        print(f"\n❌ {total - passed} test suite(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
