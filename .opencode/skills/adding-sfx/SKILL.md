---
name: adding-sfx
description: ใช้เมื่อเพิ่ม Sound Effects (SFX) ลงใน timeline ของ DaVinci Resolve เพื่อทำให้คลิปสนุก มีจังหวะ และน่าสนใจขึ้น — "เพิ่ม SFX", "เพิ่มเสียงประกอบ", "ใส่เสียงตลก", "add SFX", "sound effects", "make the clip more interesting/lively". ใช้ด้วยเมื่อ review หรือตรวจสอบ SFX ที่วางอยู่แล้วว่าควรปรับ/ลบ/เพิ่มตรงไหน
---

# Adding SFX ลง Timeline ของ DaVinci Resolve

## หลักการ

SFX คือเครื่องปรุง ไม่ใช่ตัวอาหาร จุดประสงค์คือคลิปที่**มีชีวิตชีวาและตั้งใจ** ไม่ใช่คลิปที่ทุกช่วงมีเสียง SFX ทุกตัวต้อง**มีเหตุผล**ว่ามันช่วยจังหวะ/อารมณ์ตอนไหน (มุก, reaction, ตกใจ, เน้นคำ, transition, dramatic, fail, สำเร็จ) ห้ามสุ่มใส่ ห้ามทับเสียงพูด

## ตรวจ Library ก่อนเสมอ

มี 2 โฟลเดอร์ — **ใช้ shell tool เปิด list จริงทุกครั้งก่อนเริ่ม** แล้วอ้างถึงเฉพาะไฟล์ที่อยู่ใน list เท่านั้น:

- `Z:\SFX` — ไฟล์ต้นฉบับ (~71 ไฟล์, mp3/wav)
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
- **Density cap:** อย่างมาก **1 ตัว ต่อ ~5 วินาที** และรวมได้แค่หยิบมือต่อนาที (คลิป 45s ได้ 3–5 ตัว ไม่ใช่ 13)
- **ห้ามซ้อน:** ห้ามมี 2 SFX ทับกันหรือห่างกันไม่ถึง ~1 วินาที (เสียงดัง 1 ตัวต่อจังหวะ เลือกตัวที่แรงกว่า)
- **ห้ามยิงตระกูลเดิมซ้ำ:** ไม่ใช้ตระกูลเดียวกัน (whoosh×3, harp×2) ใกล้กัน ต้องสลับ
- **ทุกตำแหน่งต้องบอกเหตุผล 1 บรรทัด** ถ้าบอกไม่ได้ว่ามันช่วยจังหวะไหน → ตัดทิ้ง
- ให้ความสำคัญกับจุด Impact ต่อผู้ชมมากที่สุด อย่าใส่ทุกประโยค ทุกการตัดต่อ

## Workflow

1. **Inspect:** list `Z:\SFX` และ `Z:\SFX_processed`, ดู timeline ปัจจุบัน (`timeline.list` / `timeline.get_current`), audio track (`timeline.probe_audio_track`), อ่าน transcript ถ้ามี (`timeline.get_transcript`) เพื่อหาจังหวะและช่องว่างของบทพูด
2. **หาจุด:** จาก transcript/beats — หา punchline, reaction, ช่วงตกใจ, "ดูสิเกิดอะไรขึ้น" moment, transition คิดแบบเล็กและตั้งใจ
3. **เลือกเสียง:** จับคู่เหตุการณ์+โทน จาก Beat Taxonomy กับ list จริง ควรใช้ `Z:\SFX_processed` ตามกฎข้อจำกัด
4. **ลงมือวาง** (ดูด้านล่าง)
5. **ตรวจสอบ** (ดู checklist)

## วางจริง (MCP sequence ที่ทดสอบแล้ว)

SFX วางบน **audio track เฉพาะ SFX** — **track index ไม่ตายตัว** ต้อง probe ก่อนเสมอ: ถ้ายังไม่มี track SFX ต้องสร้างด้วย `AddTrack("audio")` ก่อน (ได้ index สุดท้ายของ audio track ใน timeline นั้น) แล้วใช้ `record_frame = seconds × fps` เสมอ อ่าน `timeline.get_setting(timelineFrameRate)` ก่อนแปลงวินาทีเป็น frame ทุกครั้ง (โปรเจคนี้ 60fps)

1. **Import** ไฟล์ที่เลือกเข้ารวม Media Pool bin SFX (ถ้าใส่ `target_folder` ได้ ใช้เสมอ):
   ```
   media_pool.safe_import_media
     paths: ["Z:\\SFX_processed\\pop-14.wav"]
     target_folder: "Master/SFX"
   ```
   → ได้ `id` ของคลิปกลับมา ถ้า SFX bin มีคลิปชื่อเดียวกันอยู่แล้ว ให้ใช้ของเดิม **ห้าม import ซ้ำ**

2. **Append วางตำแหน่ง** ลง timeline (audio clip ยาว ~1–2s ให้ตัดเหลือ ~0.5s sting = 30 frames ที่ 60fps):
   ```
   media_pool.append_to_timeline
     clip_infos: [{
       clip_id: "<id>",
       start_frame: 0, end_frame: 30,
       record_frame: <seconds*fps>,
       track_index: 4, media_type: 2
     }]
   ```
   ต้อง readback ตรวจว่า item ลง track ถูก frame ถูก

