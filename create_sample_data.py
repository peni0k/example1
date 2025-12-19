import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample synthetic traffic data
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 1, 1)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Generate synthetic session data with some patterns
np.random.seed(42)  # For reproducible results
base_sessions = 100
trend = np.linspace(0, 50, len(date_range))  # Slight upward trend
seasonal = 20 * np.sin(2 * np.pi * np.arange(len(date_range)) / 365.25)  # Annual seasonality
weekly_pattern = np.tile([0, -10, -5, 0, 5, 15, 10], len(date_range)//7 + 1)[:len(date_range)]  # Weekly pattern
noise = np.random.normal(0, 15, len(date_range))

sessions = base_sessions + trend + seasonal + weekly_pattern + noise
sessions = np.maximum(sessions, 0).round().astype(int)  # Ensure positive values

# Create DataFrame
df = pd.DataFrame({
    'date': date_range,
    'sessions': sessions
})

# Save to CSV
df.to_csv('synthetic_traffic.csv', index=False)
print("Sample synthetic_traffic.csv file created successfully!")
print(f"Data range: {df['date'].min()} to {df['date'].max()}")
print(f"Total records: {len(df)}")
print("\nFirst 5 rows:")
print(df.head())