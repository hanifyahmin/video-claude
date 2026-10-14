# Storyline Oyen — Philips earbuds (18.2s)

Oyen ialah maskot gaya Clippy. Mini-cerita: Oyen tidur di sudut, terjaga bila
lid dibuka, jatuh cinta dengan earbuds, terangkan ciri-cirinya, terkejut dengan
bunyi KLIK, kemudian ajak penonton checkout.

Sumber data: `storyline.py` (`BEATS`). Storyboard: `storyboard/oyen-storyboard.png`.

| Masa (s) | Babak | Postur | Dialog Oyen | Nota animasi |
|---|---|---|---|---|
| 0.00–0.45 | 1 Hook | Tidur | — | Oyen dah ada di frame 0, tidur dengan Zz |
| 0.45–2.20 | 1 Hook | Terkejut | Eh?! Mahal ke ni? | Lid terbuka + bass hit: Oyen terjaga dan melompat, "!" |
| 2.20–3.80 | 2 Logo PHILIPS | Kenyit mata | Brand PHILIPS tau~ | Kenyit masa logo + LED |
| 3.80–5.50 | 3 Tarik earbud | Layan lagu | Jom layan lagu~ | Headphone muncul (pop), not muzik bergoyang |
| 5.50–8.80 | 4 Close-up | Jatuh cinta | Cantiknya chrome~ | Mata love + hati, serentak dengan kilauan |
| 8.80–11.40 | 5 Casing | Bercakap | Kecik, muat poket! | Pose asas bercakap |
| 11.40–13.70 | 6 Charge | Teruja | Charge guna USB-C! | Mata bersinar, mulut ternganga |
| 13.70–14.55 | 7 Tutup lid | Senyum | — | Diam, tengok lid ditutup |
| 14.55–15.30 | 7 KLIK! | Terkejut | — | Lompat tepat pada bunyi KLIK |
| 15.30–17.40 | 8 CTA | Shopping | Jom checkout! | Pegang beg kuning, sebelah butang CTA |
| 17.40–18.20 | 8 CTA | Thumbs up | — | Penutup: thumbs up + kenyit |

Tidak digunakan: Berfikir, Makan.

Peraturan:
- Bubble maksimum ~20 aksara supaya tak sampai ke butang kanan TikTok.
- Masa bercakap, cuma layer mulut yang bergerak; mata kekal ikut postur.
- Tukar postur dengan "pop" pixel (steps) serentak dengan cut video.
