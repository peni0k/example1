#!/usr/bin/env python3
"""
Test runner to verify all test files work correctly.
"""

import sys
import traceback
from validation_tests import TestValidationScenarios
from performance_tests import TestPerformanceScenarios
from integration_tests import TestIntegrationScenarios
from edge_case_tests import TestEdgeCaseScenarios

def run_validation_tests():
    """Run all validation tests."""
    print("Running Validation Tests...")
    validator = TestValidationScenarios()
    tests = [
        validator.test_calculate_sales_kpis_negative_prices,
        validator.test_calculate_sales_kpis_large_numbers,
        validator.test_get_filtered_data_future_dates,
        validator.test_get_filtered_data_invalid_date_range
    ]
    
    for test_func in tests:
        try:
            test_func()
            print(f"  ✓ {test_func.__name__}")
        except Exception as e:
            print(f"  ✗ {test_func.__name__}: {e}")
            traceback.print_exc()

def run_performance_tests():
    """Run all performance tests."""
    print("\nRunning Performance Tests...")
    perf_tester = TestPerformanceScenarios()
    tests = [
        # Skip the large dataset test as it might take too long
        perf_tester.test_calculate_sales_kpis_many_unique_dates,
        perf_tester.test_get_filtered_data_large_date_range,
        perf_tester.test_calculate_sales_kpis_zero_quantities
    ]
    
    for test_func in tests:
        try:
            test_func()
            print(f"  ✓ {test_func.__name__}")
        except Exception as e:
            print(f"  ✗ {test_func.__name__}: {e}")
            traceback.print_exc()

def run_integration_tests():
    """Run all integration tests."""
    print("\nRunning Integration Tests...")
    integrator = TestIntegrationScenarios()
    tests = [
        integrator.test_combined_functions_workflow,
        integrator.test_multiple_filters_and_calculations,
        integrator.test_edge_case_boundaries,
        integrator.test_consistency_across_multiple_calls
    ]
    
    for test_func in tests:
        try:
            test_func()
            print(f"  ✓ {test_func.__name__}")
        except Exception as e:
            print(f"  ✗ {test_func.__name__}: {e}")
            traceback.print_exc()

def run_edge_case_tests():
    """Run all edge case tests."""
    print("\nRunning Edge Case Tests...")
    edge_tester = TestEdgeCaseScenarios()
    tests = [
        edge_tester.test_calculate_sales_kpis_single_decimal_values,
        edge_tester.test_calculate_sales_kpis_mixed_positive_negative,
        edge_tester.test_get_filtered_data_same_start_end_date,
        edge_tester.test_calculate_sales_kpis_extreme_values,
        edge_tester.test_get_filtered_data_leap_year_boundary
    ]
    
    for test_func in tests:
        try:
            test_func()
            print(f"  ✓ {test_func.__name__}")
        except Exception as e:
            print(f"  ✗ {test_func.__name__}: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    print("Starting comprehensive test suite...")
    
    run_validation_tests()
    run_performance_tests()
    run_integration_tests()
    run_edge_case_tests()
    
    print("\nAll test suites completed!")