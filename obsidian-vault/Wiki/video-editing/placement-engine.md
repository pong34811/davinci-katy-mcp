---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-08-27
---

# Placement Engine

`SFXPlacer` in `davinci-resolve-mcp/src/sfx_engine/placer.py` bridges the recommendation engine with the DaVinci Resolve scripting API. Handles the full lifecycle: track setup → media import → WAV trimming → frame-accurate placement → verification.

## Workflow

```
1. find_or_create_sfx_track()     → track index
2. ensure_sfx_bin()               → Master/SFX folder
3. import_sfx_files(paths)        → dedup + batch import
4. prepare_sting(path, duration)  → pre-trim WAV if needed
5. place_single(path, timestamp)  → AppendToTimeline
6. verify_placements()            → readback + overlap check
```

## Track Management

`find_or_create_sfx_track(track_name="SFX 1")`:
1. Search existing audio tracks for name containing "SFX"
2. If found → return that index
3. If not → `timeline.AddTrack("audio")`, set name, return new index
4. Fallback: use last audio track count if AddTrack fails

**Critical lesson:** Track index is NOT always 2. May be 1, 3, or variable depending on timeline. Always check first.

## Media Pool

`ensure_sfx_bin()`:
- Creates `Master/SFX` folder hierarchy if missing
- Caches reference to avoid repeated lookups

`import_sfx_files(file_paths)`:
- Gets existing clips in SFX bin by name
- Filters out already-imported files (dedup)
- Calls `media_pool.SetCurrentFolder(sfx_bin)` then `ImportMedia(to_import)`
- Indexes imported clips by filename and basename (without extension)

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
seconds_to_frame(seconds) = start_frame + round(seconds * fps)
frame_to_seconds(frame) = (frame - start_frame) / fps
```

- `start_frame` from `timeline.GetStartFrame()` (may be non-zero)
- `fps` from `timeline.GetSetting("timelineFrameRate")`

## Placement

`place_single(sfx_path, timestamp_seconds, ...)`:

```python
clip_info = {
    "mediaPoolItem": clip,           # MediaPoolItem from import
    "startFrame": 0,                 # always from beginning
    "endFrame": max(1, dur_frames),  # pre-trimmed duration
    "recordFrame": target_frame,     # seconds_to_frame(timestamp)
    "trackIndex": track_idx,         # SFX track
    "mediaType": 2,                  # MEDIA_TYPE_AUDIO
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

## Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| DEFAULT_STING_DURATION_SECONDS | 0.5 | Default trim length |
| DEFAULT_FADE_OUT_SECONDS | 0.03 | Click prevention fade |
| MEDIA_TYPE_AUDIO | 2 | Resolve media type constant |
| DEFAULT_SFX_TRACK_NAME | "SFX 1" | Track name to search/create |
| SFX_BIN_PATH | "Master/SFX" | Media Pool bin location |

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `AppendToTimeline` places full file | endFrame ignored for audio | Pre-trim WAV with `trim_wav()` |
| Track index wrong | Timeline has variable tracks | Use `find_or_create_sfx_track()`, don't hardcode |
| Import returns empty | File already in bin | Dedup handled by `import_sfx_files()` |
| Clip not found after import | Filename mismatch | `get_clip_by_name()` tries exact + basename |
| Verification shows 0 items | Wrong track index | Check `verify_placements()` track report |

See also: [[placement-engine]], [[negative-knowledge]], [[audio-mixing]]
