---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-09-02
---

# Thai Language Analysis

Detects sarcasm, idioms, cultural references, and politeness patterns in Thai subtitles.

## Key Features

| Feature | Detection | Impact on SFX |
|---------|-----------|---------------|
| **Sarcasm** | Praise after negative setup, exaggerated words | +0.2 comedy score, +sarcasm bonus |
| **Idioms** | Fixed expressions (ชิบหายวายวอด, ไม่ว่าไร) | +0.15 emotional intensity |
| **Cultural Refs** | 555+, kra rong, nak ruk | Context-aware SFX selection |
| **Politeness** | Particle analysis (ครับ, ค่ะ, จ้้า) | Tone adjustment |
| **Indirectness** | Questions, "but" markers, sarcasm | Higher impact for indirect beats |

## Sarcasm Patterns

```
Positive words after negative setup = SARCASM
- "แต่เก่งมากเลย" after "ทำผิดมา"
- "ดีว่ะ" with exaggerated tone
- "เยี่ยมเลย" after failure context
```

## Thai Idioms

| Idiom | Meaning | SFX Type |
|-------|---------|----------|
| ชิบหายวายวอด | Disaster, screwed | fail/wrong |
| ไม่ว่าไร | It's okay, no worry | neutral/soft |
| สนุก | Fun, enjoyable | comedy/pop |
| ใจมืดlung | Lost heart, depressed | sad/awkward |

## Cultural References

| Reference | Context | SFX |
|-----------|---------|-----|
| 555+ | Laughter | comedy (pop/blip) |
| kra rong | Tension, nervous | suspense/rise |
| nak ruk | Cute, endearing | sparkle/soft |

## Implementation

Located in `scripts/thai_language_analyzer.py` — use `analyze_thai_text()` for Thai-specific analysis.

## Subtitle Source

**Primary source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` — SRT file matching the DaVinci Resolve timeline (60fps).

**⚠️ Local SRT files** at the project root (e.g., `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`) have WRONG timestamps — they must NOT be used.

## Integration with Impact Scoring

Thai linguistic features are combined with the 7-dimension impact scoring:
- Sarcasm → +comedy score
- High emotional intensity → +emotion score
- Cultural references → +context score
- Indirectness → bonus for punchline detection
