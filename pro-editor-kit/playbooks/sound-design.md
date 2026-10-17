# Playbook — sound design

Sources: `5UnK3c-nlIs` (sound-design training), `dT5-x3u5nCg` (Astra), `MzUV03KouXM` (sound maps, deliberate silence), `Z3tvYkwAzHE` (SFX dictionary with prohibited uses), `Ll45R_Z8tQc` (tail fades, reverb).

## Philosophy: sound follows motion
| Family | Sounds | Placement rule | Level vs voice |
|---|---|---|---|
| Movement | whooshes (short, long, textured) | **Peak on the cut** (start = cut − peak offset) | −12 to −16 dB |
| Texture | clicks, pops, UI click/success/fail, sci-fi ticks | On the **first visible frame** of the element | −16 to −20 dB |
| Anticipation | risers, hits | Riser **ends** on the reveal; hit lands on it | −10 to −14 dB |
| Bed | one continuous music track | Under narration at about −20 dB, side-chain ducked 10–14 dB | — |

## Rules
- Fewer, better: at most 3 SFX per second, never two of the same family within 0.3 s (whoosh) or 0.12 s (texture). `sfx_map.py` enforces both.
- **Silence is a sound:** drop the music for 0.3–0.8 s before the biggest reveal.
- A click lands on every interface change, and music carries the longer moves (Astra).
- Generate B-roll with "no background music, natural sound only", then add your own bed (`MzUV03KouXM`).
- Rotate variants so the same whoosh never repeats back to back.
- Finish: voice −14 LUFS integrated (social), true peak ≤ −1 dBTP. `render_qa.py` checks both.

## Library manifest
Describe your files in `sfx-library.json` (schema: `schemas/sfx-library.schema.json`). For whooshes, give `peak` (the seconds from file start to the loudest point) so cuts land exactly. For risers, give `dur`. Give each sound a description, use cases and **prohibited uses**, the dictionary approach from `Z3tvYkwAzHE`.
