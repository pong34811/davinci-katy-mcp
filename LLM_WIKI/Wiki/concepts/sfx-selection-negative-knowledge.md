---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept, sfx, negative-knowledge]
audience: agent
summary: >
  Anti-patterns and hard skip rules for SFX selection.
  Use this page to override default matching whenever a known failure pattern appears.
date_updated: 2026-09-02
---

# SFX Selection Negative Knowledge

Knowledge of what NOT to do when placing SFX. Equally important as positive rules.

## When to Skip SFX

- **Neutral filler** — segments with impact < 0.15
- **Continuous speech** — talking-head segments without emotional peaks
- **Over-saturation** — when density already exceeds format cap
- **Context conflict** — when SFX would compete with important audio
- **Weak reason** — if you can't explain WHY this SFX belongs here, don't place it

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| SFX on every subtitle | Creates audio fatigue, drowns dialogue | Only place on high-impact segments |
| Same family repeated 3+ times | Sounds monotonous, loses impact | Rotate families (pop→ding→sparkle) |
| Loud SFX over speech | Destroys dialogue clarity | Use -16dB or lower for speech-heavy formats |
| Long SFX (>2s) on short segments | Overwhelms the moment | Use stings (0.3-0.6s) for emphasis |
| Ignoring context window | Misses setup→punchline relationships | Always read 3 subtitles before/after |
| Placing on setup, not punchline | Wastes SFX on non-climactic moments | Save impact for the payoff |

## Format-Specific Avoidances

### Talking-Head
- ❌ Don't use whoosh between every sentence
- ❌ Don't use impact sounds during serious explanations
- ❌ Don't exceed 5 SFX/min (target: 4/min)
- ❌ Don't use local SRT files — use `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`

### Podcast
- ❌ Don't use any SFX during dialogue
- ❌ Don't use loud sounds at all
- ❌ Only 1-2 SFX per segment

### Game
- ❌ Don't suppress action SFX (unlike other formats)
- ❌ Don't avoid close-spaced SFX for action pairs
- ✅ Can be more aggressive with density

### Meme
- ❌ Don't be too restrained — sound IS the joke
- ❌ Don't avoid repetition for comedic effect
- ✅ Can break all other rules

## Related

- [[impact-scoring-system]] — when to place vs skip
- [[video-editing/plan-generation]] — density and spacing enforcement
- [[end-to-end-sfx-workflow]] — complete workflow with failure modes
