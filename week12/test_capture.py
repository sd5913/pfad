"""Metadata checks only: these do not manufacture or prove graphical capture."""
import unittest

import world


class CaptureMetadataTests(unittest.TestCase):
    def test_rejects_short_wrong_size_or_missing_frame_count(self):
        self.assertTrue(hasattr(world, "validate_movie"), "capture validation is missing")
        good = {"format": {"duration": "4.0"}, "streams": [
            {"codec_type": "video", "width": 960, "height": 540, "nb_frames": "120"}]}
        world.validate_movie(good)
        for broken in [
            {**good, "format": {"duration": "0.01"}},
            {**good, "streams": [{"codec_type": "video", "width": 960, "height": 540}]},
            {**good, "streams": [{"codec_type": "video", "width": 64, "height": 64, "nb_frames": "120"}]},
        ]:
            with self.assertRaises(ValueError):
                world.validate_movie(broken)


if __name__ == "__main__":
    unittest.main()
