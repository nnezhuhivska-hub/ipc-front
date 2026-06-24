import streamlit as st
import pandas as pd
import io
import time

# Налаштування сторінки під мобільний інтерфейс
st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

# 🔥 ЕКСТРЕМАЛЬНО ВИСОКОКОНТРАСТНИЙ ПОЛЬОВИЙ ДИЗАЙН
st.markdown("""
    <style>
    /* Суворе чорне тло для максимального контрасту літер */
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    
    /* Великі яскраві заголовки */
    h1 { color: #FFFF00 !important; font-size: 34px !important; font-weight: 900 !important; }
    h2 { color: #FFFFFF !important; font-size: 26px !important; font-weight: 800 !important; }
    h3 { color: #FFFF00 !important; font-size: 24px !important; font-weight: 800 !important; }
    
    /* Підписи до полів вибору */
    label[data-testid="stWidgetLabel"] p { font-size: 22px !important; font-weight: bold !important; color: #FFFFFF !important; }
    
    /* 🔥 ТЕМНО-СИНЄ ТЛО ДЛЯ КОМІРОК ВИБОРУ ТА ТОУСТА ЖОВТА РАМКА */
    div[data-baseweb="select"] { border: 4px solid #FFFF00 !important; border-radius: 8px !important; background-color: #001F3F !important; }
    div[data-baseweb="select"] * { color: #FFFFFF !important; font-size: 20px !important; font-weight: 900 !important; }
    
    /* 🔥 ТЕМНО-СИНЄ ТЛО ДЛЯ САМОГО ВИПАДАЮЧОГО ВІКНА */
    div[data-baseweb="popover"] { background-color: #001F3F !important; border: 3px solid #FFFF00 !important; border-radius: 8px !important; }
    div[data-baseweb="popover"] ul { background-color: #001F3F !important; }
    div[data-baseweb="popover"] li { background-color: #001F3F !important; color: #FFFFFF !important; font-size: 20px !important; font-weight: bold !important; padding: 12px !important; }
    div[data-baseweb="popover"] li:hover { background-color: #FFFF00 !important; color: #000000 !important; }
    
    /* Радіо-кнопки вибору забруднення */
    div[data-testid="stMarkdownContainer"] p { font-size: 22px !important; font-weight: bold !important; color: #FFFFFF !important; }
    div[data-testid="stMarkdownContainer"] strong { color: #FFFF00 !important; }
    
    /* Результати розрахунків */
    div[data-testid="stMetricValue"] { color: #00FF00 !important; font-size: 54px !important; font-weight: 900 !important; background-color: #111111 !important; padding: 15px; border-radius: 8px; border: 2px solid #00FF00; text-align: center; }
    div[data-testid="stMetricLabel"] p { color: #FFFFFF !important; font-size: 20px !important; font-weight: bold !important; }
    
    /* Головна жовта кнопка калькулятора */
    .stButton>button { background-color: #FFFF00 !important; color: #000000 !important; border: 3px solid #FFFF00 !important; border-radius: 10px !important; width: 100%; height: 65px !important; font-size: 24px !important; font-weight: 900 !important; }
    
    /* 🔥 ТАКТИЧНИЙ ЧЕРВОНИЙ ТАЙМЕР НА ЧОРНОМУ ТЛІ В ТОНЕНЬКІЙ ЧЕРВОНІЙ РАМЦІ */
    .tactical-timer {
        background-color: #000000 !important;
        color: #FF0000 !important;
        border: 2px solid #FF0000 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-top: 15px !important;
        box-shadow: 0 0 10px #FF0000;
    }
    </style>
""", unsafe_allow_html=True)

# Завантаження повної бази із Секретів
@st.cache_data
def load_data_from_secrets():
    try:
        raw_data = st.secrets["database"]["data"]
        return pd.read_csv(io.StringIO(raw_data.strip()), sep="|")
    except Exception as e:
        st.error(f"Помилка завантаження даних: {e}")
        return None

df = load_data_from_secrets()

# КНОПКА-ГЛОБУС ДЛЯ ВИБОРУ МОВИ
lang_options = {
    "🇺🇦 Українська (UA)": "UA", "🇬🇧 English (EN)": "EN", "🇵🇱 Polski (PL)": "PL", "🇩🇪 Deutsch (DE)": "DE",
    "🇫🇷 Français (FR)": "FR", "🇪🇸 Español (ES)": "ES", "🇮🇹 Italiano (IT)": "IT", "🇵🇹 Português (PT)": "PT"
}
selected_lang_label = st.selectbox("🌐 Оберіть мову / Select Language:", list(lang_options.keys()))
lang = lang_options[selected_lang_label]

# Завантажуємо тексти інтерфейсу з Секретів
try:
    title_text = st.secrets["translations"][f"title_{lang}"]
    caption_text = st.secrets["translations"][f"caption_{lang}"]
    step1_text = st.secrets["translations"][f"step1_{lang}"]
    step2_text = st.secrets["translations"][f"step2_{lang}"]
    step3_text = st.secrets["translations"][f"step3_{lang}"]
    cont_yes = st.secrets["translations"][f"yes_{lang}"]
    cont_no = st.secrets["translations"][f"no_{lang}"]
    result_text = st.secrets["translations"][f"result_{lang}"]
    conc_text = st.secrets["translations"][f"conc_{lang}"]
    tablets_text = st.secrets["translations"][f"tablets_{lang}"]
    method_text_lbl = st.secrets["translations"][f"method_{lang}"]
    exp_text_lbl = st.secrets["translations"][f"exp_{lang}"]
    btn_timer_text = st.secrets["translations"][f"btn_timer_{lang}"]
    timer_done_text = st.secrets["translations"][f"timer_done_{lang}"]
    tab1_name = st.secrets["translations"][f"tab1_{lang}"]
    tab2_name = st.secrets["translations"][f"tab2_{lang}"]
    examples_lbl = st.secrets["translations"][f"examples_{lang}"]
