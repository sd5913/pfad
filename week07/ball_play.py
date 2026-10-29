# /// script
# requires-python = ">=3.10"
# dependencies = ["watchfiles==1.3.0"]
# ///
"""An animated ASCII view of the shared Ball physics model."""

import shutil
import sys
import textwrap
import time

if __package__:
    from .ball_live import Simulation
else:
    from ball_live import Simulation


def render_ascii(balls, width, height, columns=61, rows=19):
    cells = [[" "] * columns for _ in range(rows)]
    for index, ball in enumerate(balls):
        x = min(columns - 1, max(0, round(ball.x / width * (columns - 1))))
        y = min(rows - 1, max(0, round(ball.y / height * (rows - 1))))
        cells[y][x] = "R" if index == 0 else "B"
    border = "+" + "-" * columns + "+"
    return "\n".join([border, *("|" + "".join(row) + "|" for row in cells), border])


class AsciiView:
    def __init__(self, stream=None):
        self.stream = sys.stdout if stream is None else stream
        self.enabled = self.stream.isatty()
        if self.enabled:
            self.stream.write("\033[2J\033[?25l")

    def draw(self, simulation):
        if not self.enabled:
            return
        terminal = shutil.get_terminal_size((80, 30))
        # Leave a column and a row unused to avoid terminal wrapping and scrolling.
        width, height = max(1, terminal.columns - 1), max(1, terminal.lines - 1)
        heading = textwrap.wrap("BALL PHYSICS / ASCII / same model as the graphical view", width)
        counter = textwrap.wrap(f"Frame {simulation.ticks} / revision {simulation.revision}", width)
        status = textwrap.wrap(simulation.status, width)
        if len(status) > 2:
            status = [status[0], status[1][:max(0, width - 3)] + "." * min(3, width)]
        help_text = textwrap.wrap("Edit ball.py and save. Ctrl+C or close the window to stop.", width)
        rows = min(19, height - len(heading + counter + status + help_text) - 2)
        if width < 10 or rows < 2:
            text = "Enlarge terminal"[:width]
        else:
            board = render_ascii(simulation.balls, simulation.model.WIDTH, simulation.model.HEIGHT,
                                 columns=min(61, width - 2), rows=rows)
            text = "\n".join([*heading, board, *counter, *status, *help_text])
        self.stream.write("\033[H" + text + "\033[J")
        self.stream.flush()

    def close(self):
        if self.enabled:
            self.stream.write("\033[?25h\n")
            self.stream.flush()


def main():
    simulation = Simulation()
    view = AsciiView()
    previous = time.monotonic()
    try:
        while True:
            now = time.monotonic()
            simulation.advance(now - previous)
            previous = now
            view.draw(simulation)
            time.sleep(1 / 30)
    except KeyboardInterrupt:
        pass
    finally:
        simulation.close()
        view.close()


if __name__ == "__main__":
    main()
