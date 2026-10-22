"""Oyen v2, the tabby: frame-by-frame pixel-art animations from a packed sprite sheet.

oyen-tabby.png / oyen-tabby.json are built by `tools/oyen_from_flow.py` from Google Flow
reference sheets (see README.md here). A storyline with `character="tabby"` uses the
animation names below as its poses; the installer turns each beat into a schedule of
sprite-frame switches (`frames_for`), so playback is seek-safe like the chibi's.
"""
import json
from functools import lru_cache
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHEET = HERE / "oyen-tabby.png"

# on-screen placement in the 1080x1920 video (bottom-left, clear of TikTok's caption area)
SCALE = 6            # screen px per art px (a standing cat is 48 art px: 288px)
ANCHOR_X = 300       # x of the cell's right edge: the cat faces right, its head sits here
GROUND = 1560        # y of the cell floor


@lru_cache(maxsize=1)
def meta():
    return json.loads((HERE / "oyen-tabby.json").read_text())


def anims():
    return meta()["anims"]


POSES = tuple(meta()["anims"])


def cell():
    return tuple(meta()["cell"])


def frame_xy(anim, n):
    """Sheet position of frame n (1-based) of an animation."""
    return tuple(meta()["frames"][anims()[anim]["frames"][n - 1]])


def key_frame(anim):
    return anims()[anim].get("key", 1)


@lru_cache(maxsize=None)
def frame_image(anim, n=None, scale=1):
    """One frame as an RGBA image (cell-sized, cat right-aligned on the floor)."""
    n = n or key_frame(anim)
    x, y = frame_xy(anim, n)
    w, h = cell()
    im = Image.open(SHEET).convert("RGBA").crop((x, y, x + w, y + h))
    return im.resize((w * scale, h * scale), Image.NEAREST) if scale != 1 else im


def trimmed(anim, n=None, scale=1):
    """frame_image cropped to the cat."""
    im = frame_image(anim, n, scale)
    return im.crop(im.getbbox())


def frames_for(anim, start, end, talk=None, blinks=()):
    """[(time, frame number)] switches for a beat; the first entry is at `start`.

    talk: (t0, t1) while a speech line types; a pose with a `talk` animation flaps it then.
    blinks: times inside the beat; a pose with a `blink` frame shows it for 0.12s.
    """
    spec = anims()[anim]
    out = []
    t, i = start, 0
    seq = spec["seq"]
    while t < end - 1e-6:
        n, dur = seq[i]
        out.append((round(t, 3), n))
        t += dur
        i += 1
        if i == len(seq):
            if not spec.get("loop"):
                break
            i = 0
    if talk and spec.get("talk"):
        t0, t1 = max(talk[0], start), min(talk[1], end)
        tseq = anims()[spec["talk"]]["seq"]
        flaps, t, j = [], t0, 0
        while t < t1 - 1e-6:
            flaps.append((round(t, 3), ("talk", tseq[j][0])))
            t += tseq[j][1]
            j = (j + 1) % len(tseq)
        before = [f for f in out if f[0] < t0]
        after = [f for f in out if f[0] >= t1]
        resume = before[-1][1] if before else seq[0][0]
        out = before + flaps + [(round(t1, 3), resume)] + [f for f in after if f[0] > t1]
    for b in blinks:
        if spec.get("blink") and start <= b < end - 0.15:
            current = [f for f in out if f[0] <= b][-1][1]
            if current == seq[0][0]:  # only blink from the resting frame
                out += [(round(b, 3), spec["blink"]), (round(b + 0.12, 3), current)]
    return sorted(out, key=lambda f: f[0])


def resolve(anim, n):
    """Frame number or ("talk", n) -> (anim, n)."""
    if isinstance(n, tuple):
        return anims()[anim]["talk"], n[1]
    return anim, n
