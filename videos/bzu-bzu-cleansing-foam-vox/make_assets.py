"""Collage materials for the Vox-style edit of BZU BZU Cleansing Foam.

  python3 videos/bzu-bzu-cleansing-foam-vox/make_assets.py   (from the repo root)

-> assets/: paper texture, masking tape, a torn paper edge, photo prints cut from the footage
(stills; the edit plays the same moments as video inside the prints) and two cut-outs
(hands + bottle) made with `hyperframes remove-background`.
"""
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
A = HERE / "assets"
SOURCE = A / "source-portrait.mp4"

# (name, second, crop box on the 1080x1920 frame)
PRINTS = [
    ("dirty", 66.5, (0, 330, 1080, 1530)),     # milk residue in the bottle
    ("clean", 70.8, (0, 300, 1080, 1500)),     # the same bottle washed
    ("front", 16.4, (60, 120, 1020, 1760)),    # front label
    ("back", 7.0, (100, 150, 1000, 1480)),     # back label: claims + washing directions
    ("zero", 16.4, (120, 980, 980, 1250)),     # the 0% box
]
CUTOUTS = [("hand-pump", 32.6), ("bottle-clean", 70.8)]


def frame(t, path):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(SOURCE), "-frames:v", "1", str(path)],
                   check=True)


def paper(w=1080, h=1920, seed=4):
    """Warm newsprint: soft blotches, fine grain and a few fibres."""
    rng = np.random.default_rng(seed)
    base = np.array([241, 236, 226], float)
    low = Image.fromarray((rng.random((h // 60, w // 60)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    low = (np.asarray(low, float) / 255 - 0.5) * 14
    fine = rng.normal(0, 5, (h, w))
    img = base[None, None, :] + (low + fine)[..., None]
    fib = Image.new("L", (w, h), 0)
    px = fib.load()
    for _ in range(900):
        x, y = rng.integers(0, w), rng.integers(0, h)
        dx, dy = rng.normal(0, 1, 2)
        for k in range(int(rng.integers(8, 30))):
            xx, yy = int(x + dx * k), int(y + dy * k)
            if 0 <= xx < w and 0 <= yy < h:
                px[xx, yy] = 22
    img -= np.asarray(fib.filter(ImageFilter.GaussianBlur(0.6)), float)[..., None] * 0.5
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def tape(w=230, h=64, seed=1):
    rng = np.random.default_rng(seed)
    a = np.full((h, w), 190, np.uint8)
    for x in range(10):                       # torn ends
        a[:, x][rng.random(h) < (10 - x) / 10] = 0
        a[:, w - 1 - x][rng.random(h) < (10 - x) / 10] = 0
    rgb = np.dstack([np.full((h, w), c, np.uint8) for c in (236, 224, 186)])
    rgb = np.clip(rgb.astype(int) + rng.normal(0, 4, (h, w, 1)).astype(int), 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb, a]), "RGBA")


def torn_edge(w=1080, h=90, seed=2):
    """White paper strip whose bottom edge is torn (for paper-rip transitions)."""
    rng = np.random.default_rng(seed)
    edge = np.cumsum(rng.normal(0, 3, w))
    edge = 50 + (edge - np.convolve(edge, np.ones(60) / 60, "same")) * 1.4
    a = np.zeros((h, w), np.uint8)
    for x in range(w):
        a[: int(np.clip(edge[x], 20, h - 4)), x] = 255
    rgb = np.dstack([np.full((h, w), c, np.uint8) for c in (250, 248, 243)])
    return Image.fromarray(np.dstack([rgb, a]), "RGBA")


def main():
    A.mkdir(exist_ok=True)
    paper().save(A / "paper.jpg", quality=90)
    tape().save(A / "tape.png")
    torn_edge().save(A / "torn.png")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, t, box in PRINTS:
            f = tmp / f"{name}.png"
            frame(t, f)
            im = Image.open(f).convert("RGB").crop(box)
            ImageEnhance.Contrast(im).enhance(1.05).save(A / f"print-{name}.jpg", quality=88)
        for name, t in CUTOUTS:
            f = tmp / f"{name}.png"
            frame(t, f)
            out = A / f"cut-{name}.png"
            subprocess.run(["npx", "--yes", "hyperframes@0.8.150", "remove-background", str(f), "-o", str(out)],
                           check=True, capture_output=True)
            im = Image.open(out)
            im.crop(im.getbbox()).save(out)
    print("assets ->", A)


if __name__ == "__main__":
    main()
