"""Oyen (Chibi): one head + body, and every pose as a declarative spec.

A pose = eyes + mouth + stamps (props/limbs) on the shared head and body, so
the character stays identical everywhere. From each spec we derive the
frames a video needs: the resting frame, a talking frame (same pose, open
mouth) and a blink frame (eyes closed), when the pose supports them.

Coordinates: faces are (row, col, colour) in head space (the 20x14 head,
drawn at HX, HY); stamps are (canvas_x, canvas_y, rows) on the CW x CH
canvas.

To add a pose: add an entry to POSE_SPECS, run `python3 -m oyen poses`, look
at oyen/gallery/poses/oyen-postur.png.
"""
from dataclasses import dataclass, field

CW, CH = 28, 24
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

# ---------------- eyes (head space) ----------------
L_EYE, R_EYE = (3, 4, 5), (14, 15, 16)


def eyes_open(cols=L_EYE + R_EYE):
    cells = [(r, c, "E") for r in (6, 7, 8) for c in cols]
    for side in (L_EYE, R_EYE):
        if side[0] in cols:
            cells.append((6, side[0], "W"))
    return cells


def eyes_happy(sides=(L_EYE, R_EYE)):  # ^ ^
    out = []
    for a, b, c in sides:
        out += [(6, b, "K"), (7, a, "K"), (7, c, "K")]
    return out


def eyes_sleep():  # — —
    return [(8, c, "K") for c in L_EYE + R_EYE]


def eyes_blink():  # closed mid-blink
    return [(7, c, "K") for c in L_EYE + R_EYE]


def eyes_heart():
    out = []
    for a, b, c in (L_EYE, R_EYE):
        out += [(6, a, "R"), (6, c, "R"), (7, a, "R"), (7, b, "R"), (7, c, "R"), (8, b, "R")]
    return out


def eyes_shock():  # big white eyes, tiny pupils, raised brows
    out = []
    for a, b, c in (L_EYE, R_EYE):
        out += [(r, x, "W") for r in (6, 7, 8) for x in (a, b, c)]
        out += [(7, b, "E")]
        out += [(5, a, "K"), (5, b, "K"), (5, c, "K")]
    return out


def eyes_sparkle():
    return eyes_open() + [(8, 5, "W"), (8, 16, "W")]


def eyes_think():  # looking up-right
    cells = [(r, c, "E") for r in (6, 7, 8) for c in L_EYE + R_EYE]
    return cells + [(6, 5, "W"), (6, 16, "W")]


def eyes_wink():  # left open, right ^
    return eyes_open(L_EYE) + eyes_happy([R_EYE])


BLUSH = [(10, 2, "B"), (10, 3, "B"), (10, 16, "B"), (10, 17, "B")]

# ---------------- mouths (head space) ----------------
MOUTH_UU = [(10, 6, "K"), (10, 9, "K"), (10, 10, "K"), (10, 13, "K"),
            (11, 7, "K"), (11, 8, "K"), (11, 11, "K"), (11, 12, "K")]  # signature ω "uu"
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
NO_MOUTH = []

# ---------------- stamps: (canvas_x, canvas_y, rows) ----------------
PAW_CHIN = (15, 14, [".KKK.", "KLLLK", "KLLLK", ".KOOK", "..KOK", "..KOK"])
QMARK = (21, 0, [".YYY.", "Y...Y", "...Y.", "..Y..", ".....", "..Y.."])
BANG = (22, 0, ["YY", "YY", "YY", "YY", "..", "YY"])
SWEAT = (2, 7, [".N", "NN", "NN"])
ZZZ = (19, 0, ["NNNN...", "..N....", ".N..NNN", "NNNN..N", ".....N.", "....NNN"])
HEARTS = (20, 0, [".R.R..", "RRRRR.", ".RRR..", "..R.R.", "...RRR", "....R."])
SPARKS = (0, 0, ["..Y...................W...", ".YYY.................WWW..", "..Y...................W..."])
TWINKLE = (24, 2, [".Y.", "YWY", ".Y."])
NOTE = (23, 1, [".NN", ".NN", ".N.", "NN.", "NN."])
HEADPHONES = [  # band over the head between the ears + cups on the cheeks
    (6, 5, ["KKKKKKKKKKKKKK"]),
    (5, 6, ["KSSSSSSSSSSSSSSK"]),
    (4, 7, ["KSK", "KSK"]), (19, 7, ["KSK", "KSK"]),
    (2, 9, ["KKKK", "KGGK", "KGGK", "KGGK", "KKKK"]), (20, 9, ["KKKK", "KGGK", "KGGK", "KGGK", "KKKK"]),
]
BAG = (17, 15, ["...KKK...", "..K...K..", "KKKKKKKKK", "KYYYYYYYK", "KYYyYyYYK",
                "KYYYyYYYK", "KYYYYYYYK", "KyyyyyyyK", "KKKKKKKKK"])
