#!/usr/bin/env python3
"""Synthesize a calm lo-fi music bed (soft keys, sub bass, brushed beat, vinyl crackle).

  python3 tools/lofi_bed.py OUT.mp3 --seconds 22.4 [--bpm 80] [--seed 3] [--style lofi|explainer]

"explainer" drops the kick and snare for a plucked 8th-note arpeggio (Vox-style edits).

For the archive theme, which runs on text + music only. Licence-free (made here), so it is a
stand-in until a real track is supplied: swap assets/music.mp3 for any royalty-free song.
Chord changes land on bar lines: bar = 4 beats = 240/bpm seconds.
"""
import argparse
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 44100
# Fmaj7 Em7 Dm7 Cmaj7 (MIDI notes), one chord per bar
CHORDS = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, attack, decay):
    t = np.arange(n) / SR
    return np.minimum(t / attack, 1.0) * np.exp(-t / decay)


def key(m, n, rng):
    """Electric-piano-ish note: sine + fast-fading bright partials, slightly detuned."""
    t = np.arange(n) / SR
    f = hz(m) * (1 + rng.uniform(-0.0015, 0.0015))
    tone = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t / 0.25)
            + 0.12 * np.sin(6 * np.pi * f * t) * np.exp(-t / 0.12))
    return tone * env(n, 0.012, 1.6) * (1 + 0.08 * np.sin(2 * np.pi * 4.5 * t))


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):  # one-pole; fine for a few seconds of audio
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def mix(out, start, x):
    """Add x into out from sample `start`, clipped at the end."""
    x = x[:max(len(out) - start, 0)]
    out[start:start + len(x)] += x


def build(seconds, bpm, seed, style="lofi"):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    out = np.zeros(n + SR * 3)
    beat = 60 / bpm
    bar = 4 * beat
    for b in range(int(seconds / bar) + 2):
        t0 = b * bar
        chord = CHORDS[b % len(CHORDS)]
        for j, m in enumerate(chord):  # gently rolled chord on beat 1, a softer echo on the "and" of 3
            for at, vel in ((t0 + j * 0.03, 0.16), (t0 + 2.5 * beat + j * 0.02, 0.07)):
                s = int(at * SR)
                note = key(m + 12, int(bar * SR), rng) * vel
                mix(out, s, note)
        s = int(t0 * SR)  # sub bass: root, held for the bar
        tb = np.arange(int(bar * SR)) / SR
        bass = np.sin(2 * np.pi * hz(chord[0] - 12) * tb) * env(len(tb), 0.02, 2.2) * 0.22
        mix(out, s, bass)
        if style == "explainer":  # plucked arpeggio through the chord on 8ths
            for k in range(8):
                s = int((t0 + k * beat / 2) * SR)
                m = chord[(k * 3) % len(chord)] + 24
                pluck = key(m, int(0.6 * SR), rng) * env(int(0.6 * SR), 0.004, 0.16) * (0.11 if k % 2 == 0 else 0.07)
                mix(out, s, pluck)
        for k in range(4):  # soft kick on 1 and 3, brushed snare on 2 and 4, quiet hats on 8ths
            s = int((t0 + k * beat) * SR)
            tk = np.arange(int(0.35 * SR)) / SR
            if style == "explainer":
                hit = np.zeros(1)
            elif k % 2 == 0:
                hit = np.sin(2 * np.pi * (50 + 70 * np.exp(-tk / 0.03)) * tk) * np.exp(-tk / 0.12) * 0.35
            else:
                hit = rng.normal(0, 1, len(tk)) * np.exp(-tk / 0.07) * 0.05
            mix(out, s, hit)
            for h in (0, 0.5):
                s = int((t0 + (k + h) * beat) * SR)
                th = np.arange(int(0.05 * SR)) / SR
                hat = np.diff(rng.normal(0, 1, len(th) + 1)) * np.exp(-th / 0.012) * 0.018
                mix(out, s, hat)
    out = out[:n]
    out = lowpass(out, 3800)
    crackle = (rng.random(n) < 0.0009) * rng.normal(0, 0.12, n) + rng.normal(0, 0.003, n)
    out += lowpass(crackle, 5000)
    fade_in, fade_out = int(0.25 * SR), int(1.5 * SR)
    out[:fade_in] *= np.linspace(0, 1, fade_in)
    out[-fade_out:] *= np.linspace(1, 0, fade_out)
    return out / (np.abs(out).max() + 1e-9) * 0.7


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float, required=True)
    ap.add_argument("--bpm", type=float, default=80)
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--style", choices=("lofi", "explainer"), default="lofi")
    args = ap.parse_args()
    pcm = (build(args.seconds, args.bpm, args.seed, args.style) * 32767).astype(np.int16)
    with tempfile.TemporaryDirectory() as tmp:
        wav_path = Path(tmp) / "bed.wav"
        with wave.open(str(wav_path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path), "-ac", "2", "-b:a", "192k", args.out],
                       check=True)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
