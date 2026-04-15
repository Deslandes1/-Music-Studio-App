import streamlit as st
import os
import base64
import requests
import tempfile
import subprocess
import wave
import numpy as np
import io
import pedalboard as pb
import soundfile as sf
import time

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="Music Studio Pro", layout="wide")

# Colorful music studio logo (shiny, animated)
def show_music_logo(width=120):
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <div style="text-align: center;">
                <svg width="{width}" height="{width}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#ff007f;stop-opacity:1" />
                            <stop offset="50%" style="stop-color:#ffcc00;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#00ffcc;stop-opacity:1" />
                        </linearGradient>
                        <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#ff6600;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#ff00ff;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                    <!-- Equalizer bars -->
                    <rect x="15" y="30" width="10" height="40" fill="url(#grad1)" rx="3">
                        <animate attributeName="height" values="40;20;50;30;40" dur="1.5s" repeatCount="indefinite" />
                    </rect>
                    <rect x="30" y="20" width="10" height="50" fill="url(#grad2)" rx="3">
                        <animate attributeName="height" values="50;60;30;45;50" dur="1.2s" repeatCount="indefinite" />
                    </rect>
                    <rect x="45" y="10" width="10" height="60" fill="url(#grad1)" rx="3">
                        <animate attributeName="height" values="60;40;70;50;60" dur="1.8s" repeatCount="indefinite" />
                    </rect>
                    <rect x="60" y="25" width="10" height="45" fill="url(#grad2)" rx="3">
                        <animate attributeName="height" values="45;55;35;65;45" dur="1.3s" repeatCount="indefinite" />
                    </rect>
                    <rect x="75" y="35" width="10" height="35" fill="url(#grad1)" rx="3">
                        <animate attributeName="height" values="35;25;45;30;35" dur="1.6s" repeatCount="indefinite" />
                    </rect>
                    <!-- Music note -->
                    <circle cx="50" cy="75" r="8" fill="white" opacity="0.9"/>
                    <path d="M55 75 L55 50 L70 55 L70 60 L58 56 L58 75" fill="white" opacity="0.9"/>
                </svg>
                <p style="color: #FFD700; margin-top: 5px; font-weight: bold;">Music Studio Pro</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "purchase_unlocked" not in st.session_state:
    st.session_state.purchase_unlocked = False

