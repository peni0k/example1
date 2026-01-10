import pandas as pd
import pytest
from datetime import date
from analysis import calculate_sales_kpis, get_filtered_data


class TestIntegrationScenarios:
    """Integration tests combining multiple functions and scenarios."""
    
    def test_combined_functions_workflow(self):
        """Test a typical workflow using both functions together."""
        # Create sample data
        data = {
            "date": pd.to_datetime([
                "2023-01-01", "2023-01-01", "2023-01-02", 
                "2023-01-03", "2023-01-03", "2023-01-04"
            ]),
            "category": [
                "Electronics", "Clothing", "Electronics", 
                "Home", "Books", "Electronics"
            ],
            "price": [100.0, 50.0, 200.0, 150.0, 30.0, 120.0],
            "quantity": [2, 1, 3, 2, 4, 1],
        }
        df = pd.DataFrame(data)

        # Apply date filter first
        start_date = date(2023, 1, 2)
        end_date = date(2023, 1, 3)
        filtered_df = get_filtered_data(df, start_date, end_date)

        # Then calculate KPIs on filtered data
        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(filtered_df)
        )

        # Expected values for filtered data:
        # 2023-01-02: Electronics (200 * 3 = 600)
        # 2023-01-03: Home (150 * 2 = 300), Books (30 * 4 = 120)
        # Total revenue: 600 + 300 + 120 = 1020
        # Total quantity: 3 + 2 + 4 = 9
        # Avg daily revenue: 1020 / 2 = 510 (2 unique dates)
        # Avg daily quantity: 9 / 2 = 4.5 (2 unique dates)
        
        expected_total_revenue = 1020.0
        expected_avg_daily_revenue = 510.0
        expected_total_quantity = 9
        expected_avg_daily_quantity = 4.5

        assert total_revenue == expected_total_revenue
        assert avg_daily_revenue == expected_avg_daily_revenue
        assert total_quantity == expected_total_quantity
        assert avg_daily_quantity == expected_avg_daily_quantity

    def test_multiple_filters_and_calculations(self):
        """Test applying multiple filters and calculations sequentially."""
        # Create sample data
        data = {
            "date": pd.to_datetime([
                "2023-01-01", "2023-01-02", "2023-01-03",
                "2023-01-04", "2023-01-05", "2023-01-06"
            ]),
            "category": [
                "Electronics", "Clothing", "Electronics",
                "Home", "Books", "Electronics"
            ],
            "price": [100.0, 50.0, 200.0, 150.0, 30.0, 120.0],
            "quantity": [2, 1, 3, 2, 4, 1],
        }
        df = pd.DataFrame(data)

        # Calculate KPIs for the entire dataset
        full_total_rev, full_avg_daily_rev, full_total_qty, full_avg_daily_qty = (
            calculate_sales_kpis(df)
        )
        
        # Calculate KPIs for different date ranges and compare
        start_date1, end_date1 = date(2023, 1, 1), date(2023, 1, 3)
        filtered_df1 = get_filtered_data(df, start_date1, end_date1)
        part1_total_rev, part1_avg_daily_rev, part1_total_qty, part1_avg_daily_qty = (
            calculate_sales_kpis(filtered_df1)
        )
        
        start_date2, end_date2 = date(2023, 1, 4), date(2023, 1, 6)
        filtered_df2 = get_filtered_data(df, start_date2, end_date2)
        part2_total_rev, part2_avg_daily_rev, part2_total_qty, part2_avg_daily_qty = (
            calculate_sales_kpis(filtered_df2)
        )

        # Check that the sum of parts equals the whole for total revenue and quantity
        assert abs((part1_total_rev + part2_total_rev) - full_total_rev) < 0.01
        assert (part1_total_qty + part2_total_qty) == full_total_qty

    def test_edge_case_boundaries(self):
        """Test boundary conditions in date filtering."""
        # Create data with dates at boundaries
        data = {
            "date": pd.to_datetime([
                "2023-01-01", "2023-01-15", "2023-01-31",  # Jan dates
                "2023-02-01", "2023-02-14", "2023-02-28"   # Feb dates
            ]),
            "category": ["A", "B", "C", "D", "E", "F"],
            "price": [100.0, 50.0, 200.0, 150.0, 30.0, 120.0],
            "quantity": [2, 1, 3, 2, 4, 1],
        }
        df = pd.DataFrame(data)

        # Test filtering exactly at month boundaries
        start_date = date(2023, 1, 15)
        end_date = date(2023, 1, 31)
        result = get_filtered_data(df, start_date, end_date)

        # Should include 2023-01-15 and 2023-01-31, but not 2023-02-01
        assert len(result) == 2
        assert all(date(2023, 1, 15) <= d.date() <= date(2023, 1, 31) for d in result['date'])

    def test_consistency_across_multiple_calls(self):
        """Test that functions return consistent results across multiple calls."""
        # Create sample data
        data = {
            "date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            "category": ["Electronics", "Clothing"],
            "price": [100.0, 50.0],
            "quantity": [2, 1],
        }
        df = pd.DataFrame(data)

        # Call functions multiple times and verify consistency
        results = []
        for _ in range(5):
            total_rev, avg_daily_rev, total_qty, avg_daily_qty = calculate_sales_kpis(df)
            results.append((total_rev, avg_daily_rev, total_qty, avg_daily_qty))

        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            assert result == first_result

        # Same test for filtering function
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 2)
        filter_results = []
        for _ in range(5):
            filtered_df = get_filtered_data(df, start_date, end_date)
            filter_results.append(len(filtered_df))

        # All results should be identical
        first_len = filter_results[0]
        for length in filter_results[1:]:
            assert length == first_len