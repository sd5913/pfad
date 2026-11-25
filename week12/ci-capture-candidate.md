# Proposed public CI graphics acceptance

**Candidate only, not run evidence.** The coordinator owns shared workflows.
This file supplies a normal read-only PR job proposal; it does not install or
start anything on the authoring laptop, change a token's rights or publish a
course release. Local Wayland transport is blocked by EPERM, so repeated GUI
attempts here would add no useful proof.

Use an ordinary `pull_request` workflow, Ubuntu 24.04 GitHub-hosted runner,
`permissions: {contents: read}`, no secrets/model calls and a 10-minute job
limit. Do not use `pull_request_target`. Use the repository's verified checkout
and uv setup actions. The command step below works from repository root and
uses task-specific environment variable names. Record both download time and
engine/capture duration; runner download timing is still not a student's cold
graphical bootstrap measurement.

The pinned download is the latest stable verified on 29 October 2026, 4.7.2.
Recheck the official release before running; if a newer stable exists, update
version/asset/checksum together and rerun rather than silently using an old
release. The Linux x86_64 standard ZIP is 77,860,424 bytes. Its SHA-256 was
supplied by the coordinator's primary-source verification:
`cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4`.

```bash
set -euo pipefail
sudo apt-get update
sudo apt-get install -y xvfb xauth libgl1-mesa-dri libglx-mesa0 libegl1 ffmpeg unzip
mkdir -p "$RUNNER_TEMP/week12-godot"
curl --fail --location --retry 3 \
  'https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip' \
  --output "$RUNNER_TEMP/week12-godot/godot.zip"
python - <<'PY'
import hashlib
import os
from pathlib import Path
archive = Path(os.environ['RUNNER_TEMP']) / 'week12-godot/godot.zip'
assert archive.stat().st_size == 77860424
assert hashlib.sha256(archive.read_bytes()).hexdigest() == 'cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4'
PY
unzip -q "$RUNNER_TEMP/week12-godot/godot.zip" -d "$RUNNER_TEMP/week12-godot"
export GODOT_PATH="$RUNNER_TEMP/week12-godot/Godot_v4.7.2-stable_linux.x86_64"
chmod +x "$GODOT_PATH"
"$GODOT_PATH" --version
cd week12
uv run --locked python -m unittest discover -p 'test_*.py' -v
uv run python world.py set speed 275
uv run python world.py check
xvfb-run -a -s '-screen 0 1280x720x24' \
  env LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe \
  uv run python world.py capture
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,nb_frames \
  -of json .output/world.mp4
ffmpeg -v error -xerror -i .output/world.mp4 -f null -
```

`world.py` supplies a writable project-local XDG_DATA_HOME; do not rewrite the
runner's HOME. Project settings select Godot's Compatibility renderer. Xvfb is
a real software graphics target here; **do not add `--headless` to capture**.
The engine's real headless tests are separate. Capture checks a new behavior
run, discards old movie outputs, requires actual replay completion, encodes,
validates 960x540/about 4 seconds/120 frames, decodes all frames and extracts three
sample PNGs. A failed command must fail the job, even if a partial file exists.

Afterward upload only the explicit files below, with `if: always()` so errors
survive, `if-no-files-found: error` and `retention-days: 7` (within repository
limits). Use the repository's reviewed upload-artifact action; current GitHub
docs show v4. Specify `include-hidden-files: true` for the `.output` path and
explicitly list safe public outputs instead of uploading caches or the whole
checkout:

```yaml
with:
  name: week12-graphics-evidence
  include-hidden-files: true
  if-no-files-found: error
  retention-days: 7
  path: |
    week12/godot/world.json
    week12/.output/check.json
    week12/.output/capture.json
    week12/.output/last-error.json
    week12/.output/world.mp4
    week12/.output/frame-start.png
    week12/.output/frame-middle.png
    week12/.output/frame-end.png
```

Retain normal job logs for exact source commit, engine version, package setup,
checks and download/capture timings. A reviewer downloads and plays the actual
MP4, inspects all three PNGs at full size and records player movement, light
collection, exit opening and COMPLETE. Metadata/decode success alone does not
close the film gate. A runner success also does not time the first-time desktop
student route or prove Windows/macOS setup and partner-machine retrieval.
Those remain separate acceptance tasks in the README.

Sources fetched through Context7 on 29 October: official Godot 4.7 Movie Maker
and CLI docs; GitHub Actions workflow `permissions` and artifact retention
[documentation](https://docs.github.com/en/actions/tutorials/store-and-share-data).
Official [Godot release](https://github.com/godotengine/godot-builds/releases/tag/4.7.2-stable).
No job has been run from this proposal and no artifact is claimed to exist.
