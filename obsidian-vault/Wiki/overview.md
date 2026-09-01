---
type: synthesis
tags: [wiki, wiki/synthesis]
date_updated: 2026-08-27
source_count: 12
---

# Wiki Overview

High-level synthesis of everything in the wiki. Updated as sources are ingested and concepts emerge.

## Current State

6 original sources + 6 engine code files ingested. 13 concepts, 3 entities, 1 synthesis. Knowledge base now covers the full pipeline from subtitle analysis through SFX placement with machine-usable structure. Enhanced with impact scoring, story arc analysis, timing intelligence, evaluation framework, and Thai-language-aware comedy beat detection.

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
              │ End-to-End SFX Workflow        │
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

## Key Insights

- **Beat detection is the core challenge** — subtitle text + emotion signals → beat → SFX
- **Format determines everything** — talking-head 3–5/min vs game 5–8/min vs meme "no limits"
- **Negative knowledge is critical** — knowing what NOT to do prevents the most common failures
- **3-round analysis is mandatory** — single-pass consistently under-selects
- **Path awareness matters** — SFX files at local SFX/, not Z:/SFX_processed

## Categories at a Glance

| Category | Pages | Purpose |
|----------|-------|---------|
| core/ | 3 | System foundation: models, config, taxonomy |
| subtitle/ | 2 | How beats are detected from transcripts |
| sfx/ | 5 | Library intelligence, search, families, negatives, evaluation |
| video-editing/ | 3 | Plan generation, placement, audio mixing |
| sources/ | 6 | Raw source summaries |
| entities/ | 3 | Tool/entity pages |
| synthesis/ | 1 | Cross-cutting workflow guide |
