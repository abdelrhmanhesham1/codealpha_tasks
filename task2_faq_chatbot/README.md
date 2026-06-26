# 🤖 AI FAQ Chatbot

> An NLP-powered FAQ chatbot that answers questions about Artificial Intelligence & Machine Learning using TF-IDF vectorization and cosine similarity — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

The AI FAQ Chatbot is an intelligent question-answering system designed to respond to user queries about AI/ML topics. Instead of relying on a pre-trained language model, it uses classical NLP techniques — **TF-IDF vectorization** and **cosine similarity** — to match user questions against a curated FAQ database and return the most relevant answer.

The chatbot features a fully interactive **chat-style UI** built with Streamlit, complete with a sidebar listing all available topics.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| NLP Preprocessing | [NLTK](https://www.nltk.org/) — tokenization, stopword removal |
| Vectorization | [scikit-learn](https://scikit-learn.org/) — `TfidfVectorizer` |
| Similarity Matching | `sklearn.metrics.pairwise.cosine_similarity` |
| Data | Custom `faqs.json` — 20 AI/ML Q&A pairs |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
User Question (Chat Input)
        │
        ▼
NLP Preprocessing (NLTK)
  - Lowercase
  - Remove punctuation
  - Remove stopwords
        │
        ▼
TF-IDF Vectorization
  (scikit-learn TfidfVectorizer)
        │
        ▼
Cosine Similarity
  against all FAQ vectors
        │
        ▼
Best Match Selection
  (threshold: 0.15)
        │
   ┌────┴────┐
   ▼         ▼
Return      "I don't know"
Answer      fallback message
```

**FAQ Knowledge Base (`faqs.json`):**
- 20 hand-curated AI/ML questions and answers
- Topics: neural networks, LLMs, CNNs, LSTMs, GANs, NLP, RL, TF-IDF, embeddings, etc.

---

## ✨ Features

- **Chat-style UI** — persistent conversation history with Streamlit's `st.chat_message`
- **NLP Preprocessing** — NLTK-based cleaning for more accurate matching
- **TF-IDF + Cosine Similarity** — proven IR technique, no GPU needed
- **Confidence Score** — each response shows match confidence (%)
- **Graceful Fallback** — low-confidence answers trigger a helpful fallback message
- **Topic Sidebar** — full list of available FAQ questions visible at all times
- **Clear Chat** — reset button to start fresh

---

## 🧪 Testing

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run chatbot.py
```

### Test Queries

| User Input | Expected Match Topic | Expected Confidence |
|-----------|---------------------|---------------------|
| `What is AI?` | "What is artificial intelligence?" | High (>80%) |
| `explain deep learning` | "What is deep learning?" | High |
| `how does cosine similarity work` | "What is cosine similarity?" | High |
| `tell me a joke` | — | Low → fallback message |
| `what is an LSTM network` | "What is an LSTM?" | High |

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/codealpha_tasks.git
cd codealpha_tasks/task2_faq_chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run chatbot.py
```

The app opens at `http://localhost:8501`.

---

## 📁 Project Structure

```
task2_faq_chatbot/
├── chatbot.py          # Main Streamlit app + FAQChatbot class
├── faqs.json           # 20 AI/ML FAQ entries (question + answer)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🔧 Extending the Chatbot

To add more FAQs, simply append entries to `faqs.json`:
```json
{
  "question": "Your new question here?",
  "answer": "The answer to your question."
}
```
No retraining needed — the TF-IDF matrix rebuilds on every app launch.

---

*Built as part of the **CodeAlpha AI Internship** — Task 2*
