"""Write Oyen into a video's index.html from its storyline.

`python3 -m oyen install videos/<name>`

The composition must contain four marker blocks (the template has them):

    /* OYEN:CSS:START */ ... /* OYEN:CSS:END */      inside <style>
    <!-- OYEN:START --> ... <!-- OYEN:END -->         inside the root, above overlays you want on top
    <!-- OYEN:SFX:START --> ... <!-- OYEN:SFX:END --> inside the root
    // OYEN:START ... // OYEN:END                     in the timeline script, before window.__timelines

Only text between markers is replaced, so a rerun after editing the
storyline is safe. Everything else in the composition is left alone.
"""
import re
import shutil
from pathlib import Path

from . import character as C
from . import tabby
from .palette import INK, PAPER
from .render import svg_rects
from .storyline import load

REPO = Path(__file__).resolve().parent.parent
SHARED_SFX = REPO / "shared" / "sfx"
NEEDED_SFX = ("pop.mp3", "typing.mp3")
TABBY_ASSET = "oyen-tabby.png"   # copied into the video's assets/ when the storyline uses the tabby

MARKERS = {
    "css": (r"      /\* OYEN:CSS:START.*?/\* OYEN:CSS:END \*/\n", "/* OYEN:CSS:START"),
    "html": (r"      <!-- OYEN:START.*?<!-- OYEN:END -->", "<!-- OYEN:START"),
    "sfx": (r"      <!-- OYEN:SFX:START -->.*?<!-- OYEN:SFX:END -->", "<!-- OYEN:SFX:START -->"),
    "js": (r"      // OYEN:START.*?// OYEN:END\n", "// OYEN:START"),
}


# ---------------- frames ----------------
def frame_id(pose, kind="rest"):
    return C.slug(pose) if kind == "rest" else f"{C.slug(pose)}--{kind}"


def used_frames(story):
    """Only the frames this storyline needs, in first-use order."""
    frames = {}
    for b in story.beats:
        vf = C.video_frames(b.pose)
        frames.setdefault(frame_id(b.pose), vf["rest"])
        if b.line and "talk" in vf:
            frames.setdefault(frame_id(b.pose, "talk"), vf["talk"])
    for t in story.blinks:
        b = story.beat_at(t)
        vf = C.video_frames(b.pose)
        if "blink" in vf:
            frames.setdefault(frame_id(b.pose, "blink"), vf["blink"])
    return frames


def bubbles(story):
    """(id, start, end, text, pose) for every beat with a line."""
    out = []
    for b in story.beats:
        if b.line:
            out.append((f"ob{len(out)}", round(b.start + 0.15, 2), round(b.end - 0.05, 2), b.line, b.pose))
    return out


# ---------------- blocks ----------------
def geometry(story):
    """Screen boxes for the cat and the bubble."""
    L = story.layout
    if story.character == "tabby":
        w, h = tabby.cell()
        s = tabby.SCALE
        head = tabby.GROUND - tabby.meta()["stand_px"] * s     # ear tips of a standing cat
        left = tabby.ANCHOR_X + 14
        return dict(cat_left=tabby.ANCHOR_X - w * s, cat_top=tabby.GROUND - h * s, cat_w=w * s, cat_h=h * s,
                    bubble_left=left, bubble_top=head + 10, bubble_max_width=1040 - left)
    return dict(cat_left=L.cat_left, cat_top=L.cat_top, cat_w=C.CW * L.scale, cat_h=C.CH * L.scale,
                bubble_left=L.bubble_left, bubble_top=L.bubble_top, bubble_max_width=L.bubble_max_width)


CUTE_INK = "#2a1f1a"   # same ink and cloud colours as the cute cover (promo/cute.py)
CUTE_CLOUD = "#fff3b8"


