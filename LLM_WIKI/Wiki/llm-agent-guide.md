---
type: guide
tags: [wiki, wiki/llm-guide, quickref]
audience: agent
date_updated: 2026-09-05
dependencies:
  - index.md
  - overview.md
  - core/system-config.md
  - core/event-taxonomy.md
  - subtitle/beat-detection.md
  - sfx/family-mapping.md
  - video-editing/plan-generation.md
  - video-editing/placement-engine.md
  - concepts/three-round-sfx-analysis.md
  - concepts/timing-intelligence.md
  - concepts/sfx-selection-negative-knowledge.md
summary: >
  Oneshot reading order + compact reference for SFX placement agents.
  Read top-down when time is limited.
---

# LLM Guide

> Oneshot reading order + compact reference for SFX placement agents.
> Read top-down when time is limited.

## Reading Order

1. [[overview]]
2. [[core/system-config]]
3. [[core/event-taxonomy]]
4. [[subtitle/beat-detection]]
5. [[sfx/family-mapping]]
6. [[concepts/three-round-sfx-analysis]]
7. [[concepts/timing-intelligence]]
8. [[concepts/sfx-selection-negative-knowledge]]
9. [[video-editing/plan-generation]]
10. [[video-editing/placement-engine]]
11. [[sfx/evaluation-system]]
12. [[end-to-end-sfx-workflow]]

## Quick Reference

| Item | Value |
|------|-------|
| SRT | `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` |
| SFX root | `C:\Users\warit\Desktop\davinci-katy-mcp\SFX` |
| Timeline | Track 2 = SFX 1 |
| FPS | 60 |
| Default density | 10–15/min |
| Min gap | 1s between SFX |
| Overlap rule | fail→reaction ติดกัน OK |
| CLI | `davinci-resolve-mcp\venv\Scripts\python.exe scripts\sfx_place.py` |

## Decision Flow

```
read SRT
 → detect format
 → Round 1: section map
 → Round 2: harvest beats
 → Round 3: filter/rank
 → generate plan.json
 → place on Track 2
 → verify
```

## Must-Read Pages by Task

| Task | Page |
|------|------|
| อ่าน subtitle | [[subtitle/analysis-pipeline]] |
| เลือก SFX | [[sfx/family-mapping]], [[sfx/search-engine]] |
| วาง SFX | [[video-editing/placement-engine]] |
| จังหวะเวลา | [[concepts/timing-intelligence]] |
| วิเคราะห์อารมณ์ | [[concepts/thai-language-analysis]] |
| ตรวจคุณภาพ | [[sfx/evaluation-system]] |
| ดูว่าวางผิด où | [[concepts/sfx-selection-negative-knowledge]] |

## Failure Modes

- ซ้อน <1s → fail
- same family ซ้ำใกล้กัน → swap/cut
- local SRT → wrong timestamps, ห้ามใช้
- processed ≠ raw → check path
- single-pass → under-select อยู่ดี

## Tags to Search

- `sfx`, `timing`, `subtitle`, `negative-knowledge`, `thai`, `comedy`
