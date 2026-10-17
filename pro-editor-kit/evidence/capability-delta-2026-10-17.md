# Capability delta — 2026-10-17

Items that are **publicly documented today but were not found** in the existing atlases (`skills/gemini-4-argon-forensic-atlas`, `skills/higgsfield-forensic-atlas`, `skills/heygen-github-forensic-atlas`, `skills/remotion-github-forensic-atlas`, `docs/forensics/`) when grepped on 2026-10-17. Those files are unchanged. Read this file alongside them.
The full public-docs inventory these items were drawn from is reproduced in the appendix.

## Gemini (Google)
- **Video clipping and custom sampling:** `start_offset`, `end_offset`, `fps` (static processing). Use them to review only a changed range at higher fps. [video guide](https://ai.google.dev/gemini-api/docs/video-understanding)
- **`media_resolution`** global or per part: 66 vs 258 tokens/frame, about 3 h vs 1 h of video per 1M window. [resolution](https://ai.google.dev/gemini-api/docs/generate-content/media-resolution)
- **`gemini-omni-1.1-flash`:** conversational video editing, interpolation, extension, `previous_interaction_id`. 1080p/4K outputs are upscaled. [Omni](https://ai.google.dev/gemini-api/docs/omni)
- **Veo 3.1** `veo-3.1-generate-preview`: first/last frame, ≤3 reference images, 720p/1080p/4K, +7 s extensions up to 20×. [Veo](https://ai.google.dev/gemini-api/docs/veo)
- **Nano Banana 2.1** `gemini-nano-banana-2.1`, GA 2026-10-06: ratios up to 1:8 / 8:1, 1K/2K/4K. [changelog](https://ai.google.dev/gemini-api/docs/changelog)
- **Antigravity managed agent id** `antigravity-preview-09-2026`, configurable to Argon. [migration](https://ai.google.dev/gemini-api/docs/latest-model)
- `gemini-3.8-live` / `-extended-thinking` GA 2026-09-15. Argon itself has no Live API.

## Higgsfield
- **AI Motion Designer** (2026-09-11) and **Faceless Studio** (2026-08-20). [changelog](https://higgsfield.ai/creator-hub/changelog)
- **Draw-to-video:** arrows, numbered actions and inserted product images; 2–3 actions recommended. [guide](https://higgsfield.ai/blog/Turn-Your-Sketch-Into-a-Cinema)
- **DoP advanced params:** 3/5 s duration, seed, steps, Mix, Enhance. [DoP](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-dop)
- **Genjutsu limits:** one 4–30 s source video, ≤30 references, 30+ presets, ≤1080p. Restyle: 20+ styles at 480p/720p/1080p. The official spelling is *Genjutsu*. [spec](https://higgsfield.ai/blog/higgsfield-genjutsu)
- **Katana:** up to five photos, follows shot order, pacing and music cuts; categories Aura Farming / Motion / Clipping. [Katana](https://higgsfield.ai/blog/higgsfield-katana)
- **Automated MCP/CLI/Canvas/Supercomputer generation always spends credits**, even on "Unlimited" manual-web plans. [MCP billing](https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp)
- SDKs `higgsfield-client` (Python) and `@higgsfield/client/v2` (server-side only). [SDK](https://docs.higgsfield.ai/docs/how-to/sdk)
- Credit rules: subscription credits do not roll over; purchased packs expire after 90 days. [credits](https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work)

## HeyGen
- **Avatar V API engine** `engine.type: "avatar_v"` (not "V5"): Digital Twin looks only, `supported_api_engines` preflight, `motion_prompt`, same-group `reference_look_id`, no `expressiveness`. **Avatar IV** (default) supports `expressiveness: low|medium|high`. `/v3/videos` is async, with a 30-minute single-scene limit. [Avatar V](https://developers.heygen.com/avatar-v) · [IV](https://developers.heygen.com/avatar-iv)
- **Remote OAuth MCP** `https://mcp.heygen.com/mcp/v1/` (subscription credits). [MCP](https://developers.heygen.com/mcp/overview)
- **Video translate:** 175+ languages, Speed/Precision modes, `translate_audio_only`, glossary, proofreading. [translate](https://developers.heygen.com/docs/video-translate)
- **HyperFrames v0.8.169** (2026-10-17, macOS-sandbox Chrome fix), **v0.8.168** (distributed 25 fps, 720p/480p downscaled output), **`hyperframes audio`** diagnostics for onsets, peaks, pauses and loudness (2026-10-14). [releases](https://github.com/heygen-com/hyperframes/releases)

## Remotion
- `<Video>` from **`@remotion/media`** (Mediabunny exact-frame extraction): `trimBefore`; **`trimAfter` deprecated**; HLS support. [Video](https://www.remotion.dev/docs/media/video)
- **Effects API:** ordered multipass, custom Canvas2D/WebGL2/WebGPU via `createEffect()`. `@remotion/light-leaks` is deprecated in favour of `@remotion/effects/light-leak`. [effects](https://www.remotion.dev/docs/effects)
- **`@remotion/web-renderer`** stable since 4.0.491 (WebCodecs, no bundling, subset of CSS). [web-renderer](https://www.remotion.dev/docs/web-renderer)
- **4.0.536** (2026-10-16): Studio timeline rolling edits, `Interactive.create()`, `effectsOutputSize`, `Config.setSequenceActivityLimit()`, Lambda webhook-validation helpers. [release](https://github.com/remotion-dev/remotion/releases/tag/v4.0.536)
- Cloud Run is **Alpha / not actively developed**. Prefer Lambda for parallel renders. [Cloud Run](https://www.remotion.dev/docs/cloudrun)

## Editing hosts seen in the wild (not in the repo before)
- **Borumi** via Settings → AI MCP (`AW3Uku__BBE`) · **DaVinci Resolve 21.1 MCP** (`V7CtHz8JFWA`) · **Premiere Pro via computer use** with accessibility-tree inspection (`1ji3qE9VY2k`) · **Deepgram / ElevenLabs** word timings for retake detection (`Z3tvYkwAzHE`).

---

## Appendix — full public-docs inventory (2026-10-17)

# Public-documentation research — 17 October 2026

“Recent” means **19 July–17 October 2026**; Higgsfield’s requested 60-day window starts **18 August**. This is a comparison-ready inventory, not a claim that these features are missing from the repo. Undated documentation was checked as current; vendor performance claims are not independently verified.

## 1. Google Gemini / Veo / Antigravity

### Features, parameters and limits
- **Gemini 4 Argon is documented**, model ID **`gemini-4-argon`**, stable, October 2026. Text/image/video/audio/PDF input; **text output only**. Unified **1,048,576-token input + thinking + output window**; synchronous output maximum **65,536**, long decode up to the remaining context. Supports structured output, function calling, code execution, file/search/Maps grounding, URL context and preview computer use. **No native image/audio generation or Live API; implicit caching only, not explicit caching.** [Model specifications](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)
- **Long-decode controls:** `thinking_level: low|medium|high` (default `medium`); `max_output_tokens` includes thinking. Beyond 65,536, use `background:true` and an explicit higher limit; background alone still defaults to 64K. Responses progress in hops up to 64K. Introductory price through **30 November 2026:** $2 input/$10 output per million tokens; thereafter $4/$20. [Argon migration guide](https://ai.google.dev/gemini-api/docs/latest-model)
- **Video understanding:** default static sampling **1 FPS**; approximately **3 hours at low media resolution or 1 hour at high** for 1M-context models—not an unconditional duration allowance. Frames cost 66 tokens at low resolution versus 258 otherwise; audio approximately 32 tokens/second. Supports audiovisual descriptions, segmentation, questions and `MM:SS` timestamp references. [Video guide, updated 13 October](https://ai.google.dev/gemini-api/docs/video-understanding)
- **Inputs:** Files API **20GB paid/2GB free**; Cloud Storage registration **2GB/file**; inline table says **<100MB**. Public YouTube URLs: free tier **8 hours/day**, Gemini 2.5+ **10 videos/request**; private/unlisted excluded. **Clipping/custom sampling:** Interactions API `processing:{type:"static",start_offset,end_offset,fps}`; these customizations are static-mode only. Do not confuse these with generateContent’s `videoMetadata` spelling. [Video guide](https://ai.google.dev/gemini-api/docs/video-understanding)
- **Agentic video:** opt-in `processing:"agentic"` dynamically examines transcripts, frames and audio. Google claims **up to 88% fewer tokens** and approximately **7% higher quality** on long-form content; short/broad queries may cost more due to navigation. Per-item resolution controls can coexist with processing mode; generateContent additionally supports global/per-part `media_resolution`. [Processing modes](https://ai.google.dev/gemini-api/docs/video-understanding#agentic-video-understanding), [resolution controls](https://ai.google.dev/gemini-api/docs/generate-content/media-resolution)
- **Generation is separate from Argon:** `gemini-omni-1.1-flash` supports audiovisual generation, conversational video edits, interpolation and extension; `previous_interaction_id` retains editing context. Resolution options: 360p/720p/1080p/4K, with **1080p/4K upscaled**. [Omni guide](https://ai.google.dev/gemini-api/docs/omni)
- **Veo 3.1:** `veo-3.1-generate-preview`; native audio, portrait/landscape, first/last frames, up to **3 reference images**, 720p/1080p/4K. Extension adds seven seconds, up to 20 times; extension availability differs by variant. Image models can supply starting frames. [Veo guide](https://ai.google.dev/gemini-api/docs/veo)
- **3D/Blender:** Google’s **13 October** guide explicitly documents Three.js, React Three Fiber, WebGPU shaders, screenshot feedback, **headless Blender MCP**, Python-generated hero assets and `.glb` export. These are agent/tool workflows, not Argon directly emitting finished meshes. Antigravity managed agent ID: `antigravity-preview-09-2026`, configurable to Argon. [3D workflows](https://aistudio.google.com/learn/building-3d-games-and-worlds-with-gemini-4-argon), [agent integration](https://ai.google.dev/gemini-api/docs/latest-model)

### Recent changes
- **13 October:** Argon GA; agentic video GA on Argon; managed Antigravity support. **6 October:** Nano Banana 2.1 GA, `gemini-nano-banana-2.1`, panoramic ratios through 1:8/8:1 and 1K/2K/4K. **15 September:** `gemini-3.8-live` and `gemini-3.8-live-extended-thinking` GA. **27 August:** Omni 1.1 GA with extension/interpolation/resolution controls. [Release notes](https://ai.google.dev/gemini-api/docs/changelog)

**Not confirmed:** Additional publicly listed Gemini 4-family models beyond Argon; a dedicated Argon video-editor/VFX API or native mesh-output endpoint. [Current model inventory](https://ai.google.dev/gemini-api/docs/models)

## 2. Higgsfield

### Features, parameters and limits
- **Cinema Studio versions:** 2.0 Hero Frame/start-end workflow; 2.5 up to **3 Soul Cast characters** and grading; 3.0 **9 references**, native audio and vendor-claimed physics reasoning; 3.5 AI Director, Elements and collaboration; **4.0 default, 50 references, clips up to 30 seconds**, Director’s Panel and per-shot optics. Current marketing lists six genres; older 3.0 documentation lists seven. [Version guide](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-cinema-studio), [4.0](https://higgsfield.ai/cinematic-video-generator)
- **DoP/Higgsfield Standard:** native image-to-video; camera/VFX preset categories, **Mix** combinations, **Enhance** prompt expansion; advanced **3/5-second duration, seed and steps**. [DoP guide](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-dop)
- **Genjutsu:** Motion Transfer and targeted Object Swap; **one 4–30-second video, up to 30 references, 30+ presets, up to 1080p**, optional prompt. Restyle adds 20+ animation styles and 480p/720p/1080p. Official spelling found is **Genjutsu**, not a separate “Genjitsu” product. [Specifications](https://higgsfield.ai/blog/higgsfield-genjutsu)
- **Katana:** Claude skill through Higgsfield MCP; rebuilds reference edits/presets around **up to five photos**, following shot order, pacing and music cuts; Aura Farming/Motion/Clipping categories. [Katana](https://higgsfield.ai/blog/higgsfield-katana)
- **Supercomputer:** chat-based planning, model routing, generation/assembly, connectors, memory, apps/games/websites and recurring tasks. Other distinct surfaces include **Canvas**, Marketing/Ads Studio, AI Influencer and Faceless Studio. [Tool selector](https://higgsfield.ai/creator-hub/help-center/tools/which-higgsfield-tool-should-i-use), [Supercomputer](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-supercomputer)
- **Soul / Soul 2.0 / Soul Cinema:** presets, Moodboards, Soul HEX palettes and reusable identities. Soul 2.0 reference-image mode disables the prompt field. **Soul ID training: 20–80 photos.** **Popcorn:** manual/automatic consistent storyboards, up to four input images. [Soul](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-soul-to-generate-images), [Soul ID](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character), [Popcorn](https://higgsfield.ai/blog/The-AI-Storyboard-Generator-That-Feels-Like-Directing)
- **Draw-to-video:** arrows, numbered actions and inserted product/object images; vendor recommends **2–3 actions**. **Lipsync Studio/Speak:** image/video talking clips; Audio supplies TTS, voice change, cloning and translation into **18 languages**. [Drawing guide](https://higgsfield.ai/blog/Turn-Your-Sketch-Into-a-Cinema), [audio/lipsync](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-lipsync-voiceover-and-aspect-ratios)
- **Apps/effects inventory:** Recast, Character Swap 2.0, photo/video Face Swap, Commercial Faces, Headshots; Angles 2.0, Shots, Transitions, Expand; Relight, Skin Enhancer, AI Stylist, Outfit Swap; ClipCut, Urban Cuts, video/background removal, Breakdown; Click-to-Ad, billboard/truck/bullet-time ads; 3D Rotation/Render/Figure, game styles, memes and viral templates. Upscale includes FLUX 3 video and ByteDance 4K options. [Apps catalog](https://higgsfield.ai/apps), [identity tools](https://higgsfield.ai/apps/face-identity), [changelog](https://higgsfield.ai/creator-hub/changelog)
- **Integration:** OAuth MCP `https://mcp.higgsfield.ai/mcp`; **automated MCP/CLI/Canvas/Supercomputer generation always spends credits**, irrespective of manual-web Unlimited offers. Separate asynchronous API supports polling/webhooks/cancellation; official SDKs **`higgsfield-client`** and **`@higgsfield/client/v2`**, server-side only. [MCP billing](https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp), [SDKs](https://docs.higgsfield.ai/docs/how-to/sdk)
- **Pricing displayed:** annual-billed monthly equivalents Starter **$19/270 credits**, Plus **$47/1,200**, Ultra **$99/3,000**; promotional/model access varies. Subscription credits do not roll over; purchased packs expire after **90 days**. [Pricing](https://higgsfield.ai/pricing), [credit rules](https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work)

### Recent changes
- **12 August:** Cinema Studio 4.0. Within 60 days: **20 August** Faceless Studio; **21 August** Blender plugin plus standalone video Relight/HEX; **1 September** Genjutsu; **4 September** editable **3D Jutsu** scenes; **11 September** AI Motion Designer; **16 September** API; **23 September** Production Skills Bundle; **30 September** Genjutsu Restyle/ChatGPT extension/Ads Studio; **2 October** AI Influencer; **6 October** Ad Multiplier; **8 October** Katana; **15 October** FLUX 3 upscale update/Community; **16 October** Academy course. [Dated changelog](https://higgsfield.ai/creator-hub/changelog)

**Not confirmed:** Exhaustive counts of the changing effects/Apps libraries, universal upload/output limits, or a fixed credit cost valid across models/resolutions. Some tool pages require login.

## 3. HeyGen / `heygen-com`

### Features, parameters and limits
- **Current organization listing: 34 public repositories**, including forks/archives. Inventory: hyperframes; ray; heygen-cli; hyperframes-community-skills; hyperframes-launches; TAVR; live-streamer; hyperframes-modal-template; TransVLM; liveavatar-web-sdk; liveavatar-sales-agent; stripe-projects-templates; liveavatar-agent-skills; liveavatar-gpt-live-demos; liveavatar-hyperframes-demo; SwiftTweaks; hyperframes-vercel-template; liveavatar-starter-livekit-agent-python; hyperframes-cloudflare-template; openclaw-plugin-heygen; skills; auto-model-optim; hyperframes-gemini-agent; n8n-integration-heygen-node; website-to-hyperframes-demo; hyperframes-launch-video; skills-legacy; heygen-stack; posthog; infra_intern_interview; mcp-shrimp-task-manager; posthog-mcp; facedetection-devops; mediadevices. [Page 1](https://github.com/orgs/heygen-com/repositories?type=public), [page 2](https://github.com/orgs/heygen-com/repositories?type=public&page=2)
- **HyperFrames:** deterministic HTML/CSS/media/seekable-animation→MP4; Node **22+**, FFmpeg. CLI: `init`, `preview`, `lint`, `check`, `snapshot`, `render`, `publish`, `doctor`, `add`, `audio`, `cloud render`, `lambda deploy/render/progress`. Packages cover core, engine, producer, Studio/server, player, SDK, shader transitions, AWS Lambda and GCP Cloud Run. **21 published skills**, router plus creation/domain workflows; install `npx skills add heygen-com/hyperframes` or core-only `npx hyperframes skills update`. [README](https://github.com/heygen-com/hyperframes), [packages](https://github.com/heygen-com/hyperframes/tree/main/packages)
- **Avatar V—not “V5” in the API:** `engine.type:"avatar_v"`; eligible Digital Twin looks only, `supported_api_engines` preflight, `motion_prompt`, same-group `reference_look_id`; no `expressiveness`. **Avatar IV** is default, supports arbitrary image animation and `expressiveness:low|medium|high`. `/v3/videos` is asynchronous; single-scene script/audio limit **30 minutes**. [V](https://developers.heygen.com/avatar-v), [IV](https://developers.heygen.com/avatar-iv), [duration](https://developers.heygen.com/generate-avatar-video)
- **Translation:** 175+ languages; Speed/Precision modes, voice preservation, optional `translate_audio_only`, glossary, dynamic duration and proofreading. **Remote OAuth MCP:** `https://mcp.heygen.com/mcp/v1/`, subscription-credit billing. Legacy Python `heygen-mcp` also has public documentation, but is absent from the current 34-repo listing. [Translation](https://developers.heygen.com/docs/video-translate), [current MCP](https://developers.heygen.com/mcp/overview), [legacy](https://github.com/heygen-com/heygen-mcp)
- **Streaming:** legacy `@heygen/streaming-avatar` **2.1.1**, updated 12 May; voice chat, interruptions, LiveKit input. Its repository is **HeyGen-Official**, not heygen-com. Migration points toward **LiveAvatar**; current org provides `@heygen/liveavatar-web-sdk`, voice-chat and background-removal demos. [Legacy package](https://www.npmjs.com/package/@heygen/streaming-avatar), [LiveAvatar](https://github.com/heygen-com/liveavatar-web-sdk)

### Recent changes
- **17 October:** HyperFrames **v0.8.169** fixes agent macOS-sandbox Chrome rendering; **v0.8.168** adds distributed 25 FPS and 720p/480p downscaled output. **14 October:** `hyperframes audio` diagnostics for onsets/peaks/pauses/loudness. [Releases](https://github.com/heygen-com/hyperframes/releases)

**Not confirmed:** A separate “Avatar V5” model identifier or reliable publication dates for the current v3 API/MCP pages.

## 4. Remotion

### Features, parameters and limits
- **Latest observed: 4.0.536, 16 October.** Keep `remotion` and `@remotion/*` versions aligned. [Releases](https://github.com/remotion-dev/remotion/releases)
- **Official Agent Skills:** `npx skills add remotion-dev/skills`; best-practices, create, markup, Studio, render, maps, captions, SaaS, interactivity, docs, upgrade and multimedia skills. [Skills](https://www.remotion.dev/docs/ai/skills)
- **Recommended `<Video>` is from `@remotion/media`**, using Mediabunny exact-frame extraction and buffering. Parameters include `from`, `durationInFrames`, `trimBefore`, playback rate, loop, crop ratios, effects, pre/postmount, `onVideoFrame`, audio stream selection and request options; **`trimAfter` deprecated**. HLS supported. [Video API](https://www.remotion.dev/docs/media/video)
- **Motion/3D:** [`@remotion/three`](https://www.remotion.dev/docs/three) integrates R3F, video textures and WebGPU/TSL; [`shapes`](https://www.remotion.dev/docs/shapes)/[`paths`](https://www.remotion.dev/docs/paths) supply vector geometry/morphing; [`transitions`](https://www.remotion.dev/docs/transitions) supplies TransitionSeries; [`captions`](https://www.remotion.dev/docs/captions/api) supplies SRT/TikTok utilities and transcription adapters.
- **Effects:** ordered multipass arrays; custom Canvas2D/WebGL2/WebGPU via `createEffect()`. **`@remotion/light-leaks` deprecated** ahead of v5; migrate to `@remotion/effects/light-leak`, parameters `seed`, `hueShift`, `progress`, `disabled`. [Effects](https://www.remotion.dev/docs/effects), [migration](https://www.remotion.dev/docs/light-leaks/light-leak-effect)
- **Browser rendering:** `@remotion/web-renderer`, stable since **4.0.491**, WebCodecs/Mediabunny, no bundling; only a subset of HTML/CSS. **Lambda:** parallel AWS rendering, 15-minute function timeout and storage/concurrency constraints. **Cloud Run:** explicitly **Alpha/not actively developed**. [Browser](https://www.remotion.dev/docs/web-renderer), [Lambda](https://www.remotion.dev/docs/lambda), [Cloud Run](https://www.remotion.dev/docs/cloudrun)

### Recent changes
- **21 August / 4.0.515:** encoder backpressure, outline effect, captions ESM export. [Release](https://github.com/remotion-dev/remotion/releases/tag/v4.0.515)
- **13 September / 4.0.524:** browser `toneFrequency` pitch-shifting; Mediabunny 1.56.1; Recorder migration. [Release](https://github.com/remotion-dev/remotion/releases/tag/v4.0.524)
- **16 October / 4.0.536:** new Studio timeline/rolling edits, `Interactive.create()`, `effectsOutputSize`, `Config.setSequenceActivityLimit()` and Lambda webhook-validation helpers. [Release](https://github.com/remotion-dev/remotion/releases/tag/v4.0.536)

**Not confirmed:** A separately versioned product officially named “Video v2”; current docs identify the component by package, not that label.
