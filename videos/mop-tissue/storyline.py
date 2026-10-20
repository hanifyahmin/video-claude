"""Oyen storyline for the disposable-sheet floor mop set (~21s).

Footage: assets/source-portrait.mp4 = the 5 phone clips joined in order (camera
sound removed). Usable (joined-file seconds):
  set flat lay (mop head, poles, both sheet packs) 2-5.5
  "Tisu Basah" Super WET wiper sheet pack 6.2-9; dry sheet pack (30枚入, 200x300mm) 12-14.5
  mop head: top with 4 grip slots 18-20, textured pad 21; pole sections 26-28.5
  attach: sheet on floor 44-49, head placed 50-53, corners pushed into the slots 54-66,
          sheet held on 67-72; mopping 74-80
  detach: pull sheet out of the slots 92-100, used sheet crumpled in hand 100.5-102.5
  The rest is empty floor.
Claims come from the packs/footage only: 30 dry sheets (200x300mm) that catch dust
and hair (pack text), a wet-sheet pack, push-in corners, pull off and throw away.

  python3 -m oyen storyboard videos/mop-tissue
  python3 -m oyen install videos/mop-tissue
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="Mop Tisu Pakai Buang (21s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.8, "1 Hook", "Terkejut", None,
             "Mop dengan tisu ditolak atas lantai (2x). Caption: Malas cuci kain mop? / Pakai, terus buang!", src=75.0),
        Beat(0.8, 2.4, "1 Hook", "Teruja", "Mop pakai buang!",
             "Sambungan mop atas lantai.", src=77.5),
        Beat(2.4, 4.4, "2 Set", "Senyum", "Set lengkap~",
             "Flat lay: kepala mop, batang, 2 pek tisu. Caption: Satu set / mop + 2 jenis tisu", src=3.5),
        Beat(4.4, 6.4, "3 Kering", "Bercakap", "30 helai tau!",
             "Pek tisu kering (30 helai, 200x300mm). Caption: Tisu kering 30 helai / tangkap habuk & rambut", src=13.0),
        Beat(6.4, 8.2, "4 Basah", "Kenyit mata", "Basah pun ada~",
             "Pek Tisu Basah (Super WET wiper sheet). Caption: Ada tisu basah / untuk lap lantai", src=7.3),
        Beat(8.2, 10.2, "5 Kepala", "Berfikir", "Macam mana pasang?",
             "Kepala mop: 4 lubang penjepit, lalu pad bertekstur. Caption: Kepala mop / 4 penjepit tisu", src=19.0),
        Beat(10.2, 11.6, "6 Batang", "Senyum", None,
             "Batang disambung. Caption: Batang / boleh sambung", src=27.0),
        Beat(11.6, 15.6, "7 Pasang", "Bercakap", "Tekan je penjuru~",
             "Letak tisu (1x) -> letak kepala mop -> tekan 4 penjuru (3x) -> tisu siap terpasang. "
             "Caption ikut langkah: 1 Letak tisu / 2 Letak mop / 3 Tekan penjuru", src=60.0),
        Beat(15.6, 18.2, "8 Buang", "Thumbs up", "Tak payah cuci!",
             "Tarik tisu keluar dari penjepit (2.5x) -> tisu kotor digumpal dalam tangan. Caption: Dah kotor? / Tarik & buang!",
             src=101.7),
        Beat(18.2, 20.4, "9 CTA", "Shopping", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah), mop siap bertisu di belakang.", src=69.0),
        Beat(20.4, 21.0, "9 CTA", "Kenyit mata", None,
             "Penutup: Oyen kenyit mata.", src=70.0),
    ],
    blinks=[3.4, 13.0],
    jumps=[0.8, 15.6],
)
