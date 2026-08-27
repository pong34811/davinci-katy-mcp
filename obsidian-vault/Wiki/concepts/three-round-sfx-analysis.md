---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-08-26
---

# Three-Round SFX Analysis

Mandatory 3-pass workflow for selecting SFX placements from transcript/subtitle data. Prevents under-selection by separating discovery from curation.

## Rounds

### Round 1 — Structural Scan
- Convert frame cues to seconds
- Divide transcript into sections by topic/mood
- Identify section boundaries (topic changes, mood shifts)
- Output: section map with time range + topic + mood

### Round 2 — Beat Harvesting
- Walk every cue in the transcript
- For each: check text (joke? emphasis? number? reaction?), check context (what came before/after?)
- Record ALL potential beats with: timestamp, raw text, beat type, SFX family, reason
- Output: candidate list (expected to exceed density cap)

### Round 3 — Curation & Selection
Apply 4 filters sequentially:
1. **Density Check** — compare candidate count vs format cap, cut lowest-impact if over
2. **Spacing Check** — enforce ≥1s gap between SFX, keep stronger one if too close
3. **Family Variety** — prevent same-family repetition nearby, swap or cut
4. **Impact Ranking** — rank by audience impact, trim from bottom to cap

Output: final plan list with reasons for every placement

## Why 3 Rounds

Single-pass analysis consistently under-selects SFX (e.g., 5 spots for 120s = 2.5/min when target is 3–5/min). Round 2's generous harvesting ensures no beat is missed; Round 3's filters ensure the final selection is tight and rule-compliant.

## Sources

- [[adding-sfx-skill]]
