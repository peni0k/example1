def process_data(df):
    """
    Example of complex function that needs refactoring.
    This function does multiple operations that should be split.
    """
    # Calculate revenue
    df['revenue'] = df['price'] * df['quantity']
    
    # Group by date and category
    grouped = df.groupby(['date', 'category']).agg({
        'revenue': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    # Calculate moving average
    grouped = grouped.sort_values('date')
    grouped['revenue_rolling_avg'] = grouped.groupby('category')['revenue'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    
    # Calculate percentage of total
    category_totals = grouped.groupby('category')['revenue'].transform('sum')
    grouped['revenue_percentage'] = (grouped['revenue'] / category_totals) * 100
    
    # Filter out low revenue items
    filtered_df = grouped[grouped['revenue'] > grouped['revenue'].quantile(0.1)]
    
    # Return processed dataframe
    return filtered_df