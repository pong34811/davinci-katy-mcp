---
type: concept
confidence: high
source_count: 1
tags:
  - wiki
  - wiki/concept
---

# Timeline Placement Engine

`SFXPlacer` in `src/sfx_engine/placer.py` bridges the recommendation engine with DaVinci Resolve's scripting API. It handles track management, media import, WAV trimming, and frame-accurate placement.

## Workflow

```
find_or_create_sfx_track → ensure_sfx_bin → import_sfx_files → prepare_sting → place_single → verify_placements
```

### 1. Track Management (`find_or_create_sfx_track()`)

- Scans existing audio tracks for one named "SFX" (case-insensitive `in "SFX"`)
- If found, reuses that track index
- If not found, calls `timeline.AddTrack("audio")` and names it "SFX 1"
- Fallback: if `AddTrack` fails, uses the last audio track index
- Returns 1-based track index

### 2. Media Pool (`ensure_sfx_bin()` + `import_sfx_files()`)

- Creates `Master/SFX` folder hierarchy in Media Pool if it doesn't exist
- `import_sfx_files(file_paths)`:
  - Scans existing clips in the SFX bin to build `existing_names` set
  - Filters out already-imported files (dedup by filename)
  - Calls `media_pool.ImportMedia(to_import)` for remaining files
  - Indexes imported clips by both full name and name-without-extension for lookup

### 3. WAV Trimming (`prepare_sting()` + `trim_wav()`)

**Why trim?** DaVinci Resolve's `AppendToTimeline` ignores the `endFrame` parameter for audio clips. The workaround: pre-trim WAV files to the desired sting length externally before importing.

`trim_wav(src_path, dst_path, duration_seconds, fade_out_seconds)`:
- Uses Python `wave` module (stdlib) — 16-bit PCM only
- Reads raw frames, applies linear fade-out (default 30ms) to prevent clicks
- Writes trimmed WAV with original sample rate and channel count
- Returns success/output_path/duration metadata

`prepare_sting()`:
- Only trims WAV files (MP3s pass through unchanged)
- Skips if file is already ≤ 1.2× the target duration (20% tolerance)
- Caches trimmed files (checks for existing `-sting.wav` before re-trimming)

### 4. Frame Calculation

```python
target_frame = start_frame + round(seconds × fps)
```

`start_frame` is the timeline's start offset (usually 0). This converts wall-clock seconds to absolute timeline frames.

### 5. Single Placement (`place_single()`)

Constructs `clip_info` dict for `AppendToTimeline`:

```python
{
    "mediaPoolItem": clip,      # MediaPoolItem from import
    "startFrame": 0,            # always start from beginning
    "endFrame": dur_frames,     # trimmed sting length
    "recordFrame": target_frame,# timeline position
    "trackIndex": track_idx,    # SFX audio track
    "mediaType": 2,             # 2 = audio
}
```

### 6. Batch Execution (`execute_plan()`)

1. `find_or_create_sfx_track()` — setup once
2. Collect all file paths from plan, pre-trim WAVs to sting duration
3. `import_sfx_files()` — batch import all files at once
4. Sort placements by timestamp
5. `place_single()` for each placement
6. Collect results into `PlacementReport`

### 7. Verification (`verify_placements()`)

Reads back all items on the SFX track and validates:
- **Count**: expected vs actual item count
- **Overlaps**: checks if any item starts before the previous one ends
- **Spacing**: flags items < 1.0s apart as "too_close"
- Returns structured report with `items` list and `issues` list

## Data Classes

### PlacementResult

```python
@dataclass
class PlacementResult:
    success: bool
    sfx_filename: str
    target_seconds: float
    target_frame: int
    actual_frame: Optional[int]
    track_index: int
    error: Optional[str]
    clip_name: Optional[str]
```

### PlacementReport

```python
@dataclass
class PlacementReport:
    success: bool
    total_planned: int
    total_placed: int
    total_failed: int
    track_index: int
    fps: float
    results: List[PlacementResult]
    warnings: List[str]
    errors: List[str]
```

## Constants

| Name | Value | Purpose |
|------|-------|---------|
| `DEFAULT_STING_DURATION_SECONDS` | 0.5 | Default trim length for WAV stings |
| `DEFAULT_FADE_OUT_SECONDS` | 0.03 | Linear fade-out to prevent clicks |
| `MEDIA_TYPE_AUDIO` | 2 | Resolve API media type for audio |
| `DEFAULT_SFX_TRACK_NAME` | "SFX 1" | Name for newly created track |
| `SFX_BIN_PATH` | "Master/SFX" | Media Pool folder path |

## Critical Workaround

The entire `trim_wav()` → `prepare_sting()` flow exists because `AppendToTimeline` ignores `endFrame` for audio. Without pre-trimming, every placed SFX would be its full source duration. The plan's `duration_seconds` field reflects the full file length (not the 0.5s sting) so users can manually adjust trim in Resolve if needed.

## Related Pages

- [[plan-generation]] — how the placement plan is generated
- [[analysis-pipeline]] — subtitle → beat → plan flow
- [[beat-detection]] — how beats are identified from text
