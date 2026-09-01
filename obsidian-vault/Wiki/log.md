---
type: log
tags: [wiki, wiki/log]
date_updated: 2026-08-27
---

# Wiki Log

Append-only operation log. Each entry: `## [YYYY-MM-DD] operation | Title`

---

## [2026-08-26] setup | Wiki scaffold created

Created Wiki/ directory structure: sources/, entities/, concepts/, synthesis/. Added index.md, log.md, overview.md. Configured attachment folder (assets/) and download hotkey (Ctrl+Shift+D). Created Clippings/ for raw sources.

## [2026-08-26] ingest | DaVinci Resolve SFX System README

Ingested Docs/README.md → created source summary, entity page (davinci-resolve-sfx-system), concept page (sfx-beat-detection). Updated index.md and overview.md.

## [2026-08-26] ingest | SFX Library

Ingested Notes/SFX Library.md → created source summary (sfx-library), updated entity page (sfx-library) with full family catalog and beat mapping.

## [2026-08-26] ingest | Emotion Analysis

Ingested Notes/Emotion Analysis.md → created source summary (emotion-analysis), entity page (emotion-analysis-system) with face/voice signal reference tables.

## [2026-08-26] ingest | Subtitle Analysis

Ingested Notes/Subtitle Analysis.md → created source summary (subtitle-analysis), concept page (subtitle-driven-beat-detection) with keyword categories and beat taxonomy.

## [2026-08-26] ingest | Adding SFX Skill

Ingested .opencode/skills/adding-sfx/SKILL.md → created source summary (adding-sfx-skill), concept page (three-round-sfx-analysis) documenting the mandatory 3-pass workflow.

## [2026-08-26] ingest | SFX Review Skill

Ingested .opencode/skills/sfx-review/SKILL.md → created source summary (sfx-review-skill) documenting the delta-only review approach and impact scoring system.

## [2026-08-26] synthesis | End-to-End SFX Workflow

Created agent-facing synthesis page: complete step-by-step workflow from MCP calls → format detection → 3-round analysis → plan JSON → CLI placement → verification. Includes failure mode reference table.

## [2026-08-26] concept | Format-Specific SFX Behavior

Created concept page documenting distinct rules per format (talking-head, podcast, game, meme, livestream) with density, beat sources, audio mixing, and special exceptions.

## [2026-08-26] concept | SFX Placement Lessons Learned

Created concept page with empirical rules from real sessions: track index variation, sting vs full file, processed ≠ raw, single-pass under-selection, user density overrides.

## [2026-08-27] fix | SFX Engine config path corrected

Fixed sfx_engine/config.py: DEFAULT_SFX_RAW_DIR changed from Z:/SFX to local SFX/ directory. DEFAULT_SFX_PROCESSED_DIR also points to SFX/ (no SFX_processed/ exists on this machine). Both scripts/config.py and sfx_engine/config.py now agree on the correct path.

## [2026-08-27] restructure | Wiki directory reorganized for machine-usability

Created 6 new categories: core/, subtitle/, sfx/, video-editing/, davinci/, examples/. Migrated and expanded wiki from 6 source summaries + 5 concepts to full machine-usable knowledge base.

## [2026-08-27] ingest | Engine code → Wiki (10 new pages)

Ingested all SFX engine source files into wiki:
- core/data-models.md ← models.py (3 enums, 6 dataclasses, data flow)
- core/system-config.md ← config.py (paths, density limits, volume, families)
- core/event-taxonomy.md ← analyzer.py + search.py (keyword patterns, event→family maps)
- subtitle/beat-detection.md ← analyzer.py + analyze_subtitles.py (two regex systems)
- subtitle/analysis-pipeline.md ← analyze_subtitles.py (emotion→beat→SFX pipeline)
- sfx/library-scanner.md ← scanner.py (taxonomy, caching, file parsing)
- sfx/search-engine.md ← search.py (fuzzy matching, event search)
- sfx/family-mapping.md ← scripts/config.py (21 families, BEAT_TO_SFX)
- video-editing/plan-generation.md ← generate_sfx_plan.py + recommender.py
- video-editing/placement-engine.md ← placer.py (Resolve API bridge)
- video-editing/audio-mixing.md ← SKILL.md audio mixing rules
- sfx/negative-knowledge.md ← failure patterns from skills + lessons learned
- sfx/evaluation-system.md ← 6-dimension quality scoring framework

## [2026-08-27] update | Index and overview rewritten

Rewrote index.md with category-based reading order (10-step onboarding path for new agents). Rewrote overview.md with new knowledge graph and category summary table. Total: 13 concepts, 3 entities, 6 sources, 1 synthesis.

## [2026-08-27] enhancement | Impact Scoring System

Created [[impact-scoring-system]] concept with 7-dimension scoring: comedy, emotion, surprise, emphasis, transition, retention, context. Implements [[impact_scorer.py]] with ImpactScorer class.

## [2026-08-27] enhancement | Story Arc Analysis

Created [[story-arc-analysis]] concept with Setup→Build-up→Punchline→Reaction→Resolution structure. Implements [[story_arc_analyzer.py]] with StoryArcAnalyzer class.

## [2026-08-27] enhancement | Timing Intelligence

Created [[timing-intelligence]] concept with pre-hit/on-hit/post-hit timing presets. Implements [[timing_intelligence.py]] with TimingIntelligence class.

## [2026-08-27] enhancement | SFX Evaluation Framework

Created [[sfx-evaluation-framework]] concept with 9-dimension quality scoring. Implements [[sfx_evaluator.py]] with SFXEvaluator class.

## [2026-08-27] enhancement | Negative Knowledge Base

Created [[sfx-selection-negative-knowledge]] concept documenting anti-patterns and when to skip SFX.

## [2026-08-27] enhancement | Thai Language Analysis

Created [[thai-language-analysis]] concept with sarcasm detection, idiom recognition, cultural reference handling. Implements [[thai_language_analyzer.py]] with ThaiLanguageAnalyzer class.

## [2026-08-27] enhancement | Development Progress Documented

Created DEVELOPMENT_PROGRESS.md tracking all work completed for LLM Wiki + Subtitle-to-SFX Intelligence project.

## [2026-08-28] live | SFX Placement — เรื่องแปลกของยามะ (20.4s comedy short)

Read 21 subtitles from live subtitle track 1 in DaVinci Resolve (Project: "เรื่องแปลกของยามะ", Timeline 1, 60fps).
Analyzed beats manually (auto-detection missed 4 comedic beats due to Thai keyword gaps).
Generated 9-point SFX plan: 3× Pop, 2× Whoosh, 2× Bell Ding, 1× Correct Collect, 1× Wrong Answer.
Placed all 9 SFX on Track 2 (SFX 1) via SFXPlacer / Resolve API bridge.
Verified: 9/9 clips confirmed at correct timestamps on timeline.
SFX families used: pop, whoosh, ding, collect, wrong — all from C:\Users\warit\Desktop\davinci-katy-mcp\SFX\.
Plan: plan_live.json | Results: SFX_RESULTS.md | Report: placement_report.json
