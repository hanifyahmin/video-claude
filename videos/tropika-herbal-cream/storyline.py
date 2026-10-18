"""Oyen storyline for TROPIKA I'm Teddy Baby Herbal Cream (~20s).

Footage: assets/source-portrait.mp4 (85.7s, room noise removed). Usable:
front of tube 2-8s, back label + icons 17-23s, cap open + squeeze 32-36.5s,
rub on hand 38-42.5s / 55.5-61s, rubbed in 62-63.5s, tube + open hand 72.5-78s.
The rest is empty wall.

Claims come from the printed label only: VCO + tropical herbs, "membantu
melembapkan kulit bayi", "sapu lembut 3 kali sehari", Halal (JAKIM), Vegan,
Not Tested on Animals, Product of Malaysia. The Arabic text's treatment
claims (bloating, colds, fever) are NOT used.

  python3 -m oyen storyboard videos/tropika-herbal-cream
  python3 -m oyen install videos/tropika-herbal-cream
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="Tropika Baby Herbal Cream (20s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.6, "1 Hook", "Senyum", None,
             "Tiub muncul. Caption: KULIT BABY KERING? / CUBA NI MOMMY!", src=2.5),
        Beat(0.6, 2.4, "1 Hook", "Jatuh cinta", "Comelnya teddy ni!",
             "Close-up depan tiub (teddy) + kilauan.", src=4.0),
        Beat(2.4, 4.4, "2 Produk", "Teruja", "Krim herba baby!",
             "Push-in ke label depan. Caption: TROPIKA I'M TEDDY / BABY HERBAL CREAM", src=6.5),
        Beat(4.4, 7.4, "3 Ramuan", "Berfikir", "Ada apa dalam ni?",
             "Label belakang, senarai ramuan. Caption: MINYAK KELAPA DARA / + HERBA TROPIKA", src=17.5),
        Beat(7.4, 9.6, "4 Ikon", "Kenyit mata", "Halal & vegan~",
             "Ikon Halal / Vegan / Not tested. Caption: TAK DIUJI PADA HAIWAN / HALAL & VEGAN", src=21.0),
        Beat(9.6, 12.0, "5 Picit", "Senyum", None,
             "Buka penutup, picit atas tangan. Caption: TEKSTUR / KRIM PUTIH", src=34.5),
        Beat(12.0, 15.0, "6 Sapu", "Bercakap", "Sapu lembut je~",
             "Sapu atas tangan (laju sikit). Caption: SAPU LEMBUT / 3 KALI SEHARI", src=40.0),
        Beat(15.0, 17.0, "7 Rata", "Thumbs up", "Dah rata, siap!",
             "Krim dah rata atas tangan. Caption: BANTU LEMBAPKAN / KULIT BABY", src=62.5),
        Beat(17.0, 19.2, "8 CTA", "Shopping", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah), tiub + tangan di belakang.", src=74.0),
        Beat(19.2, 20.0, "8 CTA", "Kenyit mata", None,
             "Penutup: Oyen kenyit mata.", src=76.0),
    ],
    blinks=[10.8, 14.4],
    jumps=[0.6],
)
