# START HERE — operating loop for any AI editor

Read this file and `skills/master-editor-protocol/SKILL.md`, then follow the loop.
Every step ends in a file you can show. **Never claim a render is good without a `qa-report.json` showing PASS.**

## 0. Role routing (who does what)

| Stage | Default | Why (evidence) |
|---|---|---|
| Watch footage, log takes, judge renders | **Gemini 4 Argon** | Native video+audio input, `processing:"agentic"` for long footage. Text output only → [models/gemini-4-argon.md](models/gemini-4-argon.md) |
| Plan, write Remotion/HyperFrames/Blender code, long multi-file builds | **Claude Opus 5.5** (effort `high`) | Strongest long-horizon coding profile. Used in 15 of the analysed videos → [models/claude-opus-5.5.md](models/claude-opus-5.5.md) |
| Independent critic, alternate cuts, copy, computer-use in NLEs | **GPT-6.1 Sol / GPT-6 Astra** | The writer must never grade itself. Astra drove Resolve MCP and Premiere in `V7CtHz8JFWA`, `1ji3qE9VY2k` → [models/gpt-6.1-sol.md](models/gpt-6.1-sol.md) |
| Pixels that code cannot make (photoreal B-roll, restyle, swaps) | Higgsfield / Veo / Omni | **Code first, pixels last.** Generate footage with no text, then add exact type in code (`EcxvHRccXnc`) |

A single model can run every role. Even then, run the critic in a **fresh context** with no access to the writer's reasoning.

## 1. Brief (2 min)
Write `build/brief.json` (see `examples/brief.sample.json`). Validate:
```bash
python3 pro-editor-kit/tools/kit.py validate build/brief.json --schema brief
```
Ask the human only for things that are genuinely missing: platform, aspect, duration, voice, brand palette/fonts, references and their rights.

## 2. Probe and conform
```bash
ffprobe -v error -show_streams -of json raw.mp4 > build/probe.json
```
Choose one timeline fps (the source fps if it is 24/25/30/50/60). If the source is VFR (`r_frame_rate != avg_frame_rate`), conform it first:
`ffmpeg -i raw.mp4 -vf fps=30 -c:a copy build/raw.cfr.mp4`

## 3. Word-level transcript
Use any engine that gives per-word timestamps: whisper.cpp `-ojf`, faster-whisper `word_timestamps=True`, WhisperX, Deepgram, ElevenLabs Scribe, or `npx hyperframes transcribe`.
**Coverage check** (prevents the 13-second silent drop seen in `j8YDz-VC-AM`): compare `words[-1].end` with the media duration, then look for any gap longer than 5 s that contains speech (check `silencedetect`). Re-transcribe that range if one exists.

## 4. Cut (seconds, not 24 minutes)
```bash
python3 pro-editor-kit/tools/kit.py autocut build/words.json --fps 30 --source build/raw.cfr.mp4 --out build/cut --render
```
Read `cut-plan.json → removed_words`. If a removed "retake" was actually the better delivery, rerun with `--lookahead 1`, or `--retake-prefix 4` for stricter matching. Keep `--pad-in 0.06 --pad-out 0.10` unless consonants are being clipped.

## 5. Plan every line before building anything
Open `templates/planning-board.html` in a browser and load `build/cut/words.retimed.json`. For every line, choose a **scene type** (captions / captions+UI / half-screen / full-screen / B-roll), an **animation type** (text / person / object / graphic), the camera, notes and keywords, then export `scene-plan.json`. This is the workflow from `5UnK3c-nlIs`, where the human spent about 15 minutes planning and the model built the rest.
Density for reels: about one graphic every 3–5 s. **Change the scene type at least every two lines.**
```bash
python3 pro-editor-kit/tools/kit.py validate build/scene-plan.json --schema scene-plan
```

## 6. Captions
```bash
python3 pro-editor-kit/tools/kit.py captions build/cut/words.retimed.json --fps 30 --preset reel --keywords build/keywords.txt --out build/captions
```
Fix every reading-speed warning by trimming copy or extending holds. Never fix one by shrinking the font.

## 7. Build
- **Remotion:** import `pro-editor-kit/tokens/motion.ts` (`enter`, `exit`, `springIn`, `stagger`, `holdFrames`, `popScale`, `punchIn`, `safeArea`). Load captions from `captions.remotion.json` or `captions.pages.json`.
- **HyperFrames:** load `tokens/motion.gsap.js`. Create one paused timeline per composition and register it at `window.__timelines["<data-composition-id>"]` after the build finishes.
- Follow the visual training guide (`templates/visual-training-guide.md`), including the **three-object rule**, the **25%-smaller rule**, muted colours and minimal effects.
- **Ask the human for missing assets** (logos, screenshots, product shots) instead of drawing bad stand-ins (`5UnK3c-nlIs`).

## 8. Lint → preview → render
```bash
python3 pro-editor-kit/tools/kit.py lint remotion/src         # or your HyperFrames folder; 0 errors required
npx remotion studio  |  npx hyperframes preview               # look at stills at every beat before a full render
```
Render a low-resolution draft first. Duplicate the composition before any revision, and list in writing which features must be preserved (`6_rCyryA6hg`).

## 9. QA gate (blocking)
```bash
python3 pro-editor-kit/tools/kit.py qa build/final.mp4 --brief build/brief.json --out build/qa
```
Every check must PASS. Declare intentional holds explicitly (`--allow-freeze 12-14.5`).

## 10. Critic loop (blocking)
Send `build/qa/contact-sheet.png` and the MP4 to the critic using `templates/critic-prompt.md`. The critic must list **at least 3 timestamped, actionable flaws** (a review with zero flaws counts as a failed review). The writer fixes them, then a **fresh** critic reviews again (`Z3tvYkwAzHE`). Stop when no blocking flaws remain and the critic scores the cut 9/10 or higher.

## 11. Sound
```bash
python3 pro-editor-kit/tools/kit.py sfx build/scene-plan.json --library sfx/library.json --voice build/final.mp4 --music bed.mp3 --out build/sfx --render
python3 pro-editor-kit/tools/kit.py qa build/sfx/mixed.mp4 --brief build/brief.json --out build/qa-final
```
Leave deliberate silence before big reveals (`MzUV03KouXM`).

## 12. Verify the finished file, then deliver
Transcribe the **exported** audio and diff it against the script, then inspect frames from the exported file itself (the GPT-6 Astra verification loop in `dT5-x3u5nCg`).
Deliver: master + platform cuts, `captions.srt`, `cut-plan.json`, `scene-plan.json`, `qa-report.md`, contact sheet, and a one-paragraph changelog.

## Stop conditions — escalate to the human instead of guessing
- You are missing rights or consent for a reference, a likeness or a voice.
- The transcript coverage check still fails after re-transcribing.
- QA has failed three times on the same check.
- A generated asset still contains wrong text or wrong identity details after two regenerations.
