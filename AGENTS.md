# AGENTS.md — DaVinci Resolve SFX Enhancement Project

> **Portable** — works the same in Hermes, Claude Code, Codex, and OpenCode.
> Hermes-specific rules go in `.hermes.md` (loaded first by Hermes).

## Project Layout

- **Project root:** `C:\Users\warit\Desktop\davinci-katy-mcp`
- **LLM Wiki:** `LLM_WIKI/` — Karpathy-pattern wiki with raw sources and synthesized pages
  - `LLM_WIKI/raw/llm-wiki.md` — canonical source document (Karpathy wiki pattern)
  - `LLM_WIKI/raw/Wiki/sources/` — raw source summaries organized by domain (video-editing/, audio/, leadership/)
  - `LLM_WIKI/Wiki/` — synthesized pages (index, concepts, synthesis, core, sfx, subtitle, video-editing, sources, audio, leadership)
  - `LLM_WIKI/Wiki/index.md` — content catalog — read this FIRST when querying the wiki
  - `LLM_WIKI/Wiki/log.md` — append-only operation log
  - `LLM_WIKI/Wiki/overview.md` — high-level synthesis
  - `LLM_WIKI/Clippings/` — raw clipped articles (17 source files, immutable)
  - `LLM_WIKI/assets/` — downloaded images
- **MCP server:** `davinci-resolve-mcp/src/server.py` — handles all DaVinci Resolve API tools
- **Scripts:** `scripts/` — CLI tools for SFX placement, subtitle reading, analysis
- **SFX library:** `SFX/` at project root (70+ files, mp3/wav)
- **SRT subtitle source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
- **No `SFX_processed/` folder** — all scripts use raw SFX from `SFX/` directly
- **Subtitle files:** `scripts/C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` (stale, do NOT use)
- **Context files:** `.hermes.md` (Hermes-specific), `AGENTS.md` (this file, portable), `CLAUDE.md` (Claude-flavored)
- **Skills:** `.opencode/skills/` (26 project skills), `hermes-config/` (config.yaml, skills-registry.md)

## Skills Structure

Skills live in `.opencode/skills/<name>/SKILL.md`. Current skills:

- `adding-sfx` — main SFX placement skill, extensive beat taxonomy and format table
- `subtitle-driven-enhancement` — reads SRT file, analyzes, generates SFX plan
- `sfx-story-analyzer` — analyzes story arc from SRT file, places SFX
- `sfx-review` — reviews and adjusts SFX already placed on timeline
- `sfx-library-manager` — searches, categorizes, compares SFX from library
- `subtitle-analyzer` — analyzes subtitle/transcript from SRT file for editing decisions
- `emotion-analysis` — face + voice emotion analysis
- `davinci-resolve-workflow` — DaVinci Resolve MCP tool guide
- `obsidian-best-practices` / `obsidian-cli` — cloned from external repo
- `skill-creator` — create/update skill definitions
- `systematic-debugging` — 4-phase root cause debugging
- `brainstorming` — creative work and feature design
- `xlsx` — Excel spreadsheet operations

## Agent Definitions

- `.opencode/agent/skill-first.md` — primary agent, forces skill check before every task
- `.opencode/agent/sfx-editor.md` — subagent for SFX work in DaVinci Resolve

## SFX File Mapping (User's Library)

The user's SFX files use human-readable names, NOT short slug names:

|| Family | Filename |
||--------|----------|
|| pop | `Pop - Short 06.mp3` |
|| ding | `Bell - Ding 02.wav` |
|| sparkle | `Harp - Sparkle 01.mp3` |
|| whoosh | `Whoosh - Clean Fast.mp3` |
|| impact | `Impact - Comedy Hit 01.mp3` |
|| wrong | `Game - Wrong Answer.mp3` |
|| collect | `Game - Correct Collect Answer.mp3` |

Full mapping: `scripts/generate_sfx_plan.py` → `SFX_FAMILIES` dict.

## Resolve API Quirks

- `hasattr(obj, name)` is **always True** on Resolve API objects — use `callable(getattr(obj, name, None))` instead. Module `scripts/resolve_probe.py` provides `has_method()`.
- `GetClipProperty("")` returns the entire property map (a dict), not a single value. Always check `isinstance(value, dict)` after calling it.
- `GetSelectedTimelineItems` / `GetSelectedItems` / `GetSelectedClips` — three names for the same thing across different Resolve builds.
- `SetCurrentTimecode` refuses timecodes below the timeline start frame with a bare `False`. The server lifts elapsed timecodes to absolute via `_playhead_absolute_timecode()`.
- Source frame rates on WAV files are frozen at import time from the project's `timelineFrameRate`, NOT the WAV's native rate.

