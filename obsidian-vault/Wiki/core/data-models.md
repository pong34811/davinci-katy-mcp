---
type: concept
confidence: high
source_count: 1
date_ingested: 2026-08-27
tags:
  - wiki
  - wiki/concept
---

# SFX Engine Data Models

All data structures for the SFX Engine, defined in `davinci-resolve-mcp/src/sfx_engine/models.py`.

## Enums

### SFXCategory (13 values)

Classification of sound effects into functional groups:

| Value | Description |
|---|---|
| `COMEDY` | pop, blip, plink, honk, marimba — humorous punctuation |
| `REACTION` | awkward, huh, awww — emotional response sounds |
| `IMPACT` | impact, scream, glass — heavy hitting sounds |
| `ACCENT` | ding, pop, collect, sparkle — light emphasis marks |
| `FAIL` | wrong, scratch, bleep — failure/error indicators |
| `TRANSITION` | whoosh variants, rise — scene change markers |
| `SUCCESS` | collect, kaching, ding, crowd-cheer — win/achievement |
| `DRAMATIC` | rise, gong, metal, glitch — suspense/tension builders |
| `ACTION` | impact, whoosh, explosion, stomp — physical action |
| `UI` | click, UI-enter, digital, keyboard — interface sounds |
| `MUSIC` | harp, guitar, marimba stingers — musical accents |
| `CROWD` | crowd noises, cheers, applause — audience reactions |
| `WHOOSH` | clean, fast, intro whooshes — air movement sounds |

### EventType (12 values)

Events detected on the video timeline that trigger SFX placement:

| Value | Thai | Description |
|---|---|---|
| `JOKE` | มุก / punchline | จังหวะตลก, คำพูดที่ทำให้หัวเราะ |
| `REACTION` | อึ้ง/งง/เขิน | ปฏิกิริยาตอบสนอง, ความรู้สึก |
| `SURPRISE` | ตกใจ / เซอร์ไพรส์ | ความ surprise, สิ่งที่ไม่คาดคิด |
| `EMPHASIS` | เน้นคำ/ข้อความสำคัญ | ตัวเลข, สถิติ, ข้อความสำคัญ |
| `FAIL` | พลาด / ไม่ทัน | ความล้มเหลว, ความผิดพลาด |
| `TRANSITION` | เปลี่ยน scene | การเปลี่ยน scene, หัวข้อใหม่ |
| `SUCCESS` | สำเร็จ / ได้ของ | ความสำเร็จ, ชัยชนะ |
| `DRAMATIC` | Dramatic / suspense | ความตึงเครียด, ดราม่า |
| `ACTION` | Visual action ใหญ่ | การกระทำที่มีขนาดใหญ่ |
| `UI_NOTIFICATION` | UI / notification | แจ้งเตือน, UI elements |
| `INTRO` | Opening / intro | ช่วงเปิดคลิป |
| `OUTRO` | Closing / outro | ช่วงปิดคลิป |

### ContentFormat (5 values)

Video content format classification:

| Value | Description |
|---|---|
| `TALKING_HEAD` | Vlog, single speaker talking — คลิปพูดคนเดียว |
| `PODCAST` | Long form multi-speaker dialogue — รายการสนทนา |
| `GAME` | Gameplay, action, kills, alerts — เกมเพลย์ |
| `MEME` | Short video, high density meme edits — คลิปสั้น/มีม |
| `LIVESTREAM` | Long stream, alert-driven — ถ่ายทอดสด |

## Dataclasses

### SFXFile

Represents a single SFX audio file with extracted metadata.

