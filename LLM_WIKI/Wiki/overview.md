---
type: synthesis
tags: [wiki, wiki/synthesis]
date_updated: 2026-09-02
source_count: 12
---

# Wiki Overview

High-level synthesis of everything in the wiki. Updated as sources are ingested and concepts emerge.

## Current State

6 original sources + 6 engine code files ingested. 13 concepts, 3 entities, 1 synthesis + 2 live placements. Knowledge base now covers the full pipeline from subtitle analysis through SFX placement with machine-usable structure. Enhanced with impact scoring, story arc analysis, timing intelligence, evaluation framework, and Thai-language-aware comedy beat detection.

**Project reorganized as Hermes Agent project** (2026-09-02): `.hermes.md`, `AGENTS.md`, `CLAUDE.md` added. `hermes-config/` directory. All 26 project skills installed in Hermes skills system.

**Subtitle source switched to SRT file** (2026-09-02): Primary source is `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`. Local `subtitle_from_track1.srt` has incorrect timestamps.

**Live SFX placement verified** (2026-09-02): 6 SFX on Track 2 (SFX 1) for "เรื่องแปลกของยามะ" with frame readback confirmation.

## Domain

DaVinci Resolve SFX automation — AI-powered sound effects placement for video editing, driven by subtitle/transcript analysis.

## Knowledge Graph

```
                    ┌─────────────────────────────┐
                    │  core/                       │
                    │  data-models ← system-config │
                    │       ↑           ↑          │
                    │  event-taxonomy ──┘          │
                    └──────────┬──────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
  ┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
  │ subtitle/     │   │ sfx/          │   │ video-editing/│
  │ beat-detection│   │ family-mapping│   │ plan-gen      │
  │ analysis-pipe │   │ scanner       │   │ placement-eng │
  └───────┬───────┘   │ search-engine │   │ audio-mixing  │
          │           │ neg-knowledge │   └───────┬───────┘
          │           │ eval-system   │           │
          └───────────┼───────────────┼───────────┘
                      │               │
              ┌───────▼───────────────▼───────┐
              │ End-to-End SFX Workflow      │
              │ (synthesis — agent guide)      │
              └───────────────────────────────┘
```

## What Agent Needs to Know

1. **Read [[End-to-End SFX Workflow]] first** — complete step-by-step with MCP calls
2. **Detect format before anything else** — [[event-taxonomy]] rules differ dramatically per format
3. **3 rounds, never 1** — single-pass under-selects (2.5/min vs target 4/min)
4. **Use [[impact-scoring-system]]** — multi-factor scoring replaces simple keyword matching
5. **Apply [[story-arc-analysis]]** — find turning points, not just keywords
6. **Check [[negative-knowledge]]** — failure patterns that override defaults
7. **Apply [[timing-intelligence]]** — precise pre-hit/on-hit/post-hit timing
8. **Verify with [[evaluation-framework]]** — 9-dimension scoring after placement
9. **Delta-only review** — use sfx-review skill for improvements, never re-place from scratch
10. **Use SRT file, not local SRT** — `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` is the authoritative subtitle source

## Key Insights

- **Beat detection is the core challenge** — subtitle text + emotion signals → beat → SFX
- **Format determines everything** — talking-head 3–5/min vs game 5–8/min vs meme "no limits"
- **Negative knowledge is critical** — knowing what NOT to do prevents the most common failures
- **3-round analysis is mandatory** — single-pass consistently under-selects
- **Path awareness matters** — SFX files at local SFX/, not Z:/SFX_processed
- **Subtitle source matters** — always use the SRT file from hermes attachments; local SRT files have wrong timestamps
- **Frame rate is 60fps** — all timestamps are in seconds at 60fps

## Categories at a Glance

|| Category | Pages | Purpose |
||----------|-------|---------|
|| core/ | 3 | System foundation: models, config, taxonomy |
|| subtitle/ | 2 | How beats are detected from transcripts |
|| sfx/ | 5 | Library intelligence, search, families, negatives, evaluation |
|| video-editing/ | 2 | Plan generation, placement |
|| sources/ | 7 | Raw source summaries |
|| entities/ | 3 | Tool/entity pages |
|| synthesis/ | 2 | Cross-cutting workflow guide + live placement |
|| concepts/ | 11 | Detailed concept pages |

## Tools & Scripts

| Tool | Path | Purpose |
|------|------|---------|
| sfx_place.py | scripts/sfx_place.py | CLI: load plan, resolve paths, validate, place SFX |
| analyze_subtitles.py | scripts/analyze_subtitles.py | Standalone subtitle → beat analysis |
| generate_sfx_plan.py | scripts/generate_sfx_plan.py | Beat → SFX plan JSON |
| impact_scorer.py | scripts/impact_scorer.py | 7-dimension impact scoring |
| story_arc_analyzer.py | scripts/story_arc_analyzer.py | Story arc structure detection |
| timing_intelligence.py | scripts/timing_intelligence.py | Pre-hit/on-hit/post-hit timing |
| sfx_evaluator.py | scripts/sfx_evaluator.py | 9-dimension quality evaluation |
| sfx_audio_analyzer.py | scripts/sfx_audio_analyzer.py | Audio analysis for SFX |
