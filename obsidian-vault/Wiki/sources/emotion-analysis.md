---
type: source-summary
source: obsidian-vault/Notes/Emotion Analysis.md
date_ingested: 2026-08-26
tags: [wiki, wiki/source]
---

# Source: Emotion Analysis

Dual-signal emotion detection system: face (landmarks) + voice (pitch/volume/speed).

## Key Facts

- **Face signals:** mouth_open (>0.3 = surprise), mouth_smile (>0.2 = happiness), brow_raise (>0.3 = surprise/fear), eye_wide (EAR>0.35 = surprise), eye_narrow (EAR<0.2 = anger)
- **Voice signals:** pitch_high (>200Hz = excitement), pitch_low (<100Hz = sadness), volume_high (>-10dB = anger), speed_fast (>5 syllables/s = excitement)
- **Scripts:** `face_analyzer.py`, `voice_analyzer.py`, `emotion_analyzer.py`
- **Integration:** feeds into `subtitle-driven-enhancement` and `adding-sfx` skills

## Related

- [[DaVinci Resolve SFX System]]
- [[SFX Beat Detection]]
