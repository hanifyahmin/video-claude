"""Oyen storyline for {{NAME}}.

Beats must cover the timeline without gaps, starting at 0. Poses are the
names in oyen/character.py POSE_SPECS (see oyen/gallery/poses/oyen-postur.png).
Keep each line <= 20 characters.

  python3 -m oyen check videos/{{NAME}}
  python3 -m oyen storyboard videos/{{NAME}}
  python3 -m oyen install videos/{{NAME}}
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="{{NAME}}",
    source="assets/source-portrait.mp4",  # footage for storyboard thumbnails (optional)
    beats=[
        Beat(0.0, 1.5, "1 Hook", "Senyum", "Hai, aku Oyen!", "Oyen sudah ada di frame 0."),
        Beat(1.5, 3.0, "1 Hook", "Teruja", "Jom tengok!", "Teruja masa produk muncul."),
        Beat(3.0, 5.0, "2 CTA", "Shopping", "Jom checkout!", "Pegang beg kuning sebelah CTA."),
        Beat(5.0, 6.0, "2 CTA", "Thumbs up", None, "Penutup."),
    ],
    blinks=[0.9],
    jumps=[3.0],
)
