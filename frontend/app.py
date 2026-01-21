import streamlit as st
import requests
import pandas as pd
from docx import Document
import io
import zipfile

# IMPORTEM LA NOSTRA CONFIGURACIÓ I TRADUCCIONS
import config
from translations import TEXTS

# --- 1. CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="AI Anonymizer Pro", page_icon="🔒", layout="wide")

# CSS HACK PER ELIMINAR L'ESPAI SUPERIOR
st.markdown("<style>.block-container {padding-top: 0rem;}</style>", unsafe_allow_html=True)

# --- 2. SIDEBAR (Barra Lateral) ---
lang = st.sidebar.selectbox("🌐 Language / Idioma", list(TEXTS.keys()))
t = TEXTS[lang]

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Project")
st.sidebar.write(t['software_info'])

# Botó GitHub (dinàmic des de config)
st.sidebar.markdown(
    f"""<a href="{config.GITHUB_REPO_URL}" target="_blank" style="text-decoration: none;">
        <button style="width: 100%; border-radius: 5px; border: 1px solid #4f8bf9; background-color: transparent; color: #4f8bf9; padding: 5px; cursor: pointer; font-size: 0.9em; font-weight: bold;">
            📂 {t['github_btn']}
        </button>
    </a>""", unsafe_allow_html=True
)
st.sidebar.caption(config.GITHUB_PRIVACY_MSG[lang])

st.sidebar.write("")

# Botó Buy Me a Coffee (dinàmic des de config)
st.sidebar.write(t['bmc_msg'])
st.sidebar.markdown(
    f"""<a href="{config.BMC_URL}" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" style="height: 35px; width: 130px; display: block; margin: auto;" >
    </a>""", unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.write(t['cookie_disclaimer'])
with st.sidebar.expander(t['privacy_title']):
    st.write(t['privacy_text'])

# --- 3. CONTINGUT PRINCIPAL ---
st.image("frontend/banner.png", width="stretch")

with st.expander(t["expander_label"]):
    st.info(t["description"])

API_URL = "http://localhost:7000"

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

# --- LÒGICA D'ANONIMITZACIÓ ---
with tab1:
    up_file = st.file_uploader("Upload", type=["xlsx", "csv", "docx"], key="up_anon")
    if st.button("Run", key="btn_anon"):
        if up_file:
            with st.spinner(t["processing"]):
                r = requests.post(f"{API_URL}/anonymize/", files={"file": (up_file.name, up_file.getvalue())})
                if r.status_code == 200:
                    st.success("Done!")
                    st.download_button("Download Results", r.content, f"results_{up_file.name}.zip")

# --- LÒGICA DE DESANONIMITZACIÓ ---
with tab2:
    method = st.radio(t["method"], [t["method_zip"], t["method_files"]])
    # (Lògica de càrrega de fitxers de restauració ja definida anteriorment)
    # ...

# --- 4. FOOTER TRADUÏT I PERSONALITZAT ---
st.markdown("---")
footer_html = f"""
<div style='text-align: center; color: gray; font-size: 0.8em; padding-bottom: 20px;'>
    {t['footer_text']} <a href='{config.PERSONAL_WEB_URL}' target='_blank' style='color: #4f8bf9; text-decoration: none;'>Albert Ortiz</a>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
