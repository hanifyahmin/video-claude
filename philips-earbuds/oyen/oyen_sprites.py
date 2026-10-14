"""Oyen pixel-art candidates. Run: python3 oyen_sprites.py <outdir>

Each sprite is a list of equal-length strings; '.' is transparent and every
other character is a palette key.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PAL = {
    "K": (42, 22, 11),      # outline
    "O": (243, 146, 50),    # orange
    "D": (200, 97, 26),     # tabby stripe
    "H": (255, 182, 102),   # orange highlight
    "L": (255, 224, 181),   # cream
    "P": (255, 143, 163),   # pink (ears, nose)
    "B": (255, 112, 140),   # blush
    "E": (27, 27, 27),      # eye
    "W": (255, 255, 255),   # eye sparkle
    "Y": (255, 214, 10),    # beg kuning yellow
    "y": (204, 160, 0),     # yellow shade
    "G": (120, 128, 140),   # headphone grey
    "S": (55, 60, 70),      # headphone dark
    "R": (230, 57, 70),     # red accent
    "N": (90, 200, 250),    # music note blue
}

OYEN = {}

# 1. Klasik: the mascot already in the video
def _compose(base, layers):
    grid = [list(r) for r in base]
    for cells in layers:
        for r, c, k in cells:
            grid[r][c] = k
    return ["".join(r) for r in grid]


_VB = [".." + r for r in [
    "..KK........KK....", ".KOPK......KPOK...", ".KOPPK....KPPOK...", ".KOOOOKKKKOOOOK...",
    "KOODOOODDOOODOOK..", "KOOOOOOOOOOOOOOK..", "KOOOOOOOOOOOOOOK..", "KOOOOOOOOOOOOOOK..",
    "KOLLLLOPPOLLLLOK..", "KOLLLLLLLLLLLLOK..", ".KOLLLLLLLLLLOK...", "..KKOOOOOOOOKK....",
    ".KOODOOLLLLOODOK..", ".KOOOOLLLLLLOOOK..", ".KODOOLLLLLLOODK..", ".KLLKOLLLLLLOK....",
    "..KKKKKKKKKKKKKK..",
]]
_X = 2
OYEN["1 Klasik"] = _compose(_VB, [
    [(6, 3 + _X, "E"), (6, 4 + _X, "W"), (6, 11 + _X, "E"), (6, 12 + _X, "W"),
     (7, 3 + _X, "E"), (7, 4 + _X, "E"), (7, 11 + _X, "E"), (7, 12 + _X, "E")],
    [(9, 6 + _X, "K"), (9, 9 + _X, "K"), (10, 7 + _X, "K"), (10, 8 + _X, "K")],
    [(15, 13 + _X, "L"), (15, 14 + _X, "L"), (15, 15 + _X, "K")],
    [(10, 1, "K"), (11, 0, "K"), (11, 1, "O"), (11, 2, "K"), (12, 0, "K"), (12, 1, "D"),
     (12, 2, "K"), (13, 0, "K"), (13, 1, "O"), (13, 2, "K"), (14, 1, "K"), (14, 2, "O"), (15, 2, "K")],
])

# 2. Chibi: huge head, sparkly eyes, blush
OYEN["2 Chibi"] = [
    "...KK..........KK...",
    "..KOOK........KOOK..",
    "..KOPOK......KOPOK..",
    ".KOOPPOKKKKKKOPPOOK.",
    ".KOOOOOODDDDOOOOOOK.",
    "KOOOOOOOODDOOOOOOOOK",
    "KOOOOOOOOOOOOOOOOOOK",
    "KOOWEEOOOOOOOOWEEOOK",
    "KOOEEEOOOOOOOOEEEOOK",
    "KOOEEEOOOPPOOOEEEOOK",
    "KOBBOOOOKOOKOOOOBBOK",
    ".KOOOOOOOKKOOOOOOOK.",
    ".KOOOOOOOOOOOOOOOOK.",
    "..KKOOOOOOOOOOOOKK..",
    "....KOOOLLLLOOOK....",
    "....KOOLLLLLLOOK.KK.",
    "....KOOLLLLLLOOKKOK.",
    "....KOOLLLLLLOOKOK..",
    "....KLLKLLLLKLLKK...",
    ".....KK.KKKK.KK.....",
]

# 3. Roti: chonky loaf, happy squint
OYEN["3 Roti"] = [
    "....KK..........KK......",
    "...KPOK........KOPK.....",
    "..KOPPOKKKKKKKKOPPOK....",
    ".KOOOOOODDDDDDOOOOOOK...",
    ".KOOOOOOOODDOOOOOOOOK...",
    "KOOOKOKOOOOOOOOKOKOOOK..",
    "KOOKOOOKOOOOOOKOOOKOOK..",
    "KOBBOOOOOOPPOOOOOOBBOK..",
    "KOOOOOOOOKKKKOOOOOOOOK..",
    "KDOOOOOOOOOOOOOOOOOODK..",
    "KOODOOOOLLLLLLOOOODOOK..",
    "KOOOOOOLLLLLLLLOOOOOOKK.",
    "KDOOOOOLLLLLLLLOOOOODKOK",
    ".KOOOOOLLLLLLLLOOOOOOKOK",
    "..KKLLKKKKKKKKKKKLLKKKK.",
    "....KK..........KK......",
]

# 4. DJ: headphones on, vibing to the earbuds
OYEN["4 DJ"] = _compose([r.ljust(24, ".") for r in [
    "....KK........KK....",
    "...KOPK......KPOK...",
    "...KOPPK....KPPOK...",
    "..KKOOOOKKKKOOOOKK..",
    ".KSSSSSSSSSSSSSSSSK.",
    "KSKKOOOODDOOOOOKKSK.",
    "KGGKOOOOOOOOOOOOKGGK",
    "KGGKOKKOOOOOOKKOKGGK",
    "KGGKLLLLOPPOLLLLKGGK",
    "KGGKLLLKLLLLKLLLKGGK",
    ".KKKLLLLLKKLLLLLKKK.",
    "...KKOOOOOOOOOOKK...",
    "..KKOODOOLLLLOODOK..",
    ".KOKOOOOLLLLLLOOOK..",
    ".KDKODOOLLLLLLOODK..",
    "..KKLLKOLLLLLLOKLLK.",
    "....KKKKKKKKKKKKKKK.",
]], [[(0, 22, "N"), (0, 23, "N"), (1, 22, "N"), (1, 23, "N"), (2, 22, "N"), (3, 22, "N"),
      (4, 21, "N"), (4, 22, "N"), (5, 21, "N"), (5, 22, "N")]])

# 5. Shopper: holding the yellow basket bag (TikTok Shop vibe)
OYEN["5 Shopper"] = [
    "....KK........KK......",
    "...KOPK......KPOK.....",
    "...KOPPK....KPPOK.....",
    "...KOOOOKKKKOOOOK.....",
    "..KOODOOODDOOODOOK....",
    "..KOOOOOOOOOOOOOOK....",
    "..KOOEWOOOOOOEWOOK....",
    "..KOOEEOOOOOOEEOOK....",
    "..KOBLLLOPPOLLLBOK....",
    "..KOLLLKLLLLKLLLOK....",
    "...KOLLLLKKLLLLOK.KKK.",
    "....KKOOOOOOOOKK.K..K.",
    "..KKOODOOLLLLOOKKKKKKK",
    ".KOKOOOOLLLLLLOKYYYYYK",
    ".KDKODOOLLLLLLKLYYYYYK",
    "..KKOOOOLLLLLLKLYyYyYK",
    "...KOOOOLLLLLLOKYYYYYK",
    "..KKLLKOLLLLLLOKyyyyyK",
    "....KKKKKKKKKKKKKKKKKK",
]


def to_image(rows, scale):
    w = max(len(r) for r in rows)
    img = Image.new("RGBA", (w, len(rows)), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                img.putpixel((x, y), PAL[ch] + (255,))
    return img.resize((w * scale, len(rows) * scale), Image.NEAREST)


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
    card_w, card_h, pad = 420, 520, 30
    sheet = Image.new("RGB", (pad + 5 * (card_w + pad), card_h + 2 * pad + 90), (17, 19, 24))
    d = ImageDraw.Draw(sheet)
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
    d.text((pad, 24), "Pilih Oyen kegemaran kau!", font=title, fill=(255, 214, 10))
    for i, (name, rows) in enumerate(OYEN.items()):
        spr = to_image(rows, 16)
        spr.save(out / f"oyen-{name.split()[0]}-{name.split()[1].lower()}.png")
        x0, y0 = pad + i * (card_w + pad), pad + 90
        d.rounded_rectangle((x0, y0, x0 + card_w, y0 + card_h), radius=28, fill=(255, 248, 235))
        # pixel shadow then sprite, centred
        sx = x0 + (card_w - spr.width) // 2
        sy = y0 + 40 + (380 - spr.height) // 2
        shadow = Image.new("RGBA", spr.size, (0, 0, 0, 0))
        shadow.putalpha(spr.getchannel("A").point(lambda a: 70 if a else 0))
        sheet.paste((0, 0, 0), (sx + 10, sy + 10), shadow)
        sheet.paste(spr, (sx, sy), spr)
        tw = d.textlength(name, font=font)
        d.text((x0 + (card_w - tw) / 2, y0 + card_h - 80), name, font=font, fill=(42, 22, 11))
    sheet.save(out / "oyen-pilihan.png")
    print(out / "oyen-pilihan.png")


if __name__ == "__main__":
    for n, rows in OYEN.items():
        widths = {len(r) for r in rows}
        if len(widths) != 1:
            print("width mismatch", n, [(i, len(r)) for i, r in enumerate(rows)])
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
