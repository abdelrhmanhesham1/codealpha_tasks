import io
import streamlit as st
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
from gtts import gTTS

# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }

.block-container { padding: 0 2rem 2rem 2rem; max-width: 1100px; }

/* ── hero ── */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    color: white;
}
.hero h1 { font-size: 2.2rem; font-weight: 700; margin: 0 0 .4rem 0; }
.hero p  { font-size: 1rem; opacity: .85; margin: 0; }

/* ── lang row ── */
.lang-card {
    background: #f8f9ff;
    border: 1.5px solid #e5e7f0;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    height: 100%;
}
.lang-card label { font-weight: 600; color: #374151; font-size: .85rem; text-transform: uppercase; letter-spacing: .05em; }

/* ── text areas ── */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #e5e7f0 !important;
    font-size: 1rem !important;
    resize: vertical !important;
    padding: 1rem !important;
    transition: border-color .2s;
}
.stTextArea textarea:focus { border-color: #667eea !important; box-shadow: 0 0 0 3px rgba(102,126,234,.15) !important; }

/* ── translate button ── */
div[data-testid="stHorizontalBlock"] .stButton > button {
    width: 100%;
}
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .75rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: .02em !important;
    cursor: pointer !important;
    transition: opacity .2s, transform .1s !important;
    box-shadow: 0 4px 15px rgba(102,126,234,.4) !important;
}
.stButton > button:hover  { opacity: .9 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── result card ── */
.result-card {
    background: #fff;
    border: 1.5px solid #e5e7f0;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-top: 1.5rem;
    position: relative;
    box-shadow: 0 4px 24px rgba(0,0,0,.06);
}
.result-card .label {
    font-size: .78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .06em;
    color: #667eea;
    margin-bottom: .8rem;
}
.result-text {
    font-size: 1.15rem;
    color: #111827;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
}
.detected-badge {
    display: inline-block;
    background: #ede9fe;
    color: #5b21b6;
    font-size: .78rem;
    font-weight: 600;
    padding: .25rem .75rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.swap-btn button {
    background: white !important;
    color: #667eea !important;
    border: 1.5px solid #667eea !important;
    box-shadow: none !important;
    padding: .5rem 1rem !important;
    font-size: .9rem !important;
}

/* ── selectbox ── */
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #e5e7f0 !important;
}

/* ── divider ── */
hr { border: none; border-top: 1.5px solid #f0f0f5; margin: 1.5rem 0; }

/* ── audio ── */
audio { width: 100%; border-radius: 10px; margin-top: .5rem; }
</style>
""", unsafe_allow_html=True)

# ── data ───────────────────────────────────────────────────────────────────────
lang_map     = {v.title(): k for k, v in GOOGLE_LANGUAGES_TO_CODES.items()}
sorted_langs = sorted(lang_map.keys())

# ── hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🌐 Language Translator</h1>
  <p>Translate text between 100+ languages instantly. Powered by Google Translate.</p>
</div>
""", unsafe_allow_html=True)

# ── language selectors ─────────────────────────────────────────────────────────
col_src, col_mid, col_dst = st.columns([5, 1, 5])

with col_src:
    src_choice = st.selectbox("From", ["Auto Detect"] + sorted_langs, key="src_lang")

with col_mid:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    swap = st.button("⇄", help="Swap languages", key="swap_btn")

with col_dst:
    default_idx = sorted_langs.index("English") if "English" in sorted_langs else 0
    dst_choice  = st.selectbox("To", sorted_langs, index=default_idx, key="dst_lang")

# handle swap
if swap:
    if src_choice != "Auto Detect" and src_choice in sorted_langs:
        src_i   = sorted_langs.index(src_choice)
        dst_i   = sorted_langs.index(dst_choice)
        st.session_state["src_lang"] = sorted_langs[dst_i]
        st.session_state["dst_lang"] = sorted_langs[src_i]
        st.rerun()

# ── text inputs ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    source_text = st.text_area(
        "Source text",
        height=220,
        placeholder="Type or paste text here…",
        key="src_text",
        label_visibility="collapsed",
    )
    char_count = len(source_text)
    st.caption(f"{char_count} characters")

with col_right:
    result_placeholder = st.empty()
    if "translation" in st.session_state:
        result_placeholder.text_area(
            "Translation",
            value=st.session_state["translation"],
            height=220,
            key="result_display",
            label_visibility="collapsed",
        )
    else:
        result_placeholder.text_area(
            "Translation",
            value="",
            height=220,
            placeholder="Translation will appear here…",
            key="result_empty",
            label_visibility="collapsed",
            disabled=True,
        )

# ── translate button ───────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([3, 2, 3])
with btn_col:
    go = st.button("Translate →", use_container_width=True)

# ── translation logic ──────────────────────────────────────────────────────────
if go:
    if not source_text.strip():
        st.warning("Write something to translate first.")
    else:
        src_code  = "auto" if src_choice == "Auto Detect" else lang_map[src_choice]
        dest_code = lang_map[dst_choice]
        with st.spinner("Translating…"):
            try:
                translated = GoogleTranslator(source=src_code, target=dest_code).translate(
                    source_text.strip()
                )
                st.session_state["translation"]  = translated
                st.session_state["dest_lang_code"] = dest_code
                st.rerun()
            except Exception as e:
                st.error(f"Translation failed — {e}")

# ── result actions ─────────────────────────────────────────────────────────────
if "translation" in st.session_state:
    st.markdown("<hr>", unsafe_allow_html=True)
    res = st.session_state["translation"]

    st.markdown(f"""
    <div class="result-card">
      <div class="label">Translation</div>
      <div class="result-text">{res}</div>
    </div>
    """, unsafe_allow_html=True)

    act1, act2, act3 = st.columns([2, 2, 4])

    with act1:
        if st.button("📋 Copy", use_container_width=True):
            st.code(res, language=None)

    with act2:
        if st.button("🔊 Read Aloud", use_container_width=True):
            lang_code = st.session_state.get("dest_lang_code", "en")
            try:
                tts = gTTS(text=res, lang=lang_code, slow=False)
                buf = io.BytesIO()
                tts.write_to_fp(buf)
                buf.seek(0)
                st.audio(buf, format="audio/mp3")
            except Exception as e:
                st.warning(f"TTS not available for this language: {e}")

    with act3:
        st.caption(f"Translated to **{dst_choice}**")

# ── footer ─────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Google Translate API · deep-translator · gTTS · Streamlit")
