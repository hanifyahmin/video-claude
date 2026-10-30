"""Contact sheet of rendered stills: python3 contact_sheet.py out.png t1:label t2:label ..."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
out, items = sys.argv[1], [a.split(":", 1) for a in sys.argv[2:]]
cols, tw, th, lab = 4, 360, 640, 54
rows = (len(items) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw + (cols + 1) * 12, rows * (th + lab) + (rows + 1) * 12), (24, 22, 20))
f = ImageFont.truetype(str(HERE / "assets/fonts/courierprime-CourierPrime-Regular.ttf"), 19)
for k, (t, label) in enumerate(items):
    im = Image.open(HERE / "renders/frames" / f"t{float(t):07.2f}.png").resize((tw, th), Image.LANCZOS)
    x, y = 12 + (k % cols) * (tw + 12), 12 + (k // cols) * (th + lab + 12)
    sheet.paste(im, (x, y + lab))
    sec = float(t)
    ImageDraw.Draw(sheet).text((x, y + 6), f"{int(sec // 60)}:{sec % 60:04.1f}  {label}", font=f, fill=(240, 220, 180))
sheet.save(out)
print(out, sheet.size)
