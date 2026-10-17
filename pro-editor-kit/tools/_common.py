"""Shared helpers for pro-editor-kit tools. Python 3.9+ standard library only."""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

FILLERS = {"um", "uh", "erm", "uhm", "umm", "uhh", "ah", "ahh", "hmm", "mm", "mhm", "er"}
_PUNCT = re.compile(r"[^\w']+", re.UNICODE)


def norm(token: str) -> str:
    """Lower-case a token and strip punctuation for comparisons."""
    return _PUNCT.sub("", token.lower()).strip("'")


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(data: Any, path: str | Path | None) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if path in (None, "-"):
        sys.stdout.write(text + "\n")
    else:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text + "\n", encoding="utf-8")


def load_words(path: str | Path) -> list[dict]:
    """Normalise word-level transcripts from common engines into
    [{"word": str, "start": float, "end": float}] sorted by start (seconds).

    Accepted shapes: plain list; {"words": [...]}; Whisper / faster-whisper
    {"segments": [{"words": [...]}]}; WhisperX {"word_segments": [...]};
    Deepgram {"results": {"channels": [{"alternatives": [{"words": [...]}]}]}};
    ElevenLabs Scribe {"words": [{"text", "start", "end", "type"}]};
    Remotion Caption[] [{"text", "startMs", "endMs"}].
    """
    data = load_json(path)
    raw: Iterable[dict]
    if isinstance(data, list):
        raw = data
    elif "word_segments" in data:
        raw = data["word_segments"]
    elif "segments" in data:
        raw = [w for seg in data["segments"] for w in seg.get("words", [])]
    elif "results" in data:
        raw = data["results"]["channels"][0]["alternatives"][0]["words"]
    elif "words" in data:
        raw = data["words"]
    else:
        raise ValueError("Unrecognised transcript shape; expected a list of words or a known engine JSON")
    words = []
    for w in raw:
        if w.get("type") in ("spacing", "audio_event"):
            continue
        text = w.get("word", w.get("text", w.get("punctuated_word", "")))
        if "startMs" in w:
            start, end = w["startMs"] / 1000.0, w["endMs"] / 1000.0
        else:
            start, end = w.get("start"), w.get("end")
        if start is None or end is None or not str(text).strip():
            continue  # WhisperX can emit unaligned numerals without timestamps
        words.append({"word": str(text).strip(), "start": float(start), "end": float(max(end, start))})
    words.sort(key=lambda w: w["start"])
    return words


def frames(seconds: float, fps: float, mode: str = "round") -> int:
    v = seconds * fps
    if mode == "floor":
        return int(math.floor(v + 1e-9))
    if mode == "ceil":
        return int(math.ceil(v - 1e-9))
    return int(round(v))


def tc(seconds: float, sep: str = ",") -> str:
    """Seconds -> HH:MM:SS,mmm (SRT) or HH:MM:SS.mmm (VTT)."""
    ms = int(round(max(seconds, 0) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def need(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise SystemExit(f"error: '{binary}' not found on PATH. Install it (e.g. apt install ffmpeg / brew install ffmpeg).")
    return path


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)
