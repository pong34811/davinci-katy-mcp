---
name: davinci-resolve-workflow
description: "DaVinci Resolve workflow guide — ใช้ MCP tools ได้อย่างถูกต้องและมีประสิทธิภาพ ใช้เมื่อต้องการจัดการ timeline, media pool, color grading, render, export, import, หรือ DaVinci Resolve operations ทั่วไป — ครอบคลุมทุกหน้า: Edit, Cut, Color, Fusion, Fairlight, Deliver"
---

# DaVinci Resolve Workflow

ใช้ MCP tools ทำงานกับ DaVinci Resolve อย่างมีประสิทธิภาพ — รู้ tool ไหนใช้ตอนไหน, หลีกเลี่ยง common mistakes

## หลักการ

**Agent คิด, MCP ทำ:** Agent วิเคราะห์และตัดสินใจ, MCP tools ลงมือ执行

**รู้ tool chain:** ไม่ใช่ทุก operation ต้องเริ่มจาก scratch — บางอย่างมี helper แล้ว

**Safe ก่อน Mutate:** ใช้ safe_* variants เมื่อมี, ไม่มีก็ dry_run ก่อนเสมอ

## Tool Chain

### Timeline Operations

| ต้องการ | Tool | หมายเหตุ |
|---|---|---|
| ดู timeline ปัจจุบัน | `timeline.get_current()` | — |
| สร้าง timeline ใหม่ | `media_pool.create_timeline()` | ถ้ามีชื่อซ้ำจะ fail |
| ลบ timeline | `timeline.delete_timelines()` | DESTRUCTIVE — archive ก่อน |
| ดู items ใน track | `timeline.get_items()` | track_type: video/audio/subtitle |
| ลบ items | `timeline.delete_clips()` | ripple=True = CATASTROPHIC |
| ค้นหา clips | `timeline.clip_where()` | filter ได้ |
| Export timeline | `timeline.export_timeline_checked()` | ใช้ checked variant |

### Media Pool

| ต้องการ | Tool | หมายเหตุ |
|---|---|---|
| ดู folders | `media_pool.get_root_folder()` | — |
| สร้าง folder | `media_pool.add_subfolder()` | — |
| Import media | `media_pool.safe_import_media()` | ใช้ safe variant |
| ดู clips ใน folder | `folder.get_clips()` | — |
| ดู clip properties | `media_pool.probe_clip_properties()` | — |
| จัดระเบียบ clips | `media_pool.organize_clips()` | dry_run ได้ |

### Color Grading

| ต้องการ | Tool | หมายเหตุ |
|---|---|---|
| ดู node graph | `timeline_item_color.probe_node_graph()` | safe read-only |
| ดู evidence base | `timeline_item_color.grade_evidence_base()` | ใช้ก่อนทำอะไรกับ grade |
| ใส่ CDL | `timeline_item_color.safe_set_cdl()` | validate + dry_run |
| Copy grade | `timeline_item_color.safe_copy_grade()` | ใช้ safe variant |
| Apply DRX | `timeline_item_color.safe_apply_drx()` | REPLACES graph ทั้งหมด |
| ดู versions | `timeline_item_color.get_version_names()` | — |

### Render

| ต้องการ | Tool | หมายเหตุ |
|---|---|---|
| ดู formats/codecs | `render.get_formats()` / `render.get_codecs()` | — |
| ตั้ง format+codec | `render.set_format_and_codec()` | — |
| ตั้ง render settings | `render.set_settings()` | หรือ safe_set_render_settings() |
| เพิ่ม job | `render.add_job()` | — |
| เริ่ม render | `render.start()` | — |
| ดู status | `render.get_job_status()` | — |

### Export/Import

| ต้องการ | Tool | หมายเหตุ |
|---|---|---|
| Export timeline | `timeline.export_timeline_checked()` | AAF, EDL, FCPXML |
| Import timeline | `timeline.import_timeline_checked()` | safe + sanitize |
| Import from DRP | `timeline.import_from_drp()` | extract แล้ว import |

## Common Workflows

### Workflow 1: Import → Edit → Export

```
1. media_pool.safe_import_media(paths)
2. media_pool.create_timeline(name)
3. timeline.append_to_timeline(clip_infos)
4. ... edit ... (timeline tools)
5. timeline.export_timeline_checked(path, format)
```

### Workflow 2: Color Grade

```
1. timeline_item_color.grade_evidence_base()  // ดูสถานะก่อน
2. timeline_item_color.safe_set_cdl(cdl)  // หรือ safe_apply_drx()
3. timeline_item_color.safe_copy_grade(target_ids)  // copy ไป clips อื่น
```

### Workflow 3: Render

```
1. render.get_formats()  // ดู available
2. render.set_format_and_codec(format, codec)
3. render.set_settings(settings)
4. render.add_job()  // ได้ job_id
5. render.start([job_id])
6. render.get_job_status(job_id)  // poll
```

## Safety Rules

1. **DESTRUCTIVE ops ต้อง archive ก่อน:** delete_timelines, delete_clips(ripple=True), reset_all_grades
2. **dry_run เสมอ** สำหรับ mutations ที่ไม่มี safe variant
3. **อย่า guess paths** — ใช้ media_storage.get_files()/get_subfolders() ดูก่อน
4. **Timeline versioning** — ใช้ begin_run/end_run สำหรับ multi-step destructive ops
5. **Check runtime_mode()** ก่อน LoadProject — ถ้ามี UI อาจมี unsaved project dialog

## Common Mistakes

| ผิดพลาด | วิธีแก้ |
|---|---|
| ใช้ graph.apply_grade_from_drx() แทน safe_apply_drx() | ใช้ safe variant เสมอ |
| ไม่ check track count ก่อนวาง items | get_track_count() ก่อน |
| วาง SFX บน track ที่มี BGM อยู่ | check get_items() ก่อน |
| render โดยไม่ set format | set_format_and_codec() ก่อน |
| Import timeline ไม่ check media | import_timeline_checked() มี sanitize |
