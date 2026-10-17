# Reference-video breakdowns (transcript-grounded)

Retrieved 2026-10-17 from the YouTube watch pages' transcript text. Only spoken content is used. On-screen-only details (exact fonts, hex codes, easing curves) are **unknown** and were not invented.
This supersedes the "0 transcripts retrieved" status in `resources/video-editing-evidence/README.md` (2026-10-14) for these three ids. That file is left unchanged.

---

## 1. `5UnK3c-nlIs` — "How to Edit VIRAL Instagram Reels Using Opus 5.5! (New Style in 2026)"
**Model:** Claude Opus 5.5 on high effort · **Renderer:** Remotion · **Input:** 76 s raw talking head → 50 s cut

### The two trainings (the creator's core claim: bad AI edits come from bad training)
**A. Visual training guide**, with three parts (template: [`templates/visual-training-guide.md`](../templates/visual-training-guide.md)):
1. **Captions:** a reference image of the style; two fonts (a medium sans for most words, a script font for special words); white for normal words and one accent colour for words that pop; position; effects; animation is a *word-by-word pop-up, faded*; many examples. **Hook rules:** speaker always on screen, subtitles in the lower half, highlight the *one word that makes you keep watching*.
2. **Animations:** three example looks (white, cast shadows, yellow), then four types:
   - **Text-centric** (text is the star) · **Person-centric** (built around a character) · **Object-centric** · **Graphic-centric** (charts, UIs)
   - How to build the background step by step.
   - **Three-object rule:** ① a main object in the centre ② supporting elements on the edges ③ depth elements around the outside.
   - Design basics (colour options, fonts, how text, objects and backgrounds look) plus 100+ inspiration pieces.
3. **On-screen animations** (small pop-ups while talking): the background behind darkens and blurs, and the animation sits in the lower half.

Then: "drop the guide into Claude, ask it to analyse it, then **ask Claude to turn it into a skill**."

**B. Sound-design training** (template: [`templates/sound-design-guide.md`](../templates/sound-design-guide.md)):
- Minimum library: **5 whooshes** (long, short, textured), **2–3 mechanical clicks** (short, metallic, retro), **2–3 sci-fi** (impacts, clicks, shots), **2–3 UI** (click, success, fail), **2 risers + 2 hits** (bass riser, metallic riser, bass hit, heavy hit).
- Guide structure: who Claude is and the goal → philosophy (*"it's all about the motion"*) → three families → loudness → placement → per-section usage (whooshes, textures, risers/hits).

### Pipeline and timings (creator's screen recording)
| Step | What happened | Time |
|---|---|---|
| Cut | Word-level transcript; remove every silence and bad take; ~20 ms padding | **24 min** (creator: "way too slow", so cut manually or with a faster app) |
| Plan | Claude builds a **planning page**: accent colour, two fonts and font colours at the top; script lines on the left; a free-text plan box per line; **one of four scene types per line: Captions · Captions + UI (lower-half animation) · Half screen (animation top, speaker bottom) · Full screen** | 15 min (human) |
| Animate | "Here's the full plan, use Remotion to build these animations." **Tip: ask Claude what assets it needs** (it requested a screenshot and an eyeball image, and fetched brand logos itself via Chrome) | 40 min |
| Review | Watch everything, then "change X, Y and Z" | — |
| Sound | Claude lists every on-screen event, then places whooshes for movement, clicks/pops for appearances, risers and hits for anticipation. Song added at **−20 dB** | 25 min |
| **Total** | 110 min wall-clock, about 20 min of human time. Under 10% of a weekly Max plan; creator estimates $1–5 per edit | |

### The edit's own content = three design rules worth encoding
1. **Stop oversizing:** make every element **25% smaller**.
2. **Stop overusing effects:** *the less you use an effect, the more special it is*.
3. **Use duller colours:** avoid harsh black, harsh white and bright red. Luxury brands use dull blues and greens.
These are encoded in `tokens/motion-tokens.json` (`scale.element_size_rule`, `palettes`) and in lint rules Q001/Q002.

