"""Cover thumbnail + TikTok caption for the luggage scale video.

  python3 -m promo videos/luggage-scale
"""
from promo import Promo

PROMO = Promo(
    frame_src=171.0,          # LCD lit, 0.00 kg
    frame_shift=60,
    kicker="NAK FLY?",
    headline=["BAGASI", "*OVERWEIGHT?*"],
    badge="MAX 50KG",
    pose="Terkejut",
    bubble="Timbang dulu!",
    caption=(
        "Nak fly tapi takut bagasi overweight? 😱 Timbang dulu kat rumah! 🧳\n"
        "Luggage scale digital: max 50kg, skrin LCD menyala, bateri syiling dah disediakan. "
        "Tekan beg kuning untuk check harga ✈️"
    ),
    hashtags=["#luggagescale", "#timbangbagasi", "#travelmalaysia", "#barangtravel",
              "#tiktokshopmalaysia", "#fyp", "#oyen"],
)
