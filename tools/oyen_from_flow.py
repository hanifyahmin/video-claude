#!/usr/bin/env python3
"""Build Oyen's tabby sprite sheet from Google Flow (Nano Banana) reference sheets.

  python3 tools/oyen_from_flow.py <dir with the Flow .jpg files>

Each Flow image is one animation: one row of frames, facing right, on a flat background
(see the prompt guide in oyen/tabby/README.md). oyen/tabby/sources.json maps each image to
an animation name, a size factor and the playback sequence. This tool cuts every frame out,
keeps only the cat (plus anything touching it, e.g. a bowl), rescales so the cat is the same
size in every animation, quantizes all frames to one shared palette and packs them into

  oyen/tabby/oyen-tabby.png   uniform cells, cat right-aligned, standing on the cell floor
  oyen/tabby/oyen-tabby.json  cell size, frame positions and the animations

Rerun it whenever a Flow image is added or replaced, then `python3 -m oyen poses`.
"""
import json
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "oyen" / "tabby"
STAND_PX = 48        # art pixels from the ground to the ear tips of a standing cat
PALETTE = 20         # shared colours across all frames
COLS = 8             # cells per row in the packed sheet


def components(mask):
    """Label 4-connected regions; returns (labels, sizes) with sizes[0] unused."""
    h, w = mask.shape
    lab = np.zeros((h, w), int)
    sizes = [0]
    for y, x in zip(*np.nonzero(mask)):
        if lab[y, x]:
            continue
        n = len(sizes)
        sizes.append(0)
        lab[y, x] = n
        todo = deque([(y, x)])
        while todo:
            cy, cx = todo.popleft()
            sizes[n] += 1
            for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = n
                    todo.append((ny, nx))
    return lab, sizes


def cut_frames(path):
    """Frames of one Flow sheet, left to right: [(RGBA crop, bottom y on the sheet)], plus the sheet's ground y."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    bg = np.median(np.concatenate([a[:20].reshape(-1, 3), a[-20:].reshape(-1, 3)]), axis=0)
    mask = Image.fromarray(((np.abs(a - bg).max(2) > 26) * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3))
    m = np.asarray(mask) > 127
    # find frames on a half-size grid; small pieces (a tail tip, a bowl) join the nearest frame
    small = np.asarray(mask.resize((m.shape[1] // 2, m.shape[0] // 2)).filter(ImageFilter.MaxFilter(3))) > 127
    lab, sizes = components(small)
    boxes = []
    for n in range(1, len(sizes)):
        ys, xs = np.nonzero(lab == n)
        boxes.append([xs.min() * 2, ys.min() * 2, xs.max() * 2 + 2, ys.max() * 2 + 2, sizes[n]])
    big = max(b[4] for b in boxes)
    main = [b for b in boxes if b[4] >= 0.2 * big]
    for b in boxes:
        if 15 < b[4] < 0.2 * big:
            cx = (b[0] + b[2]) / 2
            t = min(main, key=lambda m_: 0 if m_[0] <= cx <= m_[2] else min(abs(cx - m_[0]), abs(cx - m_[2])))
            t[:4] = [min(t[0], b[0]), min(t[1], b[1]), max(t[2], b[2]), max(t[3], b[3])]
    frames = []
    for x0, y0, x1, y1, _ in sorted(main, key=lambda b: b[0]):
        x0, y0, x1, y1 = max(x0 - 2, 0), max(y0 - 2, 0), min(x1 + 2, im.width), min(y1 + 2, im.height)
        crop = im.crop((x0, y0, x1, y1)).convert("RGBA")
        crop.putalpha(Image.fromarray((m[y0:y1, x0:x1] * 255).astype(np.uint8)))
        frames.append((crop, y1))
    return frames, max(y1 for _, y1 in frames)


def shrink(crop, k):
    """Premultiplied Lanczos resize (no dark fringes); returns (rgb uint8, alpha bool)."""
    w, h = max(1, round(crop.width * k)), max(1, round(crop.height * k))
    a = np.asarray(crop).astype(float) / 255
    a[..., :3] *= a[..., 3:4]
    s = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(float) / 255
    al = s[..., 3]
    rgb = np.where(al[..., None] > 0.01, s[..., :3] / np.maximum(al[..., None], 1e-3), 0)
    return np.clip(rgb * 255, 0, 255).astype(np.uint8), al > 0.5


def main_body(alpha):
    """Largest blob plus anything within 2px of it: drops bits of the neighbouring cat."""
    lab, sizes = components(alpha)
    big = int(np.argmax(sizes))
    near = np.asarray(Image.fromarray(((lab == big) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 127
    return np.isin(lab, list({big} | set(np.unique(lab[near & (lab > 0)]))))


def build(src_dir):
    sources = json.loads((OUT / "sources.json").read_text())
    frames = []        # dicts: anim, rgb, alpha, lift
    for anim, spec in sources["anims"].items():
        cut, ground = cut_frames(Path(src_dir) / spec["file"])
        k = spec["scale"] * STAND_PX / sources["stand_px_at_scale_1"]
        for crop, bottom in cut:
            rgb, al = shrink(crop, k)
            al = main_body(al)
            ys, xs = np.nonzero(al)
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            lift = round((ground - bottom) * k) + (al.shape[0] - y1)
            frames.append(dict(anim=anim, rgb=rgb[y0:y1, x0:x1], alpha=al[y0:y1, x0:x1], lift=int(lift)))
        print(f"{anim}: {len(cut)} frames from {spec['file']}")

    pix = np.concatenate([f["rgb"][f["alpha"]] for f in frames])
    pal = Image.fromarray(pix.reshape(1, -1, 3)).quantize(colors=PALETTE, method=Image.Quantize.MEDIANCUT)
    cw = max(f["rgb"].shape[1] for f in frames)
    ch = max(f["rgb"].shape[0] + f["lift"] for f in frames)
    rows = (len(frames) + COLS - 1) // COLS
    sheet = Image.new("RGBA", (COLS * cw, rows * ch), (0, 0, 0, 0))
    meta = {"cell": [cw, ch], "stand_px": STAND_PX, "frames": [], "anims": {}}
    for i, f in enumerate(frames):
        q = np.asarray(Image.fromarray(f["rgb"]).quantize(palette=pal, dither=Image.Dither.NONE).convert("RGB"))
        tile = Image.fromarray(np.dstack([q, f["alpha"].astype(np.uint8) * 255]), "RGBA")
        cx, cy = (i % COLS) * cw, (i // COLS) * ch
        # right-aligned (the cat faces right, so its head stays put) and standing on the cell floor
        sheet.alpha_composite(tile, (cx + cw - tile.width, cy + ch - tile.height - f["lift"]))
        meta["frames"].append([cx, cy])
    i = 0
    for anim, spec in sources["anims"].items():
        n = sum(1 for f in frames if f["anim"] == anim)
        meta["anims"][anim] = {"frames": list(range(i, i + n)), **{k: v for k, v in spec.items()
                                                                    if k in ("seq", "loop", "blink", "talk", "key", "move")}}
        i += n
    sheet.save(OUT / "oyen-tabby.png")
    (OUT / "oyen-tabby.json").write_text(json.dumps(meta, indent=1) + "\n")
    print(f"{len(frames)} frames, cell {cw}x{ch} -> {OUT / 'oyen-tabby.png'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    build(sys.argv[1])
