"""Cover thumbnail + TikTok caption for TROPIKA I'm Rabby Baby Hair & Body Oil Sweet.

  python3 -m promo videos/tropika-hair-oil   -> promo/thumbnail.png + promo/caption.txt

Facts are from the printed label (VCO + rose, no chemicals/preservatives,
sensitive skin, healthy thick hair, Halal JAKIM, Vegan, Not Tested, 30ml).
"""
from promo import Promo

PROMO = Promo(
    style="bold",
    niche="baby",
    frame_src=79.0,                   # bottle standing, front label square on
    frame_shift=-220,                 # bottle moves down: the hook headline gets the top
    kicker="Mommy, tengok ni!",
    headline=["Rambut baby", "*nipis?*"],
    badge="Tanpa pengawet",           # printed on the box: tanpa sebarang bahan kimia dan pengawet
    tags=("30ml",),
    character="tabby",
    pose="Terkejut",
    bubble="Eh, kesian baby!",
    caption=(
        "Rambut baby nipis? 🥺 Cuba Tropika I'm Rabby Baby Hair & Body Oil Sweet 🐰\n"
        "Minyak kelapa dara + rose, tanpa bahan kimia & pengawet. Bantu lembapkan kulit sensitif "
        "& galakkan rambut sihat dan lebat 💕 Halal, vegan, tak diuji pada haiwan. Saiz 30ml, mudah bawa. "
        "Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#tropika", "#babyoil", "#minyakrambutbaby", "#rambutbaby", "#mommyhacks",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
