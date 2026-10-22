"""Cover thumbnail + TikTok caption for bzu-bzu-detergent-softener. Make with the final render.

  python3 -m promo videos/bzu-bzu-detergent-softener   -> promo/thumbnail.png + promo/caption.txt

Only claim what the footage shows or the user confirmed.
"""
from promo import Promo

PROMO = Promo(
    style="bold",
    niche="baby",
    frame_src=1.6,                    # whole bottle front, held up
    frame_shift=-180,                 # bottle moves down: the hook headline gets the top
    kicker="Kesan susu & muntah?",
    headline=["Baju baby", "*comot?*"],
    badge="2-in-1",                   # detergent + softener, as printed on the label
    tags=("1 liter",),
    pose="Terkejut",
    bubble="Ada enzim tau!",
    caption=(
        "Baju baby kena susu & muntah? 😩 Cuci dengan BZU BZU Baby Laundry Detergent & Softener 2-in-1 👶\n"
        "Detergen + pelembut dalam satu. Sistem enzim untuk kesan susu, muntah & najis. Tanpa pewarna, peluntur & "
        "bahan kimia keras, diuji dermatologi. >99% bahan semula jadi, aloe vera & soapnut. Buih rendah, sesuai "
        "mesin top & front load. Halal, 1 liter. Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#bzubzu", "#detergentbaby", "#bajubaby", "#barangbaby", "#mommyhacks",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
