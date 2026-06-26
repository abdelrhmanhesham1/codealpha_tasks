"""
Real-time Object Detection & Tracking with YOLOv8 + ByteTrack/SORT.
Usage:
  Webcam:    python detect.py
  Video:     python detect.py --source path/to/video.mp4
  Image:     python detect.py --source path/to/image.jpg --no-track
"""
import argparse
import cv2
import time
from collections import defaultdict

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

# Color palette for tracking IDs
PALETTE = [
    (255, 56, 56), (255, 157, 151), (255, 112, 31), (255, 178, 29),
    (207, 210, 49), (72, 249, 10), (146, 204, 23), (61, 219, 134),
    (26, 147, 52), (0, 212, 187), (44, 153, 168), (0, 194, 255),
    (52, 69, 147), (100, 115, 255), (0, 24, 236), (132, 56, 255),
    (82, 0, 133), (203, 56, 255), (255, 149, 200), (255, 55, 199),
]


def get_color(track_id: int):
    return PALETTE[int(track_id) % len(PALETTE)]


def draw_box(frame, box, label: str, color, conf: float = None):
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    text = f"{label} {conf:.0%}" if conf else label
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(frame, (x1, y1 - h - 8), (x1 + w + 4, y1), color, -1)
    cv2.putText(frame, text, (x1 + 2, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def run(source, model_name="yolov8n.pt", conf=0.4, track=True, save=False, classes=None):
    if not YOLO_AVAILABLE:
        print("ultralytics not installed. Run: pip install ultralytics")
        return

    model = YOLO(model_name)
    cap = cv2.VideoCapture(0 if source is None else source)

    if not cap.isOpened():
        print(f"Cannot open source: {source}")
        return

    fps_history = []
    track_history = defaultdict(list)

    writer = None
    if save:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter("output_tracked.mp4", fourcc, 20, (w, h))

    print("Press 'q' to quit, 's' to save a screenshot.")

    while True:
        t0 = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        if track:
            results = model.track(frame, persist=True, conf=conf, classes=classes, verbose=False)
        else:
            results = model(frame, conf=conf, classes=classes, verbose=False)

        result = results[0]

        object_counts = defaultdict(int)

        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls)
                cls_name = model.names[cls_id]
                confidence = float(box.conf)
                xyxy = box.xyxy[0].tolist()
                object_counts[cls_name] += 1

                if track and box.id is not None:
                    tid = int(box.id)
                    color = get_color(tid)
                    draw_box(frame, xyxy, f"{cls_name} #{tid}", color, confidence)
                    cx, cy = int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)
                    track_history[tid].append((cx, cy))
                    track_history[tid] = track_history[tid][-30:]
                    pts = track_history[tid]
                    for i in range(1, len(pts)):
                        cv2.line(frame, pts[i - 1], pts[i], color, 2)
                else:
                    draw_box(frame, xyxy, cls_name, (0, 200, 255), confidence)

        elapsed = time.time() - t0
        fps = 1.0 / elapsed if elapsed > 0 else 0
        fps_history.append(fps)
        if len(fps_history) > 30:
            fps_history.pop(0)
        avg_fps = sum(fps_history) / len(fps_history)

        cv2.putText(frame, f"FPS: {avg_fps:.1f}", (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        y_offset = 55
        for cls_name, cnt in object_counts.items():
            cv2.putText(frame, f"{cls_name}: {cnt}", (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
            y_offset += 25

        cv2.imshow("YOLOv8 Object Detection & Tracking", frame)

        if writer:
            writer.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            cv2.imwrite("screenshot.jpg", frame)
            print("Screenshot saved.")

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="YOLOv8 Real-time Object Detection & Tracking")
    parser.add_argument("--source", default=None, help="Video path or image path (default: webcam)")
    parser.add_argument("--model", default="yolov8n.pt", help="YOLO model (yolov8n/s/m/l/x.pt)")
    parser.add_argument("--conf", type=float, default=0.4, help="Confidence threshold")
    parser.add_argument("--no-track", action="store_true", help="Disable object tracking")
    parser.add_argument("--save", action="store_true", help="Save output video")
    parser.add_argument("--classes", nargs="+", type=int, default=None, help="Filter class IDs")
    args = parser.parse_args()

    run(
        source=args.source,
        model_name=args.model,
        conf=args.conf,
        track=not args.no_track,
        save=args.save,
        classes=args.classes,
    )


if __name__ == "__main__":
    main()
