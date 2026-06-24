import streamlit as st
import pandas as pd
import io
import time

st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    h1 { color: #FFFF00 !important; font-size: 34px !important; font-weight: 900 !important; }
    h2 { color: #FFFFFF !important; font-size: 26px !important; font-weight: 800 !important; }
    h3 { color: #FFFF00 !important; font-size: 24px !important; font-weight: 800 !important; }
    label[data-testid="stWidgetLabel"] p { font-size: 22px !important; font-weight: bold !important; color: #FFFFFF !important; }
    
    /* ТЕМНО-СИНЄ ТЛО ДЛЯ КОМІРОК ВИБОРУ ТА ТОУСТА ЖОВТА РАМКА */
    div[data-baseweb="select"] { border: 4px solid #FFFF00 !important; border-radius: 8px !important; background-color: #001F3F !important; }
    div[data-baseweb="select"] * { color: #FFFFFF !important; font-size: 20px !important; font-weight: 900 !important; }
    
    /* ТЕМНО-СИНЄ ТЛО ДЛЯ САМОГО ВИПАДАЮЧОГО ВІКНА (ПЕРЕФАРБОВУЄМО МЕНЮ) */
    div[data-baseweb="popover"] { background-color: #001F3F !important; border: 3px solid #FFFF00 !important; border-radius: 8px !important; }
    div[data-baseweb="popover"] ul { background-color: #001F3F !important; }
    div[data-baseweb="popover"] li { background-color: #001F3F !important; color: #FFFFFF !important; font-size: 20px !important; font-weight: bold !important; padding: 12px !important; }
    div[data-baseweb="popover"] li:hover { background-color: #FFFF00 !important; color: #000000 !important; }
    
    /* Великі яскраві кнопки ТАК / НІ */
    div[data-testid="stHorizontalBlock"] .stButton>button { background-color: #001F3F !important; color: #FFFFFF !important; border: 3px solid #FFFF00 !important; border-radius: 10px !important; height: 60px !important; font-size: 22px !important; font-weight: 900 !important; }
    div[data-testid="stHorizontalBlock"] .stButton>button:hover { background-color: #FFFF00 !important; color: #000000 !important; }
    
    /* Результати та таймер */
    div[data-testid="stMetricValue"] { color: #00FF00 !important; font-size: 54px !important; font-weight: 900 !important; background-color: #111111 !important; padding: 15px; border-radius: 8px; border: 2px solid #00FF00; text-align: center; }
    div[data-testid="stMetricLabel"] p { color: #FFFFFF !important; font-size: 20px !important; font-weight: bold !important; }
    div[data-testid="stMarkdownContainer"] p { font-size: 22px !important; font-weight: bold !important; color: #FFFFFF !important; }
    div[data-testid="stMarkdownContainer"] strong { color: #FFFF00 !important; }
    .stButton>button { background-color: #FFFF00 !important; color: #000000 !important; border: 3px solid #FFFF00 !important; border-radius: 10px !important; width: 100%; height: 65px !important; font-size: 24px !important; font-weight: 900 !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        raw_data = st.secrets["database"]["data"]
        return pd.read_csv(io.StringIO(raw_data.strip()), sep="|")
    except Exception as e:
        st.error(f"Помилка завантаження даних із Секретів: {e}")
        return None

df = load_data()

st.title("🧮 Калькулятор ВІК")
st.caption("Автономний розрахунок розчинів для польових шпиталів")

if df is not None:
    objects_list = sorted(df['Object_UA'].dropna().unique())
    selected_object = st.selectbox("1. Оберіть об'єкт дезінфекції:", objects_list)
    
    matched_rows = df[df['Object_UA'] == selected_object]
    
    if not matched_rows.empty:
        ex_txt = matched_rows['Examples_UA'].values[0]
        if pd.notna(ex_txt) and str(ex_txt).strip() != "—":
            st.markdown(f"💡 **Приклади об'єктів:** *{ex_txt}*")
        
        st.markdown(" ")
        
        available_products = sorted(matched_rows['Product'].dropna().unique())
        selected_product = st.selectbox("2. Оберіть дезінфекційний засіб:", available_products)
        product_rows = matched_rows[matched_rows['Product'] == selected_product]
        
        st.markdown(" ")
        
        st.markdown("### 3. Чи є видимі забруднення (кров, виділення тощо):")
        col1, col2 = st.columns(2)
        if 'tech_cont' not in st.session_state:
            st.session_state.tech_cont = "NO"
            
        with col1:
            if st.button("🔴 ТАК"):
                st.session_state.tech_cont = "YES"
        with col2:
            if st.button("🟢 НІ"):
                st.session_state.tech_cont = "NO"
                
        st.markdown(f"👉 **Обрано стан забруднення:** `{'ТАК (Посилений режим)' if st.session_state.tech_cont == 'YES' else 'НІ (Стандартний режим)'}`")
        
        final_row_df = product_rows[product_rows['Contamination_Tech'] == st.session_state.tech_cont]
        if final_row_df.empty and not product_rows.empty:
            final_row_df = product_rows
            
        if not final_row_df.empty:
            final_row = final_row_df.reset_index(drop=True).iloc[0]
            st.markdown("---")
            st.subheader("🏁 Результат розрахунку:")
            st.metric(label="Концентрація робочого розчину", value=f"{final_row['Conc_%']}")
            st.markdown(" ")
            
            if 'Tablets' in final_row and pd.notna(final_row['Tablets']) and str(final_row['Tablets']).strip() != "—":
                st.success(f"🧫 КІЛЬКІСТЬ: {final_row['Tablets']} табл. на 10л води")
            elif 'Volume_ml' in final_row and pd.notna(final_row['Volume_ml']) and str(final_row['Volume_ml']).strip() != "—":
                st.success(f"🧪 КІЛЬКІСТЬ: {final_row['Volume_ml']}")
                
            st.markdown(f"ℹ️ **Спосіб знезараження:** {final_row['Method_UA']}")
            
            if 'Exposure_min' in final_row and pd.notna(final_row['Exposure_min']):
                raw_exposure = str(final_row['Exposure_min'])
                exp_time = int(''.join(filter(str.isdigit, raw_exposure))) if any(char.isdigit() for char in raw_exposure) else 15
                st.markdown(f"⏱️ **Рекомендований час експозиції:** {exp_time} хв.")
                st.markdown(" ")
                
                if st.button("⏱️ ЗАПУСТИТИ ТАЙМЕР ЕКСПОЗИЦІЇ"):
                    progress_bar = st.progress(100)
                    status_text = st.empty()
                    total_seconds = exp_time
                    for remaining in range(total_seconds, -1, -1):
                        percent = int((remaining / total_seconds) * 100)
                        progress_bar.progress(percent)
                        status_text.markdown(f"⏳ **{remaining} min.**")
                        time.sleep(60)
                    st.balloons()
                    status_text.success("✅ Експозицію завершено! Об'єкт повністю безпечний.")
