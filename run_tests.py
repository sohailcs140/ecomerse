#!/usr/bin/env python
"""
Test runner script for the ecommerce API.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py tests.unit         # Run unit tests only
    python run_tests.py tests.api          # Run API tests only
    python run_tests.py tests.integration  # Run integration tests only
    python run_tests.py --coverage         # Run tests with coverage
    python run_tests.py --fast             # Run tests without migrations
"""

import os
import sys
import subprocess
import argparse


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{description}")
    print("=" * 50)
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print(f"Error: {result.stderr}", file=sys.stderr)
    
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description='Run ecommerce API tests')
    parser.add_argument('test_path', nargs='?', default='tests', 
                       help='Specific test path to run (default: tests)')
    parser.add_argument('--coverage', action='store_true', 
                       help='Run tests with coverage report')
    parser.add_argument('--fast', action='store_true', 
                       help='Run tests without creating test database')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Verbose output')
    parser.add_argument('--failfast', '-f', action='store_true', 
                       help='Stop on first failure')
    
    args = parser.parse_args()
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings.development')
    
    # Build test command
    if args.coverage:
        # Use pytest with coverage
        cmd = f"pytest {args.test_path}"
        if args.verbose:
            cmd += " -v"
        if args.failfast:
            cmd += " -x"
    else:
        # Use Django's test runner
        cmd = f"python manage.py test {args.test_path}"
        if args.verbose:
            cmd += " --verbosity=2"
        if args.failfast:
            cmd += " --failfast"
        if args.fast:
            cmd += " --keepdb"
    
    # Run the tests
    success = run_command(cmd, f"Running tests: {args.test_path}")
    
    if not success:
        print("\n❌ Tests failed!")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")


if __name__ == '__main__':
    main()
