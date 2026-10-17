# YouTube technique catalogue — 23 additional videos (transcript-grounded)

Compiled 2026-10-17 from the YouTube search results for `claude opus 5.5` and `gpt 6.1 sol` plus related queries. Excludes the three videos in [reference-video-breakdowns.md](reference-video-breakdowns.md). Every bullet ends with the source video id(s). The YouTube search pages returned partial listings, so this is broad coverage, not an exhaustive census.

## A) Table of videos analysed

**23 relevant videos:** 15 covering Opus 5.5 and 10 covering Sol/Astra, with two overlaps. Watch-page transcript text loaded for these entries. **O = Claude Opus 5.5; S = GPT-6.1 Sol; A = GPT-6 Astra.** “—” means channel not verified. Titles/model claims are those of the sources, not independent performance certification.

| Video id | Title | Channel | Model | 1-line topic |
|---|---|---|---|---|
| [MzUV03KouXM](https://www.youtube.com/watch?v=MzUV03KouXM) | 3 Skills I Use to Automate AI Video Editing With Claude Opus 5.5 | Mira AI | O | Hyperframes, generated B-roll, sound maps |
| [Z3tvYkwAzHE](https://www.youtube.com/watch?v=Z3tvYkwAzHE) | Claude Opus 5.5 Edited This ENTIRE Video In ONE SHOT | — | O | Rough cut → Remotion → independent QA → sound |
| [rjLuHtvrmMo](https://www.youtube.com/watch?v=rjLuHtvrmMo) | How I Fully Automated Video Editing with Claude Opus 5.5 | — | O* | WhisperX timing and layered Vox-style graphics |
| [6_rCyryA6hg](https://www.youtube.com/watch?v=6_rCyryA6hg) | Claude Code Can Now Automate Your Videos (Remotion + Opus 5.5) | Roboverse | O | Lower thirds, charts, ads, revision copies |
| [2moKxAZjwCE](https://www.youtube.com/watch?v=2moKxAZjwCE) | How To Create Insane Motion Graphics With Opus 5.5 | Tyler Mommsen | O | Framework selection and detailed creative briefs |
| [AsvN_feasyY](https://www.youtube.com/watch?v=AsvN_feasyY) | How To Make Insane Motion Graphics With Opus 5.5 (Claude Motion) | kaye.creatives | O | Footage overlays and launch-video comparisons |
| [Ll45R_Z8tQc](https://www.youtube.com/watch?v=Ll45R_Z8tQc) | Claude Opus 5.5 Animated Every Motion Graphic in This Video (I Didn't Keyframe a Thing) | — | O | Screenshot/screen-recording animation; CapCut finishing |
| [6Ij9-f2T2Ck](https://www.youtube.com/watch?v=6Ij9-f2T2Ck) | Claude Opus 5.5 Just Solved Motion Graphics (No More AI Slop) | — | O | Reusable morphing B-roll skill |
| [sE9wJRYH-18](https://www.youtube.com/watch?v=sE9wJRYH-18) | I Gave GPT 6.1 Sol and Opus 5.5 the Same 3 Challenges | Mikey Itua | O/S | Paper storyboards → Hyperframes launch videos |
| [q_DKy8BrZhY](https://www.youtube.com/watch?v=q_DKy8BrZhY) | I Tested Claude Fable 5.1 vs. ChatGPT Astra 6 on Real Video Editing | — | O/S/A | Same footage and reusable skill across models |
| [AW3Uku__BBE](https://www.youtube.com/watch?v=AW3Uku__BBE) | Opus 5.5 Is The Best Video Editor I've Ever Used | Paul J Lipsky | O | Borumi MCP, scene-based edits and screen recordings |
| [7jHXoPGnA4c](https://www.youtube.com/watch?v=7jHXoPGnA4c) | Opus 5.5 Just Changed Video Editing Forever (free skills) | — | O | Hyperframes, brand assets and reference-derived skills |
| [oTJGDMKAbH4](https://www.youtube.com/watch?v=oTJGDMKAbH4) | Claude Opus now EDITS my Videos for Social Media (Full Tutorial) | — | O | Beat tables/contact sheets before rendering |
| [EcxvHRccXnc](https://www.youtube.com/watch?v=EcxvHRccXnc) | Level Up Your AI Videos with Claude Opus 5.5 | — | O | Generated footage plus precise coded HUD/text overlays |
| [j8YDz-VC-AM](https://www.youtube.com/watch?v=j8YDz-VC-AM) | Claude Opus 5.5 Is INSANE at Video Editing 0$ (Turned it into a skill) | Jad M.H \| AI Automation | O | Local transcription, measured styles, rejection rules |
| [YLAvsPqC4Ms](https://www.youtube.com/watch?v=YLAvsPqC4Ms) | GPT-6.1 Sol Made This Video | Devsplainers | S | Autonomous educational-video competition |
| [OozE-pGByWg](https://www.youtube.com/watch?v=OozE-pGByWg) | GPT-6.1 Sol Built the Same 3D Scene at Every Effort Level! | Code Bear | S | Procedural underwater CG scene and effort/cost comparison |
| [o3IEkKXXXvo](https://www.youtube.com/watch?v=o3IEkKXXXvo) | GPT-6 Astra Finally Solves AI Video Editing (full guide) | Nate Herk \| AI Automation | A | Transcription, cutting, beat planning, Hyperframes QA |
| [QwzVmGov9ec](https://www.youtube.com/watch?v=QwzVmGov9ec) | The NEW Way to Edit Videos Using GPT-6 Astra \| Full Guide | — | A | Timestamped feedback and screen-text tracking |
| [MujaqZS9wtM](https://www.youtube.com/watch?v=MujaqZS9wtM) | I Think GPT-6-Astra Just Changed YouTube | Nick Saraev | A | Reference-image video stylisation through Higgsfield |
| [kOoC3yhUyDQ](https://www.youtube.com/watch?v=kOoC3yhUyDQ) | Did AI Change Editing Forever? (GPT-6 Astra + DaVinci Resolve) | — | A | Commercial/tutorial/trailer production; After Effects compositing |
| [1ji3qE9VY2k](https://www.youtube.com/watch?v=1ji3qE9VY2k) | I Just Gave GPT-6 Astra Video Editing Skills (WILD Results) | — | A | Premiere computer-use skill built through demonstrations |
| [V7CtHz8JFWA](https://www.youtube.com/watch?v=V7CtHz8JFWA) | I Let GPT-6 Astra Edit In DaVinci Resolve MCP | Creator Magic | A | Native MCP rough cut, audio checks and 4K export |

## B) Cross-video technique catalogue

### Pipeline & setup
- Separate model/harness from renderer: Claude Code/Codex directs; Remotion renders React; Hyperframes renders HTML; FFmpeg performs cuts/assembly. Obtain word-level transcription **before** cutting or synchronising graphics. [Z3tvYkwAzHE, o3IEkKXXXvo]
- Alternatives include Borumi’s Settings → AI MCP connection, Resolve 21.1 MCP, or Premiere computer use with accessibility-tree inspection and screenshots. [AW3Uku__BBE, V7CtHz8JFWA, 1ji3qE9VY2k]
- Install Node.js and official Remotion skills, launch Studio, preview locally, then batch-render approved compositions to MP4. The Windows demo also installs Git Bash and restarts after Node installation. [6_rCyryA6hg]

### Briefing/"training guide" structure
- Specify product/audience, story, format, visual style, motion style, sound, quality checks and constraints. Another workflow approves a timestamped **beat table**, then a **contact sheet—one still per beat—before rendering**. [2moKxAZjwCE, oTJGDMKAbH4]
- Supply footage paths, outline/script, clip-placement instructions, brand assets and references; first ask whether everything is clear and accessible. [QwzVmGov9ec]
- Save appearance rules separately from movement rules; maintain reusable templates and update the skill after accepted/rejected edits. Paper storyboards can precede Hyperframes implementation. [Z3tvYkwAzHE, j8YDz-VC-AM, sE9wJRYH-18]

### Cutting talking-heads
- Identify nearby identical/near-identical repeated phrases as retakes; remove the earlier failed version using word timestamps and FFmpeg. Deepgram or ElevenLabs supplies timings; WhisperX is another demonstrated option. [Z3tvYkwAzHE, rjLuHtvrmMo]
- Premiere procedure: generate transcript → filter pauses → delete all → repeat until “no results”; export/read transcript, remove bad takes, then export/reread for coherence. [1ji3qE9VY2k]
- For jump cuts, use an adjustment-layer Transform at approximately 105–110% scale, preserve headroom and reposition vertically so eye lines match across cuts. [1ji3qE9VY2k]

### Captions
- Demonstrated brief: lower-third placement, clear of the face, white words highlighted blue exactly when spoken. Another uses orange keyword emphasis and word-synchronised captions. [o3IEkKXXXvo, MzUV03KouXM]
- Premiere’s text animator supports **object type: word** for sequential word animation; save successful animation/font settings as presets. [1ji3qE9VY2k]

### Motion graphics/animation types
- Morph one persistent object through successive shapes instead of disconnected slides; the demonstrated B-roll skill offers three clips at medium density or four–five across a roughly 33-second clip at heavy density. [6Ij9-f2T2Ck]
- Vox-style parallax brief: independently describe background, midground and foreground; synchronise midground graphics to named spoken words. Refine and save a successful reference recreation as a template. [rjLuHtvrmMo]
- Other concrete treatments: rounded face-cam crops/drop shadows, fanned playing-video cards, liquid-glass backing for legibility, animated bars that switch from brand colours to gray, and word-following zoom/pan tracking. [o3IEkKXXXvo, 7jHXoPGnA4c, 6_rCyryA6hg, QwzVmGov9ec]
- Generate clean footage **without text**, then code exact annotations/HUD overlays. The demonstrated Artlist MCP sequence generates reference images, animates at 1080p, then adds overlays. [EcxvHRccXnc]

### 3D/CGI/Blender
- Procedural CG test: one Python script, no downloaded models/textures; explicitly enumerate modules, lighting, environmental motion and camera requirements. Inspect clay renders and fly-throughs for composition/clipping problems. [OozE-pGByWg]
- Stylisation pipeline: clean source recording → source-derived style image → Genjutsu performance transfer → segment assembly. Make the video authoritative for movements/lip articulation and the image authoritative only for appearance; obtain a credit quote before generation. [MujaqZS9wtM]
- For conventional compositing, Astra writes an After Effects script, renders with alpha, then imports/places the transparent animation over Resolve footage. [kOoC3yhUyDQ]

### Sound design
- Two distinct approaches: code-generate effects from timestamped sound maps, **including deliberate silence**; or select preapproved assets from a dictionary describing sound, use cases and prohibited uses. [MzUV03KouXM, Z3tvYkwAzHE]
- Generate B-roll with “no background music, natural sound only”; add one continuous music bed beneath narration. CapCut finishing uses whoosh/UI/line-draw layers, tail fades, reduced volume and optional reverb strength around 70. [MzUV03KouXM, Ll45R_Z8tQc]

### Verification/QA loops
- Independent reviewer agent checks face-safe regions, overlaps and icon meaning; creator fixes issues, then a fresh reviewer checks again. Finish with audio-level consistency checks. [Z3tvYkwAzHE]
- Preview low-resolution drafts; inspect actual rendered frames and transcript/beat synchronisation. Duplicate versions before revisions and explicitly preserve successful features. [MzUV03KouXM, o3IEkKXXXvo, 6_rCyryA6hg]
- Competition constraints are not production guarantees: Sol received one hour, internet access and $5 OpenRouter allowance; the creator reported no OpenRouter spending and code-generated music/effects. [YLAvsPqC4Ms]

### Failures & fixes
- Parakeet silently omitted 13 seconds, desynchronising later content: add minute-by-minute transcript checks. Creator still sometimes cuts manually and discusses replacing that transcription component. [j8YDz-VC-AM]
- Replace vague “boring” feedback with timestamped actions: outline the prompt, darken surrounding content, draw the outline; increase zoom and pan to track spoken words. [QwzVmGov9ec]
- Generated text became gibberish or changed wording: separate footage generation from coded typography. Residual frame-to-frame overlay wobble remained unresolved in the demonstration. [EcxvHRccXnc]
- Identical briefs produced slideshow-like Sol/Astra results; these are creator-specific comparisons, not proof of universal model rankings. [q_DKy8BrZhY, sE9wJRYH-18]

### Time/cost data points
- Prepared framework: **14m59s** edit; creator estimates **20–30 hours** to build/tune an equivalent system. [Z3tvYkwAzHE]
- Astra/Hyperframes: **49m30s first pass**, but **3–4 hours** including feedback; usage exhaustion required a plan upgrade. [QwzVmGov9ec]
- Resolve: **75 → about 22 minutes** in roughly **30 minutes**; about **one hour before rendering**; a 1.67-second trim alone took nearly two minutes. Premiere: **48 → about 26 minutes**, **56-minute** run, roughly **15%** of the creator’s $100-plan allowance. [V7CtHz8JFWA, 1ji3qE9VY2k]
- Sol CG effort levels cost approximately **$0.65/$0.67/$1.14/$1.07/$3.19**, calculated at API rates with caching—not invoices independently audited. [OozE-pGByWg]

## C) Explicit list of what I could NOT verify

- Both requested search pages returned a **401 error banner plus usable listings**; complete/live YouTube ranking and exhaustive search coverage were not established.
- Exact caption font families, point sizes, hex colours and easing curves were generally **not spoken**; I have not inferred them from unseen visuals.
- No complete, reproducible **Blender-specific editing setup** was established from the selected procedural-CG transcript.
- Several long transcript extractions were truncated; this catalogue uses retrieved passages, not a certified complete transcription of every video.
- On-screen-only prompts, downloadable/private skill contents, actual render quality, invoices and claimed “unlimited/free” operation were not independently verified.
- *rjLuHtvrmMo* names **5.5 in its title but “Opus 5” in narration**; exact run-model identity remains uncertain.
- Excluded as requested: **5UnK3c-nlIs, 5XSwP0DaHF4, dT5-x3u5nCg**. No workspace resources were created.
