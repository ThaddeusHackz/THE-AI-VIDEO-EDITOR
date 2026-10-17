#!/usr/bin/env python3
"""sfx_map — scene plan events -> sound-design placements + an ffmpeg mix command.

Encodes the sound-design training from the reference Opus 5.5 reel (YouTube
5UnK3c-nlIs): sound follows MOTION; three families (whooshes for movement,
textures = clicks/pops/UI for things appearing, risers+hits to build and drop
anticipation); music bed around -20 dB under the voice.

Usage:
  python3 sfx_map.py scene-plan.json --library sfx-library.json --out sfx/
  python3 sfx_map.py scene-plan.json --library sfx-library.json --voice cut.mp4 --music bed.mp3 --out sfx/ --render

scene-plan.json events: [{"t": 3.2, "type": "transition|text_in|ui|zoom|reveal|impact|chapter", "intensity": 1-3}]
sfx-library.json: {"whoosh": [{"file": "...", "peak": 0.18, "dur": 0.6}], "pop": [...], "ui_click": [...],
                   "riser": [{"file": "...", "dur": 2.0}], "hit": [...], "click": [...]}
"""
from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import dump_json, load_json, need, run  # noqa: E402

# event type -> (role, gain dB relative to voice, family)
ROUTE = {
    "transition": ("whoosh", -12, "movement"),
    "zoom": ("whoosh", -16, "movement"),
    "text_in": ("pop", -18, "texture"),
    "ui": ("ui_click", -18, "texture"),
    "chapter": ("click", -16, "texture"),
    "impact": ("hit", -10, "anticipation"),
    "reveal": ("riser", -14, "anticipation"),
}
MIN_GAP = {"movement": 0.30, "texture": 0.12, "anticipation": 1.5}
MAX_PER_SECOND = 3


def place(events, library, rotate=True):
    placements, last, used, dropped = [], {}, {}, []
    window = []
    for ev in sorted(events, key=lambda e: e["t"]):
        role, gain, fam = ROUTE.get(ev["type"], (None, 0, None))
        if not role or not library.get(role):
            dropped.append({**ev, "why": f"no route/library for '{ev['type']}'"})
            continue
        if ev["t"] - last.get(fam, -99) < MIN_GAP[fam]:
            dropped.append({**ev, "why": f"{fam} sounds closer than {MIN_GAP[fam]}s (stacking smears)"})
            continue
        window = [t for t in window if ev["t"] - t < 1.0]
        if len(window) >= MAX_PER_SECOND:
            dropped.append({**ev, "why": f"more than {MAX_PER_SECOND} sfx in 1s (less is more)"})
            continue
        bank = library[role]
        idx = used.get(role, 0) % len(bank) if rotate else 0
        used[role] = used.get(role, 0) + 1
        s = bank[idx]
        if role == "riser":
            start = ev["t"] - float(s.get("dur", 2.0))  # riser ENDS on the reveal
        elif role == "whoosh":
            start = ev["t"] - float(s.get("peak", 0.15))  # whoosh PEAKS on the cut
        else:
            start = ev["t"]  # textures land on the frame the visual starts
        gain_adj = gain + 3 * (int(ev.get("intensity", 2)) - 2)
        placements.append({"t": ev["t"], "start": round(max(0.0, start), 3), "role": role, "family": fam,
                           "file": s["file"], "gain_db": gain_adj, "event": ev["type"]})
        last[fam] = ev["t"]
        window.append(ev["t"])
    return placements, dropped


def mix_command(placements, voice, music, out, music_db=-20.0, duck=True):
    inputs = ["-i", voice] + (["-i", music] if music else [])
    base = 2 if music else 1
    filters, labels = [], []
    for i, p in enumerate(placements):
        inputs += ["-i", p["file"]]
        ms = int(round(p["start"] * 1000))
        filters.append(f"[{base + i}:a]adelay={ms}|{ms},volume={p['gain_db']}dB[s{i}]")
        labels.append(f"[s{i}]")
    if music:
        if duck:
            filters.append("[0:a]asplit=2[vo][vkey]")
            filters.append(f"[1:a]volume={music_db}dB[mbed]")
            filters.append("[mbed][vkey]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[mduck]")
            mus = "[mduck]"
        else:
            filters.append(f"[1:a]volume={music_db}dB[mduck]")
            filters.append("[0:a]anull[vo]")
            mus = "[mduck]"
        chain = "[vo]" + mus + "".join(labels)
        n = 2 + len(labels)
    else:
        filters.append("[0:a]anull[vo]")
        chain = "[vo]" + "".join(labels)
        n = 1 + len(labels)
    filters.append(f"{chain}amix=inputs={n}:duration=first:normalize=0,alimiter=limit=0.89[mix]")
    fc = ";".join(filters)
    return ["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", "0:v?", "-map", "[mix]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", out]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan", help="scene-plan JSON with an 'events' array")
    ap.add_argument("--library", required=True)
    ap.add_argument("--voice", help="video/audio carrying the voice track (input 0)")
    ap.add_argument("--music", help="music bed")
    ap.add_argument("--music-db", type=float, default=-20.0)
    ap.add_argument("--no-duck", action="store_true")
    ap.add_argument("--out", default="sfx")
    ap.add_argument("--render", action="store_true")
    a = ap.parse_args(argv)
    plan = load_json(a.plan)
    events = plan["events"] if isinstance(plan, dict) else plan
    placements, dropped = place(events, load_json(a.library))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    dump_json({"placements": placements, "dropped": dropped}, out / "sfx-placements.json")
    print(f"sfx_map: {len(placements)} placed, {len(dropped)} dropped -> {out}/sfx-placements.json")
    if a.voice:
        cmd = mix_command(placements, a.voice, a.music, str(out / "mixed.mp4"), a.music_db, not a.no_duck)
        (out / "mix.sh").write_text("#!/bin/sh\nset -e\n" + shlex.join(cmd) + "\n", encoding="utf-8")
        if a.render:
            need("ffmpeg")
            r = run(cmd, check=False)
            if r.returncode:
                sys.stderr.write(r.stderr[-4000:])
                return r.returncode
            print(f"sfx_map: mixed -> {out}/mixed.mp4 (run render_qa.py on it for LUFS/true-peak)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
