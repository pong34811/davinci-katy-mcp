---
tags: [subtitle, analysis]
created: 2025-08-22
---

# Subtitle Analysis

## 概述

ระบบอ่านและวิเคราะห์ subtitle track 1 จาก DaVinci Resolve

## ขั้นตอนการทำงาน

1. **อ่าน Subtitle** - ดึงข้อมูลจาก track 1
2. **วิเคราะห์อารมณ์** - ใช้ keyword matching
3. **ระบุจังหวะ** - หา punchline, reaction, transition
4. **สร้าง Beat List** -  רשימתจังหวะที่ควรเพิ่ม SFX

## Emotion Keywords

| อารมณ์ | คำภาษาไทย | คำภาษาอังกฤษ |
|---|---|---|
| surprise | มาจากไหน, ตกใจ, โอ้โห | wow, omg, surprise |
| excitement | เย้, สุดยอด, เจ๋ง | yay, awesome, amazing |
| success | สำเร็จ, ได้แล้ว, ชนะ | success, win, pass |
| fail | ล้มเหลว, ผิด, ไม่ได้ | fail, wrong, lose |
| emphasis | ตัวเลข, สถิติ, จำนวน | first, second, most |
| question | ทำไม, ยังไง, อะไร | why, how, what |
| transition | ต่อไป, แล้วก็, มาดู | next, then, now |
| closing | ลาก่อน, บาย, ขอบคุณ | bye, see you, thanks |

## วิธีใช้งาน

```bash
# อ่าน subtitle จาก Resolve
python scripts/analyze_subtitles.py --action read

# อ่านจากไฟล์ SRT
python scripts/analyze_subtitles.py --action read --input C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt

# วิเคราะห์จังหวะ
python scripts/analyze_subtitles.py --action analyze --input subtitles.json
```

## Beat Taxonomy

| จังหวะจาก Subtitle | SFX ที่เข้ากัน |
|---|---|
| ตัวเลข / สถิติ | pop, collect, kaching |
| ตกใจ / เซอร์ไพรส์ | impact, pop |
| สำเร็จ / ยินดี | sparkle, ding, collect |
| คำถาม / งง | pop, blip |
| เปิด/ปิดคลิป | sparkle, whoosh-intro |
| คำเน้น / สำคัญ | ding, pop |
| Transition | whoosh-clean, rise |

## ลิงก์ที่เกี่ยวข้อง
- [[DaVinci Resolve SFX System]]
- [[SFX Library]]
- [[Emotion Analysis]]
