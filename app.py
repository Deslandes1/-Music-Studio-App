import streamlit as st
import os
import base64
import requests
import tempfile
import subprocess
import wave
import numpy as np
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import time

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="Music Studio Pro", layout="wide")

def show_haitian_flag(width=100):
    st.image("https://flagcdn.com/w320/ht.png", width=width)

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
    .main-header { background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
    .main-header h1 { color: white; margin: 0; font-size: 2.5rem; }
    .main-header p { color: #FFD700; margin: 0; font-size: 1.1rem; }
    .unlock-section { background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 20px; margin: 1rem 0; color: white; }
    .download-btn { background-color: #28a745; color: white; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; }
    .footer { text-align: center; color: #666; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎧 Music Studio Pro</h1>
    <p>Listen, unlock, download, record, and sing over tracks</p>
</div>
""", unsafe_allow_html=True)

col_flag, col_title = st.columns([1, 3])
with col_flag:
    show_haitian_flag(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem;'>🎵 Preview tracks, upload your own, record voice, and download mixed recordings.</p>", unsafe_allow_html=True)

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
# MULTI-LANGUAGE (simplified)
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
        "contact": "📞 To get purchase password, contact us.",
        "track_info": "🎧 Preview only – download after unlocking.",
        "demo_track_name": "Demo Track",
        "no_tracks": "No tracks found. Use demo or upload.",
        "upload_track": "🎤 Upload Your Own Track",
        "upload_btn": "Upload MP3",
        "upload_success": "✅ Track uploaded! Refresh.",
        "voice_rec_title": "🎙️ Sing Over Track",
        "record_instruction": "Select a backing track, then record your voice. The app will mix them.",
        "start_rec": "🔴 Start Recording",
        "stop_rec": "⏹️ Stop Recording",
        "recording_saved": "✅ Voice recorded!",
        "download_mixed": "📥 Download Mixed Track (Backing + Voice)",
        "mix_success": "✅ Mixed track ready!",
        "mix_error": "Mixing failed. Check ffmpeg."
    }
}
def get_text(key): return TEXTS["en"].get(key, key)

lang_choice = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang_choice]

# ------------------------------
# TRACKS MANAGEMENT (upload + 20 demos)
# ------------------------------
TRACKS_DIR = "tracks"
os.makedirs(TRACKS_DIR, exist_ok=True)

# 20 demo tracks from SoundHelix (royalty‑free)
DEMO_TRACKS = [f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{i}.mp3" for i in range(1, 21)]
DEMO_NAMES = [f"Demo Track {i}" for i in range(1, 21)]

# Get user-uploaded tracks
user_tracks = [f for f in os.listdir(TRACKS_DIR) if f.endswith(".mp3")]

# Combine demo and user tracks
track_options = DEMO_NAMES + user_tracks
track_type = ["demo"] * len(DEMO_NAMES) + ["user"] * len(user_tracks)

# Upload new track
with st.expander("🎤 " + get_text("upload_track")):
    uploaded_file = st.file_uploader("", type=["mp3"], label_visibility="collapsed")
    if uploaded_file is not None:
        file_path = os.path.join(TRACKS_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(get_text("upload_success"))
        st.rerun()

st.markdown(f"<h3 style='color: #764ba2;'>{get_text('select_track')}</h3>", unsafe_allow_html=True)
selected_index = st.selectbox("", range(len(track_options)), format_func=lambda i: track_options[i], label_visibility="collapsed")
selected_track = track_options[selected_index]
is_demo = track_type[selected_index] == "demo"

if is_demo:
    track_url = DEMO_TRACKS[selected_index]
    st.audio(track_url, format="audio/mp3")
else:
    track_path = os.path.join(TRACKS_DIR, selected_track)
    st.audio(track_path, format="audio/mp3")

# ------------------------------
# UNLOCK & DOWNLOAD (same as before)
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
            response = requests.get(track_url)
            if response.status_code == 200:
                audio_bytes = response.content
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="{selected_track}.mp3" class="download-btn">📥 {get_text("download_btn")}</a>', unsafe_allow_html=True)
                st.caption(get_text("download_ready"))
            else:
                st.error("Demo fetch failed.")
        except:
            st.error("Demo unavailable.")
    else:
        with open(track_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="{selected_track}" class="download-btn">📥 {get_text("download_btn")}</a>', unsafe_allow_html=True)
            st.caption(get_text("download_ready"))
else:
    st.info("🔒 " + get_text("track_info"))

# ------------------------------
# SING OVER TRACK (RECORD VOICE OVER BACKING)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('voice_rec_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("record_instruction"))

# We'll use streamlit-webrtc to record voice, then mix with the selected backing track using ffmpeg.
class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []
    def recv(self, frame: av.AudioFrame):
        self.audio_frames.append(frame.to_ndarray().copy())
        return frame

webrtc_ctx = webrtc_streamer(
    key="voice-recorder-over-track",
    mode=WebRtcMode.SENDRECV,
    audio_receiver_size=1024,
    audio_processor_factory=AudioRecorder,
    media_stream_constraints={"audio": True, "video": False},
)

recorded_audio_path = None

if webrtc_ctx.audio_processor:
    if st.button(get_text("stop_rec")):
        # Save recorded audio as WAV
        audio_data = np.concatenate(webrtc_ctx.audio_processor.audio_frames, axis=0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            with wave.open(tmp_wav.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(48000)
                wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
            recorded_audio_path = tmp_wav.name
        st.success(get_text("recording_saved"))

        # Now mix with backing track if available
        # Get backing track file
        if is_demo:
            # Download demo track to temp file
            resp = requests.get(track_url)
            if resp.status_code == 200:
                backing_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                with open(backing_path, "wb") as f:
                    f.write(resp.content)
            else:
                st.error("Could not download backing track.")
                backing_path = None
        else:
            backing_path = track_path

        if backing_path and recorded_audio_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            # Use ffmpeg to mix backing track and voice (overlay voice, adjust volume if needed)
            # We'll mix with voice at 80% volume, backing at 100%
            cmd = f"ffmpeg -i {backing_path} -i {recorded_audio_path} -filter_complex '[1:a]volume=0.8[voice];[0:a][voice]amix=inputs=2:duration=longest' -y {output_path}"
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
                st.success(get_text("mix_success"))
                with open(output_path, "rb") as f:
                    mixed_bytes = f.read()
                    b64 = base64.b64encode(mixed_bytes).decode()
                    st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="mixed_track.mp3" class="download-btn">📥 {get_text("download_mixed")}</a>', unsafe_allow_html=True)
                os.unlink(output_path)
            except subprocess.CalledProcessError as e:
                st.error(f"{get_text('mix_error')}: {e.stderr.decode()}")
            finally:
                if backing_path and is_demo:
                    os.unlink(backing_path)
                if recorded_audio_path:
                    os.unlink(recorded_audio_path)
else:
    st.info("Click 'Start Recording' above to begin singing over the selected track. Use headphones to avoid feedback.")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown('<div class="footer">🇭🇹 *GlobalInternet.py – Music Studio Pro* 🇭🇹</div>', unsafe_allow_html=True)
