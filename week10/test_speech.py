"""A player exit alone must not accept a missing audio file."""
from pathlib import Path
import tempfile
import unittest

from speech import play


class PlaybackTests(unittest.TestCase):
    def test_missing_wave_is_rejected_before_player_start(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                play(Path(directory) / 'missing.wav')


if __name__ == '__main__':
    unittest.main()
