"""
☁️ WordCloud Studio — Frutiger Aero OS Edition
Aplicación Streamlit con rediseño estructural, navegación por pestañas y estética Web 2.0 / Aero.

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
    page_title="WordCloud Studio — Aero OS",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed", # Ocultamos el sidebar por defecto para usar la pantalla completa
)

# ─────────────────────────────────────────────
# ESTILOS — Frutiger Aero / Aqua Glass (Rediseño de Layout)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    /* Fondo acuático con destellos */
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(255, 255, 255, 0.8) 0%, transparent 40%),
                    radial-gradient(circle at 85% 75%, rgba(120, 220, 255, 0.5) 0%, transparent 50%),
                    linear-gradient(135deg, #a8d0e6 0%, #3796b6 50%, #005f73 100%) !important;
        background-attachment: fixed !important;
    }

    /* Ocultar sidebar tradicional para usar layout panorámico */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Barra Superior / Header estilo OS */
    .aero-header {
        background: linear-gradient(180deg, rgba(255,255,255,0.85) 0%, rgba(200,230,255,0.6) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 18px 28px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 40, 80, 0.2), inset 0 1px 2px rgba(255,255,255,1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Pestañas personalizadas (Tabs Aero) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0, 0, 0, 0.1);
        padding: 6px;
        border-radius: 16px;
        backdrop-filter: blur(8px);
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.4);
        color: #003554 !important;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.5);
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #ffffff 0%, #b3e5fc 100%) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 1px #fff !important;
        color: #002b49 !important;
        border: 1px solid #81d4fa !important;
    }

    /* Tarjetas de cristal (Glassmorphism) */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.75) 0%, rgba(240, 248, 255, 0.45) 100%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 10px 30px rgba(0, 50, 100, 0.12), inset 0 1px 1px rgba(255, 255, 255, 0.9);
    }

    /* Contensores de Widgets y Controles */
    textarea, input[type="text"] {
        background: linear-gradient(180deg, #ffffff 0%, #eef7ff 100%) !important;
        border: 1px solid #7eb4ea !important;
        border-radius: 10px !important;
        color: #002b49 !important;
    }

    [data-baseweb="select"] > div {
        background: linear-gradient(180deg, #ffffff 0%, #e1f5fe 100%) !important;
        border: 1px solid #81d4fa !important;
        border-radius: 10px !important;
    }

    /* Botones de Gel Verde Frutiger */
    .stButton > button, [data-testid="stDownloadButton"] button {
        background: linear-gradient(180deg, #8bc34a 0%, #4caf50 48%, #388e3c 52%, #2e7d32 100%) !important;
        color: #ffffff !important;
        border: 1px solid #1b5e20 !important;
        border-radius: 25px !important;
        font-weight: 700 !important;
        text-shadow: 0 -1px 1px rgba(0,0,0,0.4) !important;
        box-shadow: inset 0 1px 2px rgba(255,255,255,0.8), 0 4px 10px rgba(0,0,0,0.2) !important;
    }
    .stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(180deg, #aed581 0%, #66bb6a 48%, #43a047 52%, #388e3c 100%) !important;
        transform: translateY(-1px) !important;
    }

    /* Filas de la lista de frecuencias */
    .freq-row {
        background: linear-gradient(90deg, rgba(255,255,255,0.7) 0%, rgba(225,245,254,0.5) 100%);
        border: 1px solid rgba(255,255,255,0.9);
        border-radius: 12px;
        padding: 6px 12px;
        margin: 4px 0;
    }
    .freq-bar {
        background: linear-gradient(180deg, #29b6f6 0%, #0288d1 100%);
        border-radius: 10px;
        box-shadow: inset 0 1px 1px rgba(255,255,255,0.8);
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LÓGICA DE NEGOCIO Y CONFIGURACIÓN
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw

PALETAS = {
    "Frutiger Aqua (Azul/Verde)": ["#004d40", "#00796b", "#009688", "#00acc1", "#039be5", "#0288d1", "#01579b"],
    "Burbuja Cristal (Azul/Rosa)": ["#880e4f", "#ad1457", "#c2185b", "#d81b60", "#1976d2", "#0288d1", "#0097a7"],
    "Escala de grises":          ["#111827","#1f2937","#374151","#4b5563","#6b7280","#9ca3af","#d1d5db"],
    "Azul corporativo":         ["#1e3a5f","#1d4ed8","#2563eb","#3b82f6","#60a5fa","#93c5fd","#0f2942"],
    "Verde institucional":      ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7"],
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
    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words, background_color=fondo,
        color_func=color_func, mask=mascara, collocations=False,
        min_font_size=11, max_font_size=120, prefer_horizontal=0.75, margin=5
    ).generate(texto_limpio)
    
    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig

def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# NUEVA ESTRUCTURA Y NAVEGACIÓN
# ─────────────────────────────────────────────

# Header Superior
st.markdown("""
<div class="aero-header">
    <div>
        <h1 style="margin:0; font-size:1.8rem; color:#002b49;">🌐 WordCloud Studio <span style="font-size:0.9rem; color:#0288d1; font-weight:normal;">v2.0 Aero Edition</span></h1>
        <p style="margin:0; color:#005f73; font-size:0.9rem;">Visualizador interactivo de análisis léxico y minería de texto</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Pestañas principales de navegación
