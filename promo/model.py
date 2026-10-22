"""Promo data model: what the cover shows and what the post says."""
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path

from oyen import tabby
from oyen.character import POSE_SPECS

from .icons import ICONS

REPO = Path(__file__).resolve().parent.parent


def niche_colours(niche):
    """(accent, text on accent) of a niche, shared with the video theme (tools/bold_theme.py)."""
    spec = importlib.util.spec_from_file_location("bold_theme", REPO / "tools" / "bold_theme.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.NICHES[niche] if niche in mod.NICHES else None

CAPTION_MAX = 2200        # TikTok post caption limit
CAPTION_VISIBLE = 120     # roughly what shows before "more" on the feed
HEADLINE_MAX = 14         # characters per headline line at cover size
STYLES = ("bold", "cute", "classic")  # bold: matches the bold video theme (default); cute: pastel sticker cover
                                     # with a cut-out product; classic: the first dark full-frame cover
TAG_MAX = 10              # characters per line of a pink size/fact tag (1-2 lines)
FEATURE_LINE_MAX = 12     # characters per line of a feature-row label


@dataclass(frozen=True)
class Promo:
    # --- cover ---
    frame_src: float                 # source-footage second used as the cover background
    kicker: str                      # small line above the headline
    headline: list                   # 1-3 big lines; wrap a word in *stars* to make it yellow
    pose: str = "Teruja"             # Oyen pose on the cover (an animation name for the tabby)
    character: str = "chibi"         # "tabby": Oyen v2 (bold covers only); "chibi": the first Oyen
    bubble: str = None               # Oyen's speech bubble on the cover (optional)
    badge: str = None                # round sticker, e.g. "MAX 50KG" (optional, keep it a visible fact)
    badge_xy: tuple = None           # badge top-left; None = the style's default spot
    frame_shift: int = 0             # classic: px to move the background up (+) or down (-) so the product clears the text
    style: str = "bold"
    niche: str = "umum"               # bold: accent colour, same niches as tools/bold_theme.py
    tags: tuple = ()                 # cute: up to 2 pink fact tags beside the product, e.g. ("30ml", "Dijamin\nhalal")
    product_crop: tuple = None       # cute: (x, y, w, h) of the 1080x1920 frame to keep, e.g. to drop most of a hand
    cutout: bool = True              # cute: cut the product out; False = show the frame as a rounded photo card
                                     # (for products the people-trained background model cannot separate)
    features: tuple = ()             # cute: up to 3 (icon, "line 1\nline 2") items for the bottom row; icons in promo/icons.py
    source: str = "assets/source-portrait.mp4"
    # --- post ---
    caption: str = ""                # first ~120 chars are what people see: hook + key fact + CTA
    hashtags: list = field(default_factory=list)

    def problems(self):
        out = []
        poses = tabby.POSES if self.character == "tabby" else tuple(POSE_SPECS)
        if self.pose not in poses:
            out.append(f"unknown pose {self.pose!r}; choose from {list(poses)}")
        if self.character == "tabby" and self.style != "bold":
            out.append("the tabby Oyen is only drawn on bold covers")
        if not 1 <= len(self.headline) <= 3:
            out.append("headline needs 1-3 lines")
        for line in self.headline:
            if len(line.replace("*", "")) > HEADLINE_MAX:
                out.append(f"headline line {line!r} is over {HEADLINE_MAX} chars; split it")
        if self.style not in STYLES:
            out.append(f"unknown style {self.style!r}; choose from {STYLES}")
        if self.style == "bold" and niche_colours(self.niche) is None:
            out.append(f"unknown niche {self.niche!r}; see tools/bold_theme.py NICHES")
        if len(self.tags) > 2:
            out.append("at most 2 tags")
        for tag in self.tags:
            lines = tag.split("\n")
            if len(lines) > 2 or any(len(line) > TAG_MAX for line in lines):
                out.append(f"tag {tag!r} needs <= 2 lines of <= {TAG_MAX} chars")
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
