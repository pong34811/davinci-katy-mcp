---
type: synthesis
tags: [wiki, wiki/synthesis]
date_updated: 2026-09-02
---

# End-to-End SFX Workflow

Complete agent-facing guide for adding SFX to a DaVinci Resolve timeline, from request to verified placement.

## Quick Start

```
User: "เพิ่ม SFX ให้คลิปนี้"
  → Agent reads subtitles from SRT file
  → Agent runs 3-round analysis (adding-sfx skill)
  → Agent writes scripts/plan.json
  → CLI: python scripts/sfx_place.py --plan scripts/plan.json --verify
  → Verify: frame readback confirms placement on Track 2
```

## Step-by-Step

### Step 1: Read Subtitles

**Primary source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`

```bash
python scripts/analyze_subtitles.py read
python scripts/analyze_subtitles.py analyze
```

Output: `scripts/subtitles_beats.json` with 17 subtitle items (60fps timeline).

**⚠️ Do NOT use local SRT files** at project root (e.g., `subtitle_from_track1.srt`) — they have wrong timestamps.

### Step 2: Analyze Beats

Beat detection uses two independent systems:
- **System A (Engine):** 7 regex patterns (EMPHASIS, REACTION, JOKE, FAIL, SUCCESS, TRANSITION, DRAMATIC) with impact scores 0.70–0.85
- **System B (Script):** 8 emotion categories (surprise, excitement, success, fail, emphasis, question, transition, closing) with priority 0–2

### Step 3: Generate Plan

```bash
python scripts/generate_sfx_plan.py
```

Output: `scripts/plan.json` with SFX file assignments, timestamps, duration, reason, beat_type, priority.

### Step 4: Place SFX

```bash
python scripts/sfx_place.py --plan scripts/plan.json --verify
```

This connects to DaVinci Resolve, places SFX on Track 2 (SFX 1), and verifies via frame readback.

### Step 5: Review (Delta-Only)

Use the `sfx-review` skill for incremental improvements. Never re-place from scratch.

## 3-Round Analysis (from adding-sfx skill)

| Round | Name | Purpose |
|-------|------|---------|
| 1 | Structural Scan | Identify format, estimate density, scan for obvious beats |
| 2 | Beat Harvesting | Deep keyword scan, emotion detection, number detection |
| 3 | Curation (4 filters) | Dedup, spacing, family variety, density cap |

## Hard Rules

1. No overlapping SFX (<1s) — except comedy fail→reaction sequences
2. No same-family repetition close together
3. Every placement needs a 1-line reason
4. SFX goes on Track 2 (SFX 1) only
5. Use SRT file — not local `subtitle_from_track1.srt`
6. Frame rate is 60fps — timestamps in seconds

## Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Under-selected | Single-pass analysis | Use 3-round workflow |
| Wrong track | Hardcoded track index | Use `find_or_create_sfx_track()` |
| Full file placed | endFrame ignored for audio | Pre-trim WAV with `trim_wav()` |
| Wrong timestamps | Used local SRT file | Always use `Subtitle 1.srt` |
| Missing SFX | File not in SFX_DIR | Scan library first |

## Related

- [[three-round-sfx-analysis]] — the 3-round workflow
- [[Wiki/video-editing/placement-engine]] — how plans execute on timeline
- [[negative-knowledge]] — failure patterns
- [[subtitle-analysis]] — primary subtitle source
