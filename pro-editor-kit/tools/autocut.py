#!/usr/bin/env python3
"""autocut — word-level transcript -> tight talking-head cut (silences, fillers, retakes).

Why: in the reference Opus 5.5 reel tutorial (YouTube 5UnK3c-nlIs) the model spent
24 minutes cutting a 1-minute clip. This deterministic pass does the same job in
milliseconds so the model spends its tokens on design, not on arithmetic.

Usage:
  python3 autocut.py words.json --fps 30 --out cut/            # plan only
  python3 autocut.py words.json --fps 30 --out cut/ --source raw.mp4 --render

Outputs (in --out): cut-plan.json, words.retimed.json, ffmpeg-filter.txt, render.sh
All times are seconds; frame fields are integers at --fps. Never overwrites the source.
"""
from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FILLERS, dump_json, frames, load_words, need, norm, run  # noqa: E402


def mark_fillers(words: list[dict], extra: set[str]) -> None:
    bag = FILLERS | extra
    for w in words:
        if norm(w["word"]) in bag:
            w["drop"] = "filler"


def mark_stutters(words: list[dict], max_n: int = 4, gap: float = 0.6) -> None:
    """Drop the first copy of an immediately repeated 2..max_n word sequence
    ("I think I think we" -> "I think we"). Single-word doubles are kept
    because they are often intentional ("very very"). Repeats separated by a
    pause longer than `gap` are left for mark_retakes (a deliberate re-take)."""
    toks = [norm(w["word"]) for w in words]
    i = 0
    while i < len(words):
        hit = False
        for n in range(max_n, 1, -1):
            a, b = toks[i:i + n], toks[i + n:i + 2 * n]
            if (len(b) == n and a == b and all(a) and not any(words[k].get("drop") for k in range(i, i + n))
                    and words[i + n]["start"] - words[i + n - 1]["end"] <= gap):
                for k in range(i, i + n):
                    words[k]["drop"] = "stutter"
                i += n
                hit = True
                break
        if not hit:
            i += 1


def phrases(words: list[dict], gap: float) -> list[list[int]]:
    out, cur = [], []
    for idx, w in enumerate(words):
        if w.get("drop"):
            continue
        if cur:
            prev = words[cur[-1]]
            if w["start"] - prev["end"] > gap or prev["word"].rstrip().endswith((".", "?", "!")):
                out.append(cur)
                cur = []
        cur.append(idx)
    if cur:
        out.append(cur)
    return out


def mark_retakes(words: list[dict], gap: float, prefix: int, lookahead: int) -> None:
    """A phrase is a failed take when one of the next `lookahead` phrases starts
    with the same first `prefix` normalised words. Keep the LAST attempt."""
    ph = phrases(words, gap)
    for i, p in enumerate(ph):
        head = [norm(words[k]["word"]) for k in p[:prefix]]
        if len(head) < prefix:
            continue
        for q in ph[i + 1:i + 1 + lookahead]:
            if [norm(words[k]["word"]) for k in q[:prefix]] == head:
                for k in p:
                    words[k]["drop"] = "retake"
                break


def keep_ranges(words, min_silence, pad_in, pad_out, duration):
    kept = [w for w in words if not w.get("drop")]
    ranges = []
    for w in kept:
        if ranges and w["start"] - ranges[-1][1] <= min_silence:
            ranges[-1][1] = w["end"]
        else:
            ranges.append([w["start"], w["end"]])
    padded = []
    for s, e in ranges:
        s, e = max(0.0, s - pad_in), e + pad_out
        if duration:
            e = min(e, duration)
        if padded and s <= padded[-1][1]:
            padded[-1][1] = max(padded[-1][1], e)
        else:
            padded.append([s, e])
    return padded


