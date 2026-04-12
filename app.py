import streamlit as st
import os
import base64
from PIL import Image

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="Music Studio", layout="wide", page_icon="🎵")

def show_haitian_flag(width=100):
    st.image("https://flagcdn.com/w320/ht.png", width=width)

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_haitian_flag(150)
        st.markdown("<h2 style='text-align: center;'>🎧 Music Studio</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>by GlobalInternet.py</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

# ------------------------------
# AFTER LOGIN – MAIN APP
# ------------------------------
# Custom CSS for colorful music theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1DB954, #191414);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .main-header p {
        color: #FFD700;
        margin: 0;
        font-size: 1.2rem;
    }
    .track-card {
        background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    .track-card:hover {
        transform: scale(1.02);
    }
    .equalizer {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60px;
        gap: 4px;
    }
    .equalizer .bar {
        width: 6px;
        height: 20px;
        background-color: #1DB954;
        animation: bounce 0.5s infinite alternate;
    }
    @keyframes bounce {
        0% { height: 10px; }
        100% { height: 40px; }
    }
    .equalizer .bar:nth-child(1) { animation-delay: 0.1s; }
    .equalizer .bar:nth-child(2) { animation-delay: 0.2s; }
    .equalizer .bar:nth-child(3) { animation-delay: 0.3s; }
    .equalizer .bar:nth-child(4) { animation-delay: 0.4s; }
    .equalizer .bar:nth-child(5) { animation-delay: 0.5s; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎧 Music Studio</h1>
    <p>Listen to exclusive tracks | Unlock downloads with purchase password</p>
</div>
""", unsafe_allow_html=True)

col_flag, col_title = st.columns([1, 3])
with col_flag:
    show_haitian_flag(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem;'>Preview our high-quality audio. To download, you need a <strong>purchase password</strong> – contact us to get it.</p>", unsafe_allow_html=True)

# ------------------------------
# SIDEBAR – COMPANY INFO & LOGOUT
# ------------------------------
with st.sidebar:
    st.markdown("## 🇭🇹 GlobalInternet.py")
    show_haitian_flag(80)
    st.markdown("### Music Studio")
    st.markdown("---")
    st.markdown("**Founder & Developer:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 **WhatsApp:** [509 4738-5663](https://wa.me/50947385663)")
    st.markdown("📧 **Email:** deslandes78@gmail.com")
    st.markdown("🌐 **Main website:** [globalinternetsitepy...](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown("**$2,000 USD** (one‑time license, includes full source code, setup, and 1 year support)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All Rights Reserved")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ------------------------------
# MULTI-LANGUAGE SUPPORT
# ------------------------------
LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Kreyòl Ayisyen": "ht"
}
TEXTS = {
    "en": {
        "select_track": "🎵 Select a track",
        "play": "▶️ Play",
        "download": "⬇️ Download",
        "purchase_password": "Purchase password",
        "download_btn": "Unlock & Download",
        "wrong_password": "Incorrect password. Please contact us to purchase.",
        "download_success": "Download ready! Click the button below to save the file.",
        "contact": "Contact us to get the purchase password.",
        "track_info": "Preview only – full download after purchase."
    },
    "es": {
        "select_track": "🎵 Selecciona una pista",
        "play": "▶️ Reproducir",
        "download": "⬇️ Descargar",
        "purchase_password": "Contraseña de compra",
        "download_btn": "Desbloquear y descargar",
        "wrong_password": "Contraseña incorrecta. Contáctenos para comprar.",
        "download_success": "¡Descarga lista! Haga clic en el botón para guardar el archivo.",
        "contact": "Contáctenos para obtener la contraseña de compra.",
        "track_info": "Solo vista previa – descarga completa después de la compra."
    },
    "fr": {
        "select_track": "🎵 Choisissez un morceau",
        "play": "▶️ Lire",
        "download": "⬇️ Télécharger",
        "purchase_password": "Mot de passe d'achat",
        "download_btn": "Déverrouiller et télécharger",
        "wrong_password": "Mot de passe incorrect. Contactez-nous pour acheter.",
        "download_success": "Téléchargement prêt ! Cliquez sur le bouton pour enregistrer le fichier.",
        "contact": "Contactez-nous pour obtenir le mot de passe d'achat.",
        "track_info": "Aperçu seulement – téléchargement complet après achat."
    },
    "ht": {
        "select_track": "🎵 Chwazi yon mòso",
        "play": "▶️ Jwe",
        "download": "⬇️ Telechaje",
        "purchase_password": "Modpas acha",
        "download_btn": "Deklannche ak telechaje",
        "wrong_password": "Modpas pa bon. Kontakte nou pou achte.",
        "download_success": "Telechajman pare! Klike sou bouton an pou sove fichye a.",
        "contact": "Kontakte nou pou jwenn modpas acha a.",
        "track_info": "Se apèsi selman – telechajman konplè apre acha."
    }
}

def get_text(key):
    lang = st.session_state.get("language", "en")
    return TEXTS[lang].get(key, key)

# Language selector
lang_choice = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang_choice]

# ------------------------------
# TRACKS DATABASE
# ------------------------------
TRACKS_DIR = "tracks"
if not os.path.exists(TRACKS_DIR):
    os.makedirs(TRACKS_DIR)
    st.warning("No tracks folder found. Please upload MP3 files to the 'tracks' directory.")

track_files = [f for f in os.listdir(TRACKS_DIR) if f.endswith(".mp3")]
if not track_files:
    st.info("No demo tracks available yet. Please contact the administrator.")
    st.stop()

# ------------------------------
# MAIN MUSIC PLAYER SECTION
# ------------------------------
st.markdown("---")
st.markdown("### 🎶 Demo Playlist")

# Create a grid of tracks (2 columns)
cols = st.columns(2)
for idx, track in enumerate(track_files):
    with cols[idx % 2]:
        with st.container():
            st.markdown(f"""
            <div class="track-card">
                <h4 style="color: #1DB954;">🎵 {track.replace('.mp3', '')}</h4>
                <div class="equalizer">
                    <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.audio(os.path.join(TRACKS_DIR, track), format="audio/mp3")

# ------------------------------
# DOWNLOAD SECTION (with purchase password from secrets)
# ------------------------------
st.markdown("---")
st.markdown(f"### {get_text('download')}")

# Get purchase password from Streamlit secrets
purchase_password_correct = st.secrets.get("PURCHASE_PASSWORD", None)
if not purchase_password_correct:
    st.error("Purchase password not configured. Please set the PURCHASE_PASSWORD secret.")
    st.stop()

selected_track_for_download = st.selectbox(get_text("select_track"), track_files, key="download_select")
purchase_input = st.text_input(get_text("purchase_password"), type="password")
if st.button(get_text("download_btn"), type="primary"):
    if purchase_input == purchase_password_correct:
        track_path = os.path.join(TRACKS_DIR, selected_track_for_download)
        with open(track_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="{selected_track_for_download}">📥 Click here to save file</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success(get_text("download_success"))
    else:
        st.error(get_text("wrong_password"))

st.caption(get_text("track_info"))
st.markdown(f"📞 {get_text('contact')}")
