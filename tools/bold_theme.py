#!/usr/bin/env python3
"""Restyle a composition to the bold theme: one look for every niche, only the accent colour changes.

  python3 tools/bold_theme.py videos/<name> --niche baby|rumah|gajet|makanan|travel

Full-bleed footage under a dark top fade, Montserrat (auto-resolved by HyperFrames, no
bundling), kicker in an accent pill, big caption in white uppercase with a thick black
outline and one word in the accent (<span class="hl">), accent CTA button. The accent lives
in CSS variables on #root (--accent, --on-accent), which Oyen's bold bubble reads too.

Swaps the bodies of the shared rules by selector (like tools/cute_theme.py), so shots,
timing and product rules are left alone; safe to rerun, also to switch niche. Afterwards set
`layout=Layout(style="bold")` in storyline.py, rerun `python3 -m oyen install`, wrap the key
word of each big caption in <span class="hl">, and recheck caption widths (uppercase
Montserrat Black is ~0.72em per character).
"""
import argparse
import re
import sys
from pathlib import Path

INK = "#111111"
# accent, text colour on the accent
NICHES = {  # pill text must stay >= 3:1 on the accent (hyperframes check measures it)
    "baby": ("#1C86F2", "#ffffff"),
    "rumah": ("#19C37D", INK),
    "gajet": ("#FFD60A", INK),
    "makanan": ("#E8361A", "#ffffff"),
    "travel": ("#FF7A00", INK),
}

RULES = {
    "html,\n      body": """margin: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000;""",
    "#root": """position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        font-family: Montserrat, sans-serif;
        color: #fff;
        background: #000;
        --accent: {accent};
        --on-accent: {on_accent};""",
    # full-bleed footage: the shots fill the whole 9:16 frame
    "#card": """position: absolute;
        left: 0;
        top: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000;""",
    # dark fade behind the captions so white text reads on any footage
    "#card-edge-top": """position: absolute;
        left: 0;
        top: 0;
        width: 1080px;
        height: 700px;
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.78), rgba(0, 0, 0, 0.5) 50%, rgba(0, 0, 0, 0));""",
    ".kick": """position: relative;
        z-index: 2;
        display: block;
        margin-bottom: 14px;
        padding: 8px 26px 10px;
        border-radius: 14px;
        background: var(--accent);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
        font-weight: 800;
        font-size: 46px;
        line-height: 1.1;
        color: var(--on-accent);
        white-space: nowrap;
        transform: rotate(-2deg);""",
    ".big": f"""position: relative;
        display: block;
        font-family: Montserrat, sans-serif;
        font-weight: 900;
        font-size: 100px;
        line-height: 1.04;
        letter-spacing: -0.01em;
        text-transform: uppercase;
        color: #fff;
        white-space: nowrap;
        -webkit-text-stroke: 10px {INK};
        paint-order: stroke fill;
        text-shadow: 0 8px 0 rgba(0, 0, 0, 0.35);""",
    ".big::before,\n      .big::after": "content: none;",
    ".big::before": "display: none;",
    ".big::after": "display: none;",
    ".big .hl": "color: var(--accent);",
    ".big.white": "color: #fff;",
    ".big.two": "font-size: 90px;",
    ".big.three": "font-size: 80px;",
    "#cta .kick": "font-size: 58px;",
    "#cta .big": "font-size: 128px;",
    "#cta .big.white": "color: #fff;",
    "#cta-btn": f"""margin-top: 46px;
        display: flex;
        align-items: center;
        gap: 20px;
        height: 128px;
        padding: 0 50px 0 38px;
        border: 6px solid {INK};
        border-radius: 64px;
        background: var(--accent);
        font-weight: 900;
        font-size: 50px;
        color: var(--on-accent);
        box-shadow: 8px 8px 0 {INK};""",
}
# rules the theme adds when a composition lacks them, inserted after the rule named on the right
ADD_AFTER = {".big::before,\n      .big::after": ".big", ".big::before": ".big::before,\n      .big::after",
             ".big::after": ".big::before", ".big .hl": ".big::after", ".big.white": ".big .hl"}

TEXT = {
    ">Nak satu?<": ">NAK SATU?<", ">Check harga promo": ">CHECK HARGA PROMO", "Check harga promo\n": "CHECK HARGA PROMO\n",
    # cart icon follows the button text colour
    'stroke="#2a1f1a"': 'stroke="currentColor"', 'fill="#2a1f1a"': 'fill="currentColor"',
    'stroke="#0b0d10"': 'stroke="currentColor"', 'fill="#0b0d10"': 'fill="currentColor"',
    # CTA backdrop: dark blur so the white/accent CTA pops (the cute theme used a light one)
    'filter: "brightness(1.12) saturate(0.9) blur(10px)"': 'filter: "brightness(0.42) blur(7px)"',
}
# the cute theme's bundled Fredoka is not used here
FREDOKA_FACE = re.compile(r'      @font-face \{\n        font-family: "Fredoka";.*?\n      \}\n', re.S)


def rule(css, selector):
    """Match of `selector { ... }` (body without nested braces), or None."""
    # (?<!,\n): the selector must start the rule, not be the last line of a "a,\n b {" group
    return re.search(r"(?m)(?<!,\n)^      " + re.escape(selector) + r" \{\n(.*?)\n      \}\n", css, re.S)


def restyle(page, niche):
    accent, on_accent = NICHES[niche]
    page = FREDOKA_FACE.sub("", page)
    for selector, body in RULES.items():
        body = body.replace("{accent}", accent).replace("{on_accent}", on_accent)
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="video dirs or index.html files")
    ap.add_argument("--niche", choices=sorted(NICHES), required=True)
    args = ap.parse_args(argv)
    for arg in args.paths:
        f = Path(arg)
        f = f / "index.html" if f.is_dir() else f
        f.write_text(restyle(f.read_text(), args.niche))
        print("restyled", f, "niche", args.niche)
    return 0


if __name__ == "__main__":
    sys.exit(main())
