# DaVinci Resolve SFX Enhancement System

> **Hermes Agent** — autonomous AI agent for adding Sound Effects to DaVinci Resolve clips

## Overview

An AI-powered system that reads subtitle files, analyzes emotional beats, and automatically places Sound Effects (SFX) on DaVinci Resolve timelines.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Hermes Agent                       │
│  ┌─────────┐  ┌─────────┐  ┌──────────────────────┐ │
│  │  CLI     │  │ Desktop │  │ MCP Server           │ │
│  │ (hermes) │  │  App    │  │ (davinci-resolve-mcp)│ │
│  └────┬─────┘  └────┬────┘  └──────────┬───────────┘ │
│       │              │                 │              │
│       ▼              ▼                 ▼              │
│  ┌──────────────────────────────────────────────┐   │
│  │           AIAgent (run_agent.py)              │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐  │   │
│  │  │ Prompt   │ │ Provider │ │ Tool Dispatch│  │   │
│  │  │ Builder  │ │ Resolution│ │ (28 toolsets)│  │   │
│  │  └────┬─────┘ └────┬─────┘ └──────┬───────┘  │   │
│  │       │            │              │           │   │
│  │  ┌────┴────────────┴──────────────┴───────┐   │   │
│  │  │     Context Engine + Compression       │   │   │
│  │  └───────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌───────────┐      ┌──────────────┐     ┌──────────────┐
  │ Skills    │      │ DaVinci      │     │ SFX Library  │
  │ (.opencode│      │ Resolve      │     │ (SFX/)       │
  │ /skills/) │      │ MCP Server   │     │ 70+ files    │
  └───────────┘      └──────────────┘     └──────────────┘
```

## Quick Start

```bash
# Full pipeline: read SRT → analyze → plan → place SFX
davinci-resolve-mcp/venv/Scripts/python.exe scripts/sfx_place.py --plan scripts/plan.json --verify

# Analyze subtitle from SRT file
python scripts/analyze_subtitles.py --action read --srt "C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt"

# Generate SFX plan from beats
python scripts/generate_sfx_plan.py --beats scripts/subtitles_beats.json --format talking-head
```

## Workflow

1. **Read SRT** → Parse subtitle file at `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
2. **Analyze beats** → Identify emotional turning points, emphasis, fails, transitions
3. **Generate plan** → Match beats to SFX families with timestamps
4. **Dry-run** → Validate plan (file existence, timestamp overlap check)
5. **Place SFX** → Create Track 2 (SFX 1) and place all SFX
6. **Verify** → Read back frame positions and confirm placement

## Project Structure

