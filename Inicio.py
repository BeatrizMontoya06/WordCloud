"""
☁️ WordCloud Studio — Frutiger Aero Edition
Aplicación Streamlit con interfaz brillante e inspirada en los años 2000 (Aero Glass, Aqua)

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
    page_title="WordCloud Studio — Aero",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — Frutiger Aero / Aqua Glass (Años 2000)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Trebuchet+MS&display=swap');

    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Trebuchet MS', Tahoma, sans-serif !important;
    }

    /* Fondo dinámico estilo Frutiger Aero (Degradado acuático brillante con orbes de luz) */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(255, 255, 255, 0.8) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(160, 230, 255, 0.6) 0%, transparent 50%),
                    linear-gradient(135deg, #cbe5ff 0%, #a2d2ff 35%, #70b8ff 70%, #3a92e8 100%) !important;
        background-attachment: fixed !important;
    }

    /* Panel lateral de cristal esmerilado (Glassmorphism) */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.7) !important;
        box-shadow: 5px 0 15px rgba(0, 80, 160, 0.15) !important;
    }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0d47a1 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        text-shadow: 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    }
    [data-testid="stSidebar"] label {
        color: #1565c0 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] p {
        color: #1a237e !important;
    }

    /* Inputs estilo Windows Aero / Web 2.0 */
    textarea, input[type="text"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f7ff 100%) !important;
        border: 1px solid #7eb4ea !important;
        border-radius: 8px !important;
        color: #0b2545 !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1), 0 1px 0 #ffffff !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 8px rgba(33, 150, 243, 0.6), inset 0 1px 2px rgba(0,0,0,0.08) !important;
    }

    /* Selectbox Aero */
    [data-baseweb="select"] > div {
        background: linear-gradient(180deg, #ffffff 0%, #e3f2fd 100%) !important;
        border: 1px solid #90caf9 !important;
        border-radius: 8px !important;
        color: #0d47a1 !important;
        box-shadow: 0 1px 3px rgba(0,60,130,0.1) !important;
    }

    /* Botones de gel / cristal de los años 2000 */
    .stButton > button, [data-testid="stDownloadButton"] button {
        background: linear-gradient(180deg, #8bc34a 0%, #4caf50 48%, #388e3c 52%, #2e7d32 100%) !important;
        color: #ffffff !important;
        border: 1px solid #1b5e20 !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-shadow: 0 -1px 1px rgba(0, 0, 0, 0.4) !important;
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.7), 0 3px 6px rgba(0,0,0,0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(180deg, #aed581 0%, #66bb6a 48%, #43a047 52%, #388e3c 100%) !important;
        box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.9), 0 4px 10px rgba(0,0,0,0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* Tarjetas de cristal brillante (Glassmorphism + Glossy effect) */
    .header-card, .section-card, .wc-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.75) 0%, rgba(255, 255, 255, 0.45) 100%) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.8) !important;
    }

    /* Tarjetas de métricas */
    [data-testid="metric-container"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.8) 0%, rgba(227,242,253,0.6) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 4px 12px rgba(0, 80, 160, 0.1) !important;
    }
    [data-testid="metric-container"] label {
        color: #1565c0 !important;
        font-weight: 700 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0d47a1 !important;
        font-weight: 800 !important;
        text-shadow: 0 1px 2px rgba(255,255,255,0.8) !important;
    }

    /* Elementos interactivos */
    .freq-row {
        background: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        margin: 5px 0 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04) !important;
    }
    .freq-bar {
        background: linear-gradient(180deg, #29b6f6 0%, #0288d1 100%) !important;
        border-radius: 10px !important;
        box-shadow: inset 0 1px 1px rgba(255,255,255,0.6) !important;
    }
    .rank-tag {
        background: linear-gradient(180deg, #e1f5fe 0%, #b3e5fc 100%) !important;
        border: 1px solid #81d4fa !important;
        border-radius: 8px !important;
        color: #0277bd !important;
        font-weight: 700 !important;
    }
    .uso-tag {
        background: linear-gradient(180deg, #ffffff 0%, #e0f2f1 100%) !important;
        border: 1px solid #80cbd4 !important;
        border-radius: 15px !important;
        padding: 6px 14px !important;
        font-size: 0.85rem !important;
        color: #00695c !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STOPWORDS
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw


# ─────────────────────────────────────────────
# PALETAS PROFESIONALES Y AERO
# ─────────────────────────────────────────────
PALETAS = {
    "Frutiger Aqua (Azul/Verde)": ["#004d40", "#00796b", "#009688", "#00acc1", "#039be5", "#0288d1", "#01579b"],
    "Burbuja Cristal (Azul/Rosa)": ["#880e4f", "#ad1457", "#c2185b", "#d81b60", "#1976d2", "#0288d1", "#0097a7"],
    "Escala de grises":          ["#111827","#1f2937","#374151","#4b5563","#6b7280","#9ca3af","#d1d5db"],
    "Azul corporativo":         ["#1e3a5f","#1d4ed8","#2563eb","#3b82f6","#60a5fa","#93c5fd","#0f2942"],
    "Verde institucional":      ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7"],
    "Terracota":                ["#7c2d12","#9a3412","#c2410c","#ea580c","#f97316","#fb923c","#fdba74"],
}

FORMAS = {
    "Rectángulo": None,
    "Círculo":    "circle",
}

def crear_mascara(forma, size=500):
    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2
        mascara = np.ones((size, size), dtype=np.uint8) * 255
        mascara[(x - cx)**2 + (y - cy)**2 <= (size // 2 - 12)**2] = 0
        return mascara
    return None


# ─────────────────────────────────────────────
# FUNCIONES CORE
# ─────────────────────────────────────────────
def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_longitud]
    return " ".join(palabras)


def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50),
                        columns=["Palabra", "Frecuencia"])


def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma, ancho=1000, alto=520):
    import random
    colores = PALETAS[paleta_nombre]

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        rng = random_state or random.Random()
        return colores[rng.randint(0, len(colores) - 1)]

    mascara = crear_mascara(forma, size=min(ancho, alto))
    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=11, max_font_size=120,
        prefer_horizontal=0.75, relative_scaling=0.5, margin=5,
    ).generate(texto_limpio)

    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig


def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ☁️ WordCloud Studio")
    st.caption("Efecto Frutiger Aero v2.0")
    st.divider()

    # ── Fuente ──
    st.markdown("### FUENTE DE TEXTO")
    fuente = st.radio("fuente", ["✍️ Escribir / Pegar", "📂 Subir archivo"],
                      label_visibility="collapsed")
    texto_input = ""

    if fuente == "✍️ Escribir / Pegar":
        texto_input = st.text_area(
            "Texto:", height=190,
            placeholder="Pega aquí un artículo, reseña, discurso, encuesta...")

        with st.expander("Cargar texto de ejemplo"):
            ejemplos = {
                "Inteligencia Artificial": """
                La inteligencia artificial es una disciplina de la informática orientada a desarrollar
                sistemas capaces de ejecutar tareas que requieren capacidades cognitivas humanas.
                El aprendizaje automático, las redes neuronales profundas y el procesamiento del
                lenguaje natural constituyen los pilares técnicos de los sistemas modernos de
                inteligencia artificial. Los modelos de lenguaje de gran escala, la visión
                computacional y la robótica autónoma representan aplicaciones de vanguardia.
                La inteligencia artificial transforma sectores como la salud, la educación,
                la manufactura, las finanzas y el transporte, generando eficiencias significativas.
                """,
                "Colombia": """
                Colombia es una nación situada en el extremo noroccidental de América del Sur,
                reconocida por su excepcional biodiversidad, riqueza cultural y diversidad de paisajes.
                Bogotá es la capital y principal centro económico, seguida de Medellín, Cali y
                Barranquilla como ciudades de relevancia nacional. El café colombiano goza de
                reconocimiento internacional por su calidad y perfil aromático. La floricultura
                colombiana abastece mercados globales con alta competitividad. El país alberga
                ecosistemas del Amazonas, los Andes, el Caribe y el Pacífico, constituyéndose
                como uno de los territorios con mayor biodiversidad del planeta.
                """,
                "Tecnología 4.0": """
                La cuarta revolución industrial redefine los modelos productivos mediante la
                convergencia de tecnologías digitales avanzadas. El Internet de las cosas,
                la inteligencia artificial, el análisis de grandes datos, la robótica colaborativa
                y la automatización inteligente son pilares estratégicos de la industria moderna.
                Las fábricas inteligentes integran sensores, conectividad y analítica para
                optimizar procesos en tiempo real. La manufactura aditiva, los gemelos digitales
                y la realidad aumentada transforman la ingeniería de producción. La computación
                en la nube y la ciberseguridad son habilitadores fundamentales de la
                transformación digital empresarial.
                """,
            }
            ejemplo_sel = st.selectbox("Ejemplo:", list(ejemplos.keys()),
                                       label_visibility="collapsed")
            if st.button("Cargar texto seleccionado"):
                st.session_state["texto_ejemplo"] = ejemplos[ejemplo_sel]
                st.rerun()

        if "texto_ejemplo" in st.session_state and not texto_input:
            texto_input = st.session_state["texto_ejemplo"]

    else:
        archivo = st.file_uploader("Archivo:", type=["txt", "csv"],
                                   label_visibility="collapsed")
        if archivo:
            if archivo.name.endswith(".txt"):
                texto_input = archivo.read().decode("utf-8", errors="ignore")
            elif archivo.name.endswith(".csv"):
                df_csv = pd.read_csv(archivo)
                col_txt = st.selectbox("Columna de texto:", df_csv.columns.tolist())
                texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
            st.success(f"Archivo cargado — {len(texto_input):,} caracteres")

    st.divider()

    # ── Procesamiento ──
    st.markdown("### PROCESAMIENTO")
    idioma         = st.selectbox("Stopwords:", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud   = st.slider("Longitud mínima de palabra", 2, 8, 3)
    palabras_extra = st.text_input("Excluir palabras adicionales:",
                                   placeholder="ej: también, así, aquí")

    st.divider()

    # ── Apariencia ──
    st.markdown("### APARIENCIA")
    paleta_sel  = st.selectbox("Paleta:", list(PALETAS.keys()))
    fondo_sel   = st.radio("Fondo:", ["Blanco", "Negro"], horizontal=True)
    fondo_color = "white" if fondo_sel == "Blanco" else "black"
    forma_sel   = st.selectbox("Forma:", list(FORMAS.keys()))
    max_words   = st.slider("Máximo de palabras:", 20, 200, 80)

    st.divider()
    generar = st.button("GENERAR NUBE  ↗", use_container_width=True)


# ─────────────────────────────────────────────
# CONTENIDO PRINCIPAL
# ─────────────────────────────────────────────

# Header
st.markdown("""
<div class="header-card">
    <h1 style="margin:0; font-size:2.1rem; color:#0d47a1; text-shadow: 0 1px 2px rgba(255,255,255,0.8);">☁️ WordCloud Studio</h1>
    <p style="margin:6px 0 0 0; color:#1565c0 !important; font-size:1rem; font-weight:500;">
        Análisis de frecuencia léxica y visualización de nubes de palabras
    </p>
