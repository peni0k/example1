import pandas as pd
import pytest
from datetime import date
from analysis import calculate_sales_kpis, get_filtered_data


class TestPerformanceScenarios:
    """Performance and stress tests for the analysis functions."""
    
    def test_calculate_sales_kpis_large_dataset(self):
        """Test calculate_sales_kpis with a large dataset."""
        # Create a large dataset with 10000 rows
        n_rows = 10000
        data = {
            "date": pd.to_datetime(["2023-01-01"] * n_rows),
            "category": ["Electronics"] * n_rows,
            "price": [100.0] * n_rows,
            "quantity": [2] * n_rows,
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = 100.0 * 2 * n_rows  # 100 * 2 * 10000
        expected_avg_daily_revenue = expected_total_revenue  # All on same day
        expected_total_quantity = 2 * n_rows  # 2 * 10000
        expected_avg_daily_quantity = expected_total_quantity  # All on same day

        assert total_revenue == expected_total_revenue
        assert avg_daily_revenue == expected_avg_daily_revenue
        assert total_quantity == expected_total_quantity
        assert avg_daily_quantity == expected_avg_daily_quantity

    def test_calculate_sales_kpis_many_unique_dates(self):
        """Test calculate_sales_kpis with many unique dates."""
        n_dates = 1000
        data = {
            "date": pd.date_range(start="2023-01-01", periods=n_dates, freq='D'),
            "category": ["Electronics"] * n_dates,
            "price": [100.0] * n_dates,
            "quantity": [2] * n_dates,
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = 100.0 * 2 * n_dates  # 100 * 2 * 1000
        expected_avg_daily_revenue = expected_total_revenue / n_dates
        expected_total_quantity = 2 * n_dates  # 2 * 1000
        expected_avg_daily_quantity = expected_total_quantity / n_dates

        assert total_revenue == expected_total_revenue
        assert abs(avg_daily_revenue - expected_avg_daily_revenue) < 0.01
        assert total_quantity == expected_total_quantity
        assert abs(avg_daily_quantity - expected_avg_daily_quantity) < 0.01

    def test_get_filtered_data_large_date_range(self):
        """Test get_filtered_data with a very large date range."""
        # Create data spanning multiple years
        data = {
            "date": pd.date_range(start="2020-01-01", end="2025-12-31", freq='D'),
            "category": ["Electronics"] * 2191,  # Number of days in the range
            "price": [100.0] * 2191,
            "quantity": [2] * 2191,
        }
        df = pd.DataFrame(data)

        start_date = date(2022, 1, 1)
        end_date = date(2023, 12, 31)

        result = get_filtered_data(df, start_date, end_date)

        # Should include all days from 2022-01-01 to 2023-12-31
        expected_count = 730  # Days from 2022-01-01 to 2023-12-31 inclusive
        assert len(result) == expected_count

    def test_calculate_sales_kpis_zero_quantities(self):
        """Test calculate_sales_kpis with zero quantities."""
        data = {
            "date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            "category": ["Electronics", "Clothing"],
            "price": [100.0, 50.0],
            "quantity": [0, 0],  # Zero quantities
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = 0.0  # Everything multiplied by 0
        expected_avg_daily_revenue = 0.0
        expected_total_quantity = 0  # Sum of zeros
        expected_avg_daily_quantity = 0.0  # Average of zeros

        assert total_revenue == expected_total_revenue
        assert avg_daily_revenue == expected_avg_daily_revenue
        assert total_quantity == expected_total_quantity
        assert avg_daily_quantity == expected_avg_daily_quantity