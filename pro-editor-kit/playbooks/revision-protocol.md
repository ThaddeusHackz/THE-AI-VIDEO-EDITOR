# Playbook — revisions without regressions

Sources: `QwzVmGov9ec`, `6_rCyryA6hg`, `Z3tvYkwAzHE`, `5XSwP0DaHF4`.

1. **Duplicate before you change.** Copy the composition (`SceneV2`) and keep V1 renderable.
2. **Write the preservation list** ("keep the caption style, the chapter UI and the 0:12 transition").
3. **Feedback grammar:** `MM:SS – element – action – target`. For example: `0:14 – prompt box – outline it, darken everything else 60%, draw the outline over 0.4 s`. Translate vague notes ("boring") into this form before editing.
4. **Stop early:** if the live preview already shows a wrong palette or character, stop the render and correct it.
5. **Show, don't tell:** for spatial notes, attach a still with a drawn correction.
6. **Fresh critic:** after the fixes, a new critic context reviews only the changed ranges (Gemini `start_offset` / `end_offset`), then performs one full pass.
7. Update the skill (visual or sound guide) with every accepted correction so the next edit starts better.
