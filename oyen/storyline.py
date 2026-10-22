"""Storyline data model: what Oyen does, when, and what Oyen says.

Each video keeps its own `videos/<name>/storyline.py` that defines
`STORYLINE = Storyline(...)`. Nothing here is product specific.
"""
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path

from . import tabby
from .character import POSE_SPECS

CHARACTERS = ("chibi", "tabby")

MAX_LINE = 20  # characters; longer bubbles reach TikTok's right-side buttons
MAX_LINES = 3  # speech lines per video: Oyen reacts, captions carry the facts


@dataclass(frozen=True)
class Beat:
    start: float          # composition seconds
    end: float
    scene: str            # label for the storyboard ("1 Hook")
    pose: str             # chibi: a key of character.POSE_SPECS; tabby: an animation in oyen/tabby
    line: str = None      # what Oyen says (speech bubble), or None
    note: str = ""        # direction for the storyboard
    src: float = None     # source-footage time for the storyboard thumbnail


@dataclass(frozen=True)
class Layout:
    """Where Oyen and the bubble sit on a 1080x1920 canvas."""
    scale: int = 12             # screen px per sprite pixel (sprite is 28x24)
    cat_left: int = 6
    cat_top: int = 1250
    bubble_left: int = 352
    bubble_top: int = 1302
    bubble_max_width: int = 700
    style: str = "cute"         # "cute": sticker outline + cloud bubble; "bold": white box, black outline,
                                # accent shadow (tools/bold_theme.py); "pixel": ink-box bubble


@dataclass(frozen=True)
class Storyline:
    title: str
    beats: list
    blinks: list = field(default_factory=list)   # seconds; uses the current pose's blink frame
    jumps: list = field(default_factory=list)    # seconds; Oyen hops (reaction to a hit)
    source: str = None                           # footage for storyboard thumbnails (video-relative)
    layout: Layout = Layout()
    type_speed: float = 0.032                    # seconds per typed bubble character
    character: str = "chibi"                     # "tabby": Oyen v2 (oyen/tabby); "chibi": the first Oyen

    def poses(self):
        return tabby.POSES if self.character == "tabby" else tuple(POSE_SPECS)

    def can_talk(self, pose):
        if self.character == "tabby":
            return bool(tabby.anims()[pose].get("talk"))
        return POSE_SPECS[pose].talk

    def can_blink(self, pose):
        if self.character == "tabby":
            return bool(tabby.anims().get(pose, {}).get("blink"))
        return POSE_SPECS.get(pose, POSE_SPECS["Senyum"]).blink

    def problems(self):
        """Human-readable issues; empty list means the storyline is valid."""
        out = []
        if self.character not in CHARACTERS:
            return [f"character {self.character!r} must be one of {CHARACTERS}"]
        if self.layout.style not in ("cute", "bold", "pixel"):
            out.append(f"layout style {self.layout.style!r} must be 'cute', 'bold' or 'pixel'")
        prev_end = None
        for i, b in enumerate(self.beats):
            tag = f"beat {i} ({b.start:g}-{b.end:g}s)"
            if b.pose not in self.poses():
                out.append(f"{tag}: unknown pose {b.pose!r}; choose from {list(self.poses())}")
            if b.end <= b.start:
                out.append(f"{tag}: end must be after start")
            if prev_end is not None and abs(b.start - prev_end) > 1e-6:
                out.append(f"{tag}: starts at {b.start:g}s but the previous beat ends at {prev_end:g}s")
            if b.line and len(b.line) > MAX_LINE:
                out.append(f"{tag}: line {b.line!r} is {len(b.line)} chars (max {MAX_LINE})")
            prev_end = b.end
        if self.beats and self.beats[0].start != 0:
            out.append("the first beat must start at 0 (it is Oyen's state on frame 0)")
        for t in self.blinks:
            beat = self.beat_at(t)
            if beat is None or beat.pose not in self.poses() or not self.can_blink(beat.pose):
                out.append(f"blink at {t:g}s: the pose there has no blink frame")
        return out

    def notes(self):
        """Things worth knowing that are not errors."""
        out = [f"beat {i} ({b.start:g}-{b.end:g}s): {b.pose!r} has no talking frame, so the bubble "
               f"shows without mouth flaps" for i, b in enumerate(self.beats)
               if b.line and b.pose in self.poses() and not self.can_talk(b.pose)]
        lines = sum(1 for b in self.beats if b.line)
        if lines > MAX_LINES:
            out.append(f"{lines} speech lines; keep it to {MAX_LINES} (hook reaction, one punchline, CTA) "
                       f"and let poses carry the rest")
        for i, (a, b) in enumerate(zip(self.beats, self.beats[1:]), 1):
            if a.pose == b.pose:
                out.append(f"beat {i} ({b.start:g}s) repeats {b.pose!r}; vary the pose")
        return out

    def beat_at(self, t):
        for b in self.beats:
            if b.start <= t < b.end:
                return b
        return None

    @property
    def duration(self):
        return self.beats[-1].end if self.beats else 0


def load(video_dir):
    """Import videos/<name>/storyline.py and return its STORYLINE."""
    path = Path(video_dir) / "storyline.py"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found (copy templates/tiktok-9x16/storyline.py)")
    spec = importlib.util.spec_from_file_location(f"storyline_{Path(video_dir).name}", path)
    mod = importlib.util.module_from_spec(spec)
    dont_write, sys.dont_write_bytecode = sys.dont_write_bytecode, True  # no __pycache__ in videos/
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = dont_write
    return mod.STORYLINE
