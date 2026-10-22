"""Bold cover, matching the bold video theme (tools/bold_theme.py): the hook is the hero.

Full-bleed product frame, dark fades top and bottom, kicker in an accent pill, a huge
white uppercase headline with a thick black outline and the *starred* word in the
accent, an accent badge on the product, up to 2 white fact tags, and Oyen with the
bold speech box. Everything that matters sits in the 3:4 grid crop (y 240-1680).
"""
import html
import re

from oyen import character as C
from oyen.render import svg_rects

from .model import niche_colours

INK = "#111111"
SCALE = 14  # Oyen shares the bottom with the bubble; the headline is the hero here


def _headline(lines):
    out = []
    for line in lines:
        plain = line.replace("*", "")
        parts = re.split(r"(\*[^*]+\*)", html.escape(line))
        spans = "".join(f'<span class="hl">{p[1:-1]}</span>' if p.startswith("*") else p for p in parts if p)
        # Montserrat Black caps are ~0.72em wide; the outline needs a little room too
        size = min(178, int(980 / (0.74 * max(len(plain), 1))))
        out.append(f'<div class="line" style="font-size: {size}px">{spans}</div>')
    return "".join(out)


def build_html(p):
    accent, on_accent = niche_colours(p.niche)
    oyen = svg_rects(C.POSES[p.pose])
    ow, oh = C.CW * SCALE, C.CH * SCALE
    bx, by = p.badge_xy or (740, 1030)
    badge_size = min(54, int(200 / (0.72 * max((len(w) for w in (p.badge or "x").split()), default=1))))
    badge = (f'<div id="badge" style="left: {bx}px; top: {by}px"><span>{html.escape(p.badge)}</span></div>'
             if p.badge else "")
    tags = "".join(
        f'<div class="tag" style="top: {1060 + i * 104}px">{"<br />".join(html.escape(x) for x in t.split(chr(10)))}</div>'
        for i, t in enumerate(p.tags))
    bubble = f'<div id="bubble">{html.escape(p.bubble)}</div>' if p.bubble else ""
    kicker = f'<div id="kick">{html.escape(p.kicker)}</div>' if p.kicker else ""
    # frame moved down: fade its top edge into the blurred fill instead of a hard line
    fade = (f"-webkit-mask-image: linear-gradient(180deg, transparent 0, #000 {min(-p.frame_shift + 120, 360)}px);"
            if p.frame_shift < 0 else "")
    return f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: Montserrat, sans-serif; color: #fff; }}
      /* the same frame, blurred, fills any gap a negative frame_shift opens at the top */
      #fill {{ position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; object-fit: cover;
        filter: blur(34px) brightness(0.7) saturate(1.2); }}
      #bg {{ position: absolute; left: 0; top: {-p.frame_shift}px; width: 1080px; height: {1920 + abs(p.frame_shift)}px;
        object-fit: cover; filter: brightness(1.05) saturate(1.15) contrast(1.04); {fade} }}
      #fade-top {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1000px;
        background: linear-gradient(180deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.62) 45%, rgba(0,0,0,0) 100%); }}
      #fade-bot {{ position: absolute; left: 0; top: 1300px; width: 1080px; height: 620px;
        background: linear-gradient(0deg, rgba(0,0,0,0.8), rgba(0,0,0,0)); }}
      #head {{ position: absolute; left: 30px; top: 250px; width: 1020px;
        display: flex; flex-direction: column; align-items: center; text-align: center; }}
      #kick {{ display: inline-block; margin-bottom: 18px; padding: 10px 32px 14px; border-radius: 16px;
        background: {accent}; color: {on_accent}; font-weight: 800; font-size: 58px; line-height: 1.1;
        transform: rotate(-2deg); box-shadow: 0 10px 24px rgba(0,0,0,0.4); white-space: nowrap; }}
      .line {{ font-weight: 900; line-height: 1.0; letter-spacing: -0.015em; text-transform: uppercase; white-space: nowrap;
        -webkit-text-stroke: 16px {INK}; paint-order: stroke fill; text-shadow: 0 10px 0 rgba(0,0,0,0.4); }}
      .hl {{ color: {accent}; }}
      #badge {{ position: absolute; width: 270px; height: 270px; border-radius: 50%; background: {accent};
        border: 9px solid {INK}; box-shadow: 10px 10px 0 {INK}; transform: rotate(10deg);
        display: flex; align-items: center; justify-content: center; text-align: center; }}
      #badge span {{ width: 210px; font-weight: 900; font-size: {badge_size}px; line-height: 1.0; color: {on_accent};
        text-transform: uppercase; }}
      .tag {{ position: absolute; left: 44px; padding: 10px 26px 12px; border-radius: 14px; background: #fff;
        border: 6px solid {INK}; box-shadow: 8px 8px 0 {accent}; font-weight: 900; font-size: 46px; line-height: 1.05;
        color: {INK}; text-transform: uppercase; transform: rotate(-3deg); }}
      #oyen {{ position: absolute; left: 24px; top: {1660 - oh}px; width: {ow}px; height: {oh}px; }}
      #oyen svg {{ display: block; filter: drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff)
        drop-shadow(0 -5px 0 #fff) drop-shadow(0 12px 16px rgba(0,0,0,0.45)); }}
      #bubble {{ position: absolute; left: {24 + ow + 14}px; top: {1660 - oh + 40}px; max-width: {1040 - 24 - ow - 14}px;
        padding: 16px 30px 20px; background: #fff; border: 6px solid {INK}; border-radius: 30px 30px 30px 8px;
        box-shadow: 8px 8px 0 {accent}; font-weight: 800; font-size: 46px; line-height: 1.12; color: {INK}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-width="1080" data-height="1920">
      <img id="fill" src="frame.png" alt="" />
      <img id="bg" src="frame.png" alt="" />
      <div id="fade-top"></div>
      <div id="fade-bot"></div>
      {tags}
      {badge}
      <div id="head">{kicker}{_headline(p.headline)}</div>
      <div id="oyen"><svg width="{ow}" height="{oh}" viewBox="0 0 {C.CW} {C.CH}" shape-rendering="crispEdges">{oyen}</svg></div>
      {bubble}
    </div>
    <script>
      window.__timelines["cover"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
