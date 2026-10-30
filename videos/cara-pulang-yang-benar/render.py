"""Lyric video renderer: "Cara Pulang yang Benar" (1080x1920, 24 fps).

    python3 videos/cara-pulang-yang-benar/render.py frames 12.5 70 ...   # stills -> renders/frames/
    python3 videos/cara-pulang-yang-benar/render.py video <song.mp3> [--draft] [--end SECONDS]

Everything is procedural (PIL + numpy). Motif: an old framed photo of a veranda
found in a drawer. The parent sits alone on the bench; across the choruses the
child appears beside them ("Izinkan aku duduk di sebelahmu"), faint at first and
solid at the final chorus. Verse 2 (the parent's voice) turns the photo to dusk
and sends a light up to the sky ("Namamu selalu kuantar ke langit itu"). The
bridge closes the photo behind a camera shutter ("Kamera tak bisa mengulang")
and leaves ash in the dark; the final chorus opens it again in gold; the outro
lets the photo fade back to paper.

Voices: Voice 1 (the child) is a soft serif typed word by word; Voice 2 (the
parent) is handwriting written in as it is sung; both voices = the serif line
with the handwritten line answering under it. Words the child quotes from the
parent ("Pulanglah sebentar saja") are in the parent's handwriting.
"""
import json
import math
import subprocess
import sys
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).parent
FONTS = HERE / "assets" / "fonts"
W, H, FPS = 1080, 1920, 24

ALIGN = json.loads((HERE / "alignment.json").read_text())
ANAL = json.loads((HERE / "analysis.json").read_text())
DUR = ANAL["duration"]

# Safe area: TikTok/Reels UI covers the bottom ~300 px and the right edge.
TEXT_CX, TEXT_MAXW = 492, 800        # text block centred left of the button column
LYRIC_Y = 1300                       # centre of the lyric block under the photo

CREAM = np.array([243, 230, 204], np.float32)
AMBER = np.array([244, 182, 106], np.float32)
GOLD = np.array([255, 214, 140], np.float32)
INK = np.array([206, 224, 246], np.float32)


# ---------------------------------------------------------------- timeline ----

def sec(key):
    s = next(s for s in ALIGN["sections"] if s["key"] == key)
    return s["lines"][0]["start"], s["lines"][-1]["end"]


def line_start(key, i):
    return next(s for s in ALIGN["sections"] if s["key"] == key)["lines"][i]["start"]


