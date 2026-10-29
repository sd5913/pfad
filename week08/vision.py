"""Camera experiments using OpenCV and MediaPipe Tasks (Python 3.13)."""
import argparse
from contextlib import ExitStack
from pathlib import Path
import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODELS = Path(__file__).parent / "models"
TASKS = {
    "face": (vision.FaceDetector, vision.FaceDetectorOptions, "face.tflite"),
    "hand": (vision.HandLandmarker, vision.HandLandmarkerOptions, "hand.task"),
    "pose": (vision.PoseLandmarker, vision.PoseLandmarkerOptions, "pose.task"),
    "mesh": (vision.FaceLandmarker, vision.FaceLandmarkerOptions, "face_mesh.task"),
    "gesture": (vision.GestureRecognizer, vision.GestureRecognizerOptions, "gesture.task"),
    "segment": (vision.ImageSegmenter, vision.ImageSegmenterOptions, "segment.tflite"),
}
MODES = {
    "face": ["face"], "hand": ["hand"], "pose": ["pose"],
    "mesh": ["mesh"], "gesture": ["gesture"],
    "holistic": ["face", "hand", "pose"], "segment": ["segment"],
    "multi": ["face", "hand", "pose", "segment"],
    "expression": ["mesh"], "emotion": ["face"], "camera": [],
}


def make_task(name):
    cls, opts, filename = TASKS[name]
    model = MODELS / filename
    if not model.exists():
        raise FileNotFoundError(f"Missing {model}. See week08/README.md for model download instructions.")
    kwargs = {"base_options": python.BaseOptions(model_asset_path=str(model)),
              "running_mode": vision.RunningMode.VIDEO}
    if name == "mesh":
        kwargs["output_face_blendshapes"] = True
    if name in ("hand", "gesture"):
        kwargs["num_hands"] = 2
    return cls.create_from_options(opts(**kwargs))


def draw_points(frame, points, colour):
    height, width = frame.shape[:2]
    for point in points:
        cv2.circle(frame, (int(point.x * width), int(point.y * height)), 2, colour, -1)


def run(mode, camera):
    classifier = None
    if mode == "emotion":
        try:
            from emotiefflib.facial_analysis import EmotiEffLibRecognizer
        except ImportError as exc:
            raise RuntimeError("Emotion example needs --group emotion; see README") from exc
        classifier = EmotiEffLibRecognizer(engine="onnx", model_name="enet_b0_8_best_vgaf", device="cpu")
    with ExitStack() as stack:
        tasks = {name: stack.enter_context(make_task(name)) for name in MODES[mode]}
        cap = cv2.VideoCapture(camera)
        if not cap.isOpened():
            cap.release()
            raise RuntimeError(f"Cannot open camera {camera}; close other camera apps or try --camera 1")
        try:
            started = time.monotonic()
            last_timestamp = -1
            while True:
                ok, frame = cap.read()
                if not ok:
                    raise RuntimeError("Camera opened but returned no frame")
                frame = cv2.flip(frame, 1)
                image = mp.Image(image_format=mp.ImageFormat.SRGB,
                                 data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                timestamp = max(last_timestamp + 1, int((time.monotonic() - started) * 1000))
                last_timestamp = timestamp
                results = {name: (task.segment_for_video(image, timestamp) if name == "segment"
                                  else task.recognize_for_video(image, timestamp) if name == "gesture"
                                  else task.detect_for_video(image, timestamp))
                           for name, task in tasks.items()}
                if "segment" in results:
                    mask = results["segment"].confidence_masks[0].numpy_view()
                    mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                    background = np.full_like(frame, (100, 40, 20))
                    frame = np.where((mask > 0.5)[..., None], frame, background).astype(np.uint8)
                if "face" in results:
                    for detection in results["face"].detections:
                        box = detection.bounding_box
                        cv2.rectangle(frame, (box.origin_x, box.origin_y),
                                      (box.origin_x + box.width, box.origin_y + box.height), (0, 255, 255), 2)
                for name, attr, colour in [("hand", "hand_landmarks", (255, 120, 0)),
                                            ("pose", "pose_landmarks", (0, 255, 0)),
                                            ("mesh", "face_landmarks", (255, 255, 0)),
                                            ("gesture", "hand_landmarks", (255, 120, 0))]:
                    if name in results:
                        for points in getattr(results[name], attr):
                            draw_points(frame, points, colour)
                label = mode + " | q: quit"
                if classifier and results["face"].detections:
                    box = results["face"].detections[0].bounding_box
                    x1, y1 = max(0, box.origin_x), max(0, box.origin_y)
                    x2 = min(frame.shape[1], box.origin_x + box.width)
                    y2 = min(frame.shape[0], box.origin_y + box.height)
                    if x2 > x1 and y2 > y1:
                        crop = cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
                        labels, _ = classifier.predict_emotions(crop)
                        label += " | classifier: " + labels[0]
                if "gesture" in results and results["gesture"].gestures and results["gesture"].gestures[0]:
                    category = results["gesture"].gestures[0][0]
                    label += f" | {category.category_name} {category.score:.2f}"
                if mode == "expression" and results["mesh"].face_blendshapes:
                    scores = results["mesh"].face_blendshapes[0]
                    relevant = [x for x in scores if x.category_name in ("mouthSmileLeft", "mouthSmileRight")]
                    if relevant:
                        label += " | mouth smile: " + f"{sum(x.score for x in relevant)/len(relevant):.2f}"
                cv2.putText(frame, label, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.imshow("SD5913 vision", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=MODES)
    parser.add_argument("--camera", type=int, default=0)
    args = parser.parse_args()
    run(args.mode, args.camera)
