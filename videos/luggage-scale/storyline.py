"""Oyen storyline for the digital luggage scale TikTok affiliate cut (~18.5s).

Footage: assets/source-portrait.mp4 (195s, sound removed). Usable moments:
box 0-3.5s, out of blister 25-34s, hanging + "Max.50kg/110lb" 43-50s,
LCD/buttons 50-53s, strap buckle 57-61s, coin battery (included in the pack) 28-30s / 83-86s / 152-160s,
LCD lit + UNIT kg -> 37°C -> 99°F 167-181s. The rest is empty wall.
No footage of a bag being weighed, so no accuracy claims.

  python3 -m oyen storyboard videos/luggage-scale
  python3 -m oyen install videos/luggage-scale
"""
from oyen.storyline import Beat, Storyline

STORYLINE = Storyline(
    title="Luggage scale digital (18.5s)",
    source="assets/source-portrait.mp4",
    beats=[
        Beat(0.0, 0.7, "1 Hook", "Tidur", None,
             "Oyen tidur. Skrin LCD belum menyala.", src=167.6),
        Beat(0.7, 2.2, "1 Hook", "Terkejut", "Bagasi overweight?!",
             "LCD menyala hijau + bass hit, Oyen terjaga. Caption: NAK FLY? / TIMBANG DULU!", src=168.9),
        Beat(2.2, 3.8, "2 Kotak", "Teruja", "Jom unboxing!",
             "Kotak produk. Caption: LUGGAGE SCALE / DIGITAL", src=1.0),
        Beat(3.8, 6.0, "3 Keluar pek", "Senyum", None,
             "Tarik keluar dari pek. Caption: SAIZ / TAPAK TANGAN", src=30.0),
        Beat(6.0, 9.0, "4 Max 50kg", "Kenyit mata", "Max 50kg tau~",
             "Close-up tulisan Max.50kg/110lb. Caption: TAHAN SAMPAI / 50KG", src=49.0),
        Beat(9.0, 10.6, "5 Strap", "Bercakap", "Sangkut kat beg je!",
             "Strap + cangkuk logam. Caption: STRAP / + CANGKUK", src=59.0),
        Beat(10.6, 12.6, "6 Bateri", "Thumbs up", "Bateri dah sedia~",
             "Bateri syiling yang datang sekali dalam pek. Caption: BATERI SYILING / DAH DISEDIAKAN", src=84.6),
        Beat(12.6, 15.6, "7 LCD", "Jatuh cinta", "Siap ada suhu!",
             "Tekan UNIT: kg -> 37°C -> 99°F (2x laju). Caption: LCD MENYALA / KG • LB • °C • °F", src=175.5),
        Beat(15.6, 17.7, "8 CTA", "Shopping", "Jom checkout!",
             "Oyen pegang beg kuning sebelah butang CTA.", src=170.5),
        Beat(17.7, 18.5, "8 CTA", "Kenyit mata", None,
             "Penutup: Oyen kenyit mata.", src=172.0),
    ],
    blinks=[5.0, 10.35],
    jumps=[0.7],  # wakes when the LCD lights up
)
