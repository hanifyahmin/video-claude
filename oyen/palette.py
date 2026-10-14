"""Oyen's colour palette. Sprites are strings of these keys; '.' is transparent."""

PAL = {
    "K": (42, 22, 11),      # outline
    "O": (243, 146, 50),    # orange fur
    "D": (200, 97, 26),     # tabby stripe
    "H": (255, 182, 102),   # orange highlight
    "L": (255, 224, 181),   # cream (belly, paws)
    "P": (255, 143, 163),   # pink (ears, nose, tongue)
    "B": (255, 112, 140),   # blush
    "E": (27, 27, 27),      # eye
    "W": (255, 255, 255),   # eye sparkle
    "Y": (255, 214, 10),    # TikTok Shop yellow (beg kuning)
    "y": (204, 160, 0),     # yellow shade
    "G": (120, 128, 140),   # headphone grey
    "S": (55, 60, 70),      # headphone dark
    "R": (230, 57, 70),     # red (hearts)
    "N": (90, 200, 250),    # blue (notes, sweat, Zz, fish)
}

INK = "#2a160b"     # speech-bubble outline / text, same as PAL["K"]
PAPER = "#fffdf5"   # speech-bubble fill


def hexc(key):
    return "#%02x%02x%02x" % PAL[key]
