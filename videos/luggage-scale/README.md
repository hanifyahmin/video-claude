# luggage-scale

TikTok 9:16 video built with HyperFrames + Oyen. See the repo README for the workflow.

- Source footage (not in git): Drive `affiliate/electronic luggage scale/VID_20261015_211934.mp4` (195s, portrait via rotation metadata).
  Rebuild: `python3 tools/new_video.py` copies it to `assets/source.mp4`; the edit copy `assets/source-portrait.mp4` has the sound removed (`--mute`).
- Composition: `index.html`
- Oyen storyline: `storyline.py` → `python3 -m oyen install videos/luggage-scale`
