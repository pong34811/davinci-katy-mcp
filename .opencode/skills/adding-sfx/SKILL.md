---
name: adding-sfx
description: ใช้เมื่อเพิ่ม Sound Effects (SFX) ลงใน timeline ของ DaVinci Resolve เพื่อทำให้คลิปสนุก มีจังหวะ และน่าสนใจขึ้น — "เพิ่ม SFX", "เพิ่มเสียงประกอบ", "ใส่เสียงตลก", "เพิ่ม Sound Effects (SFX)", "add SFX", "sound effects", "make the clip more interesting/lively". ใช้กับคลิปทุกรูปแบบ: talking-head/vlog, podcast, game footage, meme, livestream. ใช้ด้วยเมื่อเจอ brief ลักษณะ "งานที่ต้องดำเนินการ: เพิ่ม SFX ให้กับคลิปวิดีโอ" / "เริ่มดำเนินการแก้ไขคลิปวิดีโอ" และเมื่อ review/ตรวจสอบ SFX ที่วางอยู่แล้วว่าควรปรับ/ลบ/เพิ่มตรงไหน
---

# Adding SFX ลง Timeline ของ DaVinci Resolve

## บทบาท: Agent วางแผน, CLI ลงมือ

แบ่งงานเป็นสองฝ่าย — **Agent ตัดสินใจคุณภาพ, CLI วางอัตโนมัติ**:
- **Agent** (คุณ): ระบุ format, วิเคราะห์จังหวะ, เลือกเสียง, เขียนเหตุผล, สร้าง **plan JSON**
- **CLI** (`python scripts/sfx_place.py`): สร้าง SFX track, import ลง Media Pool, trim sting, วางทุกตัวในครั้งเดียว, verify readback

**ห้ามสลับบทบาท:** อย่าวาง SFX ทีละตัวผ่าน MCP tools อีกต่อไป (ช้าและผิดพลาดง่าย) — เขียน plan แล้วให้ CLI วางทั้งชุด แก้/เพิ่มทีหลังก็ผ่าน plan ใหม่

## หลักการ

SFX คือเครื่องปรุง ไม่ใช่ตัวอาหาร จุดประสงค์คือคลิปที่**มีชีวิตชีวาและตั้งใจ** ไม่ใช่คลิปที่ทุกช่วงมีเสียง SFX ทุกตัวต้อง**มีเหตุผล**ว่ามันช่วยจังหวะ/อารมณ์ตอนไหน (มุก, reaction, ตกใจ, เน้นคำ, transition, dramatic, fail, สำเร็จ) ห้ามสุ่มใส่ ห้ามทับเสียงพูด

## ระบุรูปแบบคลิปก่อน (Format Detection) — ทำเป็นขั้นตอนแรกเสมอ

ดูจากบริบท (transcript, ภาพ, ความยาว, จำนวนผู้พูด, มี game audio/music ไหม) แล้วเลือกคอลัมน์ที่ตรงที่สุดจากตารางด้านล่าง **ค่า default ทั้งหมดอ่านจากตารางนี้** — อย่าใช้ค่า talking-head ไปกับ meme:

| รูปแบบ | Density (SFX/นาที) | เสียงหลัก (bed) | ระดับ SFX เทียบ bed | แหล่งหา beat | กฎพิเศษ |
|---|---|---|---|---|---|
| **Talking-head / vlog** | 3–5 | เสียงพูด | −10 ถึง −16 dB | transcript | sting สั้นบนคำเน้นใช้ได้ |
| **Podcast** (2+ ผู้พูด, ยาว, เน้นบทพูด) | เกือบ 0 (1–2/segment) | เสียงพูด + music bed | ต่ำสุด | wordplay, เน้นคำ, หัวข้อใหม่ | งด SFX บนมุกเล็ก, ห้ามทับคาบบทสนทนา |
| **Game** (action, kill, UI) | 5–8 (คูณ 1.5–2× ของ talking-head) | game audio | ตั้งกว่าได้ (bed กลบ) | kill/death/respawn, UI popup, power-up, เปลี่ยนฉาก | เร็ว+หนักได้, 2 ตัวชิดกันได้ถ้าเป็น action คู่ (kill+collect) |
| **Meme** (สั้น, มุกจ๋า) | สูง (เสียงคือมุก) | ไม่มี dialogue | ปกติ | จังหวะมุก, ภาพปั่น, punchline | **พักกฎ "ความยับยั้ง"** — ซ้ำตระกูลเพื่อความตลกได้, เสียงผิดจังหวะเป็นมุกได้เอง |
| **Livestream** (ยาว, alert) | ต่อชั่วโมง (alert-driven) | เสียงสตรีมเมอร์ + game + music | ต่ำสุด อย่าทับ alert | sub/follow/donation alert, เปลี่ยน segment, BRB | วางตามเหตุการณ์ alert ไม่ใช่วินาที, แยก "bed ต่อเนื่อง" vs "alert sting" |

