#!/usr/bin/env python3
"""
Test runner for ChromaDB metadata filtering functionality.
Executes all metadata filtering tests and provides a comprehensive report.
"""

import sys
import os
import time
from typing import List, Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.tests.test_chroma_metadata_filtering import (
    test_basic_metadata_filtering,
    test_cross_article_contamination_prevention,
    test_complex_metadata_filtering,
    test_metadata_filtering_performance,
    test_metadata_filtering_edge_cases,
    test_metadata_filtering_integration
)

def run_test_with_timing(test_func, test_name: str) -> Dict[str, Any]:
    """Run a test function and capture timing and results."""
    print(f"\n{'='*80}")
    print(f"RUNNING TEST: {test_name}")
    print(f"{'='*80}")
    
    start_time = time.time()
    success = False
    error_message = None
    
    try:
        test_func()
        success = True
        print(f"\n✅ {test_name} PASSED")
    except Exception as e:
        error_message = str(e)
        print(f"\n❌ {test_name} FAILED: {error_message}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    return {
        "name": test_name,
        "success": success,
        "duration": duration,
        "error": error_message
    }

def print_test_summary(results: List[Dict[str, Any]]):
    """Print a summary of all test results."""
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results if result['success'])
    failed_tests = total_tests - passed_tests
    total_duration = sum(result['duration'] for result in results)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print(f"Total Duration: {total_duration:.2f} seconds")
    
    print(f"\nDetailed Results:")
    print(f"{'Test Name':<50} {'Status':<10} {'Duration':<10}")
    print(f"{'-'*50} {'-'*10} {'-'*10}")
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        duration = f"{result['duration']:.2f}s"
        print(f"{result['name']:<50} {status:<10} {duration:<10}")
        
        if not result['success'] and result['error']:
            print(f"  Error: {result['error']}")
    
    if failed_tests == 0:
        print(f"\n🎉 ALL TESTS PASSED! ChromaDB metadata filtering is working correctly.")
    else:
        print(f"\n⚠️  {failed_tests} test(s) failed. Please review the errors above.")

def main():
    """Main test runner function."""
    print("ChromaDB Metadata Filtering Test Suite")
    print("=" * 80)
    print("This test suite verifies that ChromaDB metadata filtering is working correctly")
    print("and prevents cross-article contamination.")
    print()
    
    # Define all tests to run
    tests = [
        (test_basic_metadata_filtering, "Basic Metadata Filtering"),
        (test_cross_article_contamination_prevention, "Cross-Article Contamination Prevention"),
        (test_complex_metadata_filtering, "Complex Metadata Filtering"),
        (test_metadata_filtering_performance, "Metadata Filtering Performance"),
        (test_metadata_filtering_edge_cases, "Metadata Filtering Edge Cases"),
        (test_metadata_filtering_integration, "Metadata Filtering Integration")
    ]
    
    # Run all tests
    results = []
    for test_func, test_name in tests:
        result = run_test_with_timing(test_func, test_name)
        results.append(result)
    
    # Print summary
    print_test_summary(results)
    
    # Exit with appropriate code
    failed_tests = sum(1 for result in results if not result['success'])
    if failed_tests > 0:
        print(f"\nExiting with error code 1 due to {failed_tests} failed test(s)")
        sys.exit(1)
    else:
        print(f"\nExiting with success code 0")
        sys.exit(0)

if __name__ == "__main__":
    main()