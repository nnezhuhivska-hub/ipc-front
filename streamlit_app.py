import streamlit as st
import pandas as pd
import io
import time

st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

# 🔥 ПОЛЬОВИЙ КОНТРАСТ: ЧОРНЕ ТЛО ТА ТЕМНО-СИНІ КОМІРКИ З ЖОВТОЮ РАМКОЮ
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1 { color: #FFFF00 !important; font-size: 34px !important; font-weight: 900 !important; }
    h2 { color: #FFFFFF !important; font-size: 26px !important; font-weight: 800 !important; }
    h3 { color: #FFFF00 !important; font-size: 24px !important; font-weight: 800 !important; }
    label[data-testid="stWidgetLabel"] p { font-size: 22px !important; font-weight: bold !important; color: #FFFFFF !important; }
    
    /* 🔥 ТЕМНО-СИНЄ ТЛО ДЛЯ КОМІРОК ВИБОРУ ТА ЯСКРАВО-ЖОВТА РАМКА */
    div[data-baseweb="select"] { 
        border: 3px solid #FFFF00 !important; 
        border-radius: 8px !important; 
        background-color: #0A192F !important; 
    }
    div[data-baseweb="select"] * { 
        color: #FFFFFF !important; 
        font-size: 20px !important; 
        font-weight: 900 !important; 
    }
    
    /* Результати розрахунків */
    div[data-testid="stMetricValue"] { color: #00FF00 !important; font-size: 52px !important; font-weight: 900 !important; background-color: #111111; padding: 15px; border-radius: 8px; border: 2px solid #00FF00; text-align: center; }
    div[data-testid="stMetricLabel"] p { color: #FFFFFF !important; font-size: 20px !important; font-weight: bold !important; }
    .stAlert { background-color: #000000 !important; border: 3px solid #00FF00 !important; border-radius: 8px !important; }
    .stAlert p { font-size: 22px !important; font-weight: 900 !important; color: #00FF00 !important; }
    div[data-testid="stMarkdownContainer"] p { font-size: 20px !important; font-weight: bold !important; color: #FFFFFF !important; }
    div[data-testid="stMarkdownContainer"] strong { color: #FFFF00 !important; }
    
    /* Жовта бойова кнопка таймера */
    .stButton>button { background-color: #FFFF00 !important; color: #000000 !important; border: 3px solid #FFFF00 !important; border-radius: 10px !important; width: 100%; height: 65px !important; font-size: 24px !important; font-weight: 900 !important; }
    .stButton>button:hover { background-color: #FFFFFF !important; color: #000000 !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        raw_data = st.secrets["database"]["data"]
        return pd.read_csv(io.StringIO(raw_data.strip()), sep="|")
    except Exception as e:
        st.error(f"Помилка завантаження даних: {e}")
        return None

df = load_data()

# Кнопка-глобус
lang_options = {
    "🇺🇦 Українська (UA)": "UA", "🇬🇧 English (EN)": "EN", "🇵🇱 Polski (PL)": "PL", "🇩🇪 Deutsch (DE)": "DE",
    "🇫🇷 Français (FR)": "FR", "🇪🇸 Español (ES)": "ES", "🇮🇹 Italiano (IT)": "IT", "🇵🇹 Português (PT)": "PT"
}
selected_lang_label = st.selectbox("🌐 Оберіть мову / Select Language:", list(lang_options.keys()))
lang = lang_options[selected_lang_label]

t = {
    "UA": {
        "title": "🧮 Калькулятор ВІК", "caption": "Автономний розрахунок розчинів",
        "step1": "1. Оберіть об'єкт дезінфекції:", "step2": "2. Оберіть дезінфекційний засіб:",
        "step3": "❓ Чи є видимі забруднення (кров, виділення тощо):", "cont_opt": ["ТАК", "НІ"],
        "examples": "💡 Приклади об'єктів:", "result": "🏁 Результат розрахунку:",
        "conc": "Концентрація робочого розчину", "tabs": ["🧮 Калькулятор", "🚨 Аварійні Протоколи"],
        "tablets": "табл. на 10л води", "method": "Спосіб знезараження", "exp": "Рекомендований час експозиції",
        "btn_timer": "⏱️ ЗАПУСТИТИ ТАЙМЕР ЕКСПОЗИЦІЇ", "timer_done": "✅ Експозицію завершено!"
    },
    "EN": {
        "title": "🧮 IPC Calculator", "caption": "Autonomous solution calculation",
        "step1": "1. Select disinfection object:", "step2": "2. Select disinfectant product:",
        "step3": "❓ Is there visible soil/contamination (blood, fluids, etc.):", "cont_opt": ["YES", "NO"],
        "examples": "💡 Examples of objects:", "result": "🏁 Calculation Result:",
        "conc": "Working solution concentration", "tabs": ["🧮 Calculator", "🚨 Emergency Protocols"],
        "tablets": "tabs per 10L of water", "method": "Disinfection method", "exp": "Recommended exposure time",
        "btn_timer": "⏱️ START EXPOSURE TIMER", "timer_done": "✅ Exposure completed!"
    },
    "PL": {
        "title": "🧮 Kalkulator IPC", "caption": "Autonomiczne obliczanie roztworów",
        "step1": "1. Wybierz obiekt dezynfekcji:", "step2": "2. Wybierz środek dezynfekujący:",
        "step3": "❓ Czy występują widoczne zanieczyszczenia (krew, płyny itp.):", "cont_opt": ["TAK", "NIE"],
        "examples": "💡 Przykłady obiektów:", "result": "🏁 Wynik obliczeń:",
        "conc": "Stężenie roztworu roboczego", "tabs": ["🧮 Kalkulator", "🚨 Protokoły awaryjne"],
        "tablets": "tabl. na 10L wody", "method": "Metoda dezynfekcji", "exp": "Zalecany czas ekspozycji",
        "btn_timer": "⏱️ URUCHOM TIMER EKSPOZYCJI", "timer_done": "✅ Ekspozycja zakończona!"
    },
    "DE": {
        "title": "🧮 IPC-Rechner", "caption": "Autonome Berechnung von Lösungen",
        "step1": "1. Desinfektionsobjekt auswählen:", "step2": "2. Desinfektionsmittel auswählen:",
        "step3": "❓ Liegt eine sichtbare Kontamination vor (Blut, Sekrete usw.):", "cont_opt": ["JA", "NEIN"],
        "examples": "💡 Objektbeispiele:", "result": "🏁 Berechnungsergebnis:",
        "conc": "Konzentration der Arbeitslösung", "tabs": ["🧮 Rechner", "🚨 Notfallprotokolle"],
        "tablets": "Tabl. pro 10L Wasser", "method": "Desinfektionsmethode", "exp": "Empfohlene Einwirkzeit",
        "btn_timer": "⏱️ BELICHTUNGSTIMER STARTEN", "timer_done": "✅ Einwirkzeit beendet!"
    },
    "FR": {
        "title": "🧮 Calculateur IPC", "caption": "Calcul autonome des solutions",
        "step1": "1. Sélectionner l'objet de désinfection:", "step2": "2. Sélectionner le désinfectant:",
        "step3": "❓ Y a-t-il une contamination visible (sang, fluides, etc.):", "cont_opt": ["OUI", "NON"],
        "examples": "💡 Exemples d'objets:", "result": "🏁 Résultat du calcul:",
        "conc": "Concentration de la solution de travail", "tabs": ["🧮 Calculateur", "🚨 Protocoles d'urgence"],
        "tablets": "comprimés pour 10L d'eau", "method": "Méthode de désinfection", "exp": "Temps d'exposition recommandé",
        "btn_timer": "⏱️ DÉMARRER LE MINUTEUR D'EXPOSITION", "timer_done": "✅ Exposition terminée!"
    },
    "ES": {
        "title": "🧮 Calculadora IPC", "caption": "Cálculo autónomo de soluciones",
        "step1": "1. Seleccione objeto de desinfección:", "step2": "2. Seleccione desinfectante:",
        "step3": "❓ ¿Hay contaminación visible (sangre, fluidos, etc.):", "cont_opt": ["SÍ", "NO"],
        "examples": "💡 Ejemplos de objetos:", "result": "🏁 Resultado del cálculo:",
        "conc": "Concentración de la solución de trabajo", "tabs": ["🧮 Calculadora", "🚨 Protocolos de emergencia"],
        "tablets": "pastillas por 10L of agua", "method": "Método de desinfección", "exp": "Tiempo de exposición recomendado",
        "btn_timer": "⏱️ INICIAR TEMPORIZADOR DE EXPOSICIÓN", "timer_done": "✅ ¡Exposición completada!"
    },
    "IT": {
        "title": "🧮 Calcolatore IPC", "caption": "Calcolo autonomo delle soluzioni",
        "step1": "1. Seleziona l'oggetto di disinfezione:", "step2": "2. Seleziona il disinfettante:",
        "step3": "❓ C'è contaminazione visibile (sangue, fluidi, ecc.):", "cont_opt": ["SÌ", "NO"],
        "examples": "💡 Esempi di oggetti:", "result": "🏁 Risultato del calcolo:",
        "conc": "Concentrazione della soluzione di lavoro", "tabs": ["🧮 Calcolatore", "🚨 Protocolli di urgenza"],
        "tablets": "compresse per 10L d'acqua", "method": "Metodo di disinfezione", "exp": "Tempo di esposizione raccomandato",
        "btn_timer": "⏱️ AVVIA TIMING DI ESPOSIZIONE", "timer_done": "✅ Esposizione completata!"
    },
    "PT": {
        "title": "🧮 Calculadora IPC", "caption": "Cálculo autónomo de soluções",
        "step1": "1. Selecione o objeto de desinfecção:", "step2": "2. Selecione o desinfetante:",
        "step3": "❓ Há contaminação visível (sangue, fluidos, etc.):", "cont_opt": ["SIM", "NÃO"],
        "result": "🏁 Resultado do cálculo:", "conc": "Concentração da solução de trabalho",
        "tabs": ["🧮 Calculadora", "🚨 Protocolos de emergência"], "tablets": "pastilhas por 10L de água",
        "method": "Método de desinfecção", "exp": "Tempo de exposição recomendado",
        "btn_timer": "⏱️ INICIAR TEMPORIZADOR DE EXPOSICIÓN", "timer_done": "✅ Exposição concluída!"
    }
}

tab_home, tab_emergency = st.tabs(t[lang]["tabs"])

with tab_home:
    st.title(t[lang]["title"])
    st.caption(t[lang]["caption"])
    
    if df is not None:
        obj_col = f"Object_{lang}" if f"Object_{lang}" in df.columns else "Object_UA"
        objects = sorted(df[obj_col].dropna().unique())
        selected_object = st.selectbox(t[lang]["step1"], objects)
        
        matched_rows = df[df[obj_col] == selected_object]
        
        # 🔥 ВИВІД ПРИКЛАДІВ ВЕРНУВ НА МІСЦЕ
        if 'Examples_UA' in df.columns and not matched_rows.empty:
            ex_txt = matched_rows['Examples_UA'].values[0]
            if pd.notna(ex_txt) and str(ex_txt).strip() != "—":
                st.markdown(f"💡 **{t[lang]['examples']}** {ex_txt}")
        
        st.markdown(" ")
        
        available_products = sorted(matched_rows['Product'].dropna().unique())
        selected_product = st.selectbox(t[lang]["step2"], available_products)
        product_rows = matched_rows[matched_rows['Product'] == selected_product]
        
        selected_cont_label = st.radio(t[lang]["step3"], t[lang]["cont_opt"], horizontal=True)
