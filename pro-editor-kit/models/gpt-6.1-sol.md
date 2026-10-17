# GPT-6.1 Sol and GPT-6 Astra — playbook

> **Naming caution.** The user-supplied search "gpt 6.1 sol" returns mostly **GPT-6 Astra** demos. The linked example `dT5-x3u5nCg` is *"GPT-6 Astra Made This Entire Video"*. Specs for `gpt-6.1-sol` are in `skills/opus-5-5-sol-6-1-director/references/model-specs.md`. Claims below name the model the video actually used.

## Strengths shown on video
- **Autonomous end-to-end production with verification** (Astra, `dT5-x3u5nCg`). The model opened the original posts and captured the pages, found the user's avatar and voice clone, split the narration into short segments, generated presenter clips with HeyGen, edited in **HyperFrames**, designed sound around the cuts (music for long moves, a click on each interface change, short breaks before hits), rendered, **checked frames from the exported file**, and **transcribed the finished audio and compared it with the script**. About 50 minutes; roughly $60 at API rates on fast mode (creator estimate).
- **Driving real NLEs.** Resolve 21.1 MCP rough cut 75 → ~22 min with audio checks and 4K export (`V7CtHz8JFWA`). Premiere via computer use: transcript → filter pauses → delete → repeat until "no results"; jump cuts hidden with a 105–110% Transform and eye-line matching (`1ji3qE9VY2k`).
- **Procedural CG in one script** at different effort levels, reported costs $0.65–$3.19 (Sol, `OozE-pGByWg`).
- **Autonomous educational video** under a 1-hour budget with code-generated music/SFX (Sol, `YLAvsPqC4Ms`).

## Weakness to design around
With identical briefs, creators reported **slideshow-like** Sol/Astra motion compared with Opus (`q_DKy8BrZhY`, `sE9wJRYH-18`). These are creator-specific comparisons, not a ranking, but the remedy is cheap:
1. Require a **per-shot motion verb** in the scene plan ("morphs", "pushes", "tracks", "orbits"). Static "shows" is not allowed.
2. Require **one persistent object that morphs between ideas** instead of disconnected slides (`6Ij9-f2T2Ck`).
3. Require a **camera** value on every line (`schemas/scene-plan.schema.json`).
4. Run `kit.py lint` and have a separate critic count "static holds > 1.5 s without motion".
5. Use paper storyboards first: sketch, photograph and attach (`sE9wJRYH-18`).

## Best role in a mixed team
**Critic and verifier.** Give it the contact sheet, the QA report and the script, and require at least 3 timestamped flaws. Second-best role: **NLE operator** when the deliverable must be a Resolve/Premiere project rather than code.

## Prompt shape (Astra-style autonomous run)
> Make a 90-second video about X using my avatar and voice clone. Find the footage, capture the source posts, write the script, build the edit in HyperFrames, and design the sound. **Verify before handing back:** check frames from the exported file, transcribe the final audio and diff it against the script, and run `pro-editor-kit/tools/kit.py qa`. Don't give me the first version.
