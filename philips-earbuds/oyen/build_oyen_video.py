"""Install Oyen into ../index.html following storyline.BEATS.

python3 build_oyen_video.py

Idempotent: everything it writes sits between OYEN:START / OYEN:END markers
(CSS, HTML, SFX, timeline), and a rerun replaces those blocks. On the first
run it also removes the earlier single-sprite cat mascot.
"""
import re
from pathlib import Path

import oyen_poses as P
from oyen_sprites import PAL
from storyline import BEATS

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SCALE = 12  # px per sprite pixel -> 336 x 288
CPS = 0.032  # seconds per typed character

# ---------------- sprite frames ----------------
TALK = P.MOUTH_TALK
FRAMES = {
    "tidur": P.POSES["Tidur"],
    "terkejut": P.POSES["Terkejut"],
    "kenyit": P.POSES["Kenyit mata"],
    "kenyit-t": P.build(P.eyes_open(P.L_EYE) + P.eyes_happy([P.R_EYE]) + TALK),
    "lagu": P.POSES["Layan lagu"],
    "lagu-t": P.build(P.eyes_happy() + TALK, [P.NOTE], headphones=True),
    "cinta": P.POSES["Jatuh cinta"],
    "cinta-t": P.build(P.eyes_heart() + TALK, [P.HEARTS]),
    "cakap": P.POSES["Senyum"],
    "cakap-t": P.POSES["Bercakap"],
    "blink": P.build([(7, c, "K") for c in P.L_EYE + P.R_EYE] + P.MOUTH_UU),
    "teruja": P.POSES["Teruja"],
    "teruja-t": P.build(P.eyes_sparkle() + TALK, [P.SPARKS]),
    "senyum": P.POSES["Senyum"],
    "shop": P.POSES["Shopping"],
    "shop-t": P.build(P.eyes_sparkle() + TALK, [P.BAG, P.BAG_PAW], tail=False),
    "thumbs": P.POSES["Thumbs up"],
}
# storyline pose name -> (resting frame, talking frame or None)
POSE_FRAMES = {
    "Tidur": ("tidur", None),
    "Terkejut": ("terkejut", None),  # mouth is already an open "o"
    "Kenyit mata": ("kenyit", "kenyit-t"),
    "Layan lagu": ("lagu", "lagu-t"),
    "Jatuh cinta": ("cinta", "cinta-t"),
    "Bercakap": ("cakap", "cakap-t"),
    "Teruja": ("teruja", "teruja-t"),
    "Senyum": ("senyum", None),
    "Shopping": ("shop", "shop-t"),
    "Thumbs up": ("thumbs", None),
}
BLINKS = [(10.3, "cakap"), (14.15, "senyum")]  # (time, frame to return to)
JUMPS = [0.45, 14.55]  # wakes up at the lid-open hit, jumps at the KLIK


def hexc(k):
    return "#%02x%02x%02x" % PAL[k]


def rle_rects(rows):
    out = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            k = row[x]
            if k == ".":
                x += 1
                continue
            x2 = x
            while x2 < len(row) and row[x2] == k:
                x2 += 1
            out.append(f'<rect x="{x}" y="{y}" width="{x2 - x}" height="1" fill="{hexc(k)}"/>')
            x = x2
    return "".join(out)


def sprite_svg():
    w, h = P.CW, P.CH
    first = POSE_FRAMES[BEATS[0][3]][0]  # pose at t=0 is the static initial state
    groups = "".join(f'<g class="oy-f" id="oy-{fid}" style="opacity: {1 if fid == first else 0}">{rle_rects(rows)}</g>'
                     for fid, rows in FRAMES.items())
    return (f'<svg id="cat-svg" width="{w * SCALE}" height="{h * SCALE}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges">{groups}</svg>')


# ---------------- beats -> bubbles ----------------
def bubbles():
    out = []
    for i, (a, b, _scene, pose, line, _note, _src) in enumerate(BEATS):
        if not line:
            continue
        start = round(a + (0.15 if a > 0.5 else 0.15), 2)
        end = round(b - 0.05, 2)
        out.append((f"ob{len(out)}", start, end, line, pose))
    return out