**ถ้าระบุไม่ได้/คลุมเครือ** → ถามผู้ใช้สั้น ๆ ว่าคลิปเป็นรูปแบบไหน หรือใช้ค่า conservative (talking-head) เป็น default แล้วบอกในสรุป

## ตรวจ Library ก่อนเสมอ

มี 2 โฟลเดอร์ — **เรียก `sfx` MCP tool (`action="scan"`) เพื่อ list จริงทุกครั้งก่อนเริ่ม** แล้วอ้างถึงเฉพาะไฟล์ที่อยู่ใน list เท่านั้น:

- `Z:\SFX` — ไฟล์ต้นฉบับ (71 ไฟล์, mp3/wav)
- `Z:\SFX_processed` — **ควรใช้เป็นหลัก** ไฟล์ wav ที่ normalize ระดับเสียงไว้แล้ว โดยชื่อไฟล์บอกระดับเสียง: `<shortname>-<dB>.wav` เช่น `pop-14.wav` = Pop ที่ −14 dB

**ห้ามเดา/สร้างชื่อไฟล์เอง** ถ้าไม่อยู่ใน list = ห้ามใช้

ตารางจับคู่ processed → raw (อ้างอิงเท่านั้น, ระดับเสียงดูจากชื่อไฟล์จริง):

| processed | raw |
|---|---|
| awkward | Awkward Moment |
| blip | Comedy - Silly Blip 01 |
| collect | Game - Correct Collect Answer |
| ding | Bell - Ding 02 |
| gong | Gong - Comical Metal |
| honk1 / honk2 | Horn - Duck Honk 01 / 02 |
| impact | Impact - Comedy Hit 01 |
| kaching | Cash Register - Ka Ching 01 |
| plink | Guitar - Plink Slide 13 |
| pop | Pop - Short 06 |
| rise | Rise - Build Up |
| scratch | Scratch - Turntable Record |
| sparkle | Harp - Sparkle 01 |
| whoosh-clean | Whoosh - Clean Fast |
| whoosh-fast | Whoosh - Fast 01 |
| whoosh-intro | Transition - Whoosh 01 |
| wrong | Game - Wrong Answer |

## จังหวะ → SFX (Beat Taxonomy)

เลือก SFX ตาม **เหตุการณ์ + จังหวะ + อารมณ์** ของช่วงนั้น:

| จังหวะ | SFX ที่เข้ากัน (ตัวอย่างจาก library) |
|---|---|
| มุก / punchline | pop, blip, plink, honk, marimba, awkward |
| Reaction (อึ้ง/งง/เขิน) | awkward, huh, awww |
| ตกใจ / เซอร์ไพรส์ | impact, scream, glass, pop |
| เน้นคำ/ข้อความสำคัญ | ding, pop, collect |
| Fail / พลาด / ไม่ทัน | wrong, scratch, bleep |
| Transition / เปลี่ยน scene | whoosh-clean / whoosh-fast / whoosh-intro, rise |
| สำเร็จ / ได้ของ / ถูกต้อง | collect, kaching, ding, crowd-cheer, sparkle |
| Dramatic / suspense | rise, gong, metal, glitch |
| Visual action ใหญ่ | impact, whoosh, explosion, stomp |
| UI / notification | click, UI-enter, digital, keyboard |

**กฎจับคู่:** เหตุการณ์ยังไง → เลือกจากแถวที่ตรงที่สุด แล้วให้เสียงเข้ากับระดับความแรงของจังหวะ (มุกเบา → pop/plink, จังหวะใหญ่ → impact/rise) อย่าใส่เสียงเล็กสุดสำหรับจังหวะใหญ่สุด และอย่าใส่เสียงดังสุดสำหรับมุกเบา

## ข้อจำกัดการวาง (Hard Limits)

