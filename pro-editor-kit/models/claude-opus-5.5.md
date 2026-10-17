# Claude Opus 5.5 — playbook for editing, motion graphics and CGI

Specs, effort ladder and cost math are already in `skills/opus-5-5-sol-6-1-director/` (model id `claude-opus-5-5`, 1M context, adaptive thinking controlled by `effort`).
This file covers **how creators actually got good results**, taken from transcripts and labelled with video ids. See [evidence/](../evidence/).

## What Opus is best at here
- Turning a plan into many Remotion/HyperFrames compositions in one long session. In `5UnK3c-nlIs` it built 12 animations, captions, full/half screens, UI inserts, zooms and camera moves in about 40 minutes.
- Writing Blender Python through the Blender MCP bridge and producing 3D cinematics (`5XSwP0DaHF4`), plus voxel "galaxy → atom" zooms.
- Following a long written style guide precisely, provided it is turned into a **skill** so it persists across sessions.

## Where Opus was slow or wrong (and the fix in this kit)
| Observed | Video | Fix |
|---|---|---|
| Cutting a 1-minute talking head took **24 min** | `5UnK3c-nlIs` | `tools/autocut.py` (deterministic, < 1 s) |
| Graphics looked "simplistic", with no visuals that represented the words | `5XSwP0DaHF4` | Ask Opus to write an **asset-sheet prompt** for an image model, then animate those assets → `playbooks/editorial-explainer.md` |
| HUD perspective inverted, and verbal correction failed repeatedly | `5XSwP0DaHF4` | Draw the correct perspective on a still and attach the sketch → `playbooks/hud-and-tracked-overlays.md` |
| Blender scene had overlapping buildings and unrealistic rockets/explosions | `5XSwP0DaHF4` | Bounding-box overlap check + clay-render review → `playbooks/3d-voxel-and-blender.md` |
| Copied image assets "not exactly" | `5XSwP0DaHF4` | Treat references as style guides. Import exact assets as files whenever fidelity matters |
| First drafts ignore what the editor wants on screen | `5UnK3c-nlIs` | Planning board: the human chooses the scene type per line before any build |

## Prompt shapes that worked

**Cut** (then replace the slow part with autocut):
> I have a short-form video to edit. Use the *viral talking head editor* skill. Create a word-level transcript, remove every silence and every bad take, keep about 20 ms padding, and hand back the cut video.

**Build from the plan:**
> Here's the full plan (`scene-plan.json`). Use Remotion to build these animations following the visual training skill. **Before you start, tell me every asset you need from me.** Use `pro-editor-kit/tokens/motion.ts` for all timing and easing. Run `kit.py lint` and fix every error before rendering.

**Sound** (a separate skill):
> Use the sound design guide and my SFX library to sound-design the video you just edited. Write down everything that happens on screen first, then place each sound. Music bed at −20 dB.

**Show-reel discovery** (to find a style worth reusing):
> Create a show reel demonstrating what you can do. Go all out. → choose the strongest look → "Use that 3D voxel style for …"

## Settings
- Use effort `high` for build sessions and `medium` for edits to an existing plan. Set effort to `max` only for one-shot hero shots (see the director skill's ladder).
- Give Opus the project **folder**, not individual files. Grant network access for model downloads (e.g. `huggingface.co`, `*.hf.co` for whisper.cpp), and computer use for Blender.
- Turn every accepted correction into a skill update (`j8YDz-VC-AM`, `Z3tvYkwAzHE`): appearance rules in one file, movement rules in another.

## Reported time and cost (creator-reported, not audited)
`5UnK3c-nlIs`: 110 min wall-clock with 20 min of human input (cut 24, plan 15, animate 40, sound 25), under 10% of a weekly Max plan.
`Z3tvYkwAzHE`: 14 min 59 s edit on a prepared framework that took an estimated 20–30 h to build.