3. **Volume:** ใช้ `Z:\SFX_processed` เป็นหลัก (ระดับเสียง bake ไว้แล้ว −10 ถึง −18 dB) ถ้าต้องใช้ไฟล์ raw ให้ set ผ่าน `timeline.safe_set_audio_properties` (`Volume` 0–1 เช่น 0.2 ≈ −14 dB) — ระวังว่า writeback บน audio item ของ Resolve 21 ไม่ค่อย reliable ให้เชื่อไฟล์ pre-normalized มากกว่า post-hoc gain

### ถ้าแก้ timeline โดยตรงไม่ได้ (Fallback)

ถ้า MCP ไม่สามารถแก้โปรเจคจริงได้ ให้ส่ง**ตารางแนะนำ SFX** แทน โดยระบุต่อตัว:
- Timestamp (วินาที)
- SFX File (จาก list จริงเท่านั้น)
- เหตุผลที่เลือก (ตรง Beat ไหน)
- Volume ที่แนะนำ
- Fade In / Fade Out

## Audio Mixing

- SFX คือเสียงประกอบ, บทพูดคือเสียงหลัก ใช้ไฟล์ processed ที่ระดับสมเหตุสมผล (−10 ถึง −18 dB) ตามนั้น ไม่ต้องปรับเพิ่ม
- ไม่มี clip/distortion ไม่มีตัวไหนดังหรือเบาผิดปกติเทียบกับตัวข้างเคียง
- Fades: เสียงสั้นให้ fade-out ไว ๆ, เสียงยาวต่อเนื่อง (rise, shimmer, whoosh) ต้อง fade-in/out ไม่กี่ frame ป้องกัน click
- สุดท้ายตรวจว่า: เสียงพูดชัด, SFX ไม่กลบ dialogue, ไม่มี SFX ซ้อนกันโดยไม่จำเป็น

## Hindsight Pass (เรียนรู้จากประสบการณ์ — ทำหลังงานเสร็จ)

หลังวางเสร็จและตรวจแล้ว ให้ทบทวนงานตัวเอง 1 รอบ:

1. มี SFX ตัวไหนที่จริง ๆ แล้วไม่จำเป็นหรือซ้ำรสชาติกันไหม?
2. มีจังหวะไหนที่ควรได้ SFX แต่พลาดไปไหม?
3. ระดับเสียง/ตำแหน่ง/การเลือกเสียง มีตัวไหนที่ทำได้ดีกว่าที่ทำไปไหม?
4. มีกฎอะไรใน skill นี้ที่พิสูจน์แล้วว่าไม่ตรงกับความเป็นจริงของโปรเจคไหม?

แล้ว **update ส่วน "Lessons Learned"** ด้านล่าง: เพิ่มได้แค่ **ไม่เกิน 2 บรรทัด** ต่อ session และถ้าบรรทัดใหม่แย้ง/ซ้ำกับบรรทัดเก่า ให้ merge หรือลบบรรทัดเก่าออก — เป้าหมายคือส่วนนี้เล็ก คม และชี้ไปที่สิ่งที่ใช้ได้จริง

## Lessons Learned

- **Track index อย่าคิดว่าเป็น 4 เสมอ:** timeline จริงอาจมีแค่ 1 audio track (Dialogue) → ต้อง `AddTrack("audio")` ได้ index 2 และตั้งชื่อ "SFX 1" เอง ตรวจ track ก่อนวางทุกครั้ง
- **Talking-head 100%:** คลิป v2 (127s, 60fps) บทพูดต่อเนื่อง ~90% → sting สั้นบนคำเน้น (ตัวเลข, ช็อก, จังหวะเปิด-ปิด) 7 จุดใช้ได้จริง ไม่กลบ speech หากเป็น −10 ถึง −16dB ใช้ processed files

## Verification Checklist

ก่อนสรุปว่าเสร็จ ให้ยืนยัน:
1. ทุก SFX อยู่บน SFX track ที่ frame ที่ตั้งใจ (จาก readback ของ append)
2. ไม่มี SFX ตัวไหนทับบทพูด; บทพูดยังชัดเจน
3. ไม่มี 2 SFX ซ้อนกันในระยะ ~1 วินาที
4. ไม่มีตระกูลเสียงไหนถูกใช้ซ้ำเกินไป
5. ทุก SFX มีเหตุผลที่ระบุได้; ไม่มีตัว filler
6. ระดับเสียงสม่ำเสมอ (ไม่มีตัวดัง/เบาหวิวเทียบกับตัวข้างเคียง)
7. จังหวะรวมของคลิปสนุกและเป็นธรรมชาติขึ้นจริง

## Common Mistakes

| ผิดพลาด | วิธีแก้ |
|---|---|
| สร้างชื่อไฟล์ขึ้นเอง | ใช้เฉพาะชื่อจาก list จริงของ `Z:\SFX` / `Z:\SFX_processed` |
| ใส่ SFX ทุกประโยค | Density cap; ใส่เฉพาะจังหวะที่ impact สูง |
| วางเสียงดัง 2 ตัวซ้อนกัน (ระเบิด+กรี๊ด) | เลือกเสียงที่แรงที่สุดตัวเดียว |
| ใช้ whoosh 3 ครั้งติด | สลับตระกูล; one whoosh per transition พอแล้ว |
| SFX ดังกลบ dialogue | ใช้ไฟล์ processed; ให้ SFX เบากว่าเสียงพูดเสมอ |
| วาง track ผิด / frame ผิด | SFX บน track 4 ("SFX 1"); record_frame = seconds × fps |
| ใช้ SFX เดิมซ้ำเยอะเกินไป | ใช้ taxonomy สลับตระกูลให้หลากหลายแต่ไม่รก |
