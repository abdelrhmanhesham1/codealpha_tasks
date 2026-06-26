# 🎯 Real-Time Object Detection & Tracking

> A real-time computer vision system using YOLOv8 for object detection and ByteTrack for multi-object tracking — built for the CodeAlpha AI Internship.

---

## 📌 Project Overview

This project implements a production-grade **real-time object detection and tracking** pipeline using the state-of-the-art **YOLOv8** model and **ByteTrack** tracking algorithm. The system processes live webcam feeds or video files frame-by-frame, detects objects from 80 COCO classes, assigns persistent tracking IDs, and renders bounding boxes with smooth trail visualization.

Designed for real-world use cases including surveillance, traffic monitoring, crowd analysis, and robotics.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Object Detection | [YOLOv8](https://docs.ultralytics.com/) (Ultralytics) — `yolov8n/s/m/l/x.pt` |
| Object Tracking | ByteTrack (built into Ultralytics `model.track()`) |
| Video I/O | [OpenCV](https://opencv.org/) — `cv2` |
| Numerical Computing | [NumPy](https://numpy.org/) |
| Language | Python 3.9+ |

---

## 🏗 Architecture

```
Video Source (Webcam / File)
        │
        ▼
OpenCV Frame Capture (cv2.VideoCapture)
        │
        ▼
YOLOv8 Inference (Ultralytics)
  model.track(frame, persist=True)
        │
        ▼
Detection Results
  - Bounding boxes (xyxy)
  - Class names
  - Confidence scores
  - Track IDs (ByteTrack)
        │
        ▼
Visualization Layer
  - Color-coded bounding boxes (per track ID)
  - Label: class + track ID + confidence
  - Trail lines (last 30 center points)
  - FPS overlay
  - Per-class object count
        │
        ▼
Display (cv2.imshow) / Save (VideoWriter)
```

**ByteTrack** links detections across frames using IoU-based association, maintaining persistent IDs even through brief occlusions.

---

## ✨ Features

- **YOLOv8 Detection** — 80 COCO object classes, multiple model sizes (nano to x-large)
- **ByteTrack Multi-Object Tracking** — stable IDs across frames, handles occlusion
- **Motion Trails** — 30-frame trajectory line per tracked object
- **Per-ID Color Coding** — each track ID gets a unique color from a 20-color palette
- **FPS Counter** — rolling average FPS displayed on screen
- **Object Count Overlay** — live count per class displayed each frame
- **Screenshot** — press `s` to save the current frame as `screenshot.jpg`
- **Save Output** — `--save` flag records tracking video to `output_tracked.mp4`
- **Class Filtering** — `--classes` flag to detect only specific COCO class IDs
- **Configurable Confidence** — `--conf` threshold tuning
- **Model Size Selection** — `--model yolov8n/s/m/l/x.pt` for speed vs. accuracy tradeoff

---

## 🧪 Testing

### Prerequisites
```bash
pip install -r requirements.txt
```
> YOLOv8 weights (`yolov8n.pt`) download automatically on first run (~6MB).

### Run on Webcam
```bash
python detect.py
```

### Run on a Video File
```bash
python detect.py --source path/to/video.mp4
```

### Run on an Image (no tracking)
```bash
python detect.py --source path/to/image.jpg --no-track
```

### Advanced Options
```bash
# Use larger model for better accuracy
python detect.py --model yolov8m.pt --conf 0.5

# Detect only people (class 0) and cars (class 2)
python detect.py --classes 0 2

# Save tracking video output
python detect.py --source video.mp4 --save
```

### Keyboard Controls

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `s` | Save screenshot to `screenshot.jpg` |

### Model Size Reference

| Model | Size | Speed | mAP |
|-------|------|-------|-----|
| yolov8n | ~6MB | Fastest | 37.3 |
| yolov8s | ~22MB | Fast | 44.9 |
| yolov8m | ~50MB | Medium | 50.2 |
| yolov8l | ~87MB | Slower | 52.9 |
| yolov8x | ~137MB | Slowest | 53.9 |

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/codealpha_tasks.git
cd codealpha_tasks/task4_object_detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run on webcam
python detect.py
```

---

## 📁 Project Structure

```
task4_object_detection/
├── detect.py           # Main detection + tracking pipeline
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🔍 Supported Object Classes (COCO)

Person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, bench, bird, cat, dog, horse, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, sports ball, kite, baseball bat, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, TV, laptop, mouse, remote, keyboard, cell phone, microwave, oven, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush.

---

*Built as part of the **CodeAlpha AI Internship** — Task 4*
