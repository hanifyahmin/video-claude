"""Music analysis for the lyric video: tempo, beats, energy curve, section boundaries.

    python3 videos/cara-pulang-yang-benar/analyse.py <song.mp3> [<no_vocals.wav>]

Writes analysis.json next to this file. Curves are sampled at FPS so the renderer
can index them by frame number.
"""
import json
import sys
from pathlib import Path

import librosa
import numpy as np

FPS = 24
SR = 22050
HOP = SR // FPS  # ~one analysis frame per video frame (918.75 -> 918)
OUT = Path(__file__).with_name("analysis.json")


def smooth(x, n):
    if n <= 1:
        return x
    k = np.hanning(n * 2 + 1)
    k /= k.sum()
    return np.convolve(np.pad(x, n, mode="edge"), k, mode="valid")


def norm(x):
    lo, hi = np.percentile(x, 2), np.percentile(x, 99)
    return np.clip((x - lo) / (hi - lo + 1e-9), 0, 1)


def to_fps(curve, sr, hop, n_frames):
    t_src = librosa.frames_to_time(np.arange(len(curve)), sr=sr, hop_length=hop)
    return np.interp(np.arange(n_frames) / FPS, t_src, curve)


def main(song, accomp=None):
    y, sr = librosa.load(song, sr=SR, mono=True)
    dur = len(y) / sr
    n_frames = int(np.ceil(dur * FPS))

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=512, units="time")
    tempo = float(np.atleast_1d(tempo)[0])
    onset = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)

    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    energy = norm(smooth(librosa.amplitude_to_db(rms, ref=np.max), 40))  # ~1s window

    # Low end (bass + kick) tells us when the band comes in.
    S = np.abs(librosa.stft(y, hop_length=512))
    freqs = librosa.fft_frequencies(sr=sr)
    low = S[freqs < 150].sum(0)
    low = norm(smooth(librosa.amplitude_to_db(low, ref=np.max), 40))

    # Percussive onsets from the accompaniment stem (drums), if we have it.
    drums = None
    if accomp:
        ya, _ = librosa.load(accomp, sr=SR, mono=True)
        _, yp = librosa.effects.hpss(ya)
        drums = librosa.onset.onset_strength(y=yp, sr=sr, hop_length=512)
        drums = norm(smooth(drums, 3))

    # Section boundaries: agglomerative clustering of beat-synced chroma + MFCC.
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=512)
    bframes = librosa.time_to_frames(beats, sr=sr, hop_length=512)
    feat = np.vstack([librosa.util.normalize(chroma), librosa.util.normalize(mfcc)])
    sync = librosa.util.sync(feat, bframes, aggregate=np.median)
    k = 12
    bnd = librosa.segment.agglomerative(sync, k)
    bnd_beats = np.concatenate([[0.0], beats])
    boundaries = sorted({round(float(bnd_beats[min(b, len(bnd_beats) - 1)]), 2) for b in bnd})

    out = {
        "duration": round(dur, 3),
        "fps": FPS,
        "tempo": round(tempo, 2),
        "beats": [round(float(b), 3) for b in beats],
        "boundaries": boundaries,
        "energy": [round(float(v), 3) for v in to_fps(energy, sr, 512, n_frames)],
        "low": [round(float(v), 3) for v in to_fps(low, sr, 512, n_frames)],
        "onset": [round(float(v), 3) for v in to_fps(norm(onset), sr, 512, n_frames)],
    }
    if drums is not None:
        out["drums"] = [round(float(v), 3) for v in to_fps(drums, sr, 512, n_frames)]
    OUT.write_text(json.dumps(out))

    print(f"duration {dur:.1f}s  tempo {tempo:.1f} BPM  beats {len(beats)}")
    print("boundaries:", ", ".join(f"{b:.1f}" for b in boundaries))
    print("energy / low-end per 5 s:")
    for t in range(0, int(dur), 5):
        i = t * FPS
        e, l = out["energy"][i], out["low"][i]
        print(f"  {t//60}:{t%60:02d}  E {'#' * int(e * 30):<30} {e:.2f}  low {l:.2f}")


if __name__ == "__main__":
    main(*sys.argv[1:])
