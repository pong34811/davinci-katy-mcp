---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-09-02
---

# Format-Specific SFX Behavior

Distinct rules for SFX density, beat sources, and audio mixing per content format.

## Format Comparison

| Format | Density | Beat Source | Special |
|--------|---------|-------------|---------|
| talking-head | 3–5/min | Subtitle transcript (SRT file) | Main format for this project |
| game | 5–8/min | Action/kill/UI events | Boosts ACTION/SUCCESS/FAIL × 1.3 |
| podcast | 1–2/segment | Speech keywords | Suppresses JOKE × 0.4 |
| meme | High | Visual + audio cues | Spacing 0.4s, relaxed density cap |
| livestream | Alert-driven | User interactions | Real-time placement |

## Density Limits

- **talking-head**: 3–5/min (user preference: 4/min) — `max_sfx = duration_seconds / 60 × density_per_minute + 1`
- **game**: 5–8/min
- **podcast**: 1–2/segment (near-silent format)
- **meme**: no hard cap, min 15 SFX

## Audio Mixing

- Volume: -14 dB default
- Bed types: full-bed (continuous), sting (0.5s), accent (short hits)
- Fade rules: 30ms linear fade-out to prevent clicks
- Spacing: ≥1.0s between consecutive SFX (0.4s for meme)

## Special Exceptions

- **Thai comedy**: Requires manual beat detection — auto-detection often misses comedic beats due to Thai keyword gaps
- **Multiple SFX same second**: Allowed for comedy sequences (fail→reaction patterns)
- **SFX stacking <1s**: Fail (except comedy fail→reaction sequences)

## Related

- [[event-taxonomy]] — keyword patterns per format
- [[Wiki/subtitle/beat-detection]] — how beats are identified
- [[Wiki/video-editing/plan-generation]] — density and spacing enforcement