```
davinci-katy-mcp/
├── hermes-config/             # Hermes Agent configuration
│   ├── config.yaml            # Main config (model, toolsets, skills)
│   ├── settings.local.json    # Claude local settings (permissions)
│   ├── skills-registry.md     # Skill registration and evaluation
│   └── README.md              # Configuration guide
├── scripts/                   # CLI tools and analysis scripts
│   ├── main.py                # Entry point (status, analyze, plan, place, enhance)
│   ├── config.py              # Central configuration
│   ├── analyze_subtitles.py   # Subtitle analysis from SRT
│   ├── generate_sfx_plan.py   # SFX plan generation
│   ├── sfx_place.py           # SFX placement on timeline
│   ├── impact_scorer.py       # Impact scoring for beats
│   ├── emotion_analyzer.py    # Emotion analysis (face + voice)
│   ├── face_analyzer.py       # Face landmark detection
│   ├── voice_analyzer.py      # Voice analysis
│   ├── story_arc_analyzer.py  # Story arc detection
│   ├── sfx_evaluator.py       # SFX quality evaluation
│   ├── sfx_audio_analyzer.py  # SFX audio analysis
│   ├── timing_intelligence.py # Precise timing decisions
│   └── __pycache__/           # Compiled Python cache
├── davinci-resolve-mcp/       # MCP server for DaVinci Resolve API
│   ├── src/                   # Source code
│   │   ├── server.py          # Main MCP server (28k+ lines)
│   │   └── utils/             # Utility modules
│   ├── venv/                  # Python virtual environment
│   └── logs/                  # Server logs
├── SFX/                       # Raw SFX library (70+ files)
│   ├── Pop - Short 06.mp3
│   ├── Bell - Ding 02.wav
│   ├── Game - Wrong Answer.mp3
│   └── ...
├── .opencode/                 # OpenCode configuration
│   ├── skills/                # 20+ skill definitions
│   │   ├── adding-sfx/        # Main SFX placement skill
│   │   ├── subtitle-driven-enhancement/  # Subtitle-driven enhancement
│   │   ├── sfx-review/        # SFX review skill
│   │   ├── sfx-library-manager/   # SFX library manager
│   │   ├── sfx-story-analyzer/    # Story arc analyzer
│   │   ├── subtitle-analyzer/     # Subtitle analyzer
│   │   ├── emotion-analysis/      # Emotion analysis
│   │   ├── davinci-resolve-workflow/ # DaVinci Resolve workflow
│   │   └── ...                # 20+ additional skills
│   ├── agent/                 # Agent definitions
│   │   ├── skill-first.md     # Primary agent (skill-first)
│   │   └── sfx-editor.md      # SFX subagent
│   └── evals/                 # Skill evaluation configs
├── .hermes.md                 # Hermes-specific project rules
├── AGENTS.md                  # Portable project rules
├── CLAUDE.md                  # Claude-flavored tier checklist
├── SFX_RESULTS.md             # Latest SFX placement results
└── obsidian-vault/            # Obsidian knowledge base
    ├── Wiki/                  # LLM-maintained wiki
    ├── Clippings/             # Raw sources (immutable)
    └── Plugins/sfx-manager/   # In-Obsidian SFX library browser
```

## Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `adding-sfx` | Place SFX on timeline | "เพิ่ม SFX", "ใส่เสียงประกอบ" |
| `sfx-review` | Review/adjust placed SFX | "ใส่น้อย", "ตรวจละเอียด" |
| `subtitle-driven-enhancement` | Read SRT, analyze, enhance | "ปรับแต่งคลิปจาก SRT" |
| `sfx-library-manager` | Search SFX library | "หา SFX", "เปรียบเทียบเสียง" |
| `sfx-story-analyzer` | Story arc from SRT | "วิเคราะห์ story arc" |
| `subtitle-analyzer` | Subtitle/transcript analysis | "วิเคราะห์ subtitle" |
| `emotion-analysis` | Face + voice emotion | "วิเคราะห์อารมณ์" |
| `davinci-resolve-workflow` | Resolve MCP tools | "timeline", "color", "render" |

## SFX File Mapping

| Family | Filename |
|--------|----------|
| pop | `Pop - Short 06.mp3` |
| ding | `Bell - Ding 02.wav` |
| sparkle | `Harp - Sparkle 01.mp3` |
| whoosh | `Whoosh - Clean Fast.mp3` |
| impact | `Impact - Comedy Hit 01.mp3` |
| wrong | `Game - Wrong Answer.mp3` |
| collect | `Game - Correct Collect Answer.mp3` |

## Rules

- Read subtitles ONLY from `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
- Use ONLY files in `SFX/` directory — never guess filenames
- SFX placed on Track 2 (SFX 1)
- Density: ~10-15/min (user preference)
- Always: dry-run → place → verify
- Every SFX must have a `reason` 1 บรรทัด

## Python Environment

```bash
# Use the venv Python
davinci-resolve-mcp\venv\Scripts\python.exe scripts\sfx_place.py --plan scripts/plan.json --verify
```

## Requirements

- DaVinci Resolve (Studio or Free) — must be running
- Python 3.8+
- OpenCV + MediaPipe (for face analysis)
- ffmpeg (for audio extraction)

## Testing

```bash
# Run tests
davinci-resolve-mcp\venv\Scripts\python.exe -m pytest tests/ -v
```

## License

MIT
