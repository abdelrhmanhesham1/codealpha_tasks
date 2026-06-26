import io
import re
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

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem 2rem; max-width: 1100px; }

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    color: white;
}
.hero h1 { font-size: 2.2rem; font-weight: 700; margin: 0 0 .4rem 0; }
.hero p  { font-size: 1rem; opacity: .85; margin: 0; }

.stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #e5e7f0 !important;
    font-size: 1rem !important;
    resize: vertical !important;
    padding: 1rem !important;
    transition: border-color .2s;
}
.stTextArea textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,.15) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .75rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(102,126,234,.4) !important;
    transition: opacity .2s, transform .1s !important;
}
.stButton > button:hover  { opacity: .9 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

.result-card {
    background: #fff;
    border: 1.5px solid #e5e7f0;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-top: 1.2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,.06);
}
.result-card .label {
    font-size: .78rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: .06em; color: #667eea; margin-bottom: .8rem;
}
.result-text {
    font-size: 1.15rem; color: #111827; line-height: 1.7;
    white-space: pre-wrap; word-break: break-word;
}

.slang-badge {
    display: inline-flex; align-items: center; gap: .4rem;
    background: #fef3c7; color: #92400e;
    border: 1px solid #fde68a;
    border-radius: 8px; padding: .3rem .8rem;
    font-size: .8rem; font-weight: 500;
    margin: .2rem .2rem 0 0;
}
.slang-arrow { color: #d97706; font-weight: 700; }

.expanded-box {
    background: #fffbeb;
    border: 1.5px solid #fde68a;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
.expanded-box .title {
    font-size: .78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .06em; color: #d97706; margin-bottom: .5rem;
}
.expanded-text { font-size: .95rem; color: #374151; line-height: 1.6; }

.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #e5e7f0 !important;
}

hr { border: none; border-top: 1.5px solid #f0f0f5; margin: 1.5rem 0; }
audio { width: 100%; border-radius: 10px; margin-top: .5rem; }
</style>
""", unsafe_allow_html=True)

# ── language map: full name → code  e.g. "English" → "en" ─────────────────────
# GOOGLE_LANGUAGES_TO_CODES = {"english": "en", "arabic": "ar", ...}
lang_map     = {k.title(): v for k, v in GOOGLE_LANGUAGES_TO_CODES.items()}
sorted_langs = sorted(lang_map.keys())

# ── slang / abbreviation dictionary ───────────────────────────────────────────
SLANG = {
    # internet abbreviations
    "ngl":   "not gonna lie",
    "tbh":   "to be honest",
    "imo":   "in my opinion",
    "imho":  "in my humble opinion",
    "idk":   "I don't know",
    "idc":   "I don't care",
    "irl":   "in real life",
    "fyi":   "for your information",
    "btw":   "by the way",
    "brb":   "be right back",
    "bbl":   "be back later",
    "afk":   "away from keyboard",
    "gtg":   "got to go",
    "omg":   "oh my god",
    "omfg":  "oh my god",
    "lol":   "laughing out loud",
    "lmao":  "laughing my ass off",
    "rofl":  "rolling on the floor laughing",
    "smh":   "shaking my head",
    "smdh":  "shaking my damn head",
    "nvm":   "never mind",
    "rn":    "right now",
    "atm":   "at the moment",
    "imo":   "in my opinion",
    "iirc":  "if I recall correctly",
    "afaik": "as far as I know",
    "tfw":   "that feeling when",
    "mfw":   "my face when",
    "imo":   "in my opinion",
    "fomo":  "fear of missing out",
    "goat":  "greatest of all time",
    "gg":    "good game",
    "gl":    "good luck",
    "gj":    "good job",
    "wp":    "well played",
    "np":    "no problem",
    "np":    "no problem",
    "ty":    "thank you",
    "thx":   "thanks",
    "thnx":  "thanks",
    "yw":    "you're welcome",
    "hmu":   "hit me up",
    "dm":    "direct message",
    "pm":    "private message",
    "imo":   "in my opinion",
    "tbf":   "to be fair",
    "fr":    "for real",
    "lowkey":"secretly or subtly",
    "highkey":"very much or obviously",
    "slay":  "doing something excellently",
    "lit":   "exciting or excellent",
    "fire":  "amazing or excellent",
    "bet":   "okay or agreed",
    "cap":   "a lie",
    "no cap": "no lie, seriously",
    "sus":   "suspicious",
    "bussin":"really good especially food",
    "vibe":  "a feeling or atmosphere",
    "periodt":"and that is final",
    "wya":   "where are you",
    "wyd":   "what are you doing",
    "wym":   "what do you mean",
    "istg":  "I swear to God",
    "ikyfl": "I know you're feeling",
    "ong":   "on God, I swear",
    "salty": "bitter or upset",
    "tea":   "gossip or drama",
    "spill the tea": "share the gossip",
    "stan":  "an obsessive fan",
    "w":     "a win",
    "l":     "a loss",
    # informal contractions
    "gonna": "going to",
    "wanna": "want to",
    "gotta": "got to",
    "kinda": "kind of",
    "sorta": "sort of",
    "lemme": "let me",
    "gimme": "give me",
    "dunno": "I don't know",
    "ain't": "is not",
    "y'all": "you all",
    "cuz":   "because",
    "coz":   "because",
    "cos":   "because",
    "tho":   "though",
    "thru":  "through",
    "prolly":"probably",
    "obv":   "obviously",
    "def":   "definitely",
    "defo":  "definitely",
    "rly":   "really",
    "rlly":  "really",
    "srsly": "seriously",
    "tbr":   "to be real",
    "imo":   "in my opinion",
    "qt":    "cutie",
    "bae":   "significant other or before anyone else",
    "bff":   "best friend forever",
    "fam":   "family or close friends",
    "squad": "close friend group",
    "sib":   "sibling",
    # text shortcuts
    "u":     "you",
    "ur":    "your",
    "r":     "are",
    "b4":    "before",
    "2":     "to",
    "4":     "for",
    "gr8":   "great",
    "h8":    "hate",
    "l8":    "late",
    "l8r":   "later",
    "m8":    "mate",
    "2day":  "today",
    "2moro": "tomorrow",
    "2nite": "tonight",
    "w/":    "with",
    "w/o":   "without",
    "w/e":   "whatever",
    "b/c":   "because",
    "imo":   "in my opinion",
}

def expand_slang(text: str):
    """Replace slang/abbreviations with full forms. Returns (expanded_text, replacements_list)."""
    replacements = []

    def replace_token(match):
        token = match.group(0)
        key   = token.lower()
        if key in SLANG:
            full = SLANG[key]
            # preserve capitalisation if original started with a capital
            if token[0].isupper():
                full = full[0].upper() + full[1:]
            replacements.append((token, full))
            return full
        return token

    # match word-boundary tokens (handles multi-word slang separately)
    for phrase, expansion in sorted(SLANG.items(), key=lambda x: -len(x[0])):
        pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
        new_text = pattern.sub(lambda m: _replace_with_case(m.group(0), expansion), text)
        if new_text != text:
            replacements.append((phrase, expansion))
            text = new_text

    return text, replacements

def _replace_with_case(original, replacement):
    if original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement

# ── hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🌐 Language Translator</h1>
  <p>Translate text between 100+ languages · slang & abbreviations auto-expanded · powered by Google Translate</p>
</div>
""", unsafe_allow_html=True)

# ── language selectors ─────────────────────────────────────────────────────────
col_src, col_mid, col_dst = st.columns([5, 1, 5])

with col_src:
    src_choice = st.selectbox("From", ["Auto Detect"] + sorted_langs, key="src_lang")

with col_mid:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    swap = st.button("⇄", help="Swap languages")

with col_dst:
    default_idx = sorted_langs.index("English") if "English" in sorted_langs else 0
    dst_choice  = st.selectbox("To", sorted_langs, index=default_idx, key="dst_lang")

if swap:
    if src_choice != "Auto Detect" and src_choice in sorted_langs:
        si = sorted_langs.index(src_choice)
        di = sorted_langs.index(dst_choice)
        st.session_state["src_lang"] = sorted_langs[di]
        st.session_state["dst_lang"] = sorted_langs[si]
        st.rerun()

# ── text inputs ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    source_text = st.text_area(
        "Source text",
        height=220,
        placeholder="Type or paste text here… slang like 'ngl', 'tbh', 'gonna' will be auto-expanded",
        label_visibility="collapsed",
        key="src_text",
    )
    st.caption(f"{len(source_text)} characters")

with col_right:
    if "translation" in st.session_state:
        st.text_area(
            "Translation",
            value=st.session_state["translation"],
            height=220,
            label_visibility="collapsed",
            key="result_display",
        )
    else:
        st.text_area(
            "Translation",
            value="",
            height=220,
            placeholder="Translation appears here…",
            label_visibility="collapsed",
            key="result_empty",
            disabled=True,
        )

# ── options row ────────────────────────────────────────────────────────────────
opt_left, opt_right = st.columns([3, 3])
with opt_left:
    expand_slang_toggle = st.toggle("🔤 Expand slang & abbreviations", value=True)

# ── translate button ───────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([3, 2, 3])
with btn_col:
    go = st.button("Translate →", use_container_width=True)

# ── translation logic ──────────────────────────────────────────────────────────
if go:
    if not source_text.strip():
        st.warning("Write something to translate first.")
    else:
        working_text = source_text.strip()
        found_replacements = []

        if expand_slang_toggle:
            working_text, found_replacements = expand_slang(working_text)

        src_code  = "auto" if src_choice == "Auto Detect" else lang_map[src_choice]
        dest_code = lang_map[dst_choice]

        with st.spinner("Translating…"):
            try:
                translated = GoogleTranslator(
                    source=src_code, target=dest_code
                ).translate(working_text)

                st.session_state["translation"]      = translated
                st.session_state["dest_lang_code"]   = dest_code
                st.session_state["expanded_text"]    = working_text if found_replacements else None
                st.session_state["replacements"]     = found_replacements
                st.rerun()
            except Exception as e:
                st.error(f"Translation failed — {e}")

# ── result actions + slang info (shown below the two text areas) ───────────────
if "translation" in st.session_state:
    res           = st.session_state["translation"]
    replacements  = st.session_state.get("replacements", [])
    expanded_text = st.session_state.get("expanded_text")

    # action buttons
    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    act1, act2, _ = st.columns([2, 2, 6])
    with act1:
        if st.button("📋 Copy", use_container_width=True):
            st.code(res, language=None)
    with act2:
        if st.button("🔊 Read aloud", use_container_width=True):
            lang_code = st.session_state.get("dest_lang_code", "en")
            try:
                tts = gTTS(text=res, lang=lang_code, slow=False)
                buf = io.BytesIO()
                tts.write_to_fp(buf)
                buf.seek(0)
                st.audio(buf, format="audio/mp3")
            except Exception as e:
                st.warning(f"TTS unavailable for this language: {e}")

    # slang expansion summary
    if replacements:
        seen = {}
        for orig, full in replacements:
            if orig.lower() not in seen:
                seen[orig.lower()] = (orig, full)

        badges = "".join(
            f'<span class="slang-badge"><b>{orig}</b>'
            f'<span class="slang-arrow">→</span>{full}</span>'
            for _, (orig, full) in seen.items()
        )
        st.markdown(f"""
        <div class="expanded-box">
          <div class="title">🔤 Slang expanded before translating</div>
          <div style="margin-bottom:.6rem">{badges}</div>
          <div class="expanded-text"><b>Expanded input:</b> {expanded_text}</div>
        </div>
        """, unsafe_allow_html=True)

# ── footer ─────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Google Translate · deep-translator · gTTS · Streamlit")
