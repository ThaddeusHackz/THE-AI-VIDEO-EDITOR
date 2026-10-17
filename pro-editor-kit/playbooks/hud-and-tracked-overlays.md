# Playbook — HUD / tracked overlays on live or generated footage

Sources: `5XSwP0DaHF4` (Iron-Man HUD), `EcxvHRccXnc` (coded overlays on generated footage), `QwzVmGov9ec` (word-following zoom/pan), `kOoC3yhUyDQ` (After Effects alpha renders composited in Resolve).

1. **Plate first:** generate or shoot clean footage with **no text** and natural sound only.
2. **Track:** get per-frame anchor points (face or object) from a tracker (OpenCV, MediaPipe, Blender motion tracking or an NLE tracker) into JSON `{frame: [x, y, scale, rotation]}`. Smooth with a 3–5-frame moving average **before** use (this addresses the frame-to-frame wobble left unresolved in `EcxvHRccXnc`).
3. **Perspective:** when panels should angle away from the viewer, **draw the intended trapezoid on a still** and attach it. Verbal descriptions failed repeatedly; the sketch fixed it at once.
4. **Overlay in code:** Remotion `<OffthreadVideo>` plate plus absolutely positioned panels driven by the tracking JSON (CSS `perspective` + `rotateY`), or render the overlay with alpha (ProRes 4444 / WebM VP9 alpha) and composite in the NLE.
5. **Readability:** liquid-glass or dark backing behind text, ≥4.5:1 contrast, and darken the surrounding content when highlighting a UI region (`QwzVmGov9ec`).
6. QA: step through the tracked section at 10–15 fps with the critic and look for drift above 2 px.
