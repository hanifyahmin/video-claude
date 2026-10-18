"""Promo data model: what the cover shows and what the post says."""
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path

from oyen.character import POSE_SPECS

from .icons import ICONS

CAPTION_MAX = 2200        # TikTok post caption limit
CAPTION_VISIBLE = 120     # roughly what shows before "more" on the feed
HEADLINE_MAX = 14         # characters per headline line at cover size
STYLES = ("cute", "classic")  # cute: bright sticker cover with a cut-out product; classic: dark full-frame
TAG_MAX = 10              # characters per pink size/fact tag
FEATURE_LINE_MAX = 12     # characters per line of a feature-row label


@dataclass(frozen=True)
class Promo:
    # --- cover ---
    frame_src: float                 # source-footage second used as the cover background
    kicker: str                      # small line above the headline
    headline: list                   # 1-3 big lines; wrap a word in *stars* to make it yellow
    pose: str = "Teruja"             # Oyen pose on the cover
    bubble: str = None               # Oyen's speech bubble on the cover (optional)
    badge: str = None                # round sticker, e.g. "MAX 50KG" (optional, keep it a visible fact)
    badge_xy: tuple = None           # badge top-left; None = the style's default spot
    frame_shift: int = 0             # classic: px to move the background up (+) or down (-) so the product clears the text
    style: str = "cute"
    tags: tuple = ()                 # cute: up to 2 pink fact tags beside the product, e.g. ("30ml",)
    product_crop: tuple = None       # cute: (x, y, w, h) of the 1080x1920 frame to keep, e.g. to drop most of a hand
    features: tuple = ()             # cute: up to 3 (icon, "line 1\nline 2") items for the bottom row; icons in promo/icons.py
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
        if self.style not in STYLES:
            out.append(f"unknown style {self.style!r}; choose from {STYLES}")
        if len(self.tags) > 2:
            out.append("at most 2 tags")
        for tag in self.tags:
            if len(tag) > TAG_MAX:
                out.append(f"tag {tag!r} is over {TAG_MAX} chars")
        if len(self.features) > 3:
            out.append("at most 3 features")
        for icon, label in self.features:
            if icon not in ICONS:
                out.append(f"unknown feature icon {icon!r}; choose from {list(ICONS)}")
            lines = label.split("\n")
            if len(lines) > 2 or any(len(line) > FEATURE_LINE_MAX for line in lines):
                out.append(f"feature label {label!r} needs <= 2 lines of <= {FEATURE_LINE_MAX} chars")
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
