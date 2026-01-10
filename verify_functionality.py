#!/usr/bin/env python3
"""
Verification script to test the functionality of the modules.
"""

import pandas as pd
from datetime import date
from analysis import calculate_sales_kpis, get_filtered_data

def test_basic_functionality():
    """Test basic functionality of the analysis module."""
    print("Testing basic functionality...")
    
    # Create a simple test
    data = {
        'date': pd.to_datetime(['2023-01-01', '2023-01-02']),
        'category': ['Electronics', 'Clothing'],
        'price': [100.0, 50.0],
        'quantity': [2, 1]
    }
    df = pd.DataFrame(data)

    # Test the functions
    result = calculate_sales_kpis(df)
    print(f'calculate_sales_kpis works: {result}')

    filtered = get_filtered_data(df, date(2023, 1, 1), date(2023, 1, 2))
    print(f'get_filtered_data works: {len(filtered)} rows')

    print('Basic functionality test passed!')
    return True

def test_edge_cases():
    """Test edge cases."""
    print("\nTesting edge cases...")
    
    # Empty dataframe
    empty_df = pd.DataFrame(columns=['date', 'category', 'price', 'quantity'])
    try:
        result = calculate_sales_kpis(empty_df)
        print(f'Empty dataframe test passed: {result}')
    except Exception as e:
        print(f'Empty dataframe test failed: {e}')
        return False
    
    # Single row
    single_row_df = pd.DataFrame({
        'date': [pd.to_datetime('2023-01-01')],
        'category': ['Electronics'],
        'price': [100.0],
        'quantity': [2]
    })
    try:
        result = calculate_sales_kpis(single_row_df)
        print(f'Single row test passed: {result}')
    except Exception as e:
        print(f'Single row test failed: {e}')
        return False
    
    print('Edge cases test passed!')
    return True

if __name__ == "__main__":
    success = True
    success &= test_basic_functionality()
    success &= test_edge_cases()
    
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")
        exit(1)