import pandas as pd

# Read the Excel file to understand its structure
df = pd.read_excel('docs/test_data.xlsx')

print("Columns in the Excel file:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print(f"\nData shape: {df.shape}")
print(f"\nData types:")
print(df.dtypes)