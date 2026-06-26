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

STOPWORDS = set(stopwords.words("english"))
FAQ_PATH = os.path.join(os.path.dirname(__file__), "faqs.json")


def load_faqs():
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    words = [w for w in text.split() if w not in STOPWORDS]
    return " ".join(words)


class FAQBot:
    def __init__(self, faqs):
        self.questions = [item["question"] for item in faqs]
        self.answers   = [item["answer"]   for item in faqs]

        cleaned = [clean(q) for q in self.questions]
        self.vec = TfidfVectorizer()
        self.matrix = self.vec.fit_transform(cleaned)

    def reply(self, user_text, cutoff=0.15):
        processed = clean(user_text)
        if not processed:
            return "Could you rephrase that?", 0.0, None

        scores = cosine_similarity(self.vec.transform([processed]), self.matrix).flatten()
        best   = int(np.argmax(scores))
        score  = float(scores[best])

        if score < cutoff:
            return (
                "Hmm, I don't have a good answer for that. "
                "Try asking about AI, ML, deep learning, NLP, or neural networks.",
                score,
                None,
            )
        return self.answers[best], score, self.questions[best]


# ── UI ─────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="AI FAQ Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 AI/ML FAQ Chatbot")
st.write("Got a question about AI or machine learning? Ask away.")

faqs = load_faqs()
bot  = FAQBot(faqs)

if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "assistant", "content": "Hey! Ask me anything about AI, ML, deep learning, or NLP."}
    ]

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_q = st.chat_input("Type your question...")

if user_q:
    st.session_state.history.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    answer, score, matched = bot.reply(user_q)

    reply_text = answer
    if matched:
        reply_text += f'\n\n<sub>Closest match: *"{matched}"* — {score:.0%} confidence</sub>'

    st.session_state.history.append({"role": "assistant", "content": reply_text})
    with st.chat_message("assistant"):
        st.markdown(reply_text, unsafe_allow_html=True)

with st.sidebar:
    st.header("Topics I know about")
    for item in faqs:
        st.markdown(f"- {item['question']}")
    st.divider()
    if st.button("Clear chat"):
        st.session_state.history = [
            {"role": "assistant", "content": "Fresh start! What do you want to know?"}
        ]
        st.rerun()
