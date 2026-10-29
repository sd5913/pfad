"""Physics shared by the terminal and graphical views."""

import unittest

from week07.ball import Ball


class PhysicsTests(unittest.TestCase):
    def test_gravity_changes_velocity_before_position(self):
        ball = Ball(x=10, y=10, vx=4, vy=0)
        ball.update(0.1)
        self.assertAlmostEqual(ball.x, 10.4)
        self.assertGreater(ball.vy, 0)
        self.assertAlmostEqual(ball.y, 10 + ball.vy * 0.1)

    def test_only_the_updated_object_moves(self):
        red = Ball(x=10, y=10, vx=4, vy=0)
        blue = Ball(x=30, y=12, vx=-2, vy=0)
        red.update(0.1)
        self.assertEqual((blue.x, blue.y, blue.vx, blue.vy), (30, 12, -2, 0))

    def test_floor_bounces_up_and_loses_speed(self):
        ball = Ball(x=20, y=34.9, vx=0, vy=12)
        ball.update(0.1)
        self.assertLessEqual(ball.y, 35)
        self.assertLess(ball.vy, 0)
        self.assertLess(abs(ball.vy), 12 + 0.1 * 28)

    def test_walls_reverse_velocity(self):
        for x, vx, direction in [(1.1, -8, 1), (58.9, 8, -1)]:
            with self.subTest(x=x):
                ball = Ball(x=x, y=10, vx=vx, vy=0)
                ball.update(0.1)
                self.assertGreaterEqual(ball.x, 1)
                self.assertLessEqual(ball.x, 59)
                self.assertGreater(ball.vx * direction, 0)

    def test_long_run_stays_inside_the_world(self):
        ball = Ball(x=20, y=10, vx=17, vy=-13)
        for _ in range(3600):
            ball.update(1 / 120)
            self.assertTrue(1 <= ball.x <= 59)
            self.assertTrue(1 <= ball.y <= 35)


if __name__ == "__main__":
    unittest.main()
