# 🌐 AI Language Translation Tool

> A real-time language translation web app powered by Google Translate API with auto-detection and text-to-speech — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

The AI Language Translation Tool is an interactive web application that enables users to translate text between **100+ languages** instantly. Users select source and target languages, type or paste any text, and receive an accurate translation in seconds.

The app also features **automatic language detection** (no need to know what language your input is in) and an optional **text-to-speech** button to hear the translated output read aloud — making it both powerful and accessible.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| Translation Engine | [googletrans 4.0](https://pypi.org/project/googletrans/) → Google Translate API |
| Text-to-Speech | [pyttsx3](https://pyttsx3.readthedocs.io/) — offline TTS engine |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
User Input (Streamlit UI)
        │
        ▼
Language Selection
  (source / target dropdowns)
        │
        ▼
googletrans Library
  └──► Google Translate API (HTTP)
        │
        ▼
Translation Result
        │
   ┌────┴────────┐
   ▼             ▼
Display       pyttsx3
on Screen     (TTS Audio Thread)
```

1. User enters text and selects languages in the Streamlit UI.
2. `googletrans` sends the text to Google's translation endpoint.
3. The API returns the translated text + detected source language.
4. Result is displayed on-screen with a copy-friendly code block.
5. Optionally, `pyttsx3` reads the translated text aloud in a background thread.

---

## ✨ Features

- 🌍 **100+ Language Support** — all languages available via Google Translate
- 🔍 **Auto Language Detection** — identifies the source language automatically
- 🎛 **Clean 2-Column UI** — source & target dropdowns side by side
- 📋 **Copy-Friendly Output** — result in a code block for easy copying
- 🔊 **Text-to-Speech** — read translated text aloud (English output)
- 🏷 **Detected Language Caption** — shows what language was recognized

---

## 📁 Project Structure

```
task1_language_translation/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ▶ How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/abdelrhmanhesham1/codealpha_tasks.git
cd codealpha_tasks/task1_language_translation
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

### 4. Launch the app
```bash
streamlit run app.py
```

The app opens at **`http://localhost:8501`** in your browser automatically.

---

## 🧪 Testing

| Input | Source | Target | Expected Output |
|-------|--------|--------|-----------------|
| `Hello, how are you?` | Auto Detect | Arabic | `مرحبًا، كيف حالك؟` |
| `Bonjour le monde` | Auto Detect | English | `Hello world` |
| `مرحبا` | Auto Detect | Spanish | `Hola` |
| *(empty input)* | Any | Any | Warning: "Please enter some text" |

---

## 🚀 Future Improvements

- [ ] Add **DeepL API** as an alternative translation engine for higher accuracy
- [ ] Support **file upload** (translate `.txt` or `.docx` documents)
- [ ] Add **translation history** with session persistence
- [ ] Implement **language swapping** (one-click swap source ↔ target)
- [ ] Multi-language TTS using `gTTS` for non-English output
- [ ] Add **character/word count** display in real time

---

## 📸 Screenshots

> *Run the app and add screenshots here to showcase the UI.*

| Main Interface | Translation Result |
|----------------|--------------------|
| *(screenshot)* | *(screenshot)* |

To add screenshots:
1. Run the app: `streamlit run app.py`
2. Take a screenshot and save to `assets/screenshot1.png`
3. Reference it: `![UI](assets/screenshot1.png)`

---

## 🔗 Social Links

- 🐙 **GitHub Repo:** [codealpha_tasks](https://github.com/abdelrhmanhesham1/codealpha_tasks)
- 💼 **LinkedIn:** [Abdelrhman Hesham](https://www.linkedin.com/in/abdelrhman-hesham11/)
- 📧 **Email:** abdelrhman.hesham108@gmail.com

---

*Built with ❤️ as part of the **[CodeAlpha](https://codealpha.tech/) AI Internship** — Task 1*
