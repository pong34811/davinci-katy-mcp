---
type: synthesis
tags: [wiki, wiki/synthesis]
date_updated: 2026-09-02
source_count: 31
---

# Wiki Overview

High-level synthesis of everything in the wiki. Updated as sources are ingested and concepts emerge.

## Current State

31 raw sources + 17 misc raw files ingested. 74 wiki pages total: 58 source summaries, 3 entities, 11 concepts, 2 synthesis.

**Sources reorganized into subdomains** (2026-09-02): raw/Wiki/sources/ contains video-editing/, audio/, leadership/, sfx/. 17 additional root-level raw files placed in sources/misc/.

**All source summaries refreshed from raw** (2026-09-02): 21 existing summaries updated to match current raw content. 27 new summaries created from raw files that lacked wiki counterparts. 1 broken wikilink repaired in index.md.

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

1. **Read [[end-to-end-sfx-workflow]] first** — complete step-by-step with MCP calls
2. **Detect format before anything else** — [[event-taxonomy]] rules differ dramatically per format
3. **3 rounds, never 1** — single-pass under-selects (2.5/min vs target 4/min)
4. **Use [[impact-scoring-system]]** — multi-factor scoring replaces simple keyword matching
5. **Apply [[story-arc-analysis]]** — find turning points, not just keywords
6. **Check [[negative-knowledge]]** — failure patterns that override defaults
7. **Apply [[timing-intelligence]]** — precise pre-hit/on-hit/post-hit timing
8. **Verify with [[evaluation-system]]** — 9-dimension scoring after placement
9. **Delta-only review** — use sfx-review skill for improvements, never re-place from scratch
10. **Use SRT file, not local SRT** — `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` is the authoritative subtitle source

## Key Insights

- **Beat detection is the core challenge** — subtitle text + emotion signals → beat → SFX
- **Format determines everything** — talking-head 3–5/min vs game 5–8/min vs meme "no limits"
- **Negative knowledge is critical** — knowing what NOT to do prevents the most common failures
- **3-round analysis is mandatory** — single-pass consistently under-selects
- **Path awareness matters** — SFX files at local SFX/, not C:/Users/warit/Desktop/davinci-katy-mcp/SFX_processed
- **Subtitle source matters** — always use the SRT file from hermes attachments; local SRT files have wrong timestamps
- **Frame rate is 60fps** — all timestamps are in seconds at 60fps

## Categories at a Glance

|| Category | Pages | Purpose |
||----------|-------|---------|
|| sources/ | 58 | Raw source summaries from LLM_WIKI/raw |
|| entities/ | 3 | Tool/entity pages |
|| concepts/ | 11 | Detailed concept pages |
|| synthesis/ | 2 | Cross-cutting workflow guides |
|| core/ | 3 | System foundation |
|| subtitle/ | 2 | Subtitle analysis |
|| sfx/ | 5 | SFX intelligence |
|| video-editing/ | 3 | Plan generation, placement, audio mixing |

## Raw Source Distribution

- **video-editing:** 13 sources (DaVinci Resolve MCP servers, AI control, Higgsfield plugins)
- **audio:** 7 sources (Fairlight workflow, plugins, Skill Soundboard)
- **leadership:** 10 sources (AI skills gap, data analysis, leadership)
- **sfx:** 1 source (SFX library catalog)

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
