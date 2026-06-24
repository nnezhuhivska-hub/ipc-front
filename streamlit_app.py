import streamlit as st
import pandas as pd
import io
import time

# Налаштування сторінки під мобільний інтерфейс
st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

# 🔥 ЗАЛІЗНИЙ ПОЛЬОВИЙ КОНТРАСТ: ЧОРНЕ ТЛО ТА ВЕЛИКІ ЯСКРАВІ ТАКТИЧНІ КНОПКИ
st.markdown("""
    <style>
    /* Суворе чорне тло для максимального контрасту літер */
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    
    /* Великі яскраві заголовки */
    h1 { color: #FFFF00 !important; font-size: 34px !important; font-weight: 900 !important; }
    h2 { color: #FFFFFF !important; font-size: 26px !important; font-weight: 800 !important; }
    h3 { color: #FFFF00 !important; font-size: 24px !important; font-weight: 800 !important; }
    
    /* Підписи до кроків */
    div[data-testid="stMarkdownContainer"] p { font-size: 24px !important; font-weight: 900 !important; color: #FFFFFF !important; }
    div[data-testid="stMarkdownContainer"] strong { color: #FFFF00 !important; }
    
    /* 🔥 КНОПКИ-ПЛАШКИ ВИБОРУ: Глибоке темно-синє тло та товста жовта рамка */
    .stButton>button { 
        background-color: #001F3F !important; 
        color: #FFFFFF !important; 
        border: 4px solid #FFFF00 !important; 
        border-radius: 12px !important; 
        width: 100%; 
        min-height: 75px !important; 
        font-size: 22px !important; 
        font-weight: 900 !important; 
        text-align: left !important;
        padding: 15px !important;
        white-space: normal !important;
    }
    .stButton>button:hover { background-color: #FFFF00 !important; color: #000000 !important; }
    
    /* Величезне неонове поле результату розрахунку */
    div[data-testid="stMetricValue"] { 
        color: #00FF00 !important; 
        font-size: 56px !important; 
        font-weight: 900 !important; 
        background-color: #111111 !important; 
        padding: 20px; 
        border-radius: 10px; 
        border: 3px solid #00FF00; 
        text-align: center; 
    }
    div[data-testid="stMetricLabel"] p { color: #FFFFFF !important; font-size: 22px !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# Завантаження повної 8-мовної бази даних на 12 офіційних об'єктів (Вмонтовано в код!)
@st.cache_data
def load_data():
    raw_data = """Row_Code|Object_UA|Object_EN|Product|Contamination_Tech|Conc_%|Tablets|Volume_ml|Exposure_min|Examples_UA|Method_UA
Рядок_1|Поверхні приміщення|Surfaces of premises|Жавель-Клейд|NO|0.015%|1|—|60|підлога, стіни, ліжка, двері|Протирання або зрошення
Рядок_2|Санітарно-технічне обладнання|Sanitary equipment|Бланідас 300|YES|0.1%|7|—|60|ванни, раковини, унітази|Протирання дворазове
Рядок_3|Транспортний засіб|Vehicles and transport|Бланідас 300|NO|0.015%|1|—|30|санітарний транспорт, ноші|Протирання або зрошення
Рядок_4|Прибиральний інвентар|Cleaning equipment|Жавель Клейд|NO|0.2%|14|—|90|ганчірки, мопи, відра, швабри|Замочування з наступним пранням
Рядок_5|Засоби догляду за пацієнтами та особистої гігієни|Patient care items|Жавілар Ефект|NO|0.015%|1|—|15|гребінці, щітки, підкладні клейонки|Протирання або занурення
Рядок_6|Медичні відходи з текстильних матеріалів|Medical waste (textile)|Жавілар Ефект|YES|0.2%|14|—|60|використаний перев'язувальний матеріал, тампони|Занурення в розчин
Рядок_7|Медичні вироби із корозійностійких металів, скла|Metal and glass items|Бланідас 300|YES|0.06%|4|—|30|хірургічні інструменти, лотки, лабораторний посуд|Повне занурення
Рядок_8|Медичні вироби із корозійностійких металів, скла|Metal and glass items|Бланідас 300|NO|0.03%|2|—|60|хірургічні інструменти, лотки, лабораторний посуд|Повне занурення
Рядок_9|Медичні вироби з гуми, пластмас, синтетичних матеріалів|Rubber and plastic items|Бланідас 300|YES|0.06%|4|—|30|катетери, зонди, маски, трубки|Повне занурення
Рядок_10|Медичні вироби з гуми, пластмас, синтетичних матеріалів|Rubber and plastic items|Бланідас 300|NO|0.03%|2|—|60|катетери, зонди, маски, трубки|Повне занурення
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

df = load_data()

# Стартова сторінка
st.title("🧮 Калькулятор ВІК")
st.caption("Автономний розрахунок розчинів для польових шпиталів")

if df is not None:
    # Отримуємо залізно унікальний список усіх 12 медичних об'єктів
    objects_list = sorted(df['Object_UA'].dropna().unique())
    
    st.markdown("### 1. Оберіть об'єкт дезінфекції:")
    
    # Використовуємо сесію, щоб додаток запам'ятав клік на кнопку
    if 'selected_obj' not in st.session_state:
        st.session_state.selected_obj = objects_list[0]
        
    # 🔥 ВЕЛИКІ ТЕМНО-СИНІ КНОПКИ ЗАМІСТЬ БІЛОГО МЕНЮ
    for obj in objects_list:
        if st.button(f"▪️ {obj}"):
            st.session_state.selected_obj = obj
            
    st.markdown(f"👉 **Обрано:** `{st.session_state.selected_obj}`")
    st.markdown("---")
    
    # Робота з обраним об'єктом
    matched_rows = df[df['Object_UA'] == st.session_state.selected_obj]
    
    if not matched_rows.empty:
        # Вивід прикладів
        ex_txt = matched_rows['Examples_UA'].values[0]
        if pd.notna(ex_txt) and str(ex_txt).strip() != "—":
            st.markdown(f"💡 **Приклади об'єктів:** *{ex_txt}*")
            
        st.markdown("### 2. Оберіть дезінфекційний засіб:")
        available_products = sorted(matched_rows['Product'].dropna().unique())
        
        # Кнопки для вибору засобу
        if 'selected_prod' not in st.session_state or st.session_state.selected_prod not in available_products:
            st.session_state.selected_prod = available_products[0]
            
        for prod in available_products:
            if st.button(f"🧪 {prod}"):
                st.session_state.selected_prod = prod
                
        st.markdown(f"👉 **Обрано засіб:** `{st.session_state.selected_prod}`")
        st.markdown("---")
        
        product_rows = matched_rows[matched_rows['Product'] == st.session_state.selected_prod]
        
        # Перемикач забруднень великими кнопками
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
                
        st.markdown(f"👉 **Стан забруднення:** `{'ТАК (Посилений режим)' if st.session_state.tech_cont == 'YES' else 'НІ (Стандартний режим)'}`")
        
        # Фінальна фільтрація результату
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
