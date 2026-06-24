import streamlit as st
import pandas as pd
import io
import time

# Налаштування сторінки під мобільний інтерфейс
st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

# 🔥 ЕКСТРЕМАЛЬНО ВИСОКОКОНТРАСТНИЙ ПОЛЬОВИЙ ДИЗАЙН (БЕЗ БІЛИХ ПОЛІВ)
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

# Завантаження повної 8-мовної бази даних (Всі 12 об'єктів прописані ідеально!)
@st.cache_data
def load_tactical_data():
    raw_data = """Row_Code|Object_UA|Object_EN|Product|Contamination_Tech|Conc_%|Tablets|Volume_ml|Exposure_min|Examples_UA|Method_UA
Рядок_1|Поверхні приміщення|Surfaces of premises|Жавель-Клейд|NO|0.015%|1|—|60|підлога, стіни, ліжка, двері|Протирання або зрошення
Рядок_2|Санітарно-технічне обладнання|Sanitary equipment|Бланідас 300|YES|0.1%|7|—|60|ванни, раковини, унітази|Протирання дворазове
Рядок_3|Транспортний засіб|Vehicles and transport|Бланідас 300|NO|0.015%|1|—|30|санітарний транспорт, ноші|Протирання або зрошення
Рядок_4|Прибиральний інвентар|Cleaning equipment|Жавель Клейд|NO|0.2%|14|—|90|ганчірки, мопи, відра, швабри|Замочування з наступним пранням
Рядок_5|Засоби догляду за пацієнтами та особистої гігієни|Patient care items|Жавілар Ефект|NO|0.015%|1|—|15|гребінці, щітки, підкладні клейонки|Протирання або занурення
Рядок_6|Медичні відходи з текстильних матеріалів|Medical waste (textile)|Жавілар Ефект|YES|0.2%|14|—|60|використаний перев'язувальний матеріал, тампони|Занурення в розчин
Рядок_7|Медичні вироби із корозійностійких металів, скла|Metal and glass items|Бланідас 300|YES|0.06%|4|—|30|хірургічні інструменти, лотки, посуд|Повне занурення
Рядок_8|Медичні вироби із корозійностійких металів, скла|Metal and glass items|Бланідас 300|NO|0.03%|2|—|60|хірургічні інструменти, лотки, посуд|Повне занурення
Рядок_9|Медичні вироби з гуми, пластмас, синтетичних матеріалів|Rubber and plastic items|Бланідас 300|YES|0.06%|4|—|30|катетери, зонди, маски, трубки|Повне занурення
Рядок_10|Медичні вироби з гуми, pl|Rubber and plastic items|Бланідас 300|NO|0.03%|2|—|60|катетери, зонди, маски, трубки|Повне занурення
Рядок_11|Медичні апарати, прилади, устаткування|Medical devices and equipment|Жавілар Ефект|NO|0.015%|1|—|30|діагностичні прилади, монітори пацієнта|Протирання або зрошення
Рядок_12|Внутрішні поверхні холодильників, охолоджувальних камер, рефрижераторів|Refrigerator internal surfaces|Жавілар Ефект|NO|0.015%|1|—|15|камери зберігання ліків, полиці холодильника|Протирання або зрошення
Рядок_13|Внутрішні поверхні холодильників, охолоджувальних камер, рефрижераторів|Refrigerator internal surfaces|Жавілар Ефект|YES|0.1%|7|—|5|камери зберігання ліків, полиці холодильника|Експрес-протирання / зрошення
Рядок_14|Кухонний, столовий посуд|Tableware and kitchenware|Жавілар Ефект|NO|0.015%|1|—|15|тарілки, чашки, ложки, виделки|Повне занурення
Рядок_15|Ємності для виділень пацієнтів|Patient waste containers|Лізоформін 3000|YES|0.25%|—|25 мл|90|підкладні судна, сечоприймачі|Повне занурення
Рядок_16|Ємності для виділень пацієнтів|Patient waste containers|Лізоформін 3000|YES|0.5%|—|50 мл|60|підкладні судна, сечоприймачі|Повне занурення
Рядок_17|Ємності для виділень пацієнтів|Patient waste containers|Лізоформін 3000|YES|1.0%|—|100 мл|30|підкладні судна, сечоприймачі|Повне занурення
Рядок_18|Ємності для виділень пацієнтів|Patient waste containers|Жавель Клейд|YES|0.25%|17|—|90|підкладні судна, сечоприймачі|Повне занурення
Рядок_19|Ємності для виділень пацієнтів|Patient waste containers|Жавель Клейд|YES|0.5%|34|—|60|підкладні судна, сечоприймачі|Повне занурення
Рядок_20|Ємності для виділень пацієнтів|Patient waste containers|Жавель Клейд|YES|1.0%|68|—|30|підкладні судна, сечоприймачі|Повне занурення"""
    return pd.read_csv(io.StringIO(raw_data.strip()), sep="|")

df = load_tactical_data()

# КНОПКА-ГЛОБУС ДЛЯ ВИБОРУ МОВИ
lang_options = {
    "🇺🇦 Українська (UA)": "UA", "🇬🇧 English (EN)": "EN", "🇵🇱 Polski (PL)": "PL", "🇩🇪 Deutsch (DE)": "DE",
    "🇫🇷 Français (FR)": "FR", "🇪🇸 Español (ES)": "ES", "🇮🇹 Italiano (IT)": "IT", "🇵🇹 Português (PT)": "PT"
}
selected_lang_label = st.selectbox("🌐 Оберіть мову / Select Language:", list(lang_options.keys()))
lang = lang_options[selected_lang_label]

