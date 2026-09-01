---
type: concept
confidence: high
source_count: 2
tags:
  - wiki
  - wiki/concept
---

# SFX Plan Generation

Two implementations exist: the standalone script's `generate_plan()` and the engine's `SFXRecommender.generate_plan()`. Both take beat data and produce a placement plan, but differ in file selection strategy.

## Standalone Script (`generate_sfx_plan.py`)

`generate_plan(beats, format, sfx_dir)` — static file selection from the local SFX library.

### Selection Algorithm

1. **Filter**: skip neutral beats (beat_type == "neutral")
2. **Sort**: by priority descending, then timestamp ascending
3. **Density cap**: `max_sfx = duration_seconds / 60 × density_per_minute + 1`
4. **Spacing check**: ≥1.0s gap between consecutive SFX (0.4s for meme format)
5. **Family variety**: if beat's suggested family is in the last 3 placed families, try alternate from `BEAT_TO_SFX` mapping
6. **File lookup**: map family name → actual filename from `SFX_FAMILIES` dict (e.g., pop → `Pop - Short 06.mp3`)
7. **Output**: plan JSON with `sfx_file`, `timestamp_seconds`, `duration`, `reason`, `beat_type`, `priority`

### SFX_FAMILIES Mapping

```
pop       → Pop - Short 06.mp3
ding      → Bell - Ding 02.wav
sparkle   → Harp - Sparkle 01.mp3
whoosh    → Whoosh - Clean Fast.mp3
impact    → Impact - Comedy Hit 01.mp3
wrong     → Game - Wrong Answer.mp3
collect   → Game - Correct Collect Answer.mp3
```

### BEAT_TO_SFX Alternates

If the primary family is exhausted (in last 3), the system tries:
- surprise → ding (fallback from pop)
- excitement → ding (fallback from sparkle)
- success → sparkle (fallback from collect)
- fail → impact (fallback from wrong)

## Engine (`SFXRecommender.generate_plan()`)

Lives in `src/sfx_engine/recommender.py`. Uses `SFXSearch` for dynamic file selection instead of static `SFX_FAMILIES`.

### Flow

1. **Format detection**: `analyzer.detect_format()` classifies timeline as talking_head, game, meme, or podcast based on name keywords and duration heuristics.
2. **Event extraction**: `analyzer.analyze_subtitles()` or `analyzer.analyze_transcript()` produces `TimelineEvent` list.
3. **Beat conversion**: `analyzer.find_beats()` applies format-specific score adjustments.
4. **Beat selection** (`_select_beats()`):
   - Density limit from `config.get_density_limit(format)` (e.g., talking_head: 3-5/min, game: 5-8/min)
   - `max_sfx_count = density_limit × duration_minutes`
   - Meme gets relaxed cap (minimum 15)
   - Sort by impact_score descending
   - Enforce min_spacing (default 1.0s, 0.4s for meme)
5. **SFX assignment** (`_assign_sfx_for_beat()`):
   - Searches via `SFXSearch.search_by_event()` excluding recent families
   - Falls back to unfiltered search if no variety available
   - Calculates volume_db from file metadata or config default
   - Calculates duration from file metadata or default sting (0.5s)
6. **Validation** (`_validate_and_refine_plan()`):
   - Spacing violations: gap < min_spacing between consecutive placements
   - Family repetition: same family used consecutively (non-"other")
   - Density warning: exceeds format's max_per_minute

### Plan JSON Schema

```json
{
  "format": "talking_head",
  "duration_seconds": 120.0,
  "density_per_minute": 3.5,
  "sfx_count": 7,
  "sfx": [
    {
      "sfx_file": "Pop - Short 06.mp3",
      "timestamp_seconds": 5.23,
      "duration": 0.5,
      "reason": "Highlight 'wow' (reaction) -> [pop] Pop - Short 06.mp3",
      "beat_type": "reaction",
      "priority": 2
    }
  ],
  "warnings": [],
  "spacing_violations": []
}
```

## Key Differences

| Aspect | Standalone Script | Engine |
|--------|-------------------|--------|
| File selection | Static `SFX_FAMILIES` dict | Dynamic `SFXSearch` with event-type matching |
| Beat priority | Categorical (0/1/2) | Continuous impact_score (0.1–1.0) |
| Density control | Simple `duration/60 × ppm + 1` | Config-based density limits per format |
| Spacing enforcement | Pre-selection filter | Post-selection validation |
| Family variety | Last-3 sliding window | `exclude_families` param in search |

## Output Consumption

The plan JSON feeds into the placement engine:
- Standalone: `python scripts/sfx_place.py --plan plan.json`
- Engine: `SFXPlacer.execute_plan(plan.sfx)` (see [[placement-engine]])

## Related Pages

- [[beat-detection]] — how beats are identified from subtitle text
- [[analysis-pipeline]] — the full subtitle → beat → plan flow
- [[placement-engine]] — how plans execute on the DaVinci Resolve timeline
