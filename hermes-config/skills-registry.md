# Project Skills Registry

This file registers all skills available in this project for Hermes Agent discovery.

## Project Skills

### SFX Placement
| Skill | Path | Description |
|-------|------|-------------|
| `adding-sfx` | `.opencode/skills/adding-sfx/SKILL.md` | Main SFX placement skill |
| `sfx-review` | `.opencode/skills/sfx-review/SKILL.md` | Review and adjust placed SFX |
| `sfx-library-manager` | `.opencode/skills/sfx-library-manager/SKILL.md` | Search and manage SFX library |
| `sfx-story-analyzer` | `.opencode/skills/sfx-story-analyzer/SKILL.md` | Analyze story arc from SRT |

### Subtitle Analysis
| Skill | Path | Description |
|-------|------|-------------|
| `subtitle-driven-enhancement` | `.opencode/skills/subtitle-driven-enhancement/SKILL.md` | Read SRT, analyze, enhance |
| `subtitle-analyzer` | `.opencode/skills/subtitle-analyzer/SKILL.md` | Analyze subtitle/transcript |

### Emotion Analysis
| Skill | Path | Description |
|-------|------|-------------|
| `emotion-analysis` | `.opencode/skills/emotion-analysis/SKILL.md` | Face + voice emotion analysis |

### DaVinci Resolve
| Skill | Path | Description |
|-------|------|-------------|
| `davinci-resolve-workflow` | `.opencode/skills/davinci-resolve-workflow/SKILL.md` | DaVinci Resolve MCP guide |

### General Purpose
| Skill | Path | Description |
|-------|------|-------------|
| `skill-creator` | `.opencode/skills/skill-creator/SKILL.md` | Create/update skill definitions |
| `systematic-debugging` | `.opencode/skills/systematic-debugging/SKILL.md` | 4-phase root cause debugging |
| `brainstorming` | `.opencode/skills/brainstorming/SKILL.md` | Creative work and feature design |
| `xlsx` | `.opencode/skills/xlsx/SKILL.md` | Excel spreadsheet operations |

## Agent Definitions

| Agent | Path | Mode | Description |
|-------|------|------|-------------|
| `skill-first` | `.opencode/agent/skill-first.md` | primary | Forces skill check before every task |
| `sfx-editor` | `.opencode/agent/sfx-editor.md` | subagent | SFX subagent for DaVinci Resolve |

## Eval Configurations

| Skill | Eval File | Description |
|-------|-----------|-------------|
| `davinci-resolve-workflow` | `.opencode/skills/davinci-resolve-workflow/evals/evals.json` | Resolve workflow tests |
| `sfx-library-manager` | `.opencode/skills/sfx-library-manager/evals/evals.json` | Library manager tests |
| `sfx-story-analyzer` | `.opencode/skills/sfx-story-analyzer/evals/evals.json` | Story analyzer tests |

## Skill Evaluation

Each skill with evals can be tested with:
```bash
python scripts/sfx_evaluator.py --skill <skill_name> --evals <path_to_evals.json>
```
