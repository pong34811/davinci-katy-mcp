# Change Log

## 2026-09-02 — Hermes Agent Project Reorganization

### Added
- `hermes-config/config.yaml` — Hermes main configuration
- `hermes-config/README.md` — Configuration guide
- `hermes-config/skills-registry.md` — Skill registration and evaluation
- `hermes-config/settings.local.json` — Claude local permissions
- `.hermes.md` — Hermes-specific project rules (skill map, slash commands, toolsets)
- `docs/` — Documentation directory structure
- `logs/` — Log directory
- `scripts/main.py` — Entry point for the system
- Updated `README.md` — Full project architecture, workflow, and structure documentation

### Changed
- `.claude/settings.local.json` — Updated permissions for all project operations
- `AGENTS.md` — Added context file priority section, subtitle source rule, Hermes-specific notes
- `CLAUDE.md` — Aligned with `.hermes.md`, added Hermes integration section

### Skills Updated
All 5 skills updated to read from SRT file (`Subtitle 1.srt`) instead of DaVinci Resolve subtitle track:
- `subtitle-driven-enhancement/SKILL.md`
- `sfx-story-analyzer/SKILL.md`
- `sfx-review/SKILL.md`
- `subtitle-analyzer/SKILL.md`
- `adding-sfx/SKILL.md`

### Files Removed/Cleaned
- Removed stale JSON files from project root (beats_beats.json, subtitles_beats_beats.json, etc.)

## Previous Versions

### Live SFX Placement (2026-09-02)
- 9 SFX placed on 'เรื่องแปลกของยามะ' (20.4s comedy short)
- Live SFX placement implemented
- ctypes fallback bridge for fusionscript.dll
- Wiki restructuring: engine code ingested, machine-usable categories, config fix
