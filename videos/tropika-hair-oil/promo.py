"""Cover thumbnail + TikTok caption for TROPIKA I'm Rabby Baby Hair & Body Oil Sweet.

  python3 -m promo videos/tropika-hair-oil   -> promo/thumbnail.png + promo/caption.txt

Facts are from the printed label (VCO + rose, no chemicals/preservatives,
sensitive skin, healthy thick hair, Halal JAKIM, Vegan, Not Tested, 30ml).
"""
from promo import Promo

PROMO = Promo(
    frame_src=79.0,                   # bottle standing, front label square on
    frame_shift=-260,                 # bottle moves down: label clears the headline
    kicker="RAMBUT BABY",
    headline=["*NIPIS?*"],
    badge="DIJAMIN HALAL",
    badge_xy=(790, 860),
    pose="Jatuh cinta",
    bubble="Rambut lebat~",
    caption=(
        "Rambut baby nipis? 🥺 Cuba Tropika I'm Rabby Baby Hair & Body Oil Sweet 🐰\n"
        "Minyak kelapa dara + rose, tanpa bahan kimia & pengawet. Bantu lembapkan kulit sensitif "
        "& galakkan rambut sihat dan lebat 💕 Halal, vegan, tak diuji pada haiwan. Saiz 30ml, mudah bawa. "
        "Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#tropika", "#babyoil", "#minyakrambutbaby", "#rambutbaby", "#mommyhacks",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
