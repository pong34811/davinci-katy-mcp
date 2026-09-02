---
name: subtitle-driven-enhancement
description: ใช้เมื่อปรับแต่งคลิปวิดีโอโดยอ่าน SRT file ที่ `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` แล้วเพิ่ม SFX/เอฟเฟกต์ให้คลิปน่าสนใจขึ้น — "ปรับแต่งคลิปจาก SRT", "เพิ่ม SFX จาก subtitle", "enhance clip from subtitles", "make clip interesting from subtitles", "subtitle-driven editing". ใช้กับคลิปทุกรูปแบบ: talking-head, vlog, podcast, game, meme, livestream
---

# Subtitle-Driven Clip Enhancement

## บทบาท: อ่าน subtitle → วิเคราะห์ → เพิ่มความน่าสนใจ

ระบบจะอ่าน SRT file ที่ `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` แล้วใช้ AI วิเคราะห์เนื้อหาเพื่อ:
1. **ระบุจังหวะสำคัญ** — จุดที่ควรเพิ่ม SFX/เอฟเฟกต์
2. **วิเคราะห์อารมณ์** — แต่ละช่วงมีอารมณ์อะไร (ตลก, ตกใจ, สำเร็จ, ล้มเหลว)
3. **สร้าง SFX plan** — แนะนำ SFX ที่เหมาะสมพร้อม timestamp
4. **วางอัตโนมัติ** — ใช้ CLI วาง SFX ลง timeline

## Workflow

### ขั้นตอนที่ 1: อ่าน Subtitle จาก SRT File
```bash
python scripts/analyze_subtitles.py --action read --srt "C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt"
```
- อ่าน subtitle จากไฟล์ SRT ที่ `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
- แสดงผลเป็นตาราง: index, start, end, text
- บันทึกเป็น JSON สำหรับขั้นตอนถัดไป

### ขั้นตอนที่ 2: วิเคราะห์เนื้อหา
```bash
python scripts/analyze_subtitles.py --action analyze --input subtitles.json
```
- วิเคราะห์แต่ละ subtitle segment
- ระบุอารมณ์/จังหวะสำคัญ (punchline, reaction, transition, emphasis)
- สร้าง beat list พร้อม timestamp

### ขั้นตอนที่ 3: สร้าง SFX Plan
```bash
python scripts/generate_sfx_plan.py --beats beats.json --format talking-head
```
- จับคู่ beat กับ SFX ตาม Beat Taxonomy
- สร้าง plan JSON ตาม schema ของ sfx_place.py
- ตรวจสอบ density, spacing, family repetition

### ขั้นตอนที่ 4: วาง SFX
```bash
davinci-resolve-mcp/venv/Scripts/python.exe davinci-resolve-mcp/venv/Scripts/python.exe scripts/sfx_place.py --plan plan.json --dry-run  # ตรวจสอบก่อน
davinci-resolve-mcp/venv/Scripts/python.exe davinci-resolve-mcp/venv/Scripts/python.exe scripts/sfx_place.py --plan plan.json --verify    # วางจริง
```

## Beat Taxonomy (จาก Subtitle)

| จังหวะจาก Subtitle | SFX ที่เข้ากัน |
|---|---|
| ตัวเลข / สถิติ (1,649, 1000) | pop, collect, kaching |
| ตกใจ / เซอร์ไพรส์ (มาจากไหน, ตกใจหมดเลย) | impact, pop |
| สำเร็จ / ยินดี (เย้, ขอบคุณ) | sparkle, ding, collect |
| คำถาม / งง (มาจากไหน) | pop, blip |
| เปิด/ปิดคลิป | sparkle, whoosh-intro |
| คำเน้น / สำคัญ | ding, pop |
| Transition / เปลี่ยนเรื่อง | whoosh-clean, rise |

## Format Detection

ดูจาก subtitle content + บริบท:
- **Subtitles สั้น ตัดเร็ว** → Game/Meme style (density สูง)
- **Subtitles ยาวต่อเนื่อง** → Talking-head style (density 3-5/นาที)
- **Subtitles มี dialogue หลายผู้พูด** → Podcast style (density ต่ำ)

## ข้อจำกัด

- อ่านเฉพาะ SRT file เท่านั้น — `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`
- SFX ต้องไม่ทับเสียงหลัก (ดูจาก subtitle timing)
- Density ตาม Format Table
- ทุก SFX ต้องมี `reason` 1 บรรทัด
- ใช้ SFX library ที่มีอยู่จริง (Z:\SFX_processed)

## Integration กับ Skills อื่น

- ใช้ร่วมกับ `adding-sfx` skill สำหรับการวาง SFX
- ข้อมูล subtitle สามารถส่งต่อให้ `adding-sfx` skill ได้โดยตรง
- Plan JSON format เดียวกันกับ `sfx_place.py`
