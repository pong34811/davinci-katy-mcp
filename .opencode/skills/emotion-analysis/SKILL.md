---
name: emotion-analysis
description: ใช้เมื่อต้องการวิเคราะห์อารมณ์จากใบหน้าและเสียงในคลิปวิดีโอ — "วิเคราะห์อารมณ์จากคลิป", "analyze emotions from clip", "face emotion analysis", "voice emotion analysis", "อารมณ์ในคลิป". ใช้ร่วมกับ subtitle-driven-enhancement skill เพื่อเพิ่มความแม่นยำในการเลือก SFX
---

# Emotion Analysis from Face & Voice

## บทบาท: วิเคราะห์อารมณ์จาก 2 แหล่ง

ระบบจะวิเคราะห์อารมณ์จาก 2 แหล่งพร้อมกัน:
1. **ใบหน้า (Face)** — ตรวจจับ expression ผ่าน landmarks (mouth, brow, eyes)
2. **เสียง (Voice)** — วิเคราะห์ pitch, volume, speed จาก audio track

ผลลัพธ์จะถูก combine เพื่อได้อารมณ์ที่แม่นยำกว่าการอ่าน subtitle เพียงอย่างเดียว

## Workflow

### ขั้นตอนที่ 1: วิเคราะห์ใบหน้า
```bash
python scripts/face_analyzer.py --video clip.mp4 --output face_emotions.json
```
- ใช้ OpenCV + MediaPipe ตรวจจับ face landmarks
- วิเคราะห์ mouth open, brow raise, eye aspect ratio
- แปลงเป็น emotion signals: surprise, happiness, anger, fear

### ขั้นตอนที่ 2: วิเคราะห์เสียง
```bash
python scripts/voice_analyzer.py --audio clip.wav --output voice_emotions.json
```
- วิเคราะห์ pitch (Hz), volume (dB), speaking rate
- ตรวจจับ: excitement (pitch สูง), anger (volume สูง), sadness (pitch ต่ำ)

### ขั้นตอนที่ 3: รวมผล
```bash
python scripts/emotion_analyzer.py --face face_emotions.json --voice voice_emotions.json --output emotions.json
```
- Combine face + voice signals
- คำนวณ confidence score
- สร้าง timeline อารมณ์

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

## Integration กับ Skills อื่น

- ผลลัพธ์ส่งต่อให้ `subtitle-driven-enhancement` skill เพื่อปรับปรุง SFX plan
- ข้อมูลอารมณ์ช่วยลด false positive จาก subtitle text อย่างเดียว
- ใช้ร่วมกับ `adding-sfx` skill ได้โดยตรง

## ข้อจำกัด

- ต้องมีวิดีโอไฟล์สำหรับ face analysis (ไม่ใช่ audio-only)
- ต้องมี audio track สำหรับ voice analysis
- Face detection ต้องการ OpenCV + MediaPipe
- Voice analysis ใช้ Python stdlib (wave, struct) สำหรับ basic analysis