TAIL_SVG = ('<svg class="bub-tail" width="30" height="30" viewBox="0 0 5 5" shape-rendering="crispEdges">'
            '<rect x="4" y="0" width="1" height="5" fill="#fffdf5"/><rect x="3" y="1" width="1" height="3" fill="#fffdf5"/>'
            '<rect x="2" y="2" width="1" height="1" fill="#fffdf5"/><rect x="3" y="0" width="1" height="1" fill="#2a160b"/>'
            '<rect x="2" y="1" width="1" height="1" fill="#2a160b"/><rect x="1" y="2" width="1" height="1" fill="#2a160b"/>'
            '<rect x="2" y="3" width="1" height="1" fill="#2a160b"/><rect x="3" y="4" width="1" height="1" fill="#2a160b"/></svg>')

CSS = """      /* OYEN:CSS:START */
      #cat {
        position: absolute;
        left: 6px;
        top: 1250px;
        width: %(w)dpx;
        height: %(h)dpx;
      }
      #cat-svg {
        display: block;
        filter: drop-shadow(6px 6px 0 rgba(0, 0, 0, 0.45));
      }
      .bub {
        position: absolute;
        left: 352px;
        top: 1302px;
        width: 700px;
        height: 130px;
      }
      .bub-in {
        position: absolute;
        left: 0;
        top: 0;
        max-width: 700px;
        padding: 22px 28px;
        background: #fffdf5;
        box-shadow:
          0 -6px 0 0 #2a160b,
          0 6px 0 0 #2a160b,
          -6px 0 0 0 #2a160b,
          6px 0 0 0 #2a160b,
          12px 12px 0 0 rgba(0, 0, 0, 0.35);
        font-family: "Space Mono", monospace;
        font-weight: 700;
        font-size: 40px;
        line-height: 1.2;
        color: #2a160b;
        white-space: nowrap;
      }
      .bub-tail {
        position: absolute;
        left: -30px;
        top: 34px;
        width: 30px;
        height: 30px;
      }
      /* OYEN:CSS:END */
""" % {"w": P.CW * SCALE, "h": P.CH * SCALE}


def html_block():
    lines = ["      <!-- OYEN:START (generated by oyen/build_oyen_video.py) -->",
             f'      <div id="cat">{sprite_svg()}</div>']
    for bid, a, b, text, _pose in bubbles():
        chars = "".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in text)
        lines.append(f'      <div id="{bid}" class="bub clip" data-start="{a:g}" data-duration="{round(b - a, 2):g}" '
                     f'data-track-index="6"><div class="bub-in">{TAIL_SVG}{chars}</div></div>')
    lines.append("      <!-- OYEN:END -->")
    return "\n".join(lines)


def sfx_block():
    lines = ["      <!-- OYEN:SFX:START -->"]
    tr = 50
    for bid, a, _b, text, _pose in bubbles():
        typ = min(round(len(text) * CPS + 0.05, 2), 1.45)
        lines.append(f'      <audio id="sfx-pop-{bid}" src="assets/sfx/pop.mp3" data-start="{a:g}" data-track-index="{tr}" data-volume="0.45"></audio>')
        lines.append(f'      <audio id="sfx-type-{bid}" src="assets/sfx/typing.mp3" data-start="{round(a + 0.12, 2):g}" data-duration="{typ:g}" data-track-index="{tr + 1}" data-volume="0.22"></audio>')
        tr += 2
    lines.append("      <!-- OYEN:SFX:END -->")
    return "\n".join(lines)


