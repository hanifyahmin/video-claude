"""Promo data model: what the cover shows and what the post says."""
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path

from oyen.character import POSE_SPECS

CAPTION_MAX = 2200        # TikTok post caption limit
CAPTION_VISIBLE = 120     # roughly what shows before "more" on the feed
HEADLINE_MAX = 14         # characters per headline line at cover size


@dataclass(frozen=True)
class Promo:
    # --- cover ---
    frame_src: float                 # source-footage second used as the cover background
    kicker: str                      # small line above the headline
    headline: list                   # 1-3 big lines; wrap a word in *stars* to make it yellow
    pose: str = "Teruja"             # Oyen pose on the cover
    bubble: str = None               # Oyen's speech bubble on the cover (optional)
    badge: str = None                # round sticker, e.g. "MAX 50KG" (optional, keep it a visible fact)
    badge_xy: tuple = (770, 1400)    # badge top-left; keep it off the product
    frame_shift: int = 0             # px to move the background up (+) or down (-) so the product clears the text
    source: str = "assets/source-portrait.mp4"
    # --- post ---
    caption: str = ""                # first ~120 chars are what people see: hook + key fact + CTA
    hashtags: list = field(default_factory=list)

    def problems(self):
        out = []
        if self.pose not in POSE_SPECS:
            out.append(f"unknown pose {self.pose!r}; choose from {list(POSE_SPECS)}")
        if not 1 <= len(self.headline) <= 3:
            out.append("headline needs 1-3 lines")
        for line in self.headline:
            if len(line.replace("*", "")) > HEADLINE_MAX:
                out.append(f"headline line {line!r} is over {HEADLINE_MAX} chars; split it")
        if self.bubble and len(self.bubble) > 20:
            out.append(f"bubble {self.bubble!r} is over 20 chars")
        if not self.caption:
            out.append("caption is empty")
        if len(self.caption_text()) > CAPTION_MAX:
            out.append(f"caption + hashtags is over {CAPTION_MAX} chars")
        for tag in self.hashtags:
            if not tag.startswith("#") or " " in tag:
                out.append(f"hashtag {tag!r} must start with # and have no spaces")
        return out

    def caption_text(self):
        return self.caption.strip() + ("\n\n" + " ".join(self.hashtags) if self.hashtags else "") + "\n"


def load(video_dir):
    path = Path(video_dir) / "promo.py"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found (copy templates/tiktok-9x16/promo.py)")
    spec = importlib.util.spec_from_file_location(f"promo_{Path(video_dir).name}", path)
    mod = importlib.util.module_from_spec(spec)
    dont_write, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = dont_write
    return mod.PROMO
