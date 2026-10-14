"""Oyen storyline for the Philips earbuds TikTok edit.

BEATS is the plan: when Oyen is on screen, which pose, and what Oyen says.
Times are composition seconds on the approved 18.2s cut. `src` is the
matching source-portrait.mp4 time, used only for the storyboard thumbnail.

Run: python3 storyline.py <outdir>   -> writes oyen-storyboard.png
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import oyen_poses as P
from oyen_sprites import to_image

# (start, end, scene, pose, line or None, note, src)
BEATS = [
    (0.0, 0.45, "1 Hook", "Tidur", None,
     "Oyen sudah ada di frame 0, tertidur (Zz) di sudut.", 15.6),
    (0.45, 2.2, "1 Hook", "Terkejut", "Eh?! Mahal ke ni?",
     "Lid terbuka + bass hit: Oyen terjaga, melompat, '!'.", 16.6),
    (2.2, 3.8, "2 Logo PHILIPS", "Kenyit mata", "Brand PHILIPS tau~",
     "Kenyit sambil logo + LED ditunjuk.", 18.9),
    (3.8, 5.5, "3 Tarik earbud", "Layan lagu", "Jom layan lagu~",
     "Headphone muncul (pop), not muzik bergoyang.", 22.1),
    (5.5, 8.8, "4 Close-up", "Jatuh cinta", "Cantiknya chrome~",
     "Mata love + hati terapung, serentak dengan kilauan.", 37.8),
    (8.8, 11.4, "5 Casing", "Bercakap", "Kecik, muat poket!",
     "Pose asas bercakap; ekor goyang.", 4.0),
    (11.4, 13.7, "6 Charge", "Teruja", "Charge guna USB-C!",
     "Mata bersinar, mulut ternganga, kilauan.", 47.3),
    (13.7, 14.55, "7 Tutup lid", "Senyum", None,
     "Oyen diam, tengok lid ditutup.", 48.6),
    (14.55, 15.3, "7 KLIK!", "Terkejut", None,
     "Lompat terkejut tepat pada bunyi KLIK.", 49.0),
    (15.3, 17.4, "8 CTA", "Shopping", "Jom checkout!",
     "Oyen pegang beg kuning, sebelah butang CTA.", 50.3),
    (17.4, 18.2, "8 CTA", "Thumbs up", None,
     "Penutup: thumbs up + kenyit, kilauan.", 50.9),
]

UNUSED = ["Berfikir", "Makan"]


def frame(src, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(src), "-i",
                    str(Path(__file__).resolve().parent.parent / "assets/source-portrait.mp4"),
                    "-frames:v", "1", "-vf", "scale=360:640", str(out)], check=True)
    return Image.open(out).convert("RGB")


def render(outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    mono = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
    f_h, f_t, f_b, f_n = (ImageFont.truetype(bold, 30), ImageFont.truetype(bold, 24),
                          ImageFont.truetype(mono, 18), ImageFont.truetype(bold, 19))
    title = ImageFont.truetype(bold, 52)
    cols, cw, ch, pad = 4, 360, 640 + 150, 24
    rows = (len(BEATS) + cols - 1) // cols
    img = Image.new("RGB", (pad + cols * (cw + pad), 110 + rows * (ch + pad)), (17, 19, 24))
    d = ImageDraw.Draw(img)
    d.text((pad, 28), "Storyline Oyen — Philips earbuds (18.2s)", font=title, fill=(255, 214, 10))
    with tempfile.TemporaryDirectory() as tmp:
        for i, (a, b, scene, pose, line, note, src) in enumerate(BEATS):
            x0 = pad + (i % cols) * (cw + pad)
            y0 = 110 + (i // cols) * (ch + pad)
            img.paste(frame(src, Path(tmp) / f"{i}.png"), (x0, y0))
            d.rectangle((x0, y0, x0 + cw, y0 + 44), fill=(0, 0, 0))
            d.text((x0 + 10, y0 + 7), f"{a:g}–{b:g}s", font=f_h, fill=(255, 214, 10))
            d.text((x0 + 12 + d.textlength(f"{a:g}–{b:g}s", font=f_h) + 14, y0 + 10), f"· {scene}",
                   font=f_n, fill=(255, 255, 255))
            spr = to_image(P.POSES[pose], 4)
            sx, sy = x0 + 6, y0 + 640 - spr.height - 6
            img.paste(spr, (sx, sy), spr)
            if line:
                bx, by = sx + spr.width + 6, sy + 22
                bw = d.textlength(line, font=f_b) + 16
                bw = min(bw, x0 + cw - 6 - bx)
                d.rectangle((bx - 3, by - 3, bx + bw + 3, by + 33), fill=(42, 22, 11))
                d.rectangle((bx, by, bx + bw, by + 30), fill=(255, 253, 245))
                d.text((bx + 8, by + 5), line, font=f_b, fill=(42, 22, 11))
            d.rectangle((x0, y0 + 640, x0 + cw, y0 + ch), fill=(255, 248, 235))
            d.text((x0 + 12, y0 + 652), f"Postur: {pose}", font=f_t, fill=(42, 22, 11))
            # wrap the note
            words, lines, cur = note.split(), [], ""
            for w in words:
                t = (cur + " " + w).strip()
                if d.textlength(t, font=f_n) > cw - 24:
                    lines.append(cur)
                    cur = w
                else:
                    cur = t
            lines.append(cur)
            for j, ln in enumerate(lines[:4]):
                d.text((x0 + 12, y0 + 690 + j * 25), ln, font=f_n, fill=(90, 70, 55))
    path = outdir / "oyen-storyboard.png"
    img.save(path)
    return path


if __name__ == "__main__":
    print(render(sys.argv[1] if len(sys.argv) > 1 else "."))
