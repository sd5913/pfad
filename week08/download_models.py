"""Download the official MediaPipe model bundles used by this week's examples."""
from pathlib import Path
from urllib.request import urlretrieve

MODELS = {
    "face.tflite": "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite",
    "hand.task": "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
    "pose.task": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
    "face_mesh.task": "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
    "gesture.task": "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
    "segment.tflite": "https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/1/selfie_segmenter.tflite",
}

if __name__ == "__main__":
    target = Path(__file__).parent / "models"
    target.mkdir(exist_ok=True)
    for name, url in MODELS.items():
        path = target / name
        if not path.exists():
            print(f"Downloading {name} ...", flush=True)
            urlretrieve(url, path.with_suffix(path.suffix + ".part"))
            path.with_suffix(path.suffix + ".part").replace(path)
        print(f"{name}: {path.stat().st_size:,} bytes")