def css_block(story):
    L = story.layout
    g = geometry(story)
    if L.style == "bold":
        # matches tools/bold_theme.py: white speech box, black outline, offset shadow in the video's accent
        sprite = ("drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) "
                  "drop-shadow(0 -5px 0 #fff) drop-shadow(0 10px 14px rgba(0, 0, 0, 0.4))")
        bubble = """        padding: 14px 30px 18px;
        background: #fff;
        border: 6px solid #111;
        border-radius: 30px 30px 30px 8px;
        box-shadow: 8px 8px 0 var(--accent, #ffd60a);
        font-family: Montserrat, sans-serif;
        font-weight: 800;
        font-size: 44px;
        line-height: 1.15;
        color: #111;"""
    elif L.style == "cute":
        sprite = ("drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) "
                  "drop-shadow(0 -5px 0 #fff) drop-shadow(0 12px 16px rgba(42, 31, 26, 0.3))")
        bubble = f"""        padding: 16px 34px 22px;
        background: {CUTE_CLOUD};
        border: 6px solid #fff;
        border-radius: 56px 64px 56px 20px;
        box-shadow: 0 12px 26px rgba(42, 31, 26, 0.25);
        font-family: Fredoka, sans-serif;
        font-weight: 700;
        font-size: 48px;
        line-height: 1.1;
        color: {CUTE_INK};"""
    else:
        sprite = "drop-shadow(6px 6px 0 rgba(0, 0, 0, 0.45))"
        bubble = f"""        padding: 22px 28px;
        background: {PAPER};
        box-shadow:
          0 -6px 0 0 {INK},
          0 6px 0 0 {INK},
          -6px 0 0 0 {INK},
          6px 0 0 0 {INK},
          12px 12px 0 0 rgba(0, 0, 0, 0.35);
        font-family: "Space Mono", monospace;
        font-weight: 700;
        font-size: 40px;
        line-height: 1.2;
        color: {INK};"""
    return f"""      /* OYEN:CSS:START (generated by `python3 -m oyen install`) */
      #cat {{
        position: absolute;
        left: {g["cat_left"]}px;
        top: {g["cat_top"]}px;
        width: {g["cat_w"]}px;
        height: {g["cat_h"]}px;
      }}
      #cat-svg,
      #cat-spr {{
        display: block;
        filter: {sprite};
      }}{_tabby_css() if story.character == "tabby" else ""}
      .bub {{
        position: absolute;
        left: {g["bubble_left"]}px;
        top: {g["bubble_top"]}px;
        width: {g["bubble_max_width"]}px;
        height: 130px;
      }}
      .bub-in {{
        position: absolute;
        left: 0;
        top: 0;
        max-width: {g["bubble_max_width"]}px;
{bubble}
        white-space: nowrap;
      }}
      .bub-tail {{
        position: absolute;
        left: -30px;
        top: 34px;
        width: 30px;
        height: 30px;
      }}
      /* OYEN:CSS:END */
"""


def _tabby_css():
    """The sprite sheet as a pixelated background; frames switch by background-position."""
    from PIL import Image
    s = tabby.SCALE
    w, h = tabby.cell()
    sw, sh = Image.open(tabby.SHEET).size
    return f"""
      #cat-spr {{
        width: {w * s}px;
        height: {h * s}px;
        background-image: url("assets/{TABBY_ASSET}");
        background-size: {sw * s}px {sh * s}px;
        background-repeat: no-repeat;
        image-rendering: pixelated;
        transform-origin: 85% 100%;
      }}"""


_TAIL = ('<svg class="bub-tail" width="30" height="30" viewBox="0 0 5 5" shape-rendering="crispEdges">'
         f'<rect x="4" y="0" width="1" height="5" fill="{PAPER}"/><rect x="3" y="1" width="1" height="3" fill="{PAPER}"/>'
         f'<rect x="2" y="2" width="1" height="1" fill="{PAPER}"/><rect x="3" y="0" width="1" height="1" fill="{INK}"/>'
         f'<rect x="2" y="1" width="1" height="1" fill="{INK}"/><rect x="1" y="2" width="1" height="1" fill="{INK}"/>'
         f'<rect x="2" y="3" width="1" height="1" fill="{INK}"/><rect x="3" y="4" width="1" height="1" fill="{INK}"/></svg>')


