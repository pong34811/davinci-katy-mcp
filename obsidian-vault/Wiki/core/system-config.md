---
type: concept
confidence: high
source_count: 1
date_ingested: 2026-08-27
tags:
  - wiki
  - wiki/concept
---

# SFX Engine System Configuration

Configuration for the SFX Engine and supporting scripts. Two config files exist with overlapping roles.

## sfx_engine/config.py (MCP Server)

Centralized configuration for the DaVinci Resolve SFX Engine. Supports JSON file and environment variable overrides.

### Default Paths

| Setting | Value | Notes |
|---|---|---|
| `sfx_raw_dir` | `SFX/` (project root) | Computed relative to config.py location |
| `sfx_processed_dir` | `SFX/` (same as raw) | No `SFX_processed/` directory on this machine |

> [!warning] Path mismatch
> Earlier versions defaulted to `Z:/SFX` (wrong). Both paths now resolve to `C:\Users\warit\Desktop\davinci-katy-mcp\SFX\`.

### Timeline Defaults

| Setting | Value |
|---|---|
| `default_fps` | `60.0` |
| `default_sfx_track_name` | `"SFX 1"` |

### Placement Constraints

| Setting | Value | Description |
|---|---|---|
| `min_spacing_seconds` | `1.0` | Minimum gap between SFX placements |
| `default_sting_duration_seconds` | `0.5` | Default sting length |
| `max_sfx_duration_seconds` | `2.0` | Maximum SFX clip length |

### Volume Settings (dB relative to bed)

| Setting | Value |
|---|---|
| `sfx_volume_db_min` | `-16.0` |
| `sfx_volume_db_max` | `-10.0` |
| `default_volume_db` | `-14.0` |

### Fade Settings

| Setting | Value |
|---|---|
| `default_fade_out_seconds` | `0.03` |
| `default_fade_in_seconds` | `0.0` |

### Format-Specific Density Limits

| Format | Min/minute | Max/minute |
|---|---|---|
| `talking_head` | 3 | 5 |
| `podcast` | 0 | 2 |
| `game` | 5 | 8 |
| `meme` | 5 | 15 |
| `livestream` | 0 | 3 |

Unknown formats default to `talking_head` (3–5/min).

### Cache & Media Pool

| Setting | Value |
|---|---|
| `cache_dir` | `None` |
| `cache_ttl_hours` | `24` |
| `sfx_bin_path` | `"Master/SFX"` |

### Environment Variable Overrides

| Env Var | Overrides |
|---|---|
| `SFX_CONFIG_PATH` | JSON config file path |
| `SFX_RAW_DIR` | `sfx_raw_dir` |
| `SFX_PROCESSED_DIR` | `sfx_processed_dir` |
| `SFX_DEFAULT_FPS` | `default_fps` |
| `SFX_CACHE_DIR` | `cache_dir` |

## scripts/config.py (CLI Tools)

Standalone configuration for the `scripts/` CLI tools. Hardcoded paths, no env var overrides.

### Paths

| Setting | Value |
|---|---|
| `SFX_DIR` | `C:\Users\warit\Desktop\davinci-katy-mcp\SFX` |
| `SFX_PROCESSED_DIR` | `PROJECT_ROOT / "SFX_processed"` |
| `MCP_DIR` | `PROJECT_ROOT / "davinci-resolve-mcp"` |
| `OBSIDIAN_VAULT_DIR` | `PROJECT_ROOT / "obsidian-vault"` |

### SFX_FAMILIES (21 families)

Maps family names to actual filenames in the SFX library:

| Family | Files |
|---|---|
| `pop` | Pop - Short 06.mp3 |
| `ding` | Bell - Ding 02.wav, Bell - Ting.mp3 |
| `collect` | Game - Correct Collect Answer.mp3 |
| `sparkle` | Harp - Sparkle 01.mp3, Harp - Sparkle 06.mp3, Magic - Shimmer 01.mp3 |
| `whoosh` | Whoosh - Clean Fast.mp3, Whoosh - Fast 01.mp3, Transition - Whoosh 01.mp3 |
| `impact` | Impact - Comedy Hit 01.mp3, Impact - Comedy Hit 02.mp3 |
| `wrong` | Game - Wrong Answer.mp3 |
| `honk` | Horn - Duck Honk 01.mp3, Horn - Duck Honk 02.mp3 |
| `gong` | Gong - Comical Metal.wav, Gong - Metal.wav |
| `kaching` | Cash Register - Ka Ching 01.mp3, Cash Register - Ka Ching 02.mp3 |
| `blip` | Comedy - Silly Blip 01.mp3, Marimba - Comedy Blip 02.mp3 |
| `plink` | Guitar - Plink Slide 13.wav |
| `scratch` | Scratch - Turntable Record.mp3 |
| `rise` | Rise - Build Up.mp3 |
| `awkward` | Awkward Moment.mp3 |
| `scream` | Scream - Female 01.mp3, Scream - Male 01.wav |
| `glass` | Glass - Wine Glass Shatter.mp3 |
| `explosion` | Explosion - Medium 02.wav |
| `click` | Click - Button Press.wav, Click - Sharp 02.wav |
| `ui` | UI - Enter Confirm.mp3, UI - Loading Bar.mp3 |

### BEAT_TO_SFX Mapping

Maps detected beat types to candidate SFX families:

| Beat | Families |
|---|---|
| `surprise` | pop, impact |
| `excitement` | sparkle, kaching, ding |
| `success` | collect, kaching, ding, sparkle |
| `fail` | wrong, scratch |
| `emphasis` | ding, pop, collect |
| `question` | pop, blip |
| `transition` | whoosh, rise |
| `closing` | sparkle, whoosh |
| `neutral` | _(none)_ |

### FORMAT_CONFIGS

| Format | Density | Max Density | Volume (dB) | Bed |
|---|---|---|---|---|
| `talking-head` | 4/min | 5/min | -12 | speech |
| `game` | 6/min | 8/min | -8 | game_audio |
| `meme` | 10/min | 15/min | -10 | none |
| `podcast` | 1/min | 2/min | -16 | speech_music |
| `livestream` | 2/min | 4/min | -14 | streamer_game |

### EMOTION_KEYWORDS (8 categories)

Bilingual keyword lists for event detection:

| Category | Thai | English |
|---|---|---|
| `surprise` | มาจากไหน, ตกใจ, โอ้โห, ไม่น่าเชื่อ | wow, omg, surprise, really |
| `excitement` | เย้, สุดยอด, เจ๋ง, เทพ | yay, awesome, amazing |
| `success` | สำเร็จ, ได้แล้ว, ชนะ, ผ่าน | success, win, pass, correct |
| `fail` | ล้มเหลว, ผิด, ไม่ได้, พัง | fail, wrong, lose, die |
| `emphasis` | ตัวเลข, สถิติ, จำนวน, เปอร์เซ็นต์ | first, second, most, only |
| `question` | ทำไม, ยังไง, อะไร, ที่ไหน | why, how, what, where |
| `transition` | ต่อไป, แล้วก็, มาดู | next, then, now, let's |
| `closing` | ลาก่อน, บาย, ขอบคุณ | bye, see you, thanks |

### Spacing

| Setting | Value |
|---|---|
| `MIN_SPACING_SECONDS` | `1.0` |
| `DEFAULT_DURATION_SECONDS` | `0.5` |

## Config Differences

| Aspect | sfx_engine/config.py | scripts/config.py |
|---|---|---|
| Path style | Computed relative | Hardcoded absolute |
| Env vars | Yes (5 overrides) | No |
| SFX_PROCESSED_DIR | Same as raw (no SFX_processed/) | `PROJECT_ROOT / "SFX_processed"` |
| Density limits | Dict in `SFXConfig` | Separate `FORMAT_CONFIGS` |
| Volume defaults | -14 dB | Per-format (-8 to -16 dB) |
| Load method | `SFXConfig.load(path)` | Direct import |
| Use case | MCP server, analyzer, search | CLI scripts, sfx_place.py |

> [!note] The `SFX_PROCESSED_DIR` mismatch
> `scripts/config.py` defines `SFX_PROCESSED_DIR` pointing to a non-existent directory. The MCP server config correctly sets both to the same `SFX/` path. On this machine there is no `SFX_processed/` folder — all scripts use raw SFX from `SFX/` directly.
