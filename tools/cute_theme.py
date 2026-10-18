#!/usr/bin/env python3
"""Restyle a composition to the cute sticker theme used by the covers (promo/cute.py).

  python3 tools/cute_theme.py videos/<name> [more dirs or index.html files...]

Adds the bundled Fredoka font (shared/fonts), swaps the bodies of the shared rules (page backdrop, card edge, captions,
CTA) by selector, adds the burst doodles beside each big caption, lightens the
CTA's blurred footage and puts the CTA words in sentence case. Product-specific
rules, shots and timing are left alone. Safe to rerun. Afterwards re-run
`python3 -m oyen install` (the bubble style lives in the storyline Layout) and
put caption text in sentence case by hand.
"""
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FONT = REPO / "shared" / "fonts" / "fredoka-latin.woff2"
FONT_FACE = """      @font-face {
        font-family: "Fredoka";
        src: url("assets/fonts/fredoka-latin.woff2") format("woff2");
        font-weight: 300 700;
      }
"""

INK = "#2a1f1a"
# yellow "sunburst" dashes, as on the cover headline (data URI: # must be %23)
BURST_L = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 70 90'%3E%3Cpath "
           "d='M60 14L34 28M58 45H18M60 76L34 62' stroke='%23ffc928' stroke-width='10' stroke-linecap='round' "
           "fill='none'/%3E%3C/svg%3E\")")
BURST_R = BURST_L.replace("M60 14L34 28M58 45H18M60 76L34 62", "M10 14L36 28M12 45H52M10 76L36 62")

RULES = {
    "html,\n      body": f"""margin: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #fff6ee;""",
    "#root": f"""position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        font-family: Fredoka, sans-serif;
        color: {INK};
        background:
          radial-gradient(circle at 10% 4%, rgba(255, 168, 204, 0.6), rgba(255, 168, 204, 0) 30%),
          radial-gradient(circle at 92% 6%, rgba(255, 214, 102, 0.65), rgba(255, 214, 102, 0) 30%),
          linear-gradient(180deg, #fff6ee, #ffeef3);""",
    "#card": """position: absolute;
        left: 0;
        top: 220px;
        width: 1080px;
        height: 1700px;
        overflow: hidden;
        border-radius: 56px 56px 0 0;
        background: #fff1e8;""",
    "#card-edge-top": """position: absolute;
        left: 0;
        top: 220px;
        width: 1080px;
        height: 200px;
        border-radius: 56px 56px 0 0;
        background: linear-gradient(180deg, rgba(255, 246, 238, 0.8), rgba(255, 246, 238, 0));""",
    ".kick": f"""position: relative;
        z-index: 2;
        display: block;
        margin-bottom: -12px;
        padding: 4px 30px 10px;
        border-radius: 40px 64px 46px 72px / 58px 40px 66px 46px;
        background: #fff;
        box-shadow: 0 8px 0 rgba(42, 31, 26, 0.1), 0 14px 30px rgba(42, 31, 26, 0.18);
        font-weight: 700;
        font-size: 46px;
        line-height: 1.1;
        color: {INK};
        white-space: nowrap;
        transform: rotate(-3deg);""",
    ".big": f"""position: relative;
        display: block;
        padding: 4px 42px 14px;
        border-radius: 46px 70px 52px 80px / 64px 46px 74px 50px;
        background: #ffe46b;
        box-shadow: 0 10px 0 rgba(42, 31, 26, 0.1), 0 18px 36px rgba(42, 31, 26, 0.2);
        font-family: Fredoka, sans-serif;
        font-weight: 700;
        font-size: 116px;
        line-height: 1.02;
        color: {INK};
        white-space: nowrap;
        transform: rotate(-1.5deg);""",
    ".big::before,\n      .big::after": """content: "";
        position: absolute;
        top: 50%;
        width: 70px;
        height: 90px;
        margin-top: -45px;""",
    ".big::before": f"""left: -84px;
        background: {BURST_L};""",
    ".big::after": f"""right: -84px;
        background: {BURST_R};""",
    ".big.white": "background: #fff;",
    ".big.two": "font-size: 100px;",
    ".big.three": "font-size: 90px;",
    "#cta .kick": "font-size: 60px;",
    "#cta .big": "margin-top: 8px;\n        font-size: 120px;",
    "#cta .big.white": "background: #fff;\n        transform: rotate(2deg);",
    "#cta-btn": f"""margin-top: 54px;
        display: flex;
        align-items: center;
        gap: 20px;
        height: 128px;
        padding: 0 50px 0 38px;
        border: 8px solid #fff;
        border-radius: 64px;
        background: #ffb6cf;
        font-weight: 700;
        font-size: 52px;
        color: {INK};
        box-shadow: 0 16px 36px rgba(232, 72, 127, 0.3);""",
}
# rules the theme adds when a composition lacks them, inserted after the rule named on the right
ADD_AFTER = {".big::before,\n      .big::after": ".big", ".big::before": ".big::before,\n      .big::after",
             ".big::after": ".big::before", ".big.white": ".big::after"}

TEXT = {">NAK SATU?<": ">Nak satu?<", ">TEKAN<": ">Tekan<", ">BEG KUNING<": ">beg kuning<",
        "CHECK HARGA PROMO": "Check harga promo", 'stroke="#0b0d10"': f'stroke="{INK}"', 'fill="#0b0d10"': f'fill="{INK}"',
        # CTA backdrop: light, soft blur instead of a dark one, so the stickers sit on pastel
        'filter: "brightness(0.42) blur(7px)"': 'filter: "brightness(1.12) saturate(0.9) blur(10px)"'}


def rule(css, selector):
    """(start, end) of `selector { ... }` (body without nested braces), or None."""
    # (?<!,\n): the selector must start the rule, not be the last line of a "a,\n b {" group
    m = re.search(r"(?m)(?<!,\n)^      " + re.escape(selector) + r" \{\n(.*?)\n      \}\n", css, re.S)
    return m


def restyle(page):
    if "fredoka-latin.woff2" not in page:
        page = page.replace("<style>\n", "<style>\n" + FONT_FACE, 1)
    for selector, body in RULES.items():
        new = f"      {selector} {{\n        {body}\n      }}\n"
        m = rule(page, selector)
        if m:
            page = page[:m.start()] + new + page[m.end():]
        elif selector in ADD_AFTER:
            anchor = rule(page, ADD_AFTER[selector])
            if anchor:
                page = page[:anchor.end()] + new + page[anchor.end():]
    for old, new in TEXT.items():
        page = page.replace(old, new)
    return page


def main(paths):
    if not paths:
        print(__doc__)
        return 2
    for arg in paths:
        f = Path(arg)
        f = f / "index.html" if f.is_dir() else f
        f.write_text(restyle(f.read_text()))
        fonts = f.parent / "assets" / "fonts"
        if (f.parent / "assets").exists():  # the template gets its assets from new_video.py
            fonts.mkdir(exist_ok=True)
            shutil.copy2(FONT, fonts)
        print("restyled", f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