tab_editor, tab_visual, tab_datos, tab_ayuda = st.tabs([
    "✍️ 1. Entrada de Texto", 
    "🎨 2. Estudio de Visualización", 
    "📊 3. Datos y Frecuencias", 
    "❓ Ayuda & Info"
])

# Variables de estado
if "texto_input" not in st.session_state:
    st.session_state["texto_input"] = ""

# ─────────────────────────────────────────────
# TAB 1: ENTRADA DE TEXTO
# ─────────────────────────────────────────────
with tab_editor:
    col_input, col_preset = st.columns([2, 1], gap="medium")
    
    with col_input:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Fuente de Texto")
        fuente = st.radio("Método de ingreso:", ["Escribir o Pegar", "Cargar Archivo (.txt, .csv)"], horizontal=True)
        
        if fuente == "Escribir o Pegar":
            st.session_state["texto_input"] = st.text_area("Ingresa tu texto aquí:", value=st.session_state["texto_input"], height=280, placeholder="Pega un artículo, reseña, transcripción...")
        else:
            archivo = st.file_uploader("Selecciona un archivo", type=["txt", "csv"])
            if archivo:
                if archivo.name.endswith(".txt"):
                    st.session_state["texto_input"] = archivo.read().decode("utf-8", errors="ignore")
                elif archivo.name.endswith(".csv"):
                    df_csv = pd.read_csv(archivo)
                    col_txt = st.selectbox("Selecciona la columna con texto:", df_csv.columns.tolist())
                    st.session_state["texto_input"] = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
                st.success(f"Archivo cargado correctamente ({len(st.session_state['texto_input']):,} caracteres)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preset:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Cargar Ejemplos")
        ejemplos = {
            "Inteligencia Artificial": "La inteligencia artificial transforma los sistemas modernos mediante el aprendizaje automático...",
            "Tecnología 4.0": "La cuarta revolución industrial integra el internet de las cosas, analítica de datos y robótica...",
            "Colombia": "Colombia es un país biodiverso con ecosistemas que van desde los Andes hasta el Amazonas..."
        }
        ejemplo_sel = st.selectbox("Elige una muestra:", list(ejemplos.keys()))
        if st.button("Usar este texto de ejemplo", use_container_width=True):
            st.session_state["texto_input"] = ejemplos[ejemplo_sel]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 2: ESTUDIO DE VISUALIZACIÓN (PANEL DERECHO)
