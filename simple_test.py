print("Starting test...")

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