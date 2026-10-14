"""Oyen (Chibi) in many poses. Run: python3 oyen_poses.py <outdir>

Every pose is built on a 26x24 canvas from the chibi head (20x14, drawn at
x=3, y=3) and body, then stamped with eye / mouth / limb / prop overlays,
so the character stays identical across poses.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from oyen_sprites import PAL, to_image

CW, CH = 26, 24
HX, HY = 3, 3  # where the head's (0,0) lands on the canvas

HEAD = [
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
]
BODY = [  # head-space rows 14..19
    "....KOOOLLLLOOOK....",
    "....KOOLLLLLLOOK....",
    "....KOOLLLLLLOOK....",
    "....KOOLLLLLLOOK....",
    "....KLLKLLLLKLLK....",
    ".....KK.KKKK.KK.....",
]
TAIL = [(15, 17, "K"), (15, 18, "K"), (16, 16, "K"), (16, 17, "O"), (16, 18, "K"),
        (17, 16, "O"), (17, 17, "K"), (18, 16, "K")]

# ---- faces (head-space coordinates) ----
L_EYE, R_EYE = (3, 4, 5), (14, 15, 16)


def eyes_open(cols=L_EYE + R_EYE):
    cells = [(r, c, "E") for r in (6, 7, 8) for c in cols]
    for side in (L_EYE, R_EYE):
        if side[0] in cols:
            cells.append((6, side[0], "W"))
    return cells


def eyes_happy(cols=(L_EYE, R_EYE)):  # ^ ^
    out = []
    for a, b, c in cols:
        out += [(6, b, "K"), (7, a, "K"), (7, c, "K")]
    return out


def eyes_sleep():  # closed, sleepy  u u
    return [(8, c, "K") for c in (3, 4, 5, 14, 15, 16)]


def eyes_heart():
    out = []
    for a, b, c in (L_EYE, R_EYE):
        out += [(6, a, "R"), (6, c, "R"), (7, a, "R"), (7, b, "R"), (7, c, "R"), (8, b, "R")]
    return out


def eyes_shock():  # big white eyes, tiny pupils
    out = []
    for a, b, c in (L_EYE, R_EYE):
        out += [(r, x, "W") for r in (6, 7, 8) for x in (a, b, c)]
        out += [(7, b, "E")]
        out += [(5, a, "K"), (5, b, "K"), (5, c, "K")]  # raised brows
    return out


def eyes_sparkle():
    return eyes_open() + [(8, 5, "W"), (8, 16, "W")]


def eyes_think():  # looking up-right
    cells = [(r, c, "E") for r in (6, 7, 8) for c in L_EYE + R_EYE]
    return cells + [(6, 5, "W"), (6, 16, "W")]


MOUTH_UU = [(10, 6, "K"), (10, 9, "K"), (10, 10, "K"), (10, 13, "K"),
            (11, 7, "K"), (11, 8, "K"), (11, 11, "K"), (11, 12, "K")]
MOUTH_TALK = [(10, 6, "K"), (10, 13, "K"), (10, 8, "K"), (10, 9, "E"), (10, 10, "E"), (10, 11, "K"),
              (11, 7, "K"), (11, 8, "K"), (11, 9, "P"), (11, 10, "P"), (11, 11, "K"), (11, 12, "K"),
              (12, 9, "K"), (12, 10, "K")]
MOUTH_O = [(10, 9, "K"), (10, 10, "K"), (11, 8, "K"), (11, 9, "E"), (11, 10, "E"), (11, 11, "K"),
           (12, 9, "K"), (12, 10, "K")]
MOUTH_BIG = [(10, c, "K") for c in range(7, 13)] + [(11, 7, "K"), (11, 12, "K")] + \
            [(11, c, "E") for c in (8, 9, 10, 11)] + [(12, 8, "K"), (12, 11, "K"), (12, 9, "P"), (12, 10, "P"),
                                                      (13, 9, "K"), (13, 10, "K")]
MOUTH_SMALL = [(10, 9, "K"), (10, 10, "K")]
MOUTH_FLAT = [(11, 8, "K"), (11, 9, "K"), (11, 10, "K"), (11, 11, "K")]

# ---- limbs / props: (canvas_x, canvas_y, rows) stamps ----
PAW_WAVE = (22, 7, [
    ".KK.",
    "KLLK",
    "KLLK",
    "KOOK",
    ".KOK",
    ".KOK",
    ".KOK",
    "..KK",
])
WAVE_LINES = (22, 2, [
    "...K",
    "..K.",
    "....",
    ".K.K",
])
PAW_HOORAY_L = (0, 8, [
    ".KK.",
    "KLLK",
    "KLLK",
    "KOOK",
    "KOK.",
    "KOK.",
    "KOK.",
    "KK..",
])
PAW_HOORAY_R = (22, 8, [
    ".KK.",
    "KLLK",
    "KLLK",
    "KOOK",
    ".KOK",
    ".KOK",
    ".KOK",
    "..KK",
])
PAW_POINT = (18, 18, [
    "KKKKKK.",
    "OOOOLLK",
    "KKKKKK.",
])
PAW_CHIN = (15, 14, [
    ".KKK.",
    "KLLLK",
    "KLLLK",
    ".KOOK",
    "..KOK",
    "..KOK",
])
QMARK = (21, 0, [
    ".YYY.",
    "Y...Y",
    "...Y.",
    "..Y..",
    ".....",
    "..Y..",
])
BANG = (22, 0, [
    "YY",
    "YY",
    "YY",
    "YY",
    "..",
    "YY",
])
SWEAT = (2, 7, [
    ".N",
    "NN",
    "NN",
])
ZZZ = (19, 0, [
    "NNNN...",
    "..N....",
    ".N..NNN",
    "NNNN..N",
    ".....N.",
    "....NNN",
])
HEARTS = (20, 0, [
    ".R.R..",
    "RRRRR.",
    ".RRR..",
    "..R.R.",
    "...RRR",
    "....R.",
])
SPARKS = (0, 0, [
    "..Y...................W...",
    ".YYY.................WWW..",
    "..Y...................W...",
])
HEADPHONES = [  # band over the head between the ears + cups on the cheeks
    (6, 5, ["KKKKKKKKKKKKKK"]),
    (5, 6, ["KSSSSSSSSSSSSSSK"]),
    (4, 7, ["KSK", "KSK"]), (19, 7, ["KSK", "KSK"]),
    (2, 9, ["KKKK", "KGGK", "KGGK", "KGGK", "KKKK"]), (20, 9, ["KKKK", "KGGK", "KGGK", "KGGK", "KKKK"]),
]
NOTE = (23, 1, [
    ".NN",
    ".NN",
    ".N.",
    "NN.",
    "NN.",
])
BAG = (17, 15, [
    "...KKK...",
    "..K...K..",
    "KKKKKKKKK",
    "KYYYYYYYK",
    "KYYyYyYYK",
    "KYYYyYYYK",
    "KYYYYYYYK",
    "KyyyyyyyK",
    "KKKKKKKKK",
])
BAG_PAW = (16, 17, [
    "KK",
    "LK",
])


def build(face, stamps=(), tail=True, headphones=False):
    g = [["."] * CW for _ in range(CH)]

    def put(cells_or_stamp, head_space=False):
        if head_space:
            for r, c, k in cells_or_stamp:
                g[r + HY][c + HX] = k
        else:
            x0, y0, rows = cells_or_stamp
            for dy, row in enumerate(rows):
                for dx, k in enumerate(row):
                    if k != ".":
                        g[y0 + dy][x0 + dx] = k

    for r, row in enumerate(HEAD + BODY):
        for c, k in enumerate(row):
            if k != ".":
                g[r + HY][c + HX] = k
    if tail:
        put(TAIL, head_space=True)
    put(face, head_space=True)
    if headphones:
        for st in HEADPHONES:
            put(st)
    for st in stamps:
        put(st)
    return ["".join(r) for r in g]


POSES = {
    "Senyum": build(eyes_open() + MOUTH_UU),
    "Melambai": build(eyes_happy() + MOUTH_TALK, [PAW_WAVE, WAVE_LINES]),
    "Teruja": build(eyes_sparkle() + MOUTH_BIG, [PAW_HOORAY_L, PAW_HOORAY_R, SPARKS]),
    "Jatuh cinta": build(eyes_heart() + MOUTH_UU, [HEARTS]),
    "Terkejut": build(eyes_shock() + MOUTH_O, [BANG, SWEAT]),
    "Kenyit mata": build(eyes_open(L_EYE) + eyes_happy([R_EYE]) + MOUTH_UU),
    "Tunjuk": build(eyes_open() + MOUTH_TALK, [PAW_POINT]),
    "Berfikir": build(eyes_think() + MOUTH_FLAT, [PAW_CHIN, QMARK]),
    "Tidur": build(eyes_sleep() + MOUTH_SMALL, [ZZZ]),
    "Layan lagu": build(eyes_happy() + MOUTH_UU, [NOTE], headphones=True),
    "Shopping": build(eyes_sparkle() + MOUTH_UU, [BAG, BAG_PAW], tail=False),
    "Bercakap": build(eyes_open() + MOUTH_TALK),
}


def sheet(out, cols=4, scale=14):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
    cw, ch, pad = CW * scale + 60, CH * scale + 110, 28
    rows = (len(POSES) + cols - 1) // cols
    img = Image.new("RGB", (pad + cols * (cw + pad), 120 + rows * (ch + pad)), (17, 19, 24))
    d = ImageDraw.Draw(img)
    d.text((pad, 30), "Oyen — pelbagai postur", font=title, fill=(255, 214, 10))
    for i, (name, rows_) in enumerate(POSES.items()):
        spr = to_image(rows_, scale)
        spr.save(out / f"oyen-pose-{i + 1:02d}-{name.lower().replace(' ', '-')}.png")
        x0 = pad + (i % cols) * (cw + pad)
        y0 = 120 + (i // cols) * (ch + pad)
        d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=26, fill=(255, 248, 235))
        sx, sy = x0 + 30, y0 + 22
        sh = Image.new("RGBA", spr.size, (0, 0, 0, 0))
        sh.putalpha(spr.getchannel("A").point(lambda a: 60 if a else 0))
        img.paste((0, 0, 0), (sx + 8, sy + 8), sh)
        img.paste(spr, (sx, sy), spr)
        label = f"{i + 1}. {name}"
        tw = d.textlength(label, font=font)
        d.text((x0 + (cw - tw) / 2, y0 + ch - 68), label, font=font, fill=(42, 22, 11))
    img.save(out / "oyen-postur.png")
    return out / "oyen-postur.png"


if __name__ == "__main__":
    print(sheet(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
