# video-claude — agent notes

Multi-video repo: TikTok 9:16 videos built with HyperFrames, plus the shared pixel mascot **Oyen**.
Videos are about different products; keep product-specific content inside `videos/<name>/` only.
The user writes in Malay; reply in Malay unless they switch.

## Layout
- `oyen/` — product-agnostic mascot package (character, storyline model, installer, storyboard, gallery). CLI: `python3 -m oyen {poses|check|storyboard|install} [videos/<name>]`, run from repo root.
- `videos/<name>/` — one HyperFrames project per video: `index.html`, `storyline.py` (`STORYLINE = Storyline(...)`), `storyboard/`, `assets/`.
- `templates/tiktok-9x16/` + `tools/new_video.py <name> [--source F --rotate cw|ccw]` — scaffold a new video.
- `promo/` — post assets: `python3 -m promo videos/<name>` renders `promo/thumbnail.png` (1080x1920 cover, via HyperFrames snapshot) and `promo/caption.txt` from `videos/<name>/promo.py` (`PROMO = Promo(...)`).
- `shared/` — `vendor/gsap.min.js`, `sfx/*.mp3` (Pixabay licence, see CREDITS). New videos get copies in `assets/`.
- Tests: `python3 -m unittest discover -s tests` (also checks every `videos/*/storyline.py` and `promo.py`).

## Workflow for a new video
1. Get footage (Drive via `pip install gdown; gdown <folder-url>` into the scratchpad). Probe it; phone clips are often portrait stored landscape: extract a frame both ways and check text orientation before choosing `--rotate`.
2. Analyse: contact sheets (`ffmpeg ... fps=1,tile`), find dead/repeated sections and the strongest hook moment; propose the cut.
3. Scaffold, edit `index.html` (shots as `<video class="clip">` with `data-start/duration/media-start`, captions in the top safe band, CTA to "beg kuning").
4. Plan Oyen in `storyline.py`, review `python3 -m oyen storyboard`, then `python3 -m oyen install`.
5. `npx --yes hyperframes@0.8.150 check`, snapshots (`snapshot --at ...`, `--zoom x,y,w,h`) and look at them.
6. Send a **draft preview** (`render -q draft`, scaled to 720p with a PREVIEW label). Render `-q delivery` only after the user approves. Don't commit renders or footage.
7. **Every final delivery also ships a cover thumbnail and a post caption** (user request): fill `promo.py` (best product frame, hook headline, Oyen pose, visible-fact badge; caption = hook + key facts + beg-kuning CTA + hashtags), run `python3 -m promo videos/<name>`, look at the PNG (keep the product, headline and Oyen clear of each other and inside the 3:4 grid crop y 240-1680), then send the MP4, `thumbnail.png` and paste the caption text in the reply. Commit `promo/` outputs.

## Gotchas learned
- `cdn.jsdelivr.net` is blocked by the proxy: load GSAP from `assets/vendor/gsap.min.js`.
- GSAP: a `tl.set` at t=0 may not render on seek; make the frame-0 state static HTML/CSS. For elements tweened many times use `set()`+`to()` (not repeated `fromTo`), so seeking doesn't show a later start state.
- Lint rejects template literals inside `querySelector`; build selector strings with `+`.
- Don't put `data-start` on both a `<video>` and its wrapper. Keep `id` on every `<audio>`.
- TikTok UI: keep text below ~150px from the top, away from the right edge (buttons) and the bottom ~400px (caption, product link).
- Don't invent product claims; ask the user or use what is visible in the footage.

## User preferences
- End/CTA scene: no arrow (the old pointer to the beg kuning). Use the template CTA: NAK SATU? / TEKAN / BEG KUNING + "CHECK HARGA PROMO" button, with Oyen beside it.
- Every final delivery includes `promo/thumbnail.png` + caption (workflow step 7).
