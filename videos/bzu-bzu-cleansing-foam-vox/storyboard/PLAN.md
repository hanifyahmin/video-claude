# BZU BZU Cleansing Foam — Vox-style explainer (plan)

25.5s, 9:16, text + music (no voiceover). See `STORYBOARD.png` for the frames: each one is a
snapshot of the real layout in `index.html`, so the build animates exactly these frames.

## Look
- **Collage on newsprint**: warm paper texture, photo *prints* of the footage (white border,
  masking tape, drop shadow), cut-outs with a white sticker edge, halftone dots.
- **Annotation**: yellow highlighter swipes on real label text, red marker circles/arrows,
  Space Mono notes and a source line ("Sumber: label …"), as Vox does with documents.
- **Type**: Archivo Black headlines with one highlighted phrase, Space Mono labels.
- **Palette**: paper #F1ECE2, ink #141414, highlighter #FFE600, marker #E8402A, teal #2F9E97.
- **Motion**: the camera drifts and pushes across a 2.5D collage (layers at different depths),
  prints slap down with tape, highlighter/marker strokes draw on, a light stop-motion "boil"
  (tiny offsets at 12 fps) on notes and drawings, torn-paper wipes between scenes.
- Footage plays *inside* the prints (dirty bottle, clean bottle, pumping) so it's still real.

## Scenes
| # | Time | Beat | Content (all facts from the label or the footage) |
|---|------|------|---------------------------------------------------|
| 1 | 0–3.5 | Hook | "Sisa susu masih melekat?" + print of the bottle with milk residue, circled |
| 2 | 3.5–7 | Answer | "1 botol, 4 kegunaan": front label, highlight "FOR MILK BOTTLES, DISH, TOYS, FRUITS AND VEGETABLES" |
| 3 | 7–11.5 | Document | Back label: highlight "Foam pump to save water and reduce washing time", "Mild and gentle to hands" → notes "jimat air & masa", "lembut di tangan" |
| 4 | 11.5–14.5 | Zero list | 0% box → strips: pewangi / peluntur & paraben / pewarna tiruan / sabun & alkohol (+ tanpa sulfat, 100% bahan tumbuhan*) |
| 5 | 14.5–18 | How to | Diagram from the washing directions: 6 pam → 5L air → rendam 10 min → bilas |
| 6 | 18–21.5 | Proof | Before/after prints: residue circled, clean bottle ticked — "Mudah dibilas" |
| 7 | 21.5–25.5 | CTA | Nak satu? / Tekan BEG KUNING / CHECK HARGA PROMO + product print (no mascot in the Vox style) |

## Sound
Music bed in the explainer register (soft synth pulse, no drums) generated like
`tools/lofi_bed.py` until a real track is supplied; SFX on every action: paper slap, tape,
marker squeak (click/whoosh-short), highlighter swipe (whoosh-short), page-turn whoosh on wipes.

## Assets (`make_assets.py`)
paper texture, tape, torn edge, prints (dirty, clean, front, back, zero) and cut-outs
(hand pumping, clean bottle) from the footage; fonts are cached by HyperFrames.
