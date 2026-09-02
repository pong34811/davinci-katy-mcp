---
tags: [project, davinci-resolve, sfx]
created: 2025-08-22
status: active
---

# DaVinci Resolve SFX System

## ข้อมูลทั่วไป
- **สถานะ:** Active
- **วันที่เริ่ม:** 2025-08-22
- **เป้าหมาย:** สร้างระบบ AI สำหรับเพิ่ม SFX ให้คลิปอัตโนมัติ

## รายละเอียด

ระบบจะอ่าน subtitle track 1 จาก DaVinci Resolve แล้วใช้ AI วิเคราะห์เนื้อหาเพื่อ:
1. ระบุจังหวะสำคัญ
2. วิเคราะห์อารมณ์
3. สร้าง SFX plan
4. วางอัตโนมัติ

## โครงสร้างโปรเจค

```
davinci-katy-mcp/
├── scripts/
│   ├── analyze_subtitles.py    # อ่าน subtitle track 1
│   ├── generate_sfx_plan.py    # สร้าง SFX plan
│   ├── clip_enhancer.py        # Script หลัก
│   ├── face_analyzer.py        # วิเคราะห์ใบหน้า
│   ├── voice_analyzer.py       # วิเคราะห์เสียง
│   ├── emotion_analyzer.py     # รวมผลวิเคราะห์
│   └── sfx_place.py            # วาง SFX
├── SFX/                         # ไฟล์ SFX
└── .opencode/skills/            # Skills
```

## ขั้นตอนการทำงาน

1. **อ่าน Subtitle** → `analyze_subtitles.py`
2. **วิเคราะห์เนื้อหา** → ระบุอารมณ์/จังหวะ
3. **สร้าง SFX Plan** → `generate_sfx_plan.py`
4. **วาง SFX** → `sfx_place.py`

## SFX Library

| Family | ไฟล์ | จังหวะที่เหมาะ |
|---|---|---|
| pop | Pop - Short 06.mp3 | surprise, emphasis |
| ding | Bell - Ding 02.wav | emphasis, success |
| collect | Game - Correct Collect Answer.mp3 | success |
| sparkle | Harp - Sparkle 01.mp3 | excitement, closing |
| whoosh | Whoosh - Clean Fast.mp3 | transition |
| impact | Impact - Comedy Hit 01.mp3 | surprise |
| wrong | Game - Wrong Answer.mp3 | fail |

## วิธีใช้

```bash
# วิเคราะห์ subtitle + สร้าง plan
python scripts/clip_enhancer.py --srt subtitle_from_track1.srt --skip-place

# วางจริง
python scripts/sfx_place.py --plan plan.json --verify
```

## บันทึก

## ลิงก์ที่เกี่ยวข้อง
- [[SFX Library]]
- [[Emotion Analysis]]
- [[Subtitle Analysis]]