V1 = sec("Verse 1"); PRE1 = sec("Pre-Chorus"); CH1 = sec("Chorus"); V2 = sec("Verse 2")
PRE2 = sec("Pre-Chorus 2"); CH2 = sec("Chorus 2"); BR = sec("Bridge"); FIN = sec("Final Chorus")
T_PRAYER = line_start("Verse 2", 3)          # "Namamu selalu kuantar ke langit itu"
T_CAMERA = line_start("Bridge", 2)           # "Kamera tak bisa mengulang"
T_SIT1, T_SIT2, T_SIT3 = CH1[0], CH2[0], FIN[0]


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def kf(t, keys):
    """Piecewise smoothstep through [(time, value), ...]."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * smooth((t - t0) / (t1 - t0 + 1e-9))
    return keys[-1][1]


def curve(name, t):
    arr = ANAL[name]
    return arr[min(len(arr) - 1, max(0, int(t * FPS)))]


def state(t):
    """All the slow visual parameters at time t."""
    s = {}
    s["lamp"] = kf(t, [(0, 0), (3.5, 1), (DUR - 7, 1), (DUR - 0.5, 0)])
    s["rise"] = kf(t, [(1.5, 1), (7, 0)])                       # frame comes up out of the drawer
    s["develop"] = kf(t, [(6, 0), (14.5, 1), (DUR - 26, 1), (DUR - 9, 0.08)])
    s["dusk"] = kf(t, [(V2[0] - 3, 0), (V2[0] + 3, 1), (PRE2[0], 1), (CH2[0], 0.35),
                       (BR[0], 0.35), (FIN[0], 0)])
    s["gold"] = kf(t, [(CH1[0] - 2, 0), (CH1[0] + 2, 0.45), (CH1[1], 0.45), (V2[0], 0),
                       (CH2[0] - 2, 0), (CH2[0] + 2, 0.6), (BR[0], 0.6), (BR[0] + 3, 0),
                       (FIN[0], 0), (FIN[0] + 1.5, 1), (FIN[1] + 12, 1), (DUR - 8, 0.4)])
    s["child"] = kf(t, [(T_SIT1, 0), (T_SIT1 + 5, 0.42), (V2[0], 0.3), (T_SIT2, 0.3),
                        (T_SIT2 + 5, 0.72), (BR[0], 0.72), (T_SIT3, 0.72), (T_SIT3 + 4, 1)])
    # Bridge: the photo dims and the shutter closes; final chorus opens it again.
    s["dark"] = kf(t, [(BR[0] - 1, 0), (BR[0] + 2, 1), (FIN[0] - 0.4, 1), (FIN[0] + 0.6, 0)])
    s["shutter"] = kf(t, [(T_CAMERA, 0), (T_CAMERA + 2.2, 0.72), (FIN[0] - 0.3, 0.72), (FIN[0] + 1.6, 0)])
    s["frame_glow"] = kf(t, [(PRE1[0], 0), (PRE1[0] + 3, 0.6), (CH1[0], 0.3), (CH1[1], 0.3),
                             (V2[0], 0), (PRE2[0], 0), (PRE2[0] + 3, 0.6), (CH2[0], 0.35),
                             (BR[0], 0), (FIN[0], 0), (FIN[0] + 1, 1), (FIN[1] + 12, 0.8),
                             (DUR - 8, 0)])
    s["scale"] = kf(t, [(0, 0.97), (V1[0], 1.0), (CH1[0], 1.02), (V2[0], 1.0), (CH2[0], 1.03),
                        (BR[0], 1.03), (BR[0] + 3, 0.9), (FIN[0], 0.9), (FIN[0] + 2, 1.05),
                        (DUR, 1.0)])
    s["text_y"] = LYRIC_Y
    s["ash"] = kf(t, [(BR[0] - 1, 0), (BR[0] + 2, 1), (FIN[0], 1), (FIN[0] + 2, 0)])
    s["bokeh"] = s["gold"] * (1 - s["dark"])
    s["prayer"] = (t - T_PRAYER) / 3.4                           # light rising to the sky
    s["star"] = kf(t, [(T_PRAYER + 3.2, 0), (T_PRAYER + 3.6, 1), (DUR - 6, 1), (DUR, 0)])
    s["energy"] = curve("energy", t)
    s["low"] = curve("low", t)
    s["drum"] = curve("drums", t)
    s["fade_out"] = kf(t, [(DUR - 4, 1), (DUR - 0.2, 0)])
    return s


# ------------------------------------------------------------------ assets ----

def font(name, size, wght=None):
    f = ImageFont.truetype(str(FONTS / name), size)
    if wght is not None:
        axes = f.get_variation_axes()
        vals = []
        for a in axes:
            n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
            vals.append({"Weight": wght, "Optical Size": min(144, size), "Softness": 100,
                         "Wonky": 0}.get(n, a["default"]))
        f.set_variation_by_axes(vals)
    return f


@lru_cache(None)
def fonts():
    return {
        "serif": font("fraunces-Fraunces.ttf", 76, 560),
        "italic": font("fraunces-Fraunces-Italic.ttf", 76, 480),
        "script": font("caveat-Caveat.ttf", 92, 620),
        "echo": font("caveat-Caveat.ttf", 78, 600),
        "title": font("fraunces-Fraunces-Italic.ttf", 104, 420),
        "title_small": font("fraunces-Fraunces.ttf", 34, 400),
    }


def value_noise(h, w, cell, seed):
    rng = np.random.default_rng(seed)
    small = rng.random((h // cell + 2, w // cell + 2)).astype(np.float32)
    img = Image.fromarray((small * 255).astype(np.uint8)).resize(
        ((w // cell + 2) * cell, (h // cell + 2) * cell), Image.BICUBIC)
    return np.asarray(img, np.float32)[:h, :w] / 255


def room(top, bottom, lamp, lamp_xy=(260, 360)):
    """Dark wooden wall lit by a lamp: vertical planks, grain, radial glow."""
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    base = np.array(top, np.float32) * (1 - y) + np.array(bottom, np.float32) * y
    base = np.broadcast_to(base, (H, W, 3)).copy()
    xs = np.arange(W)
    plank = ((xs // 135) % 2) * 0.05 + 0.97
    seam = np.where((xs % 135) < 3, 0.72, 1.0)
    grain = 0.9 + 0.12 * value_noise(H, W, 6, 1) * value_noise(H, W, 40, 2)
    grain = Image.fromarray((grain * 200).astype(np.uint8)).resize((W // 4, H)).resize((W, H))
    grain = np.asarray(grain, np.float32) / 200
    base *= (plank * seam)[None, :, None] * grain[..., None]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - lamp_xy[0], (yy - lamp_xy[1]) * 0.8) / 1100
    glow = np.exp(-d * d * 2.2)[..., None]
    base = base + np.array(lamp, np.float32) * glow
    vig = 1 - 0.55 * np.clip(np.hypot((xx - W / 2) / W, (yy - H / 2) / H) * 1.6, 0, 1) ** 2
    return base * vig[..., None]


@lru_cache(None)
def backgrounds():
    return {
        "warm": room((34, 22, 15), (16, 10, 7), (95, 58, 30)),
        "dusk": room((16, 22, 40), (8, 10, 18), (40, 52, 88)),
        "dark": room((10, 9, 9), (5, 5, 5), (22, 18, 16)),
    }


# Photo scene ------------------------------------------------------------------
PW, PH = 520, 660            # photo size
MAT, WOOD = 26, 44           # mat and wooden frame widths
FW, FH = PW + 2 * (MAT + WOOD), PH + 2 * (MAT + WOOD)
FRAME_CX, FRAME_CY = 540, 600
SKY = (0, 64, 148, 300)      # open side of the veranda (x0, y0, x1, y1)
PARENT_HEAD = (214, 268)
STAR_XY = (78, 112)


def scene_layers():
    """Grayscale layers at 2x, downsampled: base scene, sky mask, window mask, figures."""
    S = 2
    def canvas(v=0):
        return Image.new("L", (PW * S, PH * S), v)
    def P(*pts):
        return [(x * S, y * S) for x, y in pts]

    base = canvas(150)
    d = ImageDraw.Draw(base)
    d.rectangle(P((0, 0), (PW, 64)), fill=58)                          # eave
    d.rectangle(P((0, 58), (PW, 66)), fill=40)
    d.rectangle(P((148, 64), (PW, 430)), fill=176)                      # back wall
    for x in range(160, PW, 34):                                        # wall boards
        d.line(P((x, 66), (x, 430)), fill=164, width=S)
    d.rectangle(P(SKY[:2], SKY[2:]), fill=205)                        # sky
    d.rectangle(P((138, 64), (156, 470)), fill=70)                       # post
    d.rectangle(P((0, 296), (148, 306)), fill=92)                        # railing
    for x in range(8, 148, 18):
        d.rectangle(P((x, 306), (x + 7, 470)), fill=96)
    d.rectangle(P((0, 300), (148, 470)), outline=None)
    d.rectangle(P((300, 120), (446, 316)), fill=72)                      # window
    d.rectangle(P((306, 126), (440, 310)), fill=120)
    d.rectangle(P((370, 126), (376, 310)), fill=80)
    d.rectangle(P((306, 214), (440, 220)), fill=80)
    d.line(P((300, 66), (300, 96)), fill=60, width=2 * S)                # hanging lamp
    d.polygon(P((282, 96), (318, 96), (310, 116), (290, 116)), fill=95)
    d.rectangle(P((0, 430), (PW, PH)), fill=124)                         # floor
    for i in range(14):
        x0 = -300 + i * 70
        d.line(P((PW / 2 + (x0 - PW / 2) * 0.35, 430), (x0, PH)), fill=108, width=S)
    for y in (470, 530, 610):
        d.line(P((0, y), (PW, y)), fill=114, width=S)
    d.polygon(P((450, 520), (500, 520), (492, 590), (458, 590)), fill=84)   # pot plant
    for a in range(-60, 70, 20):
        r = math.radians(a - 90)
        d.line(P((475, 520), (475 + 46 * math.cos(r), 520 + 70 * math.sin(r))), fill=70, width=5 * S)
    # Bench with room on the right for a second person.
    d.rectangle(P((128, 316), (420, 330)), fill=82)                       # back rest
    d.rectangle(P((128, 346), (420, 358)), fill=82)
    d.rectangle(P((118, 410), (432, 428)), fill=74)                       # seat
    for x in (132, 410):
        d.rectangle(P((x, 316), (x + 10, 520)), fill=66)

    def person(cx, head_y, cap, lean=0):
        img = canvas()
        p = ImageDraw.Draw(img)
        hx, hy = cx + lean, head_y
        p.ellipse(P((hx - 27, hy - 31), (hx + 27, hy + 30)), fill=255)          # head
        if cap:                                                               # peci
            p.rounded_rectangle(P((hx - 27, hy - 42), (hx + 27, hy - 14)), radius=6 * S, fill=255)
        else:                                                                 # hair
            p.ellipse(P((hx - 29, hy - 35), (hx + 29, hy + 4)), fill=255)
        p.rectangle(P((hx - 10, hy + 22), (hx + 10, hy + 40)), fill=255)        # neck
        p.polygon(P((hx - 18, hy + 36), (cx - 56, hy + 62), (cx - 60, 412), (cx + 60, 412),
                    (cx + 56, hy + 62), (hx + 18, hy + 36)), fill=255)          # shoulders, torso
        for sgn in (-1, 1):                                                   # arms to knees
            p.polygon(P((cx + sgn * 46, hy + 58), (cx + sgn * 64, hy + 66), (cx + sgn * 56, 418),
                        (cx + sgn * 34, 430), (cx + sgn * 30, 412)), fill=255)
        p.rounded_rectangle(P((cx - 54, 396), (cx + 54, 446)), radius=18 * S, fill=255)  # lap
        p.polygon(P((cx - 46, 436), (cx - 12, 436), (cx - 14, 552), (cx - 42, 552)), fill=255)  # legs
        p.polygon(P((cx + 12, 436), (cx + 46, 436), (cx + 42, 552), (cx + 14, 552)), fill=255)
        p.ellipse(P((cx - 54, 540), (cx - 8, 562)), fill=255)                    # feet
        p.ellipse(P((cx + 8, 540), (cx + 54, 562)), fill=255)
        return img

    sky = canvas(); ImageDraw.Draw(sky).rectangle(P(SKY[:2], SKY[2:]), fill=255)
    win = canvas(); ImageDraw.Draw(win).rectangle(P((306, 126), (440, 310)), fill=255)
    ImageDraw.Draw(win).ellipse(P((280, 92), (320, 126)), fill=255)        # lamp bulb
    parent = person(214, 268, cap=True)
    child = person(350, 258, cap=False, lean=-6)

    def down(img, blur=0):
        img = img.resize((PW, PH), Image.LANCZOS)
        if blur:
            img = img.filter(ImageFilter.GaussianBlur(blur))
        return np.asarray(img, np.float32) / 255

    return {"base": down(base, 0.6), "sky": down(sky), "window": down(win, 1.2),
            "parent": down(parent, 0.5), "child": down(child, 0.5)}


def gradient_lut(stops):
    """stops: [(pos 0..1, (r,g,b)), ...] -> 256x3 LUT."""
    pos = np.array([s[0] for s in stops]); col = np.array([s[1] for s in stops], np.float32)
    x = np.linspace(0, 1, 256)
    return np.stack([np.interp(x, pos, col[:, c]) for c in range(3)], 1).astype(np.float32)


@lru_cache(None)
def photo_assets():
    L = scene_layers()
    rng = np.random.default_rng(7)
    yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
    vig = 1 - 0.5 * np.clip(np.hypot((xx - PW / 2) / PW, (yy - PH / 2) / PH) * 1.5, 0, 1) ** 2.2
    # Aged paper: stains and scratches, used for the blank / undeveloped print.
    stain = value_noise(PH, PW, 60, 11) * 0.6 + value_noise(PH, PW, 14, 12) * 0.4
    paper = np.array([228, 212, 178], np.float32) * (0.9 + 0.12 * stain[..., None])
    scratches = Image.new("L", (PW, PH), 0)
    sd = ImageDraw.Draw(scratches)
    for _ in range(26):
        x, y = rng.uniform(0, PW), rng.uniform(0, PH)
        a = rng.uniform(-1.9, -1.2); ln = rng.uniform(30, 160)
        sd.line([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], fill=int(rng.uniform(40, 110)))
    for _ in range(140):
        x, y = rng.uniform(0, PW), rng.uniform(0, PH); r = rng.uniform(0.5, 1.8)
        sd.ellipse([(x - r, y - r), (x + r, y + r)], fill=int(rng.uniform(60, 160)))
    stars = []
    x0, y0, x1, y1 = SKY
    for _ in range(26):
        stars.append((rng.uniform(x0 + 6, x1 - 10), rng.uniform(y0 + 6, y1 - 60),
                      rng.uniform(0.6, 1.6), rng.uniform(0, 6.28)))
    return {
        "L": L, "vig": vig, "paper": paper, "stain": stain,
        "scratch": np.asarray(scratches, np.float32) / 255, "stars": stars,
        "sepia": gradient_lut([(0, (36, 22, 14)), (0.45, (128, 90, 54)), (0.8, (214, 180, 128)),
                               (1, (246, 230, 196))]),
        "dusk": gradient_lut([(0, (14, 18, 34)), (0.45, (62, 72, 110)), (0.75, (150, 140, 150)),
                              (1, (236, 214, 170))]),
        "gold": gradient_lut([(0, (52, 28, 12)), (0.4, (170, 108, 50)), (0.75, (250, 196, 112)),
                              (1, (255, 244, 214))]),
    }


@lru_cache(None)
def soft_dot(r):
    s = int(r * 4) + 2
    yy, xx = np.mgrid[-s:s + 1, -s:s + 1].astype(np.float32)
    return np.exp(-(xx * xx + yy * yy) / (2 * r * r))


def add_dot(img, x, y, r, color, a):
    k = soft_dot(round(r * 2) / 2)
    s = k.shape[0] // 2
    x, y = int(round(x)), int(round(y))
    h, w = img.shape[:2]
    x0, x1, y0, y1 = max(0, x - s), min(w, x + s + 1), max(0, y - s), min(h, y + s + 1)
    if x0 >= x1 or y0 >= y1:
        return
    kk = k[y0 - (y - s):y1 - (y - s), x0 - (x - s):x1 - (x - s)]
    img[y0:y1, x0:x1] += kk[..., None] * (np.asarray(color, np.float32) * a)


def render_photo(t, s):
    A = photo_assets(); L = A["L"]
    SIL = 0.13   # silhouettes are solid, the child's opacity grows over the song
    lum = L["base"] * (1 - L["parent"]) + SIL * L["parent"]
    ca = s["child"] * L["child"]
    lum = lum * (1 - ca) + SIL * ca
    lum = np.clip(lum + 0.25 * (s["gold"] + 0.5 * s["dusk"]) * L["window"], 0, 1)
    # Dusk darkens the sky (stars come out), gold lifts the whole print.
    lum = lum * (1 - 0.62 * s["dusk"] * L["sky"])
    idx = np.clip(lum * 255, 0, 255).astype(np.uint8)
    wd, wg = s["dusk"], s["gold"]
    rgb = A["sepia"][idx] * (1 - wd) * (1 - wg) + A["dusk"][idx] * wd * (1 - wg) + A["gold"][idx] * wg
    if wd > 0.02 or s["star"] > 0:
        for (x, y, r, ph) in A["stars"]:
            tw = 0.6 + 0.4 * math.sin(t * 2.1 + ph)
            add_dot(rgb, x, y, r, (255, 240, 210), 0.85 * wd * tw)
    # The prayer: a light leaves the parent and becomes a star over the veranda.
    p = s["prayer"]
    if 0 <= p <= 1.05:
        e = smooth(min(1, p))
        hx, hy = PARENT_HEAD
        x = hx + (STAR_XY[0] - hx) * e + 22 * math.sin(e * math.pi)
        y = hy - 40 + (STAR_XY[1] - hy + 40) * e
        add_dot(rgb, x, y, 9, (255, 226, 160), 0.8 * min(1, p * 6))
        add_dot(rgb, x, y, 3, (255, 255, 240), 1.0 * min(1, p * 6))
    if s["star"] > 0:
        tw = 0.8 + 0.2 * math.sin(t * 3)
        add_dot(rgb, *STAR_XY, 7, (255, 226, 160), 0.6 * s["star"] * tw)
        add_dot(rgb, *STAR_XY, 2.5, (255, 255, 240), 0.95 * s["star"])
    # Develop from blank aged paper; keep the print a little faded.
    dev = s["develop"]
    rgb = rgb * A["vig"][..., None]
    rgb = A["paper"] * (1 - dev) + (rgb * 0.92 + A["paper"] * 0.08) * dev
    rgb = rgb * (1 - 0.18 * A["scratch"][..., None]) + 60 * A["scratch"][..., None] * dev
    rgb = rgb * (1 - 0.6 * s["dark"])
    if s["shutter"] > 0:
        rgb = shutter(rgb, s["shutter"], t)
    return np.clip(rgb, 0, 255)


def shutter(rgb, closed, t):
    """Six-blade camera iris closing over the print."""
    img = Image.new("L", (PW * 2, PH * 2), 255)
    d = ImageDraw.Draw(img)
    cx, cy = PW, PH
    R = math.hypot(PW, PH) * (1 - smooth(closed)) + 2
    rot = closed * 1.1
    pts = [(cx + R * math.cos(rot + k * math.pi / 3), cy + R * math.sin(rot + k * math.pi / 3))
           for k in range(6)]
    d.polygon(pts, fill=0)
    blades = Image.new("L", (PW * 2, PH * 2), 0)
    bd = ImageDraw.Draw(blades)
    for k in range(6):
        x, y = pts[k]
        a = rot + k * math.pi / 3 + math.pi / 2 + 0.5
        bd.line([(x, y), (x + 2400 * math.cos(a), y + 2400 * math.sin(a))], fill=255, width=4)
    open_mask = 1 - np.asarray(img.resize((PW, PH), Image.LANCZOS), np.float32) / 255
    lines = np.asarray(blades.filter(ImageFilter.GaussianBlur(1.5)).resize((PW, PH), Image.LANCZOS), np.float32)[..., None] / 255
    shade = 0.75 + 0.25 * np.linspace(1, 0, PH, dtype=np.float32)[:, None, None]
    blade_col = np.array([58, 54, 50], np.float32) * shade
    # The last glimpse through the aperture is lit a little brighter than the dimmed print.
    out = rgb * (1 + 0.9 * closed) * open_mask[..., None] + blade_col * (1 - open_mask[..., None])
    return out + lines * (1 - open_mask[..., None]) * 70


@lru_cache(None)
def frame_assets():
    """Wooden frame with a cream mat (RGBA) and its soft shadow."""
    S = 2
    img = Image.new("RGBA", (FW * S, FH * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, FW * S, FH * S], fill=(96, 58, 32, 255))
    # Wood grain: stripes along each side of the frame, warped by low-frequency noise.
    warp = value_noise(FH * S, FW * S, 50, 21) * 7 + value_noise(FH * S, FW * S, 12, 22) * 1.5
    yy, xx = np.mgrid[0:FH * S, 0:FW * S].astype(np.float32)
    side = np.minimum(xx, FW * S - xx) < np.minimum(yy, FH * S - yy)
    across = np.where(side, xx, yy)
    g = 0.5 + 0.5 * np.sin(across * 0.16 + warp)
    g = g ** 3 * 0.6 + value_noise(FH * S, FW * S, 2, 23) * 0.4
    arr = np.asarray(img, np.float32).copy()
    arr[..., :3] *= (0.62 + 0.7 * g)[..., None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    w = WOOD * S
    for i, c in enumerate([(120, 80, 46), (96, 62, 36), (52, 32, 20)]):     # bevels
        d.rectangle([i * 4, i * 4, FW * S - 1 - i * 4, FH * S - 1 - i * 4], outline=c + (255,), width=3)
    d.rectangle([w - 8, w - 8, FW * S - w + 8, FH * S - w + 8], fill=(196, 152, 82, 255))  # gold lip
    d.rectangle([w - 3, w - 3, FW * S - w + 3, FH * S - w + 3], fill=(140, 100, 52, 255))
    d.rectangle([w, w, FW * S - w, FH * S - w], fill=(232, 220, 196, 255))                 # mat
    m = (WOOD + MAT) * S
    d.rectangle([m - 3, m - 3, FW * S - m + 3, FH * S - m + 3], fill=(176, 160, 132, 255))  # mat bevel
    d.rectangle([m, m, FW * S - m, FH * S - m], fill=(0, 0, 0, 0))
    img = img.resize((FW, FH), Image.LANCZOS)
    pad = 60
    sh = Image.new("L", (FW + 2 * pad, FH + 2 * pad), 0)
    ImageDraw.Draw(sh).rectangle([pad + 10, pad + 22, pad + FW + 10, pad + FH + 22], fill=210)
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    glow = Image.new("L", (FW + 2 * pad, FH + 2 * pad), 0)
    ImageDraw.Draw(glow).rectangle([pad, pad, pad + FW, pad + FH], outline=255, width=18)
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    return {"frame": np.asarray(img, np.float32), "shadow": np.asarray(sh, np.float32) / 255,
            "glow": np.asarray(glow, np.float32) / 255, "pad": pad}


def composite_frame(canvas, t, s):
    F = frame_assets()
    photo = render_photo(t, s)
    fr = F["frame"].copy()
    o = WOOD + MAT
    a = fr[..., 3:] / 255
    inner = fr[o:o + PH, o:o + PW, :3] * a[o:o + PH, o:o + PW] + photo * (1 - a[o:o + PH, o:o + PW])
    fr[o:o + PH, o:o + PW, :3] = inner
    fr[o:o + PH, o:o + PW, 3] = 255
    # Frame dims with the room in the bridge.
    fr[..., :3] *= 1 - 0.6 * s["dark"]
    fr[..., :3] *= 0.75 + 0.25 * s["lamp"]

    scale = s["scale"] * (1 + 0.004 * s["drum"] * s["gold"])
    alpha_all = 1 - s["rise"]
    dy = 420 * s["rise"] ** 1.6 + 6 * math.sin(t * 0.5)
    dx = 4 * math.sin(t * 0.31)
    cx, cy = FRAME_CX + dx, FRAME_CY + dy

    pad = F["pad"]
    for layer, color, strength in ((F["shadow"], None, 0.75), (F["glow"], GOLD, s["frame_glow"])):
        if strength <= 0.01:
            continue
        lw, lh = int(layer.shape[1] * scale), int(layer.shape[0] * scale)
        im = np.asarray(Image.fromarray((layer * 255).astype(np.uint8)).resize((lw, lh), Image.BILINEAR),
                        np.float32) / 255
        x0, y0 = int(cx - lw / 2), int(cy - lh / 2)
        region = blit_region(canvas, x0, y0, lw, lh)
        if region is None:
            continue
        (cy0, cy1, cx0, cx1), (sy0, sy1, sx0, sx1) = region
        m = im[sy0:sy1, sx0:sx1, None] * strength * alpha_all
        if color is None:
            canvas[cy0:cy1, cx0:cx1] *= 1 - m
        else:
            canvas[cy0:cy1, cx0:cx1] += m * color * (0.55 + 0.45 * s["drum"])

    fw, fh = int(FW * scale), int(FH * scale)
    im = np.asarray(Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8)).resize((fw, fh), Image.BICUBIC),
                    np.float32)
    x0, y0 = int(cx - fw / 2), int(cy - fh / 2)
    region = blit_region(canvas, x0, y0, fw, fh)
    if region:
        (cy0, cy1, cx0, cx1), (sy0, sy1, sx0, sx1) = region
        src = im[sy0:sy1, sx0:sx1]
        a = src[..., 3:] / 255 * alpha_all
        canvas[cy0:cy1, cx0:cx1] = canvas[cy0:cy1, cx0:cx1] * (1 - a) + src[..., :3] * a


def blit_region(canvas, x0, y0, w, h):
    H_, W_ = canvas.shape[:2]
    cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W_, x0 + w), min(H_, y0 + h)
    if cx0 >= cx1 or cy0 >= cy1:
        return None
    return (cy0, cy1, cx0, cx1), (cy0 - y0, cy1 - y0, cx0 - x0, cx1 - x0)


# ---------------------------------------------------------------- particles ----

@lru_cache(None)
def particles():
    rng = np.random.default_rng(3)
    n = 150
    return {k: rng.random(n) for k in ("x", "y", "sp", "ph", "r", "b")}


@lru_cache(None)
def bokeh():
    rng = np.random.default_rng(5)
    return [(rng.uniform(60, 1000), rng.uniform(150, 1500), rng.uniform(26, 70), rng.uniform(0, 6.3),
             rng.uniform(0.05, 0.16)) for _ in range(16)]


def draw_particles(canvas, t, s):
    P = particles()
    e = s["energy"]
    lamp = s["lamp"] * (1 - 0.7 * s["ash"])
    n_dust = int(60 + 90 * e)
    for i in range(n_dust):
        # Dust motes drift slowly up and sideways through the lamp light.
        x = (P["x"][i] * W + 18 * math.sin(t * 0.3 + P["ph"][i] * 6) + t * 6 * (P["sp"][i] - 0.5)) % W
        y = (P["y"][i] * H - t * (8 + 14 * P["sp"][i])) % H
        near = math.exp(-((x - 260) ** 2 + (y - 360) ** 2) / (2 * 520 ** 2))
        a = (0.25 + 0.75 * near) * (0.4 + 0.6 * e) * lamp * (0.5 + 0.5 * math.sin(t * 1.3 + P["ph"][i] * 9))
        col = INK if s["dusk"] > 0.5 else (255, 222, 170)
        if P["b"][i] > 0.8:   # out-of-focus mote near the lens
            add_dot(canvas, x, y, 6 + 6 * P["r"][i], col, 0.22 * a)
        else:
            add_dot(canvas, x, y, 0.9 + 1.6 * P["r"][i], col, 1.5 * a)
    if s["ash"] > 0.01:
        for i in range(110):
            # Ash: grey flakes rising and swirling in the dark (bridge).
            x = (P["x"][i] * W + 60 * math.sin(t * 0.7 + P["ph"][i] * 6)) % W
            y = (P["y"][i] * H + 120 - (t - BR[0]) * (40 + 60 * P["sp"][i])) % (H + 200) - 100
            flick = 0.5 + 0.5 * math.sin(t * 3 + P["ph"][i] * 20)
            ember = P["b"][i] > 0.86
            col = (255, 140, 70) if ember else (150, 146, 140)
            add_dot(canvas, x, y, 1.2 + 2.6 * P["r"][i], col,
                    (0.75 if ember else 0.32) * s["ash"] * (0.4 + 0.6 * flick) * (0.6 + 0.6 * e))
    if s["bokeh"] > 0.01:
        for (x, y, r, ph, sp) in bokeh():
            xx = x + 40 * math.sin(t * sp + ph)
            yy = y + 30 * math.cos(t * sp * 0.8 + ph)
            a = s["bokeh"] * (0.35 + 0.5 * s["low"] + 0.3 * s["drum"]) * (0.6 + 0.4 * math.sin(t * 0.9 + ph))
            add_dot(canvas, xx, yy, r * 0.5, GOLD, 0.11 * a)


# -------------------------------------------------------------------- text ----

PARENT_QUOTE = "Kau bilang"


def word_styles(sec, line):
    """Per-word style: the child's serif, the parent's script for quoted parent words,
    serif italic for the child's own quoted words."""
    words = line["text"].split()
    styles, inq = [], False
    parent_quote = line["text"].startswith(PARENT_QUOTE)
    base = "script" if sec["voice"] == "v2" else "serif"
    if sec["key"] == "Bridge":       # "almost spoken": an aside, in italic
        return ["italic"] * len(words)
    for w in words:
        opens = w.startswith('"')
        if opens:
            inq = True
        if inq and base == "serif":
            styles.append("script" if parent_quote else "italic")
        else:
            styles.append(base)
        if w.endswith('"') or w.endswith('",') or w.endswith('".'):
            inq = False
    return styles


