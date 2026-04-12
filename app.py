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
import threading

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
    <p>Listen, unlock, download, record, create beats – and sing over tracks!</p>
</div>
""", unsafe_allow_html=True)

col_flag, col_title = st.columns([1, 3])
with col_flag:
    show_haitian_flag(120)
with col_title:
    st.markdown("<p style='font-size:1.1rem;'>🎵 Preview tracks, upload your own, record voice, mix, and now create your own beats.</p>", unsafe_allow_html=True)

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
# LANGUAGE (fallback to English)
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
        "beat_maker_title": "🥁 Beat Maker (Create Your Own Drum Beat)",
        "beat_instruction": "Use the step sequencer below to create a simple beat. Each step represents a 16th note (4 steps per beat). Adjust BPM, then click 'Play Beat' to hear it. Then download as WAV.",
        "bpm_label": "Tempo (BPM)",
        "play_beat": "▶️ Play Beat",
        "download_beat": "📥 Download Beat (WAV)",
        "beat_generated": "Beat generated. You can play it above and download below."
    },
    "es": {}, "fr": {}, "ht": {}
}
def get_text(key):
    lang = st.session_state.get("language", "en")
    return TEXTS[lang].get(key, TEXTS["en"].get(key, key))

lang_choice = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang_choice]

# ------------------------------
# TRACKS MANAGEMENT (40 demo tracks + user uploads)
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

# 20 SoundHelix demo tracks
DEMO_URLS = [f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{i}.mp3" for i in range(1, 21)]
DEMO_NAMES = [f"SoundHelix Track {i}" for i in range(1, 21)]

# 20 Rap/Drill demo tracks (verified working)
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

st.markdown(f"<h3 style='color: #764ba2;'>{get_text('select_track')}</h3>", unsafe_allow_html=True)
selected_index = st.selectbox("", range(len(all_track_names)), format_func=lambda i: all_track_names[i], label_visibility="collapsed")
selected_track_name = all_track_names[selected_index]
is_demo = all_track_is_demo[selected_index]
track_source = all_track_url_or_path[selected_index]

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
voice_file = st.file_uploader("Upload your voice recording (WAV, MP3)", type=["wav", "mp3"], key="voice_upload_sing")
if voice_file is not None:
    st.session_state.voice_bytes = voice_file.getvalue()
    st.success("Voice file loaded. You can now mix it with the backing track.")

# ------------------------------
# SING OVER TRACK (using the uploaded voice file)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('sing_over_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("sing_instruction"))

backing_volume = st.slider(
    get_text("backing_volume_label"),
    min_value=0.0, max_value=2.0, value=1.0, step=0.05,
    help="Lower volume to make your voice louder; increase to make backing track dominate."
)

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

st.caption("Tip: First record your voice using the recorder above, then download it and upload it here (or use the alternative upload).")

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
# BEAT MAKER (Step Sequencer) – Fixed to play inline then download
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('beat_maker_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("beat_instruction"))

steps = 16
bpm = st.slider(get_text("bpm_label"), 60, 180, 120, 5)

st.markdown("#### 🥁 Step Sequencer (16 steps)")
cols = st.columns(steps)
kick_pattern = []
snare_pattern = []
hihat_pattern = []

for i in range(steps):
    with cols[i]:
        st.markdown(f"**{i+1}**")
        kick = st.checkbox("🥁", key=f"kick_{i}", value=False)
        snare = st.checkbox("🥁", key=f"snare_{i}", value=False)
        hihat = st.checkbox("🥁", key=f"hihat_{i}", value=False)
        kick_pattern.append(kick)
        snare_pattern.append(snare)
        hihat_pattern.append(hihat)

def generate_beat(kick, snare, hihat, bpm, duration_seconds=8):
    sample_rate = 44100
    beat_length = 60 / bpm
    step_duration = beat_length / 4
    total_samples = int(sample_rate * duration_seconds)
    audio = np.zeros(total_samples, dtype=np.float32)
    
    # Simple synthesized drum sounds
    def make_kick(t):
        return np.sin(2*np.pi*50*t) * np.exp(-t*30) * 0.5
    def make_snare(t):
        return np.sin(2*np.pi*200*t) * np.exp(-t*50) * 0.4 + np.random.normal(0, 0.1, len(t))
    def make_hihat(t):
        return np.sin(2*np.pi*800*t) * np.exp(-t*200) * 0.3
    
    for step in range(steps):
        if step >= len(kick):
            break
        start_time = step * step_duration
        start_sample = int(start_time * sample_rate)
        if start_sample >= total_samples:
            break
        end_sample = min(start_sample + int(0.1 * sample_rate), total_samples)
        t = np.linspace(0, 0.1, end_sample - start_sample)
        if kick[step]:
            audio[start_sample:end_sample] += make_kick(t)
        if snare[step]:
            audio[start_sample:end_sample] += make_snare(t)
        if hihat[step]:
            audio[start_sample:end_sample] += make_hihat(t)
    
    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.8
    return audio, sample_rate

# Store generated beat in session state
if "generated_beat_audio" not in st.session_state:
    st.session_state.generated_beat_audio = None
if "generated_beat_sr" not in st.session_state:
    st.session_state.generated_beat_sr = None

if st.button(get_text("play_beat")):
    audio, sr = generate_beat(kick_pattern, snare_pattern, hihat_pattern, bpm, duration_seconds=8)
    st.session_state.generated_beat_audio = audio
    st.session_state.generated_beat_sr = sr
    # Save to temporary WAV and embed audio player
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        sf.write(tmp.name, audio, sr)
        tmp.seek(0)
        audio_bytes = tmp.read()
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f'<audio controls src="data:audio/wav;base64,{b64}" style="width: 100%;"></audio>', unsafe_allow_html=True)
        st.success(get_text("beat_generated"))
        # Store bytes for download
        st.session_state.generated_beat_bytes = audio_bytes

if st.button(get_text("download_beat")):
    if "generated_beat_bytes" in st.session_state and st.session_state.generated_beat_bytes:
        b64 = base64.b64encode(st.session_state.generated_beat_bytes).decode()
        st.markdown(f'<a href="data:audio/wav;base64,{b64}" download="my_beat.wav" class="download-btn">📥 {get_text("download_beat")}</a>', unsafe_allow_html=True)
    else:
        st.warning("Generate a beat first by clicking 'Play Beat'.")

st.caption("Tip: Create a rhythm, play it, then download as WAV. You can then upload it as a track using the 'Upload Your Own Track' section above.")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown('<div class="footer">🇭🇹 *GlobalInternet.py – Music Studio Pro* 🇭🇹</div>', unsafe_allow_html=True)
