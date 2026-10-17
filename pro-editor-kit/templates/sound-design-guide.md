# Sound-design guide — <channel / brand name>

> Give this guide plus your SFX folder to the model, then say "turn this into a skill". Structure from `5UnK3c-nlIs`.

## Who you are and the goal
You are the sound designer for `<channel>`. Every sound exists to sell a **motion** on screen.

## Philosophy
Sound follows motion. Less is more. Silence before big moments.

## Families, levels and placement
| Family | Files | When | Where exactly | Level |
|---|---|---|---|---|
| Whooshes | `sfx/whoosh_short.wav`, `whoosh_long.wav`, `whoosh_textured.wav`, … (5) | camera moves, slides, scene changes | loudest point on the cut | −12 to −16 dB |
| Textures | clicks ×3 (short / metallic / retro), UI click / success / fail, sci-fi ×3 | something appears or is pressed | first visible frame | −16 to −20 dB |
| Risers & hits | bass riser, metallic riser, bass hit, heavy hit | build into and drop on reveals | riser ends on the reveal, hit on it | −10 to −14 dB |
| Music | `<track>` | whole video | under the voice, ducked | about −20 dB |

## Per-file notes (description · use for · never use for)
- `whoosh_short.wav` — airy, 0.45 s, peak at 0.12 s · quick slides, punch-ins · never under dialogue onsets
- `<…>`

## Process
1. List every on-screen event with its timestamp.
2. Assign a family and a file to each, rotating variants.
3. Remove anything that stacks or clutters (no more than 3 sounds per second).
4. Mix: voice −14 LUFS integrated, true peak ≤ −1 dBTP.