## Subtitle Source Rule

**Read subtitles ONLY from the SRT file:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`

This is the PRIMARY subtitle source. Timestamps in this SRT file match the timeline exactly. The local `scripts/C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` at project root is STALE and does NOT match — do not use it.

## LLM Wiki (Karpathy Pattern)

Persistent, interlinked wiki maintained by LLM from raw sources. Based on [Karpathy's llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

### Structure

```
LLM_WIKI/
├── raw/                      # RAW SOURCES — immutable, never modify
│   ├── llm-wiki.md           # Canonical source document (Karpathy pattern)
│   └── Wiki/sources/         # Source summaries organized by domain
│       ├── video-editing/    # DaVinci Resolve MCP servers, AI control, plugins
│       ├── audio/            # Fairlight workflow, SFX guides, plugins comparison
│       └── leadership/       # Skills analysis, AI skills gap, data analysis
├── Clippings/                # Clipped articles (immutable)
├── assets/                   # Downloaded images
└── Wiki/                     # SYNTHESIZED PAGES — LLM-owned
    ├── index.md              # Content catalog — read this FIRST
    ├── log.md                # Append-only operation log
    ├── overview.md           # High-level synthesis
    ├── sources/              # One summary per ingested source
    ├── concepts/             # Ideas, patterns, techniques
    ├── synthesis/            # Query answers filed back into wiki
    ├── core/                 # System config, data models, event taxonomy
    ├── sfx/                  # SFX library, search, negative knowledge
    ├── subtitle/             # Subtitle analysis, beat detection
    └── video-editing/        # Plan generation, placement engine
```

### Rules

- **raw/ is IMMUTABLE.** Never modify raw source files or source summaries.
- **Wiki/ is LLM-owned.** Always update `index.md` and `log.md` on every change.
- Every wiki page gets `type:` in frontmatter and `wiki/*` tags.
- Heavy use of `[[wikilinks]]` for Obsidian graph view.
- Source summaries = factual. Interpretation goes in concept/synthesis pages.
- When sources contradict, note it explicitly — don't silently overwrite.
- `[key::value]` inline metadata for Dataview queries.

### Operations

**Ingest:** Read raw source → create source summary → create/update entity pages → create/update concept pages → update index.md → update overview.md → append to log.md

**Query:** Read index.md → read relevant wiki pages → synthesize answer with wikilinks → file substantial answers into Wiki/synthesis/ → update index and log

**Lint:** Check for orphan pages, broken wikilinks, stale pages, contradictions, concepts without their own page.

### Frontmatter Schema

Source summary: `type: source-summary`, `source:`, `date_ingested:`, `tags: [wiki, wiki/source]`
Entity: `type: entity`, `entity_type:`, `source_count:`, `tags: [wiki, wiki/entity]`
Concept: `type: concept`, `confidence: high|medium|low`, `source_count:`, `tags: [wiki, wiki/concept]`
Synthesis: `type: synthesis`, `tags: [wiki, wiki/synthesis]`

### Reading All Raw Sources

When updating the wiki, read ALL files in `LLM_WIKI/raw/Wiki/sources/` recursively — every domain subdirectory (video-editing/, audio/, leadership/). Also read `LLM_WIKI/raw/llm-wiki.md` for the canonical pattern document. The raw source summaries in `raw/Wiki/sources/` are the authoritative source material for all Wiki/ synthesis pages.

## Environment

- Python venv at `davinci-resolve-mcp/venv/`
- Use `davinci-resolve-mcp/venv/Scripts/python.exe` for all Python scripts
- OpenCV + MediaPipe required for face analysis (optional, degrades gracefully)
- ffmpeg needed for audio extraction from video (voice analysis)
- DaVinci Resolve must be running for MCP tools and `sfx_place.py`

## Context File Priority (Hermes)

Hermes loads context files in this priority order (first match wins):

1. **`.hermes.md`** — Hermes-specific rules, skill invocation, slash commands, toolset requirements (CWD only)
2. **`AGENTS.md`** — Portable project rules, project layout, SFX mapping, wiki rules
3. **`CLAUDE.md`** — Claude-flavored tier-based reading checklist

The `.hermes.md` is loaded FIRST and overrides general guidance with Hermes-specific instructions.