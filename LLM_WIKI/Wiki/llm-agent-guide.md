---
type: guide
tags: [wiki, wiki/llm-guide]
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
  - concepts/negative-knowledge.md
---

# LLM Agent Guide

> จ Oneshot reading order สำหรับ LLM agent ที่เข้ามาแก้ไข/วาง SFX
> อ่านตามลิสต์ด้านล่างจากบนลงล่าง เวลาไม่พอมาก comprehension จะดีที่สุด

## Step 1 — ระ ambiente
- [[overview]] : domain, tools, paths สำคัญ
- [[core/system-config]] : density, paths, frame rate

## Step 2 — เข้าใจ metadata และ events
- [[core/data-models]] : Cue, Beat, ImpactScore, Plan
- [[core/event-taxonomy]] : keyword → event → family mapping
- [[subtitle/beat-detection]] : regex + emotion rules
- [[concepts/thai-language-analysis]] : sarcasm, idioms, ภาษาไทยคำ vysokey

## Step 3 — เลือก SFX
- [[sfx/family-mapping]] : 37 families → กา recommendations
- [[sfx/search-engine]] : fuzzy matching
- [[sfx/negative-knowledge]] : ห้ามวางตอนไหน
- [[concepts/impact-scoring-system]] : 7 dimensions
- [[concepts/story-arc-analysis]] : Setup→Build-up→Punchline→Reaction→Resolution

## Step 4 — จังหวะเวลา
- [[concepts/timing-intelligence]] : pre-hit / on-hit / post-hit
- [[concepts/three-round-sfx-analysis]] : pass 1→2→3
- [[concepts/format-specific-sfx-behavior]] : talking-head / game / meme

## Step 5 — วางและตรวจ
- [[video-editing/plan-generation]] : beat → plan.json
- [[video-editing/placement-engine]] : Resolve API bridge
- [[video-editing/audio-mixing]] : ducking, EQ, stereo
- [[sfx/evaluation-system]] : 9-dimension post-check

## Must-know facts
- SRT สำคัญ: `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
- SFX root: `C:\Users\warit\Desktop\davinci-katy-mcp\SFX`
- Timeline: Track 2 = SFX 1
- Density default: ~10–15/min; ใช้ override ได้
- ซ้อน <1s = fail; fail→reaction ติดกัน OK

## Failure modes
อ่าน [[concepts/sfx-selection-negative-knowledge]] ก่อนเลือกไฟล์เสมอ

## Quick actions
- วิเคราะห์ subtitle → [[subtitle/analysis-pipeline]]
- สร้าง plan → [[video-editing/plan-generation]]
- วาง SFX → `davinci-resolve-mcp\venv\Scripts\python.exe scripts\sfx_place.py`
- รีวิวผล → [[sfx/evaluation-system]]
