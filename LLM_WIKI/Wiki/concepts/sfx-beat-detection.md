---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-09-02
---

# SFX Beat Detection

Process of identifying moments in video content where Sound Effects would enhance engagement.

## Beat Types

| Beat | Description | SFX Families |
|------|-------------|--------------|
| punchline | joke or humorous moment | pop, blip, plink |
| reaction | emotional response (shock, awe) | awkward, awww, impact |
| emphasis | important word or number | ding, pop, collect |
| transition | scene change | whoosh, rise |
| dramatic | tension or gravity | gong, rise |
| fail | mistake or loss | wrong, scratch |
| success | achievement | collect, kaching, sparkle |
| emotional | sadness or touching moment | awww, sparkle |

## Density Rules

- Talking-head: 3–5 SFX/min (user preference: 4/min)
- Game: 5–8 SFX/min
- Podcast: 1–2 per segment
- Meme: high density (sound IS the joke)

## Beat Detection Systems

Two independent regex-based systems:

### System A: Engine (analyzer.py)
- 7 event types: EMPHASIS, REACTION, JOKE, FAIL, SUCCESS, TRANSITION, DRAMATIC
- Impact scores: 0.70–0.85
- Format-specific score modifiers
- Timestamp estimation via character position ratio

### System B: Script (analyze_subtitles.py)
- 8 emotions: surprise, excitement, success, fail, emphasis, question, transition, closing
- Priority levels: 0–2
- Built-in SFX family suggestion per beat type

## Subtitle Source

**Primary source:** `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` — SRT file with timestamps matching the DaVinci Resolve timeline (60fps).

**⚠️ Local SRT files** at the project root (e.g., `subtitle_from_track1.srt`) have WRONG timestamps — they must NOT be used.

## Sources

- [[davinci-resolve-sfx-system-readme]]
- [[subtitle-analysis]]
- [[Wiki/subtitle/beat-detection]]
