---
type: synthesis
tags: [wiki, wiki/synthesis]
date_updated: 2026-08-26
source_count: 6
---

# End-to-End SFX Placement Workflow

Complete agent guide: from receiving a "add SFX to this clip" request to verified placement on the DaVinci Resolve timeline.

## Prerequisites

- DaVinci Resolve running with a project open
- Timeline has video + at least 1 audio track (Dialogue)
- Subtitle track 1 populated (or game/meme with visual cues)
- SFX library at `C:\Users\warit\Desktop\davinci-katy-mcp\SFX`

## Step-by-Step

### 1. Setup (MCP Calls)

```
sfx(action="scan")                          → list all SFX files
timeline(action="get_current")              → timeline name, frame range
timeline(action="probe_audio_track")        → track count, names, index
project_settings(action="get_setting",      → frame rate (for frame→seconds)
  params={name: "timelineFrameRate"})
timeline(action="get_transcript",           → full transcript with timecodes
  params={with_timecodes: true})
```

### 2. Format Detection

Read transcript + context → pick format from [[SFX Beat Detection]] table:

| If you see... | Format | Density |
|---------------|--------|---------|
| Single speaker, continuous talk | talking-head | 3–5/min |
| 2+ speakers, long, conversational | podcast | 1–2/segment |
| Game footage, kills, UI | game | 5–8/min |
| Short, joke-driven, no dialogue | meme | high |
| Long stream, alerts | livestream | alert-driven |

### 3. Three-Round Analysis → [[Three-Round SFX Analysis]]

**Round 1 — Structural Scan:** Convert frames to seconds, divide transcript into sections by topic/mood, identify boundaries.

**Round 2 — Beat Harvesting:** Walk every cue. For each: check text (joke? number? reaction? emotion?), check context (before/after cues). Record ALL candidates with timestamp + text + beat type + SFX family + reason.

**Round 3 — Curation:** Apply 4 filters: density cap → spacing (≥1s) → family variety → impact ranking. Cut from bottom until within density cap.

### 4. Write Plan JSON

```json
{
  "timeline_name": "Timeline 1",
  "sfx": [
    {
      "sfx_file": "Pop - Short 06.mp3",
      "timestamp_seconds": 17.8,
      "reason": "1,800 subscribers milestone — celebratory pop"
    }
  ]
}
```

**Rules:** Every entry needs `reason` (1 line). Use filenames from `sfx(action="scan")` ONLY. Never guess filenames.

### 5. Place (CLI)

```powershell
# Dry-run first
davinci-resolve-mcp\venv\Scripts\python.exe scripts\sfx_place.py --plan plan.json --dry-run --sfx-dir "C:\Users\warit\Desktop\davinci-katy-mcp\SFX"

# Place for real
davinci-resolve-mcp\venv\Scripts\python.exe scripts\sfx_place.py --plan plan.json --verify --sfx-dir "C:\Users\warit\Desktop\davinci-katy-mcp\SFX"
```

Exit codes: 0=success, 1=partial failure, 2=plan error, 3=can't connect to Resolve.

### 6. Verify

CLI `--verify` reads back items on the SFX track. Cross-check:
- Correct count (plan vs placed)
- Correct frames (timestamp → frame conversion)
- No overlaps
- No missing files

## Post-Placement: [[SFX Review Skill]]

If user says "ใส่น้อย" / "ใส่มากไป" / "ตรวจละเอียด" → use sfx-review skill for delta-only improvements. Never re-place everything from scratch.

## Failure Modes

| Error | Cause | Fix |
|-------|-------|-----|
| `file not found in SFX dir` | Filename not in scan results | Re-run `sfx(action="scan")`, use exact filename |
| `ERROR: cannot connect to Resolve` | Resolve not running | Start DaVinci Resolve, wait for full load |
| `ERROR: no project open` | No project loaded | Open a project in Resolve first |
| `ERROR: no timeline open` | No timeline selected | Select a timeline in Resolve |
| Spacing warning | 2 SFX < 1s apart | Move one or cut the weaker one |
