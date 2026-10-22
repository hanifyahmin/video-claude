"""Cover thumbnail + TikTok caption for {{NAME}}. Make with the final render.

  python3 -m promo videos/{{NAME}}   -> promo/thumbnail.png + promo/caption.txt

The cover's job is the click, so the hook is the hero:
- headline = the problem or the result, 2-3 short lines (<= 14 chars each), uppercase on screen,
  one *starred* word in the accent; prefer a question, a number or a before/after;
- kicker = who it is for / the situation; badge = one visible fact (size, count, "2 dalam 1");
- pick the frame where the product is biggest and clearest; Oyen reacts in <= 20 chars.
Only claim what the footage or label shows, or what the user confirmed.
"""
from promo import Promo

PROMO = Promo(
    style="bold",                     # matches the video theme; niche sets the accent colour
    niche="umum",                     # baby | rumah | gajet | makanan | travel | umum
    frame_src=0.0,                    # source second with the biggest, clearest product shot
    frame_shift=0,                    # move the frame up (+) / down (-) so the product clears the headline
    kicker="{{KICKER}}",
    headline=["{{HOOK}}"],            # 2-3 lines, <= 14 chars each; *word* = accent colour
    badge=None,                       # one visible fact, e.g. "MAX 50KG"
    tags=(),                          # up to 2 more facts as white tags, e.g. ("1 liter",)
    pose="Terkejut",
    bubble="Walaweh!",
    caption=(
        "Hook soalan/masalah + 1 fakta produk + ajakan tekan beg kuning."
    ),
    hashtags=["#tiktokshopmalaysia", "#fyp", "#oyen"],
)
