"""Cute sticker cover: pastel blurred backdrop, sticker headline, cut-out product
with a white outline, pink fact tags, a cloud bubble for Oyen and a feature row.

Needs product.png (the frame with its background removed, cropped to the
product; see cutout.py) and frame.png next to the page; thumbnail.render() makes both.
Key content stays in the 3:4 grid crop (y 240-1680).
"""
import html
import re

from oyen import character as C
from oyen.render import svg_rects

from .icons import ICONS

INK = "#2a1f1a"
SCALE = 12  # Oyen shares the frame with the product here, so smaller than the classic cover
# feature-row colour pairs: (circle fill, stroke/underline)
TINTS = [("#ffd6e4", "#e8487f"), ("#d5f1dc", "#2e9b5b"), ("#fff0b3", "#e0a100")]

BURST = ('<svg class="burst {side}" width="120" height="150" viewBox="0 0 120 150">'
         '<path d="M{x1} 30 L{x2} 50 M{x1b} 75 L{x2b} 75 M{x1} 120 L{x2} 100" stroke="#ffc928" stroke-width="13" '
         'stroke-linecap="round" fill="none"/></svg>')
HEART = ('<svg class="heart" width="{w}" height="{w}" viewBox="0 0 24 24" style="{pos}">'
         '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z" fill="#ff8fb3" '
         'stroke="{ink}" stroke-width="1.6" stroke-linejoin="round"/></svg>')
SPARK = ('<svg width="{w}" height="{w}" viewBox="0 0 24 24" style="position: absolute; {pos}">'
         '<path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4z" fill="#ffd23f" '
         'stroke="{ink}" stroke-width="1.4" stroke-linejoin="round"/></svg>')


def _line(text, cls):
    """One sticker line; *word* in the text turns the line yellow."""
    plain = text.replace("*", "")
    parts = re.split(r"(\*[^*]+\*)", html.escape(text))
    spans = "".join(f'<span class="hl">{p[1:-1]}</span>' if p.startswith("*") else p for p in parts if p)
    yellow = " yellow" if "*" in text else ""
    big = cls == "head"
    # Fredoka bold is ~0.6em per glyph
    size = min(150 if big else 92, int((900 if big else 820) / (0.6 * max(len(plain), 1))))
    return f'<div class="stk {cls}{yellow}" style="font-size: {size}px">{spans}</div>'


