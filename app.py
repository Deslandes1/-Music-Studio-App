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
if "purchase_unlocked" not in st.session_state:
    st.session_state.purchase_unlocked = False

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
# Colorful header
st.markdown(
    """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🎧 Music Studio</h1>
        <p style='color: #FFD700; margin: 0; font-size: 1.1rem;'>Listen to premium tracks | Unlock download with purchase password</p>
    </div>
    """,
    unsafe_allow_html=True
)

col_flag, col_title = st.columns([1, 3])
with col_flag:
    show_haitian_flag(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem;'>🎵 Preview our exclusive collection. To download, you need a purchase password (contact us).</p>", unsafe_allow_html=True)

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
        "purchase_password_label": "🔐 Purchase password (you receive this after payment)",
        "unlock_btn": "🔓 Unlock Download",
        "wrong_password": "❌ Incorrect password. Please contact us to purchase.",
        "unlock_success": "✅ Download unlocked! You can now download the track.",
        "download_btn": "⬇️ Download Track",
        "download_ready": "Download ready! Click the button below to save the file.",
        "contact": "📞 To get the purchase password, contact us on WhatsApp or email.",
        "track_info": "🎧 Preview only – full MP3 download after unlocking."
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
        "track_info": "🎧 Solo vista previa – descarga completa después de desbloquear."
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
        "track_info": "🎧 Aperçu seulement – téléchargement complet après déverrouillage."
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
        "track_info": "🎧 Apèsi selman – telechajman konplè apre deklannchman."
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

# Colorful track selector
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('select_track')}</h3>", unsafe_allow_html=True)
selected_track = st.selectbox("", track_files, label_visibility="collapsed")
track_path = os.path.join(TRACKS_DIR, selected_track)

# Audio player (preview)
st.audio(track_path, format="audio/mp3")

# ------------------------------
# DOWNLOAD UNLOCK SECTION
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>⬇️ {get_text('purchase_password_label')}</h3>", unsafe_allow_html=True)

# Purchase password input
purchase_pass = st.text_input("", type="password", placeholder="Enter purchase password", label_visibility="collapsed")

if st.button(get_text("unlock_btn"), use_container_width=True):
    # The purchase password (you can change this to any secret word)
    if purchase_pass == "music2026":
        st.session_state.purchase_unlocked = True
        st.success(get_text("unlock_success"))
    else:
        st.session_state.purchase_unlocked = False
        st.error(get_text("wrong_password"))

# If unlocked, show download button
if st.session_state.purchase_unlocked:
    st.markdown(f"### {get_text('download_btn')}")
    with open(track_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="{selected_track}" style="background-color: #28a745; color: white; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: bold;">📥 {get_text("download_btn")}</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.caption(get_text("download_ready"))
else:
    st.info("🔒 " + get_text("track_info"))

st.markdown(f"<p style='margin-top: 20px;'>{get_text('contact')}</p>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>🇭🇹 *GlobalInternet.py – Music Studio* 🇭🇹</p>", unsafe_allow_html=True)
