"""Cover thumbnail + TikTok caption for mop-tissue. Make with the final render.

  python3 -m promo videos/mop-tissue   -> promo/thumbnail.png + promo/caption.txt

Only claim what the footage shows or the user confirmed.
"""
from promo import Promo

PROMO = Promo(
    frame_src=78.0,                   # whole mop with a sheet fitted, on the floor
    cutout=False,                     # white mop on pale tiles: shown as a photo card
    product_crop=(0, 560, 1080, 1000),
    kicker="Malas cuci kain mop?",
    headline=["Pakai,", "*terus buang!*"],
    tags=("30 helai",),
    pose="Teruja",
    bubble="Tak payah cuci!",
    features=(("sparkle", "Tangkap\nhabuk"), ("drop", "Ada tisu\nbasah"), ("check", "Tekan\npenjuru je")),
    caption=(
        "Malas cuci kain mop? 😮‍💨 Pakai tisu, dah kotor tarik & terus buang! 🧹\n"
        "Satu set: kepala mop + batang + tisu kering 30 helai (tangkap habuk & rambut) + tisu basah untuk lap lantai. "
        "Pasang senang: letak tisu, letak mop, tekan 4 penjuru. "
        "Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#mop", "#moppakaibuang", "#tisumop", "#cleaninghacks", "#rumahbersih",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
