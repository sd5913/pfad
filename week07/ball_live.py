"""Shared simulation clock and live reload support for the two views."""

import math
from pathlib import Path
from threading import Event, Thread
from types import ModuleType

STEP = 1 / 120
MODEL = Path(__file__).with_name("ball.py")


def validate_ball(ball, model):
    if not all(math.isfinite(getattr(ball, name))
               for name in ("x", "y", "vx", "vy", "radius")):
        raise ValueError("Ball coordinates, velocity and radius must be finite")
    if not 0 < ball.radius < min(model.WIDTH, model.HEIGHT) / 2:
        raise ValueError("Ball radius must be positive and fit inside the arena")
    if not (ball.radius <= ball.x <= model.WIDTH - ball.radius
            and ball.radius <= ball.y <= model.HEIGHT - ball.radius):
        raise ValueError("Ball position must fit inside the arena, including its radius")


class Simulation:
    def __init__(self, path=MODEL, watch=True):
        self.path = Path(path).resolve()
        self.changed = Event()
        self.stopped = Event()
        self.ready = Event()
        self.thread = None
        self.revision = 0
        self.status = "Save ball.py to reload."
        self.failed = False
        self.reload()
        if watch:
            self.thread = Thread(target=self._watch, daemon=True)
            self.thread.start()
            self.ready.wait(timeout=2)

    def _watch(self):
        try:
            from watchfiles import watch

            # Watch the directory so editors that replace files on save also work.
            for changes in watch(
                self.path.parent,
                watch_filter=lambda change, path: Path(path).resolve() == self.path,
                stop_event=self.stopped,
                debounce=150,
                step=50,
                rust_timeout=100,
                yield_on_timeout=True,
                recursive=False,
                raise_interrupt=False,
            ):
                self.ready.set()
                if changes:
                    self.changed.set()
        except Exception as exc:
            self.status = f"Watcher error: {exc}"
        finally:
            self.ready.set()

    def reload(self):
        try:
            # Compile fresh source: bytecode caching can miss rapid same-size edits.
            model = ModuleType("live_ball")
            model.__file__ = str(self.path)
            exec(compile(self.path.read_text(), str(self.path), "exec"), model.__dict__)
            if not (math.isfinite(model.WIDTH) and math.isfinite(model.HEIGHT)
                    and model.WIDTH > 2 and model.HEIGHT > 2):
                raise ValueError("WIDTH and HEIGHT must be finite numbers greater than 2")
            if not (math.isfinite(model.GRAVITY) and math.isfinite(model.BOUNCE)):
                raise ValueError("GRAVITY and BOUNCE must be finite numbers")
            trial = model.starting_balls()
            if not trial:
                raise ValueError("Create at least one ball in starting_balls()")
            for ball in trial:
                validate_ball(ball, model)
                ball.update(STEP)
                validate_ball(ball, model)
            balls = model.starting_balls()
            for ball in balls:
                validate_ball(ball, model)
        except Exception as exc:
            self.status = f"{type(exc).__name__}: {exc} / keeping the last working model"
            if self.revision == 0:
                raise
            return False

        self.model = model
        self.balls = balls
        self.accumulator = 0
        self.ticks = 0
        self.failed = False
        self.revision += 1
        self.status = f"ball.py loaded / revision {self.revision} / save to reload"
        return True

    def advance(self, seconds):
        if self.changed.is_set():
            self.changed.clear()
            self.reload()
        if self.failed:
            return
        self.accumulator += min(max(seconds, 0), 0.1)
        while self.accumulator + 1e-12 >= STEP:
            # Keep both views on a complete, renderable step if an edit fails later.
            previous = [vars(ball).copy() for ball in self.balls]
            try:
                for ball in self.balls:
                    ball.update(STEP)
                    validate_ball(ball, self.model)
            except Exception as exc:
                for ball, state in zip(self.balls, previous):
                    vars(ball).clear()
                    vars(ball).update(state)
                self.status = f"{type(exc).__name__}: {exc} / save ball.py to recover"
                self.failed = True
                return
            self.accumulator -= STEP
            self.ticks += 1

    def close(self):
        self.stopped.set()
        if self.thread:
            self.thread.join(timeout=1)
