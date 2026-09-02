---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-09-02
---

# Story Arc Analysis

Analyzes subtitle structure to find story arcs and turning points.
Replaces keyword matching with narrative understanding.

## Arc Structure

```
Setup → Build-up → Turning Point → Punchline → Reaction → Resolution
  ↓         ↓           ↓            ↓          ↓          ↓
 neutral  tension    shift        impact     response   calm
```

## Key Principles

1. **Read context window** — always read 3-5 subtitles before/after current one
2. **Punchline ≠ every subtitle** — only the payoff moment needs SFX
3. **Setup rarely needs SFX** — save impact for the reveal
4. **Turning points are gold** — emotional shifts = best SFX moments
5. **Reaction follows punchline** — sometimes the reaction needs SFX more than the punchline itself

## Detection Rules

| Position | Detection | SFX Priority |
|----------|-----------|-------------|
| Setup | Start of video, introducing topic | LOW |
| Build-up | Creating tension, "but", "however" | MEDIUM |
| Turning Point | Emotional shift, "actually", "but" | HIGH |
| Punchline | Short punchy text, "555", "wow" | CRITICAL |
| Reaction | "really?", "what?", responding to surprise | HIGH |
| Resolution | Closing, "bye", "thanks" | MEDIUM |

## Implementation

Located in `scripts/story_arc_analyzer.py` — use `StoryArcAnalyzer.analyze()` for full analysis.

## Subtitle Source

**Primary source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` — SRT file matching the DaVinci Resolve timeline (60fps).

**⚠️ Local SRT files** at the project root (e.g., `subtitle_from_track1.srt`) have WRONG timestamps — they must NOT be used.
