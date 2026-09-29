"""
🐝 BEES CLOUD — MIB Sub-Level 8 Text Analysis Terminal
Interfaz retro-futurista de 8 bits / Fósforo Verde (MIB Style)

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run wordcloud_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BEES CLOUD // MIB TERMINAL",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# ESTILOS — 8-Bit CRT / Fósforo Verde MIB
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Share+Tech+Mono&display=swap');

    /* Reset global estilo Terminal CRT */
    html, body, [class*="css"] {
        font-family: 'VT323', 'Share Tech Mono', monospace !important;
        background-color: #020b05 !important;
        color: #33ff66 !important;
        letter-spacing: 1px;
    }

    /* Fondo de pantalla con scanlines analógicas de los 80/90 */
    .stApp {
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.35) 50%),
                    linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03)) !important;
        background-size: 100% 4px, 6px 100% !important;
        background-color: #020b05 !important;
    }

    /* Ocultar barra lateral por defecto */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Encabezado Principal MIB Terminal */
    .mib-header {
        border: 2px solid #33ff66;
        background-color: #001405;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(51, 255, 102, 0.3), inset 0 0 10px rgba(51, 255, 102, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Pestañas estilo Sistema Militar de 8 bits */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #001405;
        padding: 6px;
        border: 1px solid #1a8035;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #020b05;
        color: #1a8035 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.3rem !important;
        border: 1px solid #1a8035 !important;
        border-radius: 0px !important;
        transition: all 0.1s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #33ff66 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #33ff66 !important;
        box-shadow: 0 0 10px rgba(51, 255, 102, 0.6) !important;
    }

    /* Contenedores Cyberpunk / MIB */
    .mib-card {
        background-color: #001104;
        border: 2px solid #33ff66;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 3px 3px 0px #1a8035;
    }

    /* Entradas de texto e Inputs */
    textarea, input[type="text"] {
        background-color: #000802 !important;
        border: 1px solid #33ff66 !important;
        color: #33ff66 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.2rem !important;
        border-radius: 0px !important;
    }
    textarea:focus, input[type="text"]:focus {
        box-shadow: 0 0 8px rgba(51, 255, 102, 0.8) !important;
    }

    /* Selectbox de 8 bits */
    [data-baseweb="select"] > div {
        background-color: #000802 !important;
        border: 1px solid #33ff66 !important;
        color: #33ff66 !important;
        border-radius: 0px !important;
    }

    /* Botones Neón Verde 8-bits */
    .stButton > button, [data-testid="stDownloadButton"] button {
        background-color: #002b0c !important;
        color: #33ff66 !important;
        border: 2px solid #33ff66 !important;
        border-radius: 0px !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.4rem !important;
        text-transform: uppercase !important;
        box-shadow: 4px 4px 0px #1a8035 !important;
        transition: all 0.1s ease !important;
    }
    .stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
        background-color: #33ff66 !important;
        color: #000000 !important;
        box-shadow: 0 0 12px rgba(51, 255, 102, 0.9) !important;
    }

    /* Métricas estilo Radar */
    [data-testid="metric-container"] {
        background-color: #001405 !important;
        border: 1px solid #33ff66 !important;
        padding: 10px !important;
        border-radius: 0px !important;
    }
    [data-testid="metric-container"] label {
        color: #1a8035 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.1rem !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #33ff66 !important;
        font-family: 'VT323', monospace !important;
        font-size: 2rem !important;
        text-shadow: 0 0 5px #33ff66;
    }

    /* Filas de tabla / Frecuencias */
    .freq-row {
        background-color: #000802;
        border: 1px solid #1a8035;
        padding: 4px 10px;
        margin: 4px 0;
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
    }
    .freq-bar {
        background-color: #33ff66;
        box-shadow: 0 0 6px #33ff66;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONFIGURACIÓN Y PALETAS MIB 8-BIT
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw

PALETAS = {
    "MIB Matrix Green":     ["#33ff66", "#00cc44", "#009933", "#66ff99", "#99ffbb", "#006622"],
    "Alien Amber (8-bit)":  ["#ffb000", "#ffcf40", "#ff8800", "#ffd766", "#cc7700"],
    "Sub-Level Cyan":       ["#00ffff", "#00cccc", "#66ffff", "#009999", "#99ffff"],
    "Monochrome CRT":       ["#ffffff", "#cccccc", "#999999", "#666666", "#eeeeee"],
}

FORMAS = {"Rectángulo": None, "Círculo": "circle"}

def crear_mascara(forma, size=500):
    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2
        mascara = np.ones((size, size), dtype=np.uint8) * 255
        mascara[(x - cx)**2 + (y - cy)**2 <= (size // 2 - 12)**2] = 0
        return mascara
    return None

def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    return " ".join([p for p in texto.split() if p not in stopwords and len(p) >= min_longitud])

def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50), columns=["Palabra", "Frecuencia"])

def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma, ancho=1000, alto=520):
    import random
    colores = PALETAS[paleta_nombre]
    color_func = lambda *args, **kwargs: colores[random.randint(0, len(colores) - 1)]
    mascara = crear_mascara(forma, size=min(ancho, alto))
    
    bg_hex = "#000000" if fondo == "Negro" else "#ffffff"
    
    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words, background_color=bg_hex,
        color_func=color_func, mask=mascara, collocations=False,
        min_font_size=12, max_font_size=110, prefer_horizontal=0.9, margin=5
    ).generate(texto_limpio)
    
    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="nearest") # Interpolación pixelada de 8 bits
    ax.axis("off")
    fig.patch.set_facecolor(bg_hex)
    plt.tight_layout(pad=0)
    return fig

def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# ESTRUCTURA BEES CLOUD // TERMINAL MIB
# ─────────────────────────────────────────────

# Header estilo MIB / Sub-Level 8
st.markdown("""
<div class="mib-header">
    <div>
        <h1 style="margin:0; font-size:2.3rem; color:#33ff66; text-shadow:0 0 8px #33ff66;">🐝 BEES CLOUD</h1>
        <p style="margin:0; color:#1a8035; font-size:1.1rem;">SUB-LEVEL 8 // TEXT ANALYSIS & FREQUENCY DECODER</p>
    </div>
    <div style="text-align:right; color:#33ff66;">
        <span style="border:1px solid #33ff66; padding:4px 8px;">CLEARANCE: LEVEL 5</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_editor, tab_visual, tab_datos = st.tabs([
    "[1] INPUT_CORPUS", 
    "[2] VISUAL_DECODER", 
    "[3] DATA_LOGS"
])