def build(words, fps, min_silence=0.35, pad_in=0.06, pad_out=0.10, retake_gap=0.6,
          retake_prefix=3, lookahead=2, extra_fillers=(), duration=None, punch=(1.0, 1.12)):
    words = [dict(w) for w in words]
    mark_fillers(words, {norm(f) for f in extra_fillers})
    mark_stutters(words, gap=retake_gap)
    mark_retakes(words, retake_gap, retake_prefix, lookahead)
    ranges = keep_ranges(words, min_silence, pad_in, pad_out, duration)
    keep, t_out = [], 0.0
    for i, (s, e) in enumerate(ranges):
        fs, fe = frames(s, fps, "floor"), frames(e, fps, "ceil")
        s, e = fs / fps, fe / fps
        keep.append({"index": i, "start": round(s, 6), "end": round(e, 6), "start_frame": fs, "end_frame": fe,
                     "out_start": round(t_out, 6), "zoom": punch[i % len(punch)]})
        t_out += e - s
    retimed = []
    for w in words:
        if w.get("drop"):
            continue
        for k in keep:
            if k["start"] - 1e-6 <= w["start"] and w["end"] <= k["end"] + 1e-6:
                off = k["out_start"] - k["start"]
                retimed.append({"word": w["word"], "start": round(w["start"] + off, 4), "end": round(w["end"] + off, 4)})
                break
    removed = [{"word": w["word"], "start": w["start"], "end": w["end"], "reason": w["drop"]} for w in words if w.get("drop")]
    src = duration or (words[-1]["end"] if words else 0.0)
    stats = {"source_seconds": round(src, 3), "output_seconds": round(t_out, 3),
             "removed_seconds": round(src - t_out, 3), "segments": len(keep),
             "dropped_words": {r: sum(1 for x in removed if x["reason"] == r) for r in ("filler", "stutter", "retake")}}
    return {"fps": fps, "params": {"min_silence": min_silence, "pad_in": pad_in, "pad_out": pad_out,
            "retake_gap": retake_gap, "retake_prefix": retake_prefix, "lookahead": lookahead},
            "keep": keep, "removed_words": removed, "stats": stats}, retimed


def ffmpeg_filter(keep: list[dict], audio: bool = True) -> str:
    parts, labels = [], []
    for k in keep:
        i = k["index"]
        parts.append(f"[0:v]trim=start={k['start']}:end={k['end']},setpts=PTS-STARTPTS[v{i}]")
        if audio:
            # 8 ms fades at every seam stop clicks without audible dips.
            fade_out = max(k["end"] - k["start"] - 0.008, 0)
            parts.append(f"[0:a]atrim=start={k['start']}:end={k['end']},asetpts=PTS-STARTPTS,"
                         f"afade=t=in:d=0.008,afade=t=out:st={fade_out:.4f}:d=0.008[a{i}]")
            labels.append(f"[v{i}][a{i}]")
        else:
            labels.append(f"[v{i}]")
    n = len(keep)
    parts.append("".join(labels) + f"concat=n={n}:v=1:a={1 if audio else 0}" + ("[outv][outa]" if audio else "[outv]"))
    return ";\n".join(parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words", help="word-level transcript JSON (Whisper, WhisperX, Deepgram, ElevenLabs, Remotion Caption[])")
    ap.add_argument("--fps", type=float, required=True)
    ap.add_argument("--out", default="cut")
    ap.add_argument("--min-silence", type=float, default=0.35, help="gaps longer than this are removed (s)")
    ap.add_argument("--pad-in", type=float, default=0.06)
    ap.add_argument("--pad-out", type=float, default=0.10)
    ap.add_argument("--retake-prefix", type=int, default=3)
    ap.add_argument("--lookahead", type=int, default=2)
    ap.add_argument("--filler", action="append", default=[], help="extra filler token (repeatable)")
    ap.add_argument("--source", help="source media for render.sh / --render")
    ap.add_argument("--duration", type=float, help="source duration (s); probed from --source when omitted")
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--render", action="store_true", help="run ffmpeg now (needs --source)")
    a = ap.parse_args(argv)

    duration = a.duration
    if a.source and duration is None:
        need("ffprobe")
        r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.source])
        duration = float(r.stdout.strip())
    plan, retimed = build(load_words(a.words), a.fps, a.min_silence, a.pad_in, a.pad_out,
                          retake_prefix=a.retake_prefix, lookahead=a.lookahead, extra_fillers=a.filler, duration=duration)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    plan["source"] = a.source
    dump_json(plan, out / "cut-plan.json")
    dump_json(retimed, out / "words.retimed.json")
    filt = ffmpeg_filter(plan["keep"], audio=not a.no_audio)
    (out / "ffmpeg-filter.txt").write_text(filt + "\n", encoding="utf-8")
    src = a.source or "INPUT.mp4"
    maps = ["-map", "[outv]"] + ([] if a.no_audio else ["-map", "[outa]"])
    cmd = ["ffmpeg", "-y", "-i", src, "-filter_complex_script", str(out / "ffmpeg-filter.txt"), *maps,
           "-r", str(a.fps), "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(out / "cut.mp4")]
    (out / "render.sh").write_text("#!/bin/sh\nset -e\n" + shlex.join(cmd) + "\n", encoding="utf-8")
    s = plan["stats"]
    print(f"autocut: {s['source_seconds']}s -> {s['output_seconds']}s in {s['segments']} segments; "
          f"dropped {s['dropped_words']}; wrote {out}/cut-plan.json")
    if a.render:
        if not a.source:
            ap.error("--render needs --source")
        need("ffmpeg")
        r = run(cmd, check=False)
        if r.returncode:
            sys.stderr.write(r.stderr[-4000:])
            return r.returncode
        print(f"autocut: rendered {out}/cut.mp4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
