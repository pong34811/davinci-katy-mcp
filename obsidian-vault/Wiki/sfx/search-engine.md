---
type: concept
confidence: high
source_count: 1
tags:
  - wiki
  - wiki/concept
---

# SFX Search Engine

The search system (`src/sfx_engine/search.py`) provides fuzzy matching, category search, event-based lookup, family filtering, and diversity recommendations across the [[library-scanner|SFX Library]].

## SFXSearch

Wraps an `SFXLibrary` instance. All methods are read-only queries — no mutations.

## search() — Free Text

`search(query, limit=5, prefer_processed=True)` → `List[SFXSearchResult]`

Scoring breakdown per file (capped at 1.0):

| Signal | Score | Condition |
|--------|-------|-----------|
| Exact family match | +0.9 | `query == file.family` |
| Substring in filename | +0.7 | `query in filename` |
| Fuzzy ratio | +ratio × 0.4 | `SequenceMatcher` between query and filename |
| Tag match | +0.5 | `query` appears in any tag |
| Processed boost | +0.15 | `file.is_processed` and `prefer_processed` |

Threshold: files scoring ≤ 0.2 are excluded. Results sorted descending by score.

## search_by_event() — Event-Driven

`search_by_event(event_type, intensity="medium", exclude_families=None, prefer_processed=True)` → `List[SFXFile]`

Two-phase search:

1. **Preferred families** (score 0.8) — looks up `EVENT_FAMILY_MAP[event_type]`, queries each family directly. Bonus: +0.15 for processed, +0.1 for matching intensity.
2. **Category fallback** (score 0.5) — if fewer than 3 candidates, queries `EVENT_TAXONOMY_MAP[event_type]` categories. Deduplicates against phase 1.

## search_by_category()

`search_by_category(category, prefer_processed=True)` → `List[SFXFile]`

Returns all files in a category. If `prefer_processed=True` and processed files exist, returns only those.

## find_similar()

`find_similar(sfx, exclude_same_family=True)` → `List[SFXFile]`

Finds files in the same category, excluding the source file and (optionally) same-family files. Useful for fallback/alternative suggestions.

## Event Taxonomy Map

Maps `EventType` → priority `SFXCategory` list:

| EventType | Categories |
|-----------|------------|
| JOKE | comedy, accent |
| REACTION | reaction, comedy |
| SURPRISE | impact, comedy |
| EMPHASIS | accent, success |
| FAIL | fail, comedy |
| TRANSITION | transition, whoosh |
| SUCCESS | success, accent |
| DRAMATIC | dramatic, impact |
| ACTION | action, impact, whoosh |
| UI_NOTIFICATION | ui, accent |
| INTRO | transition, success |
| OUTRO | transition, accent |

## Event Family Map

Maps `EventType` → preferred family names:

| EventType | Families |
|-----------|----------|
| JOKE | pop, blip, plink, honk, awkward |
| REACTION | awkward, huh, awww |
| SURPRISE | impact, scream, glass, pop |
| EMPHASIS | ding, pop, collect |
| FAIL | wrong, scratch, bleep |
| TRANSITION | whoosh, rise |
| SUCCESS | collect, kaching, ding, sparkle, crowd |
| DRAMATIC | rise, gong, metal |
| ACTION | impact, whoosh |
| UI_NOTIFICATION | click, digital, keyboard |
| INTRO | whoosh, sparkle, rise |
| OUTRO | pop, ding |

## Limitations

- No audio feature similarity (no spectral, RMS, or embedding comparison)
- No embedding-based semantic search
- Scoring is heuristic, not learned from user feedback
- Fuzzy matching is character-level (`SequenceMatcher`), not phonetic
