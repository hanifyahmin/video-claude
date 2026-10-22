# video-claude — agent notes

Multi-video repo: TikTok 9:16 videos built with HyperFrames, plus the shared pixel mascot **Oyen**.
Videos are about different products; keep product-specific content inside `videos/<name>/` only.
The user writes in Malay; reply in Malay unless they switch.

## Layout
- `oyen/` — product-agnostic mascot package (chibi character, `tabby/` Oyen v2 sprite sheet, storyline model, installer, storyboard, gallery). CLI: `python3 -m oyen {poses|check|storyboard|install} [videos/<name>]`, run from repo root.
- `videos/<name>/` — one HyperFrames project per video: `index.html`, `storyline.py` (`STORYLINE = Storyline(...)`), `storyboard/`, `assets/`.
- `templates/tiktok-9x16/` + `tools/new_video.py <name> [--source F --rotate cw|ccw --mute --grade bright|none --niche baby|rumah|gajet|makanan|travel|umum]` — scaffold a new video (bold theme; `--niche` picks the accent). The edit copy gets the `bright` grade by default (lift white point, saturation, light sharpen; user request: phone footage looked dull and dark); `--grade none` keeps it as shot.
- `promo/` — post assets: `python3 -m promo videos/<name>` renders `promo/thumbnail.png` (1080x1920 cover, via HyperFrames snapshot) and `promo/caption.txt` from `videos/<name>/promo.py` (`PROMO = Promo(...)`).
- `tools/bold_theme.py` (default look) and `tools/cute_theme.py` (older pastel look) restyle a composition by selector; safe to rerun.
- `shared/` — `vendor/gsap.min.js`, `sfx/*.mp3` (Pixabay licence, see CREDITS), `fonts/fredoka-latin.woff2` (OFL). New videos get copies in `assets/`.
- Tests: `python3 -m unittest discover -s tests` (also checks every `videos/*/storyline.py` and `promo.py`).

## Workflow for a new video
1. Get footage (Drive via `pip install gdown; gdown <folder-url>` into the scratchpad). Probe it; phone clips are often portrait stored landscape: extract a frame both ways and check text orientation before choosing `--rotate`.
2. Analyse: contact sheets (`ffmpeg ... fps=1,tile`), find dead/repeated sections and the strongest hook moment; propose the cut.
3. Scaffold, edit `index.html` (shots as `<video class="clip">` with `data-start/duration/media-start`, captions in the top safe band, CTA to "beg kuning").
4. Plan Oyen in `storyline.py`, review `python3 -m oyen storyboard`, then `python3 -m oyen install`.
5. `npx --yes hyperframes@0.8.150 check`, snapshots (`snapshot --at ...`, `--zoom x,y,w,h`) and look at them.
6. Send a **draft preview** (`render -q draft`, scaled to 720p with a PREVIEW label). Render `-q delivery` only after the user approves. Don't commit renders or footage.
7. **Every final delivery also ships a cover thumbnail and a post caption** (user request): fill `promo.py` (best product frame, hook headline, Oyen pose, visible-fact tags/features; caption = hook + key facts + beg-kuning CTA + hashtags), run `python3 -m promo videos/<name>`, look at the PNG (keep the product, headline and Oyen clear of each other and inside the 3:4 grid crop y 240-1680), then send the MP4, `thumbnail.png` and paste the caption text in the reply. Commit `promo/` outputs.

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
- Videos use the **bold** theme (user request: one look for a mixed niche, built for watch-through): full-bleed footage under a dark top fade, Montserrat, kicker in an accent pill, white uppercase big caption with a black outline and one key word in `<span class="hl">` (accent), accent CTA button, Oyen with a white outline and `Layout(style="bold")` bubble. The accent comes from the product's niche (`--niche` / `tools/bold_theme.py NICHES`; pill text must stay >= 3:1). The template has it; restyle an older video with `python3 tools/bold_theme.py videos/<name> --niche X`, set `layout=Layout(style="bold")`, rerun `oyen install`, add the `hl` spans and recheck caption widths (uppercase Montserrat Black is ~0.72em per character). Full-bleed footage: shot coordinates now equal screen coordinates (no 220px card offset).
- The older pastel `cute` look (Fredoka stickers, `tools/cute_theme.py`) is still used by tropika-*, vacuum-storage-bag, mop-tissue and bzu-bzu-cleansing-foam.
- Cover style is **bold** (`promo/bold.py`, user request: match the video and lead with a strong hook): full-bleed product frame, kicker pill, huge white uppercase headline with the *starred* word in the niche accent (`Promo.niche`), accent badge with one visible fact, up to 2 white tags, Oyen + bold bubble. Hook = problem or result in 2-3 short lines (question, number or before/after). A negative `frame_shift` moves the product down; its top edge fades into a blurred copy of the frame. Older covers keep `style="cute"` (cut-out product, `promo/cute.py`; `cutout=False` = photo card) or `"classic"`.
- **Oyen v2 (tabby)** is the default mascot (user's Google Flow art): `Storyline(character="tabby")`, poses are animations from `oyen/tabby` (Duduk, Bercakap, Menjilat, Makan, Tidur, Terkejut, Teruja, Gembira, Regang, Lompat, Jalan, Lari; gallery `oyen/gallery/tabby/`). Played as sprite frames switched by `background-position` at fixed times; Jalan/Lari walk in from the left via `#cat-walk` x (no CSS transform: HyperFrames rejects it); only Duduk/Bercakap flap the mouth while a line types; Terkejut/Regang/Lompat play once and hold. `Lari keluar` dashes off to the right; a speech bubble from the beat before it stays up and gets knocked away (with whoosh + impact SFX) — the user's CTA ending: Duduk "Jom checkout!" then Lari keluar. Placement: the cell's right edge (`tabby.ANCHOR_X`) is derived from the cell width so the widest frame's tail stays on screen. Rebuild the sheet from Flow images with `python3 tools/oyen_from_flow.py oyen/tabby/flow` (`oyen/tabby/README.md` has the prompt). Bold covers draw it with `Promo(character="tabby")`. The chibi (`character="chibi"`, default for old storylines) stays for the older videos.
- Oyen speaks at most 3 lines per video (hook reaction, one punchline, CTA), never repeating the caption; poses change on every beat (18 poses incl. Gelak, Sedih, Cool, Geram, Malu, Pening). `python3 -m oyen check` notes more lines or a repeated pose.
