---
type: concept
confidence: high
source_count: 1
tags:
  - wiki
  - wiki/concept
---

# โมเดลข้อมูลเครื่องยนต์ SFX

โครงสร้างข้อมูลทั้งหมดของเครื่องยนต์ SFX ที่กำหนดไว้ใน `scripts/main.py` และสคริปต์การวาง SFX

## Enums

### SFXCategory (13 ค่า)

การจำแนกประเภทเสียงเอฟเฟ็กต์เป็นกลุ่มฟังก์ชัน:

| ค่า | คำอธิบาย |
|---|---|
| `COMEDY` | pop, blip, plink, honk, marimba — เครื่องหมายประจักษ์ขำขัน |
| `REACTION` | awkward, huh, awww — เสียงตอบสนองอารมณ์ |
| `IMPACT` | impact, scream, glass — เสียงตีหนัก |
| `ACCENT` | ding, pop, collect, sparkle — เครื่องหมายเน้นเบาๆ |
| `FAIL` | wrong, scratch, bleep — ตัวบ่งชี้ความล้มเหลว/ข้อผิดพลาด |
| `TRANSITION` | whoosh variants, rise — เครื่องหมายเปลี่ยนฉาก |
| `SUCCESS` | collect, kaching, ding, crowd-cheer — ชนะ/ความสำเร็จ |
| `DRAMATIC` | rise, gong, metal, glitch — ตัวสร้างความตึงเครียด |
| `ACTION` | impact, whoosh, explosion, stomp — การกระทำทางกายภาพ |
| `UI` | click, UI-enter, digital, keyboard — เสียงอินเทอร์เฟซ |
| `MUSIC` | harp, guitar, marimba stingers — เสียงเน้นดนตรี |
| `CROWD` | เสียงฝูงชน, เสียงเชียร์, ปรบมือ — ปฏิกิริยาผู้ชม |
| `WHOOSH` | clean, fast, intro whooshes — เสียงการเคลื่อนที่ของอากาศ |

### EventType (12 ค่า)

เหตุการณ์ที่ตรวจจับได้บนวิดีโอไทม์ไลน์ที่กระตุ้นการวาง SFX:

| ค่า | Thai | คำอธิบาย |
|---|---|---|
| `JOKE` | มุก / punchline | จังหวะตลก, คำพูดที่ทำให้หัวเราะ |
| `REACTION` | อึ้ง/งง/เขิน | ปฏิกิริยาตอบสนอง, ความรู้สึก |
| `SURPRISE` | ตกใจ / เซอร์ไพรส์ | ความ surprise, สิ่งที่ไม่คาดคิด |
| `EMPHASIS` | เน้นคำ/ข้อความสำคัญ | ตัวเลข, สถิติ, ข้อความสำคัญ |
| `FAIL` | พลาด / ไม่ทัน | ความล้มเหลว, ความผิดพลาด |
| `TRANSITION` | เปลี่ยน scene | การเปลี่ยน scene, หัวข้อใหม่ |
| `SUCCESS` | สำเร็จ / ได้ของ | ความสำเร็จ, ชัยชนะ |
| `DRAMATIC` | Dramatic / suspense | ความตึงเครียด, ดราม่า |
| `ACTION` | Visual action ใหญ่ | การกระทำที่มีขนาดใหญ่ |
| `UI_NOTIFICATION` | UI / notification | แจ้งเตือน, UI elements |
| `INTRO` | Opening / intro | ช่วงเปิดคลิป |
| `OUTRO` | Closing / outro | ช่วงปิดคลิป |

### ContentFormat (5 ค่า)

การจำแนกรูปแบบเนื้อหาวิดีโอ:

| ค่า | คำอธิบาย |
|---|---|
| `TALKING_HEAD` | Vlog, ผู้พูดคนเดียว — คลิปพูดคนเดียว |
| `PODCAST` | Long form multi-speaker dialogue — รายการสนทนา |
| `GAME` | Gameplay, action, kills, alerts — เกมเพลย์ |
| `MEME` | Short video, high density meme edits — คลิปสั้น/มีม |
| `LIVESTREAM` | Long stream, alert-driven — ถ่ายทอดสด |

## Dataclasses

### SFXFile

แสดงถึงไฟล์เสียงเอฟเฟ็กต์เดียวพร้อม metadata ที่สกัดออกมา

| ฟิลด์ | Type | คำอธิบาย |
|---|---|---|
| `path` | `Path` | เส้นทางไฟล์แบบเต็ม |
| `filename` | `str` | ชื่อไฟล์พร้อมนามสกุล |
| `name` | `str` | ชื่อสั้นที่อ่านเข้าใจได้ |
| `extension` | `str` | `.wav`, `.mp3` |
| `is_processed` | `bool` | `True` ถ้ามาจาก SFX_processed |
| `duration_seconds` | `float` | ระยะเวลาเป็นวินาที (ค่าเริ่มต้น 0.0) |
| `sample_rate` | `int` | Sample rate ใน Hz (ค่าเริ่มต้น 0) |
| `channels` | `int` | จำนวน channel (ค่าเริ่มต้น 0) |
| `file_size_bytes` | `int` | ขนาดไฟล์เป็นไบต์ (ค่าเริ่มต้น 0) |
| `target_db` | `Optional[float]` | ระดับจากชื่อไฟล์ (เช่น -14) |
| `peak_db` | `Optional[float]` | ระดับสูงสุด |
| `rms_db` | `Optional[float]` | ความดัง RMS |
| `category` | `SFXCategory` | การจำแนกประเภท (ค่าเริ่มต้น ACCENT) |
| `tags` | `List[str]` | แท็กการค้นหา |
| `family` | `str` | ชื่อตระกูล (เช่น "whoosh", "pop") |
| `intensity` | `str` | `low`, `medium`, `high` (ค่าเริ่มต้น "medium") |
| `is_sting` | `bool` | ว่าเป็น sting variant หรือไม่ |
| `sting_path` | `Optional[Path]` | เส้นทางไปยัง sting variant |
| `content_hash` | `str` | Hash สำหรับการแคช |