| Field | Type | Description |
|---|---|---|
| `path` | `Path` | Absolute file path |
| `filename` | `str` | Filename including extension |
| `name` | `str` | Human-readable short name |
| `extension` | `str` | `.wav`, `.mp3` |
| `is_processed` | `bool` | `True` if from SFX_processed |
| `duration_seconds` | `float` | Duration in seconds (default 0.0) |
| `sample_rate` | `int` | Sample rate in Hz (default 0) |
| `channels` | `int` | Number of channels (default 0) |
| `file_size_bytes` | `int` | File size in bytes (default 0) |
| `target_db` | `Optional[float]` | Level from filename (e.g. -14) |
| `peak_db` | `Optional[float]` | Peak level |
| `rms_db` | `Optional[float]` | RMS loudness |
| `category` | `SFXCategory` | Category classification (default ACCENT) |
| `tags` | `List[str]` | Search tags |
| `family` | `str` | Family name (e.g. "whoosh", "pop") |
| `intensity` | `str` | `low`, `medium`, `high` (default "medium") |
| `is_sting` | `bool` | Whether it's a sting variant |
| `sting_path` | `Optional[Path]` | Path to sting variant |
| `content_hash` | `str` | Hash for caching |

Has `to_dict()` and `from_dict()` for JSON serialization.

### SFXSearchResult

| Field | Type | Description |
|---|---|---|
| `file` | `SFXFile` | The matched SFX file |
| `score` | `float` | Match confidence score (0.0–1.0) |

### TimelineEvent

An identified event on the video timeline requiring SFX consideration.

| Field | Type | Description |
|---|---|---|
| `type` | `EventType` | Event type |
| `timestamp` | `float` | Time in seconds |
| `description` | `str` | Human-readable description |
| `impact_score` | `float` | Importance 0.0–1.0 (default 0.5) |
| `duration` | `float` | Duration of the event window (default 0.0) |
| `text_snippet` | `Optional[str]` | Source text that triggered detection |

### BeatPoint

A scored beat point extracted for potential SFX alignment.

| Field | Type | Description |
|---|---|---|
| `timestamp` | `float` | Time in seconds |
| `event_type` | `EventType` | Event type |
| `impact_score` | `float` | Format-adjusted score |
| `description` | `str` | Human-readable description |

### SFXPlacement

Represents a planned SFX placement on the timeline.

| Field | Type | Description |
|---|---|---|
| `sfx` | `SFXFile` | The SFX file to place |
| `timestamp` | `float` | Placement time in seconds |
| `beat` | `BeatPoint` | The beat this placement satisfies |
| `volume_db` | `float` | Volume level (default -14.0) |
| `record_frame` | `int` | Timeline frame number (default 0) |
| `duration_seconds` | `float` | SFX duration (default 0.5) |
| `track_index` | `int` | Target audio track (default 2) |
| `confidence` | `float` | Placement confidence (default 0.8) |
| `reason` | `str` | Why this SFX at this moment |

Has `to_dict()` for JSON serialization.

### SFXPlan

Complete SFX recommendation plan for a video timeline.

| Field | Type | Description |
|---|---|---|
| `format` | `ContentFormat` | Detected content format |
| `placements` | `List[SFXPlacement]` | Ordered list of placements |
| `timeline_duration_seconds` | `float` | Total timeline length |
| `fps` | `float` | Frames per second (default 60.0) |
| `density_per_minute` | `float` | SFX count per minute |
| `warnings` | `List[str]` | Quality warnings |
| `spacing_violations` | `List[str]` | Placements too close together |

Has `to_dict()` for JSON serialization.

## How Models Flow

```
SFXFile (library scan)
  → SFXSearchResult (query match)
    → BeatPoint (event detection + format scoring)
      → SFXPlacement (file + beat + position + volume)
        → SFXPlan (complete timeline)
```

1. **SFXFile** — library scanner reads audio files, extracts metadata, classifies by category/family
2. **SFXSearchResult** — search engine matches files to queries, returns scored results
3. **TimelineEvent** — analyzer detects keyword matches in subtitles/transcript, creates timestamped events
4. **BeatPoint** — events are format-adjusted (PODCAST suppresses JOKE×0.4, GAME boosts ACTION×1.3)
5. **SFXPlacement** — placer selects best SFX file for each beat, computes frame position and volume
6. **SFXPlan** — all placements assembled with density checks, spacing validation, and warnings
