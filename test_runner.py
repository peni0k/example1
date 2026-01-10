#!/usr/bin/env python3
"""
Simple test runner for the analysis module.
"""

import subprocess
import sys

def run_test():
    """Run a simple test to verify functionality."""
    test_code = '''
import pandas as pd
from datetime import date
from analysis import calculate_sales_kpis, get_filtered_data

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
print(f"calculate_sales_kpis works: {result}")

filtered = get_filtered_data(df, date(2023, 1, 1), date(2023, 1, 2))
print(f"get_filtered_data works: {len(filtered)} rows")

print("SUCCESS: Basic functionality test passed!")
'''
    
    result = subprocess.run([sys.executable, '-c', test_code], capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return code:", result.returncode)
    
    return result.returncode == 0

if __name__ == "__main__":
    success = run_test()
    if success:
        print("✓ Test ran successfully!")
    else:
        print("✗ Test failed!")