def html_block(story):
    if not story.beats:
        return "      <!-- OYEN:START (no beats) -->\n      <!-- OYEN:END -->"
    if story.character == "tabby":
        return _tabby_html(story)
    first = frame_id(story.beats[0].pose)  # frame 0 is static HTML, not a t=0 tween
    groups = "".join(
        f'<g class="oy-f" id="oy-{fid}" style="opacity: {1 if fid == first else 0}">{svg_rects(rows)}</g>'
        for fid, rows in used_frames(story).items())
    s = story.layout.scale
    lines = ["      <!-- OYEN:START (generated by `python3 -m oyen install`; edit storyline.py, not this) -->",
             f'      <div id="cat"><svg id="cat-svg" width="{C.CW * s}" height="{C.CH * s}" '
             f'viewBox="0 0 {C.CW} {C.CH}" shape-rendering="crispEdges">{groups}</svg></div>']
    lines += _bubble_html(story)
    lines.append("      <!-- OYEN:END -->")
    return "\n".join(lines)


def _bubble_html(story):
    lines = []
    for bid, a, b, text, _pose in bubbles(story):
        chars = "".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in text)
        tail = _TAIL if story.layout.style == "pixel" else ""  # cute/bold: the bubble's sharp corner is its tail
        lines.append(f'      <div id="{bid}" class="bub clip" data-start="{a:g}" data-duration="{round(b - a, 2):g}" '
                     f'data-track-index="6"><div class="bub-in">{tail}{chars}</div></div>')
    return lines


def _walk_in(story, b):
    """(from_x, seconds) when a beat's animation walks the cat in from off-screen left, else None."""
    speed = tabby.anims()[b.pose].get("move")
    if not speed:
        return None
    dist = tabby.ANCHOR_X + 40
    return -dist, round(min(dist / speed, b.end - b.start), 3)


def _tabby_html(story):
    first = story.beats[0]
    x, y = tabby.frame_xy(first.pose, tabby.frames_for(first.pose, 0, first.end)[0][1])
    s = tabby.SCALE
    walk = _walk_in(story, first)
    # frame 0 is static HTML: when beat 0 walks in, #cat sits one walk-length left (static `left`, no CSS
    # transform) and #cat-walk's x carries it home; otherwise walk-ins slide #cat-walk from -dist to 0
    start = f' style="left: {geometry(story)["cat_left"] + walk[0]}px"' if walk else ""
    lines = ["      <!-- OYEN:START (generated by `python3 -m oyen install`; edit storyline.py, not this) -->",
             f'      <div id="cat"{start}><div id="cat-walk"><div id="cat-spr" '
             f'style="background-position: {-x * s}px {-y * s}px"></div></div></div>']
    lines += _bubble_html(story)
    lines.append("      <!-- OYEN:END -->")
    return "\n".join(lines)


def sfx_block(story):
    lines = ["      <!-- OYEN:SFX:START -->"]
    track = 50
    for bid, a, _b, text, _pose in bubbles(story):
        typing = min(round(len(text) * story.type_speed + 0.05, 2), 1.45)
        lines.append(f'      <audio id="sfx-pop-{bid}" src="assets/sfx/pop.mp3" data-start="{a:g}" '
                     f'data-track-index="{track}" data-volume="0.45"></audio>')
        lines.append(f'      <audio id="sfx-type-{bid}" src="assets/sfx/typing.mp3" data-start="{round(a + 0.12, 2):g}" '
                     f'data-duration="{typing:g}" data-track-index="{track + 1}" data-volume="0.22"></audio>')
        track += 2
    lines.append("      <!-- OYEN:SFX:END -->")
    return "\n".join(lines)


