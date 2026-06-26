# 🎯 Real-Time Object Detection & Tracking

> A production-grade computer vision system using YOLOv8 for object detection and ByteTrack for multi-object tracking — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

This project implements a real-time **object detection and tracking** pipeline that processes live webcam feeds or video files frame-by-frame. Using the state-of-the-art **YOLOv8** model, it detects objects from 80 COCO classes with high accuracy. **ByteTrack** then assigns persistent tracking IDs across frames, maintaining identity even through occlusion.

The system renders color-coded bounding boxes, motion trails, live FPS, and per-class object counts — making it suitable for real-world applications like surveillance, traffic analysis, crowd monitoring, and robotics.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Object Detection | [YOLOv8](https://docs.ultralytics.com/) — Ultralytics (`yolov8n/s/m/l/x.pt`) |
| Object Tracking | **ByteTrack** — built into `ultralytics model.track()` |
| Video I/O | [OpenCV](https://opencv.org/) — frame capture, rendering, saving |
| Numerical Computing | [NumPy](https://numpy.org/) |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
Video Source
  ├── Webcam (cv2.VideoCapture(0))
  └── Video / Image file
        │
        ▼
OpenCV Frame Capture
        │
        ▼
YOLOv8 Inference
  model.track(frame, persist=True)
        │
        ▼
Detection Results per Frame
  ├── Bounding boxes  (xyxy)
  ├── Class names     (80 COCO classes)
  ├── Confidence scores
  └── Track IDs       (ByteTrack)
        │
        ▼
Visualization Layer
  ├── Color-coded boxes       (unique color per track ID)
  ├── Label: class + ID + confidence
  ├── Motion trail lines      (last 30 center points)
  ├── FPS counter             (rolling 30-frame average)
  └── Per-class object count  (live overlay)
        │
   ┌────┴────┐
   ▼         ▼
cv2.imshow  VideoWriter
(display)   (save MP4)
```

**ByteTrack** links detections across frames using IoU-based association, maintaining persistent IDs even through brief occlusions or overlaps.

---

## ✨ Features

- ⚡ **YOLOv8 Detection** — 80 COCO object classes, 5 model size options (nano → x-large)
- 🔢 **ByteTrack Multi-Object Tracking** — stable IDs across frames, handles occlusion
- 🎨 **Per-ID Color Coding** — 20-color palette, unique color per tracked object
- 🛤 **Motion Trails** — 30-frame trajectory lines drawn per tracked object
- 📊 **Live Stats Overlay** — rolling-average FPS + per-class object count
- 📸 **Screenshot** — press `s` to save current frame as `screenshot.jpg`
- 💾 **Save Output** — `--save` records the tracking session to `output_tracked.mp4`
- 🎛 **Class Filtering** — `--classes` to detect only specific COCO class IDs
- 🔧 **Confidence Threshold** — `--conf` for precision vs. recall tuning
- 📦 **Auto Model Download** — YOLOv8 weights download automatically on first run

---

## 📁 Project Structure

```
task4_object_detection/
│
├── detect.py               # Full detection + tracking pipeline
├── requirements.txt        # Python dependencies
├── output_tracked.mp4      # Saved tracking video (auto-generated with --save)
├── screenshot.jpg          # Saved screenshot (press 's' during run)
└── README.md               # Project documentation
```

---

## ▶ How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/codealpha_tasks.git
cd codealpha_tasks/task4_object_detection
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
> YOLOv8 weights (`yolov8n.pt`, ~6MB) download automatically on first run.

### 4. Run on webcam
```bash
python detect.py
```

### 5. Run on a video file
```bash
python detect.py --source path/to/video.mp4
```

### 6. Run on an image (no tracking)
```bash
python detect.py --source path/to/image.jpg --no-track
```

### Advanced Options
```bash
# Larger model for higher accuracy
python detect.py --model yolov8m.pt --conf 0.5

# Detect only people (0) and cars (2)
python detect.py --classes 0 2

# Save the tracking output video
python detect.py --source video.mp4 --save
```

---

## 🧪 Testing

### Keyboard Controls

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `s` | Save screenshot to `screenshot.jpg` |

### Model Size Reference

| Model | File Size | Speed | mAP50-95 |
|-------|-----------|-------|----------|
| `yolov8n.pt` | ~6 MB | Fastest | 37.3 |
| `yolov8s.pt` | ~22 MB | Fast | 44.9 |
| `yolov8m.pt` | ~50 MB | Medium | 50.2 |
| `yolov8l.pt` | ~87 MB | Slower | 52.9 |
| `yolov8x.pt` | ~137 MB | Slowest | 53.9 |

### Common Test Scenarios

| Source | Expected Behavior |
|--------|------------------|
| Webcam | Real-time detection with FPS overlay |
| `--source video.mp4` | Frame-by-frame detection + tracking |
| `--classes 0` | Detects only people |
| `--conf 0.7` | Only high-confidence detections shown |
| `--no-track` | Bounding boxes without persistent IDs |

---

## 🚀 Future Improvements

- [ ] Add **Deep SORT** tracking for improved re-identification after long occlusion
- [ ] Build a **Streamlit web UI** for browser-based video upload and detection
- [ ] Implement **zone counting** — count objects entering/leaving a defined region
- [ ] Add **speed estimation** from tracked trajectories
- [ ] Export detections to **JSON / CSV** for downstream analysis
- [ ] Support **RTSP streams** for IP camera integration
- [ ] Add **custom YOLO model training** on domain-specific datasets

---

## 📸 Screenshots

> *Add screenshots or short GIFs of the detection in action here.*

| Webcam Detection | Video File Tracking |
|-----------------|---------------------|
| *(screenshot)* | *(screenshot)* |

To add screenshots:
1. Run `python detect.py` and press `s` to capture
2. Screenshots save as `screenshot.jpg` automatically
3. Move to `assets/` and link: `![Detection](assets/screenshot.jpg)`

---

## 🔍 Supported COCO Object Classes (80 classes)

`person · bicycle · car · motorcycle · airplane · bus · train · truck · boat · traffic light · fire hydrant · stop sign · parking meter · bench · bird · cat · dog · horse · sheep · cow · elephant · bear · zebra · giraffe · backpack · umbrella · handbag · tie · suitcase · frisbee · skis · snowboard · sports ball · kite · baseball bat · baseball glove · skateboard · surfboard · tennis racket · bottle · wine glass · cup · fork · knife · spoon · bowl · banana · apple · sandwich · orange · broccoli · carrot · hot dog · pizza · donut · cake · chair · couch · potted plant · bed · dining table · toilet · TV · laptop · mouse · remote · keyboard · cell phone · microwave · oven · toaster · sink · refrigerator · book · clock · vase · scissors · teddy bear · hair drier · toothbrush`

---

## 🔗 Social Links

- 🐙 **GitHub Repo:** [codealpha_tasks](https://github.com/<your-username>/codealpha_tasks)
- 💼 **LinkedIn:** [Your LinkedIn Profile](https://linkedin.com/in/<your-linkedin>)
- 📧 **Email:** gatebuddy11@gmail.com

---

*Built with ❤️ as part of the **[CodeAlpha](https://codealpha.tech/) AI Internship** — Task 4*
