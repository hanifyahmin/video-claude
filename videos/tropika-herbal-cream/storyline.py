"""Oyen storyline for TROPIKA I'm Teddy Baby Herbal Cream (~20s).

Footage: assets/source-portrait.mp4 (85.7s, room noise removed). Usable:
front of tube 2-8s, back label + icons 17-23s, cap open + squeeze 32-36.5s,
rub #1 38-42.5s, rub #2: dot on skin 54.5-55.5s, rubbing 55.5-61s, clean fist
61.5s, open hand with no residue 62-63.5s, tube + open hand 72.5-78s.
The rest is empty wall.

Claims come from the printed label: VCO + tropical herbs, ingredients
(ginger, eucalyptus, menthol, citronella), "membantu melembapkan kulit bayi",
"sapu lembut 3 kali sehari", Halal (JAKIM), Vegan, Not Tested on Animals.
The wind hook ("perut baby asyik masuk angin?") is the user's; the label's
Arabic text names bloating (النفخ). Absorption is shown, not claimed: the
rub scene runs dot -> rubbing (fast-forward) -> same hand clean.

  python3 -m oyen storyboard videos/tropika-herbal-cream
  python3 -m oyen install videos/tropika-herbal-cream
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="Tropika Baby Herbal Cream (20s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.6, "1 Hook", "Terkejut", None,
             "Tiub muncul + shake. Caption: PERUT BABY ASYIK / MASUK ANGIN?", src=2.5),
        Beat(0.6, 2.4, "1 Hook", "Berfikir", "Kesian baby...",
             "Close-up depan tiub (teddy), caption hook kekal.", src=4.0),
        Beat(2.4, 4.4, "2 Produk", "Teruja", "Cuba krim herba ni!",
             "Push-in ke label depan + kilauan. Caption: TROPIKA I'M TEDDY / BABY HERBAL CREAM", src=6.5),
        Beat(4.4, 7.4, "3 Ramuan", "Bercakap", "Ada halia & mentol!",
             "Label belakang, senarai ramuan. Caption: KELAPA DARA + HALIA / EUCALYPTUS & MENTOL", src=17.5),
        Beat(7.4, 9.4, "4 Ikon", "Kenyit mata", "Halal & vegan~",
             "Ikon Halal / Vegan / Not tested. Caption: TAK DIUJI PADA HAIWAN / HALAL & VEGAN", src=21.0),
        Beat(9.4, 11.4, "5 Picit", "Senyum", None,
             "Buka penutup, picit atas tangan. Caption: KRIM PUTIH / LEMBUT", src=34.5),
        Beat(11.4, 12.6, "6 Sapu", "Bercakap", "Tengok ni!",
             "Titik krim atas kulit (1x). Caption: SAPU SIKIT / ATAS KULIT", src=54.6),
        Beat(12.6, 14.6, "6 Sapu", "Senyum", None,
             "Gosok, fast-forward ~2.8x + lencana >> x3. Caption: GOSOK / PERLAHAN-LAHAN", src=58.0),
        Beat(14.6, 17.0, "7 Hilang", "Thumbs up", "Terus meresap!",
             "Penumbuk sama, bersih (61.35s) lalu buka tangan. Inset SEBELUM (titik krim) vs SELEPAS. Caption: TERUS MERESAP / TAK BERBEKAS!", src=61.5),
        Beat(17.0, 19.2, "8 CTA", "Shopping", "Jom checkout!",
             "CTA beg kuning (tanpa anak panah), tiub + tangan di belakang.", src=74.0),
        Beat(19.2, 20.0, "8 CTA", "Kenyit mata", None,
             "Penutup: Oyen kenyit mata.", src=76.0),
    ],
    blinks=[10.4, 13.6],
    jumps=[2.4, 14.6],
)
