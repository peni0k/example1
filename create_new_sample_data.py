import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample website traffic data with multiple metrics
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

np.random.seed(42)

# Generate synthetic metrics
base_sessions = 100
trend = np.linspace(0, 50, len(date_range))
seasonal = 20 * np.sin(2 * np.pi * np.arange(len(date_range)) / 365.25)
weekly_pattern = np.tile([0, -10, -5, 0, 5, 15, 10], len(date_range)//7 + 1)[:len(date_range)]
noise = np.random.normal(0, 15, len(date_range))
sessions = np.maximum(base_sessions + trend + seasonal + weekly_pattern + noise, 0).round().astype(int)

# Generate other metrics
page_views = sessions * np.random.uniform(2.0, 4.0, len(date_range))
bounce_rate = np.random.uniform(0.3, 0.6, len(date_range))
avg_session_duration = np.random.uniform(120, 300, len(date_range))  # seconds
new_users = np.maximum(sessions * np.random.uniform(0.2, 0.4), 0).round().astype(int)
returning_users = sessions - new_users

# Create DataFrame with extended metrics
df = pd.DataFrame({
    'date': date_range,
    'sessions': sessions,
    'page_views': page_views.round().astype(int),
    'bounce_rate': bounce_rate,
    'avg_session_duration': avg_session_duration.round().astype(int),
    'new_users': new_users,
    'returning_users': returning_users
})

# Save to CSV
df.to_csv('synthetic_traffic.csv', index=False)
print("Enhanced synthetic_traffic.csv file created successfully!")
print(f"Data range: {df['date'].min()} to {df['date'].max()}")
print(f"Total records: {len(df)}")
print("\nFirst 5 rows:")
print(df.head())
print("\nColumns:", list(df.columns))