import streamlit as st
import os
import base64
import requests
import tempfile
import subprocess
import wave
import numpy as np
from pathlib import Path
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av

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
    .unlock-section { background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 20px; margin: 1rem 0; color: white; }
    .download-btn { background-color: #28a745; color: white; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; }
    .footer { text-align: center; color: #666; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎧 Music Studio Pro</h1>
    <p>Listen, unlock, download, record – and sing over tracks!</p>
</div>
""", unsafe_allow_html=True)

col_flag, col_title = st.columns([1, 3])
with col_flag:
    show_haitian_flag(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem;'>🎵 Preview tracks, upload your own, record voice, and mix your singing with any backing track.</p>", unsafe_allow_html=True)

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
# MULTI-LANGUAGE SUPPORT (simplified – full translation can be added)
# ------------------------------
LANGUAGES = {"English":"en","Español":"es","Français":"fr","Kreyòl Ayisyen":"ht"}
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
        "upload_success": "✅ Track uploaded successfully! Refresh the page to see it in the list.",
        "voice_rec_title": "🎙️ Voice Recording",
        "record_instruction": "Click the button below to start recording. Allow microphone access when prompted.",
        "start_rec": "🔴 Start Recording",
        "stop_rec": "⏹️ Stop Recording",
        "recording_saved": "✅ Recording saved! You can download it or save as a track.",
        "download_recording": "📥 Download Recording (WAV)",
        "save_as_track": "💾 Save as a new track",
        "track_name_label": "Track name (without extension):",
        "track_saved": "✅ Track saved to the library! Refresh the track list.",
        "sing_over_title": "🎤 Sing Over Track (Record Voice + Backing)",
        "sing_instruction": "Select a backing track, then record your voice while it plays. The app will mix them into a single MP3.",
        "start_sing_rec": "🔴 Start Singing Recording",
        "stop_sing_rec": "⏹️ Stop Recording & Mix",
        "sing_recording_saved": "✅ Voice recorded! Mixing with backing track...",
        "mix_success": "✅ Mixed track ready! Download below.",
        "mix_error": "Mixing failed. Make sure ffmpeg is installed.",
        "download_mixed": "📥 Download Mixed Track (Backing + Voice)"
    }
}
def get_text(key): return TEXTS["en"].get(key, key)

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
# UNLOCK & DOWNLOAD (unchanged)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('purchase_password_label')}</h3>", unsafe_allow_html=True)
purchase_pass = st.text_input("", type="password", placeholder="Enter purchase password", label_visibility="collapsed")
if st.button(get_text("unlock_btn"), use_container_width=True):
    if purchase_pass == "music2026":   # ← CHANGE THIS TO YOUR SECRET
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
# VOICE RECORDING (original HTML recorder – kept)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('voice_rec_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("record_instruction"))

recorder_html = """
<div id="recorder-container">
    <button id="recordBtn" style="background-color:#ff4444; color:white; padding:10px 20px; border:none; border-radius:30px; font-weight:bold;">🔴 Start Recording</button>
    <button id="stopBtn" style="background-color:#444444; color:white; padding:10px 20px; border:none; border-radius:30px; font-weight:bold; margin-left:10px;" disabled>⏹️ Stop Recording</button>
    <div id="recording-status" style="margin-top:10px; font-weight:bold;"></div>
    <audio id="audioPlayback" controls style="width:100%; margin-top:10px; display:none;"></audio>
</div>
<script>
    let mediaRecorder;
    let audioChunks = [];
    let stream = null;

    const recordBtn = document.getElementById('recordBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusDiv = document.getElementById('recording-status');
    const audioPlayback = document.getElementById('audioPlayback');

    recordBtn.onclick = async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;
                audioPlayback.style.display = 'block';
                statusDiv.innerHTML = 'Recording saved! Click "Save Recording" below.';
                const reader = new FileReader();
                reader.onloadend = () => {
                    const base64data = reader.result.split(',')[1];
                    const data = { type: 'recording', data: base64data };
                    window.parent.postMessage(data, '*');
                };
                reader.readAsDataURL(audioBlob);
                if (stream) stream.getTracks().forEach(track => track.stop());
                recordBtn.disabled = false;
                stopBtn.disabled = true;
            };

            mediaRecorder.start();
            recordBtn.disabled = true;
            stopBtn.disabled = false;
            statusDiv.innerHTML = '🔴 Recording...';
            audioPlayback.style.display = 'none';
        } catch (err) {
            statusDiv.innerHTML = 'Error accessing microphone: ' + err.message;
        }
    };

    stopBtn.onclick = () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            statusDiv.innerHTML = 'Processing...';
        }
    };
