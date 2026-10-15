"""Post assets for a finished video: TikTok cover thumbnail + post caption.

Each video keeps `videos/<name>/promo.py` with `PROMO = Promo(...)`.
`python3 -m promo videos/<name>` writes into videos/<name>/promo/:
  thumbnail.png  1080x1920 cover (rendered with HyperFrames: same fonts + Oyen)
  caption.txt    post caption with hashtags
"""
from .model import Promo  # noqa: F401
