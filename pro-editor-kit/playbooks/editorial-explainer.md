# Playbook — editorial / documentary explainer (Vox-style, 16:9 or 9:16)

Sources: `5XSwP0DaHF4`, `rjLuHtvrmMo`, `6Ij9-f2T2Ck`, `EcxvHRccXnc`.

1. Transcript → cut → captions (`youtube` preset for 16:9).
2. **Asset sheet before animation.** Have the coding model write one image-model prompt that produces a *visual asset sheet* in the reference style (objects, icons, maps, people, textures), plus separate vertical backgrounds. Generate at 2K or higher. Add real logos and photos as files. Without this step, code-only graphics read as "simplistic".
3. **Three-layer parallax brief** (`rjLuHtvrmMo`): describe the background, midground and foreground separately. Sync midground graphics to **named spoken words** (put them in `scene-plan.lines[].keywords`).
4. **Morph, don't slide** (`6Ij9-f2T2Ck`): one persistent object transforms through the ideas. Density: medium = 3 B-roll morphs per ~33 s, heavy = 4–5.
5. **Type in code, never in generated pixels** (`EcxvHRccXnc`): generate clean footage with no text, then add numbers, labels and HUD text as code.
6. Split screen when the speaker matters: graphics top, head bottom. Desaturate the avatar to sit in the palette.
7. Save a successful recreation of a reference as a **template** and reuse it.
