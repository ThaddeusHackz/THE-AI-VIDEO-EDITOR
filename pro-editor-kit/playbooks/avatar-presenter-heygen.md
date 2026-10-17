# Playbook — avatar presenter video (HeyGen + HyperFrames), the GPT-6 Astra pattern

Source: `dT5-x3u5nCg`; API facts in [capability delta](../evidence/capability-delta-2026-10-17.md#heygen). Requires the person's **own** avatar and voice clone, or documented consent.

1. **Research and capture:** open each source, screenshot what is actually on screen, and log the URL and capture time.
2. **Script** → split into short segments (one idea, ≤ 12 s each).
3. **Presenter clips:** `POST /v3/videos` per segment (async, then poll). With Avatar V use `engine.type: "avatar_v"` (Digital Twin looks only; preflight `supported_api_engines`; optional `motion_prompt`). With Avatar IV use `expressiveness`. Or use the HeyGen remote MCP.
4. **Edit in HyperFrames:** presenter clips plus captured demos. One composition per act, each with one paused timeline. Use `ProMotion.captionPages` for captions.
5. **Sound:** music carries long moves; clicks on interface changes; short breaks before hits (`sfx_map.py`).
6. **Render, then verify the exported file:** `render_qa.py`; sample frames at every caption page and transition; transcribe the export and diff it against the script; fix clipped titles and SFX that mask words.
7. Disclose that the presenter is an AI avatar and name the tools in the description, as the source video does.
