#!/usr/bin/env python3
"""
Test runner script for the Flask website.
This script provides an easy way to run all tests with different configurations.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        if e.stdout:
            print("STDOUT:")
            print(e.stdout)
        if e.stderr:
            print("STDERR:")
            print(e.stderr)
        return False


def main():
    """Main test runner function."""
    print("🧪 Flask Website Test Runner")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if pytest is installed
    try:
        subprocess.run(["pytest", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: pytest is not installed. Please install it with: pip install -r requirements.txt")
        sys.exit(1)
    
    # Run different test configurations
    test_configs = [
        ("pytest -v", "All tests with verbose output"),
        ("pytest -v --tb=short", "All tests with short traceback"),
        ("pytest -v -m unit", "Unit tests only"),
        ("pytest -v -m integration", "Integration tests only"),
        ("pytest -v --cov=. --cov-report=term-missing", "All tests with coverage report"),
        ("pytest -v --cov=. --cov-report=html:htmlcov", "All tests with HTML coverage report"),
        ("pytest -v -k 'test_database'", "Database tests only"),
        ("pytest -v -k 'test_projects'", "Project tests only"),
        ("pytest -v -k 'test_app'", "App tests only"),
    ]
    
    success_count = 0
    total_count = len(test_configs)
    
    for command, description in test_configs:
        if run_command(command, description):
            success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Test Summary: {success_count}/{total_count} test configurations passed")
    print('='*60)
    
    if success_count == total_count:
        print("🎉 All test configurations passed!")
        return 0
    else:
        print("⚠️  Some test configurations failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
