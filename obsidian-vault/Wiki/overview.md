---
type: synthesis
tags: [wiki, wiki/synthesis]
date_updated: 2026-08-26
source_count: 6
---

# Wiki Overview

High-level synthesis of everything in the wiki. Updated as sources are ingested and concepts emerge.

## Current State

6 sources, 3 entities, 5 concepts, 1 synthesis page. Knowledge base now covers the full pipeline with agent-facing workflow guide.

## Domain

DaVinci Resolve SFX automation — AI-powered sound effects placement for video editing.

## Knowledge Graph

```
                         ┌──────────────────────────┐
                         │ DaVinci Resolve SFX      │
                         │ System (entity)          │
                         └──────────┬───────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
   ┌────────▼────────┐    ┌────────▼────────┐    ┌────────▼────────┐
   │ SFX Library     │    │ Emotion Analysis│    │ Subtitle        │
   │ (entity)        │    │ System (entity) │    │ Analysis        │
   │ 70+ files       │    │ face + voice    │    │ (source)        │
   └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                         ┌──────────▼───────────────┐
                         │ SFX Beat Detection       │
                         │ (concept)                │
                         └──────────┬───────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
┌────────▼──────────┐    ┌──────────▼──────────┐    ┌─────────▼──────────┐
│ Subtitle-Driven   │    │ Three-Round SFX     │    │ Format-Specific    │
│ Beat Detection    │    │ Analysis            │    │ SFX Behavior       │
│ (concept)         │    │ (concept)           │    │ (concept)          │
└───────────────────┘    └─────────────────────┘    └────────────────────┘
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │ End-to-End SFX Workflow       │
                    │ (synthesis — agent guide)     │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │ SFX Placement Lessons Learned │
                    │ (concept — empirical rules)   │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │ Adding SFX Skill (source)     │
                    │ SFX Review Skill (source)     │
                    └───────────────────────────────┘
```

## What Agent Needs to Know

1. **Read [[End-to-End SFX Workflow]] first** — complete step-by-step with MCP calls
2. **Detect format before anything else** — [[Format-Specific SFX Behavior]] rules differ dramatically
3. **3 rounds, never 1** — [[Three-Round SFX Analysis]] prevents under-selection
4. **Check [[SFX Placement Lessons Learned]]** — empirical rules that override defaults
5. **Delta-only review** — [[SFX Review Skill]] for improvements, never re-place from scratch

## Key Insights

- **Beat detection is the core challenge** — subtitle text + emotion signals → beat → SFX
- **Format determines everything** — talking-head 3–5/min vs game 5–8/min vs meme "no limits"
- **Lessons learned are critical** — track index varies, processed ≠ full file, user may override density
- **3-round analysis is mandatory** — single-pass consistently under-selects (2.5/min vs target 4/min)

## Open Questions

- How to capture per-session lessons learned automatically into the wiki?
- What failure patterns emerge with poor-quality transcripts?
- Can the wiki recommend SFX families based on past session success rates?
