import pandas as pd
from datetime import date
from analysis import calculate_sales_kpis, get_filtered_data

print("Running basic test...")

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

# Now test the validation tests directly
from validation_tests import TestValidationScenarios

print("\nTesting validation scenarios...")
validator = TestValidationScenarios()

try:
    validator.test_calculate_sales_kpis_negative_prices()
    print("Negative prices test passed")
except Exception as e:
    print(f"Negative prices test failed: {e}")

try:
    validator.test_calculate_sales_kpis_large_numbers()
    print("Large numbers test passed")
except Exception as e:
    print(f"Large numbers test failed: {e}")

print("\nAll validation tests completed!")