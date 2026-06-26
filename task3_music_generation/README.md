# 🎵 AI Music Generation with LSTM

> A deep learning system that learns musical patterns from MIDI files and generates original music using a stacked LSTM neural network — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

This project implements an AI-powered music composer that trains on MIDI files and generates new musical sequences. Using a **stacked LSTM (Long Short-Term Memory)** network, the model learns the temporal structure of music — notes, chords, rhythm, and transitions — then generates novel compositions that mimic the style of the training data.

The generated sequences are converted back to MIDI format using `music21` and can be played directly or exported as audio.

A **demo mode** is also included for instant MIDI generation without training, using algorithmic composition from a C major scale.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Deep Learning | [TensorFlow / Keras](https://www.tensorflow.org/) — LSTM model |
| Music Processing | [music21](https://web.mit.edu/music21/) — MIDI parsing & generation |
| Numerical Computing | [NumPy](https://numpy.org/) |
| Model Persistence | Python `pickle` — note-to-integer mappings |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
MIDI Files (training data)
        │
        ▼
music21 Parser
  → Extract Note / Chord sequences
        │
        ▼
Preprocessing
  → Build vocabulary (unique notes)
  → Integer encoding
  → Sliding window sequences (len=100)
  → Normalize: value / n_vocab
        │
        ▼
LSTM Model (Keras Sequential)
  ┌─────────────────────────────┐
  │  LSTM(512) + BatchNorm + Dropout(0.3)  │ → return_sequences=True
  │  LSTM(512) + BatchNorm + Dropout(0.3)  │ → return_sequences=True
  │  LSTM(256) + BatchNorm + Dropout(0.3)  │
  │  Dense(256, relu) + Dropout(0.3)       │
  │  Dense(n_vocab, softmax)               │
  └─────────────────────────────┘
        │
        ▼
Training (categorical_crossentropy, RMSprop)
        │
        ▼
Generation (temperature sampling)
        │
        ▼
music21 → MIDI output (.mid file)
```

---

## ✨ Features

- **Stacked LSTM Architecture** — 3-layer LSTM with BatchNorm and Dropout for stable training
- **Temperature Sampling** — controls creativity vs. accuracy of generated music
- **Chord Support** — handles both single notes and chords from MIDI data
- **Demo Mode** — generates algorithmic MIDI instantly without training data
- **Early Stopping & Checkpointing** — saves the best model during training
- **Flexible CLI** — train, generate, or demo via command-line flags
- **Music21 Integration** — full MIDI read/write pipeline

---

## 🧪 Testing

### Prerequisites
```bash
pip install -r requirements.txt
```

### Demo Mode (no training data needed)
```bash
python generate.py --mode demo --output my_melody.mid
```

### Train on Your MIDI Files
```bash
# Place .mid files in a folder called midi_data/
python generate.py --mode train --data midi_data/ --epochs 100
```

### Generate Music After Training
```bash
python generate.py --mode generate --output generated_music.mid --temperature 0.8
```

### Temperature Guide

| Temperature | Effect |
|-------------|--------|
| `0.5` | Conservative, close to training style |
| `1.0` | Balanced creativity |
| `1.5` | More experimental, random |

### Play the MIDI Output
```python
from music21 import converter
score = converter.parse("output.mid")
score.show("midi")  # opens in MuseScore or system MIDI player
```

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/codealpha_tasks.git
cd codealpha_tasks/task3_music_generation

# 2. Install dependencies
pip install -r requirements.txt

# 3. Quick demo (no data needed)
python generate.py --mode demo --output demo.mid
```

---

## 📁 Project Structure

```
task3_music_generation/
├── generate.py         # Full pipeline: parse → train → generate → MIDI
├── midi_data/          # (Place your .mid training files here)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 📦 Recommended MIDI Datasets

- [Classical Piano MIDI](http://www.piano-midi.de/) — classical compositions
- [MAESTRO Dataset](https://magenta.tensorflow.org/datasets/maestro) — high-quality piano recordings
- [Lakh MIDI Dataset](https://colinraffel.com/projects/lmd/) — diverse MIDI corpus

---

*Built as part of the **CodeAlpha AI Internship** — Task 3*
