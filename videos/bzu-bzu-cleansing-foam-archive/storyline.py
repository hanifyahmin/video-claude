"""Oyen storyline for BZU BZU Cleansing Foam, archive edit (~22.4s, text + music only).

The archive look (after the user's sample edit) keeps the screen for typed words and pixel
objects, so Oyen stays hidden (index.html: #cat visibility) until the CTA, walks in, says one
line beside the button and dashes off, knocking the bubble away.

Footage: assets/source-portrait.mp4 (same join as videos/bzu-bzu-cleansing-foam). Claims come
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
        Beat(0.0, 17.8, "1-6 Archive", "Tidur", None,
             "Oyen tersembunyi: skrin untuk teks taip, objek piksel dan footage.", src=16.0),
        Beat(17.8, 18.5, "7 CTA", "Jalan", None, "Oyen berjalan masuk dari kiri.", src=15.2),
        Beat(18.5, 21.2, "7 CTA", "Duduk", "Jom checkout!", "Duduk sebelah butang CTA (dialog 1/1).", src=15.6),
        Beat(21.2, 22.4, "7 CTA", "Lari keluar", None, "Meluru keluar, langgar bubble.", src=16.0),
    ],
    blinks=[20.4],
    layout=Layout(style="pixel"),
    character="tabby",
)