- **บทพูดคือกฎหลัก แต่ sting สั้นบนคำเน้นใช้ได้:** ตำแหน่งที่ตั้งใจ (คำเน้น, ตัวเลขสำคัญ, punchline) วาง sting สั้น ~0.5s ที่ระดับ −10 ถึง −16dB ทับบนคำพูดนั้นได้โดยไม่กลบ speech สิ่งที่ห้ามคือ**เสียงยาว/ดังที่ทับ speech** (rise 2s ทับทั้งประโยค = ห้าม) สำหรับเนื้อหาพูดต่อเนื่อง (talking-head/vlog) ที่แทบไม่มีช่องว่าง กฎนี้คือเส้นแบ่งหลัก — sting สั้นๆ บนจังหวะ OK, เสียงยืดเยื้อทับพูดไม่ OK
- **Density cap:** อ่านค่าจาก **Format Table** ตามรูปแบบที่ระบุได้ (talking-head 3–5/นาที, game 5–8, podcast เกือบ 0, meme สูง, livestream alert-driven) — ห้ามเกินค่าของตาราง และทุกตัวต้องยังห่างกันอย่างน้อย ~1 วินาที ยกเว้น game 2 ตัวชิดกันที่เป็น action คู่
- **ห้ามซ้อน:** ห้ามมี 2 SFX ทับกันหรือห่างกันไม่ถึง ~1 วินาที (เสียงดัง 1 ตัวต่อจังหวะ เลือกตัวที่แรงกว่า)
- **ห้ามยิงตระกูลเดิมซ้ำ:** ไม่ใช้ตระกูลเดียวกัน (whoosh×3, harp×2) ใกล้กัน ต้องสลับ
- **ทุกตำแหน่งต้องบอกเหตุผล 1 บรรทัด** ถ้าบอกไม่ได้ว่ามันช่วยจังหวะไหน → ตัดทิ้ง
- ให้ความสำคัญกับจุด Impact ต่อผู้ชมมากที่สุด อย่าใส่ทุกประโยค ทุกการตัดต่อ

## Impact Scoring (New!) — Multi-Factor Analysis

**ระบบคะแนน Impact 7 มิติ** แทนที่ keyword matching แบบเดิม:

| มิติ | น้ำหนั่ก | สัญญาณ |
|------|---------|---------|
| Comedy | 15% | หัวเราะ, มุก, sarcasm |
| Emotion | 20% | คำอารมณ์ไทย/อังกฤษ, particles |
| Surprise | 20% | อุทาน, disbelief |
| Emphasis | 15% | ตัวเลข, เปอร์เซ็นต์, อันดับ |
| Transition | 10% | เปลี่ยนฉาก, หัวข้อ |
| Retention | 10% | คำถาม, teaser, curiosity |
| Context | 10% | story arc position, surrounding |

**Impact Levels:**
- CRITICAL (≥0.7): วาง SFX เสมอ
- HIGH (0.5-0.7): Strong candidate
- MEDIUM (0.3-0.5): Consider if density allows
- LOW (0.15-0.3): Skip unless empty
- NONE (<0.15): Never place

**กฎสำคัญ:**
1. ไม่ทุก subtitle ต้องการ SFX — เฉพาะ impact ≥ 0.3
2. Context matters — "but" ก่อน surprise = +score
3. Sarcasm = comedy อัตโนมัติ
4. Punchlines ได้ +0.15 bonus
5. Transitions threshold ต่ำกว่า (≥0.2)

**เครื่องมือ:** `scripts/impact_scorer.py` — `ImpactScorer.score_transcript()`

## Story Arc Analysis (New!)

**อ่าน 3-5 subtitle ก่อน/หลังก่อนตัดสิน:**

```
Setup → Build-up → Turning Point → Punchline → Reaction → Resolution
 neutral   tension     shift        impact     response   calm
```

**Detection Rules:**
| Position | Detection | SFX Priority |
|----------|-----------|-------------|
| Setup | Start of video, intro | LOW |
| Build-up | Creating tension, "but" | MEDIUM |
| Turning Point | Emotional shift | HIGH |
| Punchline | Short punchy text | CRITICAL |
| Reaction | "really?", "what?" | HIGH |
| Resolution | Closing, "bye" | MEDIUM |

**เครื่องมือ:** `scripts/story_arc_analyzer.py` — `StoryArcAnalyzer.analyze()`

## Timing Intelligence (New!)

