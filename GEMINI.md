# GEMINI.md — context for Gemini CLI / Gemini 4 Argon in THE-AI-VIDEO-EDITOR

This repo is a programmatic video studio: Remotion (React), HyperFrames (HTML + GSAP), Three.js/R3F, Blender via MCP, and Higgsfield / Veo for generated pixels. Read these first:

1. `pro-editor-kit/START-HERE-FOR-AGENTS.md`: the operating loop, with the commands to run at every step.
2. `pro-editor-kit/models/gemini-4-argon.md`: your role here (eyes and critic) and the video-understanding knobs (`start_offset`/`end_offset`/`fps`, `media_resolution`, `processing: "agentic"`).
3. `skills/master-editor-protocol/SKILL.md` and `skills/gemini-4-argon-forensic-atlas/SKILL.md`.

## Your default jobs
- **Footage log** → `pro-editor-kit/templates/gemini-footage-log-prompt.md` (JSON out).
- **Reference decomposition** → fill in `pro-editor-kit/templates/visual-training-guide.md`.
- **Critic** after every render → `pro-editor-kit/templates/critic-prompt.md`. List at least 3 timestamped flaws, or the review is invalid.
- When you also write code: use `pro-editor-kit/tokens/motion.ts` (Remotion) or `tokens/motion.gsap.js` (HyperFrames).

## Non-negotiables
- You output text only. Never claim you rendered or generated media; name the tool that did.
- Run `python3 pro-editor-kit/tools/kit.py lint <dir>` before rendering, and `kit.py qa <file> --brief brief.json` before calling anything done.
- Frame-pure animation only: no `Math.random()` without a seed, no `Date.now()`, no CSS transitions in Remotion, and one paused GSAP timeline per HyperFrames composition.
- References must be owned or licensed; likeness and voice need consent.
