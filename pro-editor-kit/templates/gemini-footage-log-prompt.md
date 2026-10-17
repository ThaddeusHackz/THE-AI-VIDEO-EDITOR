Log this footage for an editor. Use timestamps MM:SS.ff everywhere. Return JSON only:
{
  "duration": "MM:SS",
  "speakers": [ { "id": "A", "description": "..." } ],
  "takes": [ { "start": "", "end": "", "text": "", "quality": "keep|retake|flub", "reason": "", "energy": 1-5 } ],
  "best_take_per_line": [ { "line": "script line or paraphrase", "take_start": "", "take_end": "" } ],
  "dead_air": [ { "start": "", "end": "" } ],
  "visual_issues": [ { "t": "", "issue": "soft focus|exposure|framing|eyeline|background distraction", "severity": 1-3 } ],
  "broll_opportunities": [ { "t": "", "spoken_words": "", "idea": "", "animation_type": "text|person|object|graphic" } ],
  "hook_candidates": [ { "start": "", "end": "", "why": "" } ],
  "palette_observed": [ "#hex" ],
  "notes": ""
}
Rules: when the same sentence is attempted more than once, mark earlier attempts "retake" and say why. Do not guess words you cannot hear; write "[inaudible]".
