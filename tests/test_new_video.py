"""python3 -m unittest discover -s tests   (from the repo root)"""
import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("new_video", REPO / "tools" / "new_video.py")
new_video = importlib.util.module_from_spec(spec)
spec.loader.exec_module(new_video)


class VideoFilterTest(unittest.TestCase):
    def test_default_grade_is_bright(self):
        self.assertEqual(new_video.video_filter(), new_video.GRADES["bright"])

    def test_rotation_comes_before_the_grade(self):
        chain = new_video.video_filter("cw", "bright")
        self.assertTrue(chain.startswith("transpose=1,"))
        self.assertIn("unsharp", chain)

    def test_no_filters(self):
        self.assertIsNone(new_video.video_filter("none", "none"))
        self.assertEqual(new_video.video_filter("ccw", "none"), "transpose=2")


if __name__ == "__main__":
    unittest.main()
