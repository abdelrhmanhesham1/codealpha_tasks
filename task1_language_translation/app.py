import streamlit as st
from googletrans import Translator, LANGUAGES
import pyttsx3
import threading

translator = Translator()

LANGUAGE_OPTIONS = {v.title(): k for k, v in LANGUAGES.items()}

st.set_page_config(page_title="AI Language Translator", page_icon="🌐", layout="centered")

st.title("🌐 AI Language Translation Tool")
st.markdown("Translate text between 100+ languages instantly using Google Translate API.")

col1, col2 = st.columns(2)
with col1:
    source_lang_name = st.selectbox("Source Language", ["Auto Detect"] + sorted(LANGUAGE_OPTIONS.keys()))
with col2:
    target_lang_name = st.selectbox("Target Language", sorted(LANGUAGE_OPTIONS.keys()), index=sorted(LANGUAGE_OPTIONS.keys()).index("English"))

input_text = st.text_area("Enter text to translate:", height=150, placeholder="Type or paste your text here...")

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    translate_clicked = st.button("Translate", type="primary", use_container_width=True)

if translate_clicked:
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            src = "auto" if source_lang_name == "Auto Detect" else LANGUAGE_OPTIONS[source_lang_name]
            dest = LANGUAGE_OPTIONS[target_lang_name]
            try:
                result = translator.translate(input_text, src=src, dest=dest)
                st.session_state["translated"] = result.text
                detected = LANGUAGES.get(result.src, result.src).title()
                st.session_state["detected_lang"] = detected
            except Exception as e:
                st.error(f"Translation failed: {e}")

if "translated" in st.session_state:
    st.markdown("---")
    if source_lang_name == "Auto Detect":
        st.caption(f"Detected source language: **{st.session_state['detected_lang']}**")

    st.subheader("Translated Text")
    st.text_area("Result:", value=st.session_state["translated"], height=150, key="result_area")

    col_copy, col_tts = st.columns(2)
    with col_copy:
        st.code(st.session_state["translated"], language=None)
        st.caption("Copy the text above")

    with col_tts:
        if st.button("🔊 Read Aloud (English output only)"):
            def speak(text):
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            t = threading.Thread(target=speak, args=(st.session_state["translated"],))
            t.start()
            st.info("Playing audio...")

st.markdown("---")
st.caption("Powered by Google Translate API · Built with Streamlit")
