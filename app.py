import streamlit as st
import os
import base64
import requests
from pathlib import Path

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="Music Studio Pro", layout="wide")

def show_haitian_flag(width=100):
    st.image("https://flagcdn.com/w320/ht.png", width=width)

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "purchase_unlocked" not in st.session_state:
    st.session_state.purchase_unlocked = False

if not st.session_state.authenticated:
    st.title("🔐 Login Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_haitian_flag(150)
        st.markdown("<h2 style='text-align: center;'>Music Studio Pro</h2>", unsafe_allow_html=True)
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
# CUSTOM CSS FOR STUDIO LOOK
# ------------------------------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        color: #FFD700;
        margin: 0;
        font-size: 1.1rem;
    }
    .track-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .track-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .unlock-section {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: white;
    }
    .download-btn {
        background-color: #28a745;
        color: white;
        padding: 10px 20px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        transition: background-color 0.3s;
    }
    .download-btn:hover {
        background-color: #218838;
    }
    .footer {
        text-align: center;
        color: #666;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# HEADER
# ------------------------------
st.markdown("""
<div class="main-header">
    <h1>🎧 Music Studio Pro</h1>
    <p>Listen, unlock, download – your premium music destination</p>
</div>
""", unsafe_allow_html=True)

col_flag, col_title = st.columns([1, 3])
with col_flag:
    show_haitian_flag(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem;'>🎵 Preview tracks before you buy. Enter the purchase password (provided after payment) to unlock downloads.</p>", unsafe_allow_html=True)

# ------------------------------
# SIDEBAR – COMPANY INFO & LOGOUT
# ------------------------------
with st.sidebar:
    st.markdown("## 🇭🇹 GlobalInternet.py")
    show_haitian_flag(80)
    st.markdown("### Music Studio Pro")
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
        "purchase_password_label": "🔐 Purchase password (you receive this after payment)",
        "unlock_btn": "🔓 Unlock Download",
        "wrong_password": "❌ Incorrect password. Please contact us to purchase.",
        "unlock_success": "✅ Download unlocked! You can now download the track.",
        "download_btn": "⬇️ Download Track",
        "download_ready": "Download ready! Click the button below to save the file.",
        "contact": "📞 To get the purchase password, contact us on WhatsApp or email.",
        "track_info": "🎧 Preview only – full MP3 download after unlocking.",
        "demo_track_name": "Demo Track (SoundHelix)",
        "no_tracks": "No tracks found. Add MP3 files to the 'tracks' folder or use the demo track.",
        "upload_track": "🎤 Upload Your Own Track (Artist)",
        "upload_btn": "Upload MP3",
        "upload_success": "✅ Track uploaded successfully! Refresh the page to see it in the list."
    },
    "es": {
        "select_track": "🎵 Selecciona una pista",
        "purchase_password_label": "🔐 Contraseña de compra (la recibes después del pago)",
        "unlock_btn": "🔓 Desbloquear descarga",
        "wrong_password": "❌ Contraseña incorrecta. Contáctenos para comprar.",
        "unlock_success": "✅ ¡Descarga desbloqueada! Ahora puedes descargar la pista.",
        "download_btn": "⬇️ Descargar pista",
        "download_ready": "¡Descarga lista! Haz clic en el botón para guardar el archivo.",
        "contact": "📞 Para obtener la contraseña de compra, contáctenos por WhatsApp o email.",
        "track_info": "🎧 Solo vista previa – descarga completa después de desbloquear.",
        "demo_track_name": "Pista de demostración (SoundHelix)",
        "no_tracks": "No se encontraron pistas. Agrega archivos MP3 a la carpeta 'tracks' o usa la pista de demostración.",
        "upload_track": "🎤 Sube tu propia pista (Artista)",
        "upload_btn": "Subir MP3",
        "upload_success": "✅ ¡Pista subida con éxito! Actualiza la página para verla en la lista."
    },
    "fr": {
        "select_track": "🎵 Choisissez un morceau",
        "purchase_password_label": "🔐 Mot de passe d'achat (vous le recevez après paiement)",
        "unlock_btn": "🔓 Déverrouiller le téléchargement",
        "wrong_password": "❌ Mot de passe incorrect. Contactez-nous pour acheter.",
        "unlock_success": "✅ Téléchargement déverrouillé ! Vous pouvez maintenant télécharger le morceau.",
        "download_btn": "⬇️ Télécharger le morceau",
        "download_ready": "Téléchargement prêt ! Cliquez sur le bouton pour enregistrer le fichier.",
        "contact": "📞 Pour obtenir le mot de passe d'achat, contactez-nous par WhatsApp ou email.",
        "track_info": "🎧 Aperçu seulement – téléchargement complet après déverrouillage.",
        "demo_track_name": "Morceau de démonstration (SoundHelix)",
        "no_tracks": "Aucun morceau trouvé. Ajoutez des fichiers MP3 dans le dossier 'tracks' ou utilisez le morceau de démonstration.",
        "upload_track": "🎤 Téléchargez votre propre morceau (Artiste)",
        "upload_btn": "Télécharger MP3",
        "upload_success": "✅ Morceau téléchargé avec succès ! Actualisez la page pour le voir dans la liste."
    },
    "ht": {
        "select_track": "🎵 Chwazi yon mòso",
        "purchase_password_label": "🔐 Modpas acha (ou resevwa li apre peman)",
        "unlock_btn": "🔓 Deklannche telechajman",
        "wrong_password": "❌ Modpas pa bon. Kontakte nou pou achte.",
        "unlock_success": "✅ Telechajman deklannche! Ou ka telechaje mòso a kounye a.",
        "download_btn": "⬇️ Telechaje mòso",
        "download_ready": "Telechajman pare! Klike sou bouton an pou sove fichye a.",
        "contact": "📞 Pou jwenn modpas acha a, kontakte nou sou WhatsApp oswa imèl.",
        "track_info": "🎧 Apèsi selman – telechajman konplè apre deklannchman.",
        "demo_track_name": "Mòso demonstrasyon (SoundHelix)",
        "no_tracks": "Pa gen mòso. Ajoute fichye MP3 nan dosye 'tracks' oswa itilize mòso demonstrasyon an.",
        "upload_track": "🎤 Telechaje pwòp mòso ou (Atis)",
        "upload_btn": "Telechaje MP3",
        "upload_success": "✅ Mòso telechaje avèk siksè! Rafrechi paj la pou wè li nan lis la."
    }
}

