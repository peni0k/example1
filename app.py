import streamlit as st

# Set page config
st.set_page_config(
    page_title="Анализатор Продаж - Главная",
    layout="wide"
)

# Show navigation options
st.title("Анализатор Продаж")
st.write("Выберите раздел для работы с приложением:")

col1, col2 = st.columns(2)

with col1:
    if st.button("📚 Справка и информация"):
        st.write("[Перейти к справке](pages/home)")

with col2:
    if st.button("📊 Анализ продаж"):
        st.write("[Перейти к анализу](pages/sales_analyzer)")

# Alternative navigation using session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Provide direct links
st.subheader("Быстрые ссылки:")
st.page_link("pages/home.py", label="Главная страница и справка", icon="🏠")
st.page_link("pages/sales_analyzer.py", label="Анализ продаж", icon="📊")

st.divider()

# Display a preview of the help content
st.subheader("Краткая справка")
st.markdown("""
**Требуемые столбцы в файле данных:**
- `date` - дата (в формате YYYY-MM-DD)
- `category` - категория товара/услуги
- `price` - цена за единицу
- `quantity` - количество

**Возможности приложения:**
- Визуализация динамики выручки и количества
- Прогнозирование показателей
- Фильтрация по категориям и датам
- Поддержка CSV и Excel файлов
""")


def main():
    pass  # Main functionality is handled by Streamlit's page navigation


if __name__ == "__main__":
    main()