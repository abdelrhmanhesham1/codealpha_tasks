"""
AI Music Generator — LSTM-based MIDI composer.

Modes:
  demo      : quick algorithmic melody, no model needed
  train     : learn from your MIDI files
  generate  : compose new music using a trained model

Examples:
  python generate.py --mode demo
  python generate.py --mode train  --data midi_data/ --epochs 80
  python generate.py --mode generate --output my_song.mid --temperature 0.9
"""

import argparse
import os
import pickle
import random
import numpy as np

try:
    from music21 import converter, instrument, note, chord, stream
    MUSIC21_OK = True
except ImportError:
    MUSIC21_OK = False

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
    TF_OK = True
except ImportError:
    TF_OK = False


# ──────────────────────────────────────────────────────────────────────────────
# MIDI parsing
# ──────────────────────────────────────────────────────────────────────────────

def extract_notes(folder):
    all_notes = []
    for root, _, files in os.walk(folder):
        for fname in files:
            if not fname.lower().endswith((".mid", ".midi")):
                continue
            fpath = os.path.join(root, fname)
            try:
                midi   = converter.parse(fpath)
                parts  = instrument.partitionByInstrument(midi)
                source = parts.parts[0].recurse() if parts else midi.flatten().notes
                for el in source:
                    if isinstance(el, note.Note):
                        all_notes.append(str(el.pitch))
                    elif isinstance(el, chord.Chord):
                        all_notes.append(".".join(str(n) for n in el.normalOrder))
            except Exception as exc:
                print(f"  skipped {fname} ({exc})")
    return all_notes


def make_sequences(notes, seq_len=100):
    vocab        = sorted(set(notes))
    note_to_int  = {n: i for i, n in enumerate(vocab)}
    int_to_note  = {i: n for n, i in note_to_int.items()}
    n_vocab      = len(vocab)

    X_raw, y_raw = [], []
    for i in range(len(notes) - seq_len):
        X_raw.append([note_to_int[n] for n in notes[i: i + seq_len]])
        y_raw.append(note_to_int[notes[i + seq_len]])

    X = np.reshape(X_raw, (len(X_raw), seq_len, 1)) / float(n_vocab)
    y = tf.keras.utils.to_categorical(y_raw, num_classes=n_vocab)
    return X, y, note_to_int, int_to_note, n_vocab


# ──────────────────────────────────────────────────────────────────────────────
# Model
# ──────────────────────────────────────────────────────────────────────────────

def build_model(seq_len, n_vocab):
    model = Sequential([
        LSTM(512, input_shape=(seq_len, 1), return_sequences=True),
        BatchNormalization(),
        Dropout(0.3),
        LSTM(512, return_sequences=True),
        BatchNormalization(),
        Dropout(0.3),
        LSTM(256),
        BatchNormalization(),
        Dropout(0.3),
        Dense(256, activation="relu"),
        Dropout(0.3),
        Dense(n_vocab, activation="softmax"),
    ])
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])
    return model


# ──────────────────────────────────────────────────────────────────────────────
# Generation
# ──────────────────────────────────────────────────────────────────────────────

def generate_sequence(model, int_to_note, n_vocab, seq_len=100, length=500, temperature=1.0):
    # pick a random seed position within the vocab range
    start = random.randint(0, max(0, n_vocab - seq_len - 1))
    pattern = list(range(start, start + seq_len))
    output = []

    for _ in range(length):
        x = np.reshape(pattern, (1, len(pattern), 1)) / float(n_vocab)
        raw = model.predict(x, verbose=0)[0].astype("float64")

        # temperature scaling to control randomness
        raw = np.log(raw + 1e-8) / temperature
        probs = np.exp(raw) / np.sum(np.exp(raw))

        chosen = np.random.choice(len(probs), p=probs)
        output.append(int_to_note[chosen])
        pattern.append(chosen)
        pattern = pattern[1:]

    return output


def notes_to_midi(note_list, out_path="output.mid"):
    offset = 0
    elements = []

    for token in note_list:
        if "." in token or token.isdigit():
            ns = [note.Note(int(p)) for p in token.split(".")]
            for n in ns:
                n.storedInstrument = instrument.Piano()
            c = chord.Chord(ns)
            c.offset = offset
            elements.append(c)
        else:
            n = note.Note(token)
            n.offset = offset
            n.storedInstrument = instrument.Piano()
            elements.append(n)
        offset += 0.5

    s = stream.Stream(elements)
    s.write("midi", fp=out_path)
    print(f"Saved → {out_path}")


# ──────────────────────────────────────────────────────────────────────────────
# Demo (no training needed)
# ──────────────────────────────────────────────────────────────────────────────

def run_demo(out_path="demo.mid"):
    random.seed(42)
    c_major = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
    elements = []
    offset   = 0.0

    for _ in range(64):
        pitch  = random.choice(c_major)
        length = random.choice([0.5, 1.0])
        n = note.Note(pitch)
        n.offset       = offset
        n.quarterLength = length
        n.storedInstrument = instrument.Piano()
        elements.append(n)
        offset += length

    s = stream.Stream(elements)
    s.write("midi", fp=out_path)
    print(f"Demo saved → {out_path}")


# ──────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LSTM Music Generator")
    parser.add_argument("--mode",        choices=["train", "generate", "demo"], default="demo")
    parser.add_argument("--data",        default="midi_data")
    parser.add_argument("--epochs",      type=int,   default=100)
    parser.add_argument("--seq-len",     type=int,   default=100)
    parser.add_argument("--n-generate",  type=int,   default=500)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--output",      default="output.mid")
    parser.add_argument("--model-path",  default="music_model.h5")
    args = parser.parse_args()

    if not MUSIC21_OK:
        print("Install music21 first:  pip install music21")
        return

    if args.mode == "demo":
        print("Generating demo melody...")
        run_demo(args.output)
        return

    if not TF_OK:
        print("Install TensorFlow first:  pip install tensorflow")
        return

    if args.mode == "train":
        print(f"Reading MIDI files from: {args.data}")
        notes = extract_notes(args.data)
        if len(notes) < args.seq_len + 1:
            print(f"Only {len(notes)} notes found — need at least {args.seq_len + 1}.")
            return
        print(f"Notes: {len(notes)}  |  Vocab size: {len(set(notes))}")

        X, y, n2i, i2n, n_vocab = make_sequences(notes, args.seq_len)
        with open("note_mappings.pkl", "wb") as f:
            pickle.dump((n2i, i2n, n_vocab), f)

        model = build_model(args.seq_len, n_vocab)
        model.summary()
        model.fit(X, y, epochs=args.epochs, batch_size=64, callbacks=[
            ModelCheckpoint(args.model_path, save_best_only=True, monitor="loss"),
            EarlyStopping(patience=10, monitor="loss"),
        ])
        print(f"Model saved → {args.model_path}")

    elif args.mode == "generate":
        if not os.path.exists(args.model_path) or not os.path.exists("note_mappings.pkl"):
            print("No trained model found. Run --mode train first, or try --mode demo.")
            return
        model = load_model(args.model_path)
        with open("note_mappings.pkl", "rb") as f:
            n2i, i2n, n_vocab = pickle.load(f)
        print(f"Generating {args.n_generate} notes...")
        output = generate_sequence(model, i2n, n_vocab, args.seq_len, args.n_generate, args.temperature)
        notes_to_midi(output, args.output)


if __name__ == "__main__":
    main()
