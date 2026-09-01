---
type: index
tags: [wiki, wiki/index]
date_updated: 2026-08-27
---

# Wiki Index

Content catalog for the LLM-maintained wiki. Read this first when answering queries or starting any operation.

## Categories

### core/ — System Foundation
| Page | Description |
|------|-------------|
| [[data-models]] | All enums, dataclasses, and data flow (SFXFile → SFXPlan) |
| [[system-config]] | Configuration: paths, density limits, volume, SFX_FAMILIES, BEAT_TO_SFX |
| [[event-taxonomy]] | Keyword patterns, event→family mapping, format score modifiers |

### subtitle/ — Subtitle Analysis
| Page | Description |
|------|-------------|
| [[beat-detection]] | Two regex systems for finding beats in transcript text |
| [[analysis-pipeline]] | Subtitle → emotion → beat type → SFX suggestion pipeline |

### sfx/ — SFX Library & Intelligence
| Page | Description |
|------|-------------|
| [[library-scanner]] | Scanning, taxonomy classification, caching |
| [[search-engine]] | Fuzzy matching, event search, family filtering |
| [[family-mapping]] | 21 families, actual filenames, BEAT_TO_SFX |
| [[negative-knowledge]] | What NOT to do — hard-won failure patterns |
| [[evaluation-system]] | 6-dimension quality scoring framework |

### video-editing/ — Editing Workflow
| Page | Description |
|------|-------------|
| [[plan-generation]] | Beats → plan JSON with density/spacing/family checks |
| [[placement-engine]] | SFXPlacer: Resolve API bridge, WAV trim, frame placement |
| [[audio-mixing]] | Volume levels, bed types, fade rules by format |

### sources/ — Raw Source Summaries
| Page | Source |
|------|--------|
| [[davinci-resolve-sfx-system-readme]] | Docs/README.md |
| [[sfx-library]] | Notes/SFX Library.md |
| [[emotion-analysis]] | Notes/Emotion Analysis.md |
| [[subtitle-analysis]] | Notes/Subtitle Analysis.md |
| [[adding-sfx-skill]] | .opencode/skills/adding-sfx/SKILL.md |
| [[sfx-review-skill]] | .opencode/skills/sfx-review/SKILL.md |

### entities/ — People, Tools, Organizations
| Page | Type |
|------|------|
| [[DaVinci Resolve SFX System]] | tool |
| [[SFX Library]] | tool |
| [[Emotion Analysis System]] | tool |

### synthesis/ — Cross-Cutting Answers
| Page | Topic |
|------|-------|
| [[End-to-End SFX Workflow]] | Complete agent guide from request to verified placement |
| [[live-sfx-placement-20260828]] | Live placement: เรื่องแปลกของยามะ (9 SFX on Track 2) |

## Reading Order for New Agents

1. [[data-models]] — understand the data types
2. [[system-config]] — know the config and paths
3. [[event-taxonomy]] — how events map to SFX
4. [[family-mapping]] — what SFX files exist
5. [[beat-detection]] — how beats are found
6. [[plan-generation]] — how plans are built
7. [[placement-engine]] — how SFX lands on timeline
8. [[negative-knowledge]] — what NOT to do
9. [[evaluation-system]] — how to score quality
10. [[End-to-End SFX Workflow]] — put it all together

## Stats

- Total sources: 6
- Total entities: 3
- Total concepts: 13 (3 old + 10 new)
- Total synthesis: 1
- Scripts: impact_scorer.py, story_arc_analyzer.py, timing_intelligence.py, sfx_evaluator.py, sfx_audio_analyzer.py
