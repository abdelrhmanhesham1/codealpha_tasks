"""
Real-time object detection and tracking using YOLOv8 + ByteTrack.

Usage:
  python detect.py                          # webcam
  python detect.py --source video.mp4       # video file
  python detect.py --source img.jpg --no-track   # image, no tracking
  python detect.py --model yolov8m.pt --conf 0.5 --save
"""

import argparse
import cv2
import time
from collections import defaultdict

try:
    from ultralytics import YOLO
except ImportError:
    raise SystemExit("ultralytics not found — run:  pip install ultralytics")

# 20 visually distinct BGR colors, one per track ID slot
COLORS = [
    (56,  56,  255), (151, 157, 255), (31,  112, 255), (29,  178, 255),
    (49,  210, 207), (10,  249,  72), (23,  204, 146), (134, 219,  61),
    (52,  147,  26), (187, 212,   0), (168, 153,  44), (255, 194,   0),
    (147,  69,  52), (255, 115, 100), (236,  24,   0), (255,  56, 132),
    (133,   0,  82), (255,  56, 203), (200, 149, 255), (199,  55, 255),
]


def pick_color(track_id):
    return COLORS[int(track_id) % len(COLORS)]


def draw_label(frame, box, text, color):
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
    cv2.putText(frame, text, (x1 + 2, y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)


def run(source, model_name, conf_thresh, use_tracking, save_output, filter_classes):
    model = YOLO(model_name)
    cap   = cv2.VideoCapture(0 if source is None else source)

    if not cap.isOpened():
        print(f"Could not open: {source or 'webcam'}")
        return

    writer       = None
    fps_buf      = []
    trail_points = defaultdict(list)

    if save_output:
        w  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter("output_tracked.mp4", fourcc, 20, (w, h))

    print("Running — press Q to quit, S to screenshot.")

    while True:
        t0 = time.time()
        ok, frame = cap.read()
        if not ok:
            break

        if use_tracking:
            results = model.track(frame, persist=True, conf=conf_thresh,
                                  classes=filter_classes, verbose=False)
        else:
            results = model(frame, conf=conf_thresh, classes=filter_classes, verbose=False)

        counts = defaultdict(int)

        for box in (results[0].boxes or []):
            cls_name   = model.names[int(box.cls)]
            confidence = float(box.conf)
            coords     = box.xyxy[0].tolist()
            counts[cls_name] += 1

            if use_tracking and box.id is not None:
                tid   = int(box.id)
                color = pick_color(tid)
                label = f"{cls_name} #{tid}  {confidence:.0%}"
                draw_label(frame, coords, label, color)

                cx = int((coords[0] + coords[2]) / 2)
                cy = int((coords[1] + coords[3]) / 2)
                trail_points[tid].append((cx, cy))
                trail_points[tid] = trail_points[tid][-30:]

                for i in range(1, len(trail_points[tid])):
                    cv2.line(frame, trail_points[tid][i - 1], trail_points[tid][i], color, 2)
            else:
                draw_label(frame, coords, f"{cls_name}  {confidence:.0%}", (0, 200, 255))

        # FPS
        fps_buf.append(1.0 / max(time.time() - t0, 1e-6))
        if len(fps_buf) > 30:
            fps_buf.pop(0)
        cv2.putText(frame, f"FPS {sum(fps_buf)/len(fps_buf):.1f}",
                    (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 0), 2)

        y = 52
        for name, cnt in counts.items():
            cv2.putText(frame, f"{name}: {cnt}", (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 200, 255), 2)
            y += 24

        cv2.imshow("Detection & Tracking", frame)
        if writer:
            writer.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("s"):
            cv2.imwrite("screenshot.jpg", frame)
            print("Screenshot saved.")

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()


def main():
    p = argparse.ArgumentParser(description="YOLOv8 object detection & tracking")
    p.add_argument("--source",   default=None,        help="Video/image path (omit for webcam)")
    p.add_argument("--model",    default="yolov8n.pt", help="YOLO weights file")
    p.add_argument("--conf",     type=float, default=0.4, help="Confidence cutoff")
    p.add_argument("--no-track", action="store_true",  help="Skip ByteTrack tracking")
    p.add_argument("--save",     action="store_true",  help="Save output to output_tracked.mp4")
    p.add_argument("--classes",  nargs="+", type=int, default=None, help="COCO class IDs to keep")
    args = p.parse_args()

    run(
        source        = args.source,
        model_name    = args.model,
        conf_thresh   = args.conf,
        use_tracking  = not args.no_track,
        save_output   = args.save,
        filter_classes= args.classes,
    )


if __name__ == "__main__":
    main()