_JS_RUNTIME = """      // every sprite swap is a tl.set at a fixed time -> seek-safe
      const frame = (id, at) => tl.set(".oy-f", { opacity: 0 }, at).set("#oy-" + id, { opacity: 1 }, at);
      tl.set("#cat-svg", { transformOrigin: "50% 100%", scale: 1, y: 0 }, 0);
      // a pose change is a frame swap plus a stepped pixel "pop"
      const pose = (id, at) => {
        frame(id, at);
        tl.set("#cat-svg", { scale: 1.14 }, at).to("#cat-svg", { scale: 1, duration: 0.15, ease: "steps(3)" }, at);
      };
      const jump = (at) =>
        tl.to("#cat", { y: -70, duration: 0.12, ease: "steps(3)" }, at).to("#cat", { y: 0, duration: 0.16, ease: "steps(4)" }, at + 0.12);
      const blink = (id, back, at) => { frame(id, at); frame(back, at + 0.12); };
      // speech bubble: stepped pop, typed text, mouth flaps while typing
      const say = (id, at, end, rest, talk, cps) => {
        const chars = document.getElementById(id).querySelectorAll(".ch");
        const typed = chars.length * cps;
        tl.fromTo("#" + id + " .bub-in", { scale: 0, transformOrigin: "0% 50%" }, { scale: 1, duration: 0.16, ease: "steps(4)" }, at);
        tl.fromTo(chars, { opacity: 0 }, { opacity: 1, duration: 0.001, stagger: cps }, at + 0.12);
        if (talk) {
          for (let t = at + 0.12, i = 0; t < at + 0.12 + typed; t += 0.09, i++) frame(i % 2 ? rest : talk, t);
          frame(rest, at + 0.12 + typed + 0.02);
        }
        tl.to("#" + id + " .bub-in", { scale: 0, duration: 0.1, ease: "steps(3)" }, end - 0.1);
      };
"""


def js_block(story, duration):
    if not story.beats:
        return "      // OYEN:START (no beats)\n      // OYEN:END\n"
    if story.character == "tabby":
        return _tabby_js(story)
    calls = [f"      // idle bob in whole sprite pixels",
             f"      for (let t = 0.9; t < {duration - 0.2:g}; t += 0.6) "
             f'tl.set("#cat-svg", {{ y: -12 }}, t).set("#cat-svg", {{ y: 0 }}, t + 0.3);']
    for b in story.beats[1:]:  # beats[0] is the static HTML state
        calls.append(f'      pose("{frame_id(b.pose)}", {b.start:g});')
    for bid, a, b, _text, pose in bubbles(story):
        talk = f'"{frame_id(pose, "talk")}"' if "talk" in C.video_frames(pose) else "null"
        calls.append(f'      say("{bid}", {a:g}, {b:g}, "{frame_id(pose)}", {talk}, {story.type_speed:g});')
    for t in story.blinks:
        p = story.beat_at(t).pose
        if "blink" in C.video_frames(p):
            calls.append(f'      blink("{frame_id(p, "blink")}", "{frame_id(p)}", {t:g});')
    for t in story.jumps:
        calls.append(f"      jump({t:g});")
    return ("      // OYEN:START (generated by `python3 -m oyen install` from storyline.py)\n"
            + _JS_RUNTIME + "\n".join(calls) + "\n      // OYEN:END\n")


_TABBY_RUNTIME = """      // sprite frames switch by background-position at fixed times -> seek-safe
      const spr = (at, x, y) => tl.set("#cat-spr", { backgroundPosition: x + "px " + y + "px" }, at);
      // a new animation starts with a small stepped pixel "pop"
      const pop = (at) =>
        tl.set("#cat-spr", { scale: 1.08 }, at).to("#cat-spr", { scale: 1, duration: 0.15, ease: "steps(3)" }, at);
      // walk/run in from off-screen left
      const walkIn = (at, from, to, dur) =>
        tl.set("#cat-walk", { x: from }, at).to("#cat-walk", { x: to, duration: dur, ease: "none" }, at);
      const jump = (at) =>
        tl.to("#cat", { y: -70, duration: 0.12, ease: "steps(3)" }, at).to("#cat", { y: 0, duration: 0.16, ease: "steps(4)" }, at + 0.12);
      // speech bubble: stepped pop and typed text (mouth flaps are sprite frames, scheduled above)
      const say = (id, at, end, cps) => {
        const chars = document.getElementById(id).querySelectorAll(".ch");
        tl.fromTo("#" + id + " .bub-in", { scale: 0, transformOrigin: "0% 50%" }, { scale: 1, duration: 0.16, ease: "steps(4)" }, at);
        tl.fromTo(chars, { opacity: 0 }, { opacity: 1, duration: 0.001, stagger: cps }, at + 0.12);
        tl.to("#" + id + " .bub-in", { scale: 0, duration: 0.1, ease: "steps(3)" }, end - 0.1);
      };
"""