if "texto_input" not in st.session_state:
    st.session_state["texto_input"] = ""

# ─────────────────────────────────────────────
# TAB 1: INPUT_CORPUS
# ─────────────────────────────────────────────
with tab_editor:
    col_input, col_preset = st.columns([2, 1], gap="medium")
    
    with col_input:
        st.markdown('<div class="mib-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#33ff66; margin-top:0;'>// CARGAR TRANSMISIÓN DE TEXTO</h3>", unsafe_allow_html=True)
        fuente = st.radio("ORIGEN DE DATOS:", ["TEXTO DIRECTO", "ARCHIVO EXTERNO (.TXT, .CSV)"], horizontal=True)
        
        if fuente == "TEXTO DIRECTO":
            st.session_state["texto_input"] = st.text_area("INSERTE TEXTO CRUDO:", value=st.session_state["texto_input"], height=250, placeholder="Inyecte aquí el mensaje interceptado...")
        else:
            archivo = st.file_uploader("SELECCIONE ARCHIVO DE DATOS:", type=["txt", "csv"])
            if archivo:
                if archivo.name.endswith(".txt"):
                    st.session_state["texto_input"] = archivo.read().decode("utf-8", errors="ignore")
                elif archivo.name.endswith(".csv"):
                    df_csv = pd.read_csv(archivo)
                    col_txt = st.selectbox("COLUMNA OBJETIVO:", df_csv.columns.tolist())
                    st.session_state["texto_input"] = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
                st.success(f">> DATOS CARGADOS: {len(st.session_state['texto_input']):,} CARACTERES")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preset:
        st.markdown('<div class="mib-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#33ff66; margin-top:0;'>// REGISTROS MIB</h3>", unsafe_allow_html=True)
        ejemplos = {
            "Archivo X-01 (Inteligencia Artificial)": "La inteligencia artificial interceptada muestra patrones avanzadas de aprendizaje automático y procesamiento cognitivo autónomo...",
            "Informe MIB-4 (Tecnología 4.0)": "Los sensores de subnivel registran convergencia de internet de las cosas, analítica masiva y cibernética autónoma...",
            "Expediente B-09 (Bioma)": "Análisis de biodiversidad territorial con ecosistemas de alta prioridad y biodiversidad crítica..."
        }
        ejemplo_sel = st.selectbox("EXPEDIENTES DE PRUEBA:", list(ejemplos.keys()))
        if st.button("CARGAR EXPEDIENTE", use_container_width=True):
            st.session_state["texto_input"] = ejemplos[ejemplo_sel]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 2: VISUAL_DECODER
# ─────────────────────────────────────────────
with tab_visual:
    col_canvas, col_controls = st.columns([3, 1], gap="medium")

    with col_controls:
        st.markdown('<div class="mib-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#33ff66; margin-top:0;'>// PARÁMETROS</h3>", unsafe_allow_html=True)
        
        idioma = st.selectbox("FILTRO STOPWORDS:", ["Español", "Inglés", "Ambos", "Ninguno"])
        min_longitud = st.slider("LONGITUD MÍNIMA:", 2, 8, 3)
        palabras_extra = st.text_input("EXCLUIR PALABRAS:", placeholder="ej: además, previo")
        
        st.markdown("---")
        paleta_sel = st.selectbox("PALETA FÓSFORO:", list(PALETAS.keys()))
        fondo_sel = st.radio("FONDO MATRIZ:", ["Negro", "Blanco"], horizontal=True)
        forma_sel = st.selectbox("MÁSCARA RADAR:", list(FORMAS.keys()))
        max_words = st.slider("MÁX. TÉRMINOS:", 20, 200, 80)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_canvas:
        st.markdown('<div class="mib-card">', unsafe_allow_html=True)
        
        if not st.session_state["texto_input"].strip():
            st.warning(">> ADVERTENCIA: NO HAY DATOS DE TEXTO CARGADOS. VAYA A [1] INPUT_CORPUS.")
        else:
            stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
            if palabras_extra.strip():
                stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

            texto_limpio = limpiar_texto(st.session_state["texto_input"], stopwords_set, min_longitud)

            if not texto_limpio.strip():
                st.error(">> ERROR: EL CORPUS QUEDÓ VACÍO TRAS EL FILTRADO DE STOPWORDS.")
            else:
                with st.spinner("PROCESANDO MATRIZ DE 8 BITS..."):
                    fig_wc = generar_wordcloud(
                        texto_limpio, paleta_sel, max_words, fondo_sel,
                        FORMAS[forma_sel], ancho=1000, alto=520
                    )
                
                st.pyplot(fig_wc, use_container_width=True)
                
                img_bytes = fig_a_bytes(fig_wc)
                st.download_button("⬇ EXPORTAR MAPA DE BITS (.PNG)", data=img_bytes, file_name="bees_cloud_8bit.png", mime="image/png", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 3: DATA_LOGS
# ─────────────────────────────────────────────
with tab_datos:
    if not st.session_state["texto_input"].strip():
        st.warning(">> REGISTRO VACÍO. INGRESE DATOS EN LA TAB 1.")
    else:
        stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
        texto_limpio = limpiar_texto(st.session_state["texto_input"], stopwords_set, min_longitud)
        df_freq = contar_palabras(texto_limpio)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("TOTAL PALABRAS PROCESADAS", len(texto_limpio.split()))
        m2.metric("VOCABULARIO ÚNICO", len(df_freq))
        m3.metric("TÉRMINO DOMINANTE", df_freq.iloc[0]["Palabra"] if not df_freq.empty else "N/A")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_list, col_tbl = st.columns([1, 1], gap="medium")
        
        with col_list:
            st.markdown('<div class="mib-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#33ff66; margin-top:0;'>// FRECUENCIA TOP 15</h3>", unsafe_allow_html=True)
            top15 = df_freq.head(15)
            max_f = top15["Frecuencia"].max() if not top15.empty else 1
            
            for rank, (_, row) in enumerate(top15.iterrows(), 1):
                p, f = row["Palabra"], int(row["Frecuencia"])
                w = max(8, int((f / max_f) * 160))
                st.markdown(
                    f'<div class="freq-row" style="display:flex; align-items:center; justify-content:space-between;">'
                    f'<span style="color:#33ff66;"><b>[{rank:02d}]</b> {p.upper()}</span>'
                    f'<div style="display:flex; align-items:center; gap:8px;">'
                    f'<div class="freq-bar" style="width:{w}px; height:8px;"></div>'
                    f'<b style="color:#33ff66;">{f}</b>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

        with col_tbl:
            st.markdown('<div class="mib-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#33ff66; margin-top:0;'>// TABLA COMPLETA</h3>", unsafe_allow_html=True)
            st.dataframe(df_freq, use_container_width=True, height=380)
            csv_bytes = df_freq.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ EXPORTAR REGISTROS (.CSV)", data=csv_bytes, file_name="bees_cloud_data.csv", mime="text/csv", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

plt.close("all")
