---
type: concept
confidence: high
source_count: 3
tags:
  - wiki
  - wiki/concept
---

# SFX Negative Knowledge — What NOT to Do

Hard-won lessons from placing SFX across talking-head, game, meme, podcast, and livestream formats. Every rule here was learned the hard way.

## Never

- **Place SFX without scanning library first** — filename guessing = plan failure. Always `sfx` scan before starting.
- **Use single-pass analysis** — consistently under-selects: 2.5/min vs target 4/min for talking-head. Use the 3-round workflow (structural scan → beat harvesting → curation).
- **Place long sounds (>1s) over continuous speech** — talking-head/podcast format. Short stings (~0.5s) on emphasis words are OK; long rise/shimmer over a sentence is not.
- **Use same family 3× in a row** — whoosh×3, pop×3 feels repetitive. Exception: meme format where repetition is the joke.
- **Place 2 SFX <1s apart** — except game action pairs (kill+collect). One loud sound per beat.
- **Use talking-head density (3-5/min) for game/meme/podcast formats** — each format has its own density cap from the Format Table.
- **Skip dry-run before placing** — `--dry-run` catches missing files, spacing issues, and overlaps before touching Resolve.
- **Use processed files when user wants full-length files** — processed files are short stings (0.5s); user may want raw files for Resolve trimming. Check preference.
- **Assume track index is always 2** — may be 1, 3, or variable depending on existing tracks. CLI creates and names the SFX track automatically.
- **Assume Z:/SFX path exists** — use local `SFX/` directory. The path varies per machine.
- **Use SFX on every sentence** — density cap exists for a reason. Over-SFX kills natural feel.
- **Re-place entire track when reviewing** — delta-only via sfx-review skill. Never wipe and redo from scratch.
- **Use generic reasons** ("เน้นจุดสำคัญ") — must be specific per beat: timestamp + word + why.
- **Place SFX during dialogue in podcast format** — podcast density is nearly 0; only wordplay, emphasis, or topic transitions get SFX.
- **Use impact/scream/glass for small jokes** — wrong scale. Small joke → pop/plink; big moment → impact/rise.
- **Trust AppendToTimeline endFrame parameter** — broken on WAV files. Pre-trim WAV to sting duration instead (CLI handles this automatically).
- **Use local SRT files** — local `subtitle_from_track1.srt` has wrong timestamps. Always use `C:\Users\warit\AppData\Local\hermes\attachments\Subtitle 1.srt`.

## Common Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Single-pass analysis | 2.5/min density (should be 3-5/min for talking-head) | Use 3-round workflow |
| Wrong format rules | Meme gets podcast density (nearly 0 SFX) | Detect format in Step 0 |
| Filename guessing | "file not found in SFX dir" error | Scan library first |
| Skipping verify | Placed at wrong frames, overlaps undetected | Always run `--verify` |
| Wrong subtitle source | Using local SRT with wrong timestamps | Always use `Subtitle 1.srt` |

## See Also

- [[sfx/evaluation-system]] — quality scoring framework
- [[video-editing/audio-mixing]] — volume and mixing rules
