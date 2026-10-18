"""Cover thumbnail + TikTok caption for the luggage scale video.

  python3 -m promo videos/luggage-scale
"""
from promo import Promo

PROMO = Promo(
    frame_src=171.0,                  # LCD lit, 0.00 kg
    cutout=False,                     # silver body on a grey wall: the background model drops it, so a photo card
    product_crop=(40, 620, 1000, 760),
    kicker="Nak fly?",
    headline=["Bagasi", "*overweight?*"],
    tags=("Max\n50kg",),
    pose="Terkejut",
    bubble="Timbang dulu!",
    features=(("sparkle", "Skrin LCD\nmenyala"), ("check", "Bateri\ndah ada"), ("star", "kg • lb\n°C • °F")),
    caption=(
        "Nak fly tapi takut bagasi overweight? 😱 Timbang dulu kat rumah! 🧳\n"
        "Luggage scale digital: max 50kg, skrin LCD menyala, bateri syiling dah disediakan. "
        "Tekan beg kuning untuk check harga ✈️"
    ),
    hashtags=["#luggagescale", "#timbangbagasi", "#travelmalaysia", "#barangtravel",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
