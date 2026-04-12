import streamlit as st
import os
import base64
import requests
from pathlib import Path
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import numpy as np
import tempfile
import wave

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
# CUSTOM CSS
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
    .main-header h1 { color: white; margin: 0; font-size: 2.5rem; }
    .main-header p { color: #FFD700; margin: 0; font-size: 1.1rem; }
    .track-card { background: #f8f9fa; border-radius: 15px; padding: 1rem; margin: 0.5rem 0; }
    .unlock-section { background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 20px; margin: 1rem 0; color: white; }
    .download-btn { background-color: #28a745; color: white; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; }
    .footer { text-align: center; color: #666; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎧 Music Studio Pro</h1>
    <p>Listen, unlock, download, record – your premium music destination</p>
</div>
""", unsafe_allow_html=True)

col_flag, col_title = st.columns([1, 3])
with col_flag:
    show_haitian_flag(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem;'>🎵 Preview tracks, record your voice, and unlock downloads with a purchase password.</p>", unsafe_allow_html=True)

# ------------------------------
# SIDEBAR
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
# MULTI-LANGUAGE (simplified for brevity – full dictionary as before)
# ------------------------------
LANGUAGES = {"English":"en","Español":"es","Français":"fr","Kreyòl Ayisyen":"ht"}
TEXTS = {
    "en": {
        "select_track": "🎵 Select a track",
        "purchase_password_label": "🔐 Purchase password (after payment)",
        "unlock_btn": "🔓 Unlock Download",
        "wrong_password": "❌ Incorrect password.",
        "unlock_success": "✅ Download unlocked!",
        "download_btn": "⬇️ Download Track",
        "download_ready": "Click the button to save the file.",
        "contact": "📞 To get the purchase password, contact us.",
        "track_info": "🎧 Preview only – download after unlocking.",
        "demo_track_name": "Demo Track",
        "no_tracks": "No tracks found. Use the demo or upload.",
        "upload_track": "🎤 Upload Your Own Track",
        "upload_btn": "Upload MP3",
        "upload_success": "✅ Track uploaded! Refresh the page.",
        "voice_rec_title": "🎙️ Voice Recording",
        "record_btn": "Start Recording",
        "stop_btn": "Stop & Save",
        "recording_saved": "Recording saved! You can download it below.",
        "download_recording": "📥 Download Recording (WAV)"
    },
    # ... other languages would mirror the structure
}
def get_text(key): return TEXTS["en"].get(key, key)  # simplified for demo

lang_choice = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang_choice]

# ------------------------------
# TRACKS MANAGEMENT (upload + demo)
# ------------------------------
TRACKS_DIR = "tracks"
os.makedirs(TRACKS_DIR, exist_ok=True)

# Upload new track
with st.expander("🎤 " + get_text("upload_track")):
    uploaded_file = st.file_uploader("", type=["mp3"], label_visibility="collapsed")
    if uploaded_file is not None:
        file_path = os.path.join(TRACKS_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(get_text("upload_success"))
        st.rerun()

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

if is_demo:
    st.audio(DEMO_MP3_URL, format="audio/mp3")
else:
    track_path = os.path.join(TRACKS_DIR, selected_track)
    st.audio(track_path, format="audio/mp3")

# ------------------------------
# UNLOCK & DOWNLOAD
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('purchase_password_label')}</h3>", unsafe_allow_html=True)
purchase_pass = st.text_input("", type="password", placeholder="Enter purchase password", label_visibility="collapsed")
if st.button(get_text("unlock_btn"), use_container_width=True):
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
                st.error("Demo fetch failed. Use your own tracks.")
        except:
            st.error("Demo unavailable. Please upload your own MP3 files.")
    else:
        with open(track_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="{selected_track}" class="download-btn">📥 {get_text("download_btn")}</a>', unsafe_allow_html=True)
            st.caption(get_text("download_ready"))
else:
    st.info("🔒 " + get_text("track_info"))

st.markdown(f"<p>{get_text('contact')}</p>", unsafe_allow_html=True)

# ------------------------------
# VOICE RECORDING (using streamlit-webrtc)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('voice_rec_title')}</h3>", unsafe_allow_html=True)

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []
    def recv(self, frame: av.AudioFrame):
        self.audio_frames.append(frame.to_ndarray().copy())
        return frame

webrtc_ctx = webrtc_streamer(
    key="voice-recorder",
    mode=WebRtcMode.SENDRECV,
    audio_receiver_size=1024,
    audio_processor_factory=AudioRecorder,
    media_stream_constraints={"audio": True, "video": False},
)

if webrtc_ctx.audio_processor:
    if st.button(get_text("stop_btn")):
        audio_data = np.concatenate(webrtc_ctx.audio_processor.audio_frames, axis=0)
        # Convert to WAV bytes
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            with wave.open(tmp.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(48000)
                wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
            with open(tmp.name, "rb") as f:
                wav_bytes = f.read()
        st.success(get_text("recording_saved"))
        b64 = base64.b64encode(wav_bytes).decode()
        st.markdown(f'<a href="data:audio/wav;base64,{b64}" download="recording.wav" class="download-btn">📥 {get_text("download_recording")}</a>', unsafe_allow_html=True)
        # Also save to tracks folder if user wants to add as a track
        track_name = st.text_input("Name your recording (to save as a track):")
        if st.button("Save as Track"):
            if track_name:
                if not track_name.endswith(".wav"):
                    track_name += ".wav"
                save_path = os.path.join(TRACKS_DIR, track_name)
                with open(save_path, "wb") as f:
                    f.write(wav_bytes)
                st.success(f"Track saved as {track_name}. Refresh to see it.")
                st.rerun()
else:
    st.info("Click 'Start Recording' above to begin. Allow microphone access.")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown('<div class="footer">🇭🇹 *GlobalInternet.py – Music Studio Pro* 🇭🇹</div>', unsafe_allow_html=True)
