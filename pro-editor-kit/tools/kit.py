#!/usr/bin/env python3
"""kit — one entry point for every pro-editor-kit tool.

  python3 pro-editor-kit/tools/kit.py doctor
  python3 pro-editor-kit/tools/kit.py autocut words.json --fps 30 --source raw.mp4 --out build/cut --render
  python3 pro-editor-kit/tools/kit.py captions build/cut/words.retimed.json --fps 30 --preset reel --out build/captions
  python3 pro-editor-kit/tools/kit.py lint remotion/src
  python3 pro-editor-kit/tools/kit.py sfx plan.json --library sfx-library.json --voice render.mp4 --music bed.mp3 --out build/sfx --render
  python3 pro-editor-kit/tools/kit.py beats --bpm 120 --events plan.json
  python3 pro-editor-kit/tools/kit.py qa build/final.mp4 --brief brief.json --out build/qa
  python3 pro-editor-kit/tools/kit.py validate brief.json --schema brief
"""
from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
CMDS = {"autocut": "autocut", "captions": "captions", "qa": "render_qa", "lint": "motion_lint",
        "sfx": "sfx_map", "beats": "beat_grid", "validate": "validate"}


def doctor() -> int:
    ok = True
    print(f"python   {sys.version.split()[0]}  {'OK' if sys.version_info >= (3, 9) else 'NEED >= 3.9'}")
    ok &= sys.version_info >= (3, 9)
    for b, why in [("ffmpeg", "cut / mix / QA"), ("ffprobe", "QA"), ("node", "Remotion / HyperFrames (Node 22+ for HyperFrames)"),
                   ("npx", "remotion / hyperframes CLIs"), ("blender", "optional: 3D/CGI via Blender MCP"),
                   ("whisper-cli", "optional: local whisper.cpp transcription"), ("whisperx", "optional: word-aligned transcription")]:
        p = shutil.which(b)
        line = f"{b:9}{' ' + p if p else ' missing'}  ({why})"
        if p and b in ("ffmpeg", "node"):
            v = subprocess.run([b, "-version" if b == "ffmpeg" else "--version"], capture_output=True, text=True).stdout.splitlines()
            line += f"  {v[0][:60] if v else ''}"
        print(line)
        if b in ("ffmpeg", "ffprobe") and not p:
            ok = False
    if shutil.which("ffmpeg"):
        filt = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
        for f in ("blackdetect", "freezedetect", "silencedetect", "ebur128", "sidechaincompress", "drawtext"):
            print(f"  filter {f:18} {'OK' if f in filt else 'missing'}")
    print("doctor:", "READY" if ok else "NOT READY")
    return 0 if ok else 1


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "doctor":
        return doctor()
    if cmd not in CMDS:
        print(f"unknown command '{cmd}'. Commands: doctor, {', '.join(CMDS)}", file=sys.stderr)
        return 2
    mod = importlib.import_module(CMDS[cmd])
    return mod.main(rest)


if __name__ == "__main__":
    raise SystemExit(main())