BAG_PAW = (16, 17, ["KK", "LK"])
THUMB = (20, 13, ["..KK....", ".KLLK...", ".KLLK...", "KKLLKKK.", "KLLLLLLK",
                  "KLLLLLKK", "KLLLLLLK", "KLLLLLKK", ".KKKKKK."])  # 👍
THUMB_ARM = (18, 17, ["KK.", "OOK", "OOK", "KK."])
FISH = (6, 13, [".KKKKKK..KK.", "KNNNNNNK.KNK", "KNWENNNNKNNK", "KNNNNNNK.KNK", ".KKKKKK..KK."])
CRUMBS = (19, 17, ["..L.", "L...", "...L"])


def build(face, stamps=(), tail=True):
    """Compose a pose: head + body (+ tail), then face cells, then stamps."""
    g = [["."] * CW for _ in range(CH)]
    for r, row in enumerate(HEAD + BODY):
        for c, k in enumerate(row):
            if k != ".":
                g[r + HY][c + HX] = k
    for r, c, k in (TAIL if tail else []) + list(face):
        g[r + HY][c + HX] = k
    for x0, y0, rows in stamps:
        for dy, row in enumerate(rows):
            for dx, k in enumerate(row):
                if k != ".":
                    g[y0 + dy][x0 + dx] = k
    return ["".join(r) for r in g]


@dataclass(frozen=True)
class PoseSpec:
    eyes: list
    mouth: list                      # what the pose shows on the gallery sheet
    stamps: tuple = ()
    tail: bool = True
    talk: bool = True                # has a talking (open-mouth) frame
    rest_mouth: list = None          # mouth while idle in a video, if not `mouth`
    blink: bool = False              # has a blink frame (eyes are open)
    extra_face: list = field(default_factory=list)


# Display names are the names used in storylines. Order = gallery order.
POSE_SPECS = {
    "Senyum": PoseSpec(eyes_open(), MOUTH_UU, blink=True),
    "Teruja": PoseSpec(eyes_sparkle(), MOUTH_BIG, (SPARKS,), blink=True),
    "Jatuh cinta": PoseSpec(eyes_heart(), MOUTH_UU, (HEARTS,)),
    "Terkejut": PoseSpec(eyes_shock(), MOUTH_O, (BANG, SWEAT), talk=False),
    "Kenyit mata": PoseSpec(eyes_wink(), MOUTH_UU),
    "Berfikir": PoseSpec(eyes_think(), MOUTH_FLAT, (PAW_CHIN, QMARK)),
    "Tidur": PoseSpec(eyes_sleep(), MOUTH_SMALL, (ZZZ,), talk=False),
    "Layan lagu": PoseSpec(eyes_happy(), MOUTH_UU, (*HEADPHONES, NOTE)),
    "Shopping": PoseSpec(eyes_sparkle(), MOUTH_UU, (BAG, BAG_PAW), tail=False, blink=True),
    "Bercakap": PoseSpec(eyes_open(), MOUTH_TALK, rest_mouth=MOUTH_UU, blink=True),
    "Thumbs up": PoseSpec(eyes_wink(), MOUTH_UU, (THUMB_ARM, THUMB, TWINKLE)),
    "Makan": PoseSpec(eyes_happy(), NO_MOUTH, (FISH, CRUMBS, TWINKLE), talk=False, extra_face=BLUSH),
}


def pose_rows(name):
    """The pose as shown on the gallery sheet."""
    s = POSE_SPECS[name]
    return build(s.eyes + s.extra_face + s.mouth, s.stamps, s.tail)


def slug(name):
    return name.lower().replace(" ", "-")


def video_frames(name):
    """Frames a video can use for this pose: {"rest": rows, "talk": rows?, "blink": rows?}."""
    s = POSE_SPECS[name]
    rest_mouth = s.mouth if s.rest_mouth is None else s.rest_mouth
    frames = {"rest": build(s.eyes + s.extra_face + rest_mouth, s.stamps, s.tail)}
    if s.talk:
        talk_mouth = MOUTH_TALK if rest_mouth != MOUTH_TALK else MOUTH_UU
        frames["talk"] = build(s.eyes + s.extra_face + talk_mouth, s.stamps, s.tail)
    if s.blink:
        frames["blink"] = build(eyes_blink() + s.extra_face + rest_mouth, s.stamps, s.tail)
    return frames


POSES = {name: pose_rows(name) for name in POSE_SPECS}
