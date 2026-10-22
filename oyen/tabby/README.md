# Oyen v2 (tabby)

Pixel-art orange tabby, drawn in Google Flow (Nano Banana) and turned into a sprite sheet.

- `flow/` the original Flow images, one animation each (frames left to right, facing right)
- `sources.json` which image is which animation, its size factor and playback sequence
- `oyen-tabby.png` / `oyen-tabby.json` the packed sheet (built, do not edit by hand)

Rebuild after adding or replacing a Flow image:

```bash
python3 tools/oyen_from_flow.py oyen/tabby/flow
python3 -m oyen poses          # gallery: oyen/gallery/tabby/oyen-tabby-animasi.png
```

A new animation = a new Flow image + an entry in `sources.json` (`scale`: tweak until the cat
matches the others in the gallery).

## Flow prompt

Attach a clean picture of Oyen (e.g. `oyen/gallery/tabby/oyen-tabby-duduk.png`) every time, then:

```
Use the attached orange tabby cat as the exact same character: same orange fur, same dark orange tabby
stripes, cream chest and paws, pink ears and nose, dark brown outline, same proportions. Pixel art sprite
sheet, 16-bit style, crisp hard-edged pixels, no anti-aliasing, no blur, limited palette. Side view,
facing right. Every frame at the same size and the same pixel scale, feet on the same ground line.
Frames in ONE horizontal row, evenly spaced, each cat fully visible with empty space around it.
Plain flat solid background color #20242C. No grid lines, no borders, no frames, no shadows, no text.
```

followed by the animation, e.g. `6-frame walk cycle, looping: legs alternate step by step, tail up and
gently swaying.` Keep frames apart (the cutter separates them by the background between them).