def _tabby_js(story):
    s = tabby.SCALE
    talk = {}  # beat index -> typing window
    for bid, a, b, text, pose in bubbles(story):
        typed = len(text) * story.type_speed
        i = next(k for k, bt in enumerate(story.beats) if bt.start <= a < bt.end)
        talk[i] = (a + 0.12, a + 0.12 + typed + 0.05)
    frames = []
    calls = []
    walk0 = _walk_in(story, story.beats[0])
    for i, b in enumerate(story.beats):
        sched = tabby.frames_for(b.pose, b.start, b.end, talk=talk.get(i),
                                 blinks=[t for t in story.blinks if b.start <= t < b.end])
        for j, (t, n) in enumerate(sched):
            if i == 0 and j == 0:
                continue  # frame 0 is the static HTML state
            x, y = tabby.frame_xy(*tabby.resolve(b.pose, n))
            frames.append([t, -x * s, -y * s])
        if i > 0:
            calls.append(f"      pop({b.start:g});")
        walk = _walk_in(story, b)
        rest = -walk0[0] if walk0 else 0     # #cat-walk's x when Oyen is home
        if walk and i > 0:
            calls.append(f"      walkIn({b.start:g}, {rest + walk[0]}, {rest}, {walk[1]:g});")
        elif walk:
            calls.append(f'      tl.to("#cat-walk", {{ x: {rest}, duration: {walk[1]:g}, ease: "none" }}, 0);')
    for bid, a, b, _text, _pose in bubbles(story):
        calls.append(f'      say("{bid}", {a:g}, {b:g}, {story.type_speed:g});')
    for t in story.jumps:
        calls.append(f"      jump({t:g});")
    data = ", ".join(f"[{t:g}, {x}, {y}]" for t, x, y in frames)
    return ("      // OYEN:START (generated by `python3 -m oyen install` from storyline.py)\n"
            + _TABBY_RUNTIME
            + f"      [{data}].forEach((f) => spr(f[0], f[1], f[2]));\n"
            + "\n".join(calls) + "\n      // OYEN:END\n")


# ---------------- install ----------------
def composition_duration(html):
    root = re.search(r"<div[^>]*data-composition-id=[^>]*>", html)
    m = root and re.search(r'data-duration="([\d.]+)"', root.group(0))
    if not m:
        raise ValueError("root composition has no data-duration")
    return float(m.group(1))


def install(video_dir):
    video_dir = Path(video_dir)
    story = load(video_dir)
    problems = story.problems()
    if problems:
        raise ValueError("storyline problems:\n  " + "\n  ".join(problems))
    index = video_dir / "index.html"
    html = index.read_text()
    duration = composition_duration(html)
    if story.duration > duration + 1e-6:
        raise ValueError(f"storyline runs to {story.duration:g}s but the composition is {duration:g}s")

    blocks = {"css": css_block(story), "html": html_block(story), "sfx": sfx_block(story),
              "js": js_block(story, duration)}
    for key, (pattern, needle) in MARKERS.items():
        if needle not in html:
            raise ValueError(f"{index}: missing {needle} marker block (see oyen/install.py docstring)")
        html, n = re.subn(pattern, lambda m, k=key: blocks[k], html, count=1, flags=re.S)
        assert n == 1, key
    index.write_text(html)

    if story.character == "tabby":
        (video_dir / "assets").mkdir(exist_ok=True)
        shutil.copy2(tabby.SHEET, video_dir / "assets" / TABBY_ASSET)
    sfx_dir = video_dir / "assets" / "sfx"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    for name in NEEDED_SFX:
        if not (sfx_dir / name).exists():
            shutil.copy2(SHARED_SFX / name, sfx_dir / name)
    return story.notes()