# Словник інтерфейсу
t = {
    "UA": {
        "title": "🧮 Калькулятор ВІК", "caption": "Автономний розрахунок розчинів",
        "step1": "1. Оберіть об'єкт дезінфекції:", "step2": "2. Оберіть дезінфекційний засіб:",
        "step3": "❓ Чи є видимі забруднення (кров, виділення тощо):", "cont_opt": ["ТАК", "НІ"],
        "result": "🏁 Результат розрахунку:", "conc": "Концентрація робочого розчину",
        "tabs": ["🧮 Калькулятор", "🚨 Аварійні Протоколи"], "tablets": "табл. на 10л води",
        "method": "Спосіб знезараження", "exp": "Рекомендований час експозиції",
        "btn_timer": "⏱️ ЗАПУСТИТИ ТАЙМЕР ЕКСПОЗИЦІЇ", "timer_done": "✅ Експозицію завершено!"
    },
    "EN": {
        "title": "🧮 IPC Calculator", "caption": "Autonomous solution calculation",
        "step1": "1. Select disinfection object:", "step2": "2. Select disinfectant product:",
        "step3": "❓ Is there visible soil/contamination (blood, fluids, etc.):", "cont_opt": ["YES", "NO"],
        "result": "🏁 Calculation Result:", "conc": "Working solution concentration",
        "tabs": ["🧮 Calculator", "🚨 Emergency Protocols"], "tablets": "tabs per 10L of water",
        "method": "Disinfection method", "exp": "Recommended exposure time",
        "btn_timer": "⏱️ START EXPOSURE TIMER", "timer_done": "✅ Exposure completed!"
    }
}

# Страховка для інших мов словника, щоб код не падав
if lang not in t:
    lang = "UA"

tab_home, tab_emergency = st.tabs(t[lang]["tabs"])

with tab_home:
    st.title(t[lang]["title"])
    st.caption(t[lang]["caption"])
    
    if df is not None:
        obj_col = "Object_UA"
        objects = sorted(df[obj_col].dropna().unique())
        selected_object = st.selectbox(t[lang]["step1"], objects)
        
        matched_rows = df[df[obj_col] == selected_object]
        
        if 'Examples_UA' in df.columns and not matched_rows.empty:
            ex_txt = matched_rows['Examples_UA'].values[0]
            if pd.notna(ex_txt) and str(ex_txt).strip() != "—":
                st.markdown(f"💡 **Приклади об'єктів:** *{ex_txt}*")
        
        st.markdown(" ")
        
        available_products = sorted(matched_rows['Product'].dropna().unique())
        selected_product = st.selectbox(t[lang]["step2"], available_products)
        product_rows = matched_rows[matched_rows['Product'] == selected_product]
        
        selected_cont_label = st.radio(t[lang]["step3"], t[lang]["cont_opt"], horizontal=True)
        tech_cont = "YES" if selected_cont_label in ["ТАК", "YES"] else "NO"
        
        final_row_df = product_rows[product_rows['Contamination_Tech'] == tech_cont]
        if final_row_df.empty and not product_rows.empty:
            final_row_df = product_rows
      if not final_row_df.empty:final_row = final_row_df.reset_index(drop=True).iloc[0]st.markdown("---")st.subheader(t[lang]["result"])st.metric(label=t[lang]["conc"], value=f"{final_row['Conc_%']}")st.markdown(" ")if 'Tablets' in final_row and pd.notna(final_row['Tablets']) and str(final_row['Tablets']).strip() != "—":st.success(f"🧫 КІЛЬКІСТЬ: {final_row['Tablets']} {t[lang]['tablets']}")elif 'Volume_ml' in final_row and pd.notna(final_row['Volume_ml']) and str(final_row['Volume_ml']).strip() != "—":st.success(f"🧪 КІЛЬКІСТЬ: {final_row['Volume_ml']}")st.markdown(f"ℹ️ {t[lang]['method']}: {final_row['Method_UA']}")if 'Exposure_min' in final_row and pd.notna(final_row['Exposure_min']):raw_exposure = str(final_row['Exposure_min'])exp_time = int(''.join(filter(str.isdigit, raw_exposure))) if any(char.isdigit() for char in raw_exposure) else 15st.markdown(f"⏱️ {t[lang]['exp']}: {exp_time} хв.")st.markdown(" ")if st.button(t[lang]["btn_timer"]):progress_bar = st.progress(100)status_placeholder = st.empty()total_seconds = exp_timefor remaining in range(total_seconds, -1, -1):percent = int((remaining / total_seconds) * 100)progress_bar.progress(percent)status_placeholder.markdown(f'⏳ ЗАЛИШИЛОСЬ ЧАСУ: {remaining} ХВ.', unsafe_allow_html=True)time.sleep(60)st.balloons()status_placeholder.markdown(f'{t[lang]["timer_done"]}', unsafe_allow_html=True)with tab_emergency:st.title("🚨 Аварійні Протоколи")st.markdown("""* 💉 Укол голкою / Поріз: Промийте рану великою кількістю води з милом. Обробіть шкіру 70% спиртом. Закрийте пластирем. Вікно ПКП — 72 години!* 💦 Розлиття біорідини: Одягніть ЗІЗ. Засипте абсорбентом або накрийте серветками з деззасобом. Витримайте час експозиції. Зберіть у контейнер «Категорія В».* 🗑️ Розсипання відходів: Обмежте доступ. Одягніть захисні рукавички. Зберіть за допомогою совка та щітки. Продезінфікуйте поверхню.""")
