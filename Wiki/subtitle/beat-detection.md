---
type: concept
confidence: high
source_count: 2
tags:
  - wiki
  - wiki/concept
---

# Beat Detection System

The SFX engine identifies "beats" — moments worth placing a sound effect — using two independent keyword-regex systems.

## System A: Engine Analyzer (`analyzer.py`)

`EventAnalyzer` lives in the MCP server under `src/sfx_engine/analyzer.py`. It operates on `KEYWORD_PATTERNS`, a list of 7 `(EventType, impact_score, regex)` tuples:

| EventType | Impact | Example Keywords |
|-----------|--------|-----------------|
| `EMPHASIS` | 0.75 | ตัวเลข, สถิติ, percent, million, vtuber |
| `REACTION` | 0.80 | เย้, ว้าว, wow, omg, shock, surprise |
| `JOKE` | 0.85 | 555, ฮ่าๆ, lol, lmao, funny, meme |
| `FAIL` | 0.85 | ผิด, พลาด, fail, wrong, died, error |
| `SUCCESS` | 0.85 | สำเร็จ, ชนะ, win, success, perfect |
| `TRANSITION` | 0.70 | ต่อไป, next, then, finally, step |
| `DRAMATIC` | 0.80 | แต่, however, secret, danger, dramatic |

All patterns use `re.UNICODE` and `(?i)` for case-insensitive Thai+English matching.

### Text → Beat Flow

1. `analyze_subtitles()` parses SRT content into blocks (start/end/text).
2. `_detect_events_in_text()` runs each pattern's `finditer()` against the subtitle text.
3. Each match becomes a `TimelineEvent` with timestamp estimated via:

```
pos_ratio = match.start() / len(text)
timestamp = start + (end - start) * pos_ratio
```

4. `find_beats()` converts `TimelineEvent` → `BeatPoint`, applying format-specific score adjustments:
   - **Podcast**: `JOKE` × 0.4 (suppress)
   - **Game**: `ACTION`/`SUCCESS`/`FAIL` × 1.3 (boost)
   - **Meme**: all × 1.2 (boost)

## System B: Script Analyzer (`analyze_subtitles.py`)

A standalone script under `scripts/analyze_subtitles.py` with its own `EMOTION_KEYWORDS` dict — 8 emotions, each with Thai+English keyword lists:

| Emotion | Beat Type | SFX Suggestion | Priority |
|---------|-----------|----------------|----------|
| `surprise` | surprise | pop | high (2) |
| `excitement` | excitement | sparkle | high (2) |
| `success` | success | collect | high (2) |
| `fail` | fail | wrong | high (2) |
| `emphasis` | emphasis | ding | medium (1) |
| `question` | question | pop | medium (1) |
| `transition` | transition | whoosh-clean | medium (1) |
| `closing` | closing | sparkle | medium (1) |

`detect_emotion()` does substring matching (`kw.lower() in text_lower`). No regex, no positional estimation — simpler but coarser than System A.

### Text → Beat Flow

1. `read_subtitles_from_resolve()` or `read_subtitles_from_srt()` produces subtitle dicts with `start_seconds`/`end_seconds`/`text`.
2. `analyze_subtitles()` calls `detect_emotion()` on each subtitle's text.
3. First matching emotion wins (priority order: surprise → excitement → success → fail → emphasis → question → transition → closing).
4. Numbers detected via `detect_numbers()` add emphasis beats independently.

## Timestamp Estimation (System A Only)

Both systems assume a keyword's timestamp is proportional to its character position within the subtitle block:

```
pos_ratio = match.start() / len(text)
timestamp = start + (end - start) × pos_ratio
```

This is an approximation — it places the SFX at the word's relative position in the spoken line, not at an actual speech-detected moment.

## Limitations

- **Keyword-only**: no semantic understanding, no context window, no prosody analysis
- **No deduplication**: the same word in two subtitles produces two beats
- **No prosody integration**: no pitch/energy/silence detection
- **Positional approximation**: timestamp based on character offset, not actual speech timing
- **Two independent systems**: System A and System B don't share results — running both produces duplicate beats

## Related Pages

- [[analysis-pipeline]] — how beats flow into SFX suggestions
- [[plan-generation]] — how beats become a placement plan
- [[placement-engine]] — how plans execute on the timeline
