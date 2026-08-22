# AGENTS.md

## Project Layout

- **Project root:** `C:\Users\warit\Desktop\davinci-katy-mcp`
- **MCP server:** `davinci-resolve-mcp/src/server.py` — 28k+ lines, handles all DaVinci Resolve API tools
- **Scripts:** `scripts/` — CLI tools for SFX placement, subtitle reading, analysis
- **SFX library:** `SFX/` at project root (70+ files, mp3/wav, NOT in `davinci-resolve-mcp/`)
- **No `SFX_processed/` folder** at this user's machine — all scripts must use raw SFX from `SFX/` directly
- **Subtitle files:** `subtitle_from_track1.srt` at project root

## SFX File Mapping (User's Library)

The user's SFX files use human-readable names (e.g., `Pop - Short 06.mp3`, `Bell - Ding 02.wav`), NOT the short slug names (`pop-14.wav`, `ding-12.wav`) that appear in `SFX_processed/`. When generating SFX plans, map families to actual filenames:

- pop → `Pop - Short 06.mp3`
- ding → `Bell - Ding 02.wav`
- sparkle → `Harp - Sparkle 01.mp3`
- whoosh → `Whoosh - Clean Fast.mp3`
- impact → `Impact - Comedy Hit 01.mp3`
- wrong → `Game - Wrong Answer.mp3`
- collect → `Game - Correct Collect Answer.mp3`

Full mapping is in `scripts/generate_sfx_plan.py` → `SFX_FAMILIES` dict.

## Resolve API Quirks

- `hasattr(obj, name)` is **always True** on Resolve API objects — use `callable(getattr(obj, name, None))` instead. Module `src/utils/resolve_probe.py` provides `has_method()`.
- `GetClipProperty("")` returns the entire property map (a dict), not a single value. Always check `isinstance(value, dict)` after calling it.
- `GetSelectedTimelineItems` / `GetSelectedItems` / `GetSelectedClips` — three names for the same thing across different Resolve builds. The server probes all three.
- `SetCurrentTimecode` refuses timecodes below the timeline start frame with a bare `False` (no error). The server lifts elapsed timecodes to absolute via `_playhead_absolute_timecode()`.
- Source frame rates on WAV files are frozen at import time from the project's `timelineFrameRate`, NOT the WAV's native rate. A WAV imported at 24fps into a 29.97fps timeline stays at 24fps for source frame calculations.

## Skills Structure

Skills live in `.opencode/skills/<name>/SKILL.md`. Current skills:

- `adding-sfx` — main SFX placement skill, extensive beat taxonomy and format table
- `subtitle-driven-enhancement` — reads subtitle track 1, analyzes, generates SFX plan
- `emotion-analysis` — face + voice emotion analysis
- `obsidian-best-practices` / `obsidian-cli` — cloned from external repo

## Obsidian Vault

Created at `obsidian-vault/` with templates, project notes, SFX Manager plugin, and docs. The `sfx-manager` plugin (`obsidian-vault/Plugins/sfx-manager/`) provides in-Obsidian SFX library browsing.

## Environment

- Python venv at `davinci-resolve-mcp/venv/`
- OpenCV + MediaPipe required for face analysis (optional, degrades gracefully)
- ffmpeg needed for audio extraction from video (voice analysis)
- DaVinci Resolve must be running for MCP tools and `sfx_place.py`
