# 🌐 AI Language Translation Tool

> A real-time language translation web application powered by Google Translate API with text-to-speech support — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

The AI Language Translation Tool is an interactive web app that enables users to translate text between **100+ languages** instantly. Users can select source and target languages, type or paste any text, and receive an accurate translation in seconds. The app also features **auto language detection** and an optional **text-to-speech** feature to hear the translated output aloud.

This project demonstrates practical integration of a commercial Translation API into a clean, user-friendly Streamlit interface.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| Translation Engine | [Google Translate API](https://pypi.org/project/googletrans/) via `googletrans` |
| Text-to-Speech | `pyttsx3` (offline TTS engine) |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
User Input (Streamlit UI)
        │
        ▼
Language Selection (source / target)
        │
        ▼
googletrans Library ──► Google Translate API (HTTP)
        │
        ▼
Translation Result
        │
   ┌────┴────┐
   ▼         ▼
Display    pyttsx3
on Screen  (TTS Audio)
```

1. The user enters text and selects languages in the Streamlit UI.
2. The `googletrans` library sends the text to Google's translation endpoint.
3. The API returns the translated text and detected source language.
4. The result is displayed on-screen with a copy-friendly code block.
5. Optionally, `pyttsx3` reads the translated text aloud via system TTS.

---

## ✨ Features

- **100+ Language Support** — all languages available via Google Translate
- **Auto Language Detection** — automatically identifies the source language
- **Clean 2-column UI** — source & target language dropdowns side by side
- **Copy-Friendly Output** — result shown in a code block for easy copying
- **Text-to-Speech** — read the translated text aloud (English output)
- **Confidence Caption** — shows the detected source language name

---

## 🧪 Testing

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app.py
```

### Manual Test Cases

| Input | Source | Target | Expected |
|-------|--------|--------|----------|
| `Hello, how are you?` | Auto Detect | Arabic | `مرحبًا، كيف حالك؟` |
| `Bonjour le monde` | Auto Detect | English | `Hello world` |
| `مرحبا` | Auto Detect | Spanish | `Hola` |
| *(empty input)* | Any | Any | Warning: "Please enter some text" |

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/codealpha_tasks.git
cd codealpha_tasks/task1_language_translation

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
task1_language_translation/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🙏 Acknowledgements

- [googletrans](https://py-googletrans.readthedocs.io/) — unofficial Google Translate Python client
- [Streamlit](https://streamlit.io/) — rapid web app framework for Python
- [pyttsx3](https://pyttsx3.readthedocs.io/) — offline text-to-speech engine

---

*Built as part of the **CodeAlpha AI Internship** — Task 1*