def build_html(p):
    oyen = svg_rects(C.POSES[p.pose])
    ow, oh = C.CW * SCALE, C.CH * SCALE
    lines = ([_line(p.kicker, "kick")] if p.kicker else []) + [_line(h, "head") for h in p.headline]
    bursts = (BURST.format(side="l", x1=95, x2=55, x1b=90, x2b=30) +
              BURST.format(side="r", x1=25, x2=65, x1b=30, x2b=90))
    tag_spots = [("left: 60px; top: 700px; transform: rotate(-7deg);"),
                 ("right: 60px; top: 720px; transform: rotate(6deg);")]
    tags = "".join(
        f'<div class="tag{" two" if "\n" in t else ""}" style="{tag_spots[i]}">'
        + "<br />".join(html.escape(x) for x in t.split("\n")) + "</div>"
        for i, t in enumerate(p.tags))
    bx, by = p.badge_xy or (790, 1170)
    badge = (f'<div id="badge" style="left: {bx}px; top: {by}px"><span>{html.escape(p.badge)}</span></div>'
             if p.badge else "")
    badge_size = min(46, int(190 / (0.62 * max((len(w) for w in (p.badge or "x").split()), default=1))))
    bubble = (f'<div id="bubble">{html.escape(p.bubble)}</div>' if p.bubble else "")
    photo = "" if p.cutout else ' class="photo"'
    feats = []
    for i, (icon, label) in enumerate(p.features):
        fill, stroke = TINTS[i % len(TINTS)]
        parts = label.split("\n")
        text = "<br />".join(html.escape(t) for t in parts)
        # Fredoka semibold is ~0.56em per glyph; the label column is ~200px wide
        size = min(38, int(200 / (0.56 * max(len(t) for t in parts))))
        feats.append(
            f'<div class="feat"><div class="ico" style="background: {fill}">'
            f'<svg width="58" height="58" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.1" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg></div>'
            f'<div class="lab" style="font-size: {size}px">{text}<i style="background: {stroke}"></i></div></div>')
    row = f'<div id="feats">{"".join(feats)}</div>' if feats else ""
    doodles = (HEART.format(w=86, ink=INK, pos="position: absolute; right: 70px; top: 520px; transform: rotate(14deg)") +
               HEART.format(w=56, ink=INK, pos="position: absolute; left: 330px; top: 1090px; transform: rotate(-12deg)") +
               SPARK.format(w=70, ink=INK, pos="right: 300px; top: 1250px") +
               SPARK.format(w=46, ink=INK, pos="right: 250px; top: 1350px") +
               SPARK.format(w=54, ink=INK, pos="left: 90px; top: 640px"))
    return f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #fff8f1; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: Fredoka, sans-serif; color: {INK}; }}
      #bg {{ position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; object-fit: cover;
        filter: blur(30px) saturate(1.15) brightness(1.12); }}
      #wash {{ position: absolute; inset: 0;
        background: radial-gradient(ellipse 75% 32% at 50% 22%, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0) 70%),
          radial-gradient(circle at 10% 68%, rgba(255, 168, 204, 0.45), rgba(255, 168, 204, 0) 32%),
          radial-gradient(circle at 94% 42%, rgba(255, 214, 102, 0.42), rgba(255, 214, 102, 0) 30%),
          radial-gradient(circle at 85% 88%, rgba(170, 222, 196, 0.4), rgba(170, 222, 196, 0) 30%),
          linear-gradient(180deg, rgba(255, 251, 245, 0.8), rgba(255, 245, 236, 0.72)); }}
      #head {{ position: absolute; left: 40px; top: 250px; width: 1000px; height: 420px;
        display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; }}
      .stk {{ position: relative; font-weight: 700; line-height: 1.04; padding: 6px 46px 16px; white-space: nowrap;
        background: #fff; border-radius: 46px 70px 52px 80px / 64px 46px 74px 50px;
        box-shadow: 0 10px 0 rgba(42, 31, 26, 0.08), 0 18px 40px rgba(42, 31, 26, 0.10); }}
      .stk.kick {{ transform: rotate(-3deg); z-index: 2; }}
      .stk.head {{ transform: rotate(-1.5deg); margin-top: -14px; }}
      .stk.yellow {{ background: #ffe46b; }}
      .burst {{ position: absolute; top: 120px; }}
      .burst.l {{ left: -10px; }}
      .burst.r {{ right: -10px; }}
      #product {{ position: absolute; left: 140px; top: 690px; width: 800px; height: 760px;
        display: flex; align-items: flex-end; justify-content: center; }}
      #product img {{ max-width: 760px; max-height: 760px; object-fit: contain;
        filter: drop-shadow(0 22px 26px rgba(42, 31, 26, 0.22)); }}  /* white outline is baked into product.png (cutout.py) */
      #product img.photo {{ max-width: 720px; max-height: 640px; border: 14px solid #fff; border-radius: 48px;
        transform: rotate(-3deg); margin-bottom: 40px; box-shadow: 0 22px 40px rgba(42, 31, 26, 0.22); filter: none; }}
      .tag {{ position: absolute; padding: 10px 40px 16px; border-radius: 60px; background: #ffb6cf;
        border: 7px solid #fff; font-weight: 700; font-size: 66px; color: {INK};
        box-shadow: 0 10px 22px rgba(232, 72, 127, 0.25); }}
      .tag.two {{ font-size: 54px; line-height: 1.0; text-align: center; padding: 14px 36px 20px; border-radius: 52px; }}
      #badge {{ position: absolute; width: 240px; height: 240px; border-radius: 50%; background: #ffe46b;
        border: 9px solid #fff; transform: rotate(9deg); display: flex; align-items: center; justify-content: center;
        text-align: center; box-shadow: 0 14px 30px rgba(42, 31, 26, 0.2); }}
      #badge span {{ font-weight: 700; font-size: {badge_size}px; line-height: 1.02; width: 190px; }}
      #oyen {{ position: absolute; left: 24px; top: {1440 - oh}px; width: {ow}px; height: {oh}px; }}
      #oyen svg {{ display: block; filter: drop-shadow(0 0 0 #fff) drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff)
        drop-shadow(0 5px 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(0 14px 18px rgba(42, 31, 26, 0.25)); }}
      #bubble {{ position: absolute; left: 34px; top: {1440 - oh - 150}px; max-width: 360px; padding: 18px 34px 22px;
        background: #fff3b8; border: 7px solid #fff; border-radius: 70px 80px 70px 26px;
        font-weight: 700; font-size: 46px; line-height: 1.08; transform: rotate(-6deg);
        box-shadow: 0 12px 26px rgba(42, 31, 26, 0.18); }}
      #feats {{ position: absolute; left: 30px; top: 1470px; width: 1020px; height: 190px; padding: 0 18px;
        display: flex; align-items: center; justify-content: space-between;
        background: rgba(255, 255, 255, 0.82); border-radius: 48px; box-shadow: 0 14px 34px rgba(42, 31, 26, 0.12); }}
      .feat {{ display: flex; align-items: center; gap: 14px; width: 322px; }}
      .ico {{ flex: none; width: 104px; height: 104px; border-radius: 50%; border: 6px solid #fff;
        display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 14px rgba(42, 31, 26, 0.12); }}
      .lab {{ position: relative; font-weight: 600; line-height: 1.08; padding-bottom: 14px; white-space: nowrap; }}
      .lab i {{ position: absolute; left: 0; bottom: 0; width: 110px; height: 8px; border-radius: 4px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-width="1080" data-height="1920">
      <img id="bg" src="frame.png" alt="" />
      <div id="wash"></div>
      <div id="product"><img{photo} src="product.png" alt="" /></div>
      {tags}
      {badge}
      {doodles}
      <div id="head">
        {bursts}
        {"".join(lines)}
      </div>
      {bubble}
      <div id="oyen"><svg width="{ow}" height="{oh}" viewBox="0 0 {C.CW} {C.CH}" shape-rendering="crispEdges">{oyen}</svg></div>
      {row}
    </div>
    <script>
      window.__timelines["cover"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
