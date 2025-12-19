import pandas as pd


def calculate_revenue(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate revenue by multiplying price and quantity columns.

    Args:
        dataframe: Input DataFrame containing 'price' and 'quantity' columns

    Returns:
        DataFrame with added 'revenue' column
    """
    result_df = dataframe.copy()
    result_df['revenue'] = result_df['price'] * result_df['quantity']
    return result_df


def group_by_date_and_category(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Group the dataframe by date and category, aggregating revenue and quantity.

    Args:
        dataframe: Input DataFrame with 'date', 'category', 'revenue', and 'quantity' columns

    Returns:
        Grouped DataFrame with aggregated values
    """
    grouped_df = dataframe.groupby(['date', 'category']).agg({
        'revenue': 'sum',
        'quantity': 'sum'
    }).reset_index()
    return grouped_df


def calculate_category_moving_average(dataframe: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """
    Calculate rolling average of revenue for each category.

    Args:
        dataframe: Input DataFrame with 'date', 'category', and 'revenue' columns
        window: Size of the moving window for rolling average calculation

    Returns:
        DataFrame with added 'revenue_rolling_avg' column
    """
    result_df = dataframe.copy()
    result_df = result_df.sort_values('date')
    result_df['revenue_rolling_avg'] = (
        result_df.groupby('category')['revenue']
        .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
    )
    return result_df


def calculate_revenue_percentage(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the percentage of revenue for each entry relative to its category total.

    Args:
        dataframe: Input DataFrame with 'category' and 'revenue' columns

    Returns:
        DataFrame with added 'revenue_percentage' column
    """
    result_df = dataframe.copy()
    category_totals = result_df.groupby('category')['revenue'].transform('sum')
    result_df['revenue_percentage'] = (result_df['revenue'] / category_totals) * 100
    return result_df


def filter_low_revenue_items(dataframe: pd.DataFrame, quantile_threshold: float = 0.1) -> pd.DataFrame:
    """
    Filter out items with revenue below the specified quantile threshold.

    Args:
        dataframe: Input DataFrame with 'revenue' column
        quantile_threshold: Threshold quantile value for filtering (e.g., 0.1 for 10th percentile)

    Returns:
        Filtered DataFrame containing only items above the revenue threshold
    """
    revenue_threshold = dataframe['revenue'].quantile(quantile_threshold)
    filtered_df = dataframe[dataframe['revenue'] > revenue_threshold]
    return filtered_df


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process sales data to calculate metrics, group by date and category, 
    calculate moving averages, revenue percentages, and filter low performers.

    Args:
        df: Input DataFrame containing 'date', 'category', 'price', and 'quantity' columns

    Returns:
        Processed DataFrame with calculated metrics and filtered results
    """
    # Calculate revenue from price and quantity
    df_with_revenue = calculate_revenue(df)
    
    # Group by date and category to aggregate sales metrics
    grouped_df = group_by_date_and_category(df_with_revenue)
    
    # Calculate moving average for revenue by category
    df_with_moving_avg = calculate_category_moving_average(grouped_df)
    
    # Calculate percentage of revenue for each category
    df_with_percentage = calculate_revenue_percentage(df_with_moving_avg)
    
    # Filter out low revenue items
    final_df = filter_low_revenue_items(df_with_percentage)
    
    return final_df