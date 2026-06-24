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

# 🔥 ОДНА КНОПКА-ГЛОБУС ДЛЯ ВИБОРУ МОВИ (8 МОВ)
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
        "examples": "💡 **Приклади об'єктів:**", "result": "🏁 Результат розрахунку:",
        "conc": "Концентрація робочого розчину", "tabs": ["🧮 Калькулятор", "🚨 Аварійні Протоколи"],
        "tablets": "табл. на 10л води", "method": "Спосіб знезараження", "exp": "Рекомендований час експозиції",
        "btn_timer": "⏱️ ЗАПУСТИТИ ТАЙМЕР ЕКСПОЗИЦІЇ", "timer_done": "✅ Експозицію завершено!"
    },
    "EN": {
        "title": "🧮 IPC Calculator", "caption": "Autonomous solution calculation",
        "step1": "1. Select disinfection object:", "step2": "2. Select disinfectant product:",
        "examples": "💡 **Examples of objects:**", "result": "🏁 Calculation Result:",
        "conc": "Working solution concentration", "tabs": ["🧮 Calculator", "🚨 Emergency Protocols"],
        "tablets": "tabs per 10L of water", "method": "Disinfection method", "exp": "Recommended exposure time",
        "btn_timer": "⏱️ START EXPOSURE TIMER", "timer_done": "✅ Exposure completed!"
    },
    "PL": {
        "title": "🧮 Kalkulator IPC", "caption": "Autonomiczne obliczanie roztworów",
        "step1": "1. Wybierz obiekt dezynfekcji:", "step2": "2. Wybierz środek dezynfekujący:",
        "examples": "💡 **Przykłady obiektów:**", "result": "🏁 Wynik obliczeń:",
        "conc": "Stężenie roztworu roboczego", "tabs": ["🧮 Kalkulator", "🚨 Protokoły awaryjne"],
        "tablets": "tabl. na 10L wody", "method": "Metoda dezynfekcji", "exp": "Zalecany czas ekspozycji",
        "btn_timer": "⏱️ URUCHOM TIMER EKSPOZYCJI", "timer_done": "✅ Ekspozycja zakończona!"
    },
    "DE": {
        "title": "🧮 IPC-Rechner", "caption": "Autonome Berechnung von Lösungen",
        "step1": "1. Desinfektionsobjekt auswählen:", "step2": "2. Desinfektionsmittel auswählen:",
        "examples": "💡 **Objektbeispiele:**", "result": "🏁 Berechnungsergebnis:",
        "conc": "Konzentration der Arbeitslösung", "tabs": ["🧮 Rechner", "🚨 Notfallprotokolle"],
        "tablets": "Tabl. pro 10L Wasser", "method": "Desinfektionsmethode", "exp": "Empfohlene Einwirkzeit",
        "btn_timer": "⏱️ BELICHTUNGSTIMER STARTEN", "timer_done": "✅ Einwirkzeit beendet!"
    },
    "FR": {
        "title": "🧮 Calculateur IPC", "caption": "Calcul autonome des solutions",
        "step1": "1. Sélectionner l'objet de désinfection:", "step2": "2. Sélectionner le désinfectant:",
        "examples": "💡 **Exemples d'objets:**", "result": "🏁 Résultat du calcul:",
        "conc": "Concentration de la solution de travail", "tabs": ["🧮 Calculateur", "🚨 Protocoles d'urgence"],
        "tablets": "comprimés pour 10L d'eau", "method": "Méthode de désinfection", "exp": "Temps d'exposition recommandé",
        "btn_timer": "⏱️ DÉMARRER LE MINUTEUR D'EXPOSITION", "timer_done": "✅ Exposition terminée!"
    },
    "ES": {
        "title": "🧮 Calculadora IPC", "caption": "Cálculo autónomo de soluciones",
        "step1": "1. Seleccione objeto de desinfección:", "step2": "2. Seleccione desinfectante:",
        "examples": "💡 **Ejemplos de objetos:**", "result": "🏁 Resultado del cálculo:",
        "conc": "Concentración de la solución de trabajo", "tabs": ["🧮 Calculadora", "🚨 Protocolos de emergencia"],
        "tablets": "pastillas por 10L de agua", "method": "Método de desinfección", "exp": "Tiempo de exposición recomendado",
        "btn_timer": "⏱️ INICIAR TEMPORIZADOR DE EXPOSICIÓN", "timer_done": "✅ ¡Exposición completada!"
    },
    "IT": {
        "title": "🧮 Calcolatore IPC", "caption": "Calcolo autonomo delle soluzioni",
        "step1": "1. Seleziona l'oggetto di disinfezione:", "step2": "2. Seleziona il disinfettante:",
        "examples": "💡 **Esempi di oggetti:**", "result": "🏁 Risultato del calcolo:",
        "conc": "Concentrazione della soluzione di lavoro", "tabs": ["🧮 Calcolatore", "🚨 Protocolli di emergenza"],
        "tablets": "compresse per 10L d'acqua", "method": "Metodo di disinfezione", "exp": "Tempo di esposizione raccomandato",
        "btn_timer": "⏱️ AVVIA TIMING DI ESPOSIZIONE", "timer_done": "✅ Esposizione completata!"
    },
    "PT": {
        "title": "🧮 Calculadora IPC", "caption": "Cálculo autónomo de soluções",
        "step1": "1. Selecione o objeto de desinfecção:", "step2": "2. Selecione o desinfetante:",
        "examples": "💡 **Exemplos de objetos:**", "result": "🏁 Resultado do cálculo:",
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
        
        matched_rows = df[df[obj_col] == selected_object]
        
        # Вивід прикладів
        if 'Examples_UA' in df.columns and not matched_rows.empty:
            examples_text = matched_rows['Examples_UA'].iloc[0]
            if pd.notna(examples_text) and str(examples_text).strip() != "—":
                st.markdown(f"{t[lang]['examples']} *{examples_text}*")
        
        st.markdown(" ")
        
        # 2. Вибір дезінфекційного засобу (УСІ засоби тепер на місці!)
        available_products = sorted(matched_rows['Product'].dropna().unique())
        selected_product = st.selectbox(t[lang]["step2"], available_products)
        
        # Фінальний точний рядок розрахунку
        final_row = matched_rows[matched_rows['Product'] == selected_product].reset_index(drop=True).iloc[0]
        
        st.markdown("---")
        st.subheader(t[lang]["result"])
        st.metric(label=t[lang]["conc"], value=f"{final_row['Conc_%']}")
        
        if 'Tablets' in final_row and pd.notna(final_row['Tablets']) and str(final_row['Tablets']).strip() != "—":
            st.success(f"🧫 {final_row['Tablets']} {t[lang]['tablets']}")
        elif 'Volume_ml' in final_row and pd.notna(final_row['Volume_ml']) and str(final_row['Volume_ml']).strip() != "—":
            st.success(f"🧪 {final_row['Volume_ml']}")
            
        if 'Method_UA' in final_row and pd.notna(final_row['Method_UA']):
            st.info(f"ℹ️ {t[lang]['method']}: **{final_row['Method_UA']}**")
            
        if 'Exposure_min' in final_row and pd.notna(final_row['Exposure_min']):
            raw_exposure = str(final_row['Exposure_min'])
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
                    time.sleep(60) # Ренальний час
                    
                st.balloons()
                status_text.success(t[lang]["timer_done"])

# --- ВКЛАДКА 2: АВАРІЙНІ ПРОТОКОЛИ ---
with tab_emergency:
    st.info("🚨 EMERGENCY PROTOCOLS")
