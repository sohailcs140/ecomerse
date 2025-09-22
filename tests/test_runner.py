"""
Custom test runner utilities and helpers.
"""

import os
import django
from django.conf import settings
from django.test.utils import get_runner


def setup_test_environment():
    """Set up the Django test environment."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings.development')
    django.setup()


def run_tests(test_labels=None, verbosity=1, interactive=True, failfast=False, keepdb=False):
    """Run tests using Django's test runner."""
    setup_test_environment()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=verbosity,
        interactive=interactive,
        failfast=failfast,
        keepdb=keepdb
    )
    
    if test_labels is None:
        test_labels = ['tests']
    
    failures = test_runner.run_tests(test_labels)
    return failures


if __name__ == '__main__':
    import sys
    
    # Parse command line arguments
    test_labels = sys.argv[1:] if len(sys.argv) > 1 else None
    
    failures = run_tests(
        test_labels=test_labels,
        verbosity=2,
        failfast=True
    )
    
    if failures:
        sys.exit(1)
