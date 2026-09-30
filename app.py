import base64
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Cabañas Analá | Delta de Tigre",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

WHATSAPP = "5491164792325"
MAPS = "https://maps.app.goo.gl/qATFhQcSDCi4pQLj8"

CALENDARIOS = {
    "Cabaña A": "e72a2ae4a579f15286ba92ebe80bd1c4593513837038a72879d9143777ec5c8e@group.calendar.google.com",
    "Cabaña B": "e6b0830034e9932954672850adbed53364f9d6f875dc04615a010d5a94458978@group.calendar.google.com",
    "Cabaña C": "7ed47203a014b06795d442d2a26f7b92c324f5ef207901f69e1d50d3eada426c@group.calendar.google.com",
    "Cabaña D": "7c69629ae0432aabbf320e333ee5fa86bd42e6a0d9d3044b175776e7e9d67ece@group.calendar.google.com",
}


# ============================================================
# FUNCIONES
# ============================================================

def imagen_base64(ruta):
    if not Path(ruta).exists():
        return ""
    with open(ruta, "rb") as archivo:
        return base64.b64encode(archivo.read()).decode()


def whatsapp_url(mensaje):
    return f"https://wa.me/{WHATSAPP}?text={quote(mensaje)}"


def conectar_google_calendar():
    credenciales_dict = dict(st.secrets)
    credenciales = service_account.Credentials.from_service_account_info(
        credenciales_dict,
        scopes=["https://www.googleapis.com/auth/calendar.readonly"],
    )
    return build("calendar", "v3", credentials=credenciales)

def cabana_disponible(servicio, calendar_id, entrada, salida):
    inicio = entrada.isoformat() + "T00:00:00-03:00"
    fin = salida.isoformat() + "T00:00:00-03:00"

    eventos = servicio.events().list(
        calendarId=calendar_id,
        timeMin=inicio,
        timeMax=fin,
        singleEvents=True,
    ).execute()

    return len(eventos.get("items", [])) == 0


# ============================================================
# IMÁGENES
# ============================================================

carpeta_fotos = Path("assets/fotos")
foto_portada = carpeta_fotos / "foto5.jpg"
portada64 = imagen_base64(foto_portada)

fotos = []
for extension in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
    fotos.extend(carpeta_fotos.glob(extension))

fotos = sorted(fotos)
galeria = [foto for foto in fotos if foto.name.lower() != "foto5.jpg"][:6]


# ============================================================
# CSS ESTILIZADO
# ============================================================

