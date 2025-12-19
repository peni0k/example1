import pandas as pd
from datetime import date
from typing import Tuple


def calculate_sales_kpis(df: pd.DataFrame) -> Tuple[float, float, int, float]:
    """
    Calculates key performance indicators for sales data.

    Args:
        df: DataFrame containing the filtered data

    Returns:
        A tuple containing:
        - Total revenue
        - Average daily revenue
        - Total quantity sold
        - Average daily quantity sold
    """
    revenue_series = df["price"] * df["quantity"]
    total_revenue = float(revenue_series.sum())

    # Calculate average daily revenue
    unique_dates = df["date"].nunique()
    if unique_dates > 0:
        avg_daily_revenue = total_revenue / unique_dates
    else:
        avg_daily_revenue = 0.0

    total_quantity = int(df["quantity"].sum())

    if unique_dates > 0:
        avg_daily_quantity = total_quantity / unique_dates
    else:
        avg_daily_quantity = 0.0

    return total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity


def get_filtered_data(
    df: pd.DataFrame, start_date: date, end_date: date
) -> pd.DataFrame:
    """
    Filters the data based on the selected date range.

    Args:
        df: Original DataFrame containing all data
        start_date: Start date for filtering
        end_date: End date for filtering

    Returns:
        Filtered DataFrame containing only data within the date range
    """
    # Convert date inputs to pandas datetime for comparison
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)

    # Filter the dataframe
    mask = (df["date"] >= start_datetime) & (df["date"] <= end_datetime)
    filtered_df = df.loc[mask].copy()

    return filtered_df
