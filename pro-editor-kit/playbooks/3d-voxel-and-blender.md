# Playbook — 3D, voxel and Blender cinematics

Sources: `5XSwP0DaHF4` (voxel zoom, Blender MCP), `OozE-pGByWg` (procedural CG in one script), Google's 3D guide (Three.js / R3F / headless Blender MCP, `.glb` export).
Existing engines: `remotion/src/engine/threeSceneStudio.tsx`, `skills/cinematic-3d-vfx-cgi`, `skills/gemini-4-argon-forensic-atlas/references/blender-mcp-loop.md`.

## Choose the lane
| Need | Lane |
|---|---|
| Stylised 3D graphics synced to VO and re-editable | Remotion + `@remotion/three` (R3F), seeded randomness |
| Voxel / particle "powers of ten" zooms | R3F instanced meshes; camera on an exponential dolly `z = z0 * exp(-k * t)` |
| Textured hero assets, lighting, overnight renders | Blender via MCP (Claude connector + add-on → *Start MCP bridge server*) |
| Specific objects you have only as images | image → upscale → image-to-3D → `.glb` → import |

## Procedural brief (`OozE-pGByWg`)
Write a single script with no downloaded assets, and explicitly list: modules or objects, lighting rig, environmental motion, camera path, duration, fps and output. Review a **clay render** and a fly-through **before** materials.

## Blocking checks before the beauty render
1. **No interpenetration:** in Blender, run a bounding-box overlap check across static meshes (the overlapping-buildings failure in `5XSwP0DaHF4`). Fail the shot on any overlap that wasn't intended.
2. **Physics plausibility:** rockets accelerate along their thrust axis, explosions expand then slow (ease-out), and debris falls with gravity.
3. **Camera:** no clipping through geometry, a 1.5–4 s ease-in-out per move, and the horizon stays level unless the move is motivated.
4. **Determinism:** fixed seeds, fixed sample counts, frame-indexed animation only.
5. Render a 1-fps contact sheet of the clay pass with `render_qa.py --sheet-every 1` and have the critic check composition and clipping.
