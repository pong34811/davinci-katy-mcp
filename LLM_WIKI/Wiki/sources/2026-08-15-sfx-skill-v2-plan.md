---
type: source-summary
source: docs/superpowers/plans/2026-08-15-sfx-skill-v2.md
date_ingested: 2026-08-15
tags: [wiki, wiki/source]
---

# Source: SFX Skill v2 Implementation Plan

Implementation plan for making SFX placement faster and more reliable by splitting work into Agent (quality decisions) + CLI/MCP (automatic batch placement).

## Key Facts

- **Architecture:** Agent plans (quality decisions), CLI places (automation via `scripts/sfx_place.py`)
- **CLI:** `scripts/sfx_place.py` — pure plan logic (load, resolve, validate) + Resolve bridge
- **MCP tool:** `davinci-resolve_sfx` — read-only: scan, search, analyze, plan
- **Frame rate:** 60fps
- **SFX track:** Track 2 (SFX 1)
- **Subtitle source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`

## Global Constraints

- CLI imports `src.sfx_engine` — sys.path must include repo root and `davinci-resolve-mcp/`
- SFX files referenced by **basename only** in plan JSON; CLI resolves against `--raw-dir`/`--processed-dir`
- The `sfx` MCP tool is **read-only**: only `scan`, `search`, `analyze`, `plan`
- Run python with: `davinci-resolve-mcp\venv\Scripts\python.exe`
- Tests use stdlib `unittest` — no pytest dependency
- Plan JSON schema: `{"timeline_name"?, "sfx": [{"sfx_file", "timestamp_seconds", "duration"?, "reason"}]}`

## Workflow

```
SRT file → analyze_subtitles.py → subtitles_beats.json → generate_sfx_plan.py → plan.json → sfx_place.py --verify → Track 2
```

## Related

- [[DaVinci Resolve SFX System]]
- [[Adding SFX Skill]]
- [[End-to-End SFX Workflow]]
