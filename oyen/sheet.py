"""Gallery of every pose: oyen/gallery/poses/ (one PNG per pose + a sheet)."""
from pathlib import Path

from PIL import Image, ImageDraw

from .character import CH, CW, POSES, slug
from .render import font, paste_with_shadow, to_image

GALLERY = Path(__file__).resolve().parent / "gallery" / "poses"
TABBY_GALLERY = Path(__file__).resolve().parent / "gallery" / "tabby"


def render(out=GALLERY, cols=4, scale=14):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("oyen-pose-*.png"):
        old.unlink()
    f_label, f_title = font(38), font(56)
    cw, ch, pad = CW * scale + 60, CH * scale + 110, 28
    rows = (len(POSES) + cols - 1) // cols
    img = Image.new("RGB", (pad + cols * (cw + pad), 120 + rows * (ch + pad)), (17, 19, 24))
    d = ImageDraw.Draw(img)
    d.text((pad, 30), "Oyen — pelbagai postur", font=f_title, fill=(255, 214, 10))
    for i, (name, sprite_rows) in enumerate(POSES.items()):
        spr = to_image(sprite_rows, scale)
        spr.save(out / f"oyen-pose-{i + 1:02d}-{slug(name)}.png")
        x0, y0 = pad + (i % cols) * (cw + pad), 120 + (i // cols) * (ch + pad)
        d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=26, fill=(255, 248, 235))
        paste_with_shadow(img, spr, (x0 + 30, y0 + 22))
        label = f"{i + 1}. {name}"
        d.text((x0 + (cw - d.textlength(label, font=f_label)) / 2, y0 + ch - 68), label, font=f_label,
               fill=(42, 22, 11))
    img.save(out / "oyen-postur.png")
    return out / "oyen-postur.png"


def render_tabby(out=TABBY_GALLERY, scale=4):
    """Oyen v2: one row per animation, every frame on a shared floor line."""
    from . import tabby

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    w, h = tabby.cell()
    cw, ch, pad, label_w = w * scale, h * scale, 16, 260
    names = list(tabby.anims())
    most = max(len(a["frames"]) for a in tabby.anims().values())
    img = Image.new("RGB", (label_w + most * (cw + pad) + pad, 120 + len(names) * (ch + pad)), (30, 33, 40))
    d = ImageDraw.Draw(img)
    f_title, f_label, f_small = font(56), font(36), font(22)
    d.text((pad, 30), "Oyen v2 — animasi", font=f_title, fill=(255, 214, 10))
    for r, name in enumerate(names):
        spec = tabby.anims()[name]
        y0 = 120 + r * (ch + pad)
        d.text((pad, y0 + ch // 2 - 30), name, font=f_label, fill=(255, 255, 255))
        kind = "ulang" if spec.get("loop") else "sekali"
        d.text((pad, y0 + ch // 2 + 14), f"{len(spec['frames'])} frame · {kind}", font=f_small, fill=(170, 175, 190))
        for i in range(len(spec["frames"])):
            x0 = label_w + i * (cw + pad)
            d.rectangle((x0, y0, x0 + cw, y0 + ch), fill=(40, 44, 53))
            im = tabby.frame_image(name, i + 1, scale)
            img.paste(im, (x0, y0), im)
        tabby.trimmed(name, scale=8).save(out / f"oyen-tabby-{name.lower()}.png")
    img.save(out / "oyen-tabby-animasi.png")
    return out / "oyen-tabby-animasi.png"
