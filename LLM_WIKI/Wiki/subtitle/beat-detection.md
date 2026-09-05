---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept, subtitle]
audience: agent
summary: >
  Beat detection pipeline from SRT timestamps to candidate events.
  Covers regex patterns, emotion coupling, and density rules.
date_updated: 2026-09-02
---

# Beat Detection

Two regex-based systems detect "SFX-worthy moments" from subtitle/transcript text. Both use keyword matching — no NLP, no semantic understanding.

## System A: Engine (analyzer.py)

`KEYWORD_PATTERNS` in `src/sfx_engine/analyzer.py` — 7 patterns with Thai+English regex:

| EventType | Default Impact | Thai Keywords | English Keywords |
|-----------|---------------|---------------|-----------------|
| EMPHASIS | 0.75 | ตัวเลข, จำนวน, สถิติ, เปอร์เซ็นต์, ล้าน, พัน, ร้อย, บาท, กิโล, เท่า, คะแนน, แสน | \b\d+[\d,.]*\b, percent, million, thousand, first, second |
| REACTION | 0.80 | เย้, ว้าว, โอ้, อ๊ะ, โห, ช็อก, งง, เหรอ, จริงดิ, เห้ย, อ้าว, อุ๊ย, ฮือ, ว๊าก | wow, omg, what, shock, surprise, yeah, hey |
| JOKE | 0.85 | 555, ฮ่าๆ, ตลก, มุก, ขำ, ปั่น, กวน, กาว | lol, lmao, haha, funny, joke, meme |
| FAIL | 0.85 | ผิด, พลาด, แตก, พัง, ดับ, ตาย, แพ้, แย่, ซวย, มั่ว, กรรม | oops, fail, wrong, died, dead, miss, lose, error, bug |
| SUCCESS | 0.85 | สำเร็จ, ชนะ, ได้แล้ว, ถูกต้อง, เยี่ยม, สุดยอด, เก่ง, ปัง, ผ่าน | win, success, correct, done, passed, perfect, level up |
| TRANSITION | 0.70 | ต่อไป, มาดูกัน, ขั้นตอน, ถัดไป, สรุป, เริ่ม, ตอนแรก, จบ | next, then, now, after, finally, let's, step |
| DRAMATIC | 0.80 | แต่, แต่ว่า, ทว่า, อย่างไรก็ตาม, ความจริง, ลับ, อันตราย, ระวัง, ระเบิด | but, however, secret, danger, warning, shocking, dramatic |

### Timestamp Estimation

```python
pos_ratio = match.start() / len(text)
timestamp = start_time + (end_time - start_time) * pos_ratio
```

Word position within subtitle block is estimated by character offset ratio. Not word-boundary accurate.

### Format-Specific Score Modifiers

| Format | Modifier |
|--------|----------|
| PODCAST | JOKE × 0.4 (suppress small jokes) |
| GAME | ACTION/SUCCESS/FAIL × 1.3 (boost action) |
| MEME | All × 1.2 (boost everything) |
| TALKING_HEAD | No modifier |

## System B: Script (analyze_subtitles.py)

`EMOTION_KEYWORDS` in `scripts/analyze_subtitles.py` — 8 emotion categories:

| Emotion | Thai | English | → Beat Type | → SFX |
|---------|------|---------|-------------|-------|
| surprise | มาจากไหน, ตกใจ, โอ้โห, ไม่น่าเชื่อ, เซอร์ไพรส์, ทำไม, จริงหรอ, เฮ้ย | wow, omg, surprise, really, no way, holy, what | surprise | pop |
| excitement | เย้, สุดยอด, เจ๋ง, เทพ, โคตร, เริ่ด, ปัง, ยินดี | yay, awesome, amazing, great, cool, love, best | excitement | sparkle |
| success | สำเร็จ, ได้แล้ว, ชนะ, ผ่าน, ถูกต้อง, เยี่ยม, สมหวัง | success, win, pass, correct, done, complete | success | collect |
| fail | ล้มเหลว, ผิด, ไม่ได้, พัง, เจ๊ง, พลาด, ตาย | fail, wrong, lose, die, dead, broken, error | fail | wrong |
| emphasis | ตัวเลข, สถิติ, จำนวน, เปอร์เซ็นต์, ล้าน, พัน, ร้อย, บาท | first, second, third, most, only, every, always, never | emphasis | ding |
| question | ทำไม, ยังไง, อะไร, ที่ไหน, เมื่อไหร่, ใคร | why, how, what, where, when, who | question | pop |
| transition | ต่อไป, แล้วก็, นอกจากนี้, มาดู, ไปดู, สำหรับ | next, then, also, now, let's, moving on | transition | whoosh-clean |
| closing | ลาก่อน, บาย, เจอกัน, ขอบคุณ, ฝากกด, ติดตาม | bye, see you, thanks, subscribe, follow, end | closing | sparkle |

Priority scoring: surprise/excitement/success/fail = high (2), emphasis/question/transition/closing = medium (1), neutral = low (0).

## Key Differences Between Systems

| Aspect | System A (engine) | System B (script) |
|--------|-------------------|-------------------|
| Event types | 7 (EMPHASIS, REACTION, JOKE, FAIL, SUCCESS, TRANSITION, DRAMATIC) | 8 (surprise, excitement, success, fail, emphasis, question, transition, closing) |
| Output | TimelineEvent → BeatPoint | beat dict with beat_type + sfx_suggestion |
| Timestamp | Character position ratio | Subtitle start time |
| Format awareness | Yes (score modifiers) | No |
| Suggestion | No SFX suggestion | Built-in SFX family suggestion |

## Limitations

- **Keyword-only**: No semantic understanding — "ไม่ผิด" (not wrong) triggers FAIL pattern
- **No context window**: Each cue analyzed independently, misses multi-cue patterns
- **No prosody**: Can't detect emphasis from speech rhythm/pitch
- **No visual cues**: Ignores facial expressions, gestures, on-screen text
- **Thai regex quality**: Some patterns may match unintended substrings
- **Timestamp inaccuracy**: Character ratio ≠ word position

## Note on Subtitle Source

**Primary source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` — SRT file matching the DaVinci Resolve timeline (60fps). Local `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` has WRONG timestamps and must NOT be used.

See also: [[subtitle/analysis-pipeline]], [[event-taxonomy]], [[negative-knowledge]]