</div>
""", unsafe_allow_html=True)

# ── Pantalla de bienvenida ──
if not generar or not texto_input.strip():
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#0d47a1;'>Acerca de esta herramienta</h3>", unsafe_allow_html=True)
        st.markdown("""
        Una **nube de palabras** representa visualmente la frecuencia de términos en un texto:
        las palabras más frecuentes aparecen con mayor tamaño, permitiendo identificar
        los temas centrales de un corpus de manera intuitiva.
        """)

        for icono, titulo, desc in [
            ("📊", "Análisis de frecuencia", "Identifica los términos dominantes de cualquier corpus textual."),
            ("🔍", "Filtrado inteligente", "Elimina palabras vacías (*stopwords*) en español e inglés."),
            ("🎨", "Personalización visual", "Selecciona paleta, forma y densidad de la nube."),
            ("⬇️", "Exportación", "Descarga la imagen en alta resolución y la tabla de frecuencias en CSV."),
        ]:
            st.markdown(
                f'<div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">'
                f'<span style="font-size:1.4rem;">{icono}</span>'
                f'<div><strong style="color:#0d47a1;">{titulo}</strong>'
                f'<p style="margin:0; color:#1b4965 !important; font-size:0.88rem;">{desc}</p></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<h4 style='color:#0d47a1;'>Instrucciones</h4>", unsafe_allow_html=True)
        for i, paso in enumerate([
            "Ingresa o sube un texto en el panel lateral.",
            "Configura el idioma de *stopwords*, paleta y número de palabras.",
            "Haz clic en **GENERAR NUBE ↗**.",
            "Descarga la imagen PNG o la tabla CSV.",
        ], 1):
            st.markdown(f"**{i}.** {paso}")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#0d47a1;'>Aplicaciones frecuentes</h3>", unsafe_allow_html=True)
        for caso in [
            "📰 Análisis de prensa y noticias",
            "📋 Resultados de encuestas abiertas",
            "💬 Reseñas y comentarios de clientes",
            "🎓 Análisis de textos académicos",
            "🗳️ Discursos y documentos políticos",
            "📚 Estudios literarios y de corpus",
            "📊 Informes de inteligencia de negocio",
        ]:
            st.markdown(
                f'<span class="uso-tag">{caso}</span>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#0d47a1;'>Paletas disponibles</h3>", unsafe_allow_html=True)
        for nombre in PALETAS.keys():
            st.markdown(
                f'<div style="padding:4px 0; color:#0277bd; font-weight:600; font-size:0.9rem;">'
                f'• {nombre}'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    if not texto_input.strip() and generar:
        st.warning("Ingresa un texto en el panel lateral antes de generar la nube.")
    st.stop()


# ─────────────────────────────────────────────
# PROCESAMIENTO Y RESULTADOS
# ─────────────────────────────────────────────
stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
if palabras_extra.strip():
    stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

texto_limpio = limpiar_texto(texto_input, stopwords_set, min_longitud)

if not texto_limpio.strip():
    st.error("El texto resultante está vacío. Reduce la longitud mínima o cambia la configuración de stopwords.")
    st.stop()

df_freq        = contar_palabras(texto_limpio)
total_palabras = len(texto_limpio.split())
vocabulario    = len(df_freq)

# ── Métricas ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("Palabras procesadas",     f"{total_palabras:,}")
m2.metric("Vocabulario único",       f"{vocabulario:,}")
m3.metric("Término más frecuente",   df_freq.iloc[0]["Palabra"] if not df_freq.empty else "—")
m4.metric("Frecuencia máxima",       int(df_freq.iloc[0]["Frecuencia"]) if not df_freq.empty else 0)

st.markdown("<br>", unsafe_allow_html=True)

# ── Nube ──
with st.spinner("Generando nube de palabras..."):
    fig_wc = generar_wordcloud(
        texto_limpio, paleta_sel, max_words, fondo_color,
        FORMAS[forma_sel], ancho=1000, alto=520,
    )

st.markdown('<div class="wc-container">', unsafe_allow_html=True)
st.markdown(f"<span style='color:#0d47a1; font-weight:600;'>Nube de palabras</span> &nbsp;·&nbsp; Paleta: <i>{paleta_sel}</i> &nbsp;·&nbsp; Fondo: <i>{fondo_sel}</i> &nbsp;·&nbsp; {max_words} palabras máx.", unsafe_allow_html=True)
st.pyplot(fig_wc, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

img_bytes = fig_a_bytes(fig_wc)
st.download_button(
    "⬇️ Descargar imagen PNG",
    data=img_bytes, file_name="wordcloud.png", mime="image/png",
    use_container_width=True,
)

st.divider()

# ── Análisis ──
col_freq, col_tabla = st.columns([3, 2], gap="large")

with col_freq:
    st.markdown("<h3 style='color:#0d47a1;'>Frecuencia léxica — Top 20</h3>", unsafe_allow_html=True)
    top20    = df_freq.head(20)
    max_freq = top20["Frecuencia"].max()

    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        p = row["Palabra"]
        f = int(row["Frecuencia"])
        barra_w = max(12, int((f / max_freq) * 210))
        st.markdown(
            f'<div class="freq-row" style="display:flex; align-items:center; gap:12px;">'
            f'<span class="rank-tag" style="padding:2px 8px;">#{rank:02d}</span>'
            f'<span style="font-weight:600; color:#0b2545; min-width:130px;">{p}</span>'
            f'<div class="freq-bar" style="width:{barra_w}px; height:12px;"></div>'
            f'<span style="font-weight:700; color:#0288d1; min-width:28px; text-align:right;">{f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_tabla:
    st.markdown("<h3 style='color:#0d47a1;'>Tabla de frecuencias</h3>", unsafe_allow_html=True)
    st.dataframe(
        df_freq.head(30).style
               .background_gradient(subset=["Frecuencia"], cmap="Blues")
               .format({"Frecuencia": "{:,}"}),
        use_container_width=True, height=500,
    )
    csv_bytes = df_freq.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️️ Exportar tabla (.csv)",
        data=csv_bytes, file_name="frecuencias.csv", mime="text/csv",
        use_container_width=True,
    )

plt.close("all")
