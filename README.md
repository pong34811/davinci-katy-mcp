# DaVinci Resolve SFX System

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
cd davinci-katy-mcp

# ติดตั้ง dependencies
pip install opencv-python mediapipe pytest

# ทดสอบระบบ
python scripts/main.py status
```

## วิธีใช้งาน

### ใช้ main.py (แนะนำ)

```bash
# แสดงสถานะระบบ
python scripts/main.py status

# วิเคราะห์ subtitle
python scripts/main.py analyze --srt subtitle_from_track1.srt

# สร้าง SFX plan
python scripts/main.py plan --beats beats.json --format talking-head

# วาง SFX
python scripts/main.py place --plan plan.json --verify

# ทำทุกขั้นตอน
python scripts/main.py enhance --srt subtitle_from_track1.srt --skip-place
```

### ใช้ scripts แยก

```bash
# อ่าน subtitle
python scripts/analyze_subtitles.py --action read --input subtitle_from_track1.srt

# วิเคราะห์อารมณ์
python scripts/face_analyzer.py --video clip.mp4 --output face_emotions.json
python scripts/voice_analyzer.py --video clip.mp4 --output voice_emotions.json
python scripts/emotion_analyzer.py --face face_emotions.json --voice voice_emotions.json

# สร้าง SFX plan
python scripts/generate_sfx_plan.py --beats beats.json --format talking-head

# วาง SFX
python scripts/sfx_place.py --plan plan.json --verify
```

## โครงสร้างโปรเจค

```
davinci-katy-mcp/
├── scripts/
│   ├── config.py                 # Configuration กลาง
│   ├── main.py                   # Entry point หลัก
│   ├── analyze_subtitles.py      # อ่าน subtitle
│   ├── generate_sfx_plan.py      # สร้าง SFX plan
│   ├── clip_enhancer.py          # Script หลัก
│   ├── face_analyzer.py          # วิเคราะห์ใบหน้า
│   ├── voice_analyzer.py         # วิเคราะห์เสียง
│   ├── emotion_analyzer.py       # รวมผลวิเคราะห์
│   └── sfx_place.py              # วาง SFX
├── tests/
│   ├── test_config.py
│   └── test_analyze_subtitles.py
├── davinci-resolve-mcp/          # MCP Server
├── SFX/                          # ไฟล์ SFX
├── SFX_processed/                # ไฟล์ SFX ที่ normalize แล้ว
├── .opencode/skills/             # Skills
└── obsidian-vault/               # Obsidian vault
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

## ทดสอบ

```bash
# รัน tests ทั้งหมด
python -m pytest tests/ -v

# รัน tests สำหรับ config
python -m pytest tests/test_config.py -v

# รัน tests สำหรับ analyze_subtitles
python -m pytest tests/test_analyze_subtitles.py -v
```

## Skills ที่ติดตั้ง

- adding-sfx - สำหรับเพิ่ม SFX ลง timeline
- subtitle-driven-enhancement - สำหรับปรับแต่งคลิปจาก subtitle
- emotion-analysis - สำหรับวิเคราะห์อารมณ์
- obsidian-best-practices - สำหรับพัฒนา Obsidian plugin
- obsidian-cli - สำหรับจัดการ Obsidian vault
- และอื่นๆ อีก 20+ skills

## ลิงก์ที่เกี่ยวข้อง

- [[DaVinci Resolve SFX System]]
- [[SFX Library]]
- [[Emotion Analysis]]
- [[Subtitle Analysis]]
