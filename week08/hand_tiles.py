"""Map one index fingertip to two visible tiles; camera is opt-in."""

import argparse
import math
import time
from pathlib import Path


# Normalized x positions: 0 is the left edge and 1 is the right edge.
SAMPLE_X = (0.20, 0.49, 0.50, 0.80, None)


def tile_for_x(x):
    if x is None or not isinstance(x, (int, float)):
        return None
    if not math.isfinite(x) or not 0 <= x <= 1:
        return None
    return "blue" if x < 0.5 else "red"


def tile_line(x):
    selected = tile_for_x(x)
    blue = "[ BLUE ]" if selected == "blue" else "  blue  "
    red = "[ RED ]" if selected == "red" else "  red  "
    return f"{blue}  {red}  ({selected or 'no input'})"


def sample_demo():
    print("Sample coordinates (not camera images and not MediaPipe output):")
    for x in SAMPLE_X:
        print(f"x={x!s:>4} -> {tile_line(x)}")


def camera_demo(model_path):
    if not model_path.is_file():
        raise ValueError(f"Model not found: {model_path}")
    try:
        import cv2
        import mediapipe as mp
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("Camera mode needs mediapipe, opencv-python and numpy") from exc

    base = mp.tasks.BaseOptions(model_asset_path=str(model_path))
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=base,
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
    )
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera.release()
        raise RuntimeError("Camera 0 unavailable; try the sample mode instead")

    try:
        with mp.tasks.vision.HandLandmarker.create_from_options(options) as tracker:
            start = time.monotonic()
            last_timestamp_ms = -1
            print("Camera active locally. Press q in the tile window to quit.")
            while True:
                ok, frame = camera.read()
                if not ok:
                    raise RuntimeError("Camera frame unavailable")
                # Mirror the camera, so moving your hand left selects the left tile.
                frame = cv2.flip(frame, 1)
                image = mp.Image(image_format=mp.ImageFormat.SRGB,
                                 data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                timestamp_ms = max(int((time.monotonic() - start) * 1000),
                                   last_timestamp_ms + 1)
                last_timestamp_ms = timestamp_ms
                result = tracker.detect_for_video(image, timestamp_ms)
                x = result.hand_landmarks[0][8].x if result.hand_landmarks else None
                selected = tile_for_x(x)

                # Draw only tiles, not camera frames or a recording.
                canvas = np.full((260, 600, 3), 245, dtype=np.uint8)
                for name, left, color in (
                    ("blue", 30, (190, 110, 35)),
                    ("red", 310, (60, 70, 210)),
                ):
                    cv2.rectangle(canvas, (left, 55), (left + 255, 195),
                                  color if name == selected else (205, 205, 205), -1)
                    cv2.putText(canvas, name.upper(), (left + 68, 135),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                cv2.putText(canvas, selected or "no input", (215, 235),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                cv2.imshow("Week 8 hand tiles (q to quit)", canvas)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        camera.release()
        cv2.destroyAllWindows()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera", action="store_true", help="opt in to local webcam")
    parser.add_argument("--model", type=Path, help="downloaded hand_landmarker.task")
    args = parser.parse_args(argv)
    if args.camera:
        if args.model is None:
            parser.error("--camera requires --model PATH; no automatic download")
        camera_demo(args.model)
    elif args.model is not None:
        parser.error("--model only applies with --camera")
    else:
        sample_demo()


if __name__ == "__main__":
    main()
