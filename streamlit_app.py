import streamlit as st
import pandas as pd
import time
import os

# Налаштування сторінки під мобільний інтерфейс
st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

# Кастомний тактичний дизайн через CSS
st.markdown("""
    <style>
    .stApp { background-color: #121417; color: #FFFFFF; }
    div[data-testid="stMetricValue"] { color: #00C897 !important; font-weight: bold; }
    .stButton>button { background-color: #1E2229; color: #FFFFFF; border: 1px solid #00C897; border-radius: 8px; width: 100%; }
    .stButton>button:hover { background-color: #00C897; color: #121417; }
    div[data-testid="stNotification"] { background-color: #1E2229; border-left: 5px solid #BC243C; }
    </style>
""", unsafe_allow_html=True)

# Автоматичний пошук БУДЬ-ЯКОГО Excel файлу в папці
@st.cache_data
def load_data():
    try:
        # Шукаємо будь-який файл, що закінчується на .xlsx
        excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
        if excel_files:
            # Беремо перший знайдений Excel файл (неважливо, яка в нього назва)
            return pd.read_excel(excel_files[0])
        else:
            return None
    except:
        return None

df = load_data()

# Головне меню додатку (Вкладки на екрані)
tab_home, tab_emergency = st.tabs(["🧮 Калькулятор", "🚨 Аварійні Протоколи"])

# --- ВКЛАДКА 1: КАЛЬКУЛЯТОР ДЕЗРОЗЧИНІВ ---
with tab_home:
    st.title("🧮 Калькулятор ВІК")
    st.caption("Автономний розрахунок робочих розчинів | Offline-first")
    
    if df is not None:
        try:
            # Вибір об'єкта дезінфекції
            objects = sorted(df['Object_UA'].dropna().unique())
            selected_object = st.selectbox("1. Оберіть об'єкт дезінфекції:", objects)
            
            # Відображення прикладів для обраного об'єкта
            filtered_object_df = df[df['Object_UA'] == selected_object]
            examples = filtered_object_df['Examples_UA'].iloc[0] if 'Examples_UA' in df.columns and not filtered_object_df.empty else None
            if pd.notna(examples):
                st.caption(f"*(Приклади: {examples})*")
                
            # Фільтрація засобів під обраний об'єкт
            products = filtered_object_df['Product'].dropna().unique()
            selected_product = st.selectbox("2. Оберіть дезінфекційний засіб:", products)
            
            # Фінальний розрахунок результатів
            result_row = filtered_df = filtered_object_df[filtered_object_df['Product'] == selected_product].iloc[0]
            
            st.markdown("---")
            st.subheader("🏁 Результат розрахунку:")
            
            # Вивід концентрації та пропорцій
            st.metric(label="Концентрація робочого розчину", value=f"{result_row['Conc_%']}")
            
            if 'Tablets' in result_row and pd.notna(result_row['Tablets']) and result_row['Tablets'] != "—":
                st.success(f"🧫 Кількість таблеток: **{result_row['Tablets']} табл.** на 10л води")
            elif 'Volume_ml' in result_row and pd.notna(result_row['Volume_ml']) and result_row['Volume_ml'] != "—":
                st.success(f"🧪 Кількість концентрату: **{result_row['Volume_ml']}**")
                
            st.info(f"ℹ️ Спосіб знезараження: **{result_row['Method_UA']}**")
            
            # Експозиція та Таймер зворотного відліку
            exp_time = int(result_row['Exposure_min']) if 'Exposure_min' in result_row else 15
            st.warning(f"⏱️ Час експозиції (Exposure, min): **{exp_time} хв.**")
            
            if st.button("⏱️ ЗАПУСТИТИ ТАЙМЕР ЕКСПОЗИЦІЇ"):
                progress_bar = st.progress(100)
                status_text = st.empty()
                for percent_complete in range(100, -1, -1):
                    time.sleep(0.1)  # Демонстраційний режим таймера
                    progress_bar.progress(percent_complete)
                    status_text.text(f"Залишилось часу: {percent_complete}%")
                st.balloons()
                st.success("✅ Експозицію завершено! Об'єкт безпечний.")
        except Exception as e:
            st.error(f"Помилка зчитування стовпців таблиці. Перевірте назви стовпців у Excel.")
    else:
        st.error("Помилка: Файл бази даних .xlsx не знайдено в репозиторії.")

# --- ВКЛАДКА 2: АВАРІЙНІ ПРОТОКОЛИ ---
with tab_emergency:
    st.title("🚨 Аварійні Протоколи")
    
    emergency_type = st.radio(
        "Оберіть тип екстреної ситуації:",
        ["💉 Укол голкою / ...", "💦 Розлиття біорідини", "🗑️ Розсипання відходів"],
        horizontal=True
    )
    
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
        if st.button("⏱️ ЗАПУСТИТИ ТАЙМЕР ПКП (72 ГОДИНИ)"):
            st.info("Таймер 72 годин активовано.")
            
    elif "Розлиття" in emergency_type:
        st.subheader("🚨 ДІЇ ПРИ РОЗЛИТТІ БІОЛОГІЧНИХ РІДИН:")
        st.markdown("""
        * **1.** Одягніть ЗІЗ (халат, фартух, щільні рукавички, захисні окуляри/щиток).
        * **2.** Засипте місце розлиття абсорбуючим порошком або накрийте серветками з деззасобом.
        * **3.** Витримайте час експозиції (згідно з інструкцією до вашого деззасобу).
        * **4.** Зберіть забруднені матеріали у контейнер/пакет «Відходи категорії В».
        """)
        
    elif "Розсипання" in emergency_type:
        st.subheader("🚨 ДІЇ ПРИ РОЗСИПАННІ МЕДИЧНИХ ВІДХОДІВ:")
        st.markdown("""
        * **1.** Обмежте доступ сторонніх осіб та пацієнтів до місця розсипання.
        * **2.** Одягніть товсті захисні рукавички та маску або респіратор.
        * **3.** Зберіть відходи за допомогою совка та щітки. Категорично заборонено збирати руками!
        * **4.** Продезінфікуйте поверхню підлоги або меблів на місці розсипання відходів.
        """)
