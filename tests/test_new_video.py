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


class BoldThemeTest(unittest.TestCase):
    def test_template_is_bold_and_niche_swaps_the_accent(self):
        page = (REPO / "templates" / "tiktok-9x16" / "index.html").read_text()
        self.assertIn("--accent: #FFD60A;", page)
        baby = new_video.bold_theme.restyle(page, "baby")
        self.assertIn("--accent: #1C86F2;", baby)
        self.assertNotIn("--accent: #FFD60A;", baby)
        self.assertEqual(new_video.bold_theme.restyle(baby, "baby"), baby)  # rerun is a no-op

    def test_niche_pills_are_readable(self):
        def lum(h):
            c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
            return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
        for niche, (accent, text) in new_video.bold_theme.NICHES.items():
            hi, lo = sorted([lum(accent), lum(text)], reverse=True)
            with self.subTest(niche=niche):
                self.assertGreaterEqual((hi + 0.05) / (lo + 0.05), 3.0)


if __name__ == "__main__":
    unittest.main()
