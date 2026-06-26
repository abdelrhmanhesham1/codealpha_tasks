# 🎵 AI Music Generation with LSTM

> A deep learning system that learns musical patterns from MIDI files and generates original compositions using a stacked LSTM neural network — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

This project implements an AI-powered music composer that trains on MIDI files and generates new musical sequences. Using a **stacked LSTM (Long Short-Term Memory)** network, the model learns the temporal structure of music — notes, chords, rhythm, and transitions — then generates novel compositions that mimic the style of the training data.

Generated sequences are converted back to MIDI format using `music21` and can be played directly or exported as audio. A **demo mode** is included for instant MIDI generation without any training, making it easy to see the pipeline in action right away.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Deep Learning Framework | [TensorFlow / Keras](https://www.tensorflow.org/) |
| Model Architecture | Stacked LSTM with BatchNorm + Dropout |
| Music Processing | [music21](https://web.mit.edu/music21/) — MIDI parse & write |
| Numerical Computing | [NumPy](https://numpy.org/) |
| Model Persistence | Python `pickle` — note/chord vocabulary mappings |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
MIDI Files (training data)
        │
        ▼
music21 Parser
  └── Extract Note / Chord sequences
        │
        ▼
Preprocessing Pipeline
  ├── Build vocabulary (unique notes + chords)
  ├── Integer encoding
  ├── Sliding window sequences (length = 100)
  └── Normalize: value ÷ n_vocab
        │
        ▼
┌──────────────────────────────────────────┐
│           LSTM Model (Keras)             │
│  LSTM(512) → BatchNorm → Dropout(0.3)   │ return_sequences=True
│  LSTM(512) → BatchNorm → Dropout(0.3)   │ return_sequences=True
│  LSTM(256) → BatchNorm → Dropout(0.3)   │
│  Dense(256, relu) → Dropout(0.3)        │
│  Dense(n_vocab, softmax)                │
└──────────────────────────────────────────┘
        │
        ▼
Training
  ├── Loss: categorical_crossentropy
  ├── Optimizer: RMSprop
  ├── ModelCheckpoint (save best)
  └── EarlyStopping (patience=10)
        │
        ▼
Generation (temperature sampling)
  └── Seed sequence → predict next note → repeat N times
        │
        ▼
music21 → MIDI Output (.mid file)
```

---

## ✨ Features

- 🧠 **Stacked LSTM Architecture** — 3-layer LSTM with BatchNorm and Dropout for stable, generalizable training
- 🎲 **Temperature Sampling** — controls how creative vs. conservative the output is
- 🎹 **Chord Support** — handles both single notes and full chords from MIDI data
- ⚡ **Demo Mode** — generates an algorithmic MIDI melody instantly with no training needed
- 💾 **Model Checkpointing** — always saves the best-performing epoch
- ⏹ **Early Stopping** — halts training automatically when improvement plateaus
- 🖥 **Full CLI Interface** — `--mode train/generate/demo`, `--temperature`, `--epochs`, `--output`

---

## 📁 Project Structure

```
task3_music_generation/
│
├── generate.py             # Full pipeline: parse → train → generate → MIDI
├── midi_data/              # Place your .mid training files here (not included)
├── music_model.h5          # Saved model after training (auto-generated)
├── note_mappings.pkl       # Note vocabulary mappings (auto-generated)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ▶ How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/codealpha_tasks.git
cd codealpha_tasks/task3_music_generation
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

### 4a. Quick Demo — no training data needed
```bash
python generate.py --mode demo --output demo_melody.mid
```

### 4b. Train on your own MIDI files
```bash
# Place .mid files in a folder called midi_data/
python generate.py --mode train --data midi_data/ --epochs 100
```

### 4c. Generate music after training
```bash
python generate.py --mode generate --output my_music.mid --temperature 0.8
```

### 5. Play the MIDI output
```python
from music21 import converter
score = converter.parse("demo_melody.mid")
score.show("midi")   # opens in MuseScore, GarageBand, or your system MIDI player
```

---

## 🧪 Testing

| Mode | Command | Expected Output |
|------|---------|-----------------|
| Demo | `python generate.py --mode demo` | `output_demo.mid` — 64-note C major melody |
| Train | `python generate.py --mode train --data midi_data/` | Model saved to `music_model.h5` |
| Generate | `python generate.py --mode generate` | `output.mid` — AI-generated MIDI |

### Temperature Guide

| Value | Effect |
|-------|--------|
| `0.5` | Conservative — closely follows training style |
| `1.0` | Balanced — some creativity, still musical |
| `1.5` | Experimental — more random, less predictable |

### Recommended MIDI Datasets

- [Classical Piano MIDI](http://www.piano-midi.de/) — Bach, Beethoven, Chopin
- [MAESTRO Dataset](https://magenta.tensorflow.org/datasets/maestro) — high-quality piano recordings
- [Lakh MIDI Dataset](https://colinraffel.com/projects/lmd/) — diverse 176k MIDI corpus

---

## 🚀 Future Improvements

- [ ] Switch to **Transformer-based** architecture (Music Transformer) for longer coherence
- [ ] Add a **Streamlit UI** for training progress visualization and in-browser playback
- [ ] Support **multi-instrument** MIDI generation (not just piano)
- [ ] Implement **style transfer** — generate in the style of a specific composer
- [ ] Add **MIDI-to-MP3 conversion** via `FluidSynth` for direct audio output
- [ ] Train on **genre-specific datasets** (jazz, classical, lo-fi) with switchable presets

---

## 📸 Screenshots

> *Add screenshots or audio waveform images of your generated MIDI here.*

| Training Progress | Generated MIDI in MuseScore |
|-------------------|-----------------------------|
| *(screenshot)* | *(screenshot)* |

To add screenshots:
1. Run training and save loss curves
2. Open generated `.mid` in MuseScore and screenshot
3. Save to `assets/` and link here

---

## 🔗 Social Links

- 🐙 **GitHub Repo:** [codealpha_tasks](https://github.com/<your-username>/codealpha_tasks)
- 💼 **LinkedIn:** [Your LinkedIn Profile](https://linkedin.com/in/<your-linkedin>)
- 📧 **Email:** gatebuddy11@gmail.com

---

*Built with ❤️ as part of the **[CodeAlpha](https://codealpha.tech/) AI Internship** — Task 3*
