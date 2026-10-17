#!/usr/bin/env python3
"""render_qa — blocking pre-delivery checks on a rendered file. Exit 1 on any FAIL.

Turns skills/motion-quality-gates into numbers a machine can enforce:
black frames, frozen frames, dead air, loudness (EBU R128 integrated LUFS),
true peak, constant frame rate, resolution, duration vs brief (+-1 frame),
plus a contact sheet (1 still every N seconds) for the visual critic pass.

Usage:
  python3 render_qa.py out.mp4 --brief brief.json --out qa/
  python3 render_qa.py out.mp4 --fps 30 --width 1080 --height 1920 --duration 45 --lufs -14 --out qa/
  python3 render_qa.py out.mp4 --allow-freeze 12.0-14.5 --allow-black 0-0.5 --out qa/

Outputs: qa/qa-report.json, qa/qa-report.md, qa/contact-sheet.png
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import dump_json, load_json, need, run  # noqa: E402

PLATFORM_LUFS = {"tiktok": -14, "reels": -14, "shorts": -14, "youtube": -14, "podcast": -16, "broadcast": -23}


def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path])
    import json
    return json.loads(r.stdout)


def parse_windows(specs):
    out = []
    for s in specs or []:
        a, b = s.split("-")
        out.append((float(a), float(b)))
    return out


def inside(windows, s, e):
    return any(a - 0.05 <= s and e <= b + 0.05 for a, b in windows)


def analyse(path, black_d=0.04, freeze_d=0.5, silence_d=1.5, silence_db=-50, has_audio=True):
    vf = f"blackdetect=d={black_d}:pix_th=0.10,freezedetect=n=-60dB:d={freeze_d}"
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vf", vf]
    if has_audio:
        cmd += ["-af", f"silencedetect=n={silence_db}dB:d={silence_d},ebur128=peak=true"]
    cmd += ["-f", "null", "-"]
    err = run(cmd, check=False).stderr
    blacks = [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", err)]
    fs = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", err)]
    fe = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", err)]
    freezes = list(zip(fs, fe + [math.inf] * (len(fs) - len(fe))))
    ss = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    silences = list(zip(ss, se + [math.inf] * (len(ss) - len(se))))
    summary = err[err.rfind("Summary:"):] if "Summary:" in err else ""
    lufs = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summary)
    lra = re.search(r"LRA:\s+(-?[\d.]+) LU", summary)
    tp = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS", summary, re.S)
    num = lambda m: (float(m.group(1)) if m and m.group(1) != "-inf" else None)  # noqa: E731
    return {"black": blacks, "freeze": freezes, "silence": silences,
            "lufs": num(lufs), "lra": num(lra), "true_peak": num(tp)}


def contact_sheet(path, out_png, duration, every, cols=6, width=320):
    n = max(1, math.ceil(duration / every))
    rows = math.ceil(n / cols)
    vf = (f"fps=1/{every},scale={width}:-2,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:"
          f"fontcolor=white:box=1:boxcolor=black@0.6,tile={cols}x{rows}:padding=4:margin=4")
    r = run(["ffmpeg", "-hide_banner", "-y", "-i", path, "-vf", vf, "-frames:v", "1", str(out_png)], check=False)
    if r.returncode:  # drawtext needs a font; retry without timestamps
        vf = f"fps=1/{every},scale={width}:-2,tile={cols}x{rows}:padding=4:margin=4"
        r = run(["ffmpeg", "-hide_banner", "-y", "-i", path, "-vf", vf, "-frames:v", "1", str(out_png)], check=False)
    return r.returncode == 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--brief", help="brief.json (fps, width, height, duration_seconds, platform, lufs)")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--duration", type=float)
    ap.add_argument("--lufs", type=float, help="integrated loudness target; default from platform or -14")
    ap.add_argument("--lufs-tolerance", type=float, default=1.0)
    ap.add_argument("--max-true-peak", type=float, default=-1.0)
    ap.add_argument("--max-silence", type=float, default=1.5, help="dead-air threshold (s)")
    ap.add_argument("--allow-freeze", action="append", help="start-end seconds of intentional holds")
    ap.add_argument("--allow-black", action="append", help="start-end seconds of intentional black (fade in/out)")
    ap.add_argument("--allow-silence", action="append")
    ap.add_argument("--sheet-every", type=float, default=1.0)
    ap.add_argument("--out", default="qa")
    a = ap.parse_args(argv)
    need("ffmpeg")
    need("ffprobe")
    brief = load_json(a.brief) if a.brief else {}
    exp_fps = a.fps or brief.get("fps")
    exp_w, exp_h = a.width or brief.get("width"), a.height or brief.get("height")
    exp_dur = a.duration or brief.get("duration_seconds")
    target = a.lufs if a.lufs is not None else brief.get("lufs", PLATFORM_LUFS.get(str(brief.get("platform", "")).lower(), -14))

    info = probe(a.video)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        print("render_qa: FAIL no video stream", file=sys.stderr)
        return 1
    r_fps, avg_fps = Fraction(v["r_frame_rate"]), Fraction(v.get("avg_frame_rate", "0/1") or "0/1")
    fps = float(r_fps)
    duration = float(info["format"].get("duration", v.get("duration", 0)))
    res = analyse(a.video, freeze_d=0.5, silence_d=a.max_silence, has_audio=au is not None)
    checks = []

    def check(name, ok, detail, blocking=True):
        checks.append({"check": name, "status": "PASS" if ok else ("FAIL" if blocking else "WARN"), "detail": detail})

    check("cfr", avg_fps == 0 or abs(float(avg_fps) - fps) < 0.01, f"r_frame_rate={r_fps} avg_frame_rate={avg_fps}")
    if exp_fps:
        check("fps", abs(fps - float(exp_fps)) < 0.01, f"{fps:.3f} vs brief {exp_fps}")
    if exp_w and exp_h:
        check("resolution", (v["width"], v["height"]) == (int(exp_w), int(exp_h)), f"{v['width']}x{v['height']} vs {exp_w}x{exp_h}")
    if exp_dur:
        tol = 1.0 / fps
        check("duration", abs(duration - float(exp_dur)) <= tol + 1e-3, f"{duration:.3f}s vs {exp_dur}s (+-1 frame = {tol:.3f}s)")
    check("pixel_format", v.get("pix_fmt") in ("yuv420p", "yuvj420p", "yuv420p10le"), f"{v.get('pix_fmt')} (yuv420p plays everywhere)", blocking=False)
    allow_b, allow_f, allow_s = parse_windows(a.allow_black), parse_windows(a.allow_freeze), parse_windows(a.allow_silence)
    bad_black = [b for b in res["black"] if not inside(allow_b, *b)]
    check("black_frames", not bad_black, f"{len(bad_black)} unexpected black span(s): {bad_black[:6]}")
    # A declared black span is also a freeze; do not double-report it.
    bad_freeze = [f for f in res["freeze"] if not inside(allow_f + allow_b, f[0], min(f[1], duration))]
    check("frozen_frames", not bad_freeze, f"{len(bad_freeze)} freeze(s) >0.5s: {bad_freeze[:6]}")
    if au:
        bad_sil = [s for s in res["silence"] if not inside(allow_s, s[0], min(s[1], duration))]
        check("dead_air", not bad_sil, f"{len(bad_sil)} silence(s) >{a.max_silence}s below -50 dB: {bad_sil[:6]}", blocking=False)
        L = res["lufs"]
        check("loudness", L is not None and abs(L - target) <= a.lufs_tolerance, f"integrated {L} LUFS vs target {target} +-{a.lufs_tolerance}")
        tp = res["true_peak"]
        check("true_peak", tp is not None and tp <= a.max_true_peak, f"{tp} dBTP (max {a.max_true_peak})")
    else:
        check("audio_present", False, "no audio stream", blocking=False)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    sheet = contact_sheet(a.video, out / "contact-sheet.png", duration, a.sheet_every)
    failed = [c for c in checks if c["status"] == "FAIL"]
    report = {"video": a.video, "verdict": "FAIL" if failed else "PASS", "fps": fps, "width": v["width"], "height": v["height"],
              "duration": duration, "codec": v.get("codec_name"), "audio": bool(au), "measurements": res, "checks": checks,
              "contact_sheet": str(out / "contact-sheet.png") if sheet else None}
    dump_json(report, out / "qa-report.json")
    md = [f"# QA report - {Path(a.video).name}", "", f"**Verdict: {report['verdict']}**", "", "| Check | Status | Detail |", "|---|---|---|"]
    md += [f"| {c['check']} | {c['status']} | {c['detail']} |" for c in checks]
    if sheet:
        md += ["", "![contact sheet](contact-sheet.png)", "", "Send the sheet + MP4 to the critic (Gemini 4 Argon) - see pro-editor-kit/templates/critic-prompt.md"]
    (out / "qa-report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    for c in checks:
        print(f"{c['status']:4}  {c['check']:14} {c['detail']}")
    print(f"render_qa: {report['verdict']} -> {out}/qa-report.json")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
