#!/usr/bin/env python3
"""motion_lint — catch the code patterns that cause flicker, non-deterministic
renders and amateur motion in Remotion (.tsx/.jsx/.ts/.js) and HyperFrames/GSAP
(.html/.js) compositions. Static, fast, zero dependencies.

Usage:
  python3 motion_lint.py remotion/src             # scan a tree
  python3 motion_lint.py comp.html --json         # machine output
  python3 motion_lint.py src --fail-on warn       # stricter gate

Exit code 1 when any finding at or above --fail-on (default: error).
Silence a line with a trailing comment:  // motion-lint-ignore R005
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LEVEL = {"info": 0, "warn": 1, "error": 2}

# (id, level, regex, message, scope) scope: remotion | gsap | any
RULES = [
    ("D001", "error", r"\bMath\.random\s*\(", "Math.random() renders differently per frame/worker. Use random('seed') from remotion or a seeded PRNG.", "any"),
    ("D002", "error", r"\bDate\.now\s*\(|\bnew Date\s*\(\s*\)|\bperformance\.now\s*\(", "Wall-clock time breaks seeking and parallel rendering. Derive time from the frame (useCurrentFrame()/fps or the GSAP timeline).", "any"),
    ("D003", "error", r"\b(setTimeout|setInterval|requestAnimationFrame)\s*\(", "Timers are not frame-accurate. Drive animation from the frame/timeline.", "any"),
    ("R001", "error", r"(?<![-\w])transition\s*:\s*['\"]?(?!none)[a-z]|@keyframes|(?<![-\w])animation\s*:\s*['\"]?(?!none)[a-z]", "CSS transitions/keyframes are not seekable in Remotion. Use interpolate()/spring() on useCurrentFrame().", "remotion"),
    ("R002", "warn", r"<(img|video|audio)\b", "Use Remotion's <Img>, <Video>/<OffthreadVideo> and <Audio> so renders wait for media (delayRender).", "remotion"),
    ("R003", "warn", "CALL:interpolate:extrapolateRight:frame", "Frame-driven interpolate() without extrapolateRight:'clamp' keeps moving past the last keyframe (drift/overshoot).", "remotion"),
    ("R004", "warn", r"\bEasing\.linear\b", "Linear easing reads as robotic for entrances/exits. Use Easing.bezier(0.16,1,0.3,1) (out) / (0.7,0,0.84,0) (in); keep linear for loops/tickers only.", "remotion"),
    ("R005", "warn", "CALL:spring:config", "spring() without config uses damping 10 (bouncy). Set config {damping: 12-20, mass: 0.6-1, stiffness: 100-200}.", "remotion"),
    ("R006", "warn", r"\buse(State|Effect)\s*\(", "React state/effects for timing are not frame-deterministic in Remotion. Compute from useCurrentFrame().", "remotion"),
    ("R007", "warn", r"fonts\.googleapis\.com", "Remote font CSS can render fallback glyphs on early frames. Use @remotion/google-fonts loadFont() or local woff2 + delayRender.", "remotion"),
    ("G001", "warn", "CALL:gsap.timeline:paused", "HyperFrames needs seekable timelines: gsap.timeline({ paused: true }) registered on window.__timelines.", "gsap"),
    ("G002", "warn", r"ease\s*:\s*['\"](none|linear|power0[.\w]*)['\"](?:(?!repeat\s*:\s*-1).){0,120}$", "Linear ease on a one-shot tween looks mechanical. Use expo.out / power3.out for entrances, power2.in for exits.", "gsap"),
    ("G003", "warn", r"duration\s*:\s*0?\.(0\d|1[01])\b", "Tweens under 0.12 s read as flicker on 30 fps (<4 frames).", "gsap"),
    ("G004", "warn", r"back\.out\(\s*([3-9]|[2-9]\.\d)", "Overshoot > 2 looks cheap. Keep back.out(1.2-1.7) or use a spring.", "gsap"),
    ("G005", "error", r"(?<![-\w])transition\s*:\s*(?!none)[a-z]|@keyframes", "CSS transitions/keyframes are not captured by frame-seeking renderers. Move motion into the GSAP timeline.", "gsap"),
    ("Q001", "info", r"scale\s*[:(]\s*['\"]?(1\.[3-9]|[2-9])", "Large scale jumps (>=1.3x) on UI read as amateur - reference rule: make elements ~25% smaller, move less.", "any"),
    ("Q002", "info", r"#(?:000000|000|ffffff|fff|ff0000|f00)\b", "Pure black/white/red reads harsh. Prefer muted tokens (see tokens/motion-tokens.json palettes).", "any"),
]
EXTS = {".tsx", ".jsx", ".ts", ".js", ".mjs", ".html", ".htm"}
SKIP_DIRS = {"node_modules", "dist", "build", ".git", "out", "vendor", ".next"}


class _Hit:
    def __init__(self, start: int):
        self._s = start

    def start(self) -> int:
        return self._s


def call_matches(text: str, spec: str):
    """Yield hits for calls `name(...)` whose balanced argument list lacks `needle`."""
    parts = spec.split(":")
    name, needle = parts[1], parts[2]
    first_arg_must = parts[3] if len(parts) > 3 else None
    for m in re.finditer(r"(?<![\w.])" + re.escape(name) + r"\s*\(", text):
        depth, i = 0, m.end() - 1
        while i < len(text):
            ch = text[i]
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        args = text[m.end():i]
        if first_arg_must and first_arg_must not in args.split(",")[0].lower():
            continue  # e.g. interpolate(springProgress, [0, 1], ...) is already bounded
        if needle not in args and not (needle == "extrapolateRight" and "clamp" in args):
            yield _Hit(m.start())


def scope_of(path: Path, text: str) -> set[str]:
    s = {"any"}
    if re.search(r"from\s+['\"](remotion|@remotion/)", text):
        s.add("remotion")
    if path.suffix in (".html", ".htm") or re.search(r"\bgsap\b", text):
        s.add("gsap")
    return s


_COMMENT = re.compile(r"/\*.*?\*/|(?<![:\\'\"])//[^\n]*|<!--.*?-->", re.S)


def mask_comments(text: str) -> str:
    """Blank out comments (keeping newlines) so prose like 'no Date.now()' is not flagged."""
    return _COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def in_string(line: str, col: int) -> bool:
    """True when column `col` of `line` sits inside a '...', "..." or `...` literal."""
    quote = None
    i = 0
    while i < min(col, len(line)):
        ch = line[i]
        if ch == "\\":
            i += 2
            continue
        if quote is None and ch in "'\"`":
            quote = ch
        elif ch == quote:
            quote = None
        i += 1
    return quote is not None


def lint_text(path: Path, text: str):
    scopes = scope_of(path, text)
    findings = []
    lines = text.splitlines()
    text = mask_comments(text)
    for rid, level, rx, msg, scope in RULES:
        if scope not in scopes:
            continue
        matches = call_matches(text, rx) if rx.startswith("CALL:") else re.compile(rx, re.M).finditer(text)
        for m in matches:
            line_no = text.count("\n", 0, m.start()) + 1
            line = lines[line_no - 1] if line_no - 1 < len(lines) else ""
            if f"motion-lint-ignore {rid}" in line or "motion-lint-ignore-all" in line:
                continue
            if rid[0] in "DR" and rid not in ("R001", "R002", "R007") and in_string(line, m.start() - (text.rfind("\n", 0, m.start()) + 1)):
                continue  # code shown as on-screen text, e.g. "const x = spring({...})"
            if rid == "D001" and re.search(r"seed|prng|mulberry|random\(\s*['\"]", line, re.I):
                continue
            findings.append({"file": str(path), "line": line_no, "rule": rid, "level": level, "message": msg,
                             "excerpt": line.strip()[:160]})
    return findings


def iter_files(paths):
    for p in paths:
        p = Path(p)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.suffix in EXTS and f.is_file() and not (set(f.parts) & SKIP_DIRS) and not f.name.endswith(".min.js"):
                    yield f


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fail-on", choices=list(LEVEL), default="error")
    a = ap.parse_args(argv)
    findings = []
    for f in iter_files(a.paths):
        try:
            findings += lint_text(f, f.read_text(encoding="utf-8", errors="replace"))
        except OSError as exc:
            print(f"skip {f}: {exc}", file=sys.stderr)
    if a.json:
        print(json.dumps(findings, indent=2))
    else:
        for x in findings:
            print(f"{x['file']}:{x['line']}  {x['level'].upper():5} {x['rule']}  {x['message']}\n      > {x['excerpt']}")
        counts = {lv: sum(1 for x in findings if x["level"] == lv) for lv in LEVEL}
        print(f"motion_lint: {counts['error']} error(s), {counts['warn']} warning(s), {counts['info']} note(s)")
    worst = max((LEVEL[x["level"]] for x in findings), default=-1)
    return 1 if worst >= LEVEL[a.fail_on] else 0


if __name__ == "__main__":
    raise SystemExit(main())