# ─────────────────────────────────────────────
with tab_visual:
    col_canvas, col_controls = st.columns([3, 1], gap="medium")

    # Controles en la columna derecha
    with col_controls:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Ajustes de Diseño")
        
        idioma = st.selectbox("Stopwords:", ["Español", "Inglés", "Ambos", "Ninguno"])
        min_longitud = st.slider("Largo mín. de palabra:", 2, 8, 3)
        palabras_extra = st.text_input("Excluir palabra (sep. comas):", placeholder="ej: además, también")
        
        st.divider()
        paleta_sel = st.selectbox("Paleta cromática:", list(PALETAS.keys()))
        fondo_sel = st.radio("Color de fondo:", ["Blanco", "Negro"], horizontal=True)
        fondo_color = "white" if fondo_sel == "Blanco" else "black"
        forma_sel = st.selectbox("Máscara visual:", list(FORMAS.keys()))
        max_words = st.slider("Máx. de palabras:", 20, 200, 80)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Nube en la columna izquierda
    with col_canvas:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        if not st.session_state["texto_input"].strip():
            st.info("👈 Por favor ingresa texto en la pestaña **1. Entrada de Texto** para generar la nube.")
        else:
            stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
            if palabras_extra.strip():
                stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

            texto_limpio = limpiar_texto(st.session_state["texto_input"], stopwords_set, min_longitud)

            if not texto_limpio.strip():
                st.error("El texto resultante está vacío tras aplicar los filtros.")
            else:
                with st.spinner("Sintetizando gráfica de nube..."):
                    fig_wc = generar_wordcloud(
                        texto_limpio, paleta_sel, max_words, fondo_color,
                        FORMAS[forma_sel], ancho=1000, alto=520
                    )
                
                st.pyplot(fig_wc, use_container_width=True)
                
                # Descarga abajo de la canvas
                img_bytes = fig_a_bytes(fig_wc)
                st.download_button("⬇️ Descargar Imagen en PNG", data=img_bytes, file_name="wordcloud_aero.png", mime="image/png", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 3: DATOS Y FRECUENCIAS
# ─────────────────────────────────────────────
with tab_datos:
    if not st.session_state["texto_input"].strip():
        st.warning("No hay datos para procesar. Ingresa un texto primero.")
    else:
        stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
        texto_limpio = limpiar_texto(st.session_state["texto_input"], stopwords_set, min_longitud)
        df_freq = contar_palabras(texto_limpio)
        
        # Métricas principales arriba
        m1, m2, m3 = st.columns(3)
        m1.metric("Total de Palabras Procesadas", len(texto_limpio.split()))
        m2.metric("Vocabulario Único", len(df_freq))
        m3.metric("Palabra Dominante", df_freq.iloc[0]["Palabra"] if not df_freq.empty else "—")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_list, col_tbl = st.columns([1, 1], gap="medium")
        
        with col_list:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Top 15 Frecuencias")
            top15 = df_freq.head(15)
            max_f = top15["Frecuencia"].max() if not top15.empty else 1
            
            for rank, (_, row) in enumerate(top15.iterrows(), 1):
                p, f = row["Palabra"], int(row["Frecuencia"])
                w = max(10, int((f / max_f) * 180))
                st.markdown(
                    f'<div class="freq-row" style="display:flex; align-items:center; justify-content:space-between;">'
                    f'<span><b>#{rank:02d}</b> {p}</span>'
                    f'<div style="display:flex; align-items:center; gap:8px;">'
                    f'<div class="freq-bar" style="width:{w}px; height:10px;"></div>'
                    f'<b>{f}</b>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

        with col_tbl:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Tabla Completa")
            st.dataframe(df_freq, use_container_width=True, height=380)
            csv_bytes = df_freq.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️️ Exportar CSV de Frecuencias", data=csv_bytes, file_name="frecuencias.csv", mime="text/csv", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 4: AYUDA E INFORMACIÓN
# ─────────────────────────────────────────────
with tab_ayuda:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("¿Qué es este sistema?")
    st.write("""
    Esta aplicación procesa textos en español e inglés, descarta automáticamente conectores y palabras irrelevantes 
    (*stopwords*), y calcula las métricas cuantitativas para generar gráficos con la técnica de empaquetado léxico.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

plt.close("all")
