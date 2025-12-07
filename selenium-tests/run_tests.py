#!/usr/bin/env python3
"""
Selenium Test Runner for MERN Memories
Run: python run_tests.py
"""

import pytest
import sys
import os

def main():
    """Main test runner"""
    print("\n" + "="*70)
    print("MERN MEMORIES - SELENIUM TEST SUITE")
    print("="*70)
    
    # Test arguments
    args = [
        "tests/",                    # Test directory
        "-v",                        # Verbose output
        "--html=test_report.html",   # HTML report
        "--self-contained-html",     # Single file HTML
        "--capture=tee-sys",         # Capture and display output
        "--tb=short",                # Short traceback
    ]
    
    print(f"\nRunning tests with arguments: {args}")
    print("-"*70 + "\n")
    
    # Run tests
    exit_code = pytest.main(args)
    
    print("\n" + "="*70)
    print(f"TEST EXECUTION COMPLETE")
    print(f"Exit Code: {exit_code}")
    
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Some tests failed")
    
    print("="*70)
    
    # Generate report message
    if os.path.exists("test_report.html"):
        print(f"\n📊 Test report generated: test_report.html")
        print("Open the report in your browser to view detailed results")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())