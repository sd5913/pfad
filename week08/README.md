# Week 8: cameras, landmarks and your group project

**Thursday 29 October 2026.** This two-hour tutorial follows the live lecture
and uses OpenCV and MediaPipe's current **Tasks** API. The nine exercises
follow the topics in the [2025 examples](https://github.com/sd5913/pfad/tree/2025/week08),
rewritten for MediaPipe 1.2.0. No instructor ClassPoint login is needed.

The lecture's Agile/Scrum concepts are quiz material. See the
[teamwork and GitHub tracking guide](teamwork.md) for revision and for making
your team's progress visible under the group project's 25% execution criterion.
The camera tutorial below still covers all nine vision examples.

## Before you start: 0–15 minutes

Work with a partner and ask before pointing a camera at anyone. These examples
process frames locally; do not record or upload anyone's image. You need a
laptop with a camera, a graphical desktop, internet for first-time setup, and
[uv](https://docs.astral.sh/uv/getting-started/installation/). Windows x64/ARM,
macOS Apple Silicon, and Linux x64/ARM have MediaPipe 1.2.0 wheels. Intel Macs
are not supported by that release; pair with someone on a supported machine.

From the **PFAD repository root**, enter the Week 8 folder and run:

```bash
cd week08
uv run python download_models.py
uv run python vision.py camera
```

`uv` finds this folder's project, uses its lockfile, and obtains Python 3.13
and the dependencies in the separate `week08/.venv`; it does not replace
PFAD's root environment. The download command saves Google's model files into
ignored `week08/models/`. The camera command opens a mirrored OpenCV preview.
Focus the window and press **q** to quit.
If camera 0 is unavailable, add `--camera 1` to a `vision.py` command, or
`--camera-index 1` to the hand-to-tile camera command. Grant camera access in
your OS settings; close Zoom or other camera apps. On a remote/headless machine,
use a partner's laptop with a display. Never commit models or frames.

Open [vision.py](vision.py). `cv2.VideoCapture` gets frames, OpenCV converts BGR
to RGB, a MediaPipe Task processes an `mp.Image`, and our code draws output.
`VIDEO` mode takes an increasing timestamp. The six model tasks run locally.

Keep your terminal in `week08` for every command below. First predict, then run,
observe and try the change. Press **q** before starting the next example. In a
terminal, **Ctrl+C** is a fallback if a window fails. If an example is slow,
close other apps, improve lighting and try a single model first. No detection
is a valid result: it should not crash your interaction.

## 1. Face detection: 15–23 minutes

```bash
uv run python vision.py face
```

Expect a yellow box around a detected face. Move farther away or partly cover
your face: when does the box disappear? Find `bounding_box` in the code. Change
the box colour in `cv2.rectangle`, run it, and restore it. A face box is a
location estimate; it does not identify a person.

## 2. Hand landmarks: 23–32 minutes

```bash
uv run python vision.py hand
```

Expect points on up to two hands. Look for index fingertip **landmark 8**. Move
one hand out of view, then rotate it and cover fingers; notice missed points.
Change the dot radius in `draw_points` and predict its effect. In the lecture's
[hand-to-tile example](hand_tiles.py), x below 0.5 selects blue, x at or above
0.5 selects red, and no hand selects neither:

```bash
uv run python hand_tiles.py
uv run python hand_tiles.py --camera --model models/hand.task
```

The first command uses sample coordinates and no camera. The second uses the
camera. Mirror direction and camera framing affect the mapping.

## 3. Pose landmarks: 32–40 minutes

```bash
uv run python vision.py pose
```

Expect green body points. Step back so your body is visible, then cover an arm.
Find `pose_landmarks`. Which points move when you bend an elbow? The 2025
[pose example](https://github.com/sd5913/pfad/blob/2025/week08/3_pose_estimation.py)
calculates an arm angle; predict what would happen to that angle if the elbow
straightens. A point behind your body may be inaccurate.

## 4. Face mesh: 40–50 minutes

```bash
uv run python vision.py mesh
```

Expect many cyan face points. Move your head and compare the points around the
mouth and eyes. Change the dot radius and observe whether the detail becomes
clearer. Turn sideways or remove your face from view: is the output stable?
These are geometry estimates, not an identity check.

## 5. Gesture recognition: 50–60 minutes

```bash
uv run python vision.py gesture
```

Expect hand points and a trained gesture label with a score when a hand is
recognized. Try an open palm, fist, and a rotated hand. Predict which gestures
will still work; do not treat a score as a person's intention. This Tasks
Gesture Recognizer uses a trained classifier. Contrast the 2025
[handwritten coordinate rules](https://github.com/sd5913/pfad/blob/2025/week08/5_gesture_recognition.py):
find one comparison and discuss how hand orientation might break it.

**Break: 60–70 minutes.** Press q and release the camera.

## 6. Combined detection: 70–80 minutes

```bash
uv run python vision.py holistic
```

Expect a face box plus hand and pose points on the same frame. This version
combines separate Tasks; it is not a claim that the old Holistic solution is
still the same API. Cover one hand and see which output remains. In `MODES`,
remove `"face"` from `holistic`, predict what disappears, run, and restore it.

## 7. Segmentation: 80–90 minutes

```bash
uv run python vision.py segment
```

Expect your foreground over a coloured background. Unlike landmarks, a mask
estimates pixels belonging to a person. Move hair or hands near the edge. Change
`mask > 0.5` to `mask > 0.7`, predict the edge change, run, and restore it.
Segmentation can miss transparent objects and fine details.

## 8. Multiple detectors: 90–100 minutes

```bash
uv run python vision.py multi
```

Expect segmentation, a face box, hands and pose together. Compare the speed
with `hand` alone. Remove one task from `MODES["multi"]` and compare; restore
it afterwards. Running many models has a cost; a slow laptop may be better
served by choosing just one input.

## 9. Expression classifier: 100–110 minutes

```bash
uv run --group emotion python vision.py emotion
```

This installs the additional EmotiEffLib/ONNX dependencies and downloads its
model on first use. MediaPipe finds a face; a **separate** classifier displays
one label from its trained categories. Try different expressions and lighting;
compare labels without asking anyone to disclose feelings. The output is a
model prediction from an image, **not evidence of someone's inner feelings**,
identity, truthfulness, or wellbeing. The model can be wrong and performance
can vary across people and conditions. If the extra model cannot download, read
[the 2025 classifier](https://github.com/sd5913/pfad/blob/2025/week08/9_emotion_detection.py)
and trace detector → face crop → classifier → label with a partner. The modern
`expression` mode shows a MediaPipe facial blendshape score as an alternative;
it also cannot determine a person's emotion.

## 10. Inspiration and project time: 110–120 minutes

Could any of today's ideas inspire your game, app or installation? If useful,
discuss an input, a response and what could happen when tracking fails. This is
an optional prompt: there is no requirement to use computer vision or change
your project idea. Submit your shared repository URL on Canvas as soon as it
exists, then continue working: [group project brief](../assignments/group-project.md).
Use one public repository owned by **sd5913** for the group. Accept the course
organization invitation first, then choose **Owner: sd5913** when creating it.
The [teamwork guide](teamwork.md#3-track-the-work-in-github) explains membership,
teammate permissions and a matching GitHub Projects board. Ask the instructor
for help transferring a repository you have already started.
For your board, open
[Group Project 2026](https://github.com/orgs/sd5913/projects/1), click
**Use this template**, and choose **sd5913** as the owner. Its
weekly iterations and dated tutor review cards cover the class weeks of
**5, 12, 19 and 26 November, and 3 December**. Meet your assigned tutor in your
scheduled tutorial slot that week; record a usable delivery, feedback and the
next goal. See the [delivery meeting guide](teamwork.md#4-weekly-delivery-meetings-with-your-tutor).
Final deadline: **Sunday 6 December 2026, 23:59 HKT**.

Curious about other platforms? Try Google's [hand tracking example in the browser](https://stackblitz.com/github/google-ai-edge/mediapipe-samples-web?file=src%2Ftasks%2Fhand-landmarker.ts)
and see the [JavaScript web guide](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/web_js).
MediaPipe also provides [Android](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/android)
and [iOS](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/ios)
guides and native samples. These are optional starting points, not the Python
tutorial; browser camera access requires permission and a supported browser.

If time permits, create a team repository from the
[Capacitor app starter](https://github.com/sd5913/capacitor-app-template),
[Godot game starter](https://github.com/sd5913/godot-game-template), or
[Python + uv app starter](https://github.com/sd5913/python-uv-app-template). Follow its
README to create a Codex cloud environment, make a small change and inspect its
GitHub Actions artifact. This team work is optional and does not replace the
vision tutorial. A cloud environment, an Actions runner and a hosted deployment
are separate services. Never paste a real token into a repo, prompt or chat.

## Troubleshooting and references

- `Missing ...models`: rerun the download command with internet; a failed
  download can be retried. Models are not committed to Git.
- `Cannot open camera`: grant OS permission, close other camera apps, try
  `--camera 1`, or share a partner's computer. Focus the preview before `q`.
- Window does not open over SSH: use a local graphical session. Use the sample
  coordinate command above if you have no camera.
- On a first run allow time for Python, dependencies and model downloads. If
  tracking flickers, improve light and distance; inspect the no-detection case.
- [MediaPipe Tasks Python guide](https://ai.google.dev/edge/mediapipe/solutions/guide)
  and [Hand Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python).
- [2025 archive](https://github.com/sd5913/pfad/tree/2025/week08) retains the
  original `mp.solutions` scripts and their different dependencies; do not mix
  those instructions with this environment.
