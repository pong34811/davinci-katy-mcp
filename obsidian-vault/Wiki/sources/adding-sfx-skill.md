---
type: source-summary
source: .opencode/skills/adding-sfx/SKILL.md
date_ingested: 2026-08-26
tags: [wiki, wiki/source]
---

# Source: Adding SFX Skill (3-Round Workflow)

Main skill for adding Sound Effects to DaVinci Resolve timelines. Defines the agent-CLI split, format detection, beat taxonomy, and the 3-round analysis workflow.

## Key Facts

- **Architecture:** Agent plans (quality decisions), CLI places (automation via `sfx_place.py`)
- **3-Round Workflow:** Round 1 (Structural Scan) → Round 2 (Beat Harvesting) → Round 3 (Curation with 4 filters)
- **Format Table:** talking-head 3–5/min, game 5–8/min, podcast 1–2/segment, meme high, livestream alert-driven
- **Hard Limits:** no overlapping SFX (<1s), no same-family repetition close together, every placement needs a 1-line reason
- **Density is per-format:** talking-head uses transcript beats, game uses action/kill/UI events, podcast is nearly silent

## Related

- [[DaVinci Resolve SFX System]]
- [[SFX Beat Detection]]
- [[Three-Round SFX Analysis]]
