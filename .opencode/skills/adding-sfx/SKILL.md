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

## Workflow ใหม่

0. **ระบุรูปแบบคลิป** (ดู Format Table) — เลือกค่า density/ระดับเสียง/แหล่งหา beat ให้ตรงรูปแบบ
1. **Inspect:** เรียก `sfx` MCP tool (`action="scan"`) เพื่อ list library จริง, ดู timeline ปัจจุบัน (`timeline.get_current`), audio track (`timeline.probe_audio_track`), อ่าน transcript ถ้ามี (`timeline.get_transcript`)
2. **หาจุด:** จาก transcript/beats — หา punchline, reaction, ช่วงตกใจ, transition, คำเน้น คิดแบบเล็กและตั้งใจ **ถ้าไม่มี transcript (game/meme/livestream):** หา beat จาก visual cuts, จังหวะ action, kill/death/respawn, UI popup, alert event, จุดเปลี่ยน segment ใช้ `sfx` tool (`action="analyze"` / `action="plan"`) เป็นตัวช่วยหา candidate beats ได้ แต่**ต้องคัดเองเสมอ** — อย่าเชื่อ engine 100%
3. **เลือกเสียง:** จับคู่เหตุการณ์+โทน จาก Beat Taxonomy กับ list จริง ควรใช้ `Z:\SFX_processed` ตามกฎข้อจำกัด
4. **เขียน plan JSON** (schema ด้านล่าง) — ทุกตัวต้องมี `reason` 1 บรรทัด
5. **รัน CLI** (ด้านล่าง) — รัน `--dry-run` ก่อนเสมอ แล้ววางจริง
6. **ตรวจสอบ** (Verification Checklist ด้านล่าง)

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

1. มี SFX ตัวไหนที่จริง ๆ แล้วไม่จำเป็นหรือซ้ำรสชาติกันไหม?
2. มีจังหวะไหนที่ควรได้ SFX แต่พลาดไปไหม?
3. ระดับเสียง/ตำแหน่ง/การเลือกเสียง มีตัวไหนที่ทำได้ดีกว่าที่ทำไปไหม?
4. มีกฎอะไรใน skill นี้ที่พิสูจน์แล้วว่าไม่ตรงกับความเป็นจริงของโปรเจคไหม?

แล้ว **update ส่วน "Lessons Learned"** ด้านล่าง: เพิ่มได้แค่ **ไม่เกิน 2 บรรทัด ต่อรูปแบบ** ต่อ session (แยก tag ตาม format เพื่อไม่ให้บทเรียนของ meme ไปแย่งที่ของ podcast) และถ้าบรรทัดใหม่แย้ง/ซ้ำกับบรรทัดเก่าใน tag เดียวกัน ให้ merge หรือลบบรรทัดเก่าออก — เป้าหมายคือส่วนนี้เล็ก คม และชี้ไปที่สิ่งที่ใช้ได้จริง

## Lessons Learned

- **[talking-head] Track index อย่าคิดว่าเป็น 4 เสมอ:** timeline จริงอาจมีแค่ 1 audio track (Dialogue) → CLI จะ `AddTrack("audio")` ให้อัตโนมัติ ได้ index 2 และตั้งชื่อ "SFX 1" เอง ตรวจ track ก่อนวางทุกครั้ง
- **[talking-head] คลิป v2 (127s, 60fps) บทพูดต่อเนื่อง ~90%:** sting สั้นบนคำเน้น (ตัวเลข, ช็อก, จังหวะเปิด-ปิด) 7 จุดใช้ได้จริง ไม่กลบ speech หากเป็น −10 ถึง −16dB ใช้ processed files
- **[talking-head] `AppendToTimeline` บางครั้ง ignore `endFrame` (วางทั้งไฟล์ยาว):** แก้ด้วยการ pre-trim ไฟล์ wav เป็น sting (0.4–0.6s, stdlib `wave`) ไว้ก่อน แล้ววาง full-length ของ sting นั้น (endFrame = ความยาว sting) ได้ผลทุกครั้ง — CLI/`SFXPlacer` ทำ pre-trim ให้อัตโนมัติ ไม่ต้อง pre-trim มือ
- **[meme] คลิปสั้น 34s (วันเกิดหมาใน):** sting ที่ 0.12s ตอนเปิดเลยได้ผลดี (meme ไม่มี intro ยาว), 5 sting ต่อ 34s (sparkle/ding/pop/collect/pop) จับจังหวะพีคตรง subtitle เปิดตัว→เผย→ดีใจ→สำคัญ→ปิด ได้จังหวะสนุกโดยไม่รก

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