css = f"""
<style>
/* Reset global de Streamlit corrigiendo el problema del calendario */
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ visibility: hidden; }}

html {{ scroll-behavior: smooth; }}

.stApp {{
    background-color: #F5F1E8;
    color: #26372D;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}}

.block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

/* Textura suave de fondo */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image: radial-gradient(rgba(47,73,56,0.035) 1px, transparent 1px);
    background-size: 20px 20px;
}}

/* Hero Section */
.hero {{
    width: 100%;
    min-height: 88vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 60px 24px;
    background: linear-gradient(rgba(20,35,25,0.30), rgba(20,35,25,0.65)),
                url("data:image/jpeg;base64,{portada64}");
    background-size: cover;
    background-position: center;
    color: white;
    text-align: center;
}}

.hero-inner {{ max-width: 800px; margin: 0 auto; }}
.hero-eyebrow {{
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 4px;
    margin-bottom: 20px;
    opacity: 0.9;
}}
.hero h1 {{
    font-size: 4.2rem !important;
    line-height: 1.05 !important;
    letter-spacing: -1.5px;
    margin-bottom: 20px !important;
    color: #FFFFFF !important;
}}
.hero p {{
    font-size: 1.2rem;
    line-height: 1.6;
    margin: 0 auto 32px auto;
    max-width: 580px;
}}
.hero-button {{
    display: inline-block;
    padding: 16px 36px;
    background: #F5F1E8;
    color: #26372D !important;
    border-radius: 50px;
    text-decoration: none !important;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 1px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}}
.hero-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}}

/* Secciones Generales */
.section {{
    max-width: 1000px;
    margin: 0 auto;
    padding: 70px 24px;
    text-align: center;
}}
.section h2 {{
    font-size: 2.5rem !important;
    font-weight: 600 !important;
    color: #26372D !important;
    margin-bottom: 16px !important;
    letter-spacing: -1px;
}}
.section-lead {{
    color: #5C665E;
    font-size: 1.1rem;
    line-height: 1.7;
    max-width: 640px;
    margin: 0 auto;
}}

/* Estadísticas */
.stats {{
    display: flex;
    justify-content: center;
    gap: 50px;
    margin-top: 40px;
}}
.stat-number {{
    color: #2D4937;
    font-size: 2.4rem;
    font-weight: 800;
}}
.stat-label {{
    color: #6B756D;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}}

/* ========================================= */
/* ESTILOS DEL FORMULARIO DE RESERVA NATIVO  */
/* ========================================= */
div[data-testid="stForm"] {{
    background: #FFFFFF !important;
    border: 1px solid rgba(45,73,55,0.12) !important;
    border-radius: 20px !important;
    padding: 35px !important;
    box-shadow: 0 10px 30px rgba(38,55,45,0.05) !important;
    max-width: 850px !important;
    margin: 0 auto 40px auto !important;
    box-sizing: border-box !important;
}}

div[data-baseweb="input"], div[data-baseweb="select"] > div {{
    background: #F8F6F0 !important;
    border-radius: 12px !important;
    border: 1px solid #E2DED5 !important;
}}

/* Botones Nativos */
div[data-testid="stFormSubmitButton"] button, div[data-testid="stButton"] button {{
    width: 100% !important;
    min-height: 52px !important;
    border-radius: 50px !important;
    background-color: #2D4937 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    transition: background-color 0.2s ease !important;
    display: block !important;
}}
div[data-testid="stFormSubmitButton"] button:hover, div[data-testid="stButton"] button:hover {{
    background-color: #1E3025 !important;
}}

/* ========================================= */
/* CALENDARIO POPOVER (Solución Colores)     */
/* ========================================= */
div[data-baseweb="calendar"] {{
    background-color: #FFFFFF !important;
    border: 1px solid rgba(45,73,55,0.12) !important;
    border-radius: 12px !important;
}}
div[data-baseweb="calendar"] header {{
    visibility: visible !important;
}}
div[data-baseweb="calendar"] * {{
    color: #26372D !important;
}}
div[data-baseweb="calendar"] svg {{
    fill: #2D4937 !important;
}}
div[data-baseweb="calendar"] div[aria-selected="true"] {{
    background-color: #2D4937 !important;
    color: #FFFFFF !important;
}}


/* WhatsApp Result */
.wa-result {{
    max-width: 500px;
    margin: 25px auto;
}}
.wa-result a {{
    display: flex;
    align-items: center;
    justify-content: center;
    height: 54px;
    background: #25D366;
    color: white !important;
    border-radius: 50px;
    text-decoration: none !important;
    font-size: 0.95rem;
    font-weight: 800;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(37,211,102,0.3);
}}

/* Galería de Fotos */
div[data-testid="stImage"] img {{
    border-radius: 16px;
    object-fit: cover;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}}

/* Bloque Verde */
.green-section {{
    background: #2D4937;
    color: #F5F1E8;
    padding: 80px 24px;
    text-align: center;
}}
.green-inner {{ max-width: 680px; margin: 0 auto; }}
.green-section h2 {{
    color: #F5F1E8 !important;
    font-size: 2.5rem !important;
    margin-bottom: 20px !important;
}}
.green-section p {{
    color: #E0E5E0;
    font-size: 1.1rem;
    line-height: 1.8;
}}

/* Servicios Cards */
.servicio {{
    background: rgba(255,255,255,0.5);
    border: 1px solid rgba(45,73,55,0.08);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    height: 100%;
}}
.servicio h3 {{
    font-size: 1.25rem;
    margin-bottom: 10px;
    color: #2D4937;
}}
.servicio p {{ color: #667068; font-size: 0.95rem; line-height: 1.5; }}

/* Footer */
.site-footer {{
    background: #1E3025;
    color: #CBD2CC;
    padding: 60px 24px 100px 24px;
    text-align: center;
    margin-top: 60px;
}}
.site-footer h2 {{ color: #F5F1E8 !important; font-size: 2rem !important; }}

/* Botón Flotante Celular */
.reserva-flotante {{ display: none; }}

@media (max-width: 768px) {{
    .hero h1 {{ font-size: 2.8rem !important; }}
    .stats {{ gap: 20px; }}
    .stat-number {{ font-size: 1.8rem; }}
    
    div[data-testid="stForm"] {{
        padding: 20px 15px !important;
        margin: 0 16px 30px 16px !important;
        width: auto !important;
    }}
    
    .reserva-flotante {{
        display: block;
        position: fixed;
        left: 16px;
        right: 16px;
        bottom: 16px;
        z-index: 9999;
    }}
    .reserva-flotante a {{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 52px;
        background: #2D4937;
        color: white !important;
        border-radius: 50px;
        text-decoration: none !important;
        font-weight: 800;
        box-shadow: 0 5px 20px rgba(0,0,0,0.25);
    }}
}}
</style>
"""

