"""Word-level forced alignment of lyrics.txt to the isolated vocal stem.

    python3 videos/cara-pulang-yang-benar/align.py <vocals.wav>

Uses torchaudio's MMS_FA (multilingual wav2vec2 CTC aligner). The lyrics are
aligned as given (no transcription). A <star> token sits between lines so
ad-libs and breaths outside the lyrics have somewhere to go. Writes
alignment.json and prints per-line confidence (mean CTC posterior of the
aligned characters).
"""
import json
import re
import sys
from pathlib import Path

import soundfile as sf
import torch
import torchaudio
import torchaudio.functional as F
from torchaudio.pipelines import MMS_FA as BUNDLE

HERE = Path(__file__).parent
LYRICS = HERE / "lyrics.txt"
OUT = HERE / "alignment.json"

# Who sings each section. The Suno tags name Voice 1 / Voice 2 / both; untagged
# sections follow the story (V1 is the child, V2 the parent).
VOICE = {
    "Verse 1": "v1", "Pre-Chorus": "v1", "Chorus": "v1",
    "Verse 2": "v2", "Pre-Chorus 2": "both", "Chorus 2": "both",
    "Bridge": "v1", "Final Chorus": "both",
}


def parse(path):
    """-> list of sections {name, tag, voice, lines:[str]} (instrumental ones have no lines)."""
    sections, seen = [], {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        m = re.match(r"\[([^\]:]+)(?::\s*(.*))?\]", raw)
        if m:
            name = m.group(1).strip()
            seen[name] = seen.get(name, 0) + 1
            key = name if seen[name] == 1 else f"{name} {seen[name]}"
            sections.append({"name": name, "key": key, "tag": (m.group(2) or "").strip(),
                             "voice": VOICE.get(key, "v1"), "lines": []})
        elif raw:
            sections[-1]["lines"].append(raw)
    return sections


def norm_word(w):
    return re.sub(r"[^a-z']", "", w.lower())


def emissions(wav, model, sr):
    """Run the CTC model in 30 s chunks with 2 s context on each side."""
    chunk, ctx = 30 * sr, 2 * sr
    out = []
    with torch.inference_mode():
        for s in range(0, wav.shape[1], chunk):
            a, b = max(0, s - ctx), min(wav.shape[1], s + chunk + ctx)
            em, _ = model(wav[:, a:b])
            ratio = em.shape[1] / (b - a)
            lo = round((s - a) * ratio)
            hi = lo + round((min(s + chunk, wav.shape[1]) - s) * ratio)
            out.append(em[:, lo:hi])
    return torch.cat(out, 1)


def main(vocals):
    sections = parse(LYRICS)
    data, sr = sf.read(vocals, dtype="float32", always_2d=True)
    wav = torch.from_numpy(data.T.copy())
    wav = torchaudio.functional.resample(wav.mean(0, keepdim=True), sr, BUNDLE.sample_rate)
    wav = wav / wav.abs().max()
    model = BUNDLE.get_model(with_star=True)
    tokenizer, aligner = BUNDLE.get_tokenizer(), BUNDLE.get_aligner()
    rate = BUNDLE.sample_rate

    def align(words, emission, offset, spf):
        """-> [(start, end, score)] for each non-star word."""
        spans = aligner(emission[0], tokenizer(words))
        out = []
        for w, ws in zip(words, spans):
            if w != "*":
                n = sum(len(s) for s in ws)
                out.append((offset + ws[0].start * spf, offset + ws[-1].end * spf,
                            sum(s.score * len(s) for s in ws) / n))
        return out

    out_sections = []
    for sec in sections:
        out_sections.append({k: sec[k] for k in ("name", "key", "tag", "voice")} | {
            "lines": [{"text": line, "words": [{"text": w} for w in line.split()]}
                      for line in sec["lines"]]})
    lines = [line for sec in out_sections for line in sec["lines"]]

    def tokens_of(line):
        idx = [i for i, w in enumerate(line["words"]) if norm_word(w["text"])]
        return idx, [norm_word(line["words"][i]["text"]) for i in idx]

    def store(line, idx, res):
        for i, (a, b, sc) in zip(idx, res):
            line["words"][i].update(start=round(a, 3), end=round(b, 3), score=round(sc, 3))

    # Pass 1: the whole song at once, a star between lines.
    emission = emissions(wav, model, rate)
    spf = wav.shape[1] / rate / emission.shape[1]
    words, owners = [], []
    for li, line in enumerate(lines):
        idx, toks = tokens_of(line)
        words += ["*"] + toks
        owners += [li] * len(toks)
    res = align(words + ["*"], emission, 0.0, spf)
    for li, line in enumerate(lines):
        idx, _ = tokens_of(line)
        store(line, idx, [r for r, o in zip(res, owners) if o == li])

    # Pass 2: realign each pair of neighbouring lines on its own audio window; keep
    # it if the pair scores better. The global pass can drag a boundary across a
    # long held note (bridge -> final chorus); a two-line window lets it move.
    def mean(group):
        sc = [line["words"][i]["score"] for line in group for i in tokens_of(line)[0]]
        return sum(sc) / len(sc)
    for li in range(len(lines) - 1):
        group = lines[li:li + 2]
        words, owners = ["*"], []
        for gi, line in enumerate(group):
            toks = tokens_of(line)[1]
            words += toks + ["*"]
            owners += [gi] * len(toks)
        first, last = group[0]["words"][0], group[-1]["words"][-1]
        a = lines[li - 1]["words"][-1]["end"] - 0.2 if li else first["start"] - 3
        b = lines[li + 2]["words"][0]["start"] + 0.2 if li + 2 < len(lines) else last["end"] + 3
        a, b = max(0.0, min(a, first["start"] - 0.5)), max(b, last["end"] + 0.5)
        seg = wav[:, int(a * rate):int(b * rate)]
        with torch.inference_mode():
            em, _ = model(seg / seg.abs().max())
        local = align(words, em, a, (b - a) / em.shape[1])
        before = mean(group)
        if sum(r[2] for r in local) / len(local) > before + 0.01:
            for gi, line in enumerate(group):
                line.setdefault("refined_from", round(sum(
                    line["words"][i]["score"] for i in tokens_of(line)[0]) / len(tokens_of(line)[0]), 3))
                store(line, tokens_of(line)[0], [r for r, o in zip(local, owners) if o == gi])

    # Punctuation-only tokens (e.g. a lone "...") borrow their neighbour's time.
    for sec in out_sections:
        for line in sec["lines"]:
            ws = line["words"]
            for i, w in enumerate(ws):
                if "start" not in w:
                    prev = ws[i - 1] if i else ws[i + 1]
                    w.update(start=prev["end"], end=prev["end"], score=prev.get("score", 1))
            line["start"], line["end"] = ws[0]["start"], ws[-1]["end"]
            scored = [w["score"] for w in ws]
            line["score"] = round(sum(scored) / len(scored), 3)
            line["min_word"] = min(ws, key=lambda w: w["score"])["text"]
            line["min_score"] = min(scored)

    OUT.write_text(json.dumps({"sections": out_sections}, ensure_ascii=False, indent=1))
    report(out_sections)


def report(sections):
    def ts(t):
        return f"{int(t // 60)}:{t % 60:05.2f}"
    for sec in sections:
        if not sec["lines"]:
            continue
        print(f"\n[{sec['key']}]  voice={sec['voice']}")
        for line in sec["lines"]:
            flag = "  <-- check" if line["score"] < 0.5 or line["min_score"] < 0.2 else ""
            if "refined_from" in line:
                flag += f"  (local pass, was {line['refined_from']:.2f})"
            print(f"  {ts(line['start'])}-{ts(line['end'])}  conf {line['score']:.2f}"
                  f"  (low: {line['min_word']} {line['min_score']:.2f})  {line['text']}{flag}")


if __name__ == "__main__":
    main(sys.argv[1])
