import streamlit as st
import requests
import pandas as pd
from docx import Document
import io
import zipfile

# 1. Diccionari Multilingüe (English, Català, Español, Français, Deutsch)
TEXTS = {
    "English": {
        "title": "🔒 AI Anonymizer Pro",
        "expander_label": "ℹ️ About this app & Security Information",
        "description": """
            **How it works:** This app acts as a **simple translator** that masks sensitive data using local NLP (NON-generative AI). 
            
            **⚠️ Zero Data Usage Policy:**
            * The application **DOES NOT use** the information provided for any purpose other than translation.
            * **NO DATA is stored or sent** to generative AIs (like ChatGPT).
            
            **Important for Deanonymization:**
            * **ZIP Method:** The key file inside the ZIP must be named `decryption_keys.xlsx`.
        """,
        "tab_anon": "Anonymize",
        "tab_dean": "Deanonymize",
        "method": "Upload Method",
        "method_zip": "Single ZIP file",
        "method_files": "Two separate files",
        "label_zip": "Upload the results ZIP",
        "label_anon": "Anonymized file",
        "label_keys": "Key file (decryption_keys.xlsx)",
        "btn_dean": "Restore Data",
        "processing": "Translating...",
        "preview": "👁️ Preview:",
        "success": "Restored!",
        "footer": "Program created by"
    },
    "Català": {
        "title": "🔒 Anonimitzador IA Pro",
        "expander_label": "ℹ️ Sobre aquesta app i Informació de Seguretat",
        "description": """
            **Com funciona:** Aquesta aplicació actua com un **simple traductor** que emmascara dades sensibles mitjançant IA NO generativa local.
            
            **⚠️ Política de No Ús de Dades:**
            * L'aplicació **NO fa cap mena d'ús** de la informació més enllà de la traducció.
            * **NO s'envia cap dada** a cap IA generativa (com ChatGPT).
            
            **Important per a la Desanonimització:**
            * **Mètode ZIP:** El fitxer de claus s'ha de dir `decryption_keys.xlsx`.
        """,
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
        "footer": "Programa creat per"
    },
    "Español": {
        "title": "🔒 Anonimizador IA Pro",
        "expander_label": "ℹ️ Información de Seguridad",
        "description": """
            **Cómo funciona:** Esta aplicación actúa como un **simple traductor** que enmascara datos mediante IA NO generativa local.
            
            **⚠️ Política de No Uso de Datos:**
            * La aplicación **NO hace ningún uso** de la información más allá de la traducción.
            * **NO se envían datos** a ninguna IA generativa (como ChatGPT).
        """,
        "tab_anon": "Anonimizar",
        "tab_dean": "Desanonimizar",
        "method": "Método de carga",
        "method_zip": "Un solo archivo ZIP",
        "method_files": "Dos archivos por separado",
        "label_zip": "Sube el ZIP de resultados",
        "label_anon": "Archivo anonimizado",
        "label_keys": "Archivo de claves (decryption_keys.xlsx)",
        "btn_dean": "Restaurar datos",
        "processing": "Traduciendo...",
        "preview": "👁️ Previsualización:",
        "success": "¡Restaurado!",
        "footer": "Programa creado por"
    },
    "Français": {
        "title": "🔒 Anonymiseur IA Pro",
        "expander_label": "ℹ️ À propos de cette application et Sécurité",
        "description": """
            **Comment ça marche :** Cette application agit comme un **simple traducteur** qui masque les données sensibles via une IA locale NON générative.
            
            **⚠️ Politique d'utilisation des données nulle :**
            * L'application **N'UTILISE PAS** les informations fournies à d'autres fins que la traduction.
            * **AUCUNE DONNÉE n'est envoyée** à des IA génératives (comme ChatGPT).
            
            **Important pour la désanonymisation :**
            * **Méthode ZIP :** Le fichier de clés doit s'appeler `decryption_keys.xlsx`.
        """,
        "tab_anon": "Anonymiser",
        "tab_dean": "Désanonymiser",
        "method": "Méthode de chargement",
        "method_zip": "Fichier ZIP unique",
        "method_files": "Deux fichiers séparés",
        "label_zip": "Charger le ZIP des résultats",
        "label_anon": "Fichier anonymisé",
        "label_keys": "Fichier de clés (decryption_keys.xlsx)",
        "btn_dean": "Restaurer les données",
        "processing": "Traduction...",
        "preview": "👁️ Aperçu :",
        "success": "Restauré !",
        "footer": "Programme créé par"
    },
    "Deutsch": {
        "title": "🔒 KI-Anonymisierer Pro",
        "expander_label": "ℹ️ Über diese App & Sicherheit",
        "description": """
            **Wie es funktioniert:** Diese App fungiert als **einfacher Übersetzer**, der sensible Daten mithilfe lokaler, NICHT-generativer KI maskiert.
            
            **⚠️ Keine Datennutzungsrichtlinie:**
            * Die Anwendung **VERWENDET NICHT** die bereitgestellten Informationen für andere Zwecke als die Übersetzung.
            * **ES WERDEN KEINE DATEN** an generative KIs (wie ChatGPT) gesendet.
            
            **Wichtig für die Deanonymisierung:**
            * **ZIP-Methode:** Die Schlüsseldatei muss `decryption_keys.xlsx` heißen.
        """,
        "tab_anon": "Anonymisieren",
        "tab_dean": "Deanonymisieren",
        "method": "Upload-Methode",
        "method_zip": "Einzelne ZIP-Datei",
        "method_files": "Zwei separate Dateien",
        "label_zip": "Ergebnis-ZIP hochladen",
        "label_anon": "Anonymisierte Datei",
        "label_keys": "Schlüsseldatei (decryption_keys.xlsx)",
        "btn_dean": "Daten wiederherstellen",
        "processing": "Übersetzung...",
        "preview": "👁️ Vorschau:",
        "success": "Wiederhergestellt!",
        "footer": "Programm erstellt von"
    }
}

