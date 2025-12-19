import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Tuple
import numpy as np
from datetime import datetime, timedelta


def create_revenue_trend_plot(df: pd.DataFrame, selected_categories: list = None) -> object:
    """
    Creates a bar chart showing revenue trend over time.

    Args:
        df: DataFrame containing date, price, and quantity data
        selected_categories: List of categories to filter, if None, show all

    Returns:
        Plotly figure object
    """
    # Filter by selected categories if provided
    if selected_categories is not None and len(selected_categories) > 0:
        plot_df = df[df['category'].isin(selected_categories)].copy()
    else:
        plot_df = df.copy()

    # Group by date to get daily revenue
    plot_df['revenue'] = plot_df['price'] * plot_df['quantity']
    daily_revenue = plot_df.groupby('date')['revenue'].sum().reset_index()

    # Create the bar chart
    fig = px.bar(
        daily_revenue,
        x='date',
        y='revenue',
        title='Динамика выручки по дням',
        labels={'revenue': 'Выручка (руб.)', 'date': 'Дата'}
    )

    fig.update_layout(
        xaxis_title="Дата",
        yaxis_title="Выручка (руб.)",
        hovermode='x unified',
        xaxis=dict(rangeslider_visible=True),
        dragmode='pan'
    )

    return fig


def create_quantity_trend_plot(df: pd.DataFrame, selected_categories: list = None) -> object:
    """
    Creates a bar chart showing quantity trend over time.

    Args:
        df: DataFrame containing date and quantity data
        selected_categories: List of categories to filter, if None, show all

    Returns:
        Plotly figure object
    """
    # Filter by selected categories if provided
    if selected_categories is not None and len(selected_categories) > 0:
        plot_df = df[df['category'].isin(selected_categories)].copy()
    else:
        plot_df = df.copy()

    # Group by date to get daily quantity
    daily_quantity = plot_df.groupby('date')['quantity'].sum().reset_index()

    # Create the bar chart
    fig = px.bar(
        daily_quantity,
        x='date',
        y='quantity',
        title='Динамика количества продаж по дням',
        labels={'quantity': 'Количество', 'date': 'Дата'}
    )

    fig.update_layout(
        xaxis_title="Дата",
        yaxis_title="Количество",
        hovermode='x unified',
        xaxis=dict(rangeslider_visible=True),
        dragmode='pan'
    )

    return fig


def create_forecast_plot(df: pd.DataFrame, selected_categories: list = None) -> object:
    """
    Creates a forecast plot showing revenue and quantity trends with projections.

    Args:
        df: DataFrame containing date, price, and quantity data
        selected_categories: List of categories to filter, if None, show all

    Returns:
        Plotly figure object
    """
    # Filter by selected categories if provided
    if selected_categories is not None and len(selected_categories) > 0:
        plot_df = df[df['category'].isin(selected_categories)].copy()
    else:
        plot_df = df.copy()

    # Group by date to get daily metrics
    plot_df['revenue'] = plot_df['price'] * plot_df['quantity']
    daily_data = plot_df.groupby('date').agg({
        'revenue': 'sum',
        'quantity': 'sum'
    }).reset_index()

    # Create subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add revenue trend
    fig.add_trace(
        go.Scatter(
            x=daily_data['date'],
            y=daily_data['revenue'],
            mode='lines+markers',
            name='Выручка (факт)',
            line=dict(color='blue', width=2),
            hovertemplate='Дата: %{x}<br>Выручка: %{y:,.0f} руб.<extra></extra>'
        ),
        secondary_y=False,
    )

    # Add quantity trend
    fig.add_trace(
        go.Scatter(
            x=daily_data['date'],
            y=daily_data['quantity'],
            mode='lines+markers',
            name='Количество (факт)',
            line=dict(color='red', width=2),
            hovertemplate='Дата: %{x}<br>Количество: %{y:,.0f}<extra></extra>'
        ),
        secondary_y=True,
    )

    # Add forecast if we have enough data
    if len(daily_data) >= 10:  # Only create forecast if we have sufficient data
        # Create a time series for forecasting
        dates = pd.to_datetime(daily_data['date'])
        revenue_values = daily_data['revenue'].values
        quantity_values = daily_data['quantity'].values

        # Simple linear trend forecast
        x_vals = np.arange(len(dates))

        # Revenue forecast
        revenue_coeffs = np.polyfit(x_vals, revenue_values, 1)
        revenue_trend = np.polyval(revenue_coeffs, x_vals)

        # Quantity forecast
        quantity_coeffs = np.polyfit(x_vals, quantity_values, 1)
        quantity_trend = np.polyval(quantity_coeffs, x_vals)

        # Extend dates for forecast
        last_date = dates.max()
        forecast_dates = []
        for i in range(1, 8):  # 7 days forecast
            forecast_dates.append(last_date + timedelta(days=i))

        forecast_x = np.arange(len(x_vals), len(x_vals) + len(forecast_dates))
        forecast_revenue = np.polyval(revenue_coeffs, forecast_x)
        forecast_quantity = np.polyval(quantity_coeffs, forecast_x)

        # Add forecast lines
        all_dates = list(dates) + forecast_dates
        all_revenue = list(daily_data['revenue']) + list(forecast_revenue)
        all_quantity = list(daily_data['quantity']) + list(forecast_quantity)

        # Add forecast lines
        fig.add_trace(
            go.Scatter(
                x=forecast_dates,
                y=forecast_revenue,
                mode='lines',
                name='Выручка (прогноз)',
                line=dict(color='blue', width=2, dash='dash'),
                hovertemplate='Дата: %{x}<br>Выручка (прогноз): %{y:,.0f} руб.<extra></extra>'
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=forecast_dates,
                y=forecast_quantity,
                mode='lines',
                name='Количество (прогноз)',
                line=dict(color='red', width=2, dash='dash'),
                hovertemplate='Дата: %{x}<br>Количество (прогноз): %{y:,.0f}<extra></extra>'
            ),
            secondary_y=True,
        )

    # Update layout
    fig.update_layout(
        title_text="Прогноз выручки и количества продаж",
        hovermode='x unified',
        dragmode='pan',
        xaxis=dict(rangeslider_visible=True)
    )

    fig.update_xaxes(title_text="Дата")

    fig.update_yaxes(title_text="Выручка (руб.)", secondary_y=False)
    fig.update_yaxes(title_text="Количество", secondary_y=True)

    return fig


