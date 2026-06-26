import io
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Object Detection",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 2rem 2rem 2rem; }

.hero {
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
    border-radius: 18px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
}
.hero h1 { font-size: 1.9rem; font-weight: 700; margin: 0 0 .3rem 0; }
.hero p  { opacity: .8; margin: 0; font-size: .9rem; }

.stats-row { display: flex; gap: 1rem; margin-bottom: 1.2rem; flex-wrap: wrap; }
.stat-card {
    background: #fff;
    border: 1.5px solid #e5e7eb;
    border-radius: 14px;
    padding: .9rem 1.3rem;
    flex: 1; min-width: 120px;
    box-shadow: 0 2px 10px rgba(0,0,0,.05);
}
.stat-card .num { font-size: 1.8rem; font-weight: 700; color: #2563eb; line-height: 1; }
.stat-card .lbl { font-size: .75rem; color: #6b7280; margin-top: .3rem; }

.det-row {
    display: flex; align-items: center; gap: .8rem;
    padding: .6rem 0; border-bottom: 1px solid #f3f4f6;
}
.det-row:last-child { border-bottom: none; }
.cls-badge {
    background: #eff6ff; color: #1d4ed8;
    border-radius: 8px; padding: .2rem .6rem;
    font-size: .8rem; font-weight: 600; min-width: 80px; text-align: center;
}
.conf-bar-wrap { flex: 1; background: #f3f4f6; border-radius: 999px; height: 8px; }
.conf-bar { background: linear-gradient(90deg, #2563eb, #60a5fa); border-radius: 999px; height: 8px; }
.conf-val { font-size: .8rem; font-weight: 600; color: #374151; min-width: 40px; text-align: right; }

.upload-zone {
    border: 2px dashed #93c5fd;
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    background: #eff6ff;
    color: #1d4ed8;
    font-weight: 500;
}

.stButton > button {
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(37,99,235,.35) !important;
}
.stButton > button:hover { opacity: .88 !important; }

hr { border: none; border-top: 1.5px solid #f3f4f6; margin: 1.2rem 0; }

.section-label {
    font-size: .78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .07em; color: #9ca3af; margin-bottom: .8rem;
}

.no-result {
    text-align: center; color: #9ca3af; padding: 3rem 1rem; font-size: .95rem;
}
</style>
""", unsafe_allow_html=True)

# ── sidebar controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Controls")

    model_size = st.selectbox(
        "Model size",
        ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"],
        index=0,
        help="nano=fastest, small=balanced, medium=accurate",
    )
    conf_thresh = st.slider("Confidence threshold", 0.1, 0.9, 0.4, 0.05)
    show_analytics = st.toggle("Show analytics panel", value=True)

    st.divider()
    st.markdown("### 📦 Model Info")
    model_info = {
        "yolov8n.pt": ("~6 MB", "Fastest", "37.3"),
        "yolov8s.pt": ("~22 MB", "Fast",    "44.9"),
        "yolov8m.pt": ("~50 MB", "Medium",  "50.2"),
    }
    sz, spd, mAP = model_info[model_size]
    st.caption(f"**Size:** {sz}  \n**Speed:** {spd}  \n**COCO mAP:** {mAP}")

    st.divider()
    st.markdown("### 🖥️ Real-time Detection")
    st.info("For live webcam/video tracking, run the CLI script:\n\n"
            "```\npython detect.py\n```\n"
            "or\n"
            "```\npython detect.py --source video.mp4\n```")

# ── load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model(name):
    from ultralytics import YOLO
    return YOLO(name)

# ── color palette ──────────────────────────────────────────────────────────────
PALETTE = [
    "#FF3838", "#FF9D97", "#FF701F", "#FFB21D", "#CFD231",
    "#48F90A", "#92CC17", "#3DDB86", "#1A9334", "#00D4BB",
    "#2C99A8", "#00C2FF", "#344593", "#6473FF", "#0018EC",
    "#8438FF", "#520085", "#CB38FF", "#FF95C8", "#FF37C7",
]

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def run_detection(image_pil, model, conf):
    img_array = np.array(image_pil.convert("RGB"))
    results   = model(img_array, conf=conf, verbose=False)
    result    = results[0]

    draw       = ImageDraw.Draw(image_pil)
    detections = []

    if result.boxes is not None:
        for i, box in enumerate(result.boxes):
            cls_id     = int(box.cls)
            cls_name   = model.names[cls_id]
            confidence = float(box.conf)
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            color = hex_to_rgb(PALETTE[cls_id % len(PALETTE)])
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

            label = f"{cls_name}  {confidence:.0%}"
            bbox  = draw.textbbox((x1, y1 - 20), label)
            draw.rectangle([bbox[0]-3, bbox[1]-2, bbox[2]+3, bbox[3]+2], fill=color)
            draw.text((x1, y1 - 20), label, fill="white")

            detections.append({
                "class": cls_name,
                "confidence": confidence,
                "box": (x1, y1, x2, y2),
                "color": PALETTE[cls_id % len(PALETTE)],
            })

    return image_pil, detections

# ── hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🎯 Object Detection & Tracking</h1>
  <p>Upload an image or take a webcam snapshot — YOLOv8 detects and labels every object instantly.</p>
</div>
""", unsafe_allow_html=True)

# ── source tabs ────────────────────────────────────────────────────────────────
tab_upload, tab_camera = st.tabs(["📁 Upload Image", "📷 Camera Snapshot"])

uploaded_image = None

with tab_upload:
    uploaded = st.file_uploader(
        "Drop an image here",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        label_visibility="collapsed",
    )
    if uploaded:
        uploaded_image = Image.open(uploaded)

with tab_camera:
    cam_shot = st.camera_input("Take a snapshot", label_visibility="collapsed")
    if cam_shot:
        uploaded_image = Image.open(cam_shot)

# ── detect ─────────────────────────────────────────────────────────────────────
if uploaded_image:
    model = load_model(model_size)

    with st.spinner(f"Running {model_size} detection…"):
        result_img, detections = run_detection(uploaded_image.copy(), model, conf_thresh)

    # ── layout ──────────────────────────────────────────────────────────────────
    if show_analytics and detections:
        img_col, stats_col = st.columns([3, 2])
    else:
        img_col = st.container()
        stats_col = None

    with img_col:
        st.image(result_img, use_container_width=True, caption=f"{len(detections)} objects detected")

        # download result
        buf = io.BytesIO()
        result_img.save(buf, format="JPEG", quality=95)
        buf.seek(0)
        st.download_button(
            "⬇️ Download Result",
            data=buf,
            file_name="detection_result.jpg",
            mime="image/jpeg",
        )

    if stats_col and detections:
        with stats_col:
            # summary stats
            class_counts = defaultdict(int)
            for d in detections:
                class_counts[d["class"]] += 1

            avg_conf = sum(d["confidence"] for d in detections) / len(detections)

            st.markdown(f"""
            <div class="stats-row">
              <div class="stat-card">
                <div class="num">{len(detections)}</div>
                <div class="lbl">Objects found</div>
              </div>
              <div class="stat-card">
                <div class="num">{len(class_counts)}</div>
                <div class="lbl">Unique classes</div>
              </div>
              <div class="stat-card">
                <div class="num">{avg_conf:.0%}</div>
                <div class="lbl">Avg confidence</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-label">Detections</div>', unsafe_allow_html=True)

            rows_html = ""
            for d in sorted(detections, key=lambda x: x["confidence"], reverse=True):
                bar_w = int(d["confidence"] * 100)
                rows_html += f"""
                <div class="det-row">
                  <span class="cls-badge" style="background:{d['color']}22;color:{d['color']}">{d['class']}</span>
                  <div class="conf-bar-wrap">
                    <div class="conf-bar" style="width:{bar_w}%;background:linear-gradient(90deg,{d['color']},{d['color']}99)"></div>
                  </div>
                  <span class="conf-val">{d['confidence']:.0%}</span>
                </div>
                """
            st.markdown(rows_html, unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">Class breakdown</div>', unsafe_allow_html=True)
            for cls, cnt in sorted(class_counts.items(), key=lambda x: -x[1]):
                st.markdown(f"**{cls}** — {cnt} {'object' if cnt == 1 else 'objects'}")

elif not uploaded_image:
    st.markdown("""
    <div class="no-result">
      📂 &nbsp; Upload an image or take a photo above to run detection
    </div>
    """, unsafe_allow_html=True)

# ── footer ─────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("YOLOv8 (Ultralytics) · 80 COCO classes · Streamlit UI — For real-time video use `detect.py`")
