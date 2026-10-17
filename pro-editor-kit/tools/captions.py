#!/usr/bin/env python3
"""captions — word timings -> paged, readable, emphasis-tagged captions.

Implements the caption rules shared by the reference edits: 1-4 words per page
for short-form, one emphasised keyword per page in the accent colour, no orphan
single-word pages, reading speed capped, pages split on pauses and punctuation.

Usage:
  python3 captions.py words.retimed.json --fps 30 --preset reel --out captions/
  python3 captions.py words.json --fps 30 --preset youtube --keywords keywords.txt --out captions/

Outputs: captions.srt, captions.vtt, captions.pages.json (frames + per-word emphasis),
captions.remotion.json (@remotion/captions Caption[] for createTikTokStyleCaptions).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import dump_json, frames, load_words, norm, tc  # noqa: E402

PRESETS = {
    # max_words, max_chars (per page), max_cps, min_page_s, split_gap_s
    "reel": dict(max_words=4, max_chars=22, max_cps=20.0, min_page=0.35, split_gap=0.25),
    "youtube": dict(max_words=8, max_chars=42, max_cps=17.0, min_page=0.8, split_gap=0.45),
    "broadcast": dict(max_words=12, max_chars=37 * 2, max_cps=15.0, min_page=1.0, split_gap=0.6),
}
STOP = set("""a an the and or but if then so to of in on at by for with from as is are was were be been being it its
this that these those i you he she we they me him her us them my your our their do does did not no yes just very
really there here what which who whom when where why how all any some can could would should will shall may might
must have has had about into over than too also only up down out off again more most such own same both each few
""".split())
_NUM = re.compile(r"\d")


def score(word: str) -> float:
    n = norm(word)
    if not n or n in STOP:
        return 0.0
    s = len(n)
    if _NUM.search(word) or "$" in word or "%" in word:
        s += 10  # numbers and money almost always deserve the accent
    if word[:1].isupper():
        s += 2
    return s


def paginate(words, max_words, max_chars, max_cps, min_page, split_gap):
    pages, cur = [], []

    def flush():
        if cur:
            pages.append(list(cur))
            cur.clear()

    for w in words:
        if cur:
            gap = w["start"] - cur[-1]["end"]
            text_len = len(" ".join(x["word"] for x in cur + [w]))
            ends_sentence = cur[-1]["word"].endswith((".", "?", "!", ":", ";"))
            soft_break = cur[-1]["word"].endswith(",") and len(cur) >= 2
            if len(cur) >= max_words or text_len > max_chars or gap > split_gap or ends_sentence or soft_break:
                flush()
        cur.append(w)
    flush()
    # Merge orphan single-word pages into a neighbour when it fits and is not isolated by a pause.
    merged = []
    for p in pages:
        if (len(p) == 1 and merged and len(merged[-1]) < max_words + 1
                and p[0]["start"] - merged[-1][-1]["end"] <= split_gap
                and len(" ".join(x["word"] for x in merged[-1] + p)) <= max_chars + 6):
            merged[-1].extend(p)
        elif (len(p) == 1 and merged and len(merged[-1]) >= 3
              and p[0]["start"] - merged[-1][-1]["end"] <= split_gap):
            # Rebalance instead: steal the previous page's last word ("Make every / element 25% smaller.").
            merged.append([merged[-1].pop()] + p)
        else:
            merged.append(p)
    return merged


def build(words, fps, preset="reel", keywords=None, accent_per_page=1, **over):
    cfg = dict(PRESETS[preset])
    cfg.update({k: v for k, v in over.items() if v is not None})
    kw = {norm(k) for k in (keywords or [])}
    pages = paginate(words, cfg["max_words"], cfg["max_chars"], cfg["max_cps"], cfg["min_page"], cfg["split_gap"])
    out, warnings = [], []
    for i, p in enumerate(pages):
        start = p[0]["start"]
        nxt = pages[i + 1][0]["start"] if i + 1 < len(pages) else p[-1]["end"] + 0.4
        # Hold the page a beat after the last word, at least min_page, never past the next page.
        end = max(p[-1]["end"] + 0.12, start + cfg["min_page"])
        if i + 1 < len(pages):
            end = min(end, nxt)
        text = " ".join(w["word"] for w in p)
        dur = max(end - start, 1e-3)
        cps = len(text) / dur
        if cps > cfg["max_cps"]:
            warnings.append(f"page {i}: {cps:.1f} chars/s exceeds {cfg['max_cps']} ('{text}') - consider slowing or trimming copy")
        ranked = sorted(range(len(p)), key=lambda k: (norm(p[k]["word"]) in kw, score(p[k]["word"])), reverse=True)
        emph = {k for k in ranked[:accent_per_page] if norm(p[k]["word"]) in kw or score(p[k]["word"]) > 0}
        out.append({"index": i, "start": round(start, 3), "end": round(end, 3),
                    "startFrame": frames(start, fps), "endFrame": max(frames(end, fps), frames(start, fps) + 1),
                    "text": text, "cps": round(cps, 1),
                    "words": [{"text": w["word"], "start": w["start"], "end": w["end"],
                               "startFrame": frames(w["start"], fps), "emphasis": k in emph} for k, w in enumerate(p)]})
    return out, warnings


def to_srt(pages):
    return "\n".join(f"{p['index'] + 1}\n{tc(p['start'])} --> {tc(p['end'])}\n{p['text']}\n" for p in pages)


def to_vtt(pages):
    return "WEBVTT\n\n" + "\n".join(f"{tc(p['start'], '.')} --> {tc(p['end'], '.')}\n{p['text']}\n" for p in pages)


def to_remotion(words):
    # Leading space on all but the first token is what createTikTokStyleCaptions expects.
    return [{"text": (" " if i else "") + w["word"], "startMs": round(w["start"] * 1000), "endMs": round(w["end"] * 1000),
             "timestampMs": round((w["start"] + w["end"]) * 500), "confidence": None} for i, w in enumerate(words)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words")
    ap.add_argument("--fps", type=float, required=True)
    ap.add_argument("--preset", choices=sorted(PRESETS), default="reel")
    ap.add_argument("--keywords", help="text file, one keyword per line, forced to accent")
    ap.add_argument("--max-words", type=int)
    ap.add_argument("--max-chars", type=int)
    ap.add_argument("--out", default="captions")
    a = ap.parse_args(argv)
    words = load_words(a.words)
    kws = Path(a.keywords).read_text(encoding="utf-8").split() if a.keywords else []
    pages, warnings = build(words, a.fps, a.preset, kws, max_words=a.max_words, max_chars=a.max_chars)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "captions.srt").write_text(to_srt(pages), encoding="utf-8")
    (out / "captions.vtt").write_text(to_vtt(pages), encoding="utf-8")
    dump_json({"fps": a.fps, "preset": a.preset, "pages": pages, "warnings": warnings}, out / "captions.pages.json")
    dump_json(to_remotion(words), out / "captions.remotion.json")
    for w in warnings:
        print("warn:", w, file=sys.stderr)
    print(f"captions: {len(pages)} pages ({a.preset}) -> {out}/captions.srt|.vtt|.pages.json|.remotion.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
