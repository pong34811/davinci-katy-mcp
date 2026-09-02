---
type: entity
entity_type: tool
source_count: 1
tags: [wiki, wiki/entity]
date_updated: 2026-08-26
---

# DaVinci Resolve SFX System

AI-powered system for automated Sound Effects placement in DaVinci Resolve video editing.

## Components

- **[[sfx-library]]** — 70+ audio files organized by family (pop, ding, sparkle, whoosh, impact, wrong, collect)
- **Subtitle Analyzer** — reads transcript from timeline track 1
- **Emotion Analyzer** — face + voice emotion detection
- **SFX Placer** — CLI tool that places SFX on timeline via Resolve API
- **SFX Manager Plugin** — Obsidian plugin for library browsing

## Pipeline

1. Read subtitle/transcript from DaVinci Resolve
2. Analyze emotions from face + voice
3. Detect beats (punchline, reaction, transition, emphasis)
4. Generate SFX plan (file + timestamp + reason)
5. Place SFX on timeline automatically

## Sources

- [[davinci-resolve-sfx-system-readme]]