def js_block():
    calls = []
    for a, _b, _scene, pose, _line, _note, _src in BEATS[1:]:  # BEATS[0] is the HTML initial state
        calls.append(f'      pose("{POSE_FRAMES[pose][0]}", {a:g});')
    for bid, a, b, _text, pose in bubbles():
        rest, talk = POSE_FRAMES[pose]
        talk_arg = f'"{talk}"' if talk else "null"
        calls.append(f'      say("{bid}", {a:g}, {b:g}, "{rest}", {talk_arg});')
    for t, back in BLINKS:
        calls.append(f'      frame("blink", {t:g}); frame("{back}", {t + 0.12:g});')
    for t in JUMPS:
        calls.append(f'      jump({t:g});')
    return """      // OYEN:START (generated by oyen/build_oyen_video.py from oyen/storyline.py)
      // every sprite swap is a tl.set at a fixed time -> seek-safe
      const frame = (id, at) => tl.set(".oy-f", { opacity: 0 }, at).set("#oy-" + id, { opacity: 1 }, at);
      tl.set("#cat-svg", { transformOrigin: "50%% 100%%", scale: 1, y: 0 }, 0);
      // a pose change is a frame swap plus a stepped pixel "pop"
      const pose = (id, at) => {
        frame(id, at);
        if (at > 0) tl.set("#cat-svg", { scale: 1.14 }, at).to("#cat-svg", { scale: 1, duration: 0.15, ease: "steps(3)" }, at);
      };
      const jump = (at) =>
        tl.to("#cat", { y: -70, duration: 0.12, ease: "steps(3)" }, at).to("#cat", { y: 0, duration: 0.16, ease: "steps(4)" }, at + 0.12);
      // idle bob in whole sprite pixels
      for (let t = 0.9; t < 18.0; t += 0.6) tl.set("#cat-svg", { y: -12 }, t).set("#cat-svg", { y: 0 }, t + 0.3);
      // speech bubble: stepped pop, typed text, mouth flaps while typing
      const CPS = %(cps)s;
      const say = (id, at, end, rest, talk) => {
        const chars = document.getElementById(id).querySelectorAll(".ch");
        const typed = chars.length * CPS;
        tl.fromTo("#" + id + " .bub-in", { scale: 0, transformOrigin: "0%% 50%%" }, { scale: 1, duration: 0.16, ease: "steps(4)" }, at);
        tl.fromTo(chars, { opacity: 0 }, { opacity: 1, duration: 0.001, stagger: CPS }, at + 0.12);
        if (talk) {
          for (let t = at + 0.12, i = 0; t < at + 0.12 + typed; t += 0.09, i++) frame(i %% 2 ? rest : talk, t);
          frame(rest, at + 0.12 + typed + 0.02);
        }
        tl.to("#" + id + " .bub-in", { scale: 0, duration: 0.1, ease: "steps(3)" }, end - 0.1);
      };
%(calls)s
      // OYEN:END
""" % {"cps": CPS, "calls": "\n".join(calls)}


def main():
    s = INDEX.read_text()
    # --- CSS ---
    if "/* OYEN:CSS:START */" in s:
        s = re.sub(r"      /\* OYEN:CSS:START \*/.*?/\* OYEN:CSS:END \*/\n", lambda m: CSS, s, flags=re.S)
    else:
        s, n = re.subn(r"      /\* ---------- pixel cat mascot ---------- \*/.*?(?=    </style>)", lambda m: CSS, s, flags=re.S)
        assert n == 1, "old mascot CSS not found"
    # --- HTML ---
    if "<!-- OYEN:START" in s:
        s = re.sub(r"      <!-- OYEN:START.*?<!-- OYEN:END -->", lambda m: html_block(), s, flags=re.S)
    else:
        s, n = re.subn(r"      <!-- ================= PIXEL CAT MASCOT ================= -->.*?(?=\n\n      <div id=\"flash\">)",
                       lambda m: html_block(), s, flags=re.S)
        assert n == 1, "old mascot HTML not found"
    # --- SFX ---
    if "<!-- OYEN:SFX:START -->" in s:
        s = re.sub(r"      <!-- OYEN:SFX:START -->.*?<!-- OYEN:SFX:END -->", lambda m: sfx_block(), s, flags=re.S)
    else:
        s = re.sub(r'\n      <audio id="sfx-(bub|type)-b\d"[^\n]*</audio>', "", s)
        s = s.replace("\n    </div>\n\n    <script>", "\n" + sfx_block() + "\n    </div>\n\n    <script>", 1)
    # --- timeline ---
    if "// OYEN:START" in s:
        s = re.sub(r"      // OYEN:START.*?// OYEN:END\n", lambda m: js_block(), s, flags=re.S)
    else:
        s, n = re.subn(r"      // ---------- PIXEL CAT MASCOT \(Clippy-style helper\) ----------.*?(?=\n      window\.__timelines)",
                       lambda m: js_block().rstrip("\n"), s, flags=re.S)
        assert n == 1, "old mascot timeline not found"
    for gone in ("cat-alert", "cat-tail-a", "sfx-bub-b"):
        assert gone not in s, gone
    INDEX.write_text(s)
    print("bubbles:", [(b[0], b[1], b[2], b[3]) for b in bubbles()])


if __name__ == "__main__":
    main()
