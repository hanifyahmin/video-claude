"""Cover thumbnail + TikTok caption for bzu-bzu-cleansing-foam. Make with the final render.

  python3 -m promo videos/bzu-bzu-cleansing-foam   -> promo/thumbnail.png + promo/caption.txt

Only claim what the footage shows or the user confirmed.
"""
from promo import Promo

PROMO = Promo(
    style="bold",
    niche="baby",
    frame_src=1.2,                    # bottle front, whole label, held over the sink
    frame_shift=-320,                 # bottle moves down: the hook headline gets the top
    kicker="Cuci botol susu baby?",
    headline=["Guna", "*buih ni!*"],
    badge="0% pewangi",               # printed on the label
    tags=("500ml",),
    character="tabby",
    pose="Terkejut",
    bubble="Banyaknya buih!",
    caption=(
        "Cuci botol susu baby? 🍼 Guna BZU BZU Baby Accessories Cleansing Foam, pam terus jadi buih! 🫧\n"
        "Untuk botol susu, pinggan, mainan, buah & sayur. 0% pewangi, bahan peluntur & paraben, pewarna tiruan, "
        "sabun & alkohol. Tanpa sulfat, 100% bahan tumbuhan*, ada aloe vera & chamomile, lembut di tangan, "
        "mudah dibilas, bau lemon segar. Halal, 500ml. Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#bzubzu", "#botolsusu", "#cucibotolsusu", "#barangbaby", "#mommyhacks",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
