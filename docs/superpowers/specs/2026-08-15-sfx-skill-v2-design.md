# SFX Skill v2 — Design

## เป้าหมาย

เพิ่มความเร็วและความน่าเชื่อถือของการเพิ่ม Sound Effects (SFX) ลง timeline ของ DaVinci Resolve โดยแบ่งงานออกเป็น **สมอง (Agent)** กับ **แขน (CLI/MCP)**:

- Agent เป็นผู้ตัดสินใจคุณภาพ (เลือกจังหวะ เลือกเสียง เขียนเหตุผล) ตามกฎเดิมของ skill
- CLI/MCP เป็นผู้ลงมือวาง (สร้าง track, import, trim sting, place, verify) อัตโนมัติ — วางหลายตัวในครั้งเดียวแทนการวางทีละ MCP call

## สถานการณ์ปัจจุบัน (ต้องรู้ก่อนอ่าน design)

- `.opencode/skills/adding-sfx/SKILL.md` — skill เดิมสมบูรณ์ (Format Detection, Beat Taxonomy, Hard Limits, Hindsight Pass, Verification Checklist) พิสูจน์แล้วว่าวางได้จริง 2 โปรเจค แต่ Workflow สั่งให้ Agent วิเคราะห์เองแล้ววางทีละ MCP call → ช้าและผิดพลาดง่าย
- `davinci-resolve-mcp/src/sfx_engine/` — engine Python เขียนเสร็จแล้ว (analyzer, recommender, scanner, search, placer + tests) แต่ `mcp_tools.py` ยังไม่ได้ต่อเข้ากับ server.py จริง และ actions `execute`/`verify`/`remove_all` ตอบ error ว่าไม่มี live Resolve handles
- `scripts/` — มีสคริปต์ ad-hoc 25 ไฟล์ (execute_sfx_plan.py, place_meme.py ฯลฯ) ที่ผ่านการพิสูจน์แล้วว่าวาง SFX บน Resolve ได้จริง ผ่านการต่อตรง DaVinciResolveScript
- `Z:\SFX` (71 ไฟล์) และ `Z:\SFX_processed` (27 ไฟล์ wav, ชื่อบอก dB: `pop-14.wav` = Pop ที่ −14 dB)
- `.opencode/skills/adding-sfx/kimi.plugin.json` — ไฟล์ JSON พัง syntax (มี content ซ้ำซ้อนกันหลายชั้น)

## สถาปัตยกรรม

```
Agent (สมอง)                          CLI / MCP (แขน)
─────────────────                     ─────────────────────
1. ระบุ format (Format Table เดิม)
2. inspect timeline + library
3. วิเคราะห์จังหวะจาก transcript/beats    ← ใช้ sfx MCP tool (read-only)
4. เลือก SFX + เขียนเหตุผล (Beat Taxonomy)
5. เขียน plan JSON
6. รัน CLI: python scripts/sfx_place.py    → วางทั้งหมดครั้งเดียว + verify
7. ตรวจ readback, Hindsight Pass
```

หลักการ: **Agent ตัดสินคุณภาพ, เครื่องวาง** — SFX 20 ตัวลงใน 1 CLI call แทน 20 MCP calls

## ส่วนประกอบ

### 1. `scripts/sfx_place.py` — CLI orchestrator (ใหม่)

รับ plan JSON แล้ววางทั้งหมดลง timeline ปัจจุบันของ Resolve ที่เปิดอยู่

```
python scripts/sfx_place.py --plan plan.json [--verify] [--dry-run]
```

plan JSON schema (fixed, exact — implementation ต้องใช้คีย์นี้เท่านั้น):

```json
{
  "timeline_name": "ชื่อ timeline (optional, สำหรับตรวจสอบ)",
  "sfx": [
    {
      "sfx_file": "pop-14.wav",
      "timestamp_seconds": 11.95,
      "duration": 0.5,
      "reason": "เย้ — punchline"
    }
  ]
}
```