st.set_page_config(page_title="AI Anonymizer", page_icon="🔒", layout="wide")

# Barra lateral
lang = st.sidebar.selectbox("🌐 Language", ["English", "Català", "Español", "Français", "Deutsch"])
t = TEXTS[lang]

st.title(t["title"])
with st.expander(t["expander_label"], expanded=False):
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

# --- TAB 1 ---
with tab1:
    up_file = st.file_uploader("File", type=["xlsx", "csv", "docx"], key="u1")
    if st.button("Process", key="b1"):
        if up_file:
            with st.spinner(t["processing"]):
                files = {"file": (up_file.name, up_file.getvalue())}
                r = requests.post(f"{API_URL}/anonymize/", files=files)
                if r.status_code == 200:
                    st.success("Success!")
                    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                        name = [n for n in z.namelist() if n.startswith("ANONYMIZED_")][0]
                        show_preview(z.read(name), up_file.name)
                    st.download_button("Download ZIP", r.content, f"results_{up_file.name}.zip")

# --- TAB 2 ---
with tab2:
    method = st.radio(t["method"], [t["method_zip"], t["method_files"]], key="m1")
    d_anon, n_anon, d_keys, n_keys = None, None, None, None
    if method == t["method_zip"]:
        z_up = st.file_uploader(t["label_zip"], type=["zip"], key="z1")
        if z_up:
            try:
                with zipfile.ZipFile(io.BytesIO(z_up.getvalue())) as z:
                    a_l = [n for n in z.namelist() if n.startswith("ANONYMIZED_")]
                    k_l = [n for n in z.namelist() if n == "decryption_keys.xlsx"]
                    if a_l and k_l:
                        n_anon, n_keys = a_l[0], k_l[0]
                        d_anon, d_keys = z.read(n_anon), z.read(n_keys)
                        st.success(f"Found: {n_anon}")
                    else: st.error(t["error_zip"])
            except: st.error(t["error_zip"])
    else:
        c1, c2 = st.columns(2)
        with c1: 
            fa = st.file_uploader(t["label_anon"], key="fa")
            if fa: n_anon, d_anon = fa.name, fa.getvalue()
        with c2: 
            fk = st.file_uploader(t["label_keys"], key="fk")
            if fk: n_keys, d_keys = fk.name, fk.getvalue()

    if st.button(t["btn_dean"], key="bd"):
        if d_anon and d_keys:
            with st.spinner(t["processing"]):
                r = requests.post(f"{API_URL}/deanonymize/", files={"file_anonim": (n_anon, d_anon), "file_keys": (n_keys, d_keys)})
                if r.status_code == 200:
                    st.success(t["success"])
                    show_preview(r.content, n_anon)
                    st.download_button("Download", r.content, f"RESTORED_{n_anon}")

# --- FOOTER ---
st.markdown("---")
footer_html = f"""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
    {t['footer']} <a href='https://albert.thedepablos.com' target='_blank' style='color: #4f8bf9; text-decoration: none;'>Albert Ortiz</a>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
