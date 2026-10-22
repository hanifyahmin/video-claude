"""Oyen storyline for {{NAME}}.

Beats must cover the timeline without gaps, starting at 0. Poses are the
names in oyen/character.py POSE_SPECS (see oyen/gallery/poses/oyen-postur.png).

Oyen reacts, the captions carry the facts:
- at most 3 speech lines (hook reaction, one punchline mid-video, CTA), each <= 20
  characters and never a repeat of the caption on screen; slang/humour welcome;
- a different pose on every beat (Terkejut, Sedih, Geram, Pening for the problem;
  Teruja, Gelak, Cool, Jatuh cinta, Malu, Thumbs up for the payoff), plus jumps/blinks.

  python3 -m oyen check videos/{{NAME}}
  python3 -m oyen storyboard videos/{{NAME}}
  python3 -m oyen install videos/{{NAME}}
"""
from oyen.storyline import Beat, Layout, Storyline

STORYLINE = Storyline(
    title="{{NAME}}",
    source="assets/source-portrait.mp4",  # footage for storyboard thumbnails (optional)
    beats=[
        Beat(0.0, 0.8, "1 Hook", "Geram", None, "Masalah: Oyen geram/sedih. Oyen sudah ada di frame 0."),
        Beat(0.8, 2.0, "1 Hook", "Terkejut", None, "Produk muncul."),
        Beat(2.0, 3.0, "2 Produk", "Teruja", "Walaweh!", "Reaksi (dialog 1/3)."),
        Beat(3.0, 4.0, "3 Bukti", "Cool", None, "Fakta dibawa caption; Oyen cuma beraksi."),
        Beat(4.0, 5.2, "4 CTA", "Shopping", "Jom checkout!", "Pegang beg kuning sebelah CTA (dialog 2/3)."),
        Beat(5.2, 6.0, "4 CTA", "Kenyit mata", None, "Penutup."),
    ],
    blinks=[],
    jumps=[0.8, 2.0, 4.0],
    layout=Layout(style="bold"),  # bubble matches the bold page theme (tools/bold_theme.py)
)
