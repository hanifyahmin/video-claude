"""Cover thumbnail + TikTok caption for tropika-herbal-cream. Make with the final render.

  python3 -m promo videos/tropika-herbal-cream   -> promo/thumbnail.png + promo/caption.txt

Only claim what the footage shows or the user confirmed.
"""
from promo import Promo

PROMO = Promo(
    frame_src=0.0,                    # source second with the best product shot
    frame_shift=0,                    # move the background up so the product clears the headline
    kicker="KULIT BABY KERING?",
    headline=["CUBA NI MOMMY!"],            # 1-3 lines, <= 14 chars each; *word* = yellow
    badge=None,                       # e.g. "MAX 50KG"
    pose="Teruja",
    bubble="Jom tengok!",
    caption=(
        "Hook soalan/masalah + 1 fakta produk + ajakan tekan beg kuning."
    ),
    hashtags=["#tiktokshopmalaysia", "#fyp", "#oyen"],
)
