"""
Music Generation with AI using LSTM.
Train: python generate.py --mode train
Generate: python generate.py --mode generate --output output.mid
"""
import argparse
import os
import pickle
import random
import numpy as np

try:
    from music21 import converter, instrument, note, chord, stream
    MUSIC21_AVAILABLE = True
except ImportError:
    MUSIC21_AVAILABLE = False

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


# ── Data helpers ──────────────────────────────────────────────────────────────

def parse_midi_folder(folder: str):
    """Extract note/chord sequences from all MIDI files in a folder."""
    notes = []
    for root, _, files in os.walk(folder):
        for fname in files:
            if not fname.endswith((".mid", ".midi")):
                continue
            path = os.path.join(root, fname)
            try:
                midi = converter.parse(path)
                parts = instrument.partitionByInstrument(midi)
                elements = parts.parts[0].recurse() if parts else midi.flat.notes
                for el in elements:
                    if isinstance(el, note.Note):
                        notes.append(str(el.pitch))
                    elif isinstance(el, chord.Chord):
                        notes.append(".".join(str(n) for n in el.normalOrder))
            except Exception as e:
                print(f"  Skipping {fname}: {e}")
    return notes


def build_sequences(notes, seq_len=100):
    vocab = sorted(set(notes))
    note_to_int = {n: i for i, n in enumerate(vocab)}
    int_to_note = {i: n for n, i in note_to_int.items()}

    X, y = [], []
    for i in range(len(notes) - seq_len):
        seq_in = notes[i: i + seq_len]
        seq_out = notes[i + seq_len]
        X.append([note_to_int[n] for n in seq_in])
        y.append(note_to_int[seq_out])

    n_vocab = len(vocab)
    X = np.reshape(X, (len(X), seq_len, 1)) / float(n_vocab)
    y = tf.keras.utils.to_categorical(y, num_classes=n_vocab)
    return X, y, note_to_int, int_to_note, n_vocab


# ── Model ─────────────────────────────────────────────────────────────────────

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


# ── Generation ────────────────────────────────────────────────────────────────

def generate_notes(model, int_to_note, note_to_int, n_vocab, seq_len=100, n_generate=500, temperature=1.0):
    start_idx = random.randint(0, n_vocab - seq_len - 1)
    pattern = list(range(start_idx, start_idx + seq_len))
    generated = []

    for _ in range(n_generate):
        x = np.reshape(pattern, (1, len(pattern), 1)) / float(n_vocab)
        prediction = model.predict(x, verbose=0)[0]
        # Temperature sampling
        prediction = np.log(prediction + 1e-8) / temperature
        prediction = np.exp(prediction) / np.sum(np.exp(prediction))
        idx = np.random.choice(len(prediction), p=prediction)
        generated.append(int_to_note[idx])
        pattern.append(idx)
        pattern = pattern[1:]

    return generated


def notes_to_midi(notes_list, output_path="output.mid"):
    offset = 0
    output_notes = []
    for pattern in notes_list:
        if "." in pattern or pattern.isdigit():
            # chord
            chord_notes = [note.Note(int(n)) for n in pattern.split(".")]
            for cn in chord_notes:
                cn.storedInstrument = instrument.Piano()
            new_chord = chord.Chord(chord_notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write("midi", fp=output_path)
    print(f"MIDI saved to {output_path}")


# ── Demo generation (no training data) ───────────────────────────────────────

def generate_demo_midi(output_path="output_demo.mid"):
    """Generate a simple algorithmic melody without a trained model."""
    scale = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
    output_notes = []
    offset = 0
    random.seed(42)
    for _ in range(64):
        pitch = random.choice(scale)
        new_note = note.Note(pitch)
        new_note.offset = offset
        new_note.quarterLength = random.choice([0.5, 1.0])
        new_note.storedInstrument = instrument.Piano()
        output_notes.append(new_note)
        offset += new_note.quarterLength
    midi_stream = stream.Stream(output_notes)
    midi_stream.write("midi", fp=output_path)
    print(f"Demo MIDI saved to {output_path}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AI Music Generator (LSTM)")
    parser.add_argument("--mode", choices=["train", "generate", "demo"], default="demo")
    parser.add_argument("--data", default="midi_data", help="Folder with MIDI training files")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--seq-len", type=int, default=100)
    parser.add_argument("--n-generate", type=int, default=500)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--output", default="output.mid")
    parser.add_argument("--model-path", default="music_model.h5")
    args = parser.parse_args()

    if not MUSIC21_AVAILABLE:
        print("music21 not installed. Run: pip install music21")
        return

    if args.mode == "demo":
        print("Generating demo MIDI (no training required)...")
        generate_demo_midi(args.output)
        return

    if not TF_AVAILABLE:
        print("TensorFlow not installed. Run: pip install tensorflow")
        return

    if args.mode == "train":
        print(f"Parsing MIDI files from '{args.data}'...")
        notes = parse_midi_folder(args.data)
        if len(notes) < args.seq_len + 1:
            print(f"Not enough notes found ({len(notes)}). Need at least {args.seq_len + 1}.")
            return
        print(f"Total notes: {len(notes)}, Vocabulary: {len(set(notes))}")

        X, y, note_to_int, int_to_note, n_vocab = build_sequences(notes, args.seq_len)
        with open("note_mappings.pkl", "wb") as f:
            pickle.dump((note_to_int, int_to_note, n_vocab), f)

        model = build_model(args.seq_len, n_vocab)
        model.summary()

        callbacks = [
            ModelCheckpoint(args.model_path, save_best_only=True, monitor="loss"),
            EarlyStopping(patience=10, monitor="loss"),
        ]
        model.fit(X, y, epochs=args.epochs, batch_size=64, callbacks=callbacks)
        print(f"Model saved to {args.model_path}")

    elif args.mode == "generate":
        if not os.path.exists(args.model_path) or not os.path.exists("note_mappings.pkl"):
            print("No trained model found. Run with --mode train first, or use --mode demo.")
            return
        model = load_model(args.model_path)
        with open("note_mappings.pkl", "rb") as f:
            note_to_int, int_to_note, n_vocab = pickle.load(f)
        print(f"Generating {args.n_generate} notes...")
        generated = generate_notes(model, int_to_note, note_to_int, n_vocab,
                                    args.seq_len, args.n_generate, args.temperature)
        notes_to_midi(generated, args.output)


if __name__ == "__main__":
    main()
