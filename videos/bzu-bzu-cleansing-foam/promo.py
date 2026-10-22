"""Cover thumbnail + TikTok caption for bzu-bzu-cleansing-foam. Make with the final render.

  python3 -m promo videos/bzu-bzu-cleansing-foam   -> promo/thumbnail.png + promo/caption.txt

Only claim what the footage shows or the user confirmed.
"""
from promo import Promo

PROMO = Promo(
    frame_src=0.0,                    # source second with the best product shot (background is cut away)
    product_crop=None,                # (x, y, w, h) to keep, e.g. to drop most of a holding hand; it fades at the edges
    kicker="Cuci botol susu baby?",              # white sticker line, sentence case looks cuter
    headline=["*Guna buih ni!*"],          # 1-3 lines, <= 14 chars each; a line with *word* is a yellow sticker
    tags=(),                          # up to 2 pink fact tags beside the product, e.g. ("30ml",)
    badge=None,                       # optional round sticker, e.g. "MAX 50KG"
    pose="Teruja",
    bubble="Jom tengok!",
    features=(),                      # up to 3 (icon, "line 1\nline 2"); icons: promo/icons.py
    caption=(
        "Hook soalan/masalah + 1 fakta produk + ajakan tekan beg kuning."
    ),
    hashtags=["#tiktokshopmalaysia", "#fyp", "#oyen"],
)
