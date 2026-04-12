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
import pedalboard as pb
import soundfile as sf
import io

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
# LANGUAGE
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
        "no_tracks": "No user tracks found. Demo tracks are always available.",
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
        "sing_instruction": "Select a backing track, then record your voice. Use the slider to control backing volume (lower to make your voice louder).",
        "backing_volume_label": "🔊 Backing Track Volume (0=silent, 1=normal, 2=double)",
        "start_sing_rec": "🔴 Start Recording Voice",
        "stop_sing_rec": "⏹️ Stop & Mix with Backing",
        "sing_recording_saved": "✅ Voice recorded! Mixing with backing track...",
        "mix_success": "✅ Mixed track ready! Download below.",
        "mix_error": "Mixing failed. Make sure ffmpeg is installed.",
        "download_mixed": "📥 Download Mixed Track",
        "effects_title": "🎛️ Studio Effects",
        "effects_instruction": "Adjust the knobs below to apply professional effects to your mixed track.",
        "apply_effects_btn": "🎛️ Apply Effects & Download",
        "effects_applied": "✅ Effects applied! Download your final track below."
    },
    "es": {}, "fr": {}, "ht": {}
}
def get_text(key):
    lang = st.session_state.get("language", "en")
    return TEXTS[lang].get(key, TEXTS["en"].get(key, key))

lang_choice = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang_choice]

# ------------------------------
# TRACKS MANAGEMENT (20 demo tracks + user uploads)
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

