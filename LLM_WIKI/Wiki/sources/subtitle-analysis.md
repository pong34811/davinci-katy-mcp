---
type: source-summary
source: C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt
date_ingested: 2026-08-26
tags: [wiki, wiki/source]
---

# Source: Subtitle Analysis

System for reading and analyzing subtitle tracks to detect beats for SFX placement.

**Primary source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` — SRT file with timestamps matching the DaVinci Resolve timeline (60fps).

## Key Facts

- **Pipeline:** Read subtitle (SRT) → emotion keyword matching → beat identification → beat list generation
- **Emotion keywords (Thai):** surprise (มาจากไหน, ตกใจ), excitement (เย้, สุดยอด), success (สำเร็จ, ได้แล้ว), fail (ล้มเหลว, ผิด), emphasis (ตัวเลข, สถิติ), question (ทำไม, ยังไง), transition (ต่อไป, แล้วก็), closing (ลาก่อน, บาย)
- **Beat taxonomy:** numbers/stats→pop/collect/kaching, surprise→impact/pop, success→sparkle/ding/collect, question→pop/blip, opening/closing→sparkle/whoosh, emphasis→ding/pop, transition→whoosh/rise
- **Scripts:** `scripts/analyze_subtitles.py` (read + analyze)
- **Fallback:** DaVinci Resolve `timeline.get_transcript()` — only when SRT is unavailable; timestamps must match

## ⚠️ Local SRT Warning

Local SRT files at the project root (e.g., `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`) **do not have timestamps matching the DaVinci Resolve timeline** — they must NOT be used. Always use the SRT file from `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`.

## Related

- [[davinci-resolve-sfx-system]]
- [[sfx-beat-detection]]
