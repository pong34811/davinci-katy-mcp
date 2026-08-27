---
type: concept
confidence: high
source_count: 2
tags: [wiki, wiki/concept]
date_updated: 2026-08-27
---

# Subtitle Analysis Pipeline

How raw subtitle text flows through emotion detection → beat classification → SFX suggestion. Two implementations exist: the MCP engine path and the standalone scripts path.

## Input Sources

| Source | Method | Format |
|--------|--------|--------|
| DaVinci Resolve timeline | `timeline.get_transcript(with_timecodes=True)` | Text with frame timecodes |
| SRT file | `read_subtitles_from_srt(path)` | Standard SubRip format |
| Resolve subtitle track | `read_subtitles_from_resolve()` | Frame-based entries |
| Manual transcript | Plain text or JSON list | String or dict list |

## Pipeline (scripts/analyze_subtitles.py)

```
Raw Subtitle Entry
  → detect_emotion(text) → List[str] emotions
  → detect_numbers(text) → List[str] numbers
  → classify_beat(emotions, numbers) → beat_type + sfx_suggestion + priority
  → Output: beat dict
```

### Step 1: Emotion Detection

`detect_emotion(text)` — iterates EMOTION_KEYWORDS dict, checks if any keyword appears in lowercase text. Returns list of matching emotions, or `["neutral"]` if none match.

### Step 2: Number Detection

`detect_numbers(text)` — regex `[\d,]+\.?\d*` extracts numeric strings (removes commas). Used for emphasis detection.

### Step 3: Beat Classification

Priority order (first match wins):

| Priority | Condition | Beat Type | SFX Suggestion |
|----------|-----------|-----------|----------------|
| 2 (high) | "surprise" in emotions | surprise | pop |
| 2 (high) | "excitement" in emotions | excitement | sparkle |
| 2 (high) | "success" in emotions | success | collect |
| 2 (high) | "fail" in emotions | fail | wrong |
| 1 (medium) | "emphasis" in emotions OR numbers found | emphasis | ding |
| 1 (medium) | "question" in emotions | question | pop |
| 1 (medium) | "transition" in emotions | transition | whoosh-clean |
| 1 (medium) | "closing" in emotions | closing | sparkle |
| 0 (low) | none of above | neutral | None |

### Output Format

```json
{
  "index": 1,
  "start_frame": 1428,
  "end_frame": 1548,
  "start_seconds": 23.8,
  "end_seconds": 25.8,
  "duration_seconds": 2.0,
  "text": "ตัวเลขสูงถึง 1,649",
  "emotions": ["emphasis"],
  "beat_type": "emphasis",
  "sfx_suggestion": "ding",
  "priority": 1,
  "numbers": ["1649"]
}
```

## Pipeline (MCP Engine)

```
SRT Content or Transcript
  → EventAnalyzer.analyze_subtitles(srt_content) → List[TimelineEvent]
  → EventAnalyzer.find_beats(events, content_format) → List[BeatPoint]
  → SFXRecommender.generate_plan(timeline_info, ...) → SFXPlan
```

### Step 1: SRT Parsing

`analyze_subtitles(srt_content)` — splits on blank lines, parses timestamp line with regex `(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})`, extracts text.

### Step 2: Event Detection

`_detect_events_in_text(text, start_time, end_time)` — for each KEYWORD_PATTERN, finds all regex matches, estimates timestamp by character position ratio, creates TimelineEvent with type, timestamp, description, impact_score.

### Step 3: Beat Filtering

`find_beats(events, content_format)` — applies format-specific score modifiers (podcast suppresses jokes, game boosts actions, meme boosts all), clamps score to [0.1, 1.0], creates BeatPoint objects.

### Step 4: Plan Generation (Recommender)

`_select_beats(beats, content_format, duration)` — sorts by impact_score descending, selects top N within density cap, enforces min_spacing (1.0s, or 0.4s for meme). `_assign_sfx_for_beat()` — searches by event type, excludes recent families for variety.

## Key Differences

| Aspect | Scripts Path | Engine Path |
|--------|-------------|-------------|
| Entry point | `analyze_subtitles.py` | `SFXRecommender.generate_plan()` |
| Beat classification | 8 emotions → beat_type | 7 event types → BeatPoint |
| SFX selection | Static BEAT_TO_SFX mapping | Dynamic SFXSearch with family variety |
| Format awareness | Not built-in (manual) | Built-in density caps and score modifiers |
| Output | beat dict (for generate_sfx_plan.py) | SFXPlan (ready to execute) |
| Spacing check | In generate_sfx_plan.py | In recommender._validate_and_refine_plan() |

## Integration Flow

```
User: "เพิ่ม SFX ให้คลิปนี้"
  → Agent reads transcript via MCP
  → Agent runs 3-round analysis (adding-sfx skill)
  → Agent writes plan.json
  → CLI: python scripts/sfx_place.py --plan plan.json --verify
```

See also: [[beat-detection]], [[plan-generation]], [[event-taxonomy]]
