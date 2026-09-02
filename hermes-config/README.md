# hermes-config/README.md — Hermes Configuration Guide

This directory contains Hermes Agent configuration for the DaVinci Resolve SFX project.

## Files

- `config.yaml` — Main Hermes configuration (model, toolsets, skills, paths)
- `settings.local.json` — Local Claude settings (permissions)

## Usage

Hermes loads these settings when running in this project directory.

### Key Settings

- **Model:** `inclusionai/ling-3.0-flash-fin:free` (Nous provider)
- **Toolsets:** terminal, code_execution, file, skills, todo, clarify, web, browser
- **Skills:** adding-sfx, subtitle-driven-enhancement, sfx-story-analyzer, sfx-review, sfx-library-manager, subtitle-analyzer, emotion-analysis, davinci-resolve-workflow, skill-creator, systematic-debugging, brainstorming, xlsx
- **SRT source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
- **SFX directory:** `C:\Users\warit\Desktop\davinci-katy-mcp\SFX`
- **Python:** `davinci-resolve-mcp/venv/Scripts/python.exe`

## Configuration Priority

1. `~/.hermes/config.yaml` — global Hermes config (never secrets)
2. `hermes-config/config.yaml` — project-specific config (this file)
3. `.env` — API keys and secrets ONLY
4. Environment variables — override everything
