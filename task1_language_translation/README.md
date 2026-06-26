# 🌐 AI Language Translation Tool

> A real-time language translation web app powered by Google Translate with slang expansion, auto-detection, and text-to-speech — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

The AI Language Translation Tool is an interactive web application that translates text between **100+ languages** instantly. What sets it apart is built-in **slang and abbreviation expansion** — you can type everyday internet language like `ngl`, `tbh`, `idk`, `gonna`, or `no cap` and the app automatically expands them into proper English before translating. This means you always get an accurate translation even when your input is informal or abbreviated.

Select a source and target language, type anything, and hit Translate. The app handles slang, auto-detects the source language, and can read the result aloud.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| Translation Engine | [deep-translator](https://pypi.org/project/deep-translator/) — Google Translate API |
| Text-to-Speech | [gTTS](https://pypi.org/project/gTTS/) + `st.audio()` — browser-native audio |
| Slang Expansion | Custom dictionary (80+ mappings) with regex word-boundary matching |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
User Input (Streamlit UI)
        │
        ▼
Slang / Abbreviation Expander
  (ngl → not gonna lie, tbh → to be honest, …)
        │
        ▼
Language Selection
  (source / target — full names, 100+ options)
        │
        ▼
deep-translator → Google Translate API
        │
        ▼
Translation Result
        │
   ┌────┴──────────────┐
   ▼                   ▼
Output Text Box     gTTS (optional)
(right column)      → st.audio() browser playback
        │
        ▼
Slang Summary Box
  (lists every substitution made)
```

1. User types text — slang/abbreviations are expanded before sending.
2. `deep-translator` sends the expanded text to Google Translate.
3. The result fills the right-column output box automatically.
4. A summary box shows exactly which words were substituted.
5. Optionally, gTTS reads the translated result aloud in the browser.

---

## ✨ Features

- 🌍 **100+ Language Support** — full language names in dropdowns (English, Arabic, Spanish…)
- 🔤 **Slang & Abbreviation Expansion** — 80+ mappings: `ngl`, `tbh`, `idk`, `gonna`, `wanna`, `omg`, `lol`, `brb`, `no cap`, `lowkey`, and more
- 📋 **Expansion Summary** — see exactly which abbreviations were substituted before translation
- 🔍 **Auto Language Detection** — no need to know your input language
- ⇄ **Swap Button** — flip source and target languages instantly
- 🔊 **Text-to-Speech** — hear the translated output read aloud in the browser
- 📋 **Copy Button** — copy the translation with one click
- 🎛 **Toggle Slang Expansion** — turn abbreviation expansion on or off per translation

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
python -m streamlit run app.py
```

The app opens at **`http://localhost:8501`** in your browser automatically.

---

## 🧪 Testing

| Input | Source | Target | Slang Expanded | Expected Output |
|-------|--------|--------|----------------|-----------------|
| `Hello, how are you?` | Auto | Arabic | — | `مرحبًا، كيف حالك؟` |
| `ngl this is fire` | Auto | Arabic | `ngl` → not gonna lie | Translation of "not gonna lie this is fire" |
| `tbh idk what to do rn` | Auto | Spanish | `tbh`, `idk`, `rn` → expanded | Translation of expanded text |
| `Bonjour le monde` | Auto | English | — | `Hello world` |
| `omg fr no cap` | Auto | French | `omg`, `fr`, `no cap` → expanded | Translation of "oh my god for real no lie, seriously" |
| *(empty input)* | Any | Any | — | Warning: "Write something to translate first" |

---

## 🚀 Future Improvements

- [ ] Add **DeepL API** as an alternative engine for higher accuracy on formal text
- [ ] Support **file upload** — translate `.txt` or `.docx` documents in bulk
- [ ] Add **translation history** with local session persistence
- [ ] Expand slang dictionary with **regional/cultural slang** (British, Australian, AAVE)
- [ ] Add **confidence score** for auto-detected language
- [ ] Support **bi-directional slang** — expand slang in non-English source languages too

---

## 📸 Screenshots

> *Run the app and add screenshots here to showcase the UI.*

| Main Interface | Slang Expansion Result |
|----------------|------------------------|
| *(screenshot)* | *(screenshot)* |

To add screenshots:
1. Run the app: `python -m streamlit run app.py`
2. Take a screenshot and save to `assets/screenshot1.png`
3. Reference it: `![UI](assets/screenshot1.png)`

---

## 🔗 Social Links

- 🐙 **GitHub Repo:** [codealpha_tasks](https://github.com/abdelrhmanhesham1/codealpha_tasks)
- 💼 **LinkedIn:** [Abdelrhman Hesham](https://www.linkedin.com/in/abdelrhman-hesham11/)
- 📧 **Email:** abdelrhman.hesham108@gmail.com

---

*Built with ❤️ as part of the **[CodeAlpha](https://codealpha.tech/) AI Internship** — Task 1*
