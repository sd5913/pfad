"""Real source edits, fixed-step timing and read-only ASCII rendering."""

import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from week07.ball import Ball
from week07.ball_live import MODEL, Simulation
from week07.ball_play import AsciiView, render_ascii


class LiveTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "ball.py"
        self.source = MODEL.read_text()
        self.path.write_text(self.source)

    def simulation(self, watch=False):
        simulation = Simulation(self.path, watch=watch)
        self.addCleanup(simulation.close)
        return simulation

    def test_ascii_renders_positions_without_changing_the_model(self):
        balls = [Ball(x=10, y=8, vx=3, vy=-2), Ball(x=30, y=20, vx=-4, vy=5)]
        before = [vars(ball).copy() for ball in balls]
        lines = render_ascii(balls, 60, 36).splitlines()
        self.assertEqual(lines[5][11], "R")
        self.assertEqual(lines[11][31], "B")
        self.assertEqual([vars(ball) for ball in balls], before)

    def test_different_render_rates_give_the_same_motion(self):
        slow, fast = self.simulation(), self.simulation()
        for _ in range(30):
            slow.advance(1 / 30)
        for _ in range(60):
            fast.advance(1 / 60)
        self.assertEqual(slow.ticks, fast.ticks)
        self.assertEqual([vars(ball) for ball in slow.balls], [vars(ball) for ball in fast.balls])

    def test_rapid_same_size_edit_loads_fresh_class_code(self):
        simulation = self.simulation()
        simulation.advance(0.1)
        self.path.write_text(self.source.replace("GRAVITY = 28", "GRAVITY = 56"))
        self.assertTrue(simulation.reload())
        simulation.advance(1 / 120)
        self.assertAlmostEqual(simulation.balls[0].vy, -5 + 56 / 120)
        self.assertEqual(simulation.revision, 2)

    def test_saved_update_method_changes_the_motion(self):
        simulation = self.simulation()
        self.path.write_text(self.source.replace("self.x += self.vx * seconds", "self.x -= self.vx * seconds"))
        self.assertTrue(simulation.reload())
        simulation.advance(1 / 120)
        self.assertLess(simulation.balls[0].x, 16)

    def test_bad_save_keeps_the_previous_model_running_then_recovers(self):
        simulation = self.simulation()
        model = simulation.model
        self.path.write_text("class Ball(\n")
        self.assertFalse(simulation.reload())
        self.assertIs(simulation.model, model)
        before = simulation.balls[0].x
        simulation.advance(0.1)
        self.assertGreater(simulation.balls[0].x, before)
        self.path.write_text(self.source)
        self.assertTrue(simulation.reload())
        self.assertEqual(simulation.balls[0].x, 16)

    def test_runtime_error_in_a_new_class_does_not_replace_good_code(self):
        simulation = self.simulation()
        model = simulation.model
        self.path.write_text(self.source.replace("self.vy += GRAVITY * seconds", "self.vy += 1 / 0"))
        self.assertFalse(simulation.reload())
        self.assertIs(simulation.model, model)

    def test_nonfinite_bounce_is_rejected_before_it_can_break_a_renderer(self):
        simulation = self.simulation()
        model = simulation.model
        self.path.write_text(self.source.replace("BOUNCE = 0.82", "BOUNCE = float('nan')"))
        self.assertFalse(simulation.reload())
        self.assertIs(simulation.model, model)

    def test_paused_reload_rejects_balls_that_protrude_outside_the_arena(self):
        simulation = self.simulation()
        model = simulation.model
        before = [vars(ball).copy() for ball in simulation.balls]
        for position in ("x=0.5, y=8", "x=59.5, y=8", "x=16, y=0.5", "x=16, y=35.5"):
            with self.subTest(position=position):
                self.path.write_text(self.source.replace("Ball(x=16, y=8", f"Ball({position}"))
                simulation.changed.set()
                simulation.advance(0)
                self.assertIs(simulation.model, model)
                self.assertEqual(simulation.revision, 1)
                self.assertEqual([vars(ball) for ball in simulation.balls], before)

    def test_late_invalid_state_freezes_the_last_renderable_frame(self):
        simulation = self.simulation()
        simulation.model.GRAVITY = float("nan")
        before = [vars(ball).copy() for ball in simulation.balls]
        simulation.advance(0.1)
        self.assertTrue(simulation.failed)
        self.assertEqual([vars(ball) for ball in simulation.balls], before)
        self.assertIn("R", render_ascii(simulation.balls, 60, 36))
        self.path.write_text(self.source)
        simulation.changed.set()
        simulation.advance(1 / 120)
        self.assertFalse(simulation.failed)
        self.assertGreater(simulation.balls[0].x, 16)

    def test_split_terminal_has_room_for_the_entire_frame(self):
        simulation = self.simulation()
        terminal = io.StringIO()
        terminal.isatty = lambda: True
        view = AsciiView(terminal)
        self.addCleanup(view.close)
        with patch("shutil.get_terminal_size", return_value=os.terminal_size((40, 16))):
            view.draw(simulation)
        frame = terminal.getvalue().rsplit("\033[H", 1)[-1].removesuffix("\033[J")
        lines = frame.splitlines()
        self.assertTrue(all(len(line) < 40 for line in lines), [len(line) for line in lines])
        self.assertLess(len(lines), 16)

    def test_watchfiles_detects_atomic_editor_save_and_stops_cleanly(self):
        simulation = self.simulation(watch=True)
        self.assertTrue(simulation.ready.is_set())
        replacement = self.path.with_name("replacement.py")
        replacement.write_text(self.source.replace("GRAVITY = 28", "GRAVITY = 56"))
        replacement.replace(self.path)
        self.assertTrue(simulation.changed.wait(timeout=3), simulation.status)
        simulation.advance(0)
        self.assertEqual(simulation.model.GRAVITY, 56)
        simulation.close()
        self.assertFalse(simulation.thread.is_alive())


if __name__ == "__main__":
    unittest.main()
