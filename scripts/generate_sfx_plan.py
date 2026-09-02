import json

plan = {
    "timeline_name": "Subtitle 1-3 — Varied SFX",
    "sfx": [
        {
            "sfx_file": "Pop - Short 06.mp3",
            "timestamp_seconds": 0.183,
            "duration": 0.5,
            "reason": "Punchline: 'ผมบักอ่ะ' — pop กระชับเปิดมุกแรก"
        },
        {
            "sfx_file": "Huh sound effect.mp3",
            "timestamp_seconds": 1.316,
            "duration": 0.6,
            "reason": "Reaction: 'จริงจังมาเนี่ย' — เสียงงง/อึ้งกับความจริงจัง"
        },
        {
            "sfx_file": "Game - Wrong Answer.mp3",
            "timestamp_seconds": 5.816,
            "duration": 0.5,
            "reason": "Fail/Shock: 'ชิบคายแล้ว' — ผิดทาง/ตกใจ"
        },
        {
            "sfx_file": "Impact - Comedy Hit 02.mp3",
            "timestamp_seconds": 12.216,
            "duration": 0.6,
            "reason": "Dramatic fail: 'ผมโดนขังห้องเลย' — โดนขัง แรง!"
        },
        {
            "sfx_file": "Gong - Comical Metal.wav",
            "timestamp_seconds": 23.666,
            "duration": 0.8,
            "reason": "Dark comedy closing: 'เผื่อเจอกะโหลก' — ปิดด้วย gong ตลกมืด"
        }
    ],
    "format": "talking_head",
    "timeline_duration_seconds": 25.483,
    "fps": 60.0,
    "density_per_minute": 11.77,
    "warnings": [
        "5 SFX in 25.5s = 11.77/min (高于 talking-head 3-5/min cap) — user requested maximum SFX"
    ]
}

plan_path = r"C:\Users\warit\Desktop\davinci-katy-mcp\scripts\plan.json"
with open(plan_path, 'w', encoding='utf-8') as f:
    json.dump(plan, f, indent=2, ensure_ascii=False)

print(f"SFX plan generated: {plan_path}")
print(json.dumps(plan, indent=2, ensure_ascii=False))