- `sfx_file`: ชื่อไฟล์ใน `Z:\SFX_processed` หรือ `Z:\SFX` เท่านั้น (ห้าม path สมบูรณ์; CLI แก้ path จาก config/args) — CLI ตรวจว่ามีจริง
- `timestamp_seconds`: ตำแหน่งบน timeline (seconds) แปลงเป็น frame ที่ CLI
- `duration`: ความยาว sting เป็นวินาที (default 0.5); ถ้าไฟล์ยาวกว่า → pre-trim
- `reason`: บังคับ (Hard Limit เดิม "ทุกตำแหน่งต้องบอกเหตุผล 1 บรรทัด")
- CLI flags: `--plan` (required), `--verify` (รัน verify_placements หลังวาง), `--dry-run` (ไม่แตะ Resolve), `--raw-dir`/`--processed-dir` (override default Z:\SFX / Z:\SFX_processed)

- ต่อ Resolve ผ่าน `DaVinciResolveScript` (ใช้ RESOLVE_SCRIPT_API/LIB ตามสคริปต์เดิมใน scripts/)
- อ่าน plan JSON: รายการ `{sfx_file, timestamp_seconds, duration, reason}`
- **เรียกใช้ `SFXPlacer` ที่เขียนเสร็จแล้ว** (src/sfx_engine/placer.py) — ครอบคลุม:
  - หา/สร้าง SFX track (ชื่อ "SFX 1") ผ่าน `find_or_create_sfx_track`
  - ensure `Master/SFX` bin ผ่าน `ensure_sfx_bin`
  - import แบบ dedup ผ่าน `import_sfx_files`
  - pre-trim sting ผ่าน `prepare_sting`/`trim_wav` (workaround ของ Resolve ที่ ignore endFrame)
  - place + verify ผ่าน `execute_plan`/`verify_placements`
- ไม่เขียน logic placement ซ้ำ — CLI เป็น thin wrapper ที่ wired SFXPlacer เข้ากับ handles จริง
- `--dry-run` ตรวจ plan (ไฟล์มีจริง, timestamp ภายใน timeline, ไม่ซ้อนกัน) โดยไม่แตะ Resolve
- พิมพ์ PlacementReport: วางกี่ตัว / ล้มกี่ตัว + เหตุผล / track index / frame จริง

### 2. MCP tool `sfx` ใน server.py (ใหม่, read-only เท่านั้น)

เพิ่ม `@mcp.tool()` หนึ่งตัวใน `davinci-resolve-mcp/src/server.py` ที่ delegate ไปหา `handle_sfx_action` ใน `src/sfx_engine/mcp_tools.py`

- actions ที่เปิด: `scan`, `search`, `analyze`, `plan` — ทั้งหมดเป็น pure-Python ไม่ต้องใช้ Resolve handles
- **ไม่เปิด** `execute`/`verify`/`remove_all` ผ่าน MCP (ต้องใช้ handles จริง → ไปผ่าน CLI ซึ่งต่อตรง Resolve ได้)
- ใช้เป็นตัวช่วย Agent หา candidate beats (`sfx_plan`) แล้ว Agent คัด/แต่งเอง

### 3. `.opencode/skills/adding-sfx/SKILL.md` — เขียนใหม่

คงของที่พิสูจน์แล้วว่าดี:

- Format Table (talking-head / podcast / game / meme / livestream — density, bed, ระดับ SFX, แหล่งหา beat)
- Beat Taxonomy (จังหวะ → SFX ที่เข้ากัน)
- Hard Limits (ห้ามซ้อน, density cap, ห้ามยิงตระกูลเดิมซ้ำ, sting สั้นบนคำเน้นใช้ได้)
- Library ตรวจ (Z:\SFX / Z:\SFX_processed — ใช้เฉพาะชื่อไฟล์ใน list จริง, ห้ามเดา)
- Audio Mixing, Hindsight Pass, Lessons Learned, Verification Checklist, Common Mistakes

