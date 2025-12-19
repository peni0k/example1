import streamlit as st
import pandas as pd
from datetime import datetime
from data_loader import load_data_from_path, load_uploaded_data
from analysis import calculate_sales_kpis, get_filtered_data
from plotting import (create_revenue_trend_plot, create_quantity_trend_plot,
                     create_forecast_plot, create_category_filter_plot)


def main():
    # Application title
    st.title("Анализатор Продаж")

    # File upload section in sidebar
    st.sidebar.header("Загрузка данных")
    uploaded_file = st.sidebar.file_uploader(
        "Загрузите CSV или Excel файл",
        type=['csv', 'xlsx', 'xls'],
        help="Файл должен содержать колонки 'date', 'category', 'price', 'quantity'"
    )

    # Load data based on whether a file was uploaded
    if uploaded_file is not None:
        df = load_uploaded_data(uploaded_file)
        st.sidebar.success("Файл успешно загружен!")
    else:
        # Load demo data if no file is uploaded
        df = load_data_from_path()
        if df is not None:
            st.sidebar.info("Используются демонстрационные данные. Загрузите свой файл для анализа.")
        else:
            st.sidebar.warning("Демонстрационные данные недоступны. Пожалуйста, загрузите файл.")

    if df is None or df.empty:
        st.error("Не удалось загрузить данные. Пожалуйста, загрузите файл с данными.")

        # Show help section if no data is available
        with st.expander("Формат требуемых данных", expanded=True):
            st.markdown("""
            ### Требуемый формат данных

            Приложение принимает CSV или Excel файлы со следующими столбцами:

            **Обязательные столбцы:**
            - `date` - дата в формате YYYY-MM-DD
            - `category` - категория товара/услуги
            - `price` - цена за единицу (столбец 'Цена_за_ед' в вашем файле)
            - `quantity` - количество (столбец 'Количество' в вашем файле)

            **Пример содержимого файла:**
            ```csv
            date,category,price,quantity
            2023-01-01,Электроника,5000,2
            2023-01-01,Одежда,1500,1
            2023-01-02,Дом,3000,3
            ...
            ```
            """)
        return

    # Check if required columns exist
    required_columns = ['date', 'category', 'price', 'quantity']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Отсутствуют обязательные столбцы: {missing_columns}")
        return

    # Sidebar for filters
    st.sidebar.header("Параметры фильтрации")

    # Category filter
    all_categories = df['category'].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Выберите категории",
        options=all_categories,
        default=all_categories
    )

    # Date range selection
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

    start_date = st.sidebar.date_input(
        "Начальная дата",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

    end_date = st.sidebar.date_input(
        "Конечная дата",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )

    # Validate date range
    if start_date > end_date:
        st.error("Ошибка: Конечная дата должна быть больше начальной даты.")
        return

    # Filter data based on selected dates and categories
    filtered_df = get_filtered_data(df, start_date, end_date)

    if selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]

    if filtered_df.empty:
        st.warning("Нет данных для выбранного диапазона дат и категорий.")
        return

    # Calculate KPIs
    total_revenue, avg_daily_revenue, total_quantity, avg_daily_quantity = calculate_sales_kpis(filtered_df)

    # Display KPI metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Общая выручка", f"{total_revenue:,.0f} руб.")
    col2.metric("Средняя выручка в день", f"{avg_daily_revenue:,.0f} руб.")
    col3.metric("Общее количество проданных единиц", f"{total_quantity:,}")

    # Visualization options
    st.sidebar.header("Настройки визуализации")
    chart_type = st.sidebar.selectbox(
        "Выберите тип графика",
        [
            "Динамика выручки по дням",
            "Динамика количества продаж по дням",
            "Прогноз выручки и количества",
            "Анализ по категориям"
        ]
    )

    # Create and display the selected chart
    if chart_type == "Динамика выручки по дням":
        fig = create_revenue_trend_plot(filtered_df, selected_categories)
    elif chart_type == "Динамика количества продаж по дням":
        fig = create_quantity_trend_plot(filtered_df, selected_categories)
    elif chart_type == "Прогноз выручки и количества":
        fig = create_forecast_plot(filtered_df, selected_categories)
    elif chart_type == "Анализ по категориям":
        if len(selected_categories) == 1:
            fig = create_category_filter_plot(filtered_df, selected_categories[0])
        else:
            st.warning("Для анализа по отдельной категории, пожалуйста, выберите только одну категорию")
            # Default to showing revenue trend
            fig = create_revenue_trend_plot(filtered_df, selected_categories)

    st.plotly_chart(fig, use_container_width=True)

    # Display data table
    st.subheader("Данные за выбранный период")
    display_df = filtered_df.copy()
    display_df['revenue'] = display_df['price'] * display_df['quantity']
    st.dataframe(display_df[['date', 'category', 'price', 'quantity', 'revenue']].style.format({
        'price': '{:,.0f} руб.',
        'quantity': '{:,.0f}',
        'revenue': '{:,.0f} руб.'
    }))


if __name__ == "__main__":
    main()