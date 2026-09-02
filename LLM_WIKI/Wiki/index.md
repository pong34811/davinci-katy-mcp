---
type: index
tags: [wiki, wiki/index]
date_updated: 2026-09-02
---

# Wiki Index

Content catalog for the LLM-maintained wiki. Read this first when answering queries or starting any operation.

## Categories

### core/ — System Foundation
||| Page | Description |
|||------|-------------|
||| [[data-models]] | All enums, dataclasses, and data flow (SFXFile → SFXPlan) |
||| [[system-config]] | Configuration: paths, density limits, volume, SFX_FAMILIES, BEAT_TO_SFX |
||| [[event-taxonomy]] | Keyword patterns, event→family mapping, format score modifiers |

### subtitle/ — Subtitle Analysis
||| Page | Description |
|||------|-------------|
||| [[Wiki/subtitle/beat-detection]] | Two regex systems for finding beats in transcript text |
||| [[Wiki/subtitle/analysis-pipeline]] | Subtitle → emotion → beat type → SFX suggestion pipeline |

### sfx/ — SFX Library & Intelligence
||| Page | Description |
|||------|-------------|
||| [[library-scanner]] | Scanning, taxonomy classification, caching |
||| [[search-engine]] | Fuzzy matching, event search, family filtering |
||| [[family-mapping]] | 21 families, actual filenames, BEAT_TO_SFX |
||| [[negative-knowledge]] | What NOT to do — hard-won failure patterns |
||| [[evaluation-system]] | 6-dimension quality scoring framework |

### video-editing/ — Editing Workflow
||| Page | Description |
|||------|-------------|
||| [[Wiki/video-editing/plan-generation]] | Beats → plan JSON with density/spacing/family checks |
||| [[Wiki/video-editing/placement-engine]] | SFXPlacer: Resolve API bridge, WAV trim, frame placement |

### sources/ — Raw Source Summaries
||| Page | Source |
|||------|--------|
||| [[davinci-resolve-sfx-system-readme]] | Docs/README.md |
|||| [[sfx-library-catalog]] | Complete catalog of 73 SFX files (37 families) |
||| [[emotion-analysis]] | Notes/Emotion Analysis.md |
||| [[subtitle-analysis]] | C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt |
||| [[adding-sfx-skill]] | .opencode/skills/adding-sfx/SKILL.md |
||| [[sfx-review-skill]] | .opencode/skills/sfx-review/SKILL.md |
||| [[2026-08-15-sfx-skill-v2-plan]] | docs/superpowers/plans/2026-08-15-sfx-skill-v2.md |
||| [[samuelgursky davinci-resolve-mcp MCP server]] | GitHub: samuelgursky/davinci-resolve-mcp |
||| [[I Gave Claude Direct Access to DaVinci Resolve]] | wildlion.media experiment |
||| [[lordhoell davinci-resolve-mcp MCP server]] | GitHub: lordhoell/davinci-resolve-mcp (440+ tools) |
||| [[Higgsfield Plugins for DaVinci Resolve]] | higgsfield.ai plugins |
||| [[DaVinci Resolve MCP (viaSocket)]] | viaSocket MCP server |
||| [[Best Audio & Sound Effects Plugins for DaVinci Resolve (2026)]] | xere.my comparison |
||| [[DaVinci Resolve Audio Workflow A Practical Guide to Pro Sound]] | sfxengine.com guide |
||| [[How to Add Sound Effects to DaVinci Resolve]] | sonilo.com guide |
||| [[How to Create a Sound Effects Library with DaVinci Resolve]] | macsales guide |
||| [[Skills Analysis]] | trainingindustry.com definition |
||| [[Skill analysis]] | Talently definition |
||| [[Discover How To Become An Intentional Leader]] | skills-analysis.com |

### entities/ — People, Tools, Organizations
||| Page | Type |
|||------|------|
||| [[DaVinci Resolve SFX System]] | tool |
||| [[SFX Library]] | tool |
||| [[Emotion Analysis System]] | tool |

### synthesis/ — Cross-Cutting Answers
||| Page | Topic |
|||------|-------|
||| [[End-to-End SFX Workflow]] | Complete agent guide from request to verified placement |
||| [[live-sfx-placement-20260828]] | Live placement: เรื่องแปลกของยามะ (9 SFX on Track 2) |

## Concepts

||| Page | Description |
|||------|-------------|
||| [[format-specific-sfx-behavior]] | Distinct rules per format |
||| [[impact-scoring-system]] | 7-dimension scoring framework |
||| [[sfx-beat-detection]] | Beat types and density rules |
||| [[sfx-evaluation-framework]] | 9-dimension quality scoring |
||| [[sfx-placement-lessons-learned]] | Empirical rules from real sessions |
||| [[sfx-selection-negative-knowledge]] | Anti-patterns and when to skip SFX |
||| [[story-arc-analysis]] | Setup→Build-up→Punchline→Reaction→Resolution |
||| [[subtitle-driven-beat-detection]] | Keyword-based beat identification |
||| [[thai-language-analysis]] | Sarcasm, idioms, cultural references |
||| [[three-round-sfx-analysis]] | Mandatory 3-pass workflow |
||| [[timing-intelligence]] | Pre-hit/on-hit/post-hit timing presets |

## Reading Order for New Agents

1. [[data-models]] — understand the data types
2. [[system-config]] — know the config and paths
3. [[event-taxonomy]] — how events map to SFX
4. [[family-mapping]] — what SFX files exist
5. [[Wiki/subtitle/beat-detection]] — how beats are found
6. [[Wiki/video-editing/plan-generation]] — how plans are built
7. [[Wiki/video-editing/placement-engine]] — how SFX lands on timeline
8. [[negative-knowledge]] — what NOT to do
9. [[evaluation-system]] — how to score quality
10. [[End-to-End SFX Workflow]] — put it all together

## Stats

- Total sources: 34 (14 original + 20 new from raw folder reorganization)
- Total entities: 3
- Total concepts: 13
- Total synthesis: 2
- Scripts: sfx_place.py, analyze_subtitles.py, generate_sfx_plan.py, impact_scorer.py, story_arc_analyzer.py, timing_intelligence.py, sfx_evaluator.py, sfx_audio_analyzer.py

## Key Updates (2026-09-02)

- **Subtitle source changed**: Primary source is now `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` (SRT file matching Resolve timeline). Local `subtitle_from_track1.srt` has incorrect timestamps and must NOT be used.
- **Project reorganized**: `.hermes.md`, `AGENTS.md`, `CLAUDE.md` added for Hermes Agent project structure. `hermes-config/` directory with config.yaml, skills-registry.md.
- **All 26 project skills installed** in Hermes skills system (51 builtin + 25 local).
- **6 SFX placed** on Track 2 (SFX 1) for the comedy short "เรื่องแปลกของยามะ" — verified via frame readback.
- **LLM_WIKI raw folder reorganized**: All 34 source documents consolidated into `raw/Wiki/sources/` by domain (video-editing/, audio/, leadership/). Near-duplicate articles merged into single authoritative summaries.
- **Wiki index updated**: Added 14 new source pages to Wiki/index.md sources section.
- **New source summaries added**: 16 new Wiki/sources/ pages covering DaVinci Resolve MCP servers, audio tools, leadership skills, and AI plugins.
