---
type: index
tags: [wiki, wiki/index]
date_updated: 2026-09-02
---

# Wiki Index

แคตตาลอกเนื้อหาสำหรับวิกิที่ดูแลโดย LLM อ่านที่นี่เป็นอันดับแรกเมื่อตอบคำถามหรือเริ่มการทำงานใดๆ

## หมวดหมู่

### core/ — รากฐานระบบ
|||| Page | Description |
||||------|-------------|
|||| [[data-models]] | Enum, dataclass, และข้อมูลการไหลทั้งหมด (SFXFile → SFXPlan) |
|||| [[system-config]] | การกำหนดค่า: paths, ขีดจำกัดความหนาแน่น, ระดับเสียง, SFX_FAMILIES, BEAT_TO_SFX |
|||| [[event-taxonomy]] | รูปแบบ keyword, การแมป event→family, ตัวแก้ไขคะแนน format |

### subtitle/ — Subtitle Analysis
||| Page | Description |
|||------|-------------|
||| [[Wiki/subtitle/beat-detection]] | Two regex systems for finding beats in transcript text |
||| [[Wiki/subtitle/analysis-pipeline]] | Subtitle → emotion → beat type → SFX suggestion pipeline |

### sfx/ — คลังเสียงและปัญญาประดิษฐ์
|||| Page | Description |
||||------|-------------|
|||| [[library-scanner]] | การสแกน, การจัดจำแนก taxonomy, การแคช |
|||| [[search-engine]] | Fuzzy matching, การค้นหา event, การกรอง family |
|||| [[family-mapping]] | 21 family, ชื่อไฟล์จริง, BEAT_TO_SFX |
|||| [[negative-knowledge]] | สิ่งที่ไม่ควรทำ — รูปแบบความล้มเหลวที่ได้มาอย่างยาก |
|||| [[evaluation-system]] | เฟรมเวิร์คการให้คะแนนคุณภาพ 6 มิติ |

### video-editing/ — การตัดต่อ
|||| Page | Description |
||||------|-------------|
|||| [[Wiki/video-editing/plan-generation]] | Beats → plan JSON พร้อม checks ความหนาแน่น/ช่องว่าง/family |
|||| [[Wiki/video-editing/placement-engine]] | SFXPlacer: Resolve API bridge, ตัด WAV, วางตามเฟรม |

### sources/ — สรุปแหล่งที่มาดิบ
|||| Page | Source |
||||------|--------|
|||| [[davinci-resolve-sfx-system-readme]] | Docs/README.md |
|||| [[sfx-library-catalog]] | แคตตาลอก 73 ไฟล์ SFX (37 family) |
|||| [[emotion-analysis]] | Notes/Emotion Analysis.md |
|||| [[subtitle-analysis]] | C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt |
|||| [[adding-sfx-skill]] | .opencode/skills/adding-sfx/SKILL.md |
|||| [[sfx-review-skill]] | .opencode/skills/sfx-review/SKILL.md |
|||| [[2026-08-15-sfx-skill-v2-plan]] | docs/superpowers/plans/2026-08-15-sfx-skill-v2.md |
|||| [[samuelgursky davinci-resolve-mcp MCP server]] | GitHub: samuelgursky/davinci-resolve-mcp |
|||| [[I Gave Claude Direct Access to DaVinci Resolve]] | wildlion.media experiment |
|||| [[lordhoell davinci-resolve-mcp MCP server]] | GitHub: lordhoell/davinci-resolve-mcp (440+ tools) |
|||| [[Higgsfield Plugins for DaVinci Resolve]] | higgsfield.ai plugins |
|||| [[DaVinci Resolve MCP (viaSocket)]] | viaSocket MCP server |
|||| [[Best Audio & Sound Effects Plugins for DaVinci Resolve (2026)]] | xere.my comparison |
|||| [[DaVinci Resolve Audio Workflow A Practical Guide to Pro Sound]] | sfxengine.com guide |
|||| [[How to Add Sound Effects to DaVinci Resolve]] | sonilo.com guide |
|||| [[How to Create a Sound Effects Library with DaVinci Resolve]] | macsales guide |
|||| [[Skills Analysis]] | trainingindustry.com definition |
|||| [[Skill analysis]] | Talently definition |
|||| [[Discover How To Become An Intentional Leader]] | skills-analysis.com |

### entities/ — บุคคล, เครื่องมือ, องค์กร
|||| Page | Type |
||||------|------|
|||| [[DaVinci Resolve SFX System]] | tool |
|||| [[SFX Library]] | tool |
|||| [[Emotion Analysis System]] | tool |

