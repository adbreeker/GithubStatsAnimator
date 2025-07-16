"""
Test runner for all GitHub Stats Animator tests.

This script runs all tests in the /tests directory and consolidates results
in /tests/results following the project testing standards.
"""

import asyncio
import os
import sys
from pathlib import Path

# Ensure we can import test modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def run_all_tests():
    """Run all available test suites."""
    print("🧪 GitHub Stats Animator - Full Test Suite")
    print("=" * 60)
    
    # Import and run account general tests
    from tests.test_account_general import main as test_account_general
    from tests.test_views_counter import test_views_counter

    print("Running Account General tests...")
    await test_account_general()

    print("\nRunning Views Counter tests...")
    await test_views_counter()

    print("\n" + "=" * 60)
    print("🏁 All test suites completed!")
    print(f"📁 Check results in: {project_root / 'tests' / 'results'}")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
