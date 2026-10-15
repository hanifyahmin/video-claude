"""python3 -m promo videos/<name> [--caption-only]

Writes videos/<name>/promo/thumbnail.png and caption.txt from videos/<name>/promo.py.
"""
import sys
from pathlib import Path

from . import thumbnail
from .model import CAPTION_VISIBLE, load


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    video = Path(args[0])
    promo = load(video)
    problems = promo.problems()
    for p in problems:
        print("error:", p)
    if problems:
        return 1
    out = video / "promo"
    out.mkdir(exist_ok=True)
    (out / "caption.txt").write_text(promo.caption_text())
    first = promo.caption.strip().splitlines()[0]
    if len(first) > CAPTION_VISIBLE:
        print(f"note: first caption line is {len(first)} chars; about {CAPTION_VISIBLE} show before 'more'")
    print(out / "caption.txt")
    if "--caption-only" not in argv:
        print(thumbnail.render(promo, video, out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
