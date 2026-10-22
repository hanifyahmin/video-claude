"""Oyen storyline for BZU BZU Baby Accessories Cleansing Foam 500ml (~22.4s).

Footage: assets/source-portrait.mp4 = the 6 phone clips joined in order (camera
sound removed). Usable (joined-file seconds):
  front label 0.5-3, 14-22 (steady 15.5-17.5); back label 3.5-13.5 (steady 6-8)
  sink + bottle 22-30; pump foam into the bottle 30.5-33.5 (foam stream 32-33);
  bottle brush 37.5-50; rinsing under the tap 50.5-57; rinsed bottle 58.5-60.5; bottle with milk residue (dirty) 65-69;
  clean, clear bottle 69.3-72.5
Claims come from the label only: for milk bottles, dish, toys, fruits & vegetables;
0% fragrance, bleaching agent & paraben, artificial colouring, soap & alcohol; no sulfate;
100% plant-based ingredients*; easy-to-rinse; foam pump saves water and washing time;
organic aloe vera juice + chamomile extract; mild and gentle to hands; fresh lemon
scent; Halal (JAKIM logo); 500ml. Formulated in Japan.

  python3 -m oyen storyboard videos/bzu-bzu-cleansing-foam
  python3 -m oyen install videos/bzu-bzu-cleansing-foam
"""
from oyen.storyline import Beat, Layout, Storyline

STORYLINE = Storyline(
    title="BZU BZU Cleansing Foam (22.4s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.8, "1 Hook", "Jalan", None,
             "Oyen berjalan masuk; buih dipam terus masuk botol susu. Caption: Cuci botol susu baby? / GUNA BUIH NI!",
             src=32.3),
        Beat(0.8, 2.4, "1 Hook", "Terkejut", "Banyaknya buih!",
             "Oyen terkejut (dialog 1/3).", src=32.9),
        Beat(2.4, 4.4, "2 Produk", "Teruja", None,
             "Label depan + kilauan. Caption: BZU BZU / CLEANSING FOAM 500ML", src=16.0),
        Beat(4.4, 6.6, "3 Untuk", "Gembira", None,
             "Zoom baris FOR MILK BOTTLES... Caption: Botol susu, pinggan, / MAINAN, BUAH & SAYUR", src=17.0),
        Beat(6.6, 9.0, "4 Bebas", "Duduk", "Takde pewangi pun!",
             "Zoom panel 0% + 4 cip (dialog 2/3). Caption: 0% pewangi, paraben, / PEWARNA & ALKOHOL", src=17.5),
        Beat(9.0, 11.2, "5 Bahan", "Menjilat", None,
             "Zoom 100% plant based. Caption: 100% bahan tumbuhan* / TANPA SULFAT & HALAL", src=18.0),
        Beat(11.2, 13.4, "6 Lembut", "Regang", None,
             "Label belakang: aloe vera + chamomile. Caption: Ada aloe vera & chamomile / LEMBUT DI TANGAN", src=6.8),
        Beat(13.4, 15.4, "7 Pam", "Makan", None,
             "Pam buih ke dalam botol. Caption: Pam terus jadi buih / JIMAT AIR & MASA", src=31.0),
        Beat(15.4, 17.6, "8 Berus", "Lompat", None,
             "Berus botol (2x) lalu bilas. Caption: Berus & bilas / MUDAH DIBILAS", src=40.5),
        Beat(17.6, 19.6, "9 Hasil", "Teruja", None,
             "Botol jernih + inset SEBELUM botol kotor. Caption: Bersih & / BAU LEMON SEGAR", src=71.2),
        Beat(19.6, 21.4, "10 CTA", "Duduk", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah) (dialog 3/3).", src=15.0),
        Beat(21.4, 22.4, "10 CTA", "Lari keluar", None,
             "Oyen meluru keluar dan melanggar bubble 'Jom checkout!'.", src=15.5),
    ],
    blinks=[8.4, 20.9],
    jumps=[],
    layout=Layout(style="bold"),
    character="tabby",
)
