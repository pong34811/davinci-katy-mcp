---
type: concept
confidence: high
source_count: 2
date_ingested: 2026-08-27
tags:
  - wiki
  - wiki/concept
---

# Event Taxonomy

Complete event detection system for identifying SFX-worthy moments in video content. Combines keyword matching from `analyzer.py` with taxonomy lookups from `search.py`.

## KEYWORD_PATTERNS (analyzer.py)

7 regex patterns that match Thai and English keywords in subtitle/transcript text. Each pattern has a default impact score.

| EventType | Impact Score | Thai Keywords | English Keywords |
|---|---|---|---|
| `EMPHASIS` | 0.75 | ตัวเลข, จำนวน, สถิติ, เปอร์เซ็นต์, ล้าน, พัน, ร้อย, บาท, กิโล, เท่า, คะแนน, แสน | percent, million, thousand, first, second, `\d+` (numbers) |
| `REACTION` | 0.80 | เย้, ว้าว, โอ้, อ๊ะ, โห, ช็อก, งง, เหรอ, จริงดิ, เห้ย, อ้าว, อุ๊ย, ฮือ, ว๊าก | wow, omg, what, shock, surprise, yeah, hey |
| `JOKE` | 0.85 | 555, ฮ่าๆ, ฮะฮะ, ตลก, มุก, ขำ, ปั่น, กวน, กาว | lol, lmao, haha, funny, joke, meme |
| `FAIL` | 0.85 | ผิด, พลาด, แตก, พัง, ดับ, ตาย, แพ้, แย่, ซวย, มั่ว, กรรม | oops, fail, wrong, died, dead, miss, lose, error, bug |
| `SUCCESS` | 0.85 | สำเร็จ, ชนะ, ได้แล้ว, ถูกต้อง, เยี่ยม, สุดยอด, เก่ง, ปัง, ผ่าน, เรียบร้อย | win, success, correct, done, passed, cleared, perfect, level up |
| `TRANSITION` | 0.70 | ต่อไป, มาดูกัน, ขั้นตอน, ถัดไป, สรุป, เริ่ม, ตอนแรก, จบ | next, then, now, after, finally, let's, step |
| `DRAMATIC` | 0.80 | แต่, แต่ว่า, ทว่า, อย่างไรก็ตาม, ความจริง, ลับ, อันตราย, ระวัง, ระเบิด | but, however, secret, danger, warning, shocking, dramatic |

### Matching Behavior

- Regex is case-insensitive (`re.IGNORECASE`) with Unicode support
- Multiple matches in the same subtitle block produce multiple events
- Timestamp is estimated from word position within the text block
- Each match produces a `TimelineEvent` with the pattern's default impact score

### Limitations

- **Simple regex, not NLP** — matches keywords in isolation, misses context and sarcasm
- **No disambiguation** — "fail" in "I won't fail" still triggers FAIL
- **Score is static** — same keyword always gets same base score regardless of surrounding text
- **Thai word boundary** — Thai doesn't use spaces, so some regex matches may be imprecise

## EVENT_TAXONOMY_MAP (search.py)

Maps each `EventType` to priority `SFXCategory` values (ordered by preference):

| EventType | Priority Categories |
|---|---|
| `JOKE` | COMEDY → ACCENT |
| `REACTION` | REACTION → COMEDY |
| `SURPRISE` | IMPACT → COMEDY |
| `EMPHASIS` | ACCENT → SUCCESS |
| `FAIL` | FAIL → COMEDY |
| `TRANSITION` | TRANSITION → WHOOSH |
| `SUCCESS` | SUCCESS → ACCENT |
| `DRAMATIC` | DRAMATIC → IMPACT |
| `ACTION` | ACTION → IMPACT → WHOOSH |
| `UI_NOTIFICATION` | UI → ACCENT |
| `INTRO` | TRANSITION → SUCCESS |
| `OUTRO` | TRANSITION → ACCENT |

## EVENT_FAMILY_MAP (search.py)

Maps each `EventType` to preferred SFX families (concrete file groups):

| EventType | Preferred Families |
|---|---|
| `JOKE` | pop, blip, plink, honk, awkward |
| `REACTION` | awkward, huh, awww |
| `SURPRISE` | impact, scream, glass, pop |
| `EMPHASIS` | ding, pop, collect |
| `FAIL` | wrong, scratch, bleep |
| `TRANSITION` | whoosh, rise |
| `SUCCESS` | collect, kaching, ding, sparkle, crowd |
| `DRAMATIC` | rise, gong, metal |
| `ACTION` | impact, whoosh |
| `UI_NOTIFICATION` | click, digital, keyboard |
| `INTRO` | whoosh, sparkle, rise |
| `OUTRO` | pop, ding |

## Complete Cross-Reference

| EventType | Thai Keywords | Impact | Preferred Families | Categories |
|---|---|---|---|---|
| JOKE | 555, ฮ่าๆ, ตลก, มุก, ขำ, ปั่น, กวน | 0.85 | pop, blip, plink, honk, awkward | COMEDY, ACCENT |
| REACTION | เย้, ว้าว, โอ้, งง, เหรอ, จริงดิ | 0.80 | awkward, huh, awww | REACTION, COMEDY |
| SURPRISE | _(uses REACTION pattern)_ | 0.80 | impact, scream, glass, pop | IMPACT, COMEDY |
| EMPHASIS | ตัวเลข, จำนวน, สถิติ, ล้าน, บาท | 0.75 | ding, pop, collect | ACCENT, SUCCESS |
| FAIL | ผิด, พลาด, พัง, ตาย, แพ้, มั่ว | 0.85 | wrong, scratch, bleep | FAIL, COMEDY |
| TRANSITION | ต่อไป, มาดูกัน, ถัดไป, จบ | 0.70 | whoosh, rise | TRANSITION, WHOOSH |
| SUCCESS | สำเร็จ, ชนะ, ได้แล้ว, สุดยอด, ปัง | 0.85 | collect, kaching, ding, sparkle, crowd | SUCCESS, ACCENT |
| DRAMATIC | แต่, ทว่า, ความจริง, อันตราย, ระเบิด | 0.80 | rise, gong, metal | DRAMATIC, IMPACT |
| ACTION | _(detected by visual/structural cues)_ | — | impact, whoosh | ACTION, IMPACT, WHOOSH |
| UI_NOTIFICATION | _(detected by visual cues)_ | — | click, digital, keyboard | UI, ACCENT |
| INTRO | _(structural: timeline start)_ | — | whoosh, sparkle, rise | TRANSITION, SUCCESS |
| OUTRO | _(structural: timeline end)_ | — | pop, ding | TRANSITION, ACCENT |

## Format-Specific Score Modifications

After keyword detection, scores are adjusted based on content format before creating `BeatPoint` objects:

| Format | Modification | Rationale |
|---|---|---|
| `PODCAST` | JOKE × 0.4 | Small jokes don't need SFX in long conversations |
| `GAME` | ACTION, SUCCESS, FAIL × 1.3 | Gaming content benefits from action emphasis |
| `MEME` | All events × 1.2 | Short clips benefit from higher SFX density |

Final scores are clamped to `[0.1, 1.0]`.

## Search Flow

```
Subtitle text
  → KEYWORD_PATTERNS regex match
    → TimelineEvent (type, timestamp, base_score)
      → Format adjustment (×0.4 / ×1.2 / ×1.3)
        → BeatPoint (adjusted score)
          → EVENT_FAMILY_MAP → preferred families
            → EVENT_TAXONOMY_MAP → category fallback
              → SFXSearch.search_by_event()
```
