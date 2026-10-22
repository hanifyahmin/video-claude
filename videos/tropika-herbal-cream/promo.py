"""Cover thumbnail + TikTok caption for TROPIKA I'm Teddy Baby Herbal Cream.

  python3 -m promo videos/tropika-herbal-cream   -> promo/thumbnail.png + promo/caption.txt

Hook is the user's; facts are from the label (ingredients, Halal, Vegan,
Not Tested on Animals) and the rub test shown in the video.
"""
from promo import Promo

PROMO = Promo(
    style="cute",
    frame_src=6.0,                    # front of the tube, teddy label square on
    product_crop=(60, 150, 820, 1550),  # tube; the holding hand fades out
    kicker="Perut baby asyik",
    headline=["*masuk angin?*"],
    tags=("Dijamin\nhalal",),         # Halal JAKIM logo on the label
    pose="Teruja",
    bubble="Cuba ni mommy!",
    features=(("leaf", "Halia &\nmentol"), ("drop", "Terus\nmeresap"), ("heart", "Tak diuji\npada haiwan")),
    caption=(
        "Perut baby asyik masuk angin? 😣 Cuba krim herba Tropika I'm Teddy 🧸\n"
        "Ada minyak kelapa dara + halia, eucalyptus & mentol. Sapu lembut, terus meresap, tak berbekas ✨ "
        "Halal & vegan, tak diuji pada haiwan. Tekan beg kuning untuk check harga promo 💛"
    ),
    hashtags=["#tropika", "#babyherbalcream", "#krimbaby", "#perutmasukangin", "#mommyhacks",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
