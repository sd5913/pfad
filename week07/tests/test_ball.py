"""Small checks for the optional two-object trace."""

import unittest

from week07.ball import Ball, starting_balls


class BallTests(unittest.TestCase):
    def test_only_the_updated_ball_moves(self):
        red, blue = starting_balls()
        red.update(0.1)
        self.assertAlmostEqual(red.x, 17.4)
        self.assertAlmostEqual(red.y, 7.78)
        self.assertEqual((blue.x, blue.y), (44, 14))
        blue.update(0.1)
        self.assertAlmostEqual(blue.x, 43)
        self.assertAlmostEqual(blue.y, 13.38)

    def test_zero_seconds_does_not_move(self):
        ball = Ball(x=20, y=10, vx=3, vy=-5)
        ball.update(0)
        self.assertEqual((ball.x, ball.y, ball.vx, ball.vy), (20, 10, 3, -5))


if __name__ == "__main__":
    unittest.main()
