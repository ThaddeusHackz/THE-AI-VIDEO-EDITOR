#!/usr/bin/env python3
"""beat_grid — snap cuts and motion events to the music grid.

Usage:
  python3 beat_grid.py --bpm 120 --offset 0.12 --events events.json --tolerance 0.12 --out snapped.json
  python3 beat_grid.py --bpm 96 --duration 30 --every 2 --fps 30      # list cut points every 2 beats

Snaps to the nearest beat or half-beat (--subdivision 2) when within tolerance;
otherwise leaves the event where speech put it (words beat music).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import dump_json, frames, load_json  # noqa: E402


def grid(bpm, offset, duration, subdivision=1):
    step = 60.0 / bpm / subdivision
    t, out = offset, []
    while t <= duration + 1e-9:
        out.append(round(t, 6))
        t += step
    return out


def snap(times, bpm, offset, tolerance, subdivision=2):
    step = 60.0 / bpm / subdivision
    res = []
    for t in times:
        k = round((t - offset) / step)
        g = offset + k * step
        res.append({"t": t, "snapped": round(g, 6) if abs(g - t) <= tolerance else t, "moved": abs(g - t) <= tolerance})
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bpm", type=float, required=True)
    ap.add_argument("--offset", type=float, default=0.0, help="time of the first downbeat (s)")
    ap.add_argument("--events", help="JSON list of times or of objects with 't'")
    ap.add_argument("--tolerance", type=float, default=0.12)
    ap.add_argument("--subdivision", type=int, default=2)
    ap.add_argument("--duration", type=float)
    ap.add_argument("--every", type=int, default=0, help="emit a cut point every N beats")
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    result = {}
    if a.events:
        ev = load_json(a.events)
        times = [e["t"] if isinstance(e, dict) else float(e) for e in (ev["events"] if isinstance(ev, dict) else ev)]
        result["snapped"] = [{**x, "frame": frames(x["snapped"], a.fps)} for x in snap(times, a.bpm, a.offset, a.tolerance, a.subdivision)]
    if a.every and a.duration:
        g = grid(a.bpm, a.offset, a.duration)
        result["cuts"] = [{"t": t, "frame": frames(t, a.fps)} for t in g[::a.every]]
    dump_json(result, a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
