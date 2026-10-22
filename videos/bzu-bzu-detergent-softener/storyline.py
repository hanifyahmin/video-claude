"""Oyen storyline for BZU BZU Baby Laundry Detergent and Softener 2-in-1, 1 litre (~19.8s).

Footage: assets/source-portrait.mp4 = the 3 phone clips joined in order (camera
sound removed). It is all label, no washing demo:
  whole bottle front 0.5-3; front label close 3.5-8 (name + bullets 4.5-7);
  front lower: Halal logo + icon row (>99% / enzymes / aloe vera / soapnut / 1 litre) 9-12.5;
  back: whole 13-15; text + feature boxes 19.5-25 (steady 21-23); boxes + ingredients 25-31;
  directions (pre-treat, full load 2 caps / half load 1 cap, top & front load) 32.5-40
Claims come from the label only: detergent + softener 2-in-1; long-lasting fragrance &
freshness; removes stubborn stains & odour; enzyme system for milk spills, spit-up and poop
smears; free from dyes, bleaching agent & harsh chemicals; dermatologist-tested;
plant-based surfactants gentle for newborns & sensitive skin; organic aloe vera; soapnut
extract (natural softener); low suds, gentle to fabrics & washing machines; >99% naturally
derived ingredients; Halal (JAKIM); 1 litre; dosing as printed.

  python3 -m oyen storyboard videos/bzu-bzu-detergent-softener
  python3 -m oyen install videos/bzu-bzu-detergent-softener
"""
from oyen.storyline import Beat, Layout, Storyline

STORYLINE = Storyline(
    title="BZU BZU Detergent 2-in-1 (19.8s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.8, "1 Hook", "Terkejut", None,
             "Botol penuh, zoom masuk + shake. Caption: Baju baby kena susu & muntah? / Cuci dengan ni!", src=1.5),
        Beat(0.8, 2.4, "1 Hook", "Teruja", "Baju comot lagi?",
             "Sambungan zoom ke label.", src=2.5),
        Beat(2.4, 4.6, "2 Produk", "Senyum", "2 dalam 1 tau!",
             "Nama produk pada label depan + kilauan. Caption: BZU BZU Baby · 1 liter / Detergen + pelembut", src=4.8),
        Beat(4.6, 7.0, "3 Enzim", "Bercakap", "Ada enzim tau!",
             "Teks belakang (milk spills, spit-up, poop smears), zoom ikut. Caption: Kesan susu, muntah / & najis pun hilang", src=21.5),
        Beat(7.0, 9.4, "4 Lembut", "Jatuh cinta", "Lembut untuk baby~",
             "Bullet depan: bebas pewarna, peluntur, bahan kimia keras + Dermatologist-tested. "
             "Caption: Tanpa pewarna & peluntur / Diuji dermatologi", src=6.0),
        Beat(9.4, 11.8, "5 Bahan", "Kenyit mata", "Halal pulak tu~",
             "Logo Halal + baris ikon (>99%, enzim, aloe vera, soapnut) + kilauan. Caption: >99% bahan semula jadi / Aloe vera & soapnut", src=10.5),
        Beat(11.8, 13.8, "6 Pelembut", "Senyum", None,
             "Kotak Soapnut + Low Suds. Caption: Soapnut, pelembut semula jadi / Mesra mesin basuh", src=26.5),
        Beat(13.8, 16.4, "7 Cara", "Bercakap", "Mesin apa pun ok!",
             "Arahan: penuh 2 penutup, separuh 1 penutup, top & front load. Caption: Penuh 2 penutup, separuh 1 / Top & front load",
             src=36.0),
        Beat(16.4, 19.2, "8 CTA", "Shopping", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah), botol di belakang.", src=2.0),
        Beat(19.2, 19.8, "8 CTA", "Kenyit mata", None,
             "Penutup: Oyen kenyit mata.", src=2.5),
    ],
    blinks=[3.4, 12.6],
    jumps=[0.8, 9.4],
    layout=Layout(style="bold"),
)
