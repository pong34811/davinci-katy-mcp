---
type: concept
confidence: high
source_count: 1
tags:
  - wiki
  - wiki/concept
---

# SFX Library Scanner

The SFX scanning system (`src/sfx_engine/scanner.py`) scans raw and pre-processed SFX directories, extracts metadata, classifies sounds into families/categories, and maintains a cached library index.

## SFXScanner

Entry point. `scan(force_rescan=False)` loads from cache unless forced. Scan order:

1. **Processed dir first** (`SFX_processed/`) — files already normalized, preferred
2. **Raw dir** (`SFX/`) — original source files

Both directories come from `SFXConfig`.

## File Parsing

WAV files use Python's stdlib `wave` module for exact metadata:
- Duration: `frames / sample_rate`
- Sample rate, channels extracted directly

MP3 duration is a rough estimate from filesize:
```
duration = (size_bytes * 8) / (128 * 1000)  # assumes ~128kbps
```

Content hash is `sha256(filename_size_bytes)[:12]` — used for cache invalidation.

## Processed Filename Pattern

Processed files follow: `<shortname>-<dB>.wav` or `<shortname>-<dB>-sting.wav`

Regex: `^(.+?)-(\d+)(?:-(sting))?$`

- `short_name` — the family identifier (e.g. `pop`, `whoosh-clean`)
- `dB` — target loudness as positive integer, stored as negative float (`-14.0`)
- `sting` — optional flag for sting variants

## Taxonomy Classification

`TAXONOMY_RULES` is a list of 25 regex-based rules. Each rule maps a filename pattern to a family, category, and tag list. First match wins; unmatched files get `"other"` / `SFXCategory.ACCENT` / `["sfx"]`.

| Pattern | Family | Category | Tags |
|---------|--------|----------|------|
| `pop` | pop | comedy | pop, short, bubble, punchline |
| `blip` | blip | comedy | blip, silly, marimba, short |
| `plink` | plink | comedy | plink, guitar, slide, funny |
| `honk\|duck` | honk | comedy | honk, horn, duck, silly |
| `awkward` | awkward | reaction | awkward, cricket, moment, pause |
| `huh` | huh | reaction | huh, confused, voice, question |
| `awww` | awww | reaction | awww, cute, reaction, crowd |
| `ding\|bell` | ding | accent | ding, bell, chime, ting, correct |
| `collect` | collect | success | collect, game, pickup, reward |
| `kaching\|cash` | kaching | success | kaching, register, money, cash |
| `sparkle\|harp\|magic\|shimmer` | sparkle | success | sparkle, harp, magic, shimmer |
| `wrong` | wrong | fail | wrong, game, error, fail, incorrect |
| `scratch` | scratch | fail | scratch, record, turntable, stop |
| `bleep\|censor` | bleep | fail | bleep, censor, beep |
| `whoosh.*clean\|whoosh-clean` | whoosh | transition | whoosh, clean, fast, swipe |
| `whoosh.*fast\|whoosh-fast` | whoosh | transition | whoosh, fast, quick |
| `whoosh.*intro\|whoosh-intro\|transition` | whoosh | transition | whoosh, intro, transition |
| `whoosh` | whoosh | transition | whoosh, air, movement |
| `rise\|build` | rise | dramatic | rise, buildup, suspense, tension |
| `gong` | gong | dramatic | gong, metal, comical, dramatic |
| `impact\|hit\|punch\|kung fu\|stomp` | impact | impact | impact, hit, strike, heavy |
| `scream` | scream | impact | scream, shout, vocal, fear |
| `glass\|shatter` | glass | impact | glass, shatter, break |
| `click\|button\|mouse` | click | ui | click, button, mouse, ui |
| `keyboard\|typing` | keyboard | ui | keyboard, typing, keys |
| `digital\|data\|counter` | digital | ui | digital, data, readout, tech |
| `cheer\|crowd\|applause` | crowd | crowd | crowd, cheer, applause, kids |

## Intensity Heuristic

- **"high"** if `target_db >= -12` OR `"hit"` in filename OR `"impact"` in filename
- **"medium"** otherwise

## SFXLibrary

Indexed container wrapping `List[SFXFile]`. Builds three indices on construction:

- `_by_family` — family string → files
- `_by_category` — `SFXCategory` → files
- `_by_filename` — both full filename and shortname → `SFXFile`

Methods: `get_by_filename()`, `get_by_family()`, `get_by_category()`, `get_all_families()`.

## Cache System

JSON cache at `config.get_cache_path() / "sfx_library_cache.json"`. Serialized via `SFXFile.to_dict()` / `SFXFile.from_dict()`. Cache invalidated by `force_rescan=True` — no automatic staleness detection beyond missing file.

## Limitations

- No audio content analysis (RMS, peak, spectral)
- Taxonomy is filename-only — files with misleading names get misclassified
- MP3 duration is approximate (~128kbps assumption)
- Cache has no automatic invalidation on directory changes
