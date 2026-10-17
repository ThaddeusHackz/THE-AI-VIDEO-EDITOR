# Playbook — viral talking-head reel (9:16, 30–60 s)

Source pattern: `5UnK3c-nlIs` (Opus 5.5 + Remotion) and its cross-checks in [the catalogue](../evidence/youtube-technique-catalogue.md).

## Recipe
1. `autocut` → `captions --preset reel` (≤4 words per page, one accent word, lower half, clear of the face).
2. **Hook (first 2–3 s):** speaker on screen, captions in the lower half, the hook word in the accent colour, one punch-in. No full-screen graphic before 1.5 s.
3. Plan with `templates/planning-board.html`. Target mix for 45 s: ~50% captions, ~20% captions+UI, ~20% half-screen, ~10% full-screen. **Never use the same scene type more than twice in a row.**
4. **Connective tissue:** one recurring UI device (a chapter indicator, progress dots) that returns 2–3 times.
5. Animations follow the four types (text / person / object / graphic) and the **three-object rule**: main object centred, supporting elements on the edges, depth elements around the outside.
6. On-screen UI pop-ups sit in the lower half, and the background behind them **darkens and blurs**.
7. Punch-ins alternate 100% / 112% on every cut (from `cut-plan.json → keep[].zoom`).
8. Sound with `sfx_map`, music bed at −20 dB, then QA.

## Numbers
| Thing | Value |
|---|---|
| Caption size (1080×1920) | 64–80 px, weight 600–800, 2–4 px dark stroke or soft shadow |
| Word pop | 0.12–0.18 s, `EASE.soft`, scale 0.94 → 1 |
| UI pop-up in/out | 0.4 s in (`EASE.out`) / 0.28 s out (`EASE.in`) |
| Graphic density | 1 per 3–5 s |
| Half-screen split | graphic top 50–55%, speaker bottom, face kept clear of the seam |

## Common failures
- Elements too big → shrink 25%. Too many effects → keep one signature effect per video.
- Harsh black, white or red → use `palettes.muted_luxury`.
- Captions covering the face or platform UI → check `safeArea()` and the 9:16 bottom 18%.