def get_text(key):
    lang = st.session_state.get("language", "en")
    return TEXTS[lang].get(key, key)

# Language selector
lang_choice = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang_choice]

# ------------------------------
# TRACKS MANAGEMENT
# ------------------------------
TRACKS_DIR = "tracks"
os.makedirs(TRACKS_DIR, exist_ok=True)

# Upload new track (artist/admin)
with st.expander("🎤 " + get_text("upload_track")):
    uploaded_file = st.file_uploader("", type=["mp3"], label_visibility="collapsed")
    if uploaded_file is not None:
        # Save the file
        file_path = os.path.join(TRACKS_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(get_text("upload_success"))
        st.rerun()

# Get track list
track_files = [f for f in os.listdir(TRACKS_DIR) if f.endswith(".mp3")]
DEMO_MP3_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
DEMO_TRACK_NAME = get_text("demo_track_name")

if not track_files:
    st.info(get_text("no_tracks"))
    track_list = [DEMO_TRACK_NAME]
    is_demo = True
else:
    track_list = track_files
    is_demo = False

st.markdown(f"<h3 style='color: #764ba2;'>{get_text('select_track')}</h3>", unsafe_allow_html=True)
selected_track = st.selectbox("", track_list, label_visibility="collapsed")

# Track preview (audio player)
if is_demo:
    st.audio(DEMO_MP3_URL, format="audio/mp3")
else:
    track_path = os.path.join(TRACKS_DIR, selected_track)
    st.audio(track_path, format="audio/mp3")

# ------------------------------
# UNLOCK & DOWNLOAD SECTION
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>⬇️ {get_text('purchase_password_label')}</h3>", unsafe_allow_html=True)

purchase_pass = st.text_input("", type="password", placeholder="Enter purchase password", label_visibility="collapsed")

if st.button(get_text("unlock_btn"), use_container_width=True):
    # CHANGE THIS PASSWORD TO YOUR SECRET (artist's purchase password)
    if purchase_pass == "music2026":
        st.session_state.purchase_unlocked = True
        st.success(get_text("unlock_success"))
    else:
        st.session_state.purchase_unlocked = False
        st.error(get_text("wrong_password"))

if st.session_state.purchase_unlocked:
    if is_demo:
        try:
            response = requests.get(DEMO_MP3_URL)
            if response.status_code == 200:
                audio_bytes = response.content
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="demo_track.mp3" class="download-btn">📥 {get_text("download_btn")}</a>', unsafe_allow_html=True)
                st.caption(get_text("download_ready"))
            else:
                st.error("Could not fetch demo track. Please add your own MP3 files to the 'tracks' folder.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        with open(track_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="{selected_track}" class="download-btn">📥 {get_text("download_btn")}</a>', unsafe_allow_html=True)
            st.caption(get_text("download_ready"))
else:
    st.info("🔒 " + get_text("track_info"))

st.markdown(f"<p style='margin-top: 20px;'>{get_text('contact')}</p>", unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">🇭🇹 *GlobalInternet.py – Music Studio Pro* 🇭🇹</div>', unsafe_allow_html=True)
