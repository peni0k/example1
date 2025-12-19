import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names to English equivalents if they are in Russian or other formats.

    Args:
        df: Input DataFrame

    Returns:
        DataFrame with standardized column names
    """
    # Mapping of possible Russian/encoded column names to standard names
    column_mapping = {
        # Russian text might be encoded differently, so we include various possibilities
        'date': 'date',
        'Дата': 'date',
        '─рЄр': 'date',  # How it appears in the terminal
        'sessions': 'sessions',
        'sales': 'sales',
        'Продажи': 'sales',
        '╧Ёюфрцш': 'sales',
        'quantity': 'quantity',
        'Количество': 'quantity',
        '╩юышўхёЄтю': 'quantity',
        'price': 'price',
        'Цена_за_ед': 'price',
        '╓хэр_чр_хф': 'price',
        'category': 'category',
        'Категория': 'category',
        '╩рЄхуюЁш ': 'category',
        'page_views': 'page_views',
        'bounce_rate': 'bounce_rate',
        'avg_session_duration': 'avg_session_duration',
        'new_users': 'new_users',
        'returning_users': 'returning_users'
    }

    # Create a mapping for columns that exist in the dataframe
    rename_dict = {}
    for col in df.columns:
        # Use the original name if found in mapping, otherwise keep as is
        if col in column_mapping:
            rename_dict[col] = column_mapping[col]

    return df.rename(columns=rename_dict)


def transform_sales_to_traffic(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms sales data into web traffic metrics where possible.

    Args:
        df: DataFrame with sales data

    Returns:
        DataFrame with traffic metrics
    """
    # If the data has sales data but no traffic metrics, create synthetic mappings
    if 'sales' in df.columns:
        # Create sessions based on sales and quantity
        if 'quantity' not in df.columns:
            df['quantity'] = 1  # Default to 1 if not available

        # Map sales and quantity to web traffic metrics
        # For simplicity, use sales as a proxy for sessions with some transformation
        df['sessions'] = df['quantity'].fillna(1).astype(int)
        df['page_views'] = (df['sales'] / df['sales'].quantile(0.5)).fillna(1).astype(int)

        # Add some random variation for other metrics
        import numpy as np
        np.random.seed(42)  # For reproducible results
        df['bounce_rate'] = np.clip(np.random.normal(0.45, 0.15, len(df)), 0.1, 0.8)
        df['avg_session_duration'] = np.clip(
            np.random.normal(180, 60, len(df)), 30, 600
        ).astype(int)
        df['new_users'] = (df['sessions'] * 0.4).astype(int)
        df['returning_users'] = df['sessions'] - df['new_users']

        # Ensure all values are appropriately capped
        df['page_views'] = df['page_views'].apply(lambda x: max(1, min(x, 10000)))
        df['new_users'] = df['new_users'].apply(lambda x: max(0, x))
        df['returning_users'] = df['returning_users'].apply(lambda x: max(0, x))

    elif 'sessions' not in df.columns:
        # If no sessions column but there's a date column, create basic session data
        if 'date' in df.columns:
            import numpy as np
            np.random.seed(42)
            df['sessions'] = np.random.randint(50, 300, size=len(df))
            df['page_views'] = df['sessions'] * np.random.uniform(2.0, 4.0, size=len(df)).astype(int)
            df['bounce_rate'] = np.random.uniform(0.3, 0.6, size=len(df))
            df['avg_session_duration'] = np.random.randint(120, 300, size=len(df))
            df['new_users'] = (df['sessions'] * 0.3).astype(int)
            df['returning_users'] = df['sessions'] - df['new_users']

    return df


@st.cache_data
def load_data_from_path(file_path: str = "synthetic_traffic.csv") -> Optional[pd.DataFrame]:
    """
    Loads and caches data from a CSV file at a specific path.

    Args:
        file_path: Path to the CSV file. Defaults to 'synthetic_traffic.csv'.

    Returns:
        pandas DataFrame with loaded data or None if file cannot be loaded.
    """
    csv_path = Path(file_path)
    excel_path = Path("docs/test_data.xlsx")

    df = None

    # Try loading from CSV first
    if csv_path.exists():
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            st.warning(f"Ошибка при чтении CSV файла: {str(e)}")
            # If CSV fails, try Excel file
            pass

    # If CSV doesn't exist or failed, try Excel file
    if df is None and excel_path.exists():
        try:
            df = pd.read_excel(excel_path)
        except Exception as e:
            st.warning(f"Ошибка при чтении Excel файла: {str(e)}")
            return None
    elif df is None:
        # File doesn't exist but this is OK for the demo
        return None

    # Process the dataframe if it was loaded
    if df is not None:
        # Standardize column names
        df = standardize_column_names(df)

        # Convert date column to datetime - handle multiple possible names
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        if date_cols:
            df['date'] = pd.to_datetime(df[date_cols[0]], errors='coerce')
        else:
            st.error("Колонка 'date' не найдена в данных.")
            return None

        # Remove rows with invalid dates
        df = df.dropna(subset=['date'])

        # Transform data to have traffic metrics
        df = transform_sales_to_traffic(df)

        # Sort by date to ensure chronological order
        df = df.sort_values('date').reset_index(drop=True)

    return df


def load_uploaded_data(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Loads data from an uploaded file (CSV or Excel).

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        pandas DataFrame with loaded data or None if file cannot be loaded.
    """
    if uploaded_file is None:
        return None

    try:
        # Check file type and load accordingly
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   "application/vnd.ms-excel"]:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Поддерживаются только CSV и Excel файлы")
            return None

        # Standardize column names
        df = standardize_column_names(df)

        # Convert date column to datetime - handle multiple possible names
        date_cols = [col for col in df.columns if 'date' in col.lower() or '─рЄр' in col]
        if date_cols:
            df['date'] = pd.to_datetime(df[date_cols[0]], errors='coerce')
            # Remove rows with invalid dates
            df = df.dropna(subset=['date'])
        else:
            st.error("Колонка 'date' не найдена в данных.")
            return None

        # Transform data to have traffic metrics
        df = transform_sales_to_traffic(df)

        # Sort by date to ensure chronological order
        df = df.sort_values('date').reset_index(drop=True)

        return df
    except Exception as e:
        st.error(f"Ошибка при загрузке файла: {str(e)}")
        return None