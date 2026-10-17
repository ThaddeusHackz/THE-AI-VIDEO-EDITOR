# Gemini 4 Argon — playbook (eyes and critic)

Full forensic atlas: `skills/gemini-4-argon-forensic-atlas/`. This file adds **ready-to-run usage** and the items in [evidence/capability-delta-2026-10-17.md](../evidence/capability-delta-2026-10-17.md).

## Identity (verified 2026-10-17, [model page](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon))
- Model id **`gemini-4-argon`**, stable. Inputs: text, image, video, audio, PDF. **Output: text only.**
- 1,048,576-token window shared by input, thinking and output. Synchronous output up to 65,536 tokens. Longer decodes need `background: true` plus an explicit higher `max_output_tokens` ([migration guide](https://ai.google.dev/gemini-api/docs/latest-model)).
- `thinking_level`: `low | medium | high` (default `medium`). Supports structured output, function calling, code execution, grounding, URL context and preview computer use. **No Live API, no native image/audio generation, implicit caching only.**
- Introductory pricing through 2026-11-30: $2 / $10 per 1M input/output tokens. After that: $4 / $20.

## Video understanding — the knobs that matter for editors ([video guide](https://ai.google.dev/gemini-api/docs/video-understanding))
| Knob | Use |
|---|---|
| Default sampling **1 fps** | Enough for shot logging. Raise `fps` on a **clip** to judge fast motion, lower it for long static talks |
| `start_offset` / `end_offset` / `fps` (static processing) | Review only the 20 s you changed, at 10–15 fps, instead of re-uploading the whole cut |
| `media_resolution` (global or per part) | Low resolution = 66 tokens/frame versus 258. ~3 h of video at low vs ~1 h at high in a 1M window |
| `processing: "agentic"` (opt-in, GA on Argon 2026-10-13) | Argon navigates the transcript, frames and audio itself. Google claims up to 88% fewer tokens and ~7% higher quality on long-form; short or broad queries can cost more |
| `MM:SS` timestamps in prompts | Ask about specific moments; demand timestamps in every answer |
| Inputs | Files API up to 20 GB (paid). Public YouTube URLs (≤10 per request on 2.5+). No private or unlisted videos |

Exact field placement differs between the Interactions API and `generateContent` (which uses `videoMetadata`). Check the guide before coding.

Minimal `generateContent` call (google-genai Python SDK) reviewing one changed range:
```python
from google import genai
from google.genai import types
client = genai.Client()
video = client.files.upload(file="build/final.mp4")          # wait until ACTIVE before use
resp = client.models.generate_content(
    model="gemini-4-argon",
    contents=[types.Content(parts=[
        types.Part(file_data=types.FileData(file_uri=video.uri, mime_type="video/mp4"),
                   video_metadata=types.VideoMetadata(start_offset="12s", end_offset="34s", fps=10)),
        types.Part(text=open("pro-editor-kit/templates/critic-prompt.md").read()),
    ])],
    config=types.GenerateContentConfig(response_mime_type="application/json"),
)
print(resp.text)
```

## Three jobs to give Argon
1. **Footage log** before cutting → `templates/gemini-footage-log-prompt.md`. Returns JSON with takes, best take per line, dead air, b-roll opportunities and energy curve.
2. **Reference decomposition** → shot list, per-shot camera move, caption style, pacing (cuts/min), palette, SFX moments. Feed the result into `templates/visual-training-guide.md`.
3. **Critic** after every render → `templates/critic-prompt.md` with the contact sheet and MP4 (or only the changed range).

## Generation lives elsewhere in Google's stack
- **Veo 3.1** (`veo-3.1-generate-preview`): native audio, first/last frame, up to 3 reference images, 720p/1080p/4K, +7 s extensions ([Veo](https://ai.google.dev/gemini-api/docs/veo)).
- **Gemini Omni 1.1 Flash** (`gemini-omni-1.1-flash`): conversational video edits, interpolation and extension. `previous_interaction_id` keeps editing context ([Omni](https://ai.google.dev/gemini-api/docs/omni)).
- **Nano Banana 2.1** (`gemini-nano-banana-2.1`): stills, start frames and asset sheets. Panoramic ratios up to 8:1 ([changelog](https://ai.google.dev/gemini-api/docs/changelog)).
- **3D:** Google's 2026-10-13 guide documents Three.js / R3F / WebGPU shaders, screenshot feedback loops and a **headless Blender MCP** with `.glb` export ([guide](https://aistudio.google.com/learn/building-3d-games-and-worlds-with-gemini-4-argon)). Antigravity managed agent id: `antigravity-preview-09-2026`.

## Footguns
- Never let Argon "approve" a render without listing flaws (see critic prompt).
- At 1 fps it can miss 1–3-frame glitches. Use `render_qa.py` for those and a 10–15 fps clip review for motion feel.
- Argon only outputs text. Any claim that it "rendered" something means another tool did the rendering.
