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

# ... (all previous imports and code up to the WebRTC section) ...

# ------------------------------
# NEW FEATURE: SING OVER TRACK (Record voice + backing track, mix with ffmpeg)
# ------------------------------
st.markdown("---")
st.markdown(f"<h3 style='color: #764ba2;'>{get_text('sing_over_title')}</h3>", unsafe_allow_html=True)
st.markdown(get_text("sing_instruction"))

# STUN/TURN configuration for reliable WebRTC connection
RTC_CONFIGURATION = {
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}
    ]
}

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []
    def recv(self, frame: av.AudioFrame):
        self.audio_frames.append(frame.to_ndarray().copy())
        return frame

webrtc_ctx = webrtc_streamer(
    key="sing-over-track",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,   # Added STUN servers
    audio_receiver_size=1024,
    audio_processor_factory=AudioRecorder,
    media_stream_constraints={"audio": True, "video": False},
)

# ... (rest of the code unchanged)
