---
type: concept
confidence: high
source_count: 1
tags:
  - wiki
  - wiki/concept
---

# SFX Family Mapping

Complete reference for the SFX family system defined in `scripts/config.py`. Each family groups one or more actual audio files by intended use case.

> **Important:** The user's SFX files use human-readable names (e.g. `"Pop - Short 06.mp3"`), NOT slug names. Always map families to actual filenames from `SFX_FAMILIES` when generating plans. No `SFX_processed/` directory exists — all files live in `SFX/` raw.

## SFX_FAMILIES

| Family | Files | Category | When to Use |
|--------|-------|----------|-------------|
| pop | `Pop - Short 06.mp3` | comedy | Punchline, joke payoff, quick funny moment |
| ding | `Bell - Ding 02.wav`, `Bell - Ting.mp3` | accent | Emphasis, correct answer, "aha" moment |
| collect | `Game - Correct Collect Answer.mp3` | success | Success, achievement, game reward pickup |
| sparkle | `Harp - Sparkle 01.mp3`, `Harp - Sparkle 06.mp3`, `Magic - Shimmer 01.mp3` | success | Magic, reveal, "wow" moment, something special |
| whoosh | `Whoosh - Clean Fast.mp3`, `Whoosh - Fast 01.mp3`, `Transition - Whoosh 01.mp3` | transition | Scene transitions, swipes, fast movement |
| impact | `Impact - Comedy Hit 01.mp3`, `Impact - Comedy Hit 02.mp3` | impact | Heavy hit, dramatic punch, physical comedy |
| wrong | `Game - Wrong Answer.mp3` | fail | Fail, wrong answer, error moment |
| honk | `Horn - Duck Honk 01.mp3`, `Horn - Duck Honk 02.mp3` | comedy | Silly, absurd, duck quack humor |
| gong | `Gong - Comical Metal.wav`, `Gong - Metal.wav` | dramatic | Dramatic reveal, heavy emphasis, comical metal hit |
| kaching | `Cash Register - Ka Ching 01.mp3`, `Cash Register - Ka Ching 02.mp3` | success | Money, success, cash register sound |
| blip | `Comedy - Silly Blip 01.mp3`, `Marimba - Comedy Blip 02.mp3` | comedy | Silly, quirky, short electronic blip |
| plink | `Guitar - Plink Slide 13.wav` | comedy | Funny slide, guitar plink, comedic accent |
| scratch | `Scratch - Turntable Record.mp3` | fail | Record scratch, sudden stop, "wait what" |
| rise | `Rise - Build Up.mp3` | dramatic | Buildup, suspense, rising tension |
| awkward | `Awkward Moment.mp3` | reaction | Crickets, awkward pause, uncomfortable silence |
| scream | `Scream - Female 01.mp3`, `Scream - Male 01.wav` | impact | Fear, shock, dramatic vocal |
| glass | `Glass - Wine Glass Shatter.mp3` | impact | Shatter, breakage, fragile destruction |
| explosion | `Explosion - Medium 02.wav` | impact | Heavy explosion, dramatic destruction |
| click | `Click - Button Press.wav`, `Click - Sharp 02.wav` | ui | UI button press, mouse click, interface tap |
| ui | `UI - Enter Confirm.mp3`, `UI - Loading Bar.mp3` | ui | Digital interface, data readout, tech sound |

## BEAT_TO_SFX Mapping

Maps subtitle/transcript beat types to recommended family lists:

| Beat Type | Families |
|-----------|----------|
| surprise | pop, impact |
| excitement | sparkle, kaching, ding |
| success | collect, kaching, ding, sparkle |
| fail | wrong, scratch |
| emphasis | ding, pop, collect |
| question | pop, blip |
| transition | whoosh, rise |
| closing | sparkle, whoosh |
| neutral | *(empty — no SFX recommended)* |

## Notes

- `get_sfx_file(family)` returns the first existing file from the family's list, or `""` if none found
- `get_sfx_path(filename)` returns full absolute path: `SFX_DIR / filename`
- `validate_config()` checks all mapped files exist in `SFX/` and reports missing ones
- Family names are used as keys in the [[library-scanner|SFXLibrary]] index and [[search-engine|SFXSearch]] queries