**Precise timing decisions:**
- Pre-hit (-0.1s): Anticipation before punchline
- On-hit (0.0s): Exact moment of impact
- Post-hit (+0.2s): Reaction after event

**Timing Presets:**
| Event | Timing | Duration |
|-------|--------|----------|
| Punchline | Pre-hit | 0.4s |
| Surprise | On-hit | 0.3s |
| Reaction | Post-hit | 0.5s |
| Emphasis | On-hit | 0.3s |
| Transition | Pre-hit | 0.8s |
| Fail | On-hit | 0.5s |

**Spacing:** Min gap 0.5s from adjacent SFX

**เครื่องมือ:** `scripts/timing_intelligence.py` — `TimingIntelligence.decide_timing()`

## SFX Evaluation Framework (New!)

**9-Dimension Quality Scoring:**
1. Context Accuracy (15%)
2. SFX Relevance (15%)
3. Timing Accuracy (15%)
4. Emotional Match (15%)
5. Intensity Match (10%)
6. Audio Clarity (10%)
7. Non-Intrusiveness (10%)
8. Variety (5%)
9. Viewer Engagement (5%)

**Grading:** A (8.5+), B (7-8.4), C (5.5-6.9), D (4-5.4), F (<4)

**เครื่องมือ:** `scripts/sfx_evaluator.py` — `SFXEvaluator.evaluate()`

## Negative Knowledge (Anti-Patterns)

