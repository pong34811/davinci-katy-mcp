---
tags: [docs, readme]
created: 2025-08-22
---

# DaVinci Resolve SFX System

## เกี่ยวกับโปรเจค

ระบบ AI สำหรับเพิ่ม Sound Effects ให้คลิปวิดีโอใน DaVinci Resolve โดยอัตโนมัติ

## ฟีเจอร์หลัก

1. **อ่าน Subtitle Track 1** - ดึงข้อความจาก subtitle อัตโนมัติ
2. **วิเคราะห์อารมณ์** - ใช้ AI วิเคราะห์อารมณ์จากใบหน้าและเสียง
3. **สร้าง SFX Plan** - แนะนำ SFX ที่เหมาะสมตามจังหวะ
4. **วางอัตโนมัติ** - วาง SFX ลง timeline โดยไม่ต้องทำมือ

## การติดตั้ง

### ความต้องการ
- DaVinci Resolve (Studio หรือ Free)
- Python 3.8+
- OpenCV (สำหรับ face analysis)
- MediaPipe (สำหรับ face landmarks)

### ขั้นตอนการติดตั้ง

```bash
# Clone โปรเจค
git clone <repository-url>

# ติดตั้ง dependencies
pip install opencv-python mediapipe

# ทดสอบระบบ
python scripts/analyze_subtitles.py --action read --input subtitle_from_track1.srt
```

## วิธีใช้งาน

### ขั้นตอนที่ 1: อ่าน Subtitle

```bash
python scripts/analyze_subtitles.py --action read --input subtitle_from_track1.srt
```

### ขั้นตอนที่ 2: วิเคราะห์และสร้าง Plan

```bash
python scripts/clip_enhancer.py --srt subtitle_from_track1.srt --skip-place
```

### ขั้นตอนที่ 3: วาง SFX

```bash
python scripts/sfx_place.py --plan plan.json --verify
```

## โครงสร้างโปรเจค

```
davinci-katy-mcp/
├── scripts/
│   ├── analyze_subtitles.py    # อ่าน subtitle
│   ├── generate_sfx_plan.py    # สร้าง SFX plan
│   ├── clip_enhancer.py        # Script หลัก
│   ├── face_analyzer.py        # วิเคราะห์ใบหน้า
│   ├── voice_analyzer.py       # วิเคราะห์เสียง
│   ├── emotion_analyzer.py     # รวมผลวิเคราะห์
│   └── sfx_place.py            # วาง SFX
├── SFX/                         # ไฟล์ SFX
├── SFX_processed/               # ไฟล์ SFX ที่ normalize แล้ว
└── .opencode/skills/            # Skills สำหรับ AI
```

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

## Skills ที่ติดตั้ง

1. **adding-sfx** - สำหรับเพิ่ม SFX ลง timeline
2. **subtitle-driven-enhancement** - สำหรับปรับแต่งคลิปจาก subtitle
3. **emotion-analysis** - สำหรับวิเคราะห์อารมณ์
4. **obsidian-best-practices** - สำหรับพัฒนา Obsidian plugin
5. **obsidian-cli** - สำหรับจัดการ Obsidian vault

## Obsidian Plugin

### SFX Manager Plugin
- จัดการ SFX library จาก Obsidian
- สแกนไฟล์ SFX
- แสดงรายการ SFX ตามหมวดหมู่

### การติดตั้ง Plugin
1. คัดลอกโฟลเดอร์ `Plugins/sfx-manager` ไปที่ `.obsidian/plugins/`
2. เปิด Obsidian แล้วไปที่ Settings > Community plugins
3. เปิดใช้งาน "SFX Manager"

## การแก้ไขปัญหา

### ปัญหา: ไม่สามารถเชื่อมต่อกับ DaVinci Resolve ได้
- ตรวจสอบว่า DaVinci Resolve กำลังทำงานอยู่
- ตรวจสอบว่าเปิดใช้งาน External scripting

### ปัญหา: SFX file ไม่พบ
- ตรวจสอบ path ใน settings
- รันคำสั่ง `python scripts/analyze_subtitles.py --action scan` เพื่อสแกนไฟล์

## ลิงก์ที่เกี่ยวข้อง

- [[DaVinci Resolve SFX System]]
- [[SFX Library]]
- [[Emotion Analysis]]
- [[Subtitle Analysis]]