st.markdown(css, unsafe_allow_html=True)


# ============================================================
# PORTADA (HERO)
# ============================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-inner">
        <div class="hero-eyebrow">CABAÑAS ANALÁ · DELTA DE TIGRE</div>
        <h1>Tu lugar<br>en el Delta.</h1>
        <p>Naturaleza, río y tranquilidad.<br>Una escapada diferente, a poco más de una hora de Tigre.</p>
        <a class="hero-button" href="#reservar">VER DISPONIBILIDAD</a>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# INTRODUCCIÓN
# ============================================================

st.markdown(
    """
<section class="section">
    <h2>Desconectá de la ciudad.</h2>
    <p class="section-lead">
        Descubrí un rincón del Delta donde el ritmo cambia. 
        Un lugar rodeado de naturaleza y agua, pensado para descansar y disfrutar sin apuro.
    </p>
    <div class="stats">
        <div>
            <div class="stat-number">4</div>
            <div class="stat-label">Cabañas</div>
        </div>
        <div>
            <div class="stat-number">4</div>
            <div class="stat-label">Huéspedes max</div>
        </div>
        <div>
            <div class="stat-number">100%</div>
            <div class="stat-label">Naturaleza</div>
        </div>
    </div>
</section>
""",
    unsafe_allow_html=True,
)


# ============================================================
# GALERÍA
# ============================================================

st.markdown(
    """
<section class="section" style="padding-bottom: 20px;">
    <h2>Conocé Analá</h2>
    <p class="section-lead">El verde, el río y la tranquilidad son parte de cada estadía.</p>
</section>
""",
    unsafe_allow_html=True,
)

if galeria:
    for i in range(0, len(galeria), 2):
        cols = st.columns(2)
        for col, foto in zip(cols, galeria[i : i + 2]):
            with col:
                st.image(str(foto), use_container_width=True)


# ============================================================
# BLOQUE VERDE
# ============================================================

st.markdown(
    """
<section class="green-section" style="margin-top: 50px;">
    <div class="green-inner">
        <h2>Acá el tiempo corre distinto.</h2>
        <p>
            Despertarse con el sonido del río, tomarse el desayuno sin apuro 
            y dejar que el paisaje marque el ritmo.<br><br>
            Analá es una invitación a disfrutar el Delta de otra manera.
        </p>
    </div>
</section>
""",
    unsafe_allow_html=True,
)


# ============================================================
# EXPERIENCIA / SERVICIOS
# ============================================================