**When to SKIP SFX:**
- Neutral filler (impact < 0.15)
- Continuous speech without peaks
- Over-saturation (density exceeded)
- Context conflict
- Weak reason (can't explain WHY)

**Common Mistakes:**
- SFX on every subtitle → audio fatigue
- Same family 3+ times → monotony
- Loud SFX over speech → destroys clarity
- Long SFX (>2s) on short segments → overwhelms
- Ignoring context → misses setup→punchline
- Placing on setup not punchline → wastes impact

## Workflow — 3-Round Subtitle Analysis

ทุกครั้งที่มี transcript/subtitle ให้วิเคราะห์ **3 รอบ** ก่อนเขียน plan — ห้ามข้ามรอบ ห้ามทำรอบเดียวจบ

### Step 0 — Setup

เรียก `sfx` MCP tool (`action="scan"`) เพื่อ list library จริง, ดู timeline ปัจจุบัน (`timeline.get_current`), audio track (`timeline.probe_audio_track`), frame rate (`project_settings.get_setting("timelineFrameRate")`), อ่าน transcript (`timeline.get_transcript` with_timecodes=true). ระบุรูปแบบคลิปจาก Format Table

### Round 1 — Structural Scan (โครงสร้าง)

**เป้าหมาย:** เข้าใจภาพรวมของคลิป — ไม่เลือก SFX รอบนี้

1. แปลง frame → วินาที (frame rate) ทุก cue
2. แบ่ง transcript เป็น **sections** ตามเนื้อหา (เปิด/เรื่องหลัก/เปลี่ยนประเด็น/ปิด)
3. ระบุ **section boundaries** — จุดที่เนื้อหาเปลี่ยน Topic, เปลี่ยนอารมณ์, หรือเปลี่ยนจังหวะ
4. บันทึก: format, duration, section map, อารมณ์รวมของแต่ละ section

**Output:** section map ที่มี time range + topic + mood ของแต่ละ section

### Round 2 — Beat Harvesting (เก็บเกี่ยวจังหวะ)

**เป้าหมาย:** หา candidate beat ให้มากที่สุด — ยังไม่ตัด

เดินทีละ cue ใน transcript:
- อ่าน **ข้อความ** — มีมุก? มีคำเน้น? มีตัวเลข? มี reaction?
- อ่าน **บริบทรอบข้าง** — cue ก่อน/หลังพูดถึงอะไร? มีการเปลี่ยนอารมณ์ไหม?
- จด **ทุกจังหวะที่อาจใช้ SFX** พร้อม:
  - timestamp (วินาที)
  - ข้อความที่พูด (raw transcript)
  - ประเภทจังหวะ (มุก/reaction/ตกใจ/เน้นคำ/transition/dramatic/fail/สำเร็จ/emotional)
  - SFX family ที่เข้ากัน (จาก Beat Taxonomy)
  - เหตุผลสั้น ๆ

**ถ้าไม่มี transcript (game/meme/livestream):** หา beat จาก visual cuts, จังหวะ action, kill/death/respawn, UI popup, alert event ใช้ `sfx` tool (`action="analyze"` / `action="plan"`) เป็นตัวช่วย แต่**ต้องคัดเองเสมอ**

**Output:** candidate list ที่มีทุกจังหวะที่พบ (คาดว่ามากกว่า density cap — รอบ 3 จะคัดออก)

### Round 3 — Curation & Selection (คัดเลือก)

**เป้าหมาย:** เลือกเฉพาะจังหวะที่มี impact สูงสุด ผ่าน filter 4 ชั้น

**Filter 1 — Density Check:**
- คำนวณ density cap จาก Format Table (talking-head 3–5/min, game 5–8, podcast 1–2/segment)
- คำนวณ: candidate count ÷ (duration / 60) = density ถ้าเกิน cap → ตัดจังหวะที่ impact ต่ำสุดก่อน

**Filter 2 — Spacing Check:**
- เรียง timestamp แล้วตรวจ gap — ห้ามห่างกัน < 1 วินาที
- ถ้า 2 ตัวชิดกัน → เลือกตัวที่แรงกว่า ตัดอีกตัว

**Filter 3 — Family Variety:**
- ตรวจว่าไม่ใช้ตระกูลเดียวกันซ้ำใกล้กัน (เช่น whoosh×3, pop×3 ติดกัน)
- ถ้าซ้ำ → สลับเป็นตระกูลอื่นจาก Beat Taxonomy หรือตัดออก

**Filter 4 — Impact Ranking:**
- เรียง candidate ตาม impact ต่อผู้ชม (สูง → ต่ำ)
- ตัดจากท้าย list จนเหลือเท่ากับ density cap
- ทุกตัวที่เหลือต้องระบุเหตุผลได้ 1 บรรทัด — ถ้าบอกไม่ได้ว่าช่วยจังหวะไหน → ตัด

**Output:** final plan list ที่ผ่านทุก filter + เหตุผลของแต่ละตัว

### Finalize

- **เขียน plan JSON** (schema ด้านล่าง) — ทุกตัวต้องมี `reason` 1 บรรทัด
- **รัน CLI** — รัน `--dry-run` ก่อนเสมอ แล้ววางจริง
- **ตรวจสอบ** (Verification Checklist ด้านล่าง)

## plan JSON Schema

```json
{
  "timeline_name": "ชื่อ timeline (optional)",
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

- `sfx_file`: ชื่อไฟล์ใน `Z:\SFX_processed` หรือ `Z:\SFX` เท่านั้น (ห้าม path สมบูรณ์, ห้ามเดาชื่อ — list ก่อนด้วย `sfx` scan)
- `timestamp_seconds`: วินาทีบน timeline
- `duration`: ความยาว sting (default 0.5s) — ไฟล์ยาวกว่าจะถูก pre-trim ให้โดยอัตโนมัติ
- `reason`: บังคับ 1 บรรทัด (Hard Limit เดิม)

## วางจริง (CLI)

```powershell
davinci-resolve-mcp\venv\Scripts\python.exe scripts\sfx_place.py --plan plan.json --verify
```

- `--dry-run`: ตรวจ plan (ไฟล์มีจริง, timestamp, ไม่ซ้อน) โดยไม่แตะ Resolve — **รันก่อนวางเสมอ**
- `--verify`: อ่าน readback หลังวาง แล้วรายงาน items/issues
- `--raw-dir` / `--processed-dir`: override ถ้า library อยู่ที่อื่น (default `Z:\SFX` / `Z:\SFX_processed`)
- exit code: 0 = วางครบ, 1 = มีตัวล้ม, 2 = plan ผิด, 3 = ต่อ Resolve ไม่ได้

CLI ทำทุกอย่างเอง: หา/สร้าง SFX track (ชื่อ "SFX 1"), ensure `Master/SFX` bin, import dedup, pre-trim sting (workaround `AppendToTimeline` ignore endFrame), วาง, verify

### ถ้าไม่มี Resolve / CLI ใช้ไม่ได้ (Fallback)

ถ้า MCP/CLI ไม่สามารถแก้โปรเจคจริงได้ ให้ส่ง**ตารางแนะนำ SFX** แทน โดยระบุต่อตัว:
- Timestamp (วินาที)
- SFX File (จาก list จริงเท่านั้น)
- เหตุผลที่เลือก (ตรง Beat ไหน)
- Volume ที่แนะนำ
- Fade In / Fade Out

## Audio Mixing

- SFX คือเสียงประกอบ, **เสียงหลักคือ bed ตาม Format Table** (talking-head/podcast = เสียงพูด, game = game audio, livestream = เสียงสตรีมเมอร์ + game + music) ใช้ไฟล์ processed ที่ระดับตรงตามตาราง ไม่ต้องปรับเพิ่ม
- game: bed กลบเสียงได้ → SFX ตั้งขึ้นได้โดยไม่รก; podcast/livestream: SFX ต้องเบากว่า bed มาก อย่าให้ทับการพูดหรือ alert
- ไม่มี clip/distortion ไม่มีตัวไหนดังหรือเบาผิดปกติเทียบกับตัวข้างเคียง
- Fades: เสียงสั้นให้ fade-out ไว ๆ, เสียงยาวต่อเนื่อง (rise, shimmer, whoosh) ต้อง fade-in/out ไม่กี่ frame ป้องกัน click
- สุดท้ายตรวจว่า: เสียงหลักชัด, SFX ไม่กลบมัน, ไม่มี SFX ซ้อนกันโดยไม่จำเป็น

## Hindsight Pass (เรียนรู้จากประสบการณ์ — ทำหลังงานเสร็จ)

หลังวางเสร็จและตรวจแล้ว ให้ทบทวนงานตัวเอง 1 รอบ:

1. Round 2 (Beat Harvesting) หา candidate ครบหรือยัง? มีจังหวะไหนที่漏掉ไหม?
2. Round 3 (Curation) ตัดจังหวะไหนไปที่จริง ๆ แล้วน่าจะเก็บ?
3. มี SFX ตัวไหนที่จริง ๆ แล้วไม่จำเป็นหรือซ้ำรสชาติกันไหม?
4. ระดับเสียง/ตำแหน่ง/การเลือกเสียง มีตัวไหนที่ทำได้ดีกว่าที่ทำไปไหม?
5. มีกฎอะไรใน skill นี้ที่พิสูจน์แล้วว่าไม่ตรงกับความเป็นจริงของโปรเจคไหม?

แล้ว **update ส่วน "Lessons Learned"** ด้านล่าง: เพิ่มได้แค่ **ไม่เกิน 2 บรรทัด ต่อรูปแบบ** ต่อ session (แยก tag ตาม format เพื่อไม่ให้บทเรียนของ meme ไปแย่งที่ของ podcast) และถ้าบรรทัดใหม่แย้ง/ซ้ำกับบรรทัดเก่าใน tag เดียวกัน ให้ merge หรือลบบรรทัดเก่าออก — เป้าหมายคือส่วนนี้เล็ก คม และชี้ไปที่สิ่งที่ใช้ได้จริง

## Lessons Learned

- **[talking-head] Track index อย่าคิดว่าเป็น 4 เสมอ:** timeline จริงอาจมีแค่ 1 audio track (Dialogue) → CLI จะ `AddTrack("audio")` ให้อัตโนมัติ ได้ index 2 และตั้งชื่อ "SFX 1" เอง ตรวจ track ก่อนวางทุกครั้ง
- **[talking-head] คลิป v2 (127s, 60fps) บทพูดต่อเนื่อง ~90%:** sting สั้นบนคำเน้น (ตัวเลข, ช็อก, จังหวะเปิด-ปิด) 7 จุดใช้ได้จริง ไม่กลบ speech หากเป็น −10 ถึง −16dB ใช้ processed files
- **[talking-head] `AppendToTimeline` บางครั้ง ignore `endFrame` (วางทั้งไฟล์ยาว):** แก้ด้วยการ pre-trim ไฟล์ wav เป็น sting (0.4–0.6s, stdlib `wave`) ไว้ก่อน แล้ววาง full-length ของ sting นั้น (endFrame = ความยาว sting) ได้ผลทุกครั้ง — CLI/`SFXPlacer` ทำ pre-trim ให้อัตโนมัติ ไม่ต้อง pre-trim มือ
- **[meme] คลิปสั้น 34s (วันเกิดหมาใน):** sting ที่ 0.12s ตอนเปิดเลยได้ผลดี (meme ไม่มี intro ยาว), 5 sting ต่อ 34s (sparkle/ding/pop/collect/pop) จับจังหวะพีคตรง subtitle เปิดตัว→เผย→ดีใจ→สำคัญ→ปิด ได้จังหวะสนุกโดยไม่รก
- **[talking-head] คลิป v3 (212s, 60fps, เปลี่ยน Class Elsword):** 16 sting บนคำเน้น/มุก (555+, ตัวเลข 8000%, ประชด "โครตเย่", ดราม่า "ลาก่อน") density 4.5/นาที ใช้ได้จริง ไม่กลบพูด — เปิด-ปิดคลิปได้ sparkle, ประชดใช้ wrong, ดราม่าแกล้งซึ้งใช้ gong
- **[talking-head] ผู้ใช้อาจต้องการไฟล์เต็มไม่ใช่ sting:** sting 0.5s ใช้ source หมดทั้งไฟล์ → แก้/ยืดใน Resolve ไม่ได้ User (KT404) ขอวางไฟล์เต็มจริง (duration = ความยาวไฟล์) เพื่อให้ตัด/ยืดได้เอง ใช้วิธีนี้เป็น default กับคลิปของ user รายนี้
- **[talking-head] คลิป v4 (113s, 60fps, ปลูกข้าว day 11, ประกาศไลฟ์บันนี่เกิร์ล):** 9 จุดบนตัวเลข/หัวข้อสำคัญ (1680 subs → pop, 1 ใน 10 → collect, เปิดประเด็น → ding, เป้าหมายโดเนท → kaching, เผยไฮไลต์ → sparkle) วางไฟล์เต็ม ใช้ได้จริง — transcript timecode (frame) เป็นแหล่งหา beat ที่แม่นยำกว่า subtitle text เปล่า
- **[talking-head] วิเคราะห์รอบเดียวได้ SFX น้อยผิดปกติ (5 จุด/120s = 2.5/min):** 原因是ข้าม Round 2 (Beat Harvesting) แล้วไปเลือก SFX เลย → 遗漏 candidate หลายจังหวะ แก้ด้วย workflow 3 รอบ: Round 1 (โครงสร้าง) → Round 2 (เก็บเกี่ยวให้หมด) → Round 3 (คัดด้วย density/spacing/family) ได้ 8 จุด/120s = 4/min ซึ่งตรง range มากกว่า
- **[game] คลิปสั้น 27s (Assassin's Creed ซ่อนตัว NPC เห็น, 30fps):** 4 จุด (sparkle เปิด / pop ถูกจับได้ / impact NPC มาถึง / pop ปิด) density ~8.9/นาทีตามเกณฑ์ game 5-8 ได้จริง — ถ้ามี audio track ว่าง (track 2) อยู่แล้ว CLI จะสร้างใหม่เป็น track 3 ไม่ใช่ track 2 เสมอ
- **[game] Library อยู่ที่ Z:\SFX จริง (confirmed by scan):** processed files อยู่ที่ Z:\SFX_processed, raw อยู่ที่ Z:\SFX — ใช้ processed เป็นหลัก (normalize แล้ว) ไม่ต้องส่ง --raw-dir/--processed-dir
- **[game] User preference overrides density table:** User ต้องการ SFX น้อยมาก (2-3/นาที) แม้ density table บอก game 5-8 — วิเคราะห์ story arc หา TRUE hinge/punchline เท่านั้น ไม่ใช่ทุกจังหวะ action
- **[game] processed ≠ ไฟล์เต็ม:** processed (impact-10.wav 0.67s) สั้นกว่า raw (Impact - Comedy Hit 01.mp3 2.41s) — ถ้า user ต้องการตัด/ยืดเอง ต้องวาง raw ไม่ใช่ processed

### Python environment for Resolve scripting (bridge vs direct)

The `DaVinciResolveScript` module **will segfault** (Signal 11 / exit 139) if imported without the DLL directory setup. The `src/server.py` handles this by calling `os.add_dll_directory()` and prepending the Resolve install dir to `PATH` + setting `PYTHONHOME` **before** `import DaVinciResolveScript`. Replicate this exact sequence when calling Resolve APIs from the Hermes venv (the venv's Python 3.11 cannot load the native bridge without it):

```python
import os, sys
RESOLVE_LIB = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
RESOLVE_MODULES = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
sys.path.insert(0, RESOLVE_MODULES)           # makes DaVinciResolveScript.py findable
if os.path.isfile(RESOLVE_LIB):
    _d = os.path.dirname(RESOLVE_LIB)
    if not os.environ.get("PYTHONHOME"):
        os.environ["PYTHONHOME"] = sys.base_prefix
    p = os.environ.get("PATH", "")
    if _d.lower() not in p.lower():
        os.environ["PATH"] = _d + os.pathsep + p
    if hasattr(os, "add_dll_directory"):
        try: os.add_dll_directory(_d)
        except OSError: pass
import DaVinciResolveScript as dvr           # now safe — no segfault
```

Two connection modes exist:
- **Direct (above):** works when the venv has `add_dll_directory` access and Resolve is running. Used by `scripts/sfx_place.py --plan plan.json --dry-run` and direct API calls.
- **In-app bridge** (`Workspace > Scripts > resolve_bridge`): the server's normal path; connects over loopback. Requires `DAVINCI_RESOLVE_BRIDGE=1` env var and the bridge script running inside Resolve. Use `connect_resolve()` / `BridgeProxy` for this mode.

When the direct import segfaults (Signal 11 / exit 139), the bridge is the fallback — but the bridge requires the in-Resolve script to be started first.

## Verification Checklist

ก่อนสรุปว่าเสร็จ ให้ยืนยัน:
1. ทุก SFX อยู่บน SFX track ที่ frame ที่ตั้งใจ (จาก readback ของ CLI `--verify`)
2. ไม่มี SFX ตัวไหนทับเสียงหลัก/bed จนกลบ (talking-head/podcast = ไม่กลบพูด; game = ไม่กลบ game audio; livestream = ไม่กลบ alert/พูด)
3. ไม่มี 2 SFX ซ้อนกันในระยะ ~1 วินาที (ยกเว้น game action คู่)
4. ไม่มีตระกูลเสียงไหนถูกใช้ซ้ำเกินไป (ยกเว้น meme ที่ตั้งใจซ้ำเพื่อมุก)
5. ทุก SFX มีเหตุผลที่ระบุได้; ไม่มีตัว filler
6. ระดับเสียงสม่ำเสมอ (ไม่มีตัวดัง/เบาหวิวเทียบกับตัวข้างเคียง)
7. ใช้ค่า density/ระดับเสียงตรงตาม Format Table ของรูปแบบคลิป
8. จังหวะรวมของคลิปสนุกและเป็นธรรมชาติขึ้นจริง
9. ผลจาก CLI readback ตรงกับ plan (จำนวนตัว, frame, track) ก่อนสรุปเสร็จ

## Common Mistakes

| ผิดพลาด | วิธีแก้ |
|---|---|
| สร้างชื่อไฟล์ขึ้นเอง | ใช้เฉพาะชื่อจาก list จริงของ `Z:\SFX` / `Z:\SFX_processed` (scan ก่อน) |
| ใส่ SFX ทุกประโยค | Density ตาม Format Table; ใส่เฉพาะจังหวะที่ impact สูง |
| วางเสียงดัง 2 ตัวซ้อนกัน (ระเบิด+กรี๊ด) | เลือกเสียงที่แรงที่สุดตัวเดียว (ยกเว้น game action คู่) |
| ใช้ whoosh 3 ครั้งติด | สลับตระกูล; one whoosh per transition พอแล้ว |
| SFX ดังกลบ bed | ใช้ไฟล์ processed; ให้ SFX เบากว่า bed ตาม Format Table |
| วาง track ผิด / frame ผิด | ให้ CLI จัดการ track; ตรวจ readback จาก `--verify` ว่า frame ตรงที่ตั้งใจ |
| ใช้ SFX เดิมซ้ำเยอะเกินไป | ใช้ taxonomy สลับตระกูล (ยกเว้น meme ที่ตั้งใจซ้ำเพื่อมุก) |
| ใช้ค่า talking-head กับ meme/game/podcast | อ่าน Format Table ก่อนเริ่ม ระบุรูปแบบใน step 0 |
| เขียน plan โดยไม่รัน `--dry-run` ก่อน | รัน `--dry-run` เสมอ ตรวจไฟล์/timestamp/ซ้อนก่อนวางจริง |
| ลืม `reason` ใน plan | ทุกตัวต้องมีเหตุผล 1 บรรทัด (Hard Limit; CLI เตือนเป็น warning) |
| วิเคราะห์รอบเดียวแล้วเลือก SFX เลย | ทำ 3 รอบเสมอ: Structural Scan → Beat Harvesting → Curation. ข้าม Round 2 = 遗漏 beats ทำให้ได้ SFX น้อยผิดปกติ |
