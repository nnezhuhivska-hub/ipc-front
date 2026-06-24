import streamlit as st
import pandas as pd
import io
import time

# Налаштування сторінки під мобільний інтерфейс
st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

# Кастомний тактичний дизайн через CSS
st.markdown("""
    <style>
    .stApp { background-color: #121417; color: #FFFFFF; }
    div[data-testid="stMetricValue"] { color: #00C897 !important; font-weight: bold; }
    .stButton>button { background-color: #1E2229; color: #FFFFFF; border: 1px solid #00C897; border-radius: 8px; width: 100%; height: 50px; font-weight: bold; }
    .stButton>button:hover { background-color: #00C897; color: #121417; }
    </style>
""", unsafe_allow_html=True)

# Завантаження бази даних із Секретів додатку
@st.cache_data
def load_data():
    try:
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
    st.caption("Автономний розрахунок робочих розчинів")
    
    if df is not None:
        # 1. Вибір об'єкта дезінфекції
        objects = sorted(df['Object_UA'].dropna().unique())
        selected_object = st.selectbox("1. Оберіть об'єкт дезінфекції:", objects)
        
        # ВИВІД ПРИКЛАДІВ ДЛЯ ОБРАНОГО ОБ'ЄКТА
        filtered_df = df[df['Object_UA'] == selected_object]
        if 'Examples_UA' in df.columns and not filtered_df.empty:
            examples_text = filtered_df['Examples_UA'].iloc[0]
            if pd.notna(examples_text) and str(examples_text).strip() != "—":
                st.markdown(f"💡 **Приклади об'єктів:** *{examples_text}*")
        
        st.markdown(" ") # Відступ
        
        # 2. Фільтрація засобів под обраний об'єкт
        products = filtered_df['Product'].dropna().unique()
        selected_product = st.selectbox("2. Оберіть дезінфекційний засіб:", products)
        
        # Фінальний розрахунок результатів
        result_row = filtered_df[filtered_df['Product'] == selected_product].iloc[0]
        
        st.markdown("---")
        st.subheader("🏁 Результат розрахунку:")
        st.metric(label="Концентрація робочого розчину", value=f"{result_row['Conc_%']}")
        
        if 'Tablets' in result_row and pd.notna(result_row['Tablets']) and str(result_row['Tablets']).strip() != "—":
            st.success(f"🧫 Кількість таблеток: **{result_row['Tablets']} табл.** на 10л води")
        elif 'Volume_ml' in result_row and pd.notna(result_row['Volume_ml']) and str(result_row['Volume_ml']).strip() != "—":
            st.success(f"🧪 Кількість концентрату: **{result_row['Volume_ml']}**")
            
        if 'Method_UA' in result_row and pd.notna(result_row['Method_UA']):
            st.info(f"ℹ️ Спосіб знезараження: **{result_row['Method_UA']}**")
            
        if 'Exposure_min' in result_row and pd.notna(result_row['Exposure_min']):
            # Витягуємо чисте число для таймера зворотного відліку
            raw_exposure = str(result_row['Exposure_min'])
            exp_time = int(''.join(filter(str.isdigit, raw_exposure))) if any(char.isdigit() for char in raw_exposure) else 15
            st.warning(f"⏱️ Рекомендований час експозиції: **{exp_time} хв.**")
            
            # 🔥 ФІНАЛЬНИЙ БЛОК БОЙОВОГО ТАЙМЕРА (60 СЕКУНД НА КРОК)
            if st.button("⏱️ ЗАПУСТИТИ ТАЙМЕР ЕКСПОЗИЦІЇ"):
                progress_bar = st.progress(100)
                status_text = st.empty()
                
                total_seconds = exp_time
                for remaining in range(total_seconds, -1, -1):
                    percent = int((remaining / total_seconds) * 100)
                    progress_bar.progress(percent)
                    status_text.markdown(f"⏳ **Залишилось часу: {remaining} хв.**")
                    time.sleep(60)  # 👈 Залізна хвилина (60 секунд) для госпіталю
                    
                st.balloons()
                status_text.success("✅ Експозицію завершено! Об'єкт повністю безпечний для використання.")

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
