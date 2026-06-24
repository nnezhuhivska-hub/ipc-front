import streamlit as st
import pandas as pd
import io
import time

# Налаштування сторінки під мобільний інтерфейс
st.set_page_config(page_title="ВІК Фронт / IPC Front", page_icon="🛡️", layout="centered")

# 🔥 ЕКСТРЕМАЛЬНО ВИСОКОКОНТРАСТНИЙ ДИЗАЙН ДЛЯ ПОЛЬОВИХ УМОВ (Tactical High-Contrast)
st.markdown("""
    <style>
    /* Глибоке чорне тло для максимального контрасту літер */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Збільшені та жирні заголовки */
    h1 { color: #FFFF00 !important; font-size: 32px !important; font-weight: 900 !important; text-shadow: 2px 2px #000000; }
    h2 { color: #FFFFFF !important; font-size: 26px !important; font-weight: 800 !important; }
    h3 { color: #FFFF00 !important; font-size: 22px !important; font-weight: 800 !important; }
    
    /* Великі білі підписи до випадаючих списків */
    label[data-testid="stWidgetLabel"] p { font-size: 20px !important; font-weight: bold !important; color: #FFFFFF !important; }
    
    /* Яскраві рамки для полів вибору */
    div[data-baseweb="select"] { border: 2px solid #FFFF00 !important; border-radius: 8px !important; background-color: #111111 !important; }
    div[data-baseweb="select"] * { color: #FFFFFF !important; font-size: 18px !important; font-weight: bold !important; }
    
    /* Величезний кислотно-зелений індикатор результату розрахунку */
    div[data-testid="stMetricValue"] { color: #00FF00 !important; font-size: 48px !important; font-weight: 900 !important; background-color: #111111; padding: 10px; border-radius: 8px; border: 1px solid #00FF00; text-align: center; }
    div[data-testid="stMetricLabel"] p { color: #FFFFFF !important; font-size: 18px !important; font-weight: bold !important; }
    
    /* Сигнальні плашки результатів */
    .stAlert { background-color: #111111 !important; border: 2px solid #00FF00 !important; border-radius: 8px !important; }
    .stAlert p { font-size: 20px !important; font-weight: bold !important; color: #00FF00 !important; }
    
    /* Велика тактична кнопка таймера (Яскраво-жовта з чорним текстом) */
    .stButton>button { background-color: #FFFF00 !important; color: #000000 !important; border: 2px solid #FFFF00 !important; border-radius: 10px !important; width: 100%; height: 60px !important; font-size: 22px !important; font-weight: 900 !important; }
    .stButton>button:hover { background-color: #FFFFFF !important; border-color: #FFFFFF !important; }
    
    /* Радіо-кнопки вибору мови та протоколів */
    div[data-testid="stMarkdownContainer"] p { font-size: 18px !important; }
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

# КНОПКА-ГЛОБУС ДЛЯ ВИБОРУ МОВИ
lang_options = {
    "🇺🇦 Українська (UA)": "UA",
    "🇬🇧 English (EN)": "EN",
    "🇵🇱 Polski (PL)": "PL",
    "🇩🇪 Deutsch (DE)": "DE",
    "🇫🇷 Français (FR)": "FR",
    "🇪🇸 Español (ES)": "ES",
    "🇮🇹 Italiano (IT)": "IT",
    "🇵🇹 Português (PT)": "PT"
}
selected_lang_label = st.selectbox("🌐 Оберіть мову / Select Language:", list(lang_options.keys()))
lang = lang_options[selected_lang_label]

# Словник інтерфейсу на 8 мов
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
        "tablets": "pastillas por 10L de agua", "method": "Método de desinfección", "exp": "Tiempo de exposición recomendado",
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
        "examples": "💡 Exemplos de objetos:", "result": "🏁 Resultado do cálculo:",
        "conc": "Concentração da solução de trabalho", "tabs": ["🧮 Calculadora", "🚨 Protocolos de emergência"],
        "tablets": "pastilhas por 10L de água", "method": "Método de desinfecção", "exp": "Tempo de exposição recomendado",
        "btn_timer": "⏱️ INICIAR TEMPORIZADOR DE EXPOSIÇÃO", "timer_done": "✅ Exposição concluída!"
    }
}

# Головне меню додатку (Вкладки)
tab_home, tab_emergency = st.tabs(t[lang]["tabs"])

# --- ВКЛАДКА 1: КАЛЬКУЛЯТОР ДЕЗРОЗЧИНІВ ---
with tab_home:
    st.title(t[lang]["title"])
    st.caption(t[lang]["caption"])
    
    if df is not None:
        obj_col = f"Object_{lang}" if f"Object_{lang}" in df.columns else "Object_UA"
        
        # 1. Вибір об'єкта дезінфекції
        objects = sorted(df[obj_col].dropna().unique())
        selected_object = st.selectbox(t[lang]["step1"], objects)
        
        # Фільтруємо таблицю за обраним об'єктом
        matched_rows = df[df[obj_col] == selected_object]
        
        # Вивід прикладів з фіксованими відступами
        if 'Examples_UA' in df.columns and not matched_rows.empty:
            examples_text = matched_rows['Examples_UA'].values[0]
