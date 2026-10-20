"""Oyen storyline for the vacuum storage bag set (~22.6s).

Footage: assets/source-portrait.mp4 = the 10 phone clips joined in order (camera
sound removed). Clip offsets in the joined file:
  0.0   153051 set in its bag (bags + bubble-wrapped pump + adapter) 1-5.5
  8.27  153143 size labels: MINI 60x40 @1.0, S 70x50 @6.6, L 100x70 @12.6, LL 100x80 @18.0
  30.53 153226 unwrapping the pump 0-6.5
  40.4  153248 universal plug adapter 0.5-2.5, pump in hand 7-11
  53.4  153521 bag front + valve 1-7.5, printed steps 1 Seal / 2 Unlock / 3 Vacuum / 4 Lock 8-11.5
  66.87 153800 pump's 2-pin plug 1-4.5
  71.6  154023 closing the zip seal 0-12
  84.5  154154 opening the valve on a full bag 0-3.9
  88.43 154256 pump on the valve 1-3, bag shrinks 3-10, lock 14.5-18, flat bag 19-41
  130.2 154356 full bag, valve, zipping 9-18, puffy bag 19-22.9
Claims come from the labels/footage only: 4 sizes, pump + adapter in the set, the
printed 4 steps, and the bag going flat on camera.

  python3 -m oyen storyboard videos/vacuum-storage-bag
  python3 -m oyen install videos/vacuum-storage-bag
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="Vacuum Storage Bag (22.6s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.8, "1 Hook", "Terkejut", None,
             "Pam atas injap, beg kembung terus leper (3x). Caption: Baju penuh almari? / Sedut, terus leper!", src=91.9),
        Beat(0.8, 2.4, "1 Hook", "Teruja", "Wah, leper terus!",
             "Sambungan sedutan 3x sampai leper.", src=97.4),
        Beat(2.4, 4.4, "2 Set", "Senyum", "Set beg vakum~",
             "Pek set: beg + pam + adapter. Caption: Vacuum storage bag / satu set", src=3.0),
        Beat(4.4, 7.4, "3 Saiz", "Bercakap", "Ada 4 saiz tau!",
             "4 potongan label 0.75s: MINI 60x40 / S 70x50 / L 100x70 / LL 100x80 + cip saiz. Caption: 4 saiz / Mini sampai LL",
             src=9.27),
        Beat(7.4, 9.4, "4 Pam", "Jatuh cinta", "Siap ada pam!",
             "Pam elektrik dalam tangan + kilauan. Caption: Siap ada / pam elektrik", src=48.4),
        Beat(9.4, 11.0, "5 Plug", "Kenyit mata", "Plug pun ada~",
             "Plug 2 pin (0.7s) lalu adapter universal. Caption: Plug 2 pin? / Adapter ada!", src=41.4),
        Beat(11.0, 13.8, "6 Cara", "Bercakap", "Zip, buka injap",
             "Langkah 1 zip rapat (3x) + langkah 2 buka injap. Caption: 1 Zip rapat / 2 Buka injap", src=141.5),
        Beat(13.8, 17.2, "7 Sedut", "Teruja", "Sedut... siap!",
             "Langkah 3 pam di injap + langkah 4 kunci injap. Caption: 3 Sedut udara / 4 Kunci injap", src=89.6),
        Beat(17.2, 19.8, "8 Hasil", "Thumbs up", "Jimat ruang!",
             "Beg leper dipegang + inset SEBELUM (beg kembung). Caption: Jimat ruang / leper & kemas!", src=112.4),
        Beat(19.8, 22.0, "9 CTA", "Shopping", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah), beg leper di belakang.", src=127.0),
        Beat(22.0, 22.6, "9 CTA", "Kenyit mata", None,
             "Penutup: Oyen kenyit mata.", src=128.0),
    ],
    blinks=[3.4, 12.6],
    jumps=[0.8, 17.2],
)
