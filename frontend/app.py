import streamlit as st
import requests
import pandas as pd
from docx import Document
import io
import zipfile
import config  # Importem el fitxer frontend/config.py

# --- 1. CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(
    page_title="AI Anonymizer Pro", 
    page_icon="🔒", 
    layout="wide"
)

# --- 2. CSS HACK PER ESTILITZAR EL BANNER ---
# Elimina l'espai en blanc superior perquè el banner quedi enganxat a dalt de tot.
st.markdown("""
    <style>
           .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
            }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DICCIONARI DE TRADUCCIONS (Lògica de la interfície) ---
TEXTS = {
    "English": {
        "expander_label": "ℹ️ About & Security",
        "description": "This app acts as a **simple translator** for sensitive data using local NLP (NON-generative AI).",
        "tab_anon": "Anonymize",
        "tab_dean": "Deanonymize",
        "method": "Upload Method",
        "method_zip": "Single ZIP file",
        "method_files": "Two separate files",
        "label_zip": "Upload results ZIP",
        "label_anon": "Anonymized file",
        "label_keys": "Key file (decryption_keys.xlsx)",
        "btn_dean": "Restore Data",
        "processing": "Translating...",
        "preview": "👁️ Preview:",
        "success": "Restored!",
        "github_btn": "View on GitHub",
        "cookie_disclaimer": "🍪 **No Cookies:** This site does not use cookies for tracking or advertising.",
        "privacy_title": "⚖️ Privacy Policy",
        "privacy_text": """
            **Zero Data Policy:**
            * We do not store, log, or share the content of your documents.
            * All processing is done locally on our server.
            * Temporary data is purged when the session ends.
            * This site does not use cookies.
        """,
        "software_info": "🚀 This is a **free and open-source** project.",
        "bmc_msg": "If you find it useful, please consider a small donation to help subsidize the server costs.",
    },
    "Català": {
        "expander_label": "ℹ️ Sobre l'app i Seguretat",
        "description": "Aquesta aplicació actua com un **simple traductor** de dades sensibles mitjançant IA local (NO generativa).",
        "tab_anon": "Anonimitzar",
        "tab_dean": "Desanonimitzar",
        "method": "Mètode de càrrega",
        "method_zip": "Un sol arxiu ZIP",
        "method_files": "Dos fitxers per separat",
        "label_zip": "Puja el ZIP de resultats",
        "label_anon": "Fitxer anonimitat",
        "label_keys": "Arxiu de claus (decryption_keys.xlsx)",
        "btn_dean": "Restaurar dades",
        "processing": "Traduint...",
        "preview": "👁️ Previsualització:",
        "success": "Restaurat!",
        "github_btn": "Veure a GitHub",
        "cookie_disclaimer": "🍪 **Sense Cookies:** Aquest lloc no utilitza cookies de rastreig ni publicitat.",
        "privacy_title": "⚖️ Política de Privacitat",
        "privacy_text": """
            **Política de Zero Dades:**
            * No guardem, ni registrem, ni compartim el contingut dels vostres documents.
            * Tot el processament es fa localment al nostre servidor.
            * Les dades temporals s'eliminen en finalitzar la sessió.
            * Aquest lloc no utilitza cookies de cap tipus.
        """,
        "software_info": "🚀 Aquest és un projecte **gratuït i de software lliure**.",
        "bmc_msg": "Si t'és útil, agrairia una petita donació per ajudar a subvencionar els costos del servidor.",
    },
    # Nota: Pots afegir aquí els diccionaris d'Español, Français i Deutsch igual que abans.
}

# --- 4. SIDEBAR: CONFIGURACIÓ I LINKS (Agafant de config.py) ---
lang = st.sidebar.selectbox("🌐 Language / Idioma", list(TEXTS.keys()))
t = TEXTS[lang]

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Project")
st.sidebar.write(t['software_info'])

# Botó GitHub (URL des de config.py)
st.sidebar.markdown(
    f"""
    <a href="{config.GITHUB_REPO_URL}" target="_blank" style="text-decoration: none;">
        <button style="width: 100%; border-radius: 5px; border: 1px solid #4f8bf9; background-color: transparent; color: #4f8bf9; padding: 5px; cursor: pointer; font-size: 0.9em; font-weight: bold;">
            📂 {t['github_btn']}
        </button>
    </a>
    """, 
    unsafe_allow_html=True
)
# Missatge de privacitat de GitHub des de config.py
st.sidebar.caption(config.GITHUB_PRIVACY_MSG[lang])

st.sidebar.write("")

# Secció Buy Me a Coffee (URL des de config.py)
st.sidebar.write(t['bmc_msg'])
st.sidebar.markdown(
    f"""
    <a href="{config.BMC_URL}" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 35px !important; width: 130px !important; display: block; margin-left: auto; margin-right: auto;" >
    </a>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.write(t['cookie_disclaimer'])

with st.sidebar.expander(t['privacy_title']):
    st.write(t['privacy_text'])

# --- 5. CONTINGUT PRINCIPAL ---

# Banner amb la nova sintaxi per evitar el warning del 2026
st.image("frontend/banner.png", width="stretch")

with st.expander(t["expander_label"], expanded=False):
    st.info(t["description"])

API_URL = "http://localhost:7000"

# Funcions auxiliars per a la previsualització
def show_preview(content, filename):
    st.write(t["preview"])
    try:
        if filename.lower().endswith(('.xlsx', '.xls', '.csv')):
            try: df = pd.read_excel(io.BytesIO(content), header=None)
            except: df = pd.read_csv(io.BytesIO(content), header=None, encoding='utf-8-sig')
            st.table(df.head(5))
        elif filename.lower().endswith('.docx'):
            doc = Document(io.BytesIO(content))
            for p in doc.paragraphs[:3]:
                if p.text.strip(): st.info(p.text)
    except: st.warning("Preview unavailable")

tab1, tab2 = st.tabs([t["tab_anon"], t["tab_dean"]])

# --- PESTANYA 1: ANONIMITZAR ---
with tab1:
    up_file = st.file_uploader("Upload file", type=["xlsx", "csv", "docx"], key="up_anon")
    if st.button("Run Process", key="btn_anon_exec"):
        if up_file:
            with st.spinner(t["processing"]):
                files = {"file": (up_file.name, up_file.getvalue())}
                r = requests.post(f"{API_URL}/anonymize/", files=files)
                if r.status_code == 200:
                    st.success("Done!")
                    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                        name = [n for n in z.namelist() if n.startswith("ANONYMIZED_")][0]
                        show_preview(z.read(name), up_file.name)
                    st.download_button("Download ZIP", r.content, f"results_{up_file.name}.zip")

# --- PESTANYA 2: DESANONIMITZAR ---
with tab2:
    method = st.radio(t["method"], [t["method_zip"], t["method_files"]], key="meth_dean_radio")
    
    data_anon, name_anon, data_keys, name_keys = None, None, None, None
    
    if method == t["method_zip"]:
        zip_up = st.file_uploader(t["label_zip"], type=["zip"], key="zip_dean_up")
        if zip_up:
            try:
                with zipfile.ZipFile(io.BytesIO(zip_up.getvalue())) as z:
                    anon_list = [n for n in z.namelist() if n.startswith("ANONYMIZED_")]
                    key_list = [n for n in z.namelist() if n == "decryption_keys.xlsx"]
                    if anon_list and key_list:
                        name_anon, name_keys = anon_list[0], key_list[0]
                        data_anon, data_keys = z.read(name_anon), z.read(name_keys)
                        st.success(f"Files found: {name_anon} & {name_keys}")
                    else: st.error("Files not found in ZIP")
            except: st.error("Error reading ZIP")
    else:
        c1, c2 = st.columns(2)
        with c1: 
            f_a = st.file_uploader(t["label_anon"], type=["xlsx", "csv", "docx"], key="fa_manual")
            if f_a: name_anon, data_anon = f_a.name, f_a.getvalue()
        with c2: 
            f_k = st.file_uploader(t["label_keys"], type=["xlsx"], key="fk_manual")
            if f_k: name_keys, data_keys = f_k.name, f_k.getvalue()

    if st.button(t["btn_dean"], key="btn_dean_exec"):
        if data_anon and data_keys:
            with st.spinner(t["processing"]):
                files_payload = {"file_anonim": (name_anon, data_anon), "file_keys": (name_keys, data_keys)}
                r = requests.post(f"{API_URL}/deanonymize/", files=files_payload)
                if r.status_code == 200:
                    st.success(t["success"])
                    show_preview(r.content, name_anon)
                    st.download_button("Download Restored File", r.content, f"RESTORED_{name_anon}")
                else: st.error(f"Error: {r.text}")

# --- 6. FOOTER (Agafant URL de config.py) ---
st.markdown("---")
footer_html = f"""
<div style='text-align: center; color: gray; font-size: 0.8em; margin-top: 20px; padding-bottom: 20px;'>
    © 2026 Program created by <a href='{config.PERSONAL_WEB_URL}' target='_blank' style='color: #4f8bf9; text-decoration: none;'>Albert Ortiz</a> - Webapp developed with the assistance of Gemini AI.
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