### synthesis/ — คำตอบข้ามโดเมน
|||| Page | Topic |
||||------|-------|
|||| [[End-to-End SFX Workflow]] | คู่มือ agent ครบวงจรจากคำขอถึงการวางที่ตรวจสอบแล้ว |
|||| [[live-sfx-placement-20260828]] | การวางแบบสด: เรื่องแปลกของยามะ (9 SFX บน Track 2) |

## Concepts

|||| Page | Description |
||||------|-------------|
|||| [[format-specific-sfx-behavior]] | กฎเฉพาะต่อ format |
|||| [[impact-scoring-system]] | เฟรมเวิร์คการให้คะแนน 7 มิติ |
|||| [[sfx-beat-detection]] | ประเภท beat และกฎความหนาแน่น |
|||| [[sfx-evaluation-framework]] | การให้คะแนนคุณภาพ 9 มิติ |
|||| [[sfx-placement-lessons-learned]] | กฎเชิงประจักษ์จากการทำงานจริง |
|||| [[sfx-selection-negative-knowledge]] | Anti-patterns และเมื่อใดควรข้าม SFX |
|||| [[story-arc-analysis]] | Setup→Build-up→Punchline→Reaction→Resolution |
|||| [[subtitle-driven-beat-detection]] | การระบุ beat จาก keyword |
|||| [[thai-language-analysis]] | Sarcasm, idioms, cultural references |
|||| [[three-round-sfx-analysis]] | 3-pass workflow บังคับ |
|||| [[timing-intelligence]] | Pre-hit/on-hit/post-hit timing presets |

## Reading Order for New Agents (ลำดับการอ่านสำหรับ Agent ใหม่)

1. [[data-models]] — เข้าใจชนิดข้อมูล
2. [[system-config]] — รู้จัก config และ paths
3. [[event-taxonomy]] — event map ไปยัง SFX อย่างไร
4. [[family-mapping]] — SFX file มีอะไรบ้าง
5. [[Wiki/subtitle/beat-detection]] — หา beat อย่างไร
6. [[Wiki/video-editing/plan-generation]] — plan สร้างขึ้นอย่างไร
7. [[Wiki/video-editing/placement-engine]] — SFX ลง timeline อย่างไร
8. [[negative-knowledge]] — สิ่งที่ไม่ควรทำ
9. [[evaluation-system]] — ตรวจสอบคุณภาพอย่างไร
10. [[End-to-End SFX Workflow]] — รวมทุกอย่างเข้าด้วยกัน

## Stats (สถิติ)

- รวมแหล่งที่มา: 35 (14 original + 20 new จากการจัดระเบียบ raw folder + SFX library catalog)
- รวม entities: 3
- รวม concepts: 13
- รวม synthesis: 2
- Scripts: sfx_place.py, analyze_subtitles.py, generate_sfx_plan.py, impact_scorer.py, story_arc_analyzer.py, timing_intelligence.py, sfx_evaluator.py, sfx_audio_analyzer.py

## Key Updates (การอัปเดตสำคัญ — 2026-09-02)

- **เปลี่ยนแหล่งที่มา Subtitle**: แหล่งที่มาหลักคือ `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` (SRT file ตรงกับ Resolve timeline) `subtitle_from_track1.srt` local มี timestamp ไม่ถูกต้อง ห้ามใช้
- **โปรเจกต์จัดระเบียบใหม่**: เพิ่ม `.hermes.md`, `AGENTS.md`, `CLAUDE.md` สำหรับ Hermes Agent project structure ไดเรกทอรี `hermes-config/` พร้อม config.yaml, skills-registry.md
- **ติดตั้งสกิลทั้ง 26 ตัว** ใน Hermes skills system (51 builtin + 25 local)
- **วาง SFX 6 ตัว** บน Track 2 (SFX 1) สำหรับหนังสั้นเรื่อง "เรื่องแปลกของยามะ" — ตรวจสอบแล้วผ่าน frame readback
- **จัดระเบียบ raw folder ใหม่**: รวมเอกสารต้นทาง 35 รายการใน `raw/Wiki/sources/` ตามโดเมน (video-editing/, audio/, leadership/, sfx/) รวมบทความ near-duplicate เป็นสรุปเดียว
- **อัปเดต Wiki index**: เพิ่มหน้าแหล่งที่มาใหม่ 15 หน้าใน Wiki/index.md
- **เพิ่มสรุปแหล่งที่มาใหม่**: 17 หน้า Wiki/sources/ ครอบคลุม DaVinci Resolve MCP servers, เครื่องมือ audio, ทักษะ leadership, AI plugins
