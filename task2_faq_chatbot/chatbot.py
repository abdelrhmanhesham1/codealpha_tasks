import json
import re
import os
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI FAQ Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 1.5rem 3rem 1.5rem; max-width: 780px; }

/* hero */
.hero {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    border-radius: 20px;
    padding: 2.4rem 2.8rem;
    margin-bottom: 2rem;
    color: white;
}
.hero h1 { font-size: 2rem; font-weight: 700; margin: 0 0 .4rem 0; }
.hero p  { opacity: .8; margin: 0; font-size: .95rem; }

/* search bar wrapper */
.search-wrap {
    position: relative;
    margin-bottom: 1.2rem;
}

/* chips */
.chips-row { display: flex; flex-wrap: wrap; gap: .5rem; margin-bottom: 1.8rem; }
.chip {
    background: #f0f4ff;
    color: #3b4fd8;
    border: 1.5px solid #c7d2fe;
    border-radius: 999px;
    padding: .3rem .9rem;
    font-size: .8rem;
    font-weight: 500;
    cursor: pointer;
    transition: background .15s;
    display: inline-block;
}
.chip:hover { background: #c7d2fe; }

/* answer bubble */
.bot-bubble {
    background: #fff;
    border: 1.5px solid #e5e7eb;
    border-radius: 0 18px 18px 18px;
    padding: 1.4rem 1.6rem;
    margin: .5rem 0 .8rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,.07);
    position: relative;
}
.bot-bubble::before {
    content: "🤖";
    position: absolute;
    top: -14px;
    left: 0;
    font-size: 1.2rem;
}
.bot-bubble .answer-text {
    font-size: 1rem;
    color: #111827;
    line-height: 1.75;
}
.bot-bubble .meta {
    display: flex;
    align-items: center;
    gap: .6rem;
    margin-top: .9rem;
    flex-wrap: wrap;
}
.conf-pill {
    font-size: .75rem;
    font-weight: 600;
    padding: .2rem .7rem;
    border-radius: 999px;
}
.conf-high   { background: #d1fae5; color: #065f46; }
.conf-medium { background: #fef3c7; color: #92400e; }
.conf-low    { background: #fee2e2; color: #991b1b; }
.matched-q {
    font-size: .78rem;
    color: #6b7280;
    font-style: italic;
}

/* fallback bubble */
.fallback-bubble {
    background: #fafafa;
    border: 1.5px dashed #d1d5db;
    border-radius: 0 18px 18px 18px;
    padding: 1.2rem 1.5rem;
    color: #6b7280;
    font-size: .95rem;
    margin: .5rem 0 .8rem 0;
}

/* section label */
.section-label {
    font-size: .78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #9ca3af;
    margin-bottom: .7rem;
}

/* input tweaks */
.stTextInput input {
    border-radius: 12px !important;
    border: 1.5px solid #e5e7eb !important;
    padding: .75rem 1rem !important;
    font-size: 1rem !important;
    transition: border-color .2s;
}
.stTextInput input:focus {
    border-color: #3b4fd8 !important;
    box-shadow: 0 0 0 3px rgba(59,79,216,.12) !important;
}

/* button */
.stButton > button {
    background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .65rem 1.8rem !important;
    font-weight: 600 !important;
    font-size: .95rem !important;
    box-shadow: 0 4px 15px rgba(15,32,39,.3) !important;
    transition: opacity .2s, transform .1s !important;
}
.stButton > button:hover  { opacity: .88 !important; transform: translateY(-1px) !important; }

hr { border: none; border-top: 1.5px solid #f3f4f6; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ── data / model ───────────────────────────────────────────────────────────────
STOPWORDS = set(stopwords.words("english"))
FAQ_PATH  = os.path.join(os.path.dirname(__file__), "faqs.json")

@st.cache_resource
def load_bot():
    with open(FAQ_PATH, encoding="utf-8") as f:
        faqs = json.load(f)

    def clean(t):
        t = t.lower()
        t = re.sub(r"[^a-z0-9\s]", "", t)
        return " ".join(w for w in t.split() if w not in STOPWORDS)

    questions = [x["question"] for x in faqs]
    answers   = [x["answer"]   for x in faqs]
    vec = TfidfVectorizer()
    mat = vec.fit_transform([clean(q) for q in questions])
    return faqs, questions, answers, vec, mat, clean

faqs, questions, answers, vec, mat, clean = load_bot()

def ask(query, cutoff=0.15):
    processed = clean(query)
    if not processed:
        return None, 0.0, None
    scores = cosine_similarity(vec.transform([processed]), mat).flatten()
    best   = int(np.argmax(scores))
    score  = float(scores[best])
    if score < cutoff:
        return None, score, None
    return answers[best], score, questions[best]

# ── hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🤖 AI/ML FAQ Assistant</h1>
  <p>Ask anything about artificial intelligence, machine learning, or deep learning.</p>
</div>
""", unsafe_allow_html=True)

# ── search bar ─────────────────────────────────────────────────────────────────
col_inp, col_btn = st.columns([5, 1])
with col_inp:
    query = st.text_input(
        "search",
        placeholder="e.g. What is deep learning?",
        label_visibility="collapsed",
        key="query_input",
    )
with col_btn:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    search = st.button("Ask →", use_container_width=True)

# ── topic chips ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Browse topics</div>', unsafe_allow_html=True)

chips_html = '<div class="chips-row">'
for faq in faqs:
    short = faq["question"].replace("What is ", "").replace("?", "").strip()
    chips_html += f'<span class="chip">{short}</span>'
chips_html += "</div>"
st.markdown(chips_html, unsafe_allow_html=True)

# ── query processing ───────────────────────────────────────────────────────────
active_query = query if (search or query) and query.strip() else None

if "last_query" not in st.session_state:
    st.session_state["last_query"]  = None
    st.session_state["last_answer"] = None
    st.session_state["last_score"]  = 0.0
    st.session_state["last_match"]  = None

if search and query.strip():
    answer, score, matched = ask(query)
    st.session_state["last_query"]  = query
    st.session_state["last_answer"] = answer
    st.session_state["last_score"]  = score
    st.session_state["last_match"]  = matched

# ── result ─────────────────────────────────────────────────────────────────────
if st.session_state["last_query"]:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">Result for: "{st.session_state["last_query"]}"</div>',
                unsafe_allow_html=True)

    answer = st.session_state["last_answer"]
    score  = st.session_state["last_score"]
    matched = st.session_state["last_match"]

    if answer:
        conf_class = "conf-high" if score >= 0.6 else "conf-medium" if score >= 0.3 else "conf-low"
        conf_label = f"{score:.0%} confidence"
        matched_str = f'Matched: <em>"{matched}"</em>' if matched else ""

        st.markdown(f"""
        <div class="bot-bubble">
          <div class="answer-text">{answer}</div>
          <div class="meta">
            <span class="conf-pill {conf_class}">{conf_label}</span>
            <span class="matched-q">{matched_str}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="fallback-bubble">
          🤔 &nbsp; I don't have a confident answer for that. Try rephrasing, or click one of the
          topic chips above to explore what I know.
        </div>
        """, unsafe_allow_html=True)

# ── sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📚 All Topics")
    for faq in faqs:
        st.markdown(f"**Q:** {faq['question']}")
        st.caption(faq['answer'][:80] + "…")
        st.divider()