st.markdown(
    """
<section class="section">
    <h2>Viví el Delta</h2>
    <p class="section-lead">Todo lo que necesitás para cambiar el ruido de la ciudad por unos días de descanso.</p>
</section>
""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="servicio">
            <h3>🏡 Tu Cabaña</h3>
            <p>Dos cuartos (matrimonial y de soltero), cocina full equipada, TV con DirecTV, Wifi y climatización para tu mayor comodidad.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="servicio">
            <h3>🎯 Instalaciones</h3>
            <p>Quincho, parrillas internas y externas, mesa de pool, ping pong y metegol para compartir en familia o con amigos.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="servicio">
            <h3>🌊 Al Aire Libre</h3>
            <p>Muelle privado, amplio deck sobre el río y una playita de arena perfecta para disfrutar al máximo el entorno del Delta.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RESERVA (FORMULARIO NATIVO BINDING)
# ============================================================

st.markdown(
    """
<section id="reservar" class="section" style="padding-bottom: 10px;">
    <h2>¿Cuándo querés venir?</h2>
    <p class="section-lead">Elegí tus fechas y consultá la disponibilidad en tiempo real.</p>
</section>
""",
    unsafe_allow_html=True,
)

hoy = date.today()

with st.container():
    with st.form("form_reserva"):
        f_col1, f_col2, f_col3 = st.columns(3)

        with f_col1:
            entrada = st.date_input(
                "Llegada",
                value=hoy + timedelta(days=1),
                min_value=hoy,
                format="DD/MM/YYYY",
            )

        with f_col2:
            salida = st.date_input(
                "Salida",
                value=hoy + timedelta(days=3),
                min_value=hoy + timedelta(days=1),
                format="DD/MM/YYYY",
            )

        with f_col3:
            huespedes = st.selectbox("Huéspedes", [1, 2, 3, 4], index=1)

        buscar = st.form_submit_button("CONSULTAR DISPONIBILIDAD")

# Procesamiento de la búsqueda
if buscar:
    if salida <= entrada:
        st.error("La fecha de salida debe ser posterior a la de llegada.")
    else:
        try:
            servicio_calendar = conectar_google_calendar()
            cabanas_libres = []

            for nombre, calendar_id in CALENDARIOS.items():
                if cabana_disponible(servicio_calendar, calendar_id, entrada, salida):
                    cabanas_libres.append(nombre)

            noches = (salida - entrada).days

            if cabanas_libres:
                st.success("🌿 ¡Tenemos disponibilidad para esas fechas!")

                mensaje_reserva = (
                    f"Hola 👋\n\n"
                    f"Estuve viendo la web de Cabañas Analá y quería consultar para reservar:\n\n"
                    f"📅 Llegada: {entrada.strftime('%d/%m/%Y')}\n"
                    f"📅 Salida: {salida.strftime('%d/%m/%Y')}\n"
                    f"🌙 Noches: {noches}\n"
                    f"👥 Huéspedes: {huespedes}\n\n"
                    f"¡Gracias!"
                )
                url_reserva = whatsapp_url(mensaje_reserva)

                st.markdown(
                    f"""
                    <div style="text-align:center; font-size:1.1rem; margin-bottom:15px;">
                        <strong>{entrada.strftime('%d/%m/%Y')} → {salida.strftime('%d/%m/%Y')}</strong><br>
                        <span style="color:#666;">{noches} noche{'s' if noches != 1 else ''} · {huespedes} huésped{'es' if huespedes != 1 else ''}</span>
                    </div>
                    <div class="wa-result">
                        <a href="{url_reserva}" target="_blank">CONTINUAR POR WHATSAPP 💬</a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning(
                    "No tenemos disponibilidad para las fechas seleccionadas. "
                    "Te recomendamos probar con otros días."
                )

        except Exception as e:
            st.error(
                "Ocurrió un inconveniente al conectar con la agenda. "
                "Por favor intenta nuevamente en unos instantes."
            )


# ============================================================
# UBICACIÓN
# ============================================================

st.markdown(
    """
<section class="section">
    <h2>Llegar también es parte del viaje.</h2>
    <p class="section-lead">
        Analá está ubicada en el Delta, a poco más de una hora de la estación de Tigre.
    </p>
</section>
""",
    unsafe_allow_html=True,
)

_, centro, _ = st.columns([1, 1.5, 1])
with centro:
    st.link_button("📍 VER UBICACIÓN EN GOOGLE MAPS", MAPS, use_container_width=True)


# ============================================================
# FAQ
# ============================================================

st.markdown(
    """
<section class="section" style="padding-bottom: 20px;">
    <h2>Antes de venir</h2>
    <p class="section-lead">Respuestas a las preguntas más frecuentes para planificar tu visita.</p>
</section>
""",
    unsafe_allow_html=True,
)

with st.expander("🚤 ¿Cómo se llega a las cabañas?"):
    st.write(
        "Nos encontramos a poco más de una hora de viaje. "
        "Se llega mediante lancha colectivo de la empresa LÍNEAS DELTA, "
        "saliendo desde la Estación Fluvial de Tigre (Ventanilla N°1, Teléfono: 4749-0537)."
    )

with st.expander("🕒 ¿Cuáles son los horarios de ingreso y salida?"):
    st.write(
        "Para que aproveches el día completo, podés ingresar a partir de la primera lancha "
        "(por ejemplo, la de las 8:00 hs desde Tigre) y el día de salida tenés tiempo para "
        "retirarte hasta las 19:00 hs."
    )

with st.expander("🛒 ¿Cómo hago con la comida y bebidas?"):
    st.write(
        "¡No hace falta que cargues con todo! Diariamente pasa por el muelle una lancha almacenera. "
        "Además, contamos con un vecino que vende bebidas, carbón y comestibles básicos de almacén."
    )

with st.expander("💳 ¿Cómo se realiza la reserva?"):
    st.write(
        "Verificás las fechas disponibles en este sitio web y hacés clic en 'Continuar por WhatsApp' "
        "para finalizar el proceso directo con nosotros."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<footer class="site-footer">
    <h2>Cabañas Analá</h2>
    <p>Delta de Tigre · Buenos Aires</p>
    <p style="font-size:0.85rem; opacity:0.7; margin-top:20px;">Naturaleza · Río · Descanso</p>
</footer>

<div class="reserva-flotante">
    <a href="#reservar">CONSULTAR DISPONIBILIDAD</a>
</div>
""",
    unsafe_allow_html=True,
)