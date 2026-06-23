import streamlit as st
import pandas as pd
import io

# Налаштування сторінки
st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

# Кастомний тактичний дизайн через CSS
st.markdown("""
    <style>
    .stApp { background-color: #121417; color: #FFFFFF; }
    div[data-testid="stMetricValue"] { color: #00C897 !important; font-weight: bold; }
    .stButton>button { background-color: #1E2229; color: #FFFFFF; border: 1px solid #00C897; border-radius: 8px; width: 100%; }
    .stButton>button:hover { background-color: #00C897; color: #121417; }
    </style>
""", unsafe_allow_html=True)

# Завантаження бази даних прямо із Секретів додатку (Без Excel файлів!)
@st.cache_data
def load_data():
    try:
        # Читаємо текстову матрицю, яку ми вставили в секрети
        raw_data = st.secrets["database"]["data"]
        return pd.read_csv(io.StringIO(raw_data.strip()), sep="|")
    except Exception as e:
        st.error(f"Помилка завантаження даних із Секретів: {e}")
        return None

df = load_data()

# Головне меню додатку (Вкладки)
tab_home, tab_emergency = st.tabs(["🧮 Калькулятор", "🚨 Аварійні Протоколи"])

# --- ВКЛАДКА 1: КАЛЬКУЛЯТОР ДЕЗРОЗЧИНІВ ---
with tab_home:
    st.title("🧮 Калькулятор ВІК")
    st.caption("Автономний розрахунок робочих розчинів | Секрети активовано")
    
    if df is not None:
        # Вибір об'єкта дезінфекції
        objects = sorted(df['Object_UA'].dropna().unique())
        selected_object = st.selectbox("1. Оберіть об'єкт дезінфекції:", objects)
        
        # Фільтрація засобів під обраний об'єкт
        filtered_df = df[df['Object_UA'] == selected_object]
        products = filtered_df['Product'].dropna().unique()
        selected_product = st.selectbox("2. Оберіть дезінфекційний засіб:", products)
        
        # Фінальний розрахунок результатів
        result_row = filtered_df[filtered_df['Product'] == selected_product].iloc[0]
        
        st.markdown("---")
        st.subheader("🏁 Результат розрахунку:")
        st.metric(label="Концентрація робочого розчину", value=f"{result_row['Conc_%']}")
        
        if pd.notna(result_row['Tablets']) and result_row['Tablets'] != "—":
            st.success(f"🧫 Кількість таблеток: **{result_row['Tablets']} табл.** на 10л води")
        elif pd.notna(result_row['Volume_ml']) and result_row['Volume_ml'] != "—":
            st.success(f"🧪 Кількість концентрату: **{result_row['Volume_ml']}**")
            
        st.info(f"ℹ️ Спосіб знезараження: **{result_row['Method_UA']}**")
        st.warning(f"⏱️ Час експозиції: **{result_row['Exposure_min']} хв.**")

# --- ВКЛАДКА 2: АВАРІЙНІ ПРОТОКОЛИ ---
with tab_emergency:
    st.title("🚨 Аварійні Протоколи")
    emergency_type = st.radio("Оберіть тип ситуації:", ["💉 Укол / Поріз", "💦 Розлиття біорідини", "🗑️ Розсипання відходів"], horizontal=True)
    st.markdown("---")
    
    if "Укол" in emergency_type:
        st.subheader("🚨 АЛГОРИТМ ДІЙ ПРИ УКОЛІ ТА ПОРІЗІ:")
        st.markdown("""
        * **1.** НЕ ПАНІКУВАТИ! Зупиніть маніпуляцію. Не стискайте і не тріть місце уколу!
        * **2.** Промийте рану великою кількістю води з милом під проточною водою (мінімум 3 хв).
        * **3.** Обробіть шкіру 70% спиртом або антисептиком. Не лийте йод углиб рани!
        * **4.** Закрийте рану водонепроникним пластирем.
        """)
        st.error("⚠️ ВІКНО ЕФЕКТИВНОСТІ ПОСТКОНТАКТНОЇ ПРОФІЛАКТИКИ (ПКП) — 72 ГОДИНИ!")
