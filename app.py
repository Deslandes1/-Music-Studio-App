import streamlit as st
import os
import base64
from PIL import Image

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="Music Studio", layout="wide")

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
        st.markdown("<h2 style='text-align: center;'>Music Studio</h2>", unsafe_allow_html=True)
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
st.markdown(
    """
    <div style='background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 1.5rem; border-radius: 20px; text-align: center;'>
        <h1 style='color: white; margin: 0;'>🎧 Music Studio</h1>
        <p style='color: #FFD700; margin: 0;'>Listen to demo tracks | Buy to download</p>
    </div>
    """,
    unsafe_allow_html=True
)

col_flag, col_title = st.columns([1, 3])
with col_flag:
    show_haitian_flag(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem;'>Preview our exclusive tracks. To download, you will need a purchase password (contact us).</p>", unsafe_allow_html=True)

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
# MULTI-LANGUAGE SUPPORT (optional)
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
# TRACKS DATABASE (add your own MP3 files in the 'tracks' folder)
# ------------------------------
# Create a folder named 'tracks' in your GitHub repository and put .mp3 files there.
# The code will list all .mp3 files in that folder.
TRACKS_DIR = "tracks"
if not os.path.exists(TRACKS_DIR):
    os.makedirs(TRACKS_DIR)
    # Create a placeholder message if no tracks
    st.warning("No tracks found. Please upload MP3 files to the 'tracks' folder.")

# Get list of MP3 files
track_files = [f for f in os.listdir(TRACKS_DIR) if f.endswith(".mp3")]
if not track_files:
    st.info("No demo tracks available yet. Please contact the administrator.")
    st.stop()

# Let user select a track
selected_track = st.selectbox(get_text("select_track"), track_files)
track_path = os.path.join(TRACKS_DIR, selected_track)

# Display audio player (preview only)
st.audio(track_path, format="audio/mp3")

# Download section
st.markdown("---")
st.markdown(f"### {get_text('download')}")

# Purchase password input
purchase_password = st.text_input(get_text("purchase_password"), type="password")
if st.button(get_text("download_btn")):
    if purchase_password == "music2026":  # ← CHANGE THIS TO YOUR SECRET PURCHASE PASSWORD
        # Provide download link
        with open(track_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="{selected_track}">📥 Click here to save file</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success(get_text("download_success"))
    else:
        st.error(get_text("wrong_password"))

st.caption(get_text("track_info"))
st.markdown(f"📞 {get_text('contact')}")
