---
type: concept
confidence: high
source_count: 2
tags: [wiki, wiki/concept]
date_updated: 2026-09-02
---

# Subtitle-Driven Beat Detection

Identifying SFX placement opportunities by analyzing subtitle text with keyword matching and contextual cues.

## Method

1. Read subtitle from **SRT file** (`C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`) — primary source
2. Match keywords against emotion categories (Thai + English)
3. Detect numbers, dates, percentages for emphasis beats
4. Identify topic transitions and closing segments
5. Score impact level (0-3) per beat
6. Map beat type → SFX family from [[SFX Beat Detection]] taxonomy

## ⚠️ Local SRT Warning

Local SRT files at the project root (e.g., `subtitle_from_track1.srt`) **do not have timestamps matching the DaVinci Resolve timeline**. The authoritative subtitle source is `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`.

## Keyword Categories

| Category | Thai Keywords | English Keywords |
|----------|--------------|-----------------|
| surprise | มาจากไหน, ตกใจ, โอ้โห | wow, omg, surprise |
| excitement | เย้, สุดยอด, เจ๋ง | yay, awesome, amazing |
| success | สำเร็จ, ได้แล้ว, ชนะ | success, win, pass |
| fail | ล้มเหลว, ผิด, ไม่ได้ | fail, wrong, lose |
| emphasis | ตัวเลข, สถิติ, จำนวน | first, second, most |
| transition | ต่อไป, แล้วก็, มาดู | next, then, now |
| closing | ลาก่อน, บาย, ขอบคุณ | bye, see you, thanks |

## Sources

- [[subtitle-analysis]]
- [[sfx-beat-detection]]
