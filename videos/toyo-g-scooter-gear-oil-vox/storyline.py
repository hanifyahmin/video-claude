"""Oyen storyline for TOYO-G Scooter Gear Oil 80W-90, Vox-style edit (25.5s, text + music only).

Vox explainers carry no mascot, so Oyen stays hidden (index.html: #cat visibility) until the
CTA, walks in as a paper sticker, says one line and dashes off, knocking the bubble away.

Facts come from the bottle label and the seller description only (see storyboard/PLAN.md);
"synthetic" is not used (the label says CONVENTIONAL).

  python3 -m oyen check videos/toyo-g-scooter-gear-oil-vox
  python3 -m oyen install videos/toyo-g-scooter-gear-oil-vox
"""
from oyen.storyline import Beat, Layout, Storyline

STORYLINE = Storyline(
    title="TOYO-G Scooter Gear Oil, Vox (25.5s)",
    beats=[
        Beat(0.0, 21.5, "1-6 Explainer", "Tidur", None, "Oyen tersembunyi: skrin untuk kolaj dan diagram."),
        Beat(21.5, 22.2, "7 CTA", "Jalan", None, "Oyen berjalan masuk dari kiri."),
        Beat(22.2, 24.3, "7 CTA", "Duduk", "Jom checkout!", "Duduk bawah butang CTA (dialog 1/1)."),
        Beat(24.3, 25.5, "7 CTA", "Lari keluar", None, "Meluru keluar, langgar bubble."),
    ],
    blinks=[23.4],
    layout=Layout(style="bold"),
    character="tabby",
)
