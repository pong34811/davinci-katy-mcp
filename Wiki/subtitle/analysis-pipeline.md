---
type: concept
confidence: high
source_count: 2
tags:
  - wiki
  - wiki/concept
---

# Subtitle Analysis Pipeline

Two scripts analyze subtitle tracks and produce beat data for SFX placement. They share the same input (subtitle text + timestamps) but differ in output format and integration path.

## Script Pipeline (`analyze_subtitles.py`)

A standalone CLI tool. Three actions: `read`, `analyze`, `both`.

### Input Sources

- **DaVinci Resolve** (`read_subtitles_from_resolve()`): reads subtitle track 1 via `timeline.GetItemListInTrack("subtitle", 1)`, converts frames to seconds using project FPS.
- **SRT file** (`read_subtitles_from_srt(path)`): parses SubRip format with `HH:MM:SS,mmm --> HH:MM:SS,mmm` timestamps.
- **JSON file**: reads previously exported subtitle dicts.

### Processing

1. `detect_emotion(text)` — substring match against `EMOTION_KEYWORDS` dict (8 emotions × Thai+English keyword lists). Returns list of matched emotions or `["neutral"]`.
2. `detect_numbers(text)` — regex `[\d,]+\.?\d*` extracts numeric values for emphasis detection.
3. `analyze_subtitles(subtitles)` — for each subtitle entry:
   - Runs `detect_emotion()` on text
   - Runs `detect_numbers()` on text
   - Classifies beat type (first matching emotion wins)
   - Maps to SFX suggestion
   - Assigns priority (high=2, medium=1, low=0)
   - Appends emotions, beat_type, sfx_suggestion, priority, numbers to the subtitle dict

### Beat Type → SFX Mapping

| Beat Type | SFX Family | Priority |
|-----------|------------|----------|
| surprise | pop | 2 |
| excitement | sparkle | 2 |
| success | collect | 2 |
| fail | wrong | 2 |
| emphasis | ding | 1 |
| question | pop | 1 |
| transition | whoosh-clean | 1 |
| closing | sparkle | 1 |
| neutral | — | 0 |

### Output Format

```json
{
  "index": 1,
  "start_seconds": 1.234,
  "end_seconds": 3.456,
  "duration_seconds": 2.222,
  "text": "owntown",
  "fps": 30.0,
  "emotions": ["surprise"],
  "beat_type": "surprise",
  "sfx_suggestion": "pop",
  "priority": 2,
  "numbers": []
}
```

## Engine Pipeline (`analyzer.py` + `recommender.py`)

The MCP server's internal path. Used when the `davinci-resolve_sfx` tool calls `plan()`.

### Input Sources

- SRT file content (string or path)
- Transcript dict list (`[{"text": "...", "start": 1.2, "end": 3.4}]`)
- Plain text transcript (estimated 3s per line)

### Processing

1. `EventAnalyzer.analyze_subtitles(srt_content)` — parses SRT, runs `KEYWORD_PATTERNS` regex (7 event types), produces `TimelineEvent` list with positional timestamp estimation.
2. `EventAnalyzer.find_beats(events, content_format)` — converts events to `BeatPoint` objects, applies format-specific score adjustments (podcast suppresses jokes, game boosts actions, meme boosts all).
3. `SFXRecommender.generate_plan()` — takes beats through selection, SFX assignment, and validation (see [[plan-generation]]).

### Key Difference from Script Pipeline

The engine pipeline produces raw `BeatPoint` objects with numeric `impact_score` values (0.1–1.0), not the script's categorical priority levels. The engine handles beat selection and density capping internally.

## Integration with MCP Tools

```
timeline.get_transcript()  →  analyze_subtitles.py  →  JSON beats
                                    ↓
                        sfx(action="plan")  →  SFX plan JSON
                                    ↓
                        python scripts/sfx_place.py --plan plan.json
```

The `sfx` MCP tool's `plan` action uses the engine pipeline internally. The `analyze_subtitles.py` script is for manual/standalone use or custom workflows.

## Priority Scoring

| Level | Value | Beats |
|-------|-------|-------|
| High | 2 | surprise, excitement, success, fail |
| Medium | 1 | emphasis, question, transition, closing |
| Low | 0 | neutral (no SFX suggested) |

High-priority beats always get SFX. Medium beats get SFX if density cap allows. Low/neutral beats are skipped.

## Related Pages

- [[beat-detection]] — the keyword matching systems in detail
- [[plan-generation]] — how beats become an SFX placement plan
- [[placement-engine]] — how plans execute on the DaVinci Resolve timeline