def clean(w):
    return w.replace('"', "")


def layout(words, styles, maxw):
    """Balanced wrap into 1-2 rows. -> rows of (word_idx, x_offset) and row widths."""
    F = fonts()
    space = {k: F[k].getlength(" ") for k in F}
    widths = [F[st].getlength(clean(w)) for w, st in zip(words, styles)]
    total = sum(widths) + sum(space[st] for st in styles[:-1])
    if total <= maxw:
        splits = [len(words)]
    else:
        best, best_cost = None, 1e9
        for k in range(1, len(words)):
            a = sum(widths[:k]) + sum(space[st] for st in styles[:k - 1])
            b = sum(widths[k:]) + sum(space[st] for st in styles[k:-1])
            if max(a, b) > maxw:
                continue
            cost = abs(a - b) - (120 if words[k - 1].endswith((",", "...")) else 0)
            if cost < best_cost:
                best, best_cost = k, cost
        splits = [best or len(words) // 2, len(words)]
    rows, start = [], 0
    for end in splits:
        x, row = 0.0, []
        for i in range(start, end):
            row.append((i, x))
            x += widths[i] + (space[styles[i]] if i < end - 1 else 0)
        rows.append((row, x))
        start = end
    return rows, widths


def all_lines():
    out = []
    for sec in ALIGN["sections"]:
        for line in sec["lines"]:
            out.append((sec, line))
    return out


LINES = all_lines()
ROW_H = {"serif": 98, "script": 104, "echo": 82}


def line_window(i):
    """(appear, disappear) for line i."""
    sec, line = LINES[i]
    appear = line["start"] - 0.45
    if i > 0:
        appear = max(appear, LINES[i - 1][1]["end"] + 0.05)
    nxt = LINES[i + 1][1]["start"] - 0.45 if i + 1 < len(LINES) else line["end"] + 4
    gone = min(max(nxt, line["end"] + 0.3), line["end"] + 2.6)
    return appear, gone


def draw_text_layer(t, s):
    """-> (rgba float array HxWx4 over the whole frame) or None."""
    active = []
    for i, (sec, line) in enumerate(LINES):
        a0, a1 = line_window(i)
        if a0 - 0.3 <= t <= a1 + 0.35:
            active.append(i)
    title_a = kf(t, [(3.5, 0), (5.5, 1), (12.4, 1), (14.6, 0)])
    end_a = kf(t, [(DUR - 20, 0), (DUR - 17, 1), (DUR - 5.5, 1), (DUR - 2.5, 0)])
    if not active and title_a <= 0 and end_a <= 0:
        return None
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, g = ImageDraw.Draw(layer), ImageDraw.Draw(glow)
    F = fonts()
    for a, cy in ((title_a, LYRIC_Y), (end_a, LYRIC_Y + 40)):
        if a > 0:
            for k, (txt, f, dy) in enumerate((("Cara Pulang", F["title"], -50), ("yang Benar", F["title"], 60))):
                w = f.getlength(txt)
                d.text((TEXT_CX - w / 2, cy + dy - (1 - a) * 14), txt, font=f, anchor="ls",
                       fill=tuple(int(c) for c in CREAM) + (int(255 * a),))
    for i in active:
        draw_line(d, g, i, t, s)
    gl = glow.filter(ImageFilter.GaussianBlur(14))
    shadow = layer.split()[3].filter(ImageFilter.GaussianBlur(8))
    lay = np.asarray(layer, np.float32); gla = np.asarray(gl, np.float32)
    sh = np.asarray(shadow, np.float32)[..., None] / 255 * 0.7
    return lay, gla, sh


def draw_line(d, g, i, t, s):
    sec, line = LINES[i]
    a0, a1 = line_window(i)
    fade_in = smooth((t - (a0 - 0.3)) / 0.3)
    fade_out = 1 - smooth((t - a1) / 0.35)
    la = fade_in * fade_out
    if la <= 0:
        return
    rise = (1 - fade_in) * 18 - (1 - fade_out) * 22
    words = line["text"].split()
    styles = word_styles(sec, line)
    both = sec["voice"] == "both"
    F = fonts()
    rows, widths = layout(words, styles, TEXT_MAXW)
    row_h = [max(ROW_H["script" if st == "script" else "serif"] for st in
                 (styles[j] for j, _ in row)) for row, _ in rows]
    echo_rows, echo_w = None, None
    total_h = sum(row_h)
    if both:
        echo_rows, echo_w = layout(words, ["echo"] * len(words), TEXT_MAXW - 40)
        total_h += 20 + ROW_H["echo"] * len(echo_rows)
    y = s["text_y"] - total_h / 2 + rise
    gold_mix = s["gold"] if both else 0.0
    for (row, rw), rh in zip(rows, row_h):
        x0 = TEXT_CX - rw / 2
        base_y = y + rh * 0.78
        for j, xo in row:
            draw_word(d, g, words[j], line["words"][j], styles[j], x0 + xo, base_y, t, la, gold_mix)
        y += rh
    if both:
        y += 20
        for row, rw in echo_rows:
            x0 = TEXT_CX - rw / 2 + 10
            for j, xo in row:
                draw_word(d, g, words[j], line["words"][j], "echo", x0 + xo, y + ROW_H["echo"] * 0.75,
                          t, la * 0.82, 0)
            y += ROW_H["echo"]


def draw_word(d, g, text, w, style, x, y, t, la, gold_mix):
    F = fonts()
    f = F[style]
    txt = clean(text)
    st, en = w["start"], max(w["end"], w["start"] + 0.12)
    if style in ("script", "echo"):
        # Handwriting: the word is written in left to right while it is sung.
        prog = smooth((t - st + 0.05) / max(0.22, min(0.7, en - st)))
        if prog <= 0:
            return
        col = INK
        active = st - 0.05 <= t <= en + 0.15
        wl = f.getlength(txt)
        mask = Image.new("L", (int(wl + 40), 220), 0)
        ImageDraw.Draw(mask).text((10, 150), txt, font=f, anchor="ls", fill=255)
        cut = int(10 + (wl + 20) * prog)
        arr = np.asarray(mask).copy()
        ramp = np.clip((cut - np.arange(arr.shape[1])) / 14, 0, 1)
        arr = (arr * ramp[None, :]).astype(np.uint8)
        a = la * (1.0 if active or t > en else 0.9)
        d.bitmap((x - 10, y - 150), Image.fromarray((arr * a).astype(np.uint8)), fill=tuple(int(v) for v in col))
        if active:
            g.bitmap((x - 10, y - 150), Image.fromarray((arr * 0.55 * la).astype(np.uint8)),
                     fill=(150, 190, 255))
        return
    # Serif: upcoming words sit faint, a word lifts in as it is sung, the sung word glows.
    pop = smooth((t - st + 0.08) / 0.18)
    active = st - 0.05 <= t <= en + 0.12
    alpha = 0.26 + 0.74 * pop
    lift = (1 - pop) * 8
    base = CREAM * (1 - gold_mix) + GOLD * gold_mix
    col = AMBER if active else base
    if active:
        k = smooth((t - st + 0.05) / 0.12)
        col = base * (1 - k) + AMBER * k
    fill = tuple(int(c) for c in col) + (int(255 * alpha * la),)
    d.text((x, y + lift), txt, font=f, anchor="ls", fill=fill)
    if active:
        g.text((x, y + lift), txt, font=f, anchor="ls", fill=(255, 170, 80, int(200 * la)))


# ------------------------------------------------------------------- frame ----

@lru_cache(None)
def grain():
    rng = np.random.default_rng(9)
    small = [rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
    return [np.asarray(Image.fromarray(((g * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR),
                       np.float32) - 128 for g in small]


def render(t):
    s = state(t)
    B = backgrounds()
    wd = s["dusk"] * (1 - s["dark"])
    bg = B["warm"] * (1 - wd) + B["dusk"] * wd
    bg = bg * (1 - s["dark"]) + B["dark"] * s["dark"]
    canvas = bg * (0.35 + 0.65 * s["lamp"]) * (0.92 + 0.12 * s["energy"])
    draw_particles(canvas, t, s)
    composite_frame(canvas, t, s)
    txt = draw_text_layer(t, s)
    if txt is not None:
        lay, gla, sh = txt
        canvas *= 1 - sh
        canvas += gla[..., :3] * (gla[..., 3:] / 255) * 0.9
        a = lay[..., 3:] / 255
        canvas = canvas * (1 - a) + lay[..., :3] * a
    gr = grain()[int(t * 12) % 6]   # grain at 12 fps: filmic, and cheaper to encode
    canvas += gr[..., None] * 0.15
    canvas *= s["fade_out"]
    return np.clip(canvas, 0, 255).astype(np.uint8)


def _frame(i):
    return render(i / FPS).tobytes()


def write_video(song, out, draft=False, end=None):
    end = min(end or DUR, DUR)
    n = int(end * FPS)
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = ["-vf", "scale=720:1280"] if draft else []
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-t", f"{end:.3f}", "-i", str(song), *vf,
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow",
           "-crf", "26" if draft else "19", "-maxrate", "6M" if draft else "10M",
           "-bufsize", "20M", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "256k", "-shortest", str(out)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for k, buf in enumerate(pool.imap(_frame, range(n), chunksize=6)):
            ff.stdin.write(buf)
            if k % (FPS * 10) == 0:
                print(f"{k / FPS:6.1f}s / {end:.1f}s", flush=True)
    ff.stdin.close()
    ff.wait()
    print("wrote", out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "frames":
        d = HERE / "renders" / "frames"; d.mkdir(parents=True, exist_ok=True)
        for a in sys.argv[2:]:
            Image.fromarray(render(float(a))).save(d / f"t{float(a):07.2f}.png")
            print("frame", a)
    elif cmd == "video":
        draft = "--draft" in sys.argv
        end = float(sys.argv[sys.argv.index("--end") + 1]) if "--end" in sys.argv else None
        name = ("draft" if draft else "cara-pulang-yang-benar") + (f"-first{end:g}s" if end else "")
        write_video(Path(sys.argv[2]), HERE / "renders" / f"{name}.mp4", draft, end)