if not st.session_state.authenticated:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e);
        }
        .stApp, .stApp h1, .stApp p, .stApp label, .stMarkdown {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("🔐 Login Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_music_logo(150)
        st.markdown("<h2 style='text-align: center; color: white;'>Music Studio Pro</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #FFD700;'>by GlobalInternet.py</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

# ------------------------------
# AFTER LOGIN – MAIN APP (colorful studio theme)
# ------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
    .stApp label, .stApp .stMarkdown, .stApp .stText, .stApp .stCaption, .stApp .stInfo, 
    .stApp .stSuccess, .stApp .stWarning, .stApp .stError {
        color: white !important;
    }
    .stAlert {
        color: white !important;
    }
    .stButton button {
        color: white !important;
    }
    .stSlider label, .stSlider div[data-baseweb="slider"] span {
        color: white !important;
    }
    .stCheckbox label {
        color: white !important;
    }
    .stNumberInput input, .stTextInput input, .stTextArea textarea {
        color: white !important;
        background-color: rgba(255,255,255,0.1) !important;
    }
    div[data-testid="stTextInput"]:has(input[placeholder="Enter purchase password"]) input {
        color: black !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #ccc !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    section[data-testid="stSidebar"] * {
        color: black !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stTextInput,
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stButton button {
        color: black !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        background-color: #e0e0e0 !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }
    section[data-testid="stSidebar"] p[style*="color: #FFD700"] {
        color: black !important;
    }
    .footer {
        color: white !important;
    }
    .main-header {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .main-header h1 { color: white; margin: 0; font-size: 2.5rem; text-shadow: 0 0 10px #ff00cc; }
    .main-header p { color: #FFD700; margin: 0; font-size: 1.1rem; }
    .download-btn { background-color: #28a745; color: white; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class="main-header">
    <h1>🎧 Music Studio Pro</h1>
    <p>Listen, unlock, download, record, create beats – and sing over tracks!</p>
</div>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 3])
with col_logo:
    show_music_logo(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem; color:white;'>🎵 Preview tracks, upload your own, record voice, mix, and create multi‑track beats.</p>", unsafe_allow_html=True)

# ------------------------------
# SIDEBAR – COMPANY INFO & LOGOUT
# ------------------------------
with st.sidebar:
    st.markdown("## 🎧 GlobalInternet.py")
    show_music_logo(80)
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
        "sing_instruction": "Select a backing track, then record your voice using the recorder above. Use the slider to control backing volume (lower to make your voice louder).",
        "backing_volume_label": "🔊 Backing Track Volume (0=silent, 1=normal, 2=double)",
        "mix_with_recording": "🎤 Use Last Voice Recording to Mix",
        "no_recording_found": "No voice recording found. Please record your voice using the recorder above first.",
        "mix_success": "✅ Mixed track ready! Download below.",
        "mix_error": "Mixing failed. Make sure ffmpeg is installed.",
        "download_mixed": "📥 Download Mixed Track",
        "effects_title": "🎛️ Studio Effects",
        "effects_instruction": "Adjust the knobs below to apply professional effects to your mixed track.",
        "apply_effects_btn": "🎛️ Apply Effects & Download",
        "effects_applied": "✅ Effects applied! Download your final track below.",
        "beat_maker_title": "🥁 Multi‑Track Beat Maker",
        "beat_instruction": "Create patterns for each drum sound. Adjust volume faders, then play all tracks together. Download the mixed beat.",
        "bpm_label": "Tempo (BPM)",
        "play_all": "▶️ Play All Tracks",
        "download_beat": "📥 Download Mixed Beat (WAV)",
        "track_kick": "Kick",
        "track_snare": "Snare",
        "track_hihat": "Hi‑Hat",
        "track_clap": "Clap",
        "track_crash": "Crash",
        "track_tom": "Tom",
        "volume": "Volume"
    },
    "es": {}, "fr": {}, "ht": {}
}
def get_text(key):
    lang = st.session_state.get("language", "en")
    return TEXTS[lang].get(key, TEXTS["en"].get(key, key))

lang_choice = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang_choice]

# ------------------------------
# TRACKS MANAGEMENT (unchanged)
# ------------------------------
TRACKS_DIR = "tracks"
os.makedirs(TRACKS_DIR, exist_ok=True)

with st.expander("🎤 " + get_text("upload_track")):
    uploaded_file = st.file_uploader("", type=["mp3"], label_visibility="collapsed")
    if uploaded_file is not None:
        file_path = os.path.join(TRACKS_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(get_text("upload_success"))
        st.rerun()

DEMO_URLS = [f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{i}.mp3" for i in range(1, 21)]
DEMO_NAMES = [f"SoundHelix Track {i}" for i in range(1, 21)]
RAP_URLS = [
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_2b3c5d6e2f.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_3c4d5e6f7a.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_4d5e6f7a8b.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_5e6f7a8b9c.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_6f7a8b9c0d.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_7a8b9c0d1e.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_8b9c0d1e2f.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_9c0d1e2f3a.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_0d1e2f3a4b.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_1e2f3a4b5c.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_2f3a4b5c6d.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_3a4b5c6d7e.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_4b5c6d7e8f.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_5c6d7e8f9a.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_6d7e8f9a0b.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_7e8f9a0b1c.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_8f9a0b1c2d.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_9a0b1c2d3e.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_0b1c2d3e4f.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/16/audio_1c2d3e4f5a.mp3"
]
RAP_NAMES = [f"Rap/Drill Track {i}" for i in range(1, 21)]

all_demo_urls = DEMO_URLS + RAP_URLS
all_demo_names = DEMO_NAMES + RAP_NAMES
user_tracks = [f for f in os.listdir(TRACKS_DIR) if f.endswith(".mp3")]

all_track_names = all_demo_names + user_tracks
all_track_is_demo = [True] * len(all_demo_names) + [False] * len(user_tracks)
all_track_url_or_path = all_demo_urls + [os.path.join(TRACKS_DIR, f) for f in user_tracks]

if not user_tracks:
    st.info(get_text("no_tracks"))

st.markdown(f"<h3 style='color: #FFD700;'>{get_text('select_track')}</h3>", unsafe_allow_html=True)
selected_index = st.selectbox("", range(len(all_track_names)), format_func=lambda i: all_track_names[i], label_visibility="collapsed")
selected_track_name = all_track_names[selected_index]
is_demo = all_track_is_demo[selected_index]
track_source = all_track_url_or_path[selected_index]

st.audio(track_source, format="audio/mp3")

# ------------------------------
# UNLOCK & DOWNLOAD
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #FFD700;'>{get_text('purchase_password_label')}</h3>", unsafe_allow_html=True)
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
                st.error("Demo fetch failed.")
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
# VOICE RECORDING (simple recorder)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #FFD700;'>{get_text('voice_rec_title')}</h3>", unsafe_allow_html=True)
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
            mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;
                audioPlayback.style.display = 'block';
                statusDiv.innerHTML = 'Recording saved! Click "Save Recording" below.';
                const reader = new FileReader();
                reader.onloadend = () => {
                    const base64data = reader.result.split(',')[1];
                    window.parent.postMessage({ type: 'recording', data: base64data }, '*');
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
voice_file = st.file_uploader("Upload your voice recording (WAV, MP3)", type=["wav", "mp3"], key="voice_upload_sing")
if voice_file is not None:
    st.session_state.voice_bytes = voice_file.getvalue()
    st.success("Voice file loaded. You can now mix it with the backing track.")

# ------------------------------
# SING OVER TRACK (mix voice with backing)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #FFD700;'>{get_text('sing_over_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("sing_instruction"))

backing_volume = st.slider(get_text("backing_volume_label"), 0.0, 2.0, 1.0, 0.05)
if st.button(get_text("mix_with_recording"), use_container_width=True):
    if "voice_bytes" not in st.session_state or not st.session_state.voice_bytes:
        st.warning(get_text("no_recording_found"))
    else:
        voice_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        voice_wav.write(st.session_state.voice_bytes)
        voice_wav.close()
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
            cmd = f'ffmpeg -i "{backing_path}" -i "{voice_wav.name}" -filter_complex "[0:a]volume={backing_volume}[backing];[1:a][backing]amix=inputs=2:duration=longest" -y "{output_path}"'
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                st.success(get_text("mix_success"))
                with open(output_path, "rb") as f:
                    mixed_bytes = f.read()
                    b64 = base64.b64encode(mixed_bytes).decode()
                    st.session_state.mixed_audio_bytes = mixed_bytes
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" style="width: 100%;"></audio>', unsafe_allow_html=True)
                    st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="mixed_track.mp3" class="download-btn">📥 {get_text("download_mixed")}</a>', unsafe_allow_html=True)
            except subprocess.CalledProcessError as e:
                st.error(f"{get_text('mix_error')}: {e.stderr}")
            finally:
                os.unlink(voice_wav.name)
                if is_demo and backing_path:
                    os.unlink(backing_path)
st.caption("Tip: First record your voice using the recorder above, then download it and upload it here.")

# ------------------------------
# STUDIO EFFECTS (pedalboard)
# ------------------------------
if "mixed_audio_bytes" in st.session_state and st.session_state.mixed_audio_bytes:
    st.markdown("---")
    st.markdown(f"<h3 style='color: #FFD700;'>{get_text('effects_title')}</h3>", unsafe_allow_html=True)
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
# ORIGINAL BEAT MAKER (simple)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #FFD700;'>{get_text('beat_maker_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("beat_instruction"))

steps = 16
bpm = st.slider(get_text("bpm_label"), 60, 180, 120, 5)

tracks = [
    {"name": "Kick", "key": "kick", "synthesis": "kick", "vol_default": 1.0},
    {"name": "Snare", "key": "snare", "synthesis": "snare", "vol_default": 1.0},
    {"name": "Hi‑Hat", "key": "hihat", "synthesis": "hihat", "vol_default": 0.7},
    {"name": "Clap", "key": "clap", "synthesis": "clap", "vol_default": 0.8},
    {"name": "Crash", "key": "crash", "synthesis": "crash", "vol_default": 0.6},
    {"name": "Tom", "key": "tom", "synthesis": "tom", "vol_default": 0.9}
]

if "beat_patterns" not in st.session_state:
    st.session_state.beat_patterns = {t["key"]: [False]*steps for t in tracks}
if "beat_volumes" not in st.session_state:
    st.session_state.beat_volumes = {t["key"]: t["vol_default"] for t in tracks}

for tr in tracks:
    st.markdown(f"**{tr['name']}**")
    cols = st.columns(steps+1)
    pattern = st.session_state.beat_patterns[tr["key"]]
    for i in range(steps):
        with cols[i]:
            new_val = st.checkbox(f"{i+1}", key=f"{tr['key']}_{i}", value=pattern[i])
            if new_val != pattern[i]:
                pattern[i] = new_val
                st.session_state.beat_patterns[tr["key"]] = pattern
    with cols[steps]:
        vol = st.slider(get_text("volume"), 0.0, 1.0, st.session_state.beat_volumes[tr["key"]], 0.05, key=f"vol_{tr['key']}")
        st.session_state.beat_volumes[tr["key"]] = vol

def generate_kick(sample_rate, duration=0.2, freq_start=80, freq_end=40):
    t = np.linspace(0, duration, int(sample_rate*duration))
    freq = np.exp(np.linspace(np.log(freq_start), np.log(freq_end), len(t)))
    tone = np.sin(2*np.pi * freq * t)
    click = np.random.normal(0, 0.2, len(t)) * np.exp(-t*100)
    envelope = np.exp(-t*30)
    return (tone + click) * envelope * 0.5

def generate_snare(sample_rate, duration=0.15):
    t = np.linspace(0, duration, int(sample_rate*duration))
    tone = np.sin(2*np.pi * 200 * t) * np.exp(-t*40)
    noise = np.random.normal(0, 0.7, len(t)) * np.exp(-t*30)
    return (tone + noise) * 0.5

def generate_hihat(sample_rate, duration=0.1):
    t = np.linspace(0, duration, int(sample_rate*duration))
    noise = np.random.normal(0, 0.5, len(t)) * np.exp(-t*100)
    return noise * 0.3

def generate_clap(sample_rate, duration=0.1):
    t = np.linspace(0, duration, int(sample_rate*duration))
    noise = np.random.normal(0, 0.6, len(t)) * np.exp(-t*50)
    return noise * 0.4

def generate_crash(sample_rate, duration=0.8):
    t = np.linspace(0, duration, int(sample_rate*duration))
    noise = np.random.normal(0, 0.5, len(t)) * np.exp(-t*5)
    return noise * 0.3

def generate_tom(sample_rate, duration=0.2, freq=120):
    t = np.linspace(0, duration, int(sample_rate*duration))
    tone = np.sin(2*np.pi * freq * t) * np.exp(-t*20)
    return tone * 0.5

def generate_track_audio(pattern, bpm, synthesis_type, duration_seconds=8):
    sample_rate = 44100
    beat_length = 60 / bpm
    step_duration = beat_length / 4
    total_samples = int(sample_rate * duration_seconds)
    audio = np.zeros(total_samples, dtype=np.float32)
    
    for step, active in enumerate(pattern):
        if not active:
            continue
        start_time = step * step_duration
        start_sample = int(start_time * sample_rate)
        if start_sample >= total_samples:
            break
        if synthesis_type == "kick":
            sound = generate_kick(sample_rate)
        elif synthesis_type == "snare":
            sound = generate_snare(sample_rate)
        elif synthesis_type == "hihat":
            sound = generate_hihat(sample_rate)
        elif synthesis_type == "clap":
            sound = generate_clap(sample_rate)
        elif synthesis_type == "crash":
            sound = generate_crash(sample_rate)
        elif synthesis_type == "tom":
            sound = generate_tom(sample_rate)
        else:
            continue
        end_sample = min(start_sample + len(sound), total_samples)
        audio[start_sample:end_sample] += sound[:end_sample-start_sample]
    return audio, sample_rate

if st.button(get_text("play_all")):
    with st.spinner("Generating beat..."):
        mixed_audio = None
        sample_rate = 44100
        duration = 8
        any_active = False
        for tr in tracks:
            pattern = st.session_state.beat_patterns[tr["key"]]
            vol = st.session_state.beat_volumes[tr["key"]]
            if any(pattern):
                any_active = True
                track_audio, sr = generate_track_audio(pattern, bpm, tr["synthesis"], duration)
                if mixed_audio is None:
                    mixed_audio = track_audio * vol
                else:
                    max_len = max(len(mixed_audio), len(track_audio))
                    mixed_audio = np.pad(mixed_audio, (0, max_len - len(mixed_audio)), 'constant')
                    track_audio_pad = np.pad(track_audio, (0, max_len - len(track_audio)), 'constant')
                    mixed_audio += track_audio_pad * vol
        if not any_active:
            st.warning("No patterns selected. Please add some steps.")
        else:
            max_val = np.max(np.abs(mixed_audio))
            if max_val > 0:
                mixed_audio = mixed_audio / max_val * 0.8
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                sf.write(tmp.name, mixed_audio, sample_rate)
                tmp.seek(0)
                audio_bytes = tmp.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<audio controls src="data:audio/wav;base64,{b64}" style="width: 100%;"></audio>', unsafe_allow_html=True)
                st.session_state.generated_beat = audio_bytes
                st.success("Beat generated. You can download it below.")

if st.button(get_text("download_beat")):
    if "generated_beat" in st.session_state and st.session_state.generated_beat:
        b64 = base64.b64encode(st.session_state.generated_beat).decode()
        st.markdown(f'<a href="data:audio/wav;base64,{b64}" download="my_beat.wav" class="download-btn">📥 {get_text("download_beat")}</a>', unsafe_allow_html=True)
    else:
        st.warning("Generate a beat first by clicking 'Play All Tracks'.")

st.caption("Tip: Create patterns for each drum, adjust volume faders, then play all together. Download the mixed WAV and upload it as a track.")

# ------------------------------
# ENHANCED INFINITY BEAT MAKER (8 tracks + continuous loops)
# ------------------------------
st.markdown("---")
st.markdown("<h3 style='color: #FFD700;'>🎛️ Infinity Beat Maker (Pro)</h3>", unsafe_allow_html=True)
st.markdown("Professional 8‑track step sequencer + continuous bass/pad. **Click 'Start Audio' first.**", unsafe_allow_html=True)

infinity_beat_html = """
<div id="infinity-beat-root" style="background:#0a0c16; border-radius:24px; padding:20px; margin:15px 0; border:1px solid #0ff3; font-family: monospace;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px;">
        <div style="display:flex; gap:12px;">
            <button id="startAudioBtn" style="background:#0ff; color:#000; border:none; border-radius:40px; padding:8px 18px; font-weight:bold; cursor:pointer;">🎧 Start Audio</button>
            <button id="playStopBtn" style="background:#1f2a3a; color:#0ff; border:1px solid #0ff; border-radius:40px; padding:8px 18px; font-weight:bold; cursor:pointer;">▶️ Play</button>
        </div>
        <div style="display:flex; gap:15px; align-items:center;">
            <span style="color:#0ff;">BPM</span>
            <input type="range" id="bpmSlider" min="60" max="180" value="120" step="1" style="width:160px;">
            <span id="bpmValue" style="background:#00000066; padding:4px 12px; border-radius:20px; color:#0ff;">120</span>
        </div>
    </div>
    <div style="margin-bottom:28px;">
        <div style="display:grid; grid-template-columns:90px repeat(16, 1fr); gap:4px; margin-bottom:8px; align-items:center;">
            <div style="color:#0ff; font-weight:bold;">Kick</div>
            <div id="kickGrid" style="display:contents;"></div>
        </div>
        <div style="display:grid; grid-template-columns:90px repeat(16, 1fr); gap:4px; margin-bottom:8px; align-items:center;">
            <div style="color:#0ff; font-weight:bold;">Snare</div>
            <div id="snareGrid" style="display:contents;"></div>
        </div>
        <div style="display:grid; grid-template-columns:90px repeat(16, 1fr); gap:4px; margin-bottom:8px; align-items:center;">
            <div style="color:#0ff; font-weight:bold;">Hi-Hat</div>
            <div id="hihatGrid" style="display:contents;"></div>
        </div>
        <div style="display:grid; grid-template-columns:90px repeat(16, 1fr); gap:4px; margin-bottom:8px; align-items:center;">
            <div style="color:#0ff; font-weight:bold;">Clap</div>
            <div id="clapGrid" style="display:contents;"></div>
        </div>
        <div style="display:grid; grid-template-columns:90px repeat(16, 1fr); gap:4px; margin-bottom:8px; align-items:center;">
            <div style="color:#0ff; font-weight:bold;">Open Hat</div>
            <div id="openhatGrid" style="display:contents;"></div>
        </div>
        <div style="display:grid; grid-template-columns:90px repeat(16, 1fr); gap:4px; margin-bottom:8px; align-items:center;">
            <div style="color:#0ff; font-weight:bold;">Crash</div>
            <div id="crashGrid" style="display:contents;"></div>
        </div>
        <div style="display:grid; grid-template-columns:90px repeat(16, 1fr); gap:4px; margin-bottom:8px; align-items:center;">
            <div style="color:#0ff; font-weight:bold;">Tom</div>
            <div id="tomGrid" style="display:contents;"></div>
        </div>
        <div style="display:grid; grid-template-columns:90px repeat(16, 1fr); gap:4px; margin-bottom:8px; align-items:center;">
            <div style="color:#0ff; font-weight:bold;">Perc</div>
            <div id="percGrid" style="display:contents;"></div>
        </div>
    </div>
    <div style="background:#0f1222; border-radius:20px; padding:15px; margin:20px 0;">
        <div style="display:flex; flex-wrap:wrap; gap:30px; justify-content:space-between;">
            <div style="flex:1; min-width:180px;">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                    <button id="bassToggle" style="width:70px; background:#2a2f4a; color:#ccc; border-radius:40px; padding:8px 0; border:none; cursor:pointer;">OFF</button>
                    <span style="color:#0ff;">Deep Bass</span>
                    <span>Vol</span>
                    <input type="range" id="bassVol" min="0" max="1" step="0.01" value="0.8" style="width:80px;">
                </div>
            </div>
            <div style="flex:1; min-width:180px;">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                    <button id="padToggle" style="width:70px; background:#2a2f4a; color:#ccc; border-radius:40px; padding:8px 0; border:none; cursor:pointer;">OFF</button>
                    <span style="color:#0ff;">Ethereal Pad</span>
                    <span>Vol</span>
                    <input type="range" id="padVol" min="0" max="1" step="0.01" value="0.7" style="width:80px;">
                </div>
            </div>
        </div>
    </div>
    <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; margin-top:20px;">
        <div style="display:flex; gap:15px; align-items:center;">
            <span style="color:#0ff;">Master Vol</span>
            <input type="range" id="masterVol" min="0" max="1" step="0.01" value="0.8" style="width:120px;">
        </div>
        <button id="renderBtn" style="background:#0f6; color:#000; border:none; border-radius:40px; padding:8px 20px; font-weight:bold; cursor:pointer;">⬇️ Render WAV (1 bar)</button>
    </div>
    <div id="renderStatus" style="color:#0fa; margin-top:12px; font-size:0.8rem;"></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/tone@14.7.77/build/Tone.js"></script>
<script>
    (function(){
        function createGrid(containerId, steps=16) {
            const container = document.getElementById(containerId);
            if(!container) return;
            container.innerHTML = '';
            for(let i=0;i<steps;i++){
                const btn = document.createElement('button');
                btn.style.width = '100%';
                btn.style.aspectRatio = '1/1';
                btn.style.backgroundColor = '#1f253e';
                btn.style.border = '1px solid #2a3350';
                btn.style.borderRadius = '8px';
                btn.style.cursor = 'pointer';
                btn.dataset.active = 'false';
                btn.dataset.step = i;
                btn.onclick = (e) => {
                    e.stopPropagation();
                    const active = btn.dataset.active === 'true';
                    if(active){
                        btn.dataset.active = 'false';
                        btn.style.backgroundColor = '#1f253e';
                        btn.style.border = '1px solid #2a3350';
                    } else {
                        btn.dataset.active = 'true';
                        btn.style.backgroundColor = '#0ff';
                        btn.style.border = '1px solid #0ff';
                    }
                };
                container.appendChild(btn);
            }
        }
        createGrid('kickGrid', 16);
        createGrid('snareGrid', 16);
        createGrid('hihatGrid', 16);
        createGrid('clapGrid', 16);
        createGrid('openhatGrid', 16);
        createGrid('crashGrid', 16);
        createGrid('tomGrid', 16);
        createGrid('percGrid', 16);

        let transportStarted = false;
        let currentStep = 0;
        let loop = null;
        let isPlaying = false;
        let bassActive = false;
        let padActive = false;

        const kickSynth = new Tone.MembraneSynth({ pitchDecay: 0.05, octaves: 4 }).toDestination();
        const snareSynth = new Tone.NoiseSynth({ noise: { type: 'white' }, envelope: { attack: 0.001, decay: 0.2, sustain: 0 } }).toDestination();
        const hihatSynth = new Tone.NoiseSynth({ noise: { type: 'white' }, envelope: { attack: 0.001, decay: 0.05, sustain: 0 } }).toDestination();
        const clapSynth = new Tone.NoiseSynth({ noise: { type: 'white' }, envelope: { attack: 0.001, decay: 0.1, sustain: 0 } }).toDestination();
        const openhatSynth = new Tone.NoiseSynth({ noise: { type: 'white' }, envelope: { attack: 0.001, decay: 0.15, sustain: 0 } }).toDestination();
        const crashSynth = new Tone.NoiseSynth({ noise: { type: 'white' }, envelope: { attack: 0.01, decay: 0.8, sustain: 0 } }).toDestination();
        const tomSynth = new Tone.MembraneSynth({ pitchDecay: 0.1, octaves: 3 }).toDestination();
        const percSynth = new Tone.MetalSynth({ frequency: 800, envelope: { attack: 0.001, decay: 0.2 } }).toDestination();
        const bassSynth = new Tone.Synth({ oscillator: { type: 'sine' }, envelope: { attack: 0.01, decay: 0.2, sustain: 0.7, release: 0.3 } }).toDestination();
        bassSynth.volume.value = -6;
        const padSynth = new Tone.PolySynth(Tone.Synth, { oscillator: { type: 'sawtooth' }, envelope: { attack: 0.5, decay: 0.8, sustain: 0.6, release: 1.5 } }).toDestination();
        padSynth.volume.value = -12;
        const bassGain = new Tone.Gain(0.8).toDestination();
        const padGain = new Tone.Gain(0.7).toDestination();
        bassSynth.connect(bassGain);
        padSynth.connect(padGain);
        const masterGain = new Tone.Gain(0.8).toDestination();
        [kickSynth, snareSynth, hihatSynth, clapSynth, openhatSynth, crashSynth, tomSynth, percSynth, bassGain, padGain].forEach(s => s.connect(masterGain));
        
        document.getElementById('bassVol').addEventListener('input', (e) => bassGain.gain.value = parseFloat(e.target.value));
        document.getElementById('padVol').addEventListener('input', (e) => padGain.gain.value = parseFloat(e.target.value));
        document.getElementById('masterVol').addEventListener('input', (e) => masterGain.gain.value = parseFloat(e.target.value));
        
        const bpmSlider = document.getElementById('bpmSlider');
        const bpmVal = document.getElementById('bpmValue');
        bpmSlider.addEventListener('input', (e) => {
            const bpm = parseInt(e.target.value);
            bpmVal.innerText = bpm;
            Tone.Transport.bpm.value = bpm;
        });
        
        const bassBtn = document.getElementById('bassToggle');
        const padBtn = document.getElementById('padToggle');
        bassBtn.onclick = () => {
            bassActive = !bassActive;
            bassBtn.innerText = bassActive ? 'ON' : 'OFF';
            bassBtn.style.backgroundColor = bassActive ? '#0f6' : '#2a2f4a';
            bassBtn.style.color = bassActive ? '#000' : '#ccc';
            if(bassActive){
                if(window.bassLoop) window.bassLoop.stop();
                window.bassLoop = new Tone.Loop((time) => { bassSynth.triggerAttackRelease('C2', '8n', time); }, '4n');
                if(transportStarted) window.bassLoop.start(0);
            } else { if(window.bassLoop) window.bassLoop.stop(); }
        };
        padBtn.onclick = () => {
            padActive = !padActive;
            padBtn.innerText = padActive ? 'ON' : 'OFF';
            padBtn.style.backgroundColor = padActive ? '#0f6' : '#2a2f4a';
            padBtn.style.color = padActive ? '#000' : '#ccc';
            if(padActive){
                if(window.padLoop) window.padLoop.stop();
                window.padLoop = new Tone.Loop((time) => { padSynth.triggerAttackRelease(['C3','Eb3','G3','Bb3','D4'], '2n', time); }, '1m');
                if(transportStarted) window.padLoop.start(0);
            } else { if(window.padLoop) window.padLoop.stop(); padSynth.releaseAll(); }
        };
        
        function scheduleStep(time, step) {
            const stepIndex = step % 16;
            document.querySelectorAll('[data-step]').forEach(btn => {
                const stepNum = parseInt(btn.dataset.step);
                btn.style.boxShadow = stepNum === stepIndex ? '0 0 0 2px #0ff' : 'none';
            });
            const getActive = (gridId, idx) => document.querySelectorAll(`#${gridId} button`)[idx]?.dataset.active === 'true';
            if(getActive('kickGrid', stepIndex)) kickSynth.triggerAttackRelease('C1', '16n', time);
            if(getActive('snareGrid', stepIndex)) snareSynth.triggerAttackRelease('16n', time);
            if(getActive('hihatGrid', stepIndex)) hihatSynth.triggerAttackRelease('32n', time);
            if(getActive('clapGrid', stepIndex)) clapSynth.triggerAttackRelease('16n', time);
            if(getActive('openhatGrid', stepIndex)) openhatSynth.triggerAttackRelease('16n', time);
            if(getActive('crashGrid', stepIndex)) crashSynth.triggerAttackRelease('2n', time);
            if(getActive('tomGrid', stepIndex)) tomSynth.triggerAttackRelease('D2', '16n', time);
            if(getActive('percGrid', stepIndex)) percSynth.triggerAttackRelease('32n', time);
        }
        
        function startSequencer() {
            if(loop) loop.dispose();
            loop = new Tone.Loop((time) => { scheduleStep(time, currentStep); currentStep = (currentStep+1)%16; }, '16n');
            loop.start(0);
        }
        
        const playBtn = document.getElementById('playStopBtn');
        playBtn.onclick = async () => {
            if(!transportStarted){
                await Tone.start();
                transportStarted = true;
                document.getElementById('startAudioBtn').innerText = '✅ Audio Ready';
                document.getElementById('startAudioBtn').style.background = '#0f6';
            }
            if(isPlaying){
                Tone.Transport.stop();
                if(loop) loop.stop();
                if(window.bassLoop && bassActive) window.bassLoop.stop();
                if(window.padLoop && padActive) window.padLoop.stop();
                isPlaying = false;
                playBtn.innerText = '▶️ Play';
            } else {
                Tone.Transport.start();
                startSequencer();
                if(bassActive && window.bassLoop) window.bassLoop.start(0);
                if(padActive && window.padLoop) window.padLoop.start(0);
                isPlaying = true;
                playBtn.innerText = '⏹️ Stop';
            }
        };
        
        const startBtn = document.getElementById('startAudioBtn');
        startBtn.onclick = async () => {
            await Tone.start();
            transportStarted = true;
            startBtn.innerText = '✅ Audio Ready';
            startBtn.style.background = '#0f6';
            Tone.Transport.bpm.value = parseInt(bpmSlider.value);
        };
        
        const renderBtn = document.getElementById('renderBtn');
        const statusDiv = document.getElementById('renderStatus');
        renderBtn.onclick = async () => {
            if(!transportStarted){ statusDiv.innerText = '⚠️ Click "Start Audio" first.'; return; }
            statusDiv.innerText = 'Rendering... please wait.';
            const bpm = Tone.Transport.bpm.value;
            const duration = (60 / bpm) * 4;
            const recorder = new Tone.Recorder();
            masterGain.connect(recorder);
            if(loop) loop.stop();
            const tempLoop = new Tone.Loop((time) => { scheduleStep(time, currentStep); currentStep = (currentStep+1)%16; }, '16n');
            const bassWasActive = bassActive, padWasActive = padActive;
            if(window.bassLoop) window.bassLoop.stop();
            if(window.padLoop) window.padLoop.stop();
            const tempBassLoop = bassWasActive ? new Tone.Loop((time) => { bassSynth.triggerAttackRelease('C2', '8n', time); }, '4n') : null;
            const tempPadLoop = padWasActive ? new Tone.Loop((time) => { padSynth.triggerAttackRelease(['C3','Eb3','G3','Bb3','D4'], '2n', time); }, '1m') : null;
            Tone.Transport.stop();
            currentStep = 0;
            Tone.Transport.bpm.value = bpm;
            await Tone.start();
            recorder.start();
            tempLoop.start(0);
            if(tempBassLoop) tempBassLoop.start(0);
            if(tempPadLoop) tempPadLoop.start(0);
            Tone.Transport.start();
            await new Promise(resolve => setTimeout(resolve, duration * 1000 + 200));
            Tone.Transport.stop();
            const recording = await recorder.stop();
            const blob = await recording.getBlob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'infinity_beat_1bar.wav';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            statusDiv.innerHTML = '✅ Render complete! Download started.';
            tempLoop.dispose();
            if(tempBassLoop) tempBassLoop.dispose();
            if(tempPadLoop) tempPadLoop.dispose();
            if(isPlaying){
                startSequencer();
                if(bassActive && window.bassLoop) window.bassLoop.start(0);
                if(padActive && window.padLoop) window.padLoop.start(0);
                Tone.Transport.start();
            }
        };
    })();
</script>
"""
st.components.v1.html(infinity_beat_html, height=750)

# ------------------------------
# FIXED AUTO‑TUNE VOICE RECORDER (Play Processed works)
# ------------------------------
st.markdown("---")
st.markdown("<h3 style='color: #FFD700;'>🎤 Auto‑Tune Voice Recorder</h3>", unsafe_allow_html=True)
st.markdown("Record your voice, apply professional pitch correction (auto‑tune), and download the processed audio.", unsafe_allow_html=True)

autotune_html = """
<div id="autotune-container" style="background:#0f1222; border-radius:24px; padding:20px; margin:15px 0;">
    <div style="display:flex; gap:15px; flex-wrap:wrap; align-items:center; margin-bottom:20px;">
        <button id="atRecordBtn" style="background:#ff4444; color:white; border:none; border-radius:40px; padding:8px 20px; cursor:pointer;">🔴 Record</button>
        <button id="atStopBtn" style="background:#444; color:white; border:none; border-radius:40px; padding:8px 20px; cursor:pointer;" disabled>⏹️ Stop</button>
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="color:#0ff;">Pitch (semitones)</span>
            <input type="range" id="atPitchSlider" min="-12" max="12" value="0" step="1" style="width:150px;">
            <span id="atPitchValue" style="color:#0ff;">0</span>
        </div>
        <button id="atProcessBtn" style="background:#0f6; color:#000; border:none; border-radius:40px; padding:8px 20px; cursor:pointer;">✨ Apply Auto‑Tune & Download</button>
        <button id="atPlayProcessedBtn" style="background:#ffaa00; color:#000; border:none; border-radius:40px; padding:8px 20px; cursor:pointer;">🔊 Play Processed</button>
    </div>
    <div id="atStatus" style="color:#ffaa00; margin-bottom:10px;"></div>
    <audio id="atPlayback" controls style="width:100%; display:none;"></audio>
</div>
<script>
    (function(){
        let mediaRecorder;
        let audioChunks = [];
        let stream = null;
        let recordedBlob = null;
        let processedBlob = null;
        let processedUrl = null;
        const recordBtn = document.getElementById('atRecordBtn');
        const stopBtn = document.getElementById('atStopBtn');
        const statusDiv = document.getElementById('atStatus');
        const playback = document.getElementById('atPlayback');
        const pitchSlider = document.getElementById('atPitchSlider');
        const pitchVal = document.getElementById('atPitchValue');
        const processBtn = document.getElementById('atProcessBtn');
        const playProcessedBtn = document.getElementById('atPlayProcessedBtn');
        
        pitchSlider.addEventListener('input', () => { pitchVal.innerText = pitchSlider.value; });
        
        recordBtn.onclick = async () => {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
                mediaRecorder.onstop = () => {
                    recordedBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const url = URL.createObjectURL(recordedBlob);
                    playback.src = url;
                    playback.style.display = 'block';
                    statusDiv.innerHTML = 'Recording saved. Use slider to set pitch shift, then click "Apply Auto‑Tune & Download".';
                    if(stream) stream.getTracks().forEach(t => t.stop());
                    recordBtn.disabled = false;
                    stopBtn.disabled = true;
                    // reset processed blob
                    processedBlob = null;
                    if(processedUrl) URL.revokeObjectURL(processedUrl);
                    processedUrl = null;
                };
                mediaRecorder.start();
                recordBtn.disabled = true;
                stopBtn.disabled = false;
                statusDiv.innerHTML = '🔴 Recording...';
                playback.style.display = 'none';
            } catch(err) {
                statusDiv.innerHTML = 'Microphone error: ' + err.message;
            }
        };
        stopBtn.onclick = () => {
            if(mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                statusDiv.innerHTML = 'Processing...';
            }
        };
        
        async function pitchShiftAudio(blob, semitones) {
            const arrayBuffer = await blob.arrayBuffer();
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            const sampleRate = audioBuffer.sampleRate;
            const ratio = Math.pow(2, semitones / 12);
            const newLength = Math.floor(audioBuffer.length / ratio);
            const offlineContext = new OfflineAudioContext(audioBuffer.numberOfChannels, newLength, sampleRate);
            const source = offlineContext.createBufferSource();
            source.buffer = audioBuffer;
            source.playbackRate.value = ratio;
            source.connect(offlineContext.destination);
            source.start();
            const renderedBuffer = await offlineContext.startRendering();
            return bufferToWav(renderedBuffer);
        }
        
        processBtn.onclick = async () => {
            if(!recordedBlob) {
                statusDiv.innerHTML = 'No recording. Please record first.';
                return;
            }
            const semitones = parseFloat(pitchSlider.value);
            statusDiv.innerHTML = 'Applying pitch shift (auto‑tune)... please wait.';
            try {
                processedBlob = await pitchShiftAudio(recordedBlob, semitones);
                // Create a download link
                const url = URL.createObjectURL(processedBlob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'autotune_voice.wav';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                // Store for playback
                if(processedUrl) URL.revokeObjectURL(processedUrl);
                processedUrl = url;
                statusDiv.innerHTML = '✅ Auto‑tune applied! Download started. Click "Play Processed" to listen.';
            } catch(err) {
                statusDiv.innerHTML = 'Error processing audio: ' + err.message;
            }
        };
        
        playProcessedBtn.onclick = () => {
            if(processedBlob) {
                if(processedUrl) URL.revokeObjectURL(processedUrl);
                const url = URL.createObjectURL(processedBlob);
                processedUrl = url;
                playback.src = url;
                playback.style.display = 'block';
                playback.load();
                playback.play().catch(e => statusDiv.innerHTML = 'Play error: ' + e.message);
                statusDiv.innerHTML = 'Playing processed voice.';
            } else {
                statusDiv.innerHTML = 'No processed audio. Apply auto‑tune first.';
            }
        };
        
        function bufferToWav(buffer) {
            const numChannels = buffer.numberOfChannels;
            const sampleRate = buffer.sampleRate;
            const format = 1;
            const bitDepth = 16;
            let samples = buffer.getChannelData(0);
            let dataLength = samples.length * 2;
            let bufferLength = 44 + dataLength;
            const arrayBuffer = new ArrayBuffer(bufferLength);
            const view = new DataView(arrayBuffer);
            function writeString(view, offset, str) {
                for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
            }
            writeString(view, 0, 'RIFF');
            view.setUint32(4, bufferLength - 8, true);
            writeString(view, 8, 'WAVE');
            writeString(view, 12, 'fmt ');
            view.setUint32(16, 16, true);
            view.setUint16(20, format, true);
            view.setUint16(22, numChannels, true);
            view.setUint32(24, sampleRate, true);
            view.setUint32(28, sampleRate * numChannels * 2, true);
            view.setUint16(32, numChannels * 2, true);
            view.setUint16(34, bitDepth, true);
            writeString(view, 36, 'data');
            view.setUint32(40, dataLength, true);
            let offset = 44;
            for (let i = 0; i < samples.length; i++) {
                let sample = Math.max(-1, Math.min(1, samples[i]));
                view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
                offset += 2;
            }
            return new Blob([view], { type: 'audio/wav' });
        }
    })();
</script>
"""
st.components.v1.html(autotune_html, height=350)

# ------------------------------
# FOOTER
# ------------------------------
st.markdown('<div class="footer">🎧 *GlobalInternet.py – Music Studio Pro* 🎧</div>', unsafe_allow_html=True)
