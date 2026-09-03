"""
Schotter — after Georg Nees, 1968.

A square grid that falls apart as it descends. The top row is perfectly ordered;
each row after it is rotated and displaced a little more than the one before.
Nees plotted the original on a Zuse Graphomat; you are about to do it in a
language he did not have, on a machine he would have envied.

Run it:

    python sketch.py

It writes sketch.svg next to this file. Open that in a browser (or drag it into
VS Code). Nothing to install — this uses only what ships with Python.

Then change one of the numbers below, run it again, and commit. GitHub will show
you the two images side by side.
"""

import math
import random

# ---------------------------------------------------------------------------
# The knobs. These are yours. Change them, run again, look, commit.
# ---------------------------------------------------------------------------

COLS = 12            # hexagons across
ROWS = 22            # hexagons down — the chaos builds over this many rows
SEED = 5913          # any integer. Same seed = same image, every time, forever.
CHAOS = 1           # how fast order collapses. 0 = perfect grid. 2 = rubble.
SQUARE = 40          # size of one hexagon, in svg units
MARGIN = 60          # breathing room around the grid
STROKE = "#111111"   # line colour
BACKGROUND = "#faf8f4"
STROKE_WIDTH = 3

OUTPUT = "sketch2.svg"

# ---------------------------------------------------------------------------
# The drawing.
# ---------------------------------------------------------------------------


def hexagon(x, y, size, angle_deg, dx, dy):
    """One hexagon, rotated about its own centre and nudged off its grid slot."""
    cx, cy = x + size / 2, y + size / 2
    radius = size / 2
    points = []
    for i in range(6):
        angle = math.radians(90 + i * 60)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        points.append(f"{px:.2f},{py:.2f}")
    points_str = " ".join(points)
    return (
        f'  <polygon points="{points_str}" '
        f'transform="translate({dx:.2f} {dy:.2f}) '
        f'rotate({angle_deg:.2f} {cx:.2f} {cy:.2f})" />'
    )


def draw():
    rng = random.Random(SEED)
    parts = []

    for row in range(ROWS):
        # Disorder grows with depth. Hexagons keep the top calm and let the
        # bottom really come apart — the whole point of the piece.
        damage = CHAOS * (row / ROWS) ** 2

        for col in range(COLS):
            x = MARGIN + col * SQUARE * 0.9
            y = MARGIN + row * SQUARE * 0.75
            if row % 2:
                x += SQUARE * 0.45
            angle = rng.uniform(-1, 1) * damage * 45
            dx = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            dy = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            parts.append(hexagon(x, y, SQUARE, angle, dx, dy))

    width = COLS * SQUARE * 0.9 + SQUARE + MARGIN * 2
    height = ROWS * SQUARE * 0.75 + SQUARE + MARGIN * 2

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">',
            f'  <rect width="100%" height="100%" fill="{BACKGROUND}" />',
            f'  <g fill="none" stroke="{STROKE}" stroke-width="{STROKE_WIDTH}">',
            *parts,
            "  </g>",
            "</svg>",
        ]
    )


if __name__ == "__main__":
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(draw())
    print(f"wrote {OUTPUT} — {COLS}x{ROWS} hexagons, seed {SEED}, chaos {CHAOS}")
    print("open it in a browser, then change a number and run me again")
