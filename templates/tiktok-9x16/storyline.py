"""Oyen storyline for {{NAME}}.

Oyen v2 (character="tabby"): every pose is a pixel-art animation from oyen/tabby
(see oyen/gallery/tabby/oyen-tabby-animasi.png):
  Duduk, Bercakap, Menjilat, Makan, Tidur, Terkejut, Teruja, Gembira, Regang, Lompat, Jalan, Lari, Lari keluar.
Jalan/Lari walk Oyen in from the left; Lari keluar dashes off to the right and knocks away
the previous beat's bubble; Terkejut, Regang and Lompat play once and hold.

Oyen reacts, the captions carry the facts:
- at most 3 speech lines (hook reaction, one punchline mid-video, CTA), each <= 20
  characters and never a repeat of the caption on screen; slang/humour welcome.
  Only Duduk (mouth flaps) and Bercakap talk on screen, so give lines to those beats;
- a different animation on every beat: Terkejut/Tidur for the problem, Teruja/Gembira/
  Lompat for the payoff, Makan/Menjilat/Regang for a breather.

Beats must cover the timeline without gaps, starting at 0.

  python3 -m oyen check videos/{{NAME}}
  python3 -m oyen storyboard videos/{{NAME}}
  python3 -m oyen install videos/{{NAME}}
"""
from oyen.storyline import Beat, Layout, Storyline

STORYLINE = Storyline(
    title="{{NAME}}",
    source="assets/source-portrait.mp4",  # footage for storyboard thumbnails (optional)
    beats=[
        Beat(0.0, 1.0, "1 Hook", "Jalan", None, "Oyen berjalan masuk dari kiri (frame 0 di luar skrin)."),
        Beat(1.0, 2.0, "1 Hook", "Terkejut", None, "Produk muncul: Oyen terkejut."),
        Beat(2.0, 3.0, "2 Produk", "Duduk", "Walaweh!", "Reaksi (dialog 1/3)."),
        Beat(3.0, 4.0, "3 Bukti", "Gembira", None, "Fakta dibawa caption; Oyen cuma beraksi."),
        Beat(4.0, 4.9, "4 CTA", "Duduk", "Jom checkout!", "Sebelah CTA (dialog 2/3)."),
        Beat(4.9, 6.0, "4 CTA", "Lari keluar", None, "Oyen meluru keluar, langgar bubble 'Jom checkout!'."),
    ],
    blinks=[],
    jumps=[],
    layout=Layout(style="bold"),  # bubble matches the bold page theme (tools/bold_theme.py)
    character="tabby",
)
