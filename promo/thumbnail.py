"""Cover thumbnail: a one-frame HyperFrames project rendered with `snapshot`.

Layout respects both TikTok crops: the full 9:16 cover, and the 3:4 centre
crop used in profile grids (y 240-1680), so headline and Oyen stay inside it.
"""
import html
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

from oyen import character as C
from oyen.palette import INK, PAPER
from oyen.render import svg_rects

REPO = Path(__file__).resolve().parent.parent
HF = "hyperframes@0.8.150"
SCALE = 18  # Oyen is bigger on the cover than in the video


def _headline_html(lines):
    out = []
    for line in lines:
        parts = re.split(r"(\*[^*]+\*)", html.escape(line))
        spans = "".join(f'<span class="hl">{p[1:-1]}</span>' if p.startswith("*") else p for p in parts if p)
        n = len(line.replace("*", ""))
        size = min(132, int(960 / (max(n, 1) * 0.75)))  # Archivo Black caps ≈ 0.75em wide
        out.append(f'<div class="line" style="font-size: {size}px">{spans}</div>')
    return "\n          ".join(out)


def build_html(p):
    if p.style == "cute":
        from .cute import build_html as cute_html
        return cute_html(p)
    return _classic_html(p)


def _classic_html(p):
    oyen = svg_rects(C.POSES[p.pose])
    bx, by = p.badge_xy or (770, 1400)
    bubble = (f'<div id="bubble">{html.escape(p.bubble)}</div>' if p.bubble else "")
    badge = (f'<div id="badge"><span>{html.escape(p.badge)}</span></div>' if p.badge else "")
    # Space Mono is ~0.6em per glyph: shrink long bubbles so they stay on one line inside the box
    bubble_room = 1040 - C.CW * SCALE - 30 - 60
    bubble_size = min(44, int(bubble_room / (0.6 * max(len(p.bubble or ""), 1))))
    # + shift: background moves up and is enlarged to keep the bottom filled; - shift: it moves down
    # Archivo Black caps are ~0.8em wide: fit the longest badge word inside the 220px disc
    badge_size = min(50, int(220 / (0.8 * max((len(w) for w in (p.badge or "x").split()), default=1))))
    bg_height = 1920 + max(p.frame_shift, 0)
    # a frame moved down leaves a gap at the top: fade it into the backdrop instead of a hard edge
    bg_fade = (f"-webkit-mask-image: linear-gradient(180deg, transparent 0, #000 {min(-p.frame_shift, 260)}px);"
               if p.frame_shift < 0 else "")
    return f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #07080a; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: Montserrat, sans-serif;
        background: radial-gradient(ellipse 80% 30% at 50% 12%, rgba(255, 214, 10, 0.16), transparent 70%), #0b0d10; }}
      #bg {{ position: absolute; left: 0; top: {-p.frame_shift}px; width: 1080px; height: {bg_height}px; object-fit: cover; {bg_fade} }}
      #shade-top {{ position: absolute; left: 0; top: 0; width: 1080px; height: 900px;
        background: linear-gradient(180deg, rgba(7,8,10,0.92) 0%, rgba(7,8,10,0.75) 45%, rgba(7,8,10,0) 100%); }}
      #shade-bot {{ position: absolute; left: 0; top: 1300px; width: 1080px; height: 620px;
        background: linear-gradient(0deg, rgba(7,8,10,0.85), rgba(7,8,10,0)); }}
      #text {{ position: absolute; left: 50px; top: 300px; width: 980px; height: 560px;
        display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }}
      .kick {{ font-weight: 900; font-size: 58px; letter-spacing: 0.06em; color: #fff;
        text-shadow: 0 4px 18px rgba(0,0,0,0.8); margin-bottom: 14px; }}
      .line {{ font-family: "Archivo Black", sans-serif; font-size: 132px; line-height: 1.02; color: #fff;
        text-shadow: 0 8px 0 rgba(0,0,0,0.6), 0 12px 34px rgba(0,0,0,0.7); }}
      .hl {{ color: #ffd60a; }}
      #badge {{ position: absolute; left: {bx}px; top: {by}px; width: 270px; height: 270px; border-radius: 135px;
        background: #ffd60a; border: 10px solid {INK}; transform: rotate(-10deg);
        display: flex; align-items: center; justify-content: center; text-align: center;
        box-shadow: 12px 12px 0 rgba(0,0,0,0.45); }}
      #badge span {{ font-family: "Archivo Black", sans-serif; font-size: {badge_size}px; line-height: 1.0; color: {INK}; width: 220px; }}
      #oyen {{ position: absolute; left: 20px; top: {1640 - C.CH * SCALE}px; width: {C.CW * SCALE}px; height: {C.CH * SCALE}px; }}
      #oyen svg {{ display: block; filter: drop-shadow(10px 10px 0 rgba(0,0,0,0.5)); }}
      #bubble {{ position: absolute; left: {20 + C.CW * SCALE + 10}px; top: {1640 - C.CH * SCALE + 70}px;
        max-width: {1040 - C.CW * SCALE - 30}px; padding: 24px 30px; background: {PAPER};
        font-family: "Space Mono", monospace; font-weight: 700; font-size: {bubble_size}px; color: {INK}; white-space: nowrap;
        box-shadow: 0 -8px 0 0 {INK}, 0 8px 0 0 {INK}, -8px 0 0 0 {INK}, 8px 0 0 0 {INK}, 14px 14px 0 0 rgba(0,0,0,0.35); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-width="1080" data-height="1920">
      <img id="bg" src="frame.png" alt="" />
      <div id="shade-top"></div>
      <div id="shade-bot"></div>
      <div id="text">
          <div class="kick">{html.escape(p.kicker)}</div>
          {_headline_html(p.headline)}
      </div>
      {badge}
      <div id="oyen"><svg width="{C.CW * SCALE}" height="{C.CH * SCALE}" viewBox="0 0 {C.CW} {C.CH}" shape-rendering="crispEdges">{oyen}</svg></div>
      {bubble}
    </div>
    <script>
      window.__timelines["cover"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


OUTLINE = 9        # px: white sticker outline around the cut-out product, at cover size
PRODUCT_FIT = 760  # px: the cute cover fits the product into this square (see cute.py #product)
EDGE_FADE = 180  # px: whatever the cut-out keeps at a crop/frame edge (a wrist, a hand) fades out instead of ending in a straight line


def _edge_fade(alpha):
    """Mask that fades the sides the subject touches; sides it doesn't touch stay untouched."""
    w, h = alpha.size
    down = Image.linear_gradient("L")      # black at the top -> white at the bottom
    left = down.rotate(90)                 # black at the left
    mask = Image.new("L", alpha.size, 255)
    sides = {
        "left": ((0, 0, 2, h), left.resize((EDGE_FADE, h)), (0, 0)),
        "right": ((w - 2, 0, w, h), left.transpose(Image.FLIP_LEFT_RIGHT).resize((EDGE_FADE, h)), (w - EDGE_FADE, 0)),
        "top": ((0, 0, w, 2), down.resize((w, EDGE_FADE)), (0, 0)),
        "bottom": ((0, h - 2, w, h), down.transpose(Image.FLIP_TOP_BOTTOM).resize((w, EDGE_FADE)), (0, h - EDGE_FADE)),
    }
    for edge, strip, at in sides.values():
        if alpha.crop(edge).getextrema()[1] > 24:
            band = Image.new("L", alpha.size, 255)
            band.paste(strip, at)
            mask = ImageChops.darker(mask, band)
    return mask


def _pad(img, pad, edge=False):
    """Grow img by pad px per side: transparent/black, or (edge=True) repeating its border pixels."""
    w, h = img.size
    out = Image.new(img.mode, (w + 2 * pad, h + 2 * pad))
    out.paste(img, (pad, pad))
    if edge:
        out.paste(img.crop((0, 0, w, 1)).resize((w, pad)), (pad, 0))
        out.paste(img.crop((0, h - 1, w, h)).resize((w, pad)), (pad, h + pad))
        out.paste(out.crop((pad, 0, pad + 1, h + 2 * pad)).resize((pad, h + 2 * pad)), (0, 0))
        out.paste(out.crop((w + pad - 1, 0, w + pad, h + 2 * pad)).resize((pad, h + 2 * pad)), (w + pad, 0))
    return out


def _cut_out(frame, out, crop=None):
    """Remove the frame's background (HyperFrames' local model), crop to the product and give it a white
    sticker outline. The outline is baked in here, not drawn in CSS, so it fades out with a cut-off hand too."""
    raw = out.with_name("cut-raw.png")
    subprocess.run(["npx", "--yes", HF, "remove-background", str(frame), "-o", str(raw)],
                   check=True, capture_output=True, text=True)
    im = Image.open(raw).convert("RGBA")
    raw.unlink()
    if crop:
        x, y, w, h = crop
        im = im.crop((x, y, x + w, y + h))
    alpha = im.getchannel("A")
    box = alpha.point(lambda a: 255 if a > 24 else 0).getbbox()
    if not box:
        raise RuntimeError(f"background removal found no product in {frame}")
    fade = _edge_fade(alpha)
    # outline width in source px so it shows ~OUTLINE px once the product is fitted into the cover
    grow = round(OUTLINE / min(PRODUCT_FIT / (box[2] - box[0]), PRODUCT_FIT / (box[3] - box[1]), 1))
    pad = grow * 2
    im, alpha, fade = _pad(im, pad), _pad(alpha, pad), _pad(fade, pad, edge=True)
    hard = alpha.point(lambda a: 255 if a > 128 else 0)
    ring = hard.filter(ImageFilter.GaussianBlur(grow / 2)).point(lambda a: 255 if a > 8 else 0)
    sticker = Image.new("RGBA", im.size, (255, 255, 255, 0))
    sticker.putalpha(ImageChops.multiply(ring.filter(ImageFilter.GaussianBlur(1.2)), fade))
    im.putalpha(ImageChops.multiply(alpha, fade))
    sticker.alpha_composite(im)
    sticker.crop(sticker.getchannel("A").point(lambda a: 255 if a > 24 else 0).getbbox()).save(out)


def render(promo, video_dir, out_dir):
    """Build the cover project in out_dir/_cover and snapshot it to out_dir/thumbnail.png."""
    video_dir, out_dir = Path(video_dir), Path(out_dir)
    work = out_dir / "_cover"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    src = video_dir / promo.source
    if not src.exists():
        raise FileNotFoundError(f"{src} not found; the cover background comes from the footage")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(promo.frame_src), "-i", str(src), "-frames:v", "1",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                    str(work / "frame.png")], check=True)
    if promo.style == "cute":
        _cut_out(work / "frame.png", work / "product.png", promo.product_crop)
    shutil.copy2(REPO / "shared" / "vendor" / "gsap.min.js", work / "gsap.min.js")
    page = build_html(promo).replace("<style>", '<script src="gsap.min.js"></script>\n    <style>', 1)
    (work / "index.html").write_text(page)
    (work / "hyperframes.json").write_text('{"paths": {"assets": "."}}\n')
    subprocess.run(["npx", "--yes", HF, "snapshot", "--at", "0", "--no-end", "-o", "shots"],
                   cwd=work, check=True, capture_output=True, text=True)
    shot = next((work / "shots").glob("frame-00-*.png"))
    out = out_dir / "thumbnail.png"
    shutil.copy2(shot, out)
    shutil.rmtree(work)
    return out
