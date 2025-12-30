import streamlit as st
from gtts import gTTS
import io
import speech_recognition as sr

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

st.title("Urdu Text-to-Speech & Speech-to-Text Converter")

# =======================
# Text-to-Speech (UNCHANGED)
# =======================
st.subheader("Text-to-Speech (Urdu)")

urdu_text = st.text_area("Enter Urdu text here:", height=150)

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if st.button("Generate MP3"):
    if urdu_text.strip():
        try:
            tts = gTTS(text=urdu_text, lang="ur")
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            st.session_state.audio_bytes = audio_io.getvalue()
            st.success("Audio generated successfully!")
        except Exception as e:
            st.error(str(e))
    else:
        st.warning("Please enter some Urdu text.")

if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
    st.download_button(
        "Download MP3",
        st.session_state.audio_bytes,
        "urdu_audio.mp3",
        "audio/mp3"
    )

if st.button("Clear Audio"):
    st.session_state.audio_bytes = None

# =======================
# Speech-to-Text (WAV ONLY)
# =======================
st.subheader("Speech-to-Text (Urdu)")

st.info(
    "📢 Upload WAV file only\n"
    "- Mono\n"
    "- 16-bit PCM\n"
    "- Max 60 seconds\n"
    "- Clear speech\n"
)

uploaded_file = st.file_uploader(
    "Upload WAV audio file",
    type=["wav"]
)

if uploaded_file:
    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile(uploaded_file) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language="ur-PK"
        )

        st.success("Urdu text generated from audio:")
        st.text_area("Urdu Text", value=text, height=150)

    except sr.UnknownValueError:
        st.error("Speech was unclear or could not be recognized.")
    except sr.RequestError:
        st.error("Google Speech API rejected the audio. Please check format.")
    except Exception as e:
        st.error(str(e))