except:
    title_text, caption_text, step1_text, step2_text, step3_text = "Калькулятор ВІК", "Розрахунок розчинів", "1. Об'єкт:", "2. Засіб:", "❓ Забруднення:"
    cont_yes, cont_no, result_text, conc_text, tablets_text = "ТАК", "НІ", "🏁 Результат:", "Концентрація", "табл."
    method_text_lbl, exp_text_lbl, btn_timer_text, timer_done_text = "Спосіб", "Час експозиції", "⏱️ ЗАПУСТИТИ ТАЙМЕР", "✅ Готово!"
    tab1_name, tab2_name, examples_lbl = "🧮 Калькулятор", "🚨 Протоколи", "💡 Приклади:"

tab_home, tab_emergency = st.tabs([tab1_name, tab2_name])

# --- ВКЛАДКА 1: КАЛЬКУЛЯТОР ДЕЗРОЗЧИНІВ ---
with tab_home:
    st.title(title_text)
    st.caption(caption_text)
    
    if df is not None:
        obj_col = f"Object_{lang}" if f"Object_{lang}" in df.columns else "Object_UA"
        objects = sorted(df[obj_col].dropna().unique())
        selected_object = st.selectbox(step1_text, objects)
        
        matched_rows = df[df[obj_col] == selected_object]
        
        # ВИВІД ПРИКЛАДІВ ОБ'ЄКТІВ
        if 'Examples_UA' in df.columns and not matched_rows.empty:
            ex_txt = matched_rows['Examples_UA'].values[0]
            if pd.notna(ex_txt) and str(ex_txt).strip() != "—":
                st.markdown(f"💡 **{examples_lbl}** *{ex_txt}*")
        
        st.markdown(" ")
        
        available_products = sorted(matched_rows['Product'].dropna().unique())
        selected_product = st.selectbox(step2_text, available_products)
        product_rows = matched_rows[matched_rows['Product'] == selected_product]
        
        selected_cont_label = st.radio(step3_text, [cont_yes, cont_no], horizontal=True)
        tech_cont = "YES" if selected_cont_label == cont_yes else "NO"
        
        final_row_df = product_rows[product_rows['Contamination_Tech'] == tech_cont]
        if final_row_df.empty and not product_rows.empty:
            final_row_df = product_rows
            
        if not final_row_df.empty:
            final_row = final_row_df.reset_index(drop=True).iloc[0]
            st.markdown("---")
            st.subheader(result_text)
            st.metric(label=conc_text, value=f"{final_row['Conc_%']}")
            st.markdown(" ")
            
            if 'Tablets' in final_row and pd.notna(final_row['Tablets']) and str(final_row['Tablets']).strip() != "—":
                st.success(f"🧫 КІЛЬКІСТЬ: {final_row['Tablets']} {tablets_text}")
            elif 'Volume_ml' in final_row and pd.notna(final_row['Volume_ml']) and str(final_row['Volume_ml']).strip() != "—":
                st.success(f"🧪 КІЛЬКІСТЬ: {final_row['Volume_ml']}")
                
            meth_col = f"Method_{lang}" if f"Method_{lang}" in df.columns else "Method_UA"
            method_text = final_row[meth_col] if meth_col in final_row else final_row['Method_UA']
            st.markdown(f"ℹ️ **{method_text_lbl}:** {method_text}")
            
            if 'Exposure_min' in final_row and pd.notna(final_row['Exposure_min']):
                raw_exposure = str(final_row['Exposure_min'])
                exp_time = int(''.join(filter(str.isdigit, raw_exposure))) if any(char.isdigit() for char in raw_exposure) else 15
                st.markdown(f"⏱️ **{exp_text_lbl}:** {exp_time} min.")
                st.markdown(" ")
                
                if st.button(btn_timer_text):
                    progress_bar = st.progress(100)
                    status_placeholder = st.empty()
                    total_seconds = exp_time
                    for remaining in range(total_seconds, -1, -1):
                        percent = int((remaining / total_seconds) * 100)
                        progress_bar.progress(percent)
                        status_placeholder.markdown(f'<div class="tactical-timer">⏳ ЗАЛИШИЛОСЬ ЧАСУ: {remaining} ХВ.</div>', unsafe_allow_html=True)
                        time.sleep(60)
                    st.balloons()
                    status_placeholder.markdown(f'<div class="tactical-timer" style="color:#00FF00 !important; border-color:#00FF00 !important; box-shadow: 0 0 10px #00FF00;">{timer_done_text}</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ No data.")

# --- ВКЛАДКА 2: АВАРІЙНІ ПРОТОКОЛИ ---
with tab_emergency:
    st.title("🚨 Аварійні Протоколи")
    st.markdown("""
    * **💉 Укол голкою / Поріз**: Промийте рану великою кількістю води з милом. Обробіть шкіру 70% спиртом. Закрийте пластирем. Вікно ПКП — 72 години!
    * **💦 Розлиття біорідини**: Одягніть ЗІЗ. Засипте абсорбентом або накрийте серветками з деззасобом. Витримайте час експозиції. Зберіть у контейнер «Категорія В».
    * **🗑️ Розсипання відходів**: Обмежте доступ. Одягніть захисні рукавички. Зберіть за допомогою совка та щітки. Продезінфікуйте поверхню.
