---
tags: [emotion, analysis, ai]
created: 2025-08-22
---

# Emotion Analysis

## 概述

ระบบวิเคราะห์อารมณ์จาก 2 แหล่ง:
1. **ใบหน้า (Face)** - ตรวจจับ expression ผ่าน landmarks
2. **เสียง (Voice)** - วิเคราะห์ pitch, volume, speed

## Emotion Signals จาก Face

| Signal | Measurement | Emotion |
|---|---|---|
| mouth_open | > 0.3 | surprise, excitement |
| mouth_smile | > 0.2 | happiness |
| brow_raise | > 0.3 | surprise, fear |
| eye_wide | EAR > 0.35 | surprise, fear |
| eye_narrow | EAR < 0.2 | anger, suspicion |

## Emotion Signals จาก Voice

| Signal | Range | Emotion |
|---|---|---|
| pitch_high | > 200 Hz | excitement, surprise |
| pitch_low | < 100 Hz | sadness, calm |
| volume_high | > -10 dB | anger, excitement |
| volume_low | < -20 dB | sadness, whisper |
| speed_fast | > 5 syllables/s | excitement, anger |
| speed_slow | < 2 syllables/s | sadness, thoughtfulness |

## วิธีใช้งาน

```bash
# วิเคราะห์ใบหน้า
python scripts/face_analyzer.py --video clip.mp4 --output face_emotions.json

# วิเคราะห์เสียง
python scripts/voice_analyzer.py --video clip.mp4 --output voice_emotions.json

# รวมผล
python scripts/emotion_analyzer.py --face face_emotions.json --voice voice_emotions.json --output emotions.json
```

## Integration กับ Skills อื่น

- ผลลัพธ์ส่งต่อให้ `subtitle-driven-enhancement` skill
- ข้อมูลอารมณ์ช่วยลด false positive จาก subtitle text อย่างเดียว
- ใช้ร่วมกับ `adding-sfx` skill ได้โดยตรง

## ลิงก์ที่เกี่ยวข้อง
- [[DaVinci Resolve SFX System]]
- [[SFX Library]]
- [[Subtitle Analysis]]
