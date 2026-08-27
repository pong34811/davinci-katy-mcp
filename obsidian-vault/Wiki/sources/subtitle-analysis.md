---
type: source-summary
source: obsidian-vault/Notes/Subtitle Analysis.md
date_ingested: 2026-08-26
tags: [wiki, wiki/source]
---

# Source: Subtitle Analysis

System for reading and analyzing subtitle track 1 from DaVinci Resolve to detect beats for SFX placement.

## Key Facts

- **Pipeline:** Read subtitle → keyword emotion matching → beat identification → beat list generation
- **Emotion keywords (Thai):** surprise (มาจากไหน, ตกใจ), excitement (เย้, สุดยอด), success (สำเร็จ, ได้แล้ว), fail (ล้มเหลว, ผิด), emphasis (ตัวเลข, สถิติ), question (ทำไม, ยังไง), transition (ต่อไป, แล้วก็), closing (ลาก่อน, บาย)
- **Beat taxonomy:** numbers/stats→pop/collect/kaching, surprise→impact/pop, success→sparkle/ding/collect, question→pop/blip, opening/closing→sparkle/whoosh, emphasis→ding/pop, transition→whoosh/rise
- **Scripts:** `analyze_subtitles.py` (read + analyze)

## Related

- [[DaVinci Resolve SFX System]]
- [[SFX Beat Detection]]
