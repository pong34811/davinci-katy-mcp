---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-09-02
---

# Timeline Placement Engine

`SFXPlacer` bridges the recommendation engine with DaVinci Resolve's scripting API. It handles track management, media import, WAV trimming, and frame-accurate placement.

## Workflow

```
1. find_or_create_sfx_track()     → track index (1-based, always Track 2 / "SFX 1")
2. ensure_sfx_bin()               → Master/SFX folder in Media Pool
3. import_sfx_files(paths)         → dedup + batch import
4. prepare_sting(path, duration)  → pre-trim WAV if needed
5. place_single(path, timestamp)  → AppendToTimeline
6. verify_placements()             → readback + overlap check
```

## Track Management

`find_or_create_sfx_track()`:
1. Search existing audio tracks for name containing "SFX"
2. If found → return that index
3. If not → `timeline.AddTrack("audio")`, set name, return new index
4. Fallback: use last audio track count if AddTrack fails

**Note:** SFX always goes on Track 2 (SFX 1) — the only available SFX track.

## Media Pool

`ensure_sfx_bin()`:
- Creates `Master/SFX` folder hierarchy if missing
- Caches reference to avoid repeated lookups

`import_sfx_files(file_paths)`:
- Gets existing clips in SFX bin by name
- Filters out already-imported files (dedup)
- Calls `media_pool.SetCurrentFolder(sfx_bin)` then `ImportMedia(to_import)`
- Indexes imported clips by filename and basename (without extension)
- SFX files are in `C:\Users\warit\Desktop\davinci-katy-mcp\SFX\`

## WAV Trimming (Resolve API Workaround)

**Problem:** DaVinci Resolve's `AppendToTimeline` ignores the `endFrame` parameter for audio clips — places the entire file.

**Solution:** Pre-trim WAV files to sting duration externally using stdlib `wave`.

```python
trim_wav(src_path, dst_path, duration_seconds=0.5, fade_out_seconds=0.03)
```

- Only supports 16-bit PCM WAV (standard for SFX)
- Reads raw frames, applies linear fade-out to prevent clicks
- Writes trimmed file with original sample rate/channels
- MP3 files are NOT trimmed (sent as-is)

### Sting Preparation

`prepare_sting(sfx_path, duration_seconds)`:
1. Only trims WAV files (MP3s pass through)
2. Checks current duration — if already ≤ target × 1.2, use as-is
3. Generates sting path with `-sting.wav` suffix
4. Checks cache (avoids re-trimming)
5. Falls back to original on failure

**User preference note:** Some users prefer full-length files (not stings) so they can trim in Resolve. The plan uses `duration = len(file)` instead of 0.5s sting.

## Frame Calculation

```python
seconds_to_frame(seconds) = start_frame + round(seconds * fps)  # fps = 60
frame_to_seconds(frame) = (frame - start_frame) / fps
```

- `start_frame` from timeline start (usually 0)
- `fps` = 60 (project frame rate)

## Placement

`place_single(sfx_path, timestamp_seconds, ...)`:

```python
clip_info = {
    "mediaPoolItem": clip,           # MediaPoolItem from import
    "startFrame": 0,                  # always from beginning
    "endFrame": max(1, dur_frames),  # pre-trimmed duration
    "recordFrame": target_frame,     # seconds_to_frame(timestamp)
    "trackIndex": track_idx,          # SFX track (2)
    "mediaType": 2,                   # MEDIA_TYPE_AUDIO
}
result = media_pool.AppendToTimeline([clip_info])
```

## Verification

`verify_placements(expected_count)`:
- Reads all items on SFX track via `GetItemListInTrack("audio", track_idx)`
- Checks: item count matches expected, no overlaps, spacing ≥ 1.0s
- Returns structured report with items list and issues list

## execute_plan() Batch Flow

1. Setup track (`find_or_create_sfx_track`)
2. Collect all file paths, prepare stings for WAVs
3. Batch import all files at once (`import_sfx_files`)
4. Place each SFX in timestamp order
5. Return `PlacementReport` with success/fail counts

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

### SFXFile

```python
@dataclass
class SFXFile:
    filename: str
    path: str
    duration: float
    sample_rate: int
    channels: int
    bits_per_sample: int
    volume_db: float
    families: List[str]
    tags: List[str]
    impact_score: float
    source: str
```

## Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| DEFAULT_STING_DURATION_SECONDS | 0.5 | Default trim length |
| DEFAULT_FADE_OUT_SECONDS | 0.03 | Click prevention fade |
| MEDIA_TYPE_AUDIO | 2 | Resolve media type constant |
| DEFAULT_SFX_TRACK_NAME | "SFX 1" | Track name to search/create |
| SFX_BIN_PATH | "Master/SFX" | Media Pool bin location |
| SFX_FAMILIES | dict | 21 families mapped to actual filenames |
| BEAT_TO_SFX | dict | Beat type → alternate SFX family mapping |

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `AppendToTimeline` places full file | endFrame ignored for audio | Pre-trim WAV with `trim_wav()` |
| Track index wrong | Timeline has variable tracks | Use `find_or_create_sfx_track()`, don't hardcode |
| Import returns empty | File already in bin | Dedup handled by `import_sfx_files()` |
| Clip not found after import | Filename mismatch | `get_clip_by_name()` tries exact + basename |
| Verification shows 0 items | Wrong track index | Check `verify_placements()` track report |

## SFX Placement Workflow

1. Read subtitles from `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
2. Analyze beats: `python scripts/analyze_subtitles.py analyze`
3. Generate plan: `python scripts/generate_sfx_plan.py` → `scripts/plan.json`
4. Place SFX: `python scripts/sfx_place.py --plan scripts/plan.json --verify`
5. Verify: frame readback confirms placement on Track 2

## Full SFX Family Catalog (21 families)

| Family | File |
|--------|------|
| pop | Pop - Short 06.mp3 |
| ding | Bell - Ding 02.wav |
| sparkle | Harp - Sparkle 01.mp3 |
| whoosh | Whoosh - Clean Fast.mp3 |
| impact | Impact - Comedy Hit 01.mp3 |
| wrong | Game - Wrong Answer.mp3 |
| collect | Game - Correct Collect Answer.mp3 |

## Related

- [[video-editing/plan-generation]] — how the placement plan is generated
- [[subtitle/analysis-pipeline]] — subtitle → beat → plan flow
- [[subtitle/beat-detection]] — how beats are identified from text
