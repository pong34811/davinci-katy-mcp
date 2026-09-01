---
type: synthesis
title: "Live SFX Placement — เรื่องแปลกของยามะ (2026-08-28)"
tags: [wiki, wiki/synthesis, sfx, live-placement, comedy]
date: 2026-08-28
source: subtitles_live.json, plan_live.json, placement_report.json
---

# Live SFX Placement — เรื่องแปลกของยามะ

## Session
2026-08-28. Read 21 subtitles from live subtitle track 1 in DaVinci Resolve, analyzed beats, generated SFX plan, and placed 9 SFX on the timeline.

## Clip Details
- **Project**: เรื่องแปลกของยามะ
- **Timeline**: Timeline 1 (60fps)
- **Duration**: ~20.4 seconds
- **Format**: Talking-head / comedy short
- **Track 1 (Dialogue)**: 21 subtitle segments
- **Track 2 (SFX 1)**: 9 SFX clips placed

## Narrative Arc
Short workplace comedy: coworkers meet → shake heads at each other → laugh (555+) → hold hands → walk away → nothing happened (comedic anti-climax).

## SFX Plan & Placement
| # | Time (s) | SFX File | Beat Type | Reason |
|---|----------|----------|-----------|--------|
| 1 | 0.65 | Pop - Short 06.mp3 | surprise | เจอเรื่องเเปก (weird thing happened!) |
| 2 | 4.80 | Pop - Short 06.mp3 | question | ที่เแผนกใช่ไหมครับ (is this the department?) |
| 3 | 8.75 | Pop - Short 06.mp3 | surprise | เจอเเผนกอื่น (found other department!) |
| 4 | 11.05 | Whoosh - Clean Fast.mp3 | surprise | โยกหัวใส่กันทุกคน (shaking heads) |
| 5 | 12.77 | Bell - Ding 02.wav | excitement | 555+ (laughter moment) |
| 6 | 14.60 | Game - Correct Collect Answer.mp3 | success | พวกเขาก็จับมือกัน (positive connection) |
| 7 | 15.60 | Whoosh - Clean Fast.mp3 | transition | แล้วก็ (and then... transition) |
| 8 | 16.85 | Game - Wrong Answer.mp3 | fail | ไม่มีอะไรเกิดขึ้นแล้ว (comedic fail) |
| 9 | 19.97 | Bell - Ding 02.wav | excitement | หือ (final laugh punchline) |

## Verification
- **Dry-run**: PASSED (0 errors)
- **Placement**: 9/9 SUCCESS
- **Verify**: All 9 clips confirmed on Track 2 with correct timestamps

## Notes
- Auto-detection missed 4 comedic beats due to Thai keyword gaps in `analyze_subtitles.py` (หัว, 555+, จับมือ, ไม่มีอะไร). Manual beat analysis was used instead.
- Pop used 3× for variety with the same file at different timestamps — acceptable per the comedy format density (6/min).
- SFX families: pop (3), whoosh (2), ding (2), collect (1), wrong (1) — good variety, no single family overused.
