import json
import re
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words("english"))


def load_faqs(path="faqs.json"):
    with open(path, "r") as f:
        return json.load(f)


def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP_WORDS]
    return " ".join(tokens)


class FAQChatbot:
    def __init__(self, faqs):
        self.faqs = faqs
        self.questions = [faq["question"] for faq in faqs]
        self.answers = [faq["answer"] for faq in faqs]
        self.processed_qs = [preprocess(q) for q in self.questions]
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_qs)

    def get_response(self, user_input: str, threshold: float = 0.15):
        processed_input = preprocess(user_input)
        if not processed_input.strip():
            return "Please ask a valid question.", 0.0, None

        input_vec = self.vectorizer.transform([processed_input])
        similarities = cosine_similarity(input_vec, self.tfidf_matrix).flatten()
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        if best_score < threshold:
            return (
                "I'm not sure I have an answer for that. Try rephrasing your question or ask about AI/ML topics.",
                best_score,
                None,
            )

        return self.answers[best_idx], best_score, self.questions[best_idx]


# ── Streamlit UI ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="AI FAQ Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 AI FAQ Chatbot")
st.markdown("Ask me anything about **Artificial Intelligence & Machine Learning**!")

faqs = load_faqs()
bot = FAQChatbot(faqs)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your AI FAQ assistant. Ask me about AI, ML, deep learning, NLP, and more!"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a question about AI/ML...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    answer, score, matched_q = bot.get_response(user_input)

    response_md = answer
    if matched_q:
        response_md += f"\n\n*Matched FAQ: \"{matched_q}\" (confidence: {score:.0%})*"

    st.session_state.messages.append({"role": "assistant", "content": response_md})
    with st.chat_message("assistant"):
        st.markdown(response_md)

with st.sidebar:
    st.header("📚 Available Topics")
    for faq in faqs:
        st.markdown(f"- {faq['question']}")
    if st.button("Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared! Ask me a new question."}
        ]
        st.rerun()
