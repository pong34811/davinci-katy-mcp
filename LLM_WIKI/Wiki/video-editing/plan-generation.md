---
type: concept
confidence: high
source_count: 2
tags: [wiki, wiki/concept]
date_updated: 2026-09-02
---

# Plan Generation

Two systems convert beat analysis into executable SFX placement plans: the standalone script (`scripts/generate_sfx_plan.py`) and the engine recommender (`SFXRecommender`).

## Script Path (scripts/generate_sfx_plan.py)

### Input

Beats JSON from `scripts/analyze_subtitles.py` — list of dicts with `start_seconds`, `beat_type`, `sfx_suggestion`, `priority`, `text`. Timestamps are in seconds (60fps timeline).

### Selection Algorithm

```
1. Filter: keep only beats where sfx_suggestion exists AND beat_type != "neutral"
2. Sort: by priority descending, then by timestamp ascending
3. For each candidate:
   a. Check spacing: skip if < 1.0s from any already-selected timestamp
   b. Check family variety: if sfx_suggestion is in last 3 used families → try alternate from BEAT_TO_SFX
   c. Get actual file: look up first existing file in SFX_DIR from SFX_FAMILIES[family]
   d. If file found → add to plan
4. Density cap: max = (duration / 60) × density_per_minute + 1  (talking-head: 4/min)
```

### Validation

- `check_spacing(timestamps, min_spacing)` — warns if any pair < 1.0s apart
- `check_family_repetition(sfx_files, min_distance=3)` — warns if same family appears within 3 positions

### Plan JSON Schema

```json
{
  "format": "talking-head",
  "duration_seconds": 120.0,
  "density_per_minute": 4,
  "sfx_count": 8,
  "sfx": [
    {
      "sfx_file": "Pop - Short 06.mp3",
      "timestamp_seconds": 11.95,
      "duration": 0.5,
      "reason": "emphasis - ตัวเลข 1,649",
      "beat_type": "emphasis",
      "priority": 1
    }
  ]
}
```

## Engine Path (SFXRecommender)

### generate_plan() Flow

```
1. Format detection (or override)
2. Extract events from SRT file content
3. Convert events → beats (with format-specific score modifiers)
4. _select_beats(): density cap + min_spacing enforcement
5. _assign_sfx_for_beat(): SFXSearch by event type, family variety
6. _validate_and_refine_plan(): spacing + family repetition warnings
```

### Key Differences from Script Path

| Aspect | Script Path | Engine Path |
|--------|-------------|-------------|
| File selection | Static SFX_FAMILIES lookup | Dynamic SFXSearch scoring |
| Family variety | Check last 3 | Check last 3 (same) |
| Spacing | 1.0s minimum | 1.0s (0.4s for meme) |
| Density cap | (duration/60) × density + 1 | density_limit.max_per_minute × duration_min |
| Validation | check_spacing + check_family_repetition | _validate_and_refine_plan (same checks + more) |
| Output | plan dict | SFXPlan dataclass |

### Volume and Duration

- Volume: from `SFXFile.target_db` (processed files) or `config.default_volume_db` (-14 dB)
- Duration: `config.default_sting_duration_seconds` (0.5s) or file duration if ≤1.0s
- Record frame: `int(round(beat.timestamp * fps))`  # fps = 60

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Density too low | Single-pass analysis misses beats | Use 3-round analysis (adding-sfx skill) |
| Same family repeated | BEAT_TO_SFX only has 1 option for some beats | Manually alternate in plan |
| File not found | Filename not in SFX_FAMILIES | Scan library first, use actual filenames |
| Spacing too close | Two beats < 1s apart | Drop the lower-priority one |

## Plan Generation Workflow

1. Read subtitles from `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
2. Run `python scripts/analyze_subtitles.py analyze` → produces `scripts/subtitles_beats.json`
3. Run `python scripts/generate_sfx_plan.py` → produces `scripts/plan.json`
4. Plan timestamps are in seconds (60fps timeline)

## Related

- [[subtitle/beat-detection]] — how beats are identified from subtitle text
- [[subtitle/analysis-pipeline]] — the full subtitle → beat → plan flow
- [[family-mapping]] — 21 families and actual filenames
- [[negative-knowledge]] — anti-patterns and when to skip SFX
