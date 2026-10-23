"""Oyen storyline for BZU BZU Cleansing Foam, archive edit (~22.4s, text + music only).

The archive look (after the user's sample edit) keeps the screen for typed words and pixel
objects, so Oyen stays hidden (index.html: #cat visibility) until the CTA, walks in, says one
line beside the button and dashes off, knocking the bubble away.

Footage: only as glowing silhouettes, assets/source-pump.webm and source-brush.webm
(hands cut out of source-portrait.mp4 31.3-34.1s and 39.6-42.2s with `hyperframes remove-background`). Claims come
from the label only: for milk bottles, dish, toys, fruits & vegetables; 0% fragrance; no
sulfate; 100% plant-based ingredients*; Halal; mild to hands; easy to rinse; fresh lemon scent.

  python3 -m oyen check videos/bzu-bzu-cleansing-foam-archive
  python3 -m oyen install videos/bzu-bzu-cleansing-foam-archive
"""
from oyen.storyline import Beat, Layout, Storyline

STORYLINE = Storyline(
    title="BZU BZU Cleansing Foam, archive (22.4s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 18.4, "1-8 Archive", "Tidur", None,
             "Oyen tersembunyi: skrin untuk teks, objek piksel dan siluet.", src=16.0),
        Beat(18.4, 19.1, "9 CTA", "Jalan", None, "Oyen berjalan masuk dari kiri.", src=15.2),
        Beat(19.1, 21.2, "9 CTA", "Duduk", "Jom checkout!", "Duduk bawah butang CTA (dialog 1/1).", src=15.6),
        Beat(21.2, 22.4, "9 CTA", "Lari keluar", None, "Meluru keluar, langgar bubble.", src=16.0),
    ],
    blinks=[20.4],
    layout=Layout(style="pixel"),
    character="tabby",
)
