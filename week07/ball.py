# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""The shared physics model. Neither renderer belongs in this file."""

WIDTH = 60
HEIGHT = 36
GRAVITY = 28
BOUNCE = 0.82


class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 1

    def update(self, seconds):
        self.vy += GRAVITY * seconds
        self.x += self.vx * seconds
        self.y += self.vy * seconds

        if self.x < self.radius:
            self.x = self.radius
            self.vx = abs(self.vx) * BOUNCE
        elif self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.vx = -abs(self.vx) * BOUNCE

        if self.y < self.radius:
            self.y = self.radius
            self.vy = abs(self.vy) * BOUNCE
        elif self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.vy = -abs(self.vy) * BOUNCE
            if abs(self.vy) < 1:
                self.vy = 0


def starting_balls():
    return [Ball(x=16, y=8, vx=14, vy=-5), Ball(x=44, y=14, vx=-10, vy=-9)]


def main():
    red, blue = starting_balls()
    print(f"Before: red=({red.x}, {red.y}), blue=({blue.x}, {blue.y})")
    red.update(0.1)
    print(f"After red.update(0.1): red=({red.x:.2f}, {red.y:.2f}), blue=({blue.x}, {blue.y})")
    blue.update(0.1)
    print(f"After blue.update(0.1): red=({red.x:.2f}, {red.y:.2f}), blue=({blue.x:.2f}, {blue.y:.2f})")


if __name__ == "__main__":
    main()