def create_category_filter_plot(df: pd.DataFrame, category: str) -> object:
    """
    Creates a plot for a specific category showing its revenue and quantity trends.

    Args:
        df: DataFrame containing date, price, and quantity data
        category: Specific category to visualize

    Returns:
        Plotly figure object
    """
    plot_df = df[df['category'] == category].copy()
    if plot_df.empty:
        fig = go.Figure()
        fig.add_annotation(text=f"Нет данных для категории {category}")
        fig.update_layout(title=f"Данные для категории {category}")
        return fig

    plot_df['revenue'] = plot_df['price'] * plot_df['quantity']
    daily_data = plot_df.groupby('date').agg({
        'revenue': 'sum',
        'quantity': 'sum'
    }).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add revenue
    fig.add_trace(
        go.Scatter(
            x=daily_data['date'],
            y=daily_data['revenue'],
            mode='lines+markers',
            name='Выручка',
            line=dict(color='blue'),
            hovertemplate='Дата: %{x}<br>Выручка: %{y:,.0f} руб.<extra></extra>'
        ),
        secondary_y=False,
    )

    # Add quantity
    fig.add_trace(
        go.Scatter(
            x=daily_data['date'],
            y=daily_data['quantity'],
            mode='lines+markers',
            name='Количество',
            line=dict(color='red'),
            hovertemplate='Дата: %{x}<br>Количество: %{y:,.0f}<extra></extra>'
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"Динамика для категории: {category}",
        hovermode='x unified',
        dragmode='pan',
        xaxis=dict(rangeslider_visible=True)
    )

    fig.update_xaxes(title_text="Дата")

    fig.update_yaxes(title_text="Выручка (руб.)", secondary_y=False)
    fig.update_yaxes(title_text="Количество", secondary_y=True)

    return fig


def create_correlation_heatmap(df: pd.DataFrame) -> object:
    """
    Creates a correlation heatmap showing relationships between numerical columns.

    Args:
        df: DataFrame containing the data to analyze

    Returns:
        Plotly figure object
    """
    # Create additional calculated columns for analysis
    plot_df = df.copy()
    plot_df['revenue'] = plot_df['price'] * plot_df['quantity']

    # Select only numerical columns for correlation
    numerical_cols = ['price', 'quantity', 'revenue']
    corr_data = plot_df[numerical_cols].corr()

    # Create heatmap
    fig = px.imshow(
        corr_data,
        text_auto=True,
        aspect="auto",
        title="Корреляционная матрица показателей",
        color_continuous_scale='RdBu',
        range_color=[-1, 1]
    )

    fig.update_layout(
        xaxis_title="Показатели",
        yaxis_title="Показатели"
    )

    return fig