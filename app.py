import streamlit as st
from gtts import gTTS
import io
import json
import soundfile as sf
import numpy as np
from vosk import Model, KaldiRecognizer

# =======================
# Load VOSK Model
# =======================
@st.cache_resource
def load_model():
    return Model("vosk-model-small-ur-pk-0.4")

vosk_model = load_model()

# =======================
# Custom CSS (Urdu Font)
# =======================
css = """
<style>
@font-face {
    font-family: 'jameel-noori-nastaleeq';
    src: url('https://cdn.jsdelivr.net/gh/tariq-abdullah/urdu-web-font-CDN/JameelNooriNastaleeq.woff') format('woff');
}
textarea {
    font-family: 'jameel-noori-nastaleeq' !important;
    font-size: 24px !important;
    direction: rtl !important;
    text-align: right !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title("Urdu Text-to-Speech & Speech-to-Text (100% FREE)")

# =======================
# Text-to-Speech
# =======================
st.subheader("Text-to-Speech (Urdu)")

urdu_text = st.text_area("Enter Urdu text here:", height=150)

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if st.button("Generate MP3"):
    if urdu_text.strip():
        tts = gTTS(text=urdu_text, lang="ur")
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        st.session_state.audio_bytes = audio_io.getvalue()
        st.success("Audio generated successfully!")

if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
    st.download_button(
        "Download MP3",
        st.session_state.audio_bytes,
        "urdu_audio.mp3",
        "audio/mp3"
    )

# =======================
# Speech-to-Text (FREE)
# =======================
st.subheader("Speech-to-Text (Urdu – Offline)")

st.info("Upload WAV file (Mono, 16-bit PCM)")

uploaded_file = st.file_uploader(
    "Upload WAV audio file",
    type=["wav"]
)

if uploaded_file:
    try:
        data, samplerate = sf.read(uploaded_file)
        if data.ndim > 1:
            data = np.mean(data, axis=1)

        recognizer = KaldiRecognizer(vosk_model, samplerate)
        recognizer.AcceptWaveform(data.tobytes())
        result = json.loads(recognizer.Result())

        text = result.get("text", "")

        st.success("Urdu text generated from audio:")
        st.text_area("Urdu Text", value=text, height=150)

    except Exception as e:
        st.error(str(e))
