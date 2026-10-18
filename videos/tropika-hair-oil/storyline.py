"""Oyen storyline for TROPIKA I'm Rabby Baby Hair & Body Oil Sweet (~18s).

Footage: assets/source-portrait.mp4 (105s, camera sound removed). Usable:
box front 1-7s, box back text + icons 20.5-24.5s, unboxing 32-43s (bottle
slides out 38.8-41.5s), bottle back 43.5-47.5s, cap twist 54-58.5s, open
bottle 58.5-62s, bottle front standing 76-81.5s,
bottle back icons + 30ml 94-100.5s. The rest is empty wall. No use demo.

Claims come from the printed label: virgin coconut oil + rose, "tanpa sebarang
bahan kimia dan pengawet", "melembapkan kulit sensitif, melindungi kulit
daripada kering", "pertumbuhan rambut yang sihat dan lebat", Halal (JAKIM),
Vegan, Not Tested on Animals, 30ml.

  python3 -m oyen storyboard videos/tropika-hair-oil
  python3 -m oyen install videos/tropika-hair-oil
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="Tropika Hair & Body Oil (18s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 1.4, "1 Hook", "Terkejut", None,
             "Botol berdiri + shake. Caption: RAMBUT BABY / NIPIS?", src=77.5),
        Beat(1.4, 3.0, "1 Hook", "Teruja", "Jom tengok ni!",
             "Botol ditarik keluar dari kotak (1.5x). Caption: TROPIKA I'M RABBY / HAIR & BODY OIL", src=40.2),
        Beat(3.0, 5.4, "2 Ramuan", "Bercakap", "Ada rose tau~",
             "Label belakang botol. Caption: MINYAK KELAPA DARA / + ROSE", src=45.0),
        Beat(5.4, 8.0, "3 Tanpa", "Senyum", "Tanpa pengawet!",
             "Teks BM belakang kotak, zoom. Caption: TANPA BAHAN KIMIA / & PENGAWET", src=21.5),
        Beat(8.0, 10.4, "4 Fungsi", "Jatuh cinta", "Rambut lebat~",
             "Depan kotak (Rabby) + kilauan. Caption: LEMBAPKAN KULIT / RAMBUT SIHAT & LEBAT", src=3.0),
        Beat(10.4, 12.4, "5 Ikon", "Kenyit mata", "Halal & vegan~",
             "Ikon Halal / Vegan / Not tested + 30ml. Caption: TAK DIUJI PADA HAIWAN / HALAL & VEGAN", src=98.5),
        Beat(12.4, 15.0, "6 Buka", "Bercakap", "Kecik je, 30ml!",
             "Pusing penutup (1.7x), botol terbuka. Caption: SAIZ 30ML / MUDAH BAWA", src=59.0),
        Beat(15.0, 17.2, "7 CTA", "Shopping", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah), botol di belakang.", src=79.0),
        Beat(17.2, 18.0, "7 CTA", "Kenyit mata", None,
             "Penutup: Oyen kenyit mata.", src=80.0),
    ],
    blinks=[6.6, 13.6],
    jumps=[1.4, 15.0],
)