</script>
"""
st.components.v1.html(recorder_html, height=200)

st.markdown("### 🎤 Alternative: Upload a pre‑recorded voice file")
voice_file = st.file_uploader("Upload your voice recording (WAV, MP3)", type=["wav", "mp3"])
if voice_file is not None:
    track_name = st.text_input("Name your recording (to save as a track)", value="my_voice")
    if st.button("Save as Track"):
        if track_name:
            if not (track_name.endswith(".wav") or track_name.endswith(".mp3")):
                track_name += ".wav" if voice_file.type == "audio/wav" else ".mp3"
            save_path = os.path.join(TRACKS_DIR, track_name)
            with open(save_path, "wb") as f:
                f.write(voice_file.getbuffer())
            st.success(f"Track saved as {track_name}. Refresh to see it in the list.")
            st.rerun()
st.caption("Tip: You can record on your phone or computer using any voice recorder, then upload the file here.")

# ------------------------------
# NEW FEATURE: SING OVER TRACK (Record voice + backing track, mix with ffmpeg)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('sing_over_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("sing_instruction"))

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []
    def recv(self, frame: av.AudioFrame):
        self.audio_frames.append(frame.to_ndarray().copy())
        return frame

webrtc_ctx = webrtc_streamer(
    key="sing-over-track",
    mode=WebRtcMode.SENDRECV,
    audio_receiver_size=1024,
    audio_processor_factory=AudioRecorder,
    media_stream_constraints={"audio": True, "video": False},
)

if webrtc_ctx.audio_processor:
    if st.button(get_text("stop_sing_rec")):
        # Save recorded voice as WAV
        audio_data = np.concatenate(webrtc_ctx.audio_processor.audio_frames, axis=0)
        voice_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(voice_wav.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(48000)
            wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
        st.success(get_text("sing_recording_saved"))

        # Get backing track file
        if is_demo:
            # Download demo track
            resp = requests.get(DEMO_MP3_URL)
            if resp.status_code == 200:
                backing_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                with open(backing_path, "wb") as f:
                    f.write(resp.content)
            else:
                st.error("Could not download backing track.")
                backing_path = None
        else:
            backing_path = track_path

        if backing_path:
            # Mix using ffmpeg
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            # Command: mix backing track with voice (voice at 80% volume, adjust as needed)
            cmd = f"ffmpeg -i {backing_path} -i {voice_wav.name} -filter_complex '[1:a]volume=0.8[voice];[0:a][voice]amix=inputs=2:duration=longest' -y {output_path}"
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
                st.success(get_text("mix_success"))
                with open(output_path, "rb") as f:
                    mixed_bytes = f.read()
                    b64 = base64.b64encode(mixed_bytes).decode()
                    st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="mixed_track.mp3" class="download-btn">📥 {get_text("download_mixed")}</a>', unsafe_allow_html=True)
                # Clean up
                os.unlink(output_path)
            except subprocess.CalledProcessError as e:
                st.error(f"{get_text('mix_error')}: {e.stderr.decode()}")
            finally:
                os.unlink(voice_wav.name)
                if is_demo and backing_path:
                    os.unlink(backing_path)
else:
    st.info("Click the 'Start Recording' button in the WebRTC widget above to begin singing. Use headphones to avoid echo.")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown('<div class="footer">🇭🇹 *GlobalInternet.py – Music Studio Pro* 🇭🇹</div>', unsafe_allow_html=True)
