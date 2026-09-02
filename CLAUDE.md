# CLAUDE.md — SFX Enhancement Agent (Hermes-Aware)

> Aligned with `.hermes.md` and `AGENTS.md`. Hermes loads `.hermes.md` first, then this file.

## ⚠️ MANDATORY: Read Before Work

**ก่อนเริ่มงานใดๆ ต้องอ่านไฟล์เหล่านี้ก่อนเสมอ:**

### Tier 1 — อ่านทุกครั้ง (mandatory)
1. `.hermes.md` — Hermes-specific rules, skill map, slash commands, toolset requirements
2. `AGENTS.md` — project layout, SFX file mapping, subtitle source rule, wiki rules
3. `.opencode/agent/skill-first.md` — skill invocation rules
4. `CLAUDE.md` — this file (tier checklist)

### Tier 2 — อ่านตามงาน (selective)
**งาน SFX:**
5. `obsidian-vault/Wiki/synthesis/end-to-end-sfx-workflow.md` — workflow guide
6. `obsidian-vault/Wiki/concepts/sfx-placement-lessons-learned.md` — empirical rules
7. `obsidian-vault/Wiki/concepts/format-specific-sfx-behavior.md` — format rules
8. `obsidian-vault/Wiki/concepts/three-round-sfx-analysis.md` — analysis method
9. `.opencode/agent/sfx-editor.md` — SFX subagent rules
10. `.opencode/skills/adding-sfx/SKILL.md` — skill reference
11. `.opencode/skills/sfx-review/SKILL.md` — review skill

**งาน Subtitle/Emotion:**
12. `obsidian-vault/Wiki/concepts/subtitle-driven-beat-detection.md`
13. `.opencode/skills/subtitle-analyzer/SKILL.md`
14. `.opencode/skills/emotion-analysis/SKILL.md`
15. `.opencode/skills/sfx-story-analyzer/SKILL.md`

**งาน DaVinci Resolve:**
16. `.opencode/skills/davinci-resolve-workflow/SKILL.md`

**งานอื่นๆ:**
17. `.opencode/skills/*/SKILL.md` — invoke ก่อนทำ work นั้น

### Tier 3 — อ่านเมื่อจำเป็น
- `obsidian-vault/Wiki/sources/*.md` — source summaries
- `obsidian-vault/Wiki/entities/*.md` — entity pages
- `obsidian-vault/Notes/*.md` — project notes
- `obsidian-vault/Projects/*.md` — project context
- `docs/superpowers/*.md` — design docs
- `README.md` — project overview
- `Changelog.md` — history

---

## Pre-Work Checklist

```
[ ] อ่าน Tier 1 (.hermes.md, AGENTS.md, skill-first.md, CLAUDE.md)
[ ] ระบุ work type (SFX / subtitle / emotion / resolve / other)
[ ] อ่าน Tier 2 ที่เกียวข้อง
[ ] Invoke skill ที่เหมาะสม (ถ้ามี)
[ ] เริ่มงาน
```

---

## Key Rules

### Subtitle Source Rule
- **อ่านเฉพาะ SRT file:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
- ห้ามใช้ `subtitle_from_track1.srt` ที่ project root — stale, timestamps ไม่ตรง
- Timestamps ใน SRT file ตรงกับ timeline เสมอ

### SFX Specific
- ใช้เฉพาะไฟล์จริงใน `C:\Users\warit\Desktop\davinci-katy-mcp\SFX` — ห้ามเดาชื่อนามสกุล
- CLI: `davinci-resolve-mcp\venv\Scripts\python.exe scripts\sfx_place.py`
- Density target: ~10-15/min (user preference)
- SFX ซ้อน <1s = fail; ลำดับ comedy ต่อเนื่อง = OK
- Always dry-run → place → verify
- ทุก SFX ต้องมี `reason` 1 บรรทัด

### Wiki Rules (from AGENTS.md)
- `Clippings/` = IMMUTABLE — never modify raw source files
- `Wiki/` = LLM-owned — always update index.md and log.md on every change
- Every wiki page gets `type:` in frontmatter and `wiki/*` tags
- Heavy use of `[[wikilinks]]` for Obsidian graph view
- When sources contradict, note it explicitly — don't silently overwrite

### Skill-First (from .hermes.md and skill-first.md)
- Before any task, ask: "มี skill ที่เกียวข้องกับงานนี้ไหม?"
- If 1% chance → invoke skill tool first
- Exception: conversation meta-questions ("เสร็จยัง", "ได้") — answer directly

### Context Compression Awareness
- `.hermes.md` is the authoritative source for skill map and rules after compression
- If context was compressed, reload `.hermes.md` before proceeding
- The skill map, pre-work checklist, and SRT source path are preserved in `.hermes.md`

---

## Environment
- Python venv: `davinci-resolve-mcp/venv/`
- Use `davinci-resolve-mcp/venv/Scripts/python.exe`
- OpenCV + MediaPipe required for face analysis (optional)
- ffmpeg needed for audio extraction
- DaVinci Resolve must be running for MCP tools and sfx_place.py

## Hermes Integration
- `.hermes.md` loaded first — Hermes-specific rules override general guidance
- Use `hermes` CLI commands: `/skills`, `/curator`, `/cron`, `/delegate`, `/new`, `/compress`
- Spawn subagents via `delegate_task` for parallel work
- Cron jobs via `cronjob` tool for recurring SFX tasks
