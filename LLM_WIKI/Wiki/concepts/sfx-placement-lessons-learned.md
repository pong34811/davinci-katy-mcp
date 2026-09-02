---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-09-02
---

# SFX Placement Lessons Learned

Empirical rules from real sessions. These override or refine the default skill behavior.

## Talking-Head Lessons

| Lesson | Detail |
|--------|--------|
| Track index varies | Timeline may have only 1 audio track → CLI creates "SFX 1" at index 2 automatically. Always check track first. |
| Single-pass under-selects | 5 spots/120s = 2.5/min when target is 3–5/min. Fix: mandatory 3-round analysis. |
| Sting vs full file | User may prefer full files (not stings) so they can trim in Resolve. Default to full file duration unless user says otherwise. |
| `AppendToTimeline` ignores `endFrame` | Sometimes places full file instead of trimmed sting. CLI pre-trims with stdlib `wave` as workaround. |
| Frame rate is 60fps | All timestamps in seconds; convert to frames with `round(seconds × 60)` |
| Continuous speech ~90% | Short stings on emphasized words (numbers, shock, open/close) work at −10 to −16 dB without drowning speech. |

## ⚠️ Local SRT Warning

Local SRT files at the project root (e.g., `subtitle_from_track1.srt`) **do not have timestamps matching the DaVinci Resolve timeline**. The authoritative subtitle source is `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`.

## Game Lessons

| Lesson | Detail |
|--------|--------|
| User may want less | Despite density table saying 5–8/min, user may prefer 2–3/min. Ask or analyze only TRUE hinge/punchline moments. |
| Processed ≠ full file | processed (impact-10.wav 0.67s) is shorter than raw (Impact - Comedy Hit 01.mp3 2.41s). If user wants to trim in Resolve, use raw. |
| Track creation | If audio track 2 is occupied, CLI creates SFX track at index 3, not 2. |
| Library paths | SFX files at `C:\Users\warit\Desktop\davinci-katy-mcp\SFX\` (local directory) |

## Meme Lessons

| Lesson | Detail |
|--------|--------|
| Sting at 0.12s works | Memes have no long intro — start SFX immediately. |
| High density OK | 5 stings in 34s = 8.8/min. Sound IS the joke in memes. |
| Repeat families OK | Repeating pop×2 or sparkle×2 is intentional comedy, not a mistake. |

## General Lessons

| Lesson | Detail |
|--------|--------|
| Always dry-run | Catches missing files, spacing issues, timestamp errors before touching Resolve. |
| Verify after place | CLI readback confirms items are actually on the track at the right frames. |
| Delta-only review | Never re-place everything when reviewing. Use sfx-review skill for surgical fixes. |
| Use SRT file, not local | Always read from `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt` |

## Related

- [[impact-scoring-system]] — scoring to guide placement decisions
- [[Wiki/video-editing/plan-generation]] — density and spacing enforcement
- [[End-to-End SFX Workflow]] — complete workflow with failure modes
