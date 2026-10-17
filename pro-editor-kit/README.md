# Pro Editor Kit — tools that let an AI edit like a senior editor, and prove it

> **Additive pack, 2026-10-17.** Nothing outside `pro-editor-kit/`, `GEMINI.md` and `llms.txt` was changed.
> Works with **Claude Opus 5.5**, **GPT-6.1 Sol / GPT-6 Astra**, **Gemini 4 Argon**, Claude Code, Codex, Gemini CLI, or any agent with a shell.

The repo already has the *doctrine* (`skills/master-editor-protocol`, `skills/motion-quality-gates`,
`skills/opus-5-5-sol-6-1-director`, the Gemini / Higgsfield / HeyGen / Remotion forensic atlases).
This kit adds what doctrine alone cannot give an agent:

1. **Deterministic tools** for the steps where models were slow or error-prone in the reference videos
   (Opus 5.5 took **24 minutes to cut a 1-minute clip** in `5UnK3c-nlIs`; a transcription engine silently
   dropped 13 s in `j8YDz-VC-AM`; generated text turned to gibberish in `EcxvHRccXnc`).
2. **Machine-checkable gates** so "no bad motion, no mistakes" is a test result, not a hope.
3. **Transcript-grounded evidence** from 26 YouTube editing videos, plus a dated capability delta.
4. **Fill-in templates** for the two kinds of "training" every successful creator gave their model:
   a *visual training guide* and a *sound-design guide*.

## 60-second start

```bash
python3 pro-editor-kit/tools/kit.py doctor                                  # ffmpeg filters, node, optional blender/whisper
python3 -m unittest discover -s pro-editor-kit/tests                         # 19 tests, incl. real ffmpeg renders
python3 pro-editor-kit/tools/kit.py autocut words.json --fps 30 --source raw.mp4 --out build/cut --render
python3 pro-editor-kit/tools/kit.py captions build/cut/words.retimed.json --fps 30 --preset reel --out build/captions
python3 pro-editor-kit/tools/kit.py lint remotion/src                        # determinism + motion-quality lint
python3 pro-editor-kit/tools/kit.py qa build/final.mp4 --brief brief.json --out build/qa   # exit 1 = do not ship
```

Python 3.9+ standard library only. `ffmpeg`/`ffprobe` for cutting, mixing and QA. No `pip install`.

## What is in here

| Path | What it gives an agent |
|---|---|
| [`START-HERE-FOR-AGENTS.md`](START-HERE-FOR-AGENTS.md) | The operating loop: brief → transcript → cut → plan → build → lint → render → QA → critic → sound → deliver, with exact commands and stop conditions |
| [`models/`](models/) | Per-model playbooks: [Claude Opus 5.5](models/claude-opus-5.5.md) · [GPT-6.1 Sol / GPT-6 Astra](models/gpt-6.1-sol.md) · [Gemini 4 Argon](models/gemini-4-argon.md) |
| [`playbooks/`](playbooks/) | Viral talking-head reel · sound design · editorial explainer · avatar presenter (HeyGen + HyperFrames) · HUD/tracked overlays · 3D voxel & Blender · revision protocol |
| [`templates/`](templates/) | Visual training guide · sound-design guide · **planning board (HTML)** · critic prompt · Gemini footage-log prompt · beat table |
| [`tools/`](tools/) | `autocut` · `captions` · `render_qa` · `motion_lint` · `sfx_map` · `beat_grid` · `validate` · `kit` (entry point) |
| [`tokens/`](tokens/) | `motion-tokens.json` (durations, easings, springs, safe areas, palettes, loudness) + `motion.ts` (Remotion) + `motion.gsap.js` (HyperFrames) |
| [`schemas/`](schemas/) | JSON Schemas for brief, scene plan, SFX library, QA report |
| [`evidence/`](evidence/) | [Reference-video breakdowns](evidence/reference-video-breakdowns.md) · [YouTube technique catalogue (23 more videos)](evidence/youtube-technique-catalogue.md) · [Capability delta 2026-10-17](evidence/capability-delta-2026-10-17.md) |
| [`examples/`](examples/) | Sample transcript (with a filler, a stutter and a retake), scene plan, brief, SFX library |

## The tools

| Tool | Replaces | Key behaviour |
|---|---|---|
| `autocut.py` | The slowest step in the reference videos | Reads Whisper / faster-whisper / WhisperX / Deepgram / ElevenLabs / Remotion `Caption[]`. Removes silences > 350 ms, fillers, stutters (repeated 2–4-word runs) and **retakes (keeps the last attempt)**. Frame-aligned ranges, 8 ms seam fades, alternating 100/112% punch-ins, retimed word timings, ffmpeg render script |
| `captions.py` | Hand-paged subtitles | Presets `reel` (≤4 words), `youtube`, `broadcast`. Splits on pauses/punctuation, rebalances orphan words, caps reading speed, picks **one accent word per page** (numbers/money first, or your keyword list). Writes SRT, VTT, frame-indexed JSON and `@remotion/captions` `Caption[]` |
| `motion_lint.py` | Eyeballing code | Flags `Math.random`, wall clocks, timers, CSS transitions/keyframes, unclamped frame-driven `interpolate`, default-bouncy `spring`, non-paused GSAP timelines, linear one-shot eases, sub-4-frame tweens, cheap overshoot. Ignores comments and code shown as on-screen text |
| `render_qa.py` | "Looks fine to me" | Black frames, frozen frames, dead air, EBU R128 loudness, true peak, CFR, fps, resolution, duration ±1 frame, pixel format, plus a timestamped **contact sheet** for the visual critic. Declare intentional holds with `--allow-freeze` / `--allow-black` |
| `sfx_map.py` | Ad-hoc sound placement | Routes plan events to three families: whooshes **peak on the cut**, risers **end on the reveal**, pops land on the first visible frame. De-stacks, caps density at 3/s, rotates variants, builds an ffmpeg mix with the music bed at −20 dB **side-chain ducked** under the voice |
| `beat_grid.py` | Guessing at the beat | Snaps events to beats or half-beats within tolerance. When an event is too far from the grid, it stays where the speech put it |
| `validate.py` | Malformed plans | Validates brief / scene plan / SFX library against the schemas with no dependencies |

## Honesty notes

- Model names and release facts come from the existing repo atlases and the cited public pages. Vendor benchmarks are vendor claims.
- YouTube evidence comes from **transcripts**. Nobody watched the pixels, so on-screen-only details are marked as unknown.
- Most videos named "GPT 6.1 Sol" in search results actually demonstrate **GPT-6 Astra**. Each claim below is labelled with the model the video actually used.
- Reference footage must be owned or licensed, and likeness work needs consent. See `skills/higgsfield-forensic-atlas` §6.
