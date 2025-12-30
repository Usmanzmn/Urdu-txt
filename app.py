# app.py
import streamlit as st
from gtts import gTTS
import io

st.title("Urdu Text-to-Speech Converter")

# Text input
urdu_text = st.text_area("Enter Urdu text here:", height=200)

if st.button("Generate MP3"):
    if urdu_text:
        try:
            # Generate speech
            tts = gTTS(text=urdu_text, lang='ur')
            
            # Save to bytes buffer
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            # Preview audio
            st.audio(audio_bytes, format="audio/mp3")
            
            # Download button
            st.download_button(
                label="Download MP3",
                data=audio_bytes,
                file_name="urdu_audio.mp3",
                mime="audio/mp3"
            )
            
            st.success("Audio generated successfully!")
        except Exception as e:
            st.error(f"Error generating audio: {str(e)}")
    else:
        st.warning("Please enter some text.")
