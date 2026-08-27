---
type: source-summary
source: obsidian-vault/Docs/README.md
date_ingested: 2026-08-26
tags: [wiki, wiki/source]
---

# Source: DaVinci Resolve SFX System README

Project documentation for an AI-powered SFX automation system for DaVinci Resolve.

## Key Facts

- **Purpose:** Automated Sound Effects placement for video editing in DaVinci Resolve
- **Pipeline:** Subtitle Read → Emotion Analysis → Beat Detection → SFX Plan → Auto-Placement
- **SFX Library:** 70+ files in `SFX/` at project root (mp3/wav), organized by family (pop, ding, sparkle, whoosh, impact, wrong, collect, etc.)
- **Scripts:** `analyze_subtitles.py` (subtitle reader), `clip_enhancer.py` (main script), `sfx_place.py` (timeline placement), `face_analyzer.py` + `voice_analyzer.py` (emotion analysis)
- **Dependencies:** Python 3.8+, OpenCV, MediaPipe, DaVinci Resolve running
- **Obsidian Plugin:** SFX Manager for in-vault library browsing

## SFX Family → Beat Mapping

| Beat | Families |
|------|----------|
| surprise | pop, impact |
| excitement | sparkle, kaching |
| success | collect, ding |
| fail | wrong, scratch |
| transition | whoosh, rise |
| emphasis | ding, pop |
| closing | sparkle, whoosh |

## Related

- [[DaVinci Resolve SFX System]]
- [[SFX Library]]
