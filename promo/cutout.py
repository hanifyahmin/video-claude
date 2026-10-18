"""Product cut-out for the cute cover: background removal, crop, edge fade and a baked white outline."""
import subprocess

from PIL import Image, ImageChops, ImageFilter

HF = "hyperframes@0.8.150"
OUTLINE = 9        # px: white sticker outline around the cut-out product, at cover size
PRODUCT_FIT = 760  # px: the cute cover fits the product into this square (see cute.py #product)
EDGE_FADE = 180  # px: whatever the cut-out keeps at a crop/frame edge (a wrist, a hand) fades out instead of ending in a straight line


def _edge_fade(alpha):
    """Mask that fades the sides the subject touches; sides it doesn't touch stay untouched."""
    w, h = alpha.size
    down = Image.linear_gradient("L")      # black at the top -> white at the bottom
    left = down.rotate(90)                 # black at the left
    mask = Image.new("L", alpha.size, 255)
    sides = {
        "left": ((0, 0, 2, h), left.resize((EDGE_FADE, h)), (0, 0)),
        "right": ((w - 2, 0, w, h), left.transpose(Image.FLIP_LEFT_RIGHT).resize((EDGE_FADE, h)), (w - EDGE_FADE, 0)),
        "top": ((0, 0, w, 2), down.resize((w, EDGE_FADE)), (0, 0)),
        "bottom": ((0, h - 2, w, h), down.transpose(Image.FLIP_TOP_BOTTOM).resize((w, EDGE_FADE)), (0, h - EDGE_FADE)),
    }
    for edge, strip, at in sides.values():
        if alpha.crop(edge).getextrema()[1] > 24:
            band = Image.new("L", alpha.size, 255)
            band.paste(strip, at)
            mask = ImageChops.darker(mask, band)
    return mask


def _pad(img, pad, edge=False):
    """Grow img by pad px per side: transparent/black, or (edge=True) repeating its border pixels."""
    w, h = img.size
    out = Image.new(img.mode, (w + 2 * pad, h + 2 * pad))
    out.paste(img, (pad, pad))
    if edge:
        out.paste(img.crop((0, 0, w, 1)).resize((w, pad)), (pad, 0))
        out.paste(img.crop((0, h - 1, w, h)).resize((w, pad)), (pad, h + pad))
        out.paste(out.crop((pad, 0, pad + 1, h + 2 * pad)).resize((pad, h + 2 * pad)), (0, 0))
        out.paste(out.crop((w + pad - 1, 0, w + pad, h + 2 * pad)).resize((pad, h + 2 * pad)), (w + pad, 0))
    return out


def cut_out(frame, out, crop=None):
    """Remove the frame's background (HyperFrames' local model), crop to the product and give it a white
    sticker outline. The model is trained on people: check the result, and when it keeps the hands but drops
    the product, use the photo card instead (Promo.cutout=False). The outline is baked in here, not drawn in CSS, so it fades out with a cut-off hand too."""
    raw = out.with_name("cut-raw.png")
    subprocess.run(["npx", "--yes", HF, "remove-background", str(frame), "-o", str(raw)],
                   check=True, capture_output=True, text=True)
    im = Image.open(raw).convert("RGBA")
    raw.unlink()
    if crop:
        x, y, w, h = crop
        im = im.crop((x, y, x + w, y + h))
    alpha = im.getchannel("A")
    box = alpha.point(lambda a: 255 if a > 24 else 0).getbbox()
    if not box:
        raise RuntimeError(f"background removal found no product in {frame}")
    fade = _edge_fade(alpha)
    # outline width in source px so it shows ~OUTLINE px once the product is fitted into the cover
    grow = round(OUTLINE / min(PRODUCT_FIT / (box[2] - box[0]), PRODUCT_FIT / (box[3] - box[1]), 1))
    pad = grow * 2
    im, alpha, fade = _pad(im, pad), _pad(alpha, pad), _pad(fade, pad, edge=True)
    hard = alpha.point(lambda a: 255 if a > 128 else 0)
    ring = hard.filter(ImageFilter.GaussianBlur(grow / 2)).point(lambda a: 255 if a > 8 else 0)
    sticker = Image.new("RGBA", im.size, (255, 255, 255, 0))
    sticker.putalpha(ImageChops.multiply(ring.filter(ImageFilter.GaussianBlur(1.2)), fade))
    im.putalpha(ImageChops.multiply(alpha, fade))
    sticker.alpha_composite(im)
    sticker.crop(sticker.getchannel("A").point(lambda a: 255 if a > 24 else 0).getbbox()).save(out)



def photo_card(frame, out, crop=None):
    """No background removal: the (cropped) frame itself, shown as a rounded photo sticker."""
    im = Image.open(frame).convert("RGB")
    if crop:
        x, y, w, h = crop
        im = im.crop((x, y, x + w, y + h))
    im.save(out)
