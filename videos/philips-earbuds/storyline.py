"""Oyen storyline for the Philips TAT1420 earbuds TikTok affiliate cut (18.2s).

Edit, then from the repo root:
  python3 -m oyen storyboard videos/philips-earbuds   # review
  python3 -m oyen install videos/philips-earbuds      # write into index.html
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="Philips earbuds (18.2s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.45, "1 Hook", "Tidur", None,
             "Oyen sudah ada di frame 0, tertidur (Zz) di sudut.", src=15.6),
        Beat(0.45, 2.2, "1 Hook", "Terkejut", "Eh?! Mahal ke ni?",
             "Lid terbuka + bass hit: Oyen terjaga, melompat, '!'.", src=16.6),
        Beat(2.2, 3.8, "2 Logo PHILIPS", "Kenyit mata", "Brand PHILIPS tau~",
             "Kenyit sambil logo + LED ditunjuk.", src=18.9),
        Beat(3.8, 5.5, "3 Tarik earbud", "Layan lagu", "Jom layan lagu~",
             "Headphone muncul (pop), not muzik bergoyang.", src=22.1),
        Beat(5.5, 8.8, "4 Close-up", "Jatuh cinta", "Cantiknya chrome~",
             "Mata love + hati terapung, serentak dengan kilauan.", src=37.8),
        Beat(8.8, 11.4, "5 Casing", "Bercakap", "Kecik, muat poket!",
             "Pose asas bercakap; ekor goyang.", src=4.0),
        Beat(11.4, 13.7, "6 Charge", "Teruja", "Charge guna USB-C!",
             "Mata bersinar, mulut ternganga, kilauan.", src=47.3),
        Beat(13.7, 14.55, "7 Tutup lid", "Senyum", None,
             "Oyen diam, tengok lid ditutup.", src=48.6),
        Beat(14.55, 15.3, "7 KLIK!", "Terkejut", None,
             "Lompat terkejut tepat pada bunyi KLIK.", src=49.0),
        Beat(15.3, 17.4, "8 CTA", "Shopping", "Jom checkout!",
             "Oyen pegang beg kuning, sebelah butang CTA.", src=50.3),
        Beat(17.4, 18.2, "8 CTA", "Thumbs up", None,
             "Penutup: thumbs up + kenyit, kilauan.", src=50.9),
    ],
    blinks=[10.3, 14.15],
    jumps=[0.45, 14.55],  # wakes at the lid-open hit, hops at the KLIK
)
