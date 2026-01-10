import pandas as pd
import pytest
from datetime import date
from analysis import calculate_sales_kpis, get_filtered_data


class TestEdgeCaseScenarios:
    """Edge case tests for unusual or boundary inputs."""
    
    def test_calculate_sales_kpis_single_decimal_values(self):
        """Test calculate_sales_kpis with decimal values."""
        data = {
            "date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            "category": ["Electronics", "Clothing"],
            "price": [100.5, 50.25],  # Decimal prices
            "quantity": [2.5, 1.75],  # Decimal quantities
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = (100.5 * 2.5) + (50.25 * 1.75)  # 251.25 + 87.9375 = 339.1875
        expected_total_quantity = 2.5 + 1.75  # 4.25
        expected_avg_daily_revenue = expected_total_revenue / 2  # 2 days
        expected_avg_daily_quantity = expected_total_quantity / 2  # 2 days

        assert abs(total_revenue - expected_total_revenue) < 0.001
        assert abs(avg_daily_revenue - expected_avg_daily_revenue) < 0.001
        assert abs(total_quantity - expected_total_quantity) < 0.001
        assert abs(avg_daily_quantity - expected_avg_daily_quantity) < 0.001

    def test_calculate_sales_kpis_mixed_positive_negative(self):
        """Test calculate_sales_kpis with mixed positive and negative values."""
        data = {
            "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
            "category": ["Electronics", "Clothing", "Books"],
            "price": [100.0, -50.0, 75.0],  # Mixed positive/negative prices
            "quantity": [2, 3, -2],  # Mixed positive/negative quantities
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = (100.0 * 2) + (-50.0 * 3) + (75.0 * -2)  # 200 - 150 - 150 = -100
        expected_total_quantity = 2 + 3 + (-2)  # 3
        expected_avg_daily_revenue = expected_total_revenue / 3  # 3 days
        expected_avg_daily_quantity = expected_total_quantity / 3  # 3 days

        assert total_revenue == expected_total_revenue
        assert avg_daily_revenue == expected_avg_daily_revenue
        assert total_quantity == expected_total_quantity
        assert avg_daily_quantity == expected_avg_daily_quantity

    def test_get_filtered_data_same_start_end_date(self):
        """Test get_filtered_data when start and end date are the same."""
        data = {
            "date": pd.to_datetime([
                "2023-01-01", "2023-01-02", "2023-01-02", 
                "2023-01-03", "2023-01-02"
            ]),
            "category": ["A", "B", "C", "D", "E"],
            "price": [100.0, 50.0, 200.0, 150.0, 30.0],
            "quantity": [2, 1, 3, 2, 4],
        }
        df = pd.DataFrame(data)

        # Filter for only 2023-01-02
        start_date = date(2023, 1, 2)
        end_date = date(2023, 1, 2)

        result = get_filtered_data(df, start_date, end_date)

        # Should return 3 rows with date 2023-01-02
        assert len(result) == 3
        assert all(d.date() == date(2023, 1, 2) for d in result['date'])

    def test_calculate_sales_kpis_extreme_values(self):
        """Test calculate_sales_kpis with extremely large and small values."""
        data = {
            "date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            "category": ["Electronics", "Clothing"],
            "price": [1e10, 1e-10],  # Extremely large and small prices
            "quantity": [1e-10, 1e10],  # Extremely small and large quantities
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = (1e10 * 1e-10) + (1e-10 * 1e10)  # 1 + 1 = 2
        expected_total_quantity = 1e-10 + 1e10  # ~1e10
        expected_avg_daily_revenue = expected_total_revenue / 2  # 1
        expected_avg_daily_quantity = expected_total_quantity / 2  # ~0.5e10

        assert abs(total_revenue - expected_total_revenue) < 0.001
        assert abs(avg_daily_revenue - expected_avg_daily_revenue) < 0.001
        assert abs(total_quantity - expected_total_quantity) < 0.001
        assert abs(avg_daily_quantity - expected_avg_daily_quantity) < 0.001

    def test_get_filtered_data_leap_year_boundary(self):
        """Test get_filtered_data around leap year boundary."""
        data = {
            "date": pd.to_datetime([
                "2020-02-28", "2020-02-29", "2020-03-01",  # 2020 is leap year
                "2021-02-28", "2021-03-01"                 # 2021 is not leap year
            ]),
            "category": ["A", "B", "C", "D", "E"],
            "price": [100.0, 50.0, 200.0, 150.0, 30.0],
            "quantity": [2, 1, 3, 2, 4],
        }
        df = pd.DataFrame(data)

        # Filter around February boundary in leap year
        start_date = date(2020, 2, 28)
        end_date = date(2020, 3, 1)
        result = get_filtered_data(df, start_date, end_date)

        # Should include 2020-02-28, 2020-02-29, 2020-03-01
        assert len(result) == 3
        assert all(pd.Timestamp(start_date) <= d <= pd.Timestamp(end_date) for d in result['date'])