---
type: concept
confidence: high
source_count: 2
tags:
  - wiki
  - wiki/concept
---

# Audio Mixing for SFX Placement

Core principle: **SFX is seasoning, not the main dish.** Bed (main audio) is king.

## Volume Levels by Format

| Format | SFX Level vs Bed | Bed Type |
|---|---|---|
| Talking-head / vlog | −10 to −16 dB | Speech |
| Podcast | lowest (nearly silent) | Speech + music bed |
| Game | louder OK (−8 dB) | Game audio |
| Meme | normal (−10 dB) | None (no dialogue) |
| Livestream | lowest (−14 dB) | Streamer + game + music |

## Bed Types

- **Talking-head**: speech is the bed — SFX must never drown it
- **Podcast**: speech + music bed — SFX needs to be even quieter
- **Game**: game audio is the bed — SFX can be louder since bed masks it
- **Meme**: no dialogue bed — SFX can be at normal level
- **Livestream**: streamer + game + music — SFX must stay below all three, especially alerts

## Fade Rules

- **Short sounds** (pop, ding, plink): fast fade-out, ~30ms
- **Long continuous sounds** (rise, shimmer, whoosh): fade-in/out over a few frames to prevent clicks
- **Processed files** are pre-normalized — use as-is, don't adjust volume manually

## Mixing Checklist

- No clipping or distortion — no SFX should be abnormally loud or soft compared to neighbors
- Bed is clear and dominant — SFX doesn't cover it
- No unnecessary overlaps between SFX
- Final check: bed clear, SFX doesn't cover it, no unnecessary overlaps

## Volume Reference

Processed files encode target volume in the filename: `<shortname>-<dB>.wav` (e.g., `pop-14.wav` = Pop at −14 dB). Use these directly without additional gain adjustment.

## See Also

- [[sfx/negative-knowledge]] — what NOT to do when placing SFX
- [[sfx/evaluation-system]] — quality scoring framework