Scene mix used: a chapter UI (circles 1-2-3 filling) as connective tissue; half-screens for explanations (a loading bar where only one segment lights up; three colour boxes); full-screens for big moments (an eyeball spinning with timeline cards sliding around it; luxury logos spinning in a circle, then fading as new text writes on).

---

## 2. `5XSwP0DaHF4` — "Claude Opus 5.5 Changed Motion Graphics Forever (Insane Results)"
**Model:** Claude (Opus 5.5) · **Use cases:** editorial graphics for talking heads, HUD displays, 2D explainers, AI music videos, 3D voxel animation, Claude + Blender 3D cinematics

| Use case | Pipeline as described | Problems hit → fix |
|---|---|---|
| **Editorial talking head** | Install **whisper.cpp** via Claude (allow `huggingface.co` and `*.hf.co`) → SRT. Project folder with the talking head plus a **style reference video**. Prompt: transcribe, cut awkward pauses, copy the motion-graphic style, use a custom motion-graphics skill. First draft after about 30 min | Graphics "simplistic", with nothing representing the words → have Claude write an **asset-sheet prompt** for an image model (GPT Image 2.5, 2K+), generate the sheets, add CEO photos and logos, desaturate the avatar, add a split screen (head bottom, graphics top), then iterate by voice |
| **HUD on AI video** | Generate a still of yourself in an Iron-Man helmet setting → animate it (Seedance 2.5) → Claude tracks HUD panels onto it | Perspective inverted and verbal corrections failed → **draw the correct perspective in Paint and attach it**. Claude then added curved edges and tracking held |
| **2D explainer** | AI voice-over plus a style reference → transcript → 2D graphics using the skill | **Stop the render early** if the preview is wrong (palette, character maturity, missing scene) |
| **Music video** | Claude writes the lyrics (Suno song), a character-sheet prompt and background prompts. Point Claude at public GitHub repos for music-video rendering and animation | The first draft lacked effects, lyrics and environments → more asset prompts. References are followed in style but **not copied exactly** |
| **3D voxel** | "Create a show reel… go all out", then pick the voxel style → galaxy → solar system → Earth → molecules → atoms | — |
| **Blender cinematic** | Install the Claude connector for Blender and the add-on (drag the zip into Blender, then **Start MCP bridge server**). Enable computer use. Image prompts for asset sheets, then upscale, then an image-to-3D tool, then export models into the folder. Claude scripts the scenes and you render overnight | Overlapping buildings, implausible rockets and explosions → see `playbooks/3d-voxel-and-blender.md` checks |

---

## 3. `dT5-x3u5nCg` — "GPT-6 Astra Made This Entire Video" (linked by the user as the "gpt 6.1 sol" example)
**Model:** GPT-6 Astra (computer use, long tasks) · **Renderer:** HyperFrames · **Presenter:** HeyGen avatar ("Avatar V5" as spoken; the API engine is `avatar_v`, see the capability delta)

One prompt. The model then:
1. Opened the original social posts and **captured the pages**, checking what was actually on screen.
2. Worked through the creator's project folders and found the avatar setup, voice clone and connected tools.
3. Split the narration into **short segments**, sent the audio to HeyGen and placed the results beside the original demos.
4. Built the edit in **HyperFrames**, controlling the timing of each camera move, word, clip and transition.
5. Sound: **music carries the longer moves, a click lands on each interface change, and a short break gives the next shot room to hit.**
6. Rendered, **checked frames from the exported file**, **transcribed the finished audio and compared it with the script**, and fixed clipped titles or sounds that covered words.

The creator only specified "use my voice clone and avatar" and "work in some verification so you're not just giving me the first version". About 50 min; ~$60 at API rates on fast mode (estimate).
This verification loop is step 12 of [`START-HERE-FOR-AGENTS.md`](../START-HERE-FOR-AGENTS.md). Playbook: [`playbooks/avatar-presenter-heygen.md`](../playbooks/avatar-presenter-heygen.md).
