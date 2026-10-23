"""Storyboard sheet: snapshots of index.html at each scene + notes.

  cd videos/toyo-g-scooter-gear-oil-vox
  npx --yes hyperframes@0.8.150 snapshot --at 1.75,5.25,8.75,12.25,16.25,20,23.5 --no-end -o SNAPDIR
  python3 storyboard/make_sheet.py SNAPDIR
"""
import glob
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/truetype/dejavu/"
NOTES = [
    ("1 HOOK  0-3.5s", "Scooter photo as a white-edged cut-out. 'Minyak enjin selalu tukar.' then 'Minyak gear?' gets the highlighter. Red marker circles the rear gearbox, label 'kotak gear belakang'."),
    ("2 INSIDE  3.5-7s", "Vox zoom-through into the gearbox: two meshing gears turn, the bearing (galas) at the centre. Mono labels with marker leaders."),
    ("3 THE ENEMIES  7-10.5s", "'3 benda ni makan gear': red wear scratches, rust spots and a rising thermometer with heat lines appear on the gears, each with its label."),
    ("4 THE PRODUCT  10.5-14s", "Product print slaps down with tape. Spec stamps thump in one by one (SAE 80W-90, API GL-5, MIL-L-2105, 100ml); highlighted note 'untuk semua jenis skuter & motosikal' (on the label)."),
    ("5 WHAT IT DOES  14-18.5s", "An amber oil film draws around the gears; the enemies fade out. Four strips tick in: protection, wear, rust & corrosion, shear & heat stability. Source line."),
    ("6 THE RESULT  18.5-21.5s", "The scooter cut-out rides off with speed lines: 'Pecutan lebih lancar*' + note 'minyak tahan lebih lama'. Footnote: *vs other conventional lubricants, per the product description."),
    ("7 CTA  21.5-25.5s", "Nak satu? / Tekan BEG KUNING (highlighter), black CHECK HARGA PROMO button pulses, the product print slaps down under it. No mascot in the Vox style."),
]
PALETTE = [((241, 236, 226), "newsprint paper"), ((255, 230, 0), "yellow highlighter"), ((232, 64, 42), "red marker"),
           ((29, 58, 138), "navy (product, stamps)"), ((242, 165, 22), "amber (oil film)"), ((159, 214, 204), "mint (diagram accents)")]
STYLE = ["Headlines: Archivo Black", "Labels/stamps: Space Mono", "Flat diagrams, ink outlines", "Gears turn, camera zooms through",
         "Stop-motion 'boil' at 12fps", "Facts: label + your description", "No 'sintetik' (label: CONVENTIONAL)", "No mascot (Vox style)"]


def main(snapdir):
    fs = sorted(glob.glob(snapdir + "/frame-*.png"), key=lambda f: float(f.split("-at-")[1][:-5]))
    bold, reg = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 24), ImageFont.truetype(F + "DejaVuSans.ttf", 19)
    W, H, T, cols = 405, 720, 250, 4
    sheet = Image.new("RGB", (cols * (W + 20) + 20, 2 * (H + T + 20) + 90), (36, 34, 32))
    d = ImageDraw.Draw(sheet)
    d.text((20, 26), "TOYO-G Scooter Gear Oil 80W-90 - VOX-STYLE STORYBOARD (25.5s, text + music)",
           font=ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 32), fill=(255, 230, 0))
    for i, f in enumerate(fs):
        x, y = 20 + (i % cols) * (W + 20), 90 + (i // cols) * (H + T + 20)
        sheet.paste(Image.open(f).convert("RGB").resize((W, H)), (x, y))
        title, note = NOTES[i]
        d.rectangle([x, y + H, x + W, y + H + T], fill=(250, 248, 242))
        d.text((x + 12, y + H + 10), title, font=bold, fill=(20, 20, 20))
        for k, line in enumerate(textwrap.wrap(note, 37)):
            d.text((x + 12, y + H + 46 + k * 24), line, font=reg, fill=(40, 40, 40))
    x, y = 20 + 3 * (W + 20), 90 + (H + T + 20)
    d.rectangle([x, y, x + W, y + H + T], fill=(241, 236, 226))
    d.text((x + 16, y + 16), "STYLE", font=bold, fill=(20, 20, 20))
    for j, (c, name) in enumerate(PALETTE):
        d.rectangle([x + 16, y + 60 + j * 52, x + 60, y + 100 + j * 52], fill=c, outline=(20, 20, 20), width=2)
        d.text((x + 74, y + 68 + j * 52), name, font=reg, fill=(20, 20, 20))
    for k, line in enumerate(STYLE):
        d.text((x + 16, y + 390 + k * 30), "- " + line, font=reg, fill=(20, 20, 20))
    sheet.save("storyboard/STORYBOARD.png")


if __name__ == "__main__":
    main(sys.argv[1])
