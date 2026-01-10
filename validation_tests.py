import pandas as pd
import pytest
from datetime import date
from analysis import calculate_sales_kpis, get_filtered_data


class TestValidationScenarios:
    """Additional validation tests for edge cases and error conditions."""
    
    def test_calculate_sales_kpis_negative_prices(self):
        """Test calculate_sales_kpis with negative prices."""
        data = {
            "date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            "category": ["Electronics", "Clothing"],
            "price": [-100.0, 50.0],  # Negative price
            "quantity": [2, 1],
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = -150.0  # (-100*2) + (50*1)
        expected_avg_daily_revenue = -75.0  # -150/2
        expected_total_quantity = 3  # 2+1
        expected_avg_daily_quantity = 1.5  # 3/2

        assert total_revenue == expected_total_revenue
        assert avg_daily_revenue == expected_avg_daily_revenue
        assert total_quantity == expected_total_quantity
        assert avg_daily_quantity == expected_avg_daily_quantity

    def test_calculate_sales_kpis_large_numbers(self):
        """Test calculate_sales_kpis with very large numbers."""
        data = {
            "date": pd.to_datetime(["2023-01-01"]),
            "category": ["Electronics"],
            "price": [1000000.0],  # Large price
            "quantity": [1000],    # Large quantity
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = 1000000000.0  # 1000000 * 1000
        expected_avg_daily_revenue = 1000000000.0  # 1000000000/1
        expected_total_quantity = 1000
        expected_avg_daily_quantity = 1000.0  # 1000/1

        assert total_revenue == expected_total_revenue
        assert avg_daily_revenue == expected_avg_daily_revenue
        assert total_quantity == expected_total_quantity
        assert avg_daily_quantity == expected_avg_daily_quantity

    def test_get_filtered_data_future_dates(self):
        """Test get_filtered_data with future dates."""
        data = {
            "date": pd.to_datetime(["2099-01-01", "2099-01-02"]),  # Future dates
            "category": ["Electronics", "Clothing"],
            "price": [100.0, 50.0],
            "quantity": [2, 1],
        }
        df = pd.DataFrame(data)

        start_date = date(2099, 1, 1)
        end_date = date(2099, 1, 2)

        result = get_filtered_data(df, start_date, end_date)

        assert len(result) == 2
        assert (result["date"] >= pd.Timestamp(start_date)).all()
        assert (result["date"] <= pd.Timestamp(end_date)).all()

    def test_get_filtered_data_invalid_date_range(self):
        """Test get_filtered_data with end date before start date."""
        data = {
            "date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            "category": ["Electronics", "Clothing"],
            "price": [100.0, 50.0],
            "quantity": [2, 1],
        }
        df = pd.DataFrame(data)

        start_date = date(2023, 1, 2)  # Later date
        end_date = date(2023, 1, 1)    # Earlier date

        result = get_filtered_data(df, start_date, end_date)

        # Should return empty DataFrame since end date is before start date
        assert len(result) == 0