import pandas as pd
import pytest
from datetime import date
from analysis import calculate_sales_kpis, get_filtered_data


@pytest.fixture
def sample_dataframe():
    """Fixture that provides a sample DataFrame for testing."""
    data = {
        "date": pd.to_datetime(
            ["2023-01-01", "2023-01-01", "2023-01-02", "2023-01-03"]
        ),
        "category": ["Electronics", "Clothing", "Electronics", "Home"],
        "price": [100.0, 50.0, 200.0, 150.0],
        "quantity": [2, 1, 3, 2],
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_dataframe():
    """Fixture that provides an empty DataFrame for testing."""
    return pd.DataFrame(columns=["date", "category", "price", "quantity"])


@pytest.fixture
def dataframe_with_missing_values():
    """Fixture that provides a DataFrame with some missing values."""
    data = {
        "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "category": ["Electronics", "Clothing", None],
        "price": [100.0, 50.0, 200.0],
        "quantity": [2, 1, 3],
    }
    return pd.DataFrame(data)


class TestCalculateSalesKpis:
    """Test class for calculate_sales_kpis function."""

    def test_calculate_sales_kpis_basic(self, sample_dataframe):
        """Test calculate_sales_kpis with basic DataFrame."""
        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(sample_dataframe)
        )

        # Expected values: (100*2) + (50*1) + (200*3) + (150*2) = 200 + 50 + 600 + 300 = 1150
        expected_total_revenue = 1150.0
        # 3 unique dates, so avg daily revenue = 1150/3
        expected_avg_daily_revenue = 1150.0 / 3
        expected_total_quantity = 8  # 2+1+3+2
        expected_avg_daily_quantity = 8 / 3  # 3 unique dates

        assert total_revenue == expected_total_revenue
        assert abs(avg_daily_revenue - expected_avg_daily_revenue) < 0.01
        assert total_quantity == expected_total_quantity
        assert abs(avg_daily_quantity - expected_avg_daily_quantity) < 0.01

    def test_calculate_sales_kpis_empty_dataframe(self, empty_dataframe):
        """Test calculate_sales_kpis with empty DataFrame."""
        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(empty_dataframe)
        )

        assert total_revenue == 0.0
        assert avg_daily_revenue == 0.0
        assert total_quantity == 0
        assert avg_daily_quantity == 0.0

    def test_calculate_sales_kpis_single_date(self):
        """Test calculate_sales_kpis with single date."""
        data = {
            "date": pd.to_datetime(["2023-01-01", "2023-01-01"]),
            "category": ["Electronics", "Clothing"],
            "price": [100.0, 50.0],
            "quantity": [2, 1],
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = 250.0  # (100*2) + (50*1)
        expected_avg_daily_revenue = 250.0  # 250/1 (only 1 unique date)
        expected_total_quantity = 3  # 2+1
        expected_avg_daily_quantity = 3.0  # 3/1

        assert total_revenue == expected_total_revenue
        assert avg_daily_revenue == expected_avg_daily_revenue
        assert total_quantity == expected_total_quantity
        assert avg_daily_quantity == expected_avg_daily_quantity

    def test_calculate_sales_kpis_single_row(self):
        """Test calculate_sales_kpis with single row."""
        data = {
            "date": [pd.to_datetime("2023-01-01")],
            "category": ["Electronics"],
            "price": [100.0],
            "quantity": [2],
        }
        df = pd.DataFrame(data)

        total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = (
            calculate_sales_kpis(df)
        )

        expected_total_revenue = 200.0  # 100*2
        expected_avg_daily_revenue = 200.0  # 200/1
        expected_total_quantity = 2
        expected_avg_daily_quantity = 2.0  # 2/1

        assert total_revenue == expected_total_revenue
        assert avg_daily_revenue == expected_avg_daily_revenue
        assert total_quantity == expected_total_quantity
        assert avg_daily_quantity == expected_avg_daily_quantity


class TestGetFilteredData:
    """Test class for get_filtered_data function."""

    def test_get_filtered_data_no_filter(self, sample_dataframe):
        """Test get_filtered_data without filtering (start and end date cover all data)."""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 3)

        result = get_filtered_data(sample_dataframe, start_date, end_date)

        # All rows should be included
        assert len(result) == len(sample_dataframe)
        pd.testing.assert_frame_equal(result, sample_dataframe)

    def test_get_filtered_data_partial_filter(self, sample_dataframe):
        """Test get_filtered_data with partial date range."""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 2)

        result = get_filtered_data(sample_dataframe, start_date, end_date)

        # Should only include rows from 2023-01-01 and 2023-01-02
        expected_dates = pd.to_datetime(["2023-01-01", "2023-01-01", "2023-01-02"])
        assert len(result) == 3
        pd.testing.assert_series_equal(
            result["date"].reset_index(drop=True),
            pd.Series(expected_dates, name="date"),
        )

    def test_get_filtered_data_out_of_range(self, sample_dataframe):
        """Test get_filtered_data with date range outside the data range."""
        start_date = date(2023, 2, 1)
        end_date = date(2023, 2, 10)

        result = get_filtered_data(sample_dataframe, start_date, end_date)

        # Should return empty DataFrame
        assert len(result) == 0

    def test_get_filtered_data_single_date(self, sample_dataframe):
        """Test get_filtered_data for a single date."""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 1)

        result = get_filtered_data(sample_dataframe, start_date, end_date)

        # Should only include rows from 2023-01-01
        expected_dates = pd.to_datetime(["2023-01-01", "2023-01-01"])
        assert len(result) == 2
        pd.testing.assert_series_equal(
            result["date"].reset_index(drop=True),
            pd.Series(expected_dates, name="date"),
        )

    def test_get_filtered_data_empty_dataframe(self, empty_dataframe):
        """Test get_filtered_data with empty DataFrame."""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 10)

        result = get_filtered_data(empty_dataframe, start_date, end_date)

        assert len(result) == 0
        pd.testing.assert_frame_equal(result, empty_dataframe)