เปลี่ยน Workflow:

- เดิม: วิเคราะห์เอง → วางทีละ MCP call → ตรวจ
- ใหม่: วิเคราะห์ (ใช้ sfx MCP tool ช่วยหา beats ได้) → **เขียน plan JSON** → **รัน CLI** → ตรวจ readback

เพิ่ม section:

- CLI usage + plan JSON schema
- ตัวอย่าง plan (โจทย์ meme 34s เดิม 5 sting)
- Fallback: ถ้าไม่มี CLI/Resolve ยังส่งตารางแนะนำได้ (เหมือนเดิม)

### 4. `kimi.plugin.json` — แก้ JSON ที่พัง

เขียนใหม่เป็นโครงสร้างที่ถูกต้อง (name, version, description, skills: [path])

### 5. `scripts/tests_sfx_place.py` — test (ใหม่)

- unit: parse/build plan JSON, dry-run ตรวจ plan (ไฟล์มีจริง, timestamp, ซ้อน), error cases
- ไม่ต้องต่อ Resolve จริง
- เรียกผ่าน `python -m pytest` หรือรันตรงได้ (ใช้ stdlib unittest)

## ไฟล์ที่แตะ

| ไฟล์ | การเปลี่ยนแปลง |
|---|---|
| `scripts/sfx_place.py` | ใหม่ — CLI orchestrator (wires SFXPlacer + handles) |
| `.opencode/skills/adding-sfx/SKILL.md` | เขียนใหม่ทั้งตัว (คงกฎเดิม, เปลี่ยน workflow) |
| `.opencode/skills/adding-sfx/kimi.plugin.json` | แก้ JSON ที่พัง |
| `davinci-resolve-mcp/src/server.py` | +1 tool `sfx` (delegate ไป handle_sfx_action, read-only) |
| `scripts/tests_sfx_place.py` | ใหม่ — test plan logic |

ไม่แตะ: sfx_engine modules (มีอยู่แล้ว), ไฟล์ใน scripts/ อื่นๆ

## ขอบเขตที่ตัดออก (YAGNI / ไว้ทีหลัง)

- ไม่เชื่อม placer เข้ากับ mcp_tools ฝั่ง execute (Resolve handles เข้าถึงยากจาก server.py; CLI ครอบคลุมแล้ว)
- ไม่ทำ C (Resolve Script Plugin) — layer ซ้อน ไม่ได้ใช้จริง
- ไม่แก้ sfx_engine core (analyzer/recommender ทำงานแล้ว)
- ไม่ refactor scripts/ 25 ไฟล์เดิม

## Testing / Verification

1. `python scripts/tests_sfx_place.py` — ผ่าน (plan logic)
2. `--dry-run` บน plan ตัวอย่าง — รายงานถูกต้อง
3. server.py import ได้โดยไม่มี error (`python -c "import src.server"` หรือรัน smoke)
4. Live test (ต้อง Resolve เปิด + timeline): วาง plan ตัวอย่าง 3–5 ตัว แล้ว `--verify` ได้ readback ตรง frame ที่ตั้งใจ
5. ตรวจ SKILL.md workflow ว่าสั่ง Agent ได้ครบโดยไม่พึ่งขั้นตอนที่ไม่มีจริง

## เกณฑ์สำเร็จ

- Agent วาง SFX ครบชุดใน 1 CLI call (ไม่ต้องทำทีละ MCP call)
- placement ตรง frame ที่ตั้งใจ และ verify ผ่าน (อ่าน readback ได้)
- SKILL.md สอน workflow ใหม่ครบ โดยคงกฎคุณภาพเดิมครบ
- kimi.plugin.json เป็น JSON ที่ valid
- server.py ยังทำงานปกติ (tool ใหม่ไม่ breaking)
