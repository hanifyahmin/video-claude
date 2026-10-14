"""Oyen (Chibi) — the chosen mascot, split into animation layers.

python3 oyen_chibi.py svg   -> prints the <svg id="cat-svg"> block for index.html
python3 oyen_chibi.py png D -> writes oyen-chibi-uu.png and oyen-chibi-poses.png into D
"""
import sys
from pathlib import Path

from oyen_sprites import PAL

# head + body only; eyes, mouth, right paw and tail live in layers below
BASE = [
    "...KK..........KK...",
    "..KOOK........KOOK..",
    "..KOPOK......KOPOK..",
    ".KOOPPOKKKKKKOPPOOK.",
    ".KOOOOOODDDDOOOOOOK.",
    "KOOOOOOOODDOOOOOOOOK",
    "KOOOOOOOOOOOOOOOOOOK",
    "KOOOOOOOOOOOOOOOOOOK",
    "KOOOOOOOOOOOOOOOOOOK",
    "KOBBOOOOOPPOOOOOBBOK",
    "KOOOOOOOOOOOOOOOOOOK",
    ".KOOOOOOOOOOOOOOOOK.",
    ".KOOOOOOOOOOOOOOOOK.",
    "..KKOOOOOOOOOOOOKK..",
    "....KOOOLLLLOOOK....",
    "....KOOLLLLLLOOK....",
    "....KOOLLLLLLOOK....",
    "....KOOLLLLLLOOK....",
    "....KOOKLLLLKLLK....",
    ".....KK.KKKK.KK.....",
]

EYES_OPEN = [(6, 3, "W"), (6, 4, "E"), (6, 5, "E"), (6, 14, "W"), (6, 15, "E"), (6, 16, "E")] + [
    (r, c, "E") for r in (7, 8) for c in (3, 4, 5, 14, 15, 16)]
EYES_SHUT = [(7, c, "K") for c in (3, 4, 5, 14, 15, 16)]
# "uu" / ω mouth hanging off the nose: \_/\_/
MOUTH_SHUT = [(10, 6, "K"), (10, 9, "K"), (10, 10, "K"), (10, 13, "K"),
              (11, 7, "K"), (11, 8, "K"), (11, 11, "K"), (11, 12, "K")]
# talking: same corners, little open mouth with a tongue
MOUTH_OPEN = [(10, 6, "K"), (10, 13, "K"), (10, 8, "K"), (10, 9, "E"), (10, 10, "E"), (10, 11, "K"),
              (11, 7, "K"), (11, 8, "K"), (11, 9, "P"), (11, 10, "P"), (11, 11, "K"), (11, 12, "K"),
              (12, 9, "K"), (12, 10, "K")]
PAW_DOWN = [(18, 5, "L"), (18, 6, "L")]
PAW_UP = [(18, 5, "O"), (18, 6, "O"),
          (12, 2, "K"), (12, 3, "K"), (13, 1, "K"), (13, 2, "L"), (13, 3, "L"), (13, 4, "K"),
          (14, 1, "K"), (14, 2, "L"), (14, 3, "L"), (14, 4, "K"), (15, 2, "K"), (15, 3, "O"), (15, 4, "K"),
          (16, 3, "K"), (16, 4, "O"), (17, 4, "K")]
TAIL_A = [(15, 17, "K"), (15, 18, "K"), (16, 16, "K"), (16, 17, "O"), (16, 18, "K"),
          (17, 16, "O"), (17, 17, "K"), (18, 16, "K")]
TAIL_B = [(16, 17, "K"), (16, 18, "K"), (17, 16, "O"), (17, 17, "O"), (17, 18, "O"), (17, 19, "K"),
          (18, 16, "K"), (18, 17, "K"), (18, 18, "K")]

W, H = 20, 20


def _hex(k):
    return "#%02x%02x%02x" % PAL[k]


def rects(cells):
    return "".join(f'<rect x="{c}" y="{r}" width="1" height="1" fill="{_hex(k)}"/>' for r, c, k in cells)


def svg(size=280):
    base = [(r, c, ch) for r, row in enumerate(BASE) for c, ch in enumerate(row) if ch != "."]
    g = lambda gid, cells, on: f'<g id="{gid}"{"" if on else " opacity=\"0\""}>{rects(cells)}</g>'
    return (f'<svg id="cat-svg" width="{size}" height="{size}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges">'
            f'<g>{rects(base)}</g>'
            + g("cat-tail-a", TAIL_A, True) + g("cat-tail-b", TAIL_B, False)
            + g("cat-eyes-open", EYES_OPEN, True) + g("cat-eyes-shut", EYES_SHUT, False)
            + g("cat-mouth-shut", MOUTH_SHUT, True) + g("cat-mouth-open", MOUTH_OPEN, False)
            + g("cat-paw-down", PAW_DOWN, True) + g("cat-paw-up", PAW_UP, False)
            + "</svg>")


def pose(*layers):
    grid = [list(r) for r in BASE]
    for cells in layers:
        for r, c, k in cells:
            grid[r][c] = k
    return ["".join(r) for r in grid]


if __name__ == "__main__":
    assert all(len(r) == W for r in BASE) and len(BASE) == H
    if sys.argv[1] == "svg":
        print(svg())
    else:
        from PIL import Image, ImageDraw, ImageFont
        from oyen_sprites import to_image
        out = Path(sys.argv[2])
        idle = pose(TAIL_A, EYES_OPEN, MOUTH_SHUT, PAW_DOWN)
        to_image(idle, 16).save(out / "oyen-chibi-uu.png")
        poses = [("Senyum uu", idle),
                 ("Bercakap", pose(TAIL_A, EYES_OPEN, MOUTH_OPEN, PAW_DOWN)),
                 ("Kelip mata", pose(TAIL_B, EYES_SHUT, MOUTH_SHUT, PAW_DOWN)),
                 ("Melambai", pose(TAIL_B, EYES_OPEN, MOUTH_OPEN, PAW_UP))]
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        cw, ch, pad = 400, 470, 30
        sheet = Image.new("RGB", (pad + 4 * (cw + pad), ch + 2 * pad), (17, 19, 24))
        d = ImageDraw.Draw(sheet)
        for i, (name, rows) in enumerate(poses):
            spr = to_image(rows, 16)
            x0, y0 = pad + i * (cw + pad), pad
            d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=28, fill=(255, 248, 235))
            sx, sy = x0 + (cw - spr.width) // 2, y0 + 30
            sh = Image.new("RGBA", spr.size, (0, 0, 0, 0))
            sh.putalpha(spr.getchannel("A").point(lambda a: 70 if a else 0))
            sheet.paste((0, 0, 0), (sx + 10, sy + 10), sh)
            sheet.paste(spr, (sx, sy), spr)
            tw = d.textlength(name, font=font)
            d.text((x0 + (cw - tw) / 2, y0 + ch - 70), name, font=font, fill=(42, 22, 11))
        sheet.save(out / "oyen-chibi-poses.png")
        print(out / "oyen-chibi-poses.png")
