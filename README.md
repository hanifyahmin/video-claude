# video-claude

Video TikTok (9:16) yang dibina dengan [HyperFrames](https://hyperframes.heygen.com), dengan maskot **Oyen**, kucing oren pixel.
Satu repo untuk banyak video: Oyen dan aset dikongsi, dan setiap video ada folder sendiri.

```
oyen/                  pakej maskot (dikongsi semua video)
  character.py         kepala/badan Oyen + semua postur (POSE_SPECS)
  storyline.py         model data: Beat, Layout, Storyline
  install.py           pasang Oyen dalam index.html ikut storyline
  storyboard.py        storyboard PNG + STORYLINE.md untuk semakan
  sheet.py             galeri postur → oyen/gallery/poses/
  gallery/             imej postur + eksplorasi reka bentuk awal
promo/                 thumbnail cover + caption TikTok untuk setiap video
shared/                aset dikongsi (gsap.min.js, SFX + CREDITS)
templates/tiktok-9x16/ template video baru (komposisi + storyline permulaan)
tools/new_video.py     cipta video baru dari template
videos/<nama>/         satu projek HyperFrames bagi setiap video
  index.html           komposisi (shot, caption, CTA, SFX)
  storyline.py         apa Oyen buat & cakap, ikut masa
  promo.py             teks thumbnail + caption post
  promo/               thumbnail.png + caption.txt (dijana)
  storyboard/          storyboard + STORYLINE.md (dijana)
  assets/              sfx, vendor, footage (footage tidak masuk git)
tests/                 ujian unit Oyen
```

## Buat video baru

```bash
# 1. scaffold (footage portrait yang tersimpan landscape → --rotate cw)
python3 tools/new_video.py nama-produk --source /path/footage.mp4 --rotate cw --niche gajet
#    (footage dicerahkan & ditajamkan secara automatik; --grade none untuk kekalkan asal)

# 2. sunting videos/nama-produk/index.html   → shot footage, caption, CTA, data-duration
# 3. sunting videos/nama-produk/storyline.py → babak Oyen (postur + dialog)

# 4. semak & pasang Oyen
python3 -m oyen check videos/nama-produk
python3 -m oyen storyboard videos/nama-produk     # tengok storyboard/oyen-storyboard.png
python3 -m oyen install videos/nama-produk

# 5. sahkan & preview
cd videos/nama-produk
npx --yes hyperframes@0.8.150 check
npx --yes hyperframes@0.8.150 render -q draft -o renders/draft.mp4        # preview
npx --yes hyperframes@0.8.150 render -q delivery -o renders/final.mp4     # final (lepas approve)

# 6. thumbnail + caption (bersama final)
cd ../.. && python3 -m promo videos/nama-produk    # → videos/nama-produk/promo/thumbnail.png + caption.txt
# gaya cover lalai "cute": produk dipotong (remove-background), sticker headline, tag pink, barisan ikon ciri
```

## Gaya video

Lalai: gaya **bold** (`tools/bold_theme.py`). Footage penuh skrin, font Montserrat, baris kecil dalam pil warna aksen, baris besar huruf besar putih berbingkai hitam dengan satu perkataan kunci berwarna aksen, butang CTA warna aksen. Warna aksen ikut niche: `--niche baby|rumah|gajet|makanan|travel|umum` masa `new_video.py`, atau `python3 tools/bold_theme.py videos/nama --niche X` untuk video lama.

Gaya lama **comel** (pastel, Fredoka) masih ada dalam `tools/cute_theme.py`.

## Oyen

Postur yang ada: lihat `oyen/gallery/poses/oyen-postur.png`.

| Postur | Bercakap | Kelip mata |
|---|---|---|
| Senyum, Teruja, Shopping, Bercakap | ✓ | ✓ |
| Jatuh cinta, Kenyit mata, Berfikir, Layan lagu, Thumbs up | ✓ | – |
| Terkejut, Tidur, Makan | – | – |

- **Tambah postur:** tambah entri dalam `POSE_SPECS` (`oyen/character.py`), kemudian `python3 -m oyen poses`.
- **Peraturan storyline:** babak bermula di 0s, bersambung tanpa jurang dan tamat ≤ `data-duration` komposisi. Dialog ≤ 20 aksara supaya tak kena butang kanan TikTok.
- `install` cuma menulis antara penanda `OYEN:*` dalam `index.html`, jadi selamat dijalankan semula.

## Ujian

```bash
python3 -m unittest discover -s tests
```
