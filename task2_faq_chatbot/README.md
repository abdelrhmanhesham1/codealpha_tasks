# 🤖 AI FAQ Chatbot

> An NLP-powered FAQ chatbot that answers AI/ML questions using TF-IDF vectorization and cosine similarity — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

The AI FAQ Chatbot is an intelligent question-answering system that responds to user queries about **Artificial Intelligence & Machine Learning** topics. Instead of relying on a large language model, it uses classical NLP techniques — **TF-IDF vectorization** and **cosine similarity** — to match user questions against a curated knowledge base and return the most relevant answer.

The chatbot features a fully interactive **chat-style UI** built with Streamlit, making it feel natural and conversational right from the browser.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | [Streamlit](https://streamlit.io/) — chat UI |
| NLP Preprocessing | [NLTK](https://www.nltk.org/) — tokenization, stopword removal |
| Vectorization | [scikit-learn](https://scikit-learn.org/) — `TfidfVectorizer` |
| Similarity Matching | `sklearn.metrics.pairwise.cosine_similarity` |
| Knowledge Base | Custom `faqs.json` — 20 AI/ML Q&A pairs |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
User Question (Chat Input)
        │
        ▼
NLP Preprocessing (NLTK)
  ├── Lowercase text
  ├── Remove punctuation
  └── Remove stopwords
        │
        ▼
TF-IDF Vectorization
  (TfidfVectorizer fitted on FAQ questions)
        │
        ▼
Cosine Similarity
  (user vector vs. all FAQ vectors)
        │
        ▼
Best Match Selection
  ├── Score ≥ 0.15 → return matched answer
  └── Score < 0.15 → fallback message
        │
        ▼
Streamlit Chat UI (st.chat_message)
```

**Knowledge Base (`faqs.json`):**
- 20 hand-curated AI/ML Q&A pairs
- Topics: neural networks, LLMs, CNNs, LSTMs, GANs, NLP, RL, TF-IDF, cosine similarity, embeddings, and more

---

## ✨ Features

- 💬 **Chat-Style UI** — persistent message history with `st.chat_message`
- 🧹 **NLP Preprocessing** — NLTK cleaning for more accurate matching
- 📊 **TF-IDF + Cosine Similarity** — fast, lightweight, no GPU required
- 📈 **Confidence Score** — each response shows match confidence percentage
- 🛡 **Graceful Fallback** — low-confidence queries get a helpful redirect
- 📚 **Topic Sidebar** — full list of available FAQ questions always visible
- 🗑 **Clear Chat** — reset button to start a fresh conversation
- ⚡ **No Training Required** — TF-IDF matrix rebuilds instantly on each launch

---

## 📁 Project Structure

```
task2_faq_chatbot/
│
├── chatbot.py              # Main Streamlit app + FAQChatbot class
├── faqs.json               # 20 AI/ML FAQ entries (question + answer pairs)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ▶ How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/codealpha_tasks.git
cd codealpha_tasks/task2_faq_chatbot
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the chatbot
```bash
streamlit run chatbot.py
```

The app opens at **`http://localhost:8501`** in your browser.

---

## 🧪 Testing

| User Input | Matched Topic | Confidence |
|-----------|---------------|------------|
| `What is AI?` | "What is artificial intelligence?" | High (>80%) |
| `explain deep learning` | "What is deep learning?" | High |
| `how does cosine similarity work` | "What is cosine similarity?" | High |
| `what is an LSTM network` | "What is an LSTM?" | High |
| `tell me a joke` | — | Low → fallback message |

### Extending the Knowledge Base

To add more topics, append entries to `faqs.json` — no retraining needed:
```json
{
  "question": "Your new question here?",
  "answer": "The answer to your question."
}
```

---

## 🚀 Future Improvements

- [ ] Upgrade to **sentence-transformers** (BERT embeddings) for semantic understanding
- [ ] Add **intent classification** layer for multi-turn conversations
- [ ] Support **custom FAQ uploads** via the UI (drag & drop JSON/CSV)
- [ ] Integrate a **spell checker** to handle typos in user queries
- [ ] Add **feedback buttons** (thumbs up/down) to rate chatbot responses
- [ ] Export chat history as a downloadable `.txt` file

---

## 📸 Screenshots

> *Run the app and add screenshots here to showcase the UI.*

| Chat Interface | Sidebar Topics |
|----------------|----------------|
| *(screenshot)* | *(screenshot)* |

To add screenshots:
1. Run the app: `streamlit run chatbot.py`
2. Save screenshots to `assets/`
3. Reference them: `![Chat UI](assets/chat_ui.png)`

---

## 🔗 Social Links

- 🐙 **GitHub Repo:** [codealpha_tasks](https://github.com/<your-username>/codealpha_tasks)
- 💼 **LinkedIn:** [Your LinkedIn Profile](https://linkedin.com/in/<your-linkedin>)
- 📧 **Email:** gatebuddy11@gmail.com

---

*Built with ❤️ as part of the **[CodeAlpha](https://codealpha.tech/) AI Internship** — Task 2*
