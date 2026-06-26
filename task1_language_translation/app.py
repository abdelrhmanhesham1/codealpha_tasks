import streamlit as st
import threading
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
import pyttsx3

# name → code, e.g. "English" → "en"
lang_map     = {v.title(): k for k, v in GOOGLE_LANGUAGES_TO_CODES.items()}
sorted_langs = sorted(lang_map.keys())

st.set_page_config(page_title="Language Translator", page_icon="🌐", layout="centered")

st.title("🌐 Language Translation Tool")
st.write("Pick your languages, type some text, and hit Translate. That's it.")

col1, col2 = st.columns(2)
with col1:
    source_choice = st.selectbox("From", ["Auto Detect"] + sorted_langs)
with col2:
    default_idx = sorted_langs.index("English") if "English" in sorted_langs else 0
    target_choice = st.selectbox("To", sorted_langs, index=default_idx)

text_input = st.text_area("Your text:", height=160,
                           placeholder="Paste or type anything here...")

go = st.button("Translate", type="primary")

if go:
    if not text_input.strip():
        st.warning("Nothing to translate — write something first.")
    else:
        src_code  = "auto" if source_choice == "Auto Detect" else lang_map[source_choice]
        dest_code = lang_map[target_choice]

        with st.spinner("Working on it..."):
            try:
                result = GoogleTranslator(source=src_code, target=dest_code).translate(
                    text_input.strip()
                )
                st.session_state["result"] = result
            except Exception as err:
                st.error(f"Translation failed: {err}")

if "result" in st.session_state:
    st.divider()
    st.subheader("Translation")
    st.text_area("", value=st.session_state["result"], height=160, key="output_box")
    st.code(st.session_state["result"], language=None)
    st.caption("Select all in the box above to copy")

    if st.button("🔊 Read aloud"):
        def speak(txt):
            engine = pyttsx3.init()
            engine.say(txt)
            engine.runAndWait()
        threading.Thread(target=speak, args=(st.session_state["result"],)).start()
        st.info("Reading aloud...")

st.divider()
st.caption("Uses Google Translate under the hood · Streamlit UI")
