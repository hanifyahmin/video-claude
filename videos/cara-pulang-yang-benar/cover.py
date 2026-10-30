"""TikTok cover + post caption for the lyric video.

    python3 videos/cara-pulang-yang-benar/cover.py

Writes promo/thumbnail.png (1080x1920) and promo/caption.txt. The repo's promo
tool is built around a product and Oyen, so this cover is drawn with the video's
own renderer instead: the golden final-chorus photo (parent and child side by
side), the parent's line in handwriting as the hook, and the title in the serif.
Everything that matters sits inside the 3:4 grid crop (y 240-1680).
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import render as R

OUT = Path(__file__).with_name("promo")
T = 194.5                      # final chorus: gold, both figures solid

HOOK = "“Pulanglah sebentar saja”"
QUESTION = "Kapan terakhir kamu pulang?"

CAPTION = """Kapan terakhir kamu pulang? \U0001F3E0
“Pulanglah sebentar saja” — “Nanti, bila semua reda.”

Untuk kau yang masih punya waktu: peluklah mereka sebelum jadi abu.

\U0001F3A7 Cara Pulang yang Benar
Kirim ke seseorang yang perlu kamu telepon hari ini."""

HASHTAGS = ["#carapulangyangbenar", "#laguindonesia", "#indiefolk", "#lagusedih",
            "#rindurumah", "#orangtua", "#liriklagu", "#fyp"]


def text_layer(draw_fn):
    layer = Image.new("RGBA", (R.W, R.H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    return layer


def composite(canvas, layer, glow=None, glow_amt=0.0, shadow=0.75):
    lay = np.asarray(layer, np.float32)
    a = lay[..., 3:] / 255
    sh = np.asarray(layer.split()[3].filter(ImageFilter.GaussianBlur(10)), np.float32)[..., None] / 255
    canvas *= 1 - sh * shadow
    if glow is not None:
        g = np.asarray(glow.filter(ImageFilter.GaussianBlur(18)), np.float32)
        canvas += g[..., :3] * (g[..., 3:] / 255) * glow_amt
    return canvas * (1 - a) + lay[..., :3] * a


def centred(d, text, font, cy, fill, cx=540):   # a cover has no button column to avoid
    d.text((cx - font.getlength(text) / 2, cy), text, font=font, anchor="ls", fill=fill)


def main():
    s = R.state(T)
    s.update(rise=0.0, scale=0.92, frame_glow=0.9, drum=0.5, fade_out=1.0)
    R.FRAME_CY = 770                       # photo sits between the hook and the title
    B = R.backgrounds()
    canvas = B["warm"] * (0.92 + 0.12 * s["energy"])
    R.draw_particles(canvas, T, s)
    R.composite_frame(canvas, T, s)

    hook_font = R.font("caveat-Caveat.ttf", 96, 680)
    title_font = R.font("fraunces-Fraunces-Italic.ttf", 128, 440)
    q_font = R.font("fraunces-Fraunces.ttf", 50, 520)
    ink = tuple(int(c) for c in R.INK) + (255,)
    cream = tuple(int(c) for c in R.CREAM) + (255,)
    gold = tuple(int(c) for c in R.GOLD) + (255,)

    hook = text_layer(lambda d: centred(d, HOOK, hook_font, 330, ink))
    glow = text_layer(lambda d: centred(d, HOOK, hook_font, 330, (150, 190, 255, 160)))
    canvas = composite(canvas, hook, glow, 0.8)

    def title(d):
        centred(d, "Cara Pulang", title_font, 1330, cream)
        centred(d, "yang Benar", title_font, 1460, cream)
        centred(d, QUESTION, q_font, 1585, gold)
    tglow = text_layer(lambda d: (centred(d, "Cara Pulang", title_font, 1330, (255, 170, 80, 120)),
                                  centred(d, "yang Benar", title_font, 1460, (255, 170, 80, 120))))
    canvas = composite(canvas, text_layer(title), tglow, 0.6)

    canvas += R.grain()[0][..., None] * 0.15
    img = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
    OUT.mkdir(exist_ok=True)
    img.save(OUT / "thumbnail.png")
    caption = CAPTION.strip() + "\n\n" + " ".join(HASHTAGS) + "\n"
    (OUT / "caption.txt").write_text(caption, encoding="utf-8")
    print("wrote", OUT / "thumbnail.png", "and caption.txt", f"({len(caption)} chars)")


if __name__ == "__main__":
    main()
