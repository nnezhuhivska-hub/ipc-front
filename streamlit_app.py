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

# Глобальний перемикач мови у самому верху додатку
lang = st.radio("🌍 Мова / Language:", ["UA", "EN"], horizontal=True)

# Словник інтерфейсу
t = {
    "UA": {
        "title": "🧮 Калькулятор ВІК", "caption": "Автономний розрахунок робочих розчинів",
        "step1": "1. Оберіть об'єкт дезінфекції:", "step2": "2. Оберіть дезінфекційний засіб:",
        "examples": "💡 **Приклади об'єктів:**", "result": "🏁 Результат розрахунку:",
        "conc": "Концентрація робочого розчину", "tabs": ["🧮 Калькулятор", "🚨 Аварійні Протоколи"],
        "tab2_title": "🚨 Аварійні Протоколи", "tab2_select": "Оберіть тип ситуації:",
        "tab2_opt": ["💉 Укол / Поріз", "💦 Розлиття біорідини", "🗑️ Розсипання відходів"],
        "tablets": "табл. на 10л води", "method": "Спосіб знезараження", "exp": "Рекомендований час експозиції",
        "btn_timer": "⏱️ ЗАПУСТИТИ ТАЙМЕР ЕКСПОЗИЦІЇ", "timer_done": "✅ Експозицію завершено! Об'єкт повністю безпечний."
    },
    "EN": {
        "title": "🧮 IPC Calculator", "caption": "Autonomous calculation of working solutions",
        "step1": "1. Select disinfection object:", "step2": "2. Select disinfectant product:",
        "examples": "💡 **Examples of objects:**", "result": "🏁 Calculation Result:",
        "conc": "Working solution concentration", "tabs": ["🧮 Calculator", "🚨 Emergency Protocols"],
        "tab2_title": "🚨 Emergency Protocols", "tab2_select": "Select emergency type:",
        "tab2_opt": ["💉 Needle stick / Cut", "💦 Bioliquid spill", "🗑️ Waste spillage"],
        "tablets": "tabs per 10L of water", "method": "Disinfection method", "exp": "Recommended exposure time",
        "btn_timer": "⏱️ START EXPOSURE TIMER", "timer_done": "✅ Exposure completed! Object is fully safe."
    }
}

# Визначаємо назви стовпчиків залежно від мови
obj_col = "Object_UA" if lang == "UA" else "Object_EN"

# Головне меню додатку (Вкладки)
tab_home, tab_emergency = st.tabs(t[lang]["tabs"])

# --- ВКЛАДКА 1: КАЛЬКУЛЯТОР ДЕЗРОЗЧИНІВ ---
with tab_home:
    st.title(t[lang]["title"])
    st.caption(t[lang]["caption"])
    
    if df is not None:
        # 1. Вибір об'єкта дезінфекції
        objects = sorted(df[obj_col].dropna().unique())
        selected_object = st.selectbox(t[lang]["step1"], objects)
        
        # ВИВІД ПРИКЛАДІВ ДЛЯ ОБРАНОГО ОБ'ЄКТА
        filtered_df = df[df[obj_col] == selected_object]
        if 'Examples_UA' in df.columns and not filtered_df.empty:
            examples_text = filtered_df['Examples_UA'].iloc[0] # Тимчасово показуємо UA приклади
            st.markdown(f"{t[lang]['examples']} *{examples_text}*")
        
        st.markdown(" ")
        
        # 2. Фільтрація засобів під обраний об'єкт
        products = filtered_df['Product'].dropna().unique()
        selected_product = st.selectbox(t[lang]["step2"], products)
        
        # Фінальний розрахунок результатів
        result_row = filtered_df[filtered_df['Product'] == selected_product].iloc[0]
        
        st.markdown("---")
        st.subheader(t[lang]["result"])
        st.metric(label=t[lang]["conc"], value=f"{result_row['Conc_%']}")
        
        if 'Tablets' in result_row and pd.notna(result_row['Tablets']) and str(result_row['Tablets']).strip() != "—":
            st.success(f"🧫 {result_row['Tablets']} {t[lang]['tablets']}")
        elif 'Volume_ml' in result_row and pd.notna(result_row['Volume_ml']) and str(result_row['Volume_ml']).strip() != "—":
            st.success(f"🧪 {result_row['Volume_ml']}")
            
        st.info(f"ℹ️ {t[lang]['method']}: **{result_row['Method_UA']}**")
        
        if 'Exposure_min' in result_row and pd.notna(result_row['Exposure_min']):
            raw_exposure = str(result_row['Exposure_min'])
            exp_time = int(''.join(filter(str.isdigit, raw_exposure))) if any(char.isdigit() for char in raw_exposure) else 15
            st.warning(f"⏱️ {t[lang]['exp']}: **{exp_time} min.**")
            
            if st.button(t[lang]["btn_timer"]):
                progress_bar = st.progress(100)
                status_text = st.empty()
                total_seconds = exp_time
                for remaining in range(total_seconds, -1, -1):
                    percent = int((remaining / total_seconds) * 100)
                    progress_bar.progress(percent)
                    status_text.markdown(f"⏳ **{remaining} min.**")
                    time.sleep(60) # 60 секунд для шпиталю
                    
                st.balloons()
                status_text.success(t[lang]["timer_done"])

# --- ВКЛАДКА 2: АВАРІЙНІ ПРОТОКОЛИ ---
with tab_emergency:
    st.title(t[lang]["tab2_title"])
    emergency_type = st.radio(t[lang]["tab2_select"], t[lang]["tab2_opt"], horizontal=True)
    st.markdown("---")
    
    if "Укол" in emergency_type or "Needle" in emergency_type:
        st.subheader("🚨 EMERGENCY ACTIONS FOR NEEDLE STICK / CUT:")
        st.markdown("""
        * **1.** DO NOT PANIC! Stop the procedure. Do not squeeze or rub the injury site!
        * **2.** Wash the wound with plenty of water and soap under running water (min 3 min).
        * **3.** Treat skin with 70% alcohol or skin antiseptic. Do not pour iodine deep into the wound!
        * **4.** Cover the wound with a waterproof plaster.
        """)
        st.error("⚠️ PEP EFFICIENCY WINDOW IS 72 HOURS!")
