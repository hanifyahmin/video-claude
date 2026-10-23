"""Pixel objects for the archive edit of BZU BZU Cleansing Foam.

  python3 videos/bzu-bzu-cleansing-foam-archive/make_pixels.py   (from the repo root)

-> assets/px/: the product as a pixel object (label pixelated from a footage frame, pump drawn
by hand: no shot shows the whole bottle with its pump), the shared icons with voxel depth,
Oyen as one of the objects, and ink blots. All 1 art px = 1 image px; scale with
`image-rendering: pixelated`.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO))
import pixel_icons as P  # noqa: E402
from oyen import tabby  # noqa: E402

OUT = HERE / "assets" / "px"
SOURCE = HERE / "assets" / "source-portrait.mp4"
LABEL_AT = 16.4                     # steady front-label frame
LABEL_BOX = (130, 200, 960, 1640)   # label on that frame (x0, y0, x1, y1)
INK = (43, 32, 36, 255)

W, H = 40, 78


def _frame(t):
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "f.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(SOURCE), "-frames:v", "1", str(f)],
                       check=True)
        return Image.open(f).convert("RGB")


def _rounded(w, h, r):
    m = np.zeros((h, w), bool)
    for y in range(h):
        for x in range(w):
            dx = max(r - x, 0, x - (w - 1 - r))
            dy = max(r - y, 0, y - (h - 1 - r))
            m[y, x] = dx * dx + dy * dy <= r * r
    return m


def product():
    """The foam bottle: pump head + collar drawn, body tinted like the liquid, label from the footage."""
    rgba = np.zeros((H, W, 4), np.uint8)

    def fill(mask, colour, x0=0, y0=0):
        h, w = mask.shape
        region = rgba[y0:y0 + h, x0:x0 + w]
        region[mask] = colour

    white, grey, shade = (250, 250, 247, 255), (214, 214, 208, 255), (168, 168, 160, 255)
    fill(np.ones((7, 10), bool), white, 15, 1)            # pump head
    fill(np.ones((3, 9), bool), white, 25, 2)             # nozzle
    rgba[1:8, 23] = grey
    rgba[4, 25:34] = grey
    fill(np.ones((4, 18), bool), grey, 11, 8)             # collar
    rgba[8:12, 27:29] = shade
    for i, y in enumerate(range(12, 16)):                 # shoulder widening into the body
        x0 = 10 - 2 * i - 1
        rgba[y, x0:W - x0] = (240, 226, 168, 255)
    body = _rounded(36, 62, 6)
    liquid = np.zeros((62, 36, 4), np.uint8)
    liquid[body] = (240, 226, 168, 255)
    liquid[:, :3][body[:, :3]] = (252, 246, 214, 255)     # light catch on the left
    liquid[:, -3:][body[:, -3:]] = (204, 184, 118, 255)   # shade on the right
    sub = rgba[15:77, 2:38]
    sub[body] = liquid[body]

    src = _frame(LABEL_AT).crop(LABEL_BOX)
    src = ImageEnhance.Color(ImageEnhance.Contrast(src).enhance(1.35)).enhance(1.5).filter(ImageFilter.SHARPEN)
    label = src.resize((28, 48), Image.LANCZOS)
    label = label.quantize(colors=20, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    lab = np.asarray(label)
    lmask = _rounded(28, 48, 3)
    rgba[21:69, 6:34][lmask] = np.dstack([lab, np.full((48, 28), 255, np.uint8)])[lmask]

    im = Image.fromarray(rgba, "RGBA")
    out = Image.new("RGBA", (W + 2, H + 2), (0, 0, 0, 0))   # 1px ink outline around the silhouette
    a = np.asarray(im)[..., 3] > 0
    pad = np.pad(a, 1)
    ring = np.zeros_like(pad)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        ring |= np.roll(pad, (dy, dx), (0, 1))
    ring &= ~pad
    o = np.zeros((H + 2, W + 2, 4), np.uint8)
    o[ring] = INK
    out = Image.fromarray(o, "RGBA")
    out.alpha_composite(im, (1, 1))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prod = product()
    prod.save(OUT / "product.png")
    P.extrude(prod, 3).save(OUT / "product-3d.png")
    for name, g in P.grids().items():
        P.extrude(P.render(g), 2).save(OUT / f"{name}.png")
    P.extrude(tabby.trimmed("Duduk"), 2).save(OUT / "oyen.png")
    for i in range(3):
        P.blob(24, seed=i).save(OUT / f"blob{i}.png")
    print("pixel objects ->", OUT)


if __name__ == "__main__":
    main()
