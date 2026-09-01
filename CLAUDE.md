# CLAUDE.md — SFX Enhancement Agent

## ⚠️ MANDATORY: Read Before Work

**ก่อนเริ่มงานใดๆ (แม้แต่มอถามสั้น) ต้องอ่านไฟล์เหล่านี้นก่อนเสมอ:**

### Tier 1 — อ่านทุุกครัง (mandatory)
1. `obsidian-vault/Wiki/index.md` — content catalog, อ่านเปนแรก
2. `obsidian-vault/Wiki/overview.md` — high-level synthesis
3. `AGENTS.md` — project layout, LLM Wiki rules, SFX file mapping
4. `.opencode/agent/skill-first.md` — skill invocation rules

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

**งาน DaVinci Resolve:**
15. `.opencode/skills/davinci-resolve-workflow/SKILL.md`

**งานอื่นๆ:**
16. `.opencode/skills/*/SKILL.md` — invoke ก่อนทำ work นั้น

### Tier 3 — อ่านเมื่อจำเป็น
- `obsidian-vault/Wiki/sources/*.md` — source summaries (ถ้า Tier 1/2 ละเอียดไมพอ)
- `obsidian-vault/Wiki/entities/*.md` — entity pages
- `obsidian-vault/Notes/*.md` — project notes
- `obsidian-vault/Projects/*.md` — project context
- `docs/superpowers/*.md` — design docs
- `README.md` — project overview
- `Changelog.md` — history

---

## Pre-Work Checklist

```
[ ] อ่าน Tier 1 (index.md, overview.md, AGENTS.md, skill-first.md)
[ ] ระบุ work type (SFX / subtitle / emotion / resolve / other)
[ ] อ่าน Tier 2 ที่เกียวข้อง
[ ] invoked skill ที่เหมาะสม (ถ้ามี)
[ ] เริ่มงาน
```

---

## Key Rules

### SFX Specific
- ใช้เฉพาะไฟล์จริงใน `C:\Users\warit\Desktop\davinci-katy-mcp\SFX` — ห้ามเดาชื่อนามฝایل
- CLI: `davinci-resolve-mcp\venv\Scripts\python.exe scripts\sfx_place.py`
- Density target: ~10-15/min (user preference — higher than default)
- SFX ซ้อน <1s = fail; ลำดับ comedy ต่อเนื่อง = OK
- Always dry-run → place → verify

### Wiki Rules (from AGENTS.md)
- `Clippings/` = IMMUTABLE — never modify raw source files
- `Wiki/` = LLM-owned — always update index.md and log.md on every change
- Every wiki page gets `type:` in frontmatter and `wiki/*` tags
- Heavy use of `[[wikilinks]]` for Obsidian graph view
- When sources contradict, note it explicitly — don't silently overwrite

### Skill-First (from skill-first.md)
- Before any task, ask: "มี skill ที่เกียวข้องกับงานนี้ไหม?"
- If 1% chance → invoke skill tool first
- Exception: conversation meta-questions ("เสร็จยัง", "ได้") — answer directly

---

## Environment
- Python venv: `davinci-resolve-mcp/venv/`
- OpenCV + MediaPipe required for face analysis (optional)
- ffmpeg needed for audio extraction
- DaVinci Resolve must be running for MCP tools and sfx_place.py
