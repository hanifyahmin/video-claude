"""Scaffold a new video project from templates/tiktok-9x16.

  python3 tools/new_video.py <name> [--source FILE] [--rotate cw|ccw|none] [--mute]
                                    [--grade bright|none] [--niche NICHE] [--kicker TEXT] [--hook TEXT]

Creates videos/<name>/ with the composition, a starter Oyen storyline, the
shared GSAP, SFX and fonts copied into assets/, and (with --source) the footage as
assets/source.<ext> plus an edit-friendly assets/source-portrait.mp4
(rotated if --rotate is given; phones often store portrait clips sideways;
--mute drops the camera sound from the edit copy; --grade bright, the default,
brightens and sharpens dull phone footage in the edit copy, the original stays as is).
The page uses the bold theme (tools/bold_theme.py); --niche picks its accent colour.
"""
import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import bold_theme  # noqa: E402
TEMPLATE = REPO / "templates" / "tiktok-9x16"
SHARED = REPO / "shared"


def probe(path):
    """(width, height, duration) as displayed, i.e. after rotation metadata."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:stream_side_data=rotation:format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    s = data["streams"][0]
    w, h = s["width"], s["height"]
    if any(abs(int(sd.get("rotation", 0))) == 90 for sd in s.get("side_data_list", [])):
        w, h = h, w
    return w, h, float(data["format"]["duration"])


# Colour/sharpness passes for the edit copy. "bright" suits phone clips shot in soft window light,
# where white tiles and labels come out grey: lift the white point, open the mids a little,
# add saturation, then a light unsharp mask. It cannot recover focus or light the clip never had.
GRADES = {
    "bright": ("colorlevels=rimin=0.03:gimin=0.03:bimin=0.03:rimax=0.86:gimax=0.86:bimax=0.88,"
               "eq=gamma=1.08:contrast=1.06:saturation=1.28,"
               "unsharp=5:5:1.0:3:3:0.0"),
    "none": None,
}
ROTATIONS = {"cw": "transpose=1", "ccw": "transpose=2", "none": None}


def video_filter(rotate="none", grade="bright"):
    """ffmpeg -vf chain for the edit copy (rotation first, then the grade), or None."""
    steps = [f for f in (ROTATIONS[rotate], GRADES[grade]) if f]
    return ",".join(steps) or None


def make_portrait(src, dst, rotate, mute=False, grade="bright"):
    """Edit copy of the footage. ffmpeg already applies rotation metadata; --rotate is for clips without it."""
    chain = video_filter(rotate, grade)
    vf = ["-vf", chain] if chain else []
    audio = ["-an"] if mute else ["-c:a", "aac", "-b:a", "160k"]
    # dense keyframes (-g 15) keep frame-accurate seeking cheap in the browser
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), *vf, "-c:v", "libx264", "-crf", "16",
                    "-preset", "medium", "-g", "15", "-pix_fmt", "yuv420p", *audio,
                    "-movflags", "+faststart", str(dst)], check=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="kebab-case project name, e.g. tumbler-stanley")
    ap.add_argument("--source", type=Path, help="footage file to copy into assets/")
    ap.add_argument("--rotate", choices=["cw", "ccw", "none"], default="none",
                    help="rotate the footage into portrait (check a frame first)")
    ap.add_argument("--mute", action="store_true", help="drop the footage's sound in the edit copy")
    ap.add_argument("--grade", choices=sorted(GRADES), default="bright",
                    help="colour pass for the edit copy: bright (default) lifts dull footage, none keeps it as shot")
    ap.add_argument("--niche", choices=sorted(bold_theme.NICHES), default="umum",
                    help="accent colour of the bold theme: baby blue, rumah green, gajet yellow, makanan red, "
                         "travel orange, umum yellow")
    ap.add_argument("--kicker", default="PRODUK NI…")
    ap.add_argument("--hook", default="WAJIB ADA!")
    args = ap.parse_args(argv)

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.name):
        ap.error("name must be kebab-case: lowercase letters, digits and dashes")
    dest = REPO / "videos" / args.name
    if dest.exists():
        ap.error(f"{dest} already exists")

    shutil.copytree(TEMPLATE, dest)
    subs = {"{{NAME}}": args.name, "{{KICKER}}": args.kicker, "{{HOOK}}": args.hook,
            "{{CREATED_AT}}": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "{{SOURCE_NOTE}}": f"`{args.source.name}`" if args.source else "add with --source"}
    for f in dest.iterdir():
        if f.suffix in {".html", ".py", ".json", ".md"}:
            text = f.read_text()
            for k, v in subs.items():
                text = text.replace(k, v)
            f.write_text(text)

    page = dest / "index.html"
    page.write_text(bold_theme.restyle(page.read_text(), args.niche))

    (dest / "assets" / "vendor").mkdir(parents=True)
    shutil.copy2(SHARED / "vendor" / "gsap.min.js", dest / "assets" / "vendor")
    shutil.copytree(SHARED / "sfx", dest / "assets" / "sfx")
    shutil.copytree(SHARED / "fonts", dest / "assets" / "fonts")

    if args.source:
        raw = dest / "assets" / f"source{args.source.suffix.lower()}"
        shutil.copy2(args.source, raw)
        w, h, dur = probe(raw)
        print(f"source: {w}x{h}, {dur:.1f}s")
        if w > h and args.rotate == "none":
            print("  note: footage is landscape; if it was filmed upright, rerun make_portrait with --rotate cw/ccw")
        make_portrait(raw, dest / "assets" / "source-portrait.mp4", args.rotate, args.mute, args.grade)
        pw, ph, _ = probe(dest / "assets" / "source-portrait.mp4")
        print(f"assets/source-portrait.mp4: {pw}x{ph}, grade: {args.grade}")

    print(f"""
created {dest.relative_to(REPO)} (bold theme, niche {args.niche})
next:
  1. edit videos/{args.name}/index.html   (footage shots, captions, CTA, root data-duration)
  2. edit videos/{args.name}/storyline.py (Oyen beats; must end at the root duration)
  3. python3 -m oyen storyboard videos/{args.name} && python3 -m oyen install videos/{args.name}
  4. cd videos/{args.name} && npx --yes hyperframes@0.8.150 check
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
