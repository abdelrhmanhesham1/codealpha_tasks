import json
import re
import os
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI/ML FAQ Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── DATA PATHS & NLP INITIALIZATION ───────────────────────────────────────────
FAQ_PATH = os.path.join(os.path.dirname(__file__), "faqs.json")

# Download NLTK resources and setup preprocessing pipeline
try:
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    
    lemmatizer = WordNetLemmatizer()
    STOPWORDS = set(stopwords.words("english"))
    has_nltk = True
except Exception:
    has_nltk = False

def clean(t):
    if not t:
        return ""
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    if has_nltk:
        try:
            tokens = word_tokenize(t)
            cleaned = [
                lemmatizer.lemmatize(w)
                for w in tokens
                if w not in STOPWORDS and len(w) > 1
            ]
            return " ".join(cleaned)
        except Exception:
            pass
    # Fallback/Basic cleaning
    words = t.split()
    stop_words = STOPWORDS if 'STOPWORDS' in globals() else set()
    return " ".join(w for w in words if w not in stop_words and len(w) > 1)

# ── LOAD BOT DATA ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_bot():
    with open(FAQ_PATH, encoding="utf-8") as f:
        faqs = json.load(f)

    questions = [x["question"] for x in faqs]
    answers   = [x["answer"]   for x in faqs]
    vec = TfidfVectorizer()
    mat = vec.fit_transform([clean(q) for q in questions])
    return faqs, questions, answers, vec, mat

faqs, questions, answers, vec, mat = load_bot()

# ── SIMILARITY MATCHING ───────────────────────────────────────────────────────
def ask(query, cutoff=0.18):
    processed = clean(query)
    if not processed:
        return None, 0.0, None
    scores = cosine_similarity(vec.transform([processed]), mat).flatten()
    best   = int(np.argmax(scores))
    score  = float(scores[best])
    if score < cutoff:
        return None, score, None
    return answers[best], score, questions[best]

# ── CSS CUSTOM STYLING (Premium Aesthetics) ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Typography & General */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 1.5rem 3rem 1.5rem; max-width: 800px; }

/* Hero Card */
.hero {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 20px;
    padding: 2.2rem;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.05);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 60%);
    pointer-events: none;
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    opacity: 0.85;
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
}

/* Section labels */
.section-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #64748b;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
}

/* Quick Topic Chips Styling */
div[data-testid="stHorizontalBlock"] button {
    background: #f1f5f9 !important;
    color: #4f46e5 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 20px !important;
    padding: 0.4rem 0.8rem !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
div[data-testid="stHorizontalBlock"] button:hover {
    background: #e0e7ff !important;
    color: #3730a3 !important;
    border-color: #818cf8 !important;
    transform: translateY(-1px);
}
div[data-testid="stHorizontalBlock"] button:active {
    transform: translateY(0);
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #f8fafc !important;
}
section[data-testid="stSidebar"] button {
    text-align: left !important;
    justify-content: flex-start !important;
    background-color: #ffffff !important;
    color: #334155 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 0.8rem !important;
    white-space: normal !important;
    word-break: break-word !important;
    height: auto !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] button:hover {
    background-color: #f1f5f9 !important;
    border-color: #cbd5e1 !important;
    color: #0f172a !important;
    transform: translateX(2px);
}

/* Bot Response styling additions */
.meta {
    display: flex;
    align-items: center;
    gap: .6rem;
    margin-top: 0.8rem;
    flex-wrap: wrap;
}
.conf-pill {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    letter-spacing: 0.02em;
    display: inline-block;
}
.conf-high   { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
.conf-medium { background-color: #fef9c3; color: #854d0e; border: 1px solid #fef08a; }
.conf-low    { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
.matched-q {
    font-size: 0.75rem;
    color: #64748b;
    font-style: italic;
}

/* Chat Input Styling */
div[data-testid="stChatInput"] {
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
}

/* Custom separator */
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── HERO & HEADER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🤖 AI & ML Chatbot Assistant</h1>
  <p>Learn about Artificial Intelligence, Machine Learning, Deep Learning, and NLP. Click on quick topics or ask any custom question below!</p>
</div>
""", unsafe_allow_html=True)

# ── QUICK CHIPS ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">⚡ Quick Topics</div>', unsafe_allow_html=True)

quick_topics = [
    ("Artificial Intelligence", "What is artificial intelligence?"),
    ("Machine Learning", "What is machine learning?"),
    ("Deep Learning", "What is deep learning?"),
    ("Neural Networks", "What is a neural network?"),
    ("Natural Language Processing", "What is natural language processing NLP?"),
    ("Computer Vision", "What is computer vision?"),
    ("How Chatbots Work", "How does a chatbot work?"),
    ("Cosine Similarity", "What is cosine similarity?")
]

cols = st.columns(4)
for idx, (label, question) in enumerate(quick_topics):
    col = cols[idx % 4]
    if col.button(label, key=f"chip_{idx}", use_container_width=True):
        st.session_state.pending_query = question
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ── SESSION STATE INITIALIZATION ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your interactive FAQ chatbot assistant. Ask me questions like: 'How do neural networks learn?' or 'Explain machine learning versus deep learning'. You can also select topics from the list or the sidebar catalog!",
            "score": 1.0,
            "matched": None,
            "is_fallback": False
        }
    ]

# ── RENDER CONVERSATION ────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
        st.write(msg["content"])
        
        # Metadata / badge rendering for bot answers
        if msg["role"] == "assistant" and msg.get("matched") is not None:
            score = msg["score"]
            conf_class = "conf-high" if score >= 0.6 else "conf-medium" if score >= 0.3 else "conf-low"
            conf_label = f"{score:.0%} Match"
            matched_str = f'Matched: "{msg["matched"]}"'
            
            st.markdown(f"""
            <div class="meta">
              <span class="conf-pill {conf_class}">{conf_label}</span>
              <span class="matched-q">{matched_str}</span>
            </div>
            """, unsafe_allow_html=True)
            
        elif msg["role"] == "assistant" and msg.get("is_fallback"):
            st.markdown("""
            <div class="meta">
              <span class="conf-pill conf-low">No confident match</span>
              <span class="matched-q">Similarity below cutoff</span>
            </div>
            """, unsafe_allow_html=True)

# ── INTERACTION LOGIC ─────────────────────────────────────────────────────────
# Get input from st.chat_input
chat_input_val = st.chat_input("Ask a question about AI/ML...")

# Determine the actual query (chat_input or a clicked button/chip)
user_query = None
if chat_input_val:
    user_query = chat_input_val
elif st.session_state.get("pending_query"):
    user_query = st.session_state.pending_query
    st.session_state.pending_query = None

if user_query:
    # Append user question
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Query chatbot
    answer, score, matched = ask(user_query)
    
    if answer:
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "score": score,
            "matched": matched,
            "is_fallback": False
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🤔 I couldn't find a confident answer for that question in my database. Try rephrasing, or check out the topics on the left or the catalog in the sidebar!",
            "score": score,
            "matched": None,
            "is_fallback": True
        })
    
    # Rerun to refresh the chat window and show updates immediately
    st.rerun()

# ── SIDEBAR FAQ CATALOG ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧹 Actions")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat history cleared. How can I help you today?",
                "score": 1.0,
                "matched": None,
                "is_fallback": False
            }
        ]
        st.rerun()
        
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📚 FAQ Catalog")
    st.markdown("Click any FAQ to ask it instantly:")
    
    for idx, faq in enumerate(faqs):
        if st.button(faq["question"], key=f"side_faq_{idx}", use_container_width=True):
            st.session_state.pending_query = faq["question"]
            st.rerun()
