# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""A bounded loop to predict and trace before running."""

import sys

limit = 3
if len(sys.argv) > 1:
    limit = int(sys.argv[1])

step = 0

while step < limit:
    print(step)
    step += 1

print("done")
