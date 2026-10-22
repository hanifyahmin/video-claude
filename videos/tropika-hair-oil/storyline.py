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
from oyen.storyline import Beat, Layout, Storyline

STORYLINE = Storyline(
    title="Tropika Hair & Body Oil (18s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.7, "1 Hook", "Jalan", None,
             "Oyen berjalan masuk; botol berdiri + shake. Caption: Rambut baby / NIPIS?", src=77.5),
        Beat(0.7, 3.0, "1 Hook", "Terkejut", "Eh, kesian baby!",
             "Oyen terkejut (dialog 1/3); botol ditarik keluar dari kotak. Caption: Tropika I'm Rabby / "
             "HAIR & BODY OIL", src=40.2),
        Beat(3.0, 5.4, "2 Ramuan", "Menjilat", None,
             "Label belakang botol (VCO + rose), zoom; Oyen menjilat bulu. Caption: Minyak kelapa dara / + ROSE",
             src=44.5),
        Beat(5.4, 8.0, "3 Tanpa", "Duduk", "Fuh, padu ni!",
             "Teks BM belakang kotak, zoom (dialog 2/3). Caption: Tanpa bahan kimia / & PENGAWET", src=21.5),
        Beat(8.0, 10.4, "4 Fungsi", "Gembira", None,
             "Depan kotak (Rabby) + kilauan. Caption: Lembapkan kulit / RAMBUT SIHAT & LEBAT", src=3.0),
        Beat(10.4, 12.4, "5 Ikon", "Teruja", None,
             "Ikon Halal / Vegan / Not tested + 30ml. Caption: Tak diuji pada haiwan / HALAL & VEGAN", src=98.5),
        Beat(12.4, 15.0, "6 Buka", "Regang", None,
             "Pusing penutup (1.8x), botol terbuka. Caption: Saiz 30ml / MUDAH BAWA", src=59.0),
        Beat(15.0, 16.8, "7 CTA", "Duduk", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah) (dialog 3/3).", src=79.0),
        Beat(16.8, 18.0, "7 CTA", "Lari keluar", None,
             "Oyen meluru keluar dan melanggar bubble 'Jom checkout!'.", src=80.0),
    ],
    blinks=[7.4, 16.3],
    jumps=[],
    layout=Layout(style="bold"),
    character="tabby",
)
