# Visual training guide — <channel / brand name>

> Fill this in once, give it to the model with "analyse this, then turn it into a skill", and reuse it for every edit.
> Structure from `5UnK3c-nlIs`. The more specific you are, the better the edits get. Attach reference images next to each section.

## Part 1 — Captions
- Reference: `refs/captions/*.png` (1–3 stills of the caption style you want)
- Primary font: `<medium sans, e.g. Inter 600>` · Accent font (special words): `<script or serif>`
- Colours: normal words `<#F4F1EA>` · accent words `<#C9A44C>` · stroke/shadow `<…>`
- Position: `<lower half, ~68% from top on 9:16, clear of the face>`
- Effects: `<soft shadow 0 4 16 rgba(0,0,0,.45)>`
- Animation: `<word-by-word pop-up, fade, 0.14 s per word>`
- Words per page: `<1–4>` · Accent words per page: `<1>`
- Examples (write 5 lines exactly as they should look, with *accent* words marked):
  1. `the *one* thing nobody tells you`
- **Hook rules:** speaker always on screen · subtitles in the lower half · highlight the one word that makes viewers keep watching.

## Part 2 — Animations
- Example looks: `refs/anim/white.png`, `refs/anim/cast-shadow.png`, `refs/anim/yellow.png`
- Types and what they look like:
  - **Text-centric:** `<kinetic headline over a soft gradient; one supporting icon>`
  - **Person-centric:** `<cut-out of the speaker / character with labels>`
  - **Object-centric:** `<hero product or object, slow rotation, callouts>`
  - **Graphic-centric:** `<charts, UI mocks, timelines>`
- Background, step by step: `<1. base colour 2. subtle noise 3. vignette 4. one light leak at 10%>`
- **Three-object rule:** ① main object centred ② supporting elements on the edges ③ depth elements around the outside (blurred, low contrast).
- Design basics: palette `<3–5 muted colours>` · fonts as above · corner radius `<24 px>` · shadows `<…>`
- Size rule: design at the size that feels right, then **shrink 25%**.
- Effects budget: `<one signature effect per video>`
- Inspiration board: `refs/inspiration/` (aim for 50–100 UIs, graphs and full scenes)

## Part 3 — On-screen (lower-half) animations
- Reference: `refs/onscreen/*.png`
- Rules: the background behind darkens (−40%) and blurs (8–12 px) · the animation sits in the lower half · 0.4 s in / 0.28 s out
- UI inspiration: `refs/onscreen/ui/`

## Scene types (used by the planning board)
`captions` · `captions_ui` · `half_screen` (animation top / speaker bottom) · `full_screen` · `broll` · `pip` · `split`

## Never
- `<pure black/white/red full frames, more than 2 things moving in the focal area, text on generated footage>`
