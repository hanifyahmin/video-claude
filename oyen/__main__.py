"""Oyen command line. Run from the repo root.

  python3 -m oyen poses                      regenerate oyen/gallery/poses/
  python3 -m oyen check <video_dir>          validate a video's storyline.py
  python3 -m oyen storyboard <video_dir>     storyboard PNG + STORYLINE.md
  python3 -m oyen install <video_dir>        write Oyen into the video's index.html
"""
import sys

from . import install, sheet, storyboard
from .storyline import load


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, args = argv[0], argv[1:]
    if cmd == "poses":
        print(sheet.render())
        return 0
    if len(args) != 1:
        print(f"usage: python3 -m oyen {cmd} <video_dir>")
        return 2
    video = args[0]
    story = load(video)
    problems = story.problems()
    for p in problems:
        print("error:", p)
    for n in story.notes():
        print("note:", n)
    if problems:
        return 1
    if cmd == "storyboard":
        print(storyboard.render(video))
    elif cmd == "install":
        install.install(video)
        print(f"installed Oyen into {video}/index.html")
    elif cmd != "check":
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
