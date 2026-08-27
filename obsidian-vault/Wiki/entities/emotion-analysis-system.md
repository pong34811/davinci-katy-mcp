---
type: entity
entity_type: tool
source_count: 1
tags: [wiki, wiki/entity]
date_updated: 2026-08-26
---

# Emotion Analysis System

Dual-signal emotion detection combining face landmarks and voice analysis.

## Components

- **Face Analyzer** — MediaPipe landmarks → mouth/brow/eye measurements → emotion signals
- **Voice Analyzer** — pitch, volume, speed → emotion signals
- **Emotion Analyzer** — merges face + voice results

## Signal Reference

### Face
| Signal | Threshold | Emotion |
|--------|-----------|---------|
| mouth_open | > 0.3 | surprise, excitement |
| mouth_smile | > 0.2 | happiness |
| brow_raise | > 0.3 | surprise, fear |
| eye_wide | EAR > 0.35 | surprise, fear |
| eye_narrow | EAR < 0.2 | anger, suspicion |

### Voice
| Signal | Range | Emotion |
|--------|-------|---------|
| pitch_high | > 200 Hz | excitement, surprise |
| pitch_low | < 100 Hz | sadness, calm |
| volume_high | > -10 dB | anger, excitement |
| speed_fast | > 5 syll/s | excitement, anger |

## Sources

- [[emotion-analysis]]
