"""Cover thumbnail + TikTok caption for vacuum-storage-bag. Make with the final render.

  python3 -m promo videos/vacuum-storage-bag   -> promo/thumbnail.png + promo/caption.txt

Only claim what the footage shows or the user confirmed.
"""
from promo import Promo

PROMO = Promo(
    style="cute",
    frame_src=126.8,                  # flat, vacuumed bag of clothes, top-down, no hand
    cutout=False,                     # clear plastic on tiles: the background model drops it, so a photo card
    product_crop=(40, 160, 1000, 1200),
    kicker="Beg luggage tak muat?!",
    headline=["Sedut,", "*terus leper!*"],
    tags=("4 saiz",),
    pose="Teruja",
    bubble="Walaweh mantap do!",
    features=(("bag", "Siap ada\npam elektrik"), ("check", "Adapter\n3 pin"), ("star", "Mini\nsampai LL")),
    caption=(
        "Beg luggage tak muat?! 😩 Sedut dengan vacuum storage bag, terus leper! 🧳\n"
        "Satu set siap ada pam elektrik + adapter 3 pin (plug asal 2 pin). 4 saiz: Mini 60x40, S 70x50, "
        "L 100x70, LL 100x80 cm. Zip, pusing kiri, sedut, pusing kanan untuk lock. Nak buka balik pun senang. "
        "Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#vacuumbag", "#vacuumstoragebag", "#begvakum", "#travelhacks", "#packingtips",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
