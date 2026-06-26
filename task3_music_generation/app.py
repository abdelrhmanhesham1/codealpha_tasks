import io
import os
import random
import tempfile
import streamlit as st

# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 1.5rem 3rem 1.5rem; max-width: 720px; }

.hero {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}
.hero h1 { font-size: 2.2rem; font-weight: 700; margin: 0 0 .4rem 0; }
.hero p  { opacity: .85; margin: 0; font-size: .95rem; }

.settings-header {
    font-size: .78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .07em; color: #9ca3af; margin-bottom: .5rem;
}

/* big generate button */
.stButton > button {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 1rem 2.5rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: .02em !important;
    box-shadow: 0 6px 24px rgba(168,85,247,.4) !important;
    transition: opacity .2s, transform .1s !important;
    width: 100%;
}
.stButton > button:hover  { opacity: .88 !important; transform: translateY(-2px) !important; }

.result-card {
    background: #fff;
    border: 1.5px solid #f3e8ff;
    border-radius: 18px;
    padding: 1.8rem 2.2rem;
    margin-top: 1.5rem;
    box-shadow: 0 8px 32px rgba(168,85,247,.12);
}
.result-card .label {
    font-size: .78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .07em; color: #a855f7; margin-bottom: 1rem;
}

.note-grid {
    display: flex; flex-wrap: wrap; gap: .4rem; margin: 1rem 0;
}
.note-pill {
    background: linear-gradient(135deg, #f3e8ff, #fce7f3);
    color: #7c3aed;
    border-radius: 8px;
    padding: .25rem .6rem;
    font-size: .8rem;
    font-weight: 600;
    font-family: monospace;
}

.stat-row {
    display: flex; gap: 1.5rem; margin-top: 1rem;
}
.stat-box {
    background: #faf5ff;
    border-radius: 12px;
    padding: .8rem 1.2rem;
    flex: 1;
    text-align: center;
}
.stat-box .num { font-size: 1.6rem; font-weight: 700; color: #7c3aed; }
.stat-box .lbl { font-size: .75rem; color: #9ca3af; margin-top: .2rem; }

hr { border: none; border-top: 1.5px solid #f3f4f6; margin: 1.5rem 0; }

audio { width: 100%; border-radius: 12px; margin-top: .5rem; }

.stSlider > div { padding: 0; }
</style>
""", unsafe_allow_html=True)

# ── hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🎵 AI Music Generator</h1>
  <p>Generate original MIDI melodies using algorithmic composition.<br>
     Tune the settings, hit Generate, and download your track.</p>
</div>
""", unsafe_allow_html=True)

# ── settings expander ──────────────────────────────────────────────────────────
with st.expander("⚙️  Settings", expanded=False):
    st.markdown('<div class="settings-header">Creativity</div>', unsafe_allow_html=True)
    temperature = st.slider(
        "Temperature",
        min_value=0.3, max_value=1.8, value=1.0, step=0.1,
        help="Lower = conservative & repetitive. Higher = experimental & unpredictable.",
        label_visibility="collapsed",
    )
    col_a, col_b = st.columns(2)
    with col_a:
        n_notes = st.slider("Notes to generate", 32, 256, 64, step=16)
    with col_b:
        seed_val = st.number_input("Random seed", min_value=0, max_value=9999, value=42,
                                   help="Same seed = same melody every time.")

    st.markdown('<div class="settings-header" style="margin-top:1rem">Scale</div>',
                unsafe_allow_html=True)
    scale_choice = st.selectbox(
        "Musical scale",
        ["C Major", "A Minor", "G Major", "D Minor", "Pentatonic"],
        label_visibility="collapsed",
    )

SCALES = {
    "C Major":    ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
    "A Minor":    ["A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4"],
    "G Major":    ["G3", "A3", "B3", "C4", "D4", "E4", "F#4", "G4"],
    "D Minor":    ["D4", "E4", "F4", "G4", "A4", "Bb4", "C5", "D5"],
    "Pentatonic": ["C4", "D4", "E4", "G4", "A4", "C5"],
}

# ── generate button ────────────────────────────────────────────────────────────
st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
generate = st.button("🎹  Generate Melody", use_container_width=True)

# ── generation logic ───────────────────────────────────────────────────────────
if generate:
    try:
        from music21 import note, stream, instrument, tempo

        scale  = SCALES[scale_choice]
        random.seed(int(seed_val))

        elements = []
        offset   = 0.0
        durations = [0.5, 0.5, 1.0, 1.0, 1.5, 2.0]
        generated_notes = []

        # build melody with simple contour logic
        prev_idx = random.randint(0, len(scale) - 1)
        for _ in range(int(n_notes)):
            # bias toward stepwise motion
            step = random.choices([-2, -1, 0, 1, 2], weights=[1, 3, 2, 3, 1])[0]
            idx  = max(0, min(len(scale) - 1, prev_idx + step))
            pitch  = scale[idx]
            length = random.choice(durations)

            # add occasional rests for breathing room
            if random.random() < 0.08:
                from music21 import note as n21
                r = n21.Rest()
                r.quarterLength = 0.5
                r.offset = offset
                elements.append(r)
                offset += 0.5

            n = note.Note(pitch)
            n.offset       = offset
            n.quarterLength = length
            n.storedInstrument = instrument.Piano()
            elements.append(n)
            generated_notes.append(pitch)
            offset += length
            prev_idx = idx

        s = stream.Stream(elements)

        # write MIDI to temp file, read back as bytes
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp:
            tmp_path = tmp.name
        s.write("midi", fp=tmp_path)
        with open(tmp_path, "rb") as f:
            midi_bytes = f.read()
        os.remove(tmp_path)

        st.session_state["midi_bytes"]  = midi_bytes
        st.session_state["notes_list"]  = generated_notes
        st.session_state["scale_used"]  = scale_choice
        st.session_state["n_generated"] = len(generated_notes)
        st.session_state["offset_total"] = round(offset, 1)

    except ImportError:
        st.error("music21 is not installed. Run: `pip install music21`")
    except Exception as e:
        st.error(f"Generation failed: {e}")

# ── result ─────────────────────────────────────────────────────────────────────
if "midi_bytes" in st.session_state:
    notes_list  = st.session_state["notes_list"]
    scale_used  = st.session_state["scale_used"]
    n_gen       = st.session_state["n_generated"]
    duration    = st.session_state["offset_total"]

    unique_pitches = list(dict.fromkeys(notes_list))

    note_pills = "".join(
        f'<span class="note-pill">{p}</span>'
        for p in unique_pitches
    )

    st.markdown(f"""
    <div class="result-card">
      <div class="label">✅ Melody Generated — {scale_used}</div>
      <div class="note-grid">{note_pills}</div>
      <div class="stat-row">
        <div class="stat-box">
          <div class="num">{n_gen}</div>
          <div class="lbl">Notes</div>
        </div>
        <div class="stat-box">
          <div class="num">{len(unique_pitches)}</div>
          <div class="lbl">Unique pitches</div>
        </div>
        <div class="stat-box">
          <div class="num">{duration}s</div>
          <div class="lbl">Est. duration</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    dl_col, _ = st.columns([2, 3])
    with dl_col:
        st.download_button(
            label="⬇️  Download MIDI",
            data=st.session_state["midi_bytes"],
            file_name=f"melody_{scale_used.replace(' ', '_').lower()}.mid",
            mime="audio/midi",
            use_container_width=True,
        )

    st.caption("Open the .mid file in GarageBand, MuseScore, or any DAW to hear and edit it.")

# ── footer ─────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("music21 · Streamlit — No GPU or training data required for demo mode")
