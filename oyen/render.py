"""Turn sprite rows into PNGs (for sheets/storyboards) or SVG rects (for video)."""
from pathlib import Path

from PIL import Image, ImageFont

from .palette import PAL, hexc

_FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(size, mono=False):
    name = "DejaVuSansMono-Bold.ttf" if mono else "DejaVuSans-Bold.ttf"
    try:
        return ImageFont.truetype(str(_FONT_DIR / name), size)
    except OSError:
        return ImageFont.load_default(size)


def to_image(rows, scale):
    """Sprite rows -> RGBA image, nearest-neighbour scaled."""
    w = max(len(r) for r in rows)
    img = Image.new("RGBA", (w, len(rows)), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                img.putpixel((x, y), PAL[ch] + (255,))
    return img.resize((w * scale, len(rows) * scale), Image.NEAREST)


def paste_with_shadow(canvas, sprite, xy, offset=8, alpha=60):
    """Paste a sprite with a hard pixel drop shadow."""
    x, y = xy
    shadow = Image.new("RGBA", sprite.size, (0, 0, 0, 0))
    shadow.putalpha(sprite.getchannel("A").point(lambda a: alpha if a else 0))
    canvas.paste((0, 0, 0), (x + offset, y + offset), shadow)
    canvas.paste(sprite, (x, y), sprite)


def svg_rects(rows):
    """Sprite rows -> SVG <rect>s, one per horizontal run of a colour."""
    out = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            k = row[x]
            if k == ".":
                x += 1
                continue
            x2 = x
            while x2 < len(row) and row[x2] == k:
                x2 += 1
            out.append(f'<rect x="{x}" y="{y}" width="{x2 - x}" height="1" fill="{hexc(k)}"/>')
            x = x2
    return "".join(out)
