"""Cover thumbnail + TikTok caption for TROPIKA I'm Rabby Baby Hair & Body Oil Sweet.

  python3 -m promo videos/tropika-hair-oil   -> promo/thumbnail.png + promo/caption.txt

Facts are from the printed label (VCO + rose, no chemicals/preservatives,
sensitive skin, healthy thick hair, Halal JAKIM, Vegan, Not Tested, 30ml).
"""
from promo import Promo

PROMO = Promo(
    frame_src=79.0,                   # bottle standing, front label square on
    kicker="Rambut baby",
    headline=["*nipis?*"],
    product_crop=(110, 0, 700, 1500), # bottle + thumb; the fingers behind fade out
    tags=("30ml",),
    pose="Jatuh cinta",
    bubble="Rambut lebat~",
    features=(("leaf", "Kelapa dara\n+ rose"), ("shield", "Tanpa\npengawet"), ("check", "Dijamin\nhalal")),
    caption=(
        "Rambut baby nipis? 🥺 Cuba Tropika I'm Rabby Baby Hair & Body Oil Sweet 🐰\n"
        "Minyak kelapa dara + rose, tanpa bahan kimia & pengawet. Bantu lembapkan kulit sensitif "
        "& galakkan rambut sihat dan lebat 💕 Halal, vegan, tak diuji pada haiwan. Saiz 30ml, mudah bawa. "
        "Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#tropika", "#babyoil", "#minyakrambutbaby", "#rambutbaby", "#mommyhacks",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
