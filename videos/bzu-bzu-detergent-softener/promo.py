"""Cover thumbnail + TikTok caption for bzu-bzu-detergent-softener. Make with the final render.

  python3 -m promo videos/bzu-bzu-detergent-softener   -> promo/thumbnail.png + promo/caption.txt

Only claim what the footage shows or the user confirmed.
"""
from promo import Promo

PROMO = Promo(
    frame_src=1.6,                    # whole bottle front, held up
    kicker="Baju baby kena susu & muntah?",
    headline=["Cuci", "*dengan ni!*"],
    tags=("2 dalam 1",),
    pose="Teruja",
    bubble="Baju comot lagi?",
    features=(("sparkle", "Ada enzim\nbuang kesan"), ("leaf", ">99% bahan\nsemula jadi"), ("check", "Dijamin\nhalal")),
    caption=(
        "Baju baby kena susu & muntah? 😩 Cuci dengan BZU BZU Baby Laundry Detergent & Softener 2-in-1 👶\n"
        "Detergen + pelembut dalam satu. Sistem enzim untuk kesan susu, muntah & najis. Tanpa pewarna, peluntur & "
        "bahan kimia keras, diuji dermatologi. >99% bahan semula jadi, aloe vera & soapnut. Buih rendah, sesuai "
        "mesin top & front load. Halal, 1 liter. Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#bzubzu", "#detergentbaby", "#bajubaby", "#barangbaby", "#mommyhacks",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
