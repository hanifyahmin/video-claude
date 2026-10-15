"""python3 -m unittest discover -s tests   (from the repo root)"""
import unittest
from pathlib import Path

from promo.model import Promo, load
from promo.thumbnail import build_html

REPO = Path(__file__).resolve().parent.parent


def promo(**kw):
    base = dict(frame_src=1.0, kicker="K", headline=["SATU", "*DUA*"], caption="Hai", hashtags=["#fyp"])
    base.update(kw)
    return Promo(**base)


class PromoTest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(promo().problems(), [])

    def test_problems(self):
        p = promo(pose="Nope", headline=["X" * 20], bubble="y" * 30, caption="", hashtags=["no hash"])
        text = "\n".join(p.problems())
        for expected in ("unknown pose", "over 14 chars", "bubble", "caption is empty", "must start with #"):
            self.assertIn(expected, text)

    def test_caption_text(self):
        self.assertEqual(promo(caption=" Hai \n", hashtags=["#a", "#b"]).caption_text(), "Hai\n\n#a #b\n")

    def test_html_highlights_and_escapes(self):
        page = build_html(promo(headline=["A&B", "*YES*"], badge="MAX <50>"))
        self.assertIn('<span class="hl">YES</span>', page)
        self.assertIn("A&amp;B", page)
        self.assertIn("MAX &lt;50&gt;", page)
        self.assertIn('data-composition-id="cover"', page)

    def test_every_video_promo_is_valid(self):
        for f in sorted((REPO / "videos").glob("*/promo.py")):
            with self.subTest(video=f.parent.name):
                self.assertEqual(load(f.parent).problems(), [])


if __name__ == "__main__":
    unittest.main()
