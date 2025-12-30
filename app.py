import streamlit as st
from gtts import gTTS
import io
import speech_recognition as sr
from pydub import AudioSegment

# Custom CSS for Jameel Noori Nastaleeq font
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
# Existing TTS Feature
# =======================
st.subheader("Text-to-Speech (Urdu)")
urdu_text = st.text_area("Enter Urdu text here:", height=150)

if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None

if st.button("Generate MP3"):
    if urdu_text:
        try:
            tts = gTTS(text=urdu_text, lang='ur')
            audio_bytes_io = io.BytesIO()
            tts.write_to_fp(audio_bytes_io)
            st.session_state.audio_bytes = audio_bytes_io.getvalue()
            st.success("Audio generated successfully!")
        except Exception as e:
            st.error(f"Error generating audio: {str(e)}")
    else:
        st.warning("Please enter some text.")

if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
    st.download_button(
        label="Download MP3",
        data=st.session_state.audio_bytes,
        file_name="urdu_audio.mp3",
        mime="audio/mp3"
    )

if st.button("Clear Audio"):
    st.session_state.audio_bytes = None

# =======================
# New STT Feature
# =======================
st.subheader("Speech-to-Text (Urdu)")

uploaded_file = st.file_uploader("Upload an MP3/WAV file", type=["mp3", "wav"])

if uploaded_file:
    try:
        # Convert mp3 to wav if needed
        if uploaded_file.type == "audio/mpeg":
            audio = AudioSegment.from_mp3(uploaded_file)
            audio_io = io.BytesIO()
            audio.export(audio_io, format="wav")
            audio_io.seek(0)
        else:
            audio_io = uploaded_file

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_io) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ur-PK")  # Urdu
            st.success("Text generated from audio:")
            st.text_area("Urdu Text", value=text, height=150)
    except Exception as e:
        st.error(f"Error converting audio to text: {str(e)}")
