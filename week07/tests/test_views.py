"""Exercise the actual two-view event loop with real model-file edits."""

import inspect
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame

from week07 import ball_both, ball_pygame
from week07.ball_live import MODEL, Simulation


class Terminal(io.StringIO):
    def isatty(self):
        return True


class ViewTests(unittest.TestCase):
    def test_graphical_view_runs_without_drawing_in_the_terminal(self):
        simulation = Simulation(watch=False)
        self.addCleanup(simulation.close)
        terminal = Terminal()
        frames = 0
        original_flip = pygame.display.flip

        def flip():
            nonlocal frames
            frames += 1
            self.assertEqual(terminal.getvalue(), "")
            original_flip()
            if frames == 3:
                self.assertGreater(simulation.balls[0].x, 16)
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        with patch.object(ball_pygame, "Simulation", return_value=simulation), \
                patch("sys.stdout", terminal), patch.object(pygame.display, "flip", flip):
            ball_pygame.main()
        self.assertEqual(terminal.getvalue(), "")

    def test_both_views_move_reload_pause_and_close_together(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ball.py"
            source = MODEL.read_text()
            path.write_text(source)
            simulation = Simulation(path)
            self.addCleanup(simulation.close)
            terminal = Terminal()
            original_flip = pygame.display.flip
            phase = "moving"
            frames = 0
            pause_tick = None

            def flip():
                nonlocal phase, frames, pause_tick
                frames += 1
                self.assertLess(frames, 120, "The real file watcher did not refresh the views")
                local = inspect.currentframe().f_back.f_locals
                self.assertIs(local["simulation"], simulation)
                output = terminal.getvalue().rsplit("\033[H", 1)[-1]
                self.assertIn(f"Frame {simulation.ticks} / revision {simulation.revision}", output)
                blue = simulation.balls[1]
                grid = output.splitlines()
                self.assertEqual(grid[2 + round(blue.y / 2)][1 + round(blue.x)], "B")
                self.assertEqual(tuple(local["screen"].get_at(local["center"]))[:3], (109, 208, 221))
                original_flip()

                if phase == "moving" and simulation.ticks > 12:
                    self.assertGreater(simulation.balls[0].x, 16)
                    path.write_text(source.replace("GRAVITY = 28", "GRAVITY = 56"))
                    phase = "changed"
                elif phase == "changed" and simulation.revision == 2:
                    self.assertEqual(simulation.model.GRAVITY, 56)
                    path.write_text("class Ball(\n")
                    phase = "invalid"
                elif phase == "invalid" and "SyntaxError" in simulation.status:
                    self.assertEqual(simulation.revision, 2)
                    path.write_text(source)
                    phase = "fixed"
                elif phase == "fixed" and simulation.revision == 3:
                    self.assertEqual(simulation.model.GRAVITY, 28)
                    pause_tick = simulation.ticks
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
                    phase = "paused"
                elif phase == "paused":
                    self.assertTrue(local["paused"])
                    self.assertEqual(simulation.ticks, pause_tick)
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
                    phase = "reset"
                elif phase == "reset":
                    self.assertEqual(simulation.ticks, 0)
                    self.assertEqual(simulation.balls[0].x, 16)
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    phase = "closed"

            with patch.object(ball_pygame, "Simulation", return_value=simulation), \
                    patch("sys.stdout", terminal), \
                    patch("week07.ball_play.shutil.get_terminal_size", return_value=os.terminal_size((80, 30))), \
                    patch.object(pygame.display, "flip", flip):
                ball_both.main()
            self.assertEqual(phase, "closed")
            self.assertFalse(simulation.thread.is_alive())
            self.assertTrue(terminal.getvalue().endswith("\033[?25h\n"))


if __name__ == "__main__":
    unittest.main()