มี `to_dict()` และ `from_dict()` สำหรับการ serialization JSON

### SFXSearchResult

| ฟิลด์ | Type | คำอธิบาย |
|---|---|---|
| `file` | `SFXFile` | ไฟล์ SFX ที่ตรงกัน |
| `score` | `float` | คะแนนความมั่นใจในการตรงกัน (0.0–1.0) |

### TimelineEvent

เหตุการณ์ที่ระบุบนวิดีโอไทม์ไลน์ที่ต้องการพิจารณา SFX

| ฟิลด์ | Type | คำอธิบาย |
|---|---|---|
| `type` | `EventType` | ประเภทเหตุการณ์ |
| `timestamp` | `float` | เวลาเป็นวินาที |
| `description` | `str` | คำอธิบายที่อ่านเข้าใจได้ |
| `impact_score` | `float` | ความสำคัญ 0.0–1.0 (ค่าเริ่มต้น 0.5) |
| `duration` | `float` | ระยะเวลาของหน้าต่างเหตุการณ์ (ค่าเริ่มต้น 0.0) |
| `text_snippet` | `Optional[str]` | ข้อความต้นทางที่กระตุ้นการตรวจจับ |

### BeatPoint

จุด beat ที่มีคะแนนสกัดออกมาสำหรับการจัดแนว SFX ที่เป็นไปได้

| ฟิลด์ | Type | คำอธิบาย |
|---|---|---|
| `timestamp` | `float` | เวลาเป็นวินาที |
| `event_type` | `EventType` | ประเภทเหตุการณ์ |
| `impact_score` | `float` | คะแนนที่ปรับ format แล้ว |
| `description` | `str` | คำอธิบายที่อ่านเข้าใจได้ |

### SFXPlacement

แทนการวาง SFX ที่วางแผนไว้บือไทม์ไลน์

| ฟิลด์ | Type | คำอธิบาย |
|---|---|---|
| `sfx` | `SFXFile` | ไฟล์ SFX ที่จะวาง |
| `timestamp` | `float` | เวลาวางเป็นวินาที |
| `beat` | `BeatPoint` | จุด beat ที่การวางนี้ตอบสนอง |
| `volume_db` | `float` | ระดับเสียง (ค่าเริ่มต้น -14.0) |
| `record_frame` | `int` | เลขเฟรมไทม์ไลน์ (ค่าเริ่มต้น 0) |
| `duration_seconds` | `float` | ระยะเวลา SFX (ค่าเริ่มต้น 0.5) |
| `track_index` | `int` | Track เสียงเป้าหมาย (ค่าเริ่มต้น 2) |
| `confidence` | `float` | ความมั่นใจในการวาง (ค่าเริ่มต้น 0.8) |
| `reason` | `str` | เหตุผลที่วาง SFX นี้ในจังหวะนี้ |

มี `to_dict()` สำหรับ JSON serialization

### SFXPlan

แผนคำแนะนำ SFX ครบถ้วนสำหรับไทม์ไลน์วิดีโอ

| ฟิลด์ | Type | คำอธิบาย |
|---|---|---|
| `format` | `ContentFormat` | format เนื้อหาที่ตรวจจับ |
| `placements` | `List[SFXPlacement]` | รายการ placement ที่เรียงลำดับ |
| `timeline_duration_seconds` | `float` | ความยาวไทม์ไลน์รวม |
| `fps` | `float` | เฟรมต่อวินาที (ค่าเริ่มต้น 60.0) |
| `density_per_minute` | `float` | จำนวน SFX ต่อนาที |
| `warnings` | `List[str]` | คำเตือนคุณภาพ |
| `spacing_violations` | `List[str]` | การวางวัดชิดกันเกินไป |

มี `to_dict()` สำหรับ JSON serialization

## How Models Flow (การไหลของโมเดล)

```
SFXFile (library scan)
  → SFXSearchResult (query match)
    → BeatPoint (event detection + format scoring)
      → SFXPlacement (file + beat + position + volume)
        → SFXPlan (complete timeline)
```

1. **SFXFile** — library scanner อ่านไฟล์เสียง, สกัด metadata, จำแนกตาม category/family
2. **SFXSearchResult** — search engine จับคู่ไฟล์กับ queries, คืนผลลัพธ์ที่มีคะแนน
3. **TimelineEvent** — analyzer ตรวจจับการจับคู่ keyword ใน subtitle/transcript, สร้าง timestamped events
4. **BeatPoint** — events ถูกปรับ format (PODCAST suppresses JOKE×0.4, GAME boosts ACTION×1.3)
5. **SFXPlacement** — placer เลือกไฟล์ SFX ที่ดีที่สุดสำหรับแต่ละ beat, คำนวณ frame position และ volume
6. **SFXPlan** — ทุก placement ถูกรวบรวมพร้อม density checks, spacing validation, และ warnings

## Related

- [[library-scanner]] — scanning and taxonomy
- [[search-engine]] — fuzzy matching and event search
- [[family-mapping]] — family → filename mapping
- [[system-config]] — configuration and paths