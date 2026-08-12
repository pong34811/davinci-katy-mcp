# Changelog

ประวัติการแก้ไข/ทำงานร่วมกับ AI ในโปรเจคนี้

## [2026-08-12] — เพิ่ม SFX ลงโปรเจคจริง (vdo วันที่ 8, 127s @60fps)

- Timeline จริง: 142s→127s, มี audio track แค่ 1 (Dialogue 1) → `AddTrack("audio")` สร้าง "SFX 1" index 2 + `SetTrackName`
- Import processed SFX 7 ตัวจาก `Z:\SFX_processed` เข้า bin `Master/SFX` แล้ว `AppendToTimeline` ลง track 2 โดย `mediaType=2`, `record_frame=seconds×fps`, sting 24–42 frames
- จุดที่วาง 7 จุด: 14.3s `ding-12` (เป้า 10K), 30.2s `pop-13` (ฤดูหนาว), 37.0s `collect-10` (1,628), 44.3s `sparkle-10` (ดีใจ), 73.1s `whoosh-intro-12` (transition กติกาใหม่), 103.5s `impact-10` (ช็อก 8,000), 126.6s `pop-10` (บ๊ายบาย)
- Readback ยืนยันทุกตัวอยู่ track 2, frame ถูกต้อง
- **บทเรียน:** track index ไม่ตายตัว, talking-head พูดต่อเนื่อง → sting สั้นบนคำเน้นใช้ได้ (อัปเดต skill แล้ว)

## [2026-08-12] — รีเวิร์ค skill adding-sfx ใหม่

- เขียน `.opencode/skills/adding-sfx/SKILL.md` ใหม่ทั้งไฟล์ จากเดิมที่ยึด workflow ทั่วไป
- เพิ่ม **Beat → SFX Taxonomy**: ตารางจับคู่จังหวะเหตุการณ์ (มุก/reaction/ตกใจ/เน้นคำ/fail/transition/สำเร็จ/dramatic/visual action/UI) กับตระกูลเสียงจริงใน library
- เพิ่ม **Hindsight Pass**: หลังงานเสร็จ AI ทบทวนการวางของตัวเอง แล้วเขียนบทเรียนกลับลงในส่วน Lessons Learned (จำกัด 2 บรรทัด/session, merge/ลบบรรทัดเก่าเมื่อแย้งกัน) = loop เรียนรู้ของ skill
- เพิ่ม **Fallback mode**: ถ้าแก้ timeline โดยตรงไม่ได้ ให้ส่งตารางแนะนำ SFX (timestamp/file/เหตุผล/volume/fades)
- เปลี่ยนนโยบาย library: list `Z:\SFX` + `Z:\SFX_processed` จริงทุกครั้งก่อนเริ่ม (ไม่ hardcode), ตาราง processed→raw เก็บไว้เป็นข้อมูลอ้างอิง
- ข้อจำกัดการวาง, mixing, checklist, common mistakes: ปรับให้ตรงกับโปรเจค (track 4 "SFX 1", 60fps)

## [2026-08-12]

### สร้าง skill: adding-sfx
- สร้าง `.opencode/skills/adding-sfx/SKILL.md` — skill สำหรับเพิ่ม Sound Effects ลงใน timeline ของ DaVinci Resolve
- ตรวจสอบ SFX library: `Z:\SFX` (raw) และ `Z:\SFX_processed` (pre-normalized, ระดับเสียงในชื่อไฟล์)
- ทดสอบลำดับการทำงานกับ Resolve จริง:
  - `safe_import_media` → target_folder=`Master/SFX`
  - `append_to_timeline` → track 4 ("SFX 1"), media_type=2, record_frame = วินาที × fps (timeline นี้ 60fps)
  - Volume: ใช้ `Z:\SFX_processed` เพราะ Resolve 21 อ่านค่า Volume กลับไม่ได้ (writeback unreliable)
- RED/GREEN test: baseline ใส่ SFX 13 ตัว/45s → หลังมี skill ลดเหลือ 5 ตัว/45s
- ลบของทดสอบออกจากโปรเจคเรียบร้อย