# 20 demo tracks from SoundHelix (royalty-free)
DEMO_URLS = [f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{i}.mp3" for i in range(1, 21)]
DEMO_NAMES = [f"Demo Track {i}" for i in range(1, 21)]

# User-uploaded tracks
user_tracks = [f for f in os.listdir(TRACKS_DIR) if f.endswith(".mp3")]

# Combine: demos first, then user tracks
all_track_names = DEMO_NAMES + user_tracks
all_track_is_demo = [True] * len(DEMO_NAMES) + [False] * len(user_tracks)
all_track_url_or_path = DEMO_URLS + [os.path.join(TRACKS_DIR, f) for f in user_tracks]

if not user_tracks:
    st.info(get_text("no_tracks"))

st.markdown(f"<h3 style='color: #764ba2;'>{get_text('select_track')}</h3>", unsafe_allow_html=True)
selected_index = st.selectbox("", range(len(all_track_names)), format_func=lambda i: all_track_names[i], label_visibility="collapsed")
selected_track_name = all_track_names[selected_index]
is_demo = all_track_is_demo[selected_index]
track_source = all_track_url_or_path[selected_index]

if is_demo:
    st.audio(track_source, format="audio/mp3")
else:
    st.audio(track_source, format="audio/mp3")

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
    try:
        if is_demo:
            response = requests.get(track_source)
            if response.status_code == 200:
                audio_bytes = response.content
            else:
                st.error("Demo fetch failed. Use your own tracks.")
                audio_bytes = None
        else:
            with open(track_source, "rb") as f:
                audio_bytes = f.read()
        if audio_bytes:
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="{selected_track_name}.mp3" class="download-btn">📥 {get_text("download_btn")}</a>', unsafe_allow_html=True)
            st.caption(get_text("download_ready"))
    except Exception as e:
        st.error(f"Download error: {e}")
else:
    st.info("🔒 " + get_text("track_info"))

st.markdown(f"<p>{get_text('contact')}</p>", unsafe_allow_html=True)

# ------------------------------
# VOICE RECORDING (HTML5)
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
# SING OVER TRACK (WebRTC) with Backing Volume Control
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('sing_over_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("sing_instruction"))

class SingProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []
    def recv(self, frame: av.AudioFrame):
        self.frames.append(frame.to_ndarray().copy())
        return frame

webrtc_ctx = webrtc_streamer(
    key="sing",
    mode=WebRtcMode.SENDRECV,
    audio_receiver_size=1024,
    audio_processor_factory=SingProcessor,
    media_stream_constraints={"audio": True, "video": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
)

if webrtc_ctx.audio_processor:
    # Backing volume slider
    backing_volume = st.slider(
        get_text("backing_volume_label"),
        min_value=0.0, max_value=2.0, value=1.0, step=0.05,
        help="Lower volume to make your voice louder; increase to make backing track dominate."
    )
    if st.button(get_text("stop_sing_rec")):
        frames = webrtc_ctx.audio_processor.frames
        if frames:
            audio_data = np.concatenate(frames, axis=0)
            voice_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with wave.open(voice_wav.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(48000)
                wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
            st.success(get_text("sing_recording_saved"))

            # Get backing track file
            if is_demo:
                resp = requests.get(track_source)
                if resp.status_code == 200:
                    backing_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                    with open(backing_path, "wb") as f:
                        f.write(resp.content)
                else:
                    st.error("Could not download backing track.")
                    backing_path = None
            else:
                backing_path = track_source

            if backing_path:
                output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                # Mix: adjust backing volume, keep voice at original volume
                cmd = f"ffmpeg -i {backing_path} -i {voice_wav.name} -filter_complex '[0:a]volume={backing_volume}[backing];[1:a][backing]amix=inputs=2:duration=longest' -y {output_path}"
                try:
                    subprocess.run(cmd, shell=True, check=True, capture_output=True)
                    st.success(get_text("mix_success"))
                    with open(output_path, "rb") as f:
                        mixed_bytes = f.read()
                        b64 = base64.b64encode(mixed_bytes).decode()
                        st.session_state.mixed_audio_bytes = mixed_bytes
                        st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" style="width: 100%;"></audio>', unsafe_allow_html=True)
                        st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="mixed_track.mp3" class="download-btn">📥 {get_text("download_mixed")}</a>', unsafe_allow_html=True)
                except subprocess.CalledProcessError as e:
                    st.error(f"{get_text('mix_error')}: {e.stderr.decode()}")
                finally:
                    os.unlink(voice_wav.name)
                    if is_demo and backing_path:
                        os.unlink(backing_path)
        else:
            st.warning("No audio captured. Please click the microphone button and record something.")
else:
    st.info("Waiting for recorder to initialize... Click the microphone button when it appears.")

# ------------------------------
# STUDIO EFFECTS
# ------------------------------
if "mixed_audio_bytes" in st.session_state and st.session_state.mixed_audio_bytes:
    st.markdown("---")
    st.markdown(f"<h3 style='color: #764ba2;'>{get_text('effects_title')}</h3>", unsafe_allow_html=True)
    st.markdown(get_text("effects_instruction"))

    audio_data, sample_rate = sf.read(io.BytesIO(st.session_state.mixed_audio_bytes))
    
    st.markdown("#### 🎚️ 3-Band EQ")
    col1, col2, col3 = st.columns(3)
    with col1:
        bass_gain = st.slider("Bass Gain (dB)", -12.0, 12.0, 0.0, 0.1)
    with col2:
        mid_gain = st.slider("Mid Gain (dB)", -12.0, 12.0, 0.0, 0.1)
    with col3:
        treble_gain = st.slider("Treble Gain (dB)", -12.0, 12.0, 0.0, 0.1)

    st.markdown("#### 📢 Compressor")
    compress_amount = st.slider("Compression Amount", 0.0, 1.0, 0.0, 0.01)
    st.markdown("#### 🎸 Reverb")
    reverb_size = st.slider("Room Size", 0.0, 1.0, 0.0, 0.01)
    st.markdown("#### 🎤 Pitch Correction (Auto-Tune)")
    pitch_amount = st.slider("Pitch Amount (semitones)", -12, 12, 0, 1)

    if st.button(get_text("apply_effects_btn"), use_container_width=True):
        with st.spinner("Applying studio effects..."):
            board = pb.Pedalboard([])
            if bass_gain != 0:
                board.append(pb.LowShelfFilter(cutoff_frequency_hz=200, gain_db=bass_gain, q=0.7))
            if mid_gain != 0:
                board.append(pb.PeakFilter(cutoff_frequency_hz=2000, gain_db=mid_gain, q=0.7))
            if treble_gain != 0:
                board.append(pb.HighShelfFilter(cutoff_frequency_hz=4000, gain_db=treble_gain, q=0.7))
            if compress_amount > 0:
                ratio = 1 + (compress_amount * 7)
                threshold_db = -12 * compress_amount
                board.append(pb.Compressor(threshold_db=threshold_db, ratio=ratio, attack_ms=10, release_ms=100))
            if reverb_size > 0:
                room_size = 0.1 + (reverb_size * 0.8)
                board.append(pb.Reverb(room_size=room_size, damping=0.5, wet_level=reverb_size, dry_level=1.0 - reverb_size, width=1.0))
            if pitch_amount != 0:
                board.append(pb.PitchShift(semitones=pitch_amount))
            if board:
                processed_audio = board(audio_data, sample_rate)
            else:
                processed_audio = audio_data
            output_mp3 = io.BytesIO()
            sf.write(output_mp3, processed_audio, sample_rate, format='mp3')
            output_mp3.seek(0)
            final_bytes = output_mp3.read()
            final_b64 = base64.b64encode(final_bytes).decode()
            st.success(get_text("effects_applied"))
            st.markdown(f'<audio controls src="data:audio/mp3;base64,{final_b64}" style="width: 100%;"></audio>', unsafe_allow_html=True)
            st.markdown(f'<a href="data:audio/mp3;base64,{final_b64}" download="final_track.mp3" class="download-btn">📥 Download Final Track (with Effects)</a>', unsafe_allow_html=True)

# ------------------------------
# FOOTER
# ------------------------------
st.markdown('<div class="footer">🇭🇹 *GlobalInternet.py – Music Studio Pro* 🇭🇹</div>', unsafe_allow_html=True)
