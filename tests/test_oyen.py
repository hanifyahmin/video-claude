"""python3 -m unittest discover -s tests   (from the repo root)"""
import shutil
import tempfile
import unittest
from pathlib import Path

from oyen import character as C
from oyen import install
from oyen.palette import PAL
from oyen.storyline import Beat, Storyline, load

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "templates" / "tiktok-9x16"


class CharacterTest(unittest.TestCase):
    def assert_sprite(self, rows, label):
        self.assertEqual(len(rows), C.CH, label)
        for r in rows:
            self.assertEqual(len(r), C.CW, label)
            self.assertTrue(set(r) <= set(PAL) | {"."}, f"{label}: unknown colour key in {r!r}")

    def test_every_pose_is_a_valid_sprite(self):
        for name, rows in C.POSES.items():
            self.assert_sprite(rows, name)

    def test_video_frames(self):
        for name, spec in C.POSE_SPECS.items():
            frames = C.video_frames(name)
            for kind, rows in frames.items():
                self.assert_sprite(rows, f"{name}/{kind}")
            self.assertEqual("talk" in frames, spec.talk, name)
            self.assertEqual("blink" in frames, spec.blink, name)
            if "talk" in frames:
                self.assertNotEqual(frames["talk"], frames["rest"], f"{name}: talking frame equals rest")


class StorylineTest(unittest.TestCase):
    def test_valid(self):
        s = Storyline("t", [Beat(0, 1, "a", "Senyum", "Hai"), Beat(1, 2, "b", "Teruja")], blinks=[0.5])
        self.assertEqual(s.problems(), [])

    def test_problems(self):
        s = Storyline("t", [Beat(0.5, 1, "a", "Nope"), Beat(1.2, 2, "b", "Senyum", "x" * 30)], blinks=[1.5])
        text = "\n".join(s.problems())
        for expected in ("unknown pose", "previous beat ends", "chars (max", "start at 0"):
            self.assertIn(expected, text)

    def test_blink_needs_open_eyes(self):
        s = Storyline("t", [Beat(0, 1, "a", "Tidur")], blinks=[0.5])
        self.assertIn("no blink frame", "\n".join(s.problems()))

    def test_every_video_storyline_is_valid(self):
        for story_file in sorted((REPO / "videos").glob("*/storyline.py")):
            with self.subTest(video=story_file.parent.name):
                self.assertEqual(load(story_file.parent).problems(), [])


class TabbyScheduleTest(unittest.TestCase):
    def test_loop_talk_and_blink(self):
        from oyen import tabby
        frames = tabby.frames_for("Duduk", 0, 4, talk=(1.0, 1.5), blinks=[3.0])
        self.assertEqual(frames[0], (0, 1))
        self.assertTrue(any(isinstance(n, tuple) for t, n in frames if 1.0 <= t < 1.5))  # mouth flaps
        self.assertFalse(any(isinstance(n, tuple) for t, n in frames if t >= 1.5))
        self.assertIn((3.0, tabby.anims()["Duduk"]["blink"]), frames)

    def test_one_shot_holds(self):
        from oyen import tabby
        frames = tabby.frames_for("Lompat", 0, 10)
        self.assertEqual(len(frames), len(tabby.anims()["Lompat"]["seq"]))


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.video = self.tmp / "demo"
        shutil.copytree(TEMPLATE, self.video)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_install_is_idempotent_and_complete(self):
        install.install(self.video)
        first = (self.video / "index.html").read_text()
        install.install(self.video)
        self.assertEqual((self.video / "index.html").read_text(), first)
        story = load(self.video)
        for bid, *_ in install.bubbles(story):
            self.assertIn(f'id="{bid}"', first)
            self.assertIn(f'id="sfx-pop-{bid}"', first)
        self.assertEqual(story.character, "tabby")  # the template uses Oyen v2
        self.assertIn('<div id="cat-spr" style="background-position:', first)  # frame-0 sprite is static HTML
        self.assertIn('<div id="cat" style="left: -', first)  # Jalan on beat 0 starts off-screen
        self.assertTrue((self.video / "assets" / install.TABBY_ASSET).exists())
        for name in install.NEEDED_SFX:
            self.assertTrue((self.video / "assets" / "sfx" / name).exists())

    def test_missing_marker_is_reported(self):
        index = self.video / "index.html"
        index.write_text(index.read_text().replace("// OYEN:START", "// gone"))
        with self.assertRaisesRegex(ValueError, "missing // OYEN:START"):
            install.install(self.video)

    def test_storyline_longer_than_composition_is_rejected(self):
        index = self.video / "index.html"
        index.write_text(index.read_text().replace('data-duration="6"', 'data-duration="4"', 1))
        with self.assertRaisesRegex(ValueError, "composition is 4s"):
            install.install(self.video)


class OyenRestraintTest(unittest.TestCase):
    def test_notes_flag_chatty_and_repetitive_storylines(self):
        from oyen.storyline import Beat, Storyline
        beats = [Beat(i, i + 1, "x", "Senyum" if i < 2 else "Teruja", "hai") for i in range(4)]
        notes = "\n".join(Storyline("t", beats).notes())
        self.assertIn("4 speech lines", notes)
        self.assertIn("repeats 'Senyum'", notes)

    def test_new_poses_build(self):
        from oyen import character as C
        for name in ("Gelak", "Sedih", "Cool", "Geram", "Malu", "Pening"):
            with self.subTest(pose=name):
                self.assertEqual(len(C.POSES[name]), C.CH)
                self.assertIn("rest", C.video_frames(name))


class ChibiInstallTest(InstallTest):
    def setUp(self):
        super().setUp()
        story = (self.video / "storyline.py").read_text()
        story = story.replace('character="tabby"', 'character="chibi"')
        for old, new in (('"Jalan"', '"Senyum"'), ('"Duduk", "Walaweh!"', '"Bercakap", "Walaweh!"'),
                         ('"Gembira"', '"Cool"'), ('"Duduk", "Jom checkout!"', '"Shopping", "Jom checkout!"'),
                         ('"Lompat"', '"Kenyit mata"')):
            story = story.replace(old, new)
        (self.video / "storyline.py").write_text(story)

    def test_install_is_idempotent_and_complete(self):
        install.install(self.video)
        first = (self.video / "index.html").read_text()
        install.install(self.video)
        self.assertEqual((self.video / "index.html").read_text(), first)
        story = load(self.video)
        self.assertIn('style="opacity: 1"', first)  # frame-0 pose is static HTML
        self.assertEqual(first.count('class="oy-f"'), len(install.used_frames(story)))


if __name__ == "__main__":
    unittest.main()
