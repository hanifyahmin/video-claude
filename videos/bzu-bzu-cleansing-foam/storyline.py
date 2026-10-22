"""Oyen storyline for BZU BZU Baby Accessories Cleansing Foam 500ml (~22.4s).

Footage: assets/source-portrait.mp4 = the 6 phone clips joined in order (camera
sound removed). Usable (joined-file seconds):
  front label 0.5-3, 14-22 (steady 15.5-17.5); back label 3.5-13.5 (steady 6-8)
  sink + bottle 22-30; pump foam into the bottle 30.5-33.5 (foam stream 32-33);
  bottle brush 37.5-50; rinsing under the tap 50.5-57; clean bottle held up 58.5-60.5,
  65-72.5 (graduations visible 66-68)
Claims come from the label only: for milk bottles, dish, toys, fruits & vegetables;
0% fragrance, bleaching agent & paraben, artificial colouring, soap & alcohol; no sulfate;
100% plant-based ingredients*; easy-to-rinse; foam pump saves water and washing time;
organic aloe vera juice + chamomile extract; mild and gentle to hands; fresh lemon
scent; Halal (JAKIM logo); 500ml. Formulated in Japan.

  python3 -m oyen storyboard videos/bzu-bzu-cleansing-foam
  python3 -m oyen install videos/bzu-bzu-cleansing-foam
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="BZU BZU Cleansing Foam (22.4s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.8, "1 Hook", "Terkejut", None,
             "Pam buih terus masuk botol susu (1x). Caption: Cuci botol susu baby? / Guna buih ni!", src=32.3),
        Beat(0.8, 2.4, "1 Hook", "Teruja", "Buih terus keluar!",
             "Sambungan pam buih.", src=32.9),
        Beat(2.4, 4.4, "2 Produk", "Senyum", "BZU BZU tau~",
             "Label depan + kilauan. Caption: BZU BZU / Cleansing foam 500ml", src=16.0),
        Beat(4.4, 6.6, "3 Untuk", "Bercakap", "Bukan botol je!",
             "Zoom baris FOR MILK BOTTLES... Caption: Botol susu, pinggan, / mainan, buah & sayur", src=17.0),
        Beat(6.6, 9.0, "4 Bebas", "Jatuh cinta", "Takde pewangi pun!",
             "Zoom panel 0% + 4 cip: pewangi / paraben / pewarna / alkohol. Caption: 0% pewangi, paraben, / pewarna & alkohol",
             src=17.5),
        Beat(9.0, 11.2, "5 Bahan", "Kenyit mata", "Halal pulak tu~",
             "Zoom 100% plant based + logo Halal. Caption: 100% bahan tumbuhan* / Tanpa sulfat & halal", src=18.0),
        Beat(11.2, 13.4, "6 Lembut", "Senyum", None,
             "Label belakang: aloe vera + chamomile. Caption: Ada aloe vera & chamomile / Lembut di tangan", src=6.8),
        Beat(13.4, 15.4, "7 Pam", "Bercakap", "Pam je, jadi buih",
             "Pam buih ke dalam botol. Caption: Pam terus jadi buih / Jimat air & masa", src=31.0),
        Beat(15.4, 17.6, "8 Berus", "Teruja", "Berus, bilas, siap!",
             "Berus botol (2x) lalu bilas bawah paip. Caption: Berus & bilas / Mudah dibilas", src=40.5),
        Beat(17.6, 19.6, "9 Hasil", "Thumbs up", "Wangi lemon~",
             "Botol bersih diangkat + kilauan. Caption: Bersih & / bau lemon segar", src=66.5),
        Beat(19.6, 21.8, "10 CTA", "Shopping", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah), botol foam di belakang.", src=15.0),
        Beat(21.8, 22.4, "10 CTA", "Kenyit mata", None,
             "Penutup: Oyen kenyit mata.", src=15.5),
    ],
    blinks=[3.4, 12.2],
    jumps=[0.8, 17.6],
)
