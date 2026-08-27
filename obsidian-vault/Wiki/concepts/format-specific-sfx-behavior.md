---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-08-26
---

# Format-Specific SFX Behavior

Each clip format has distinct rules for density, beat sources, audio mixing, and special exceptions. Using wrong format rules is the #1 common mistake.

## Talking-Head / Vlog

- **Density:** 3–5 SFX/min
- **Bed:** speech (dialogue)
- **SFX level:** −10 to −16 dB relative to speech
- **Beat source:** transcript (keywords, numbers, reactions)
- **Special:** short stings on emphasized words work; long sounds over speech do NOT
- **Lessons:** transcript timecodes (frame) are more accurate than text alone for beat timing; always check actual track count (may be 1, not 4)

## Podcast

- **Density:** nearly 0 (1–2 per segment)
- **Bed:** speech + music bed
- **SFX level:** lowest possible
- **Beat source:** wordplay, emphasis, topic changes
- **Special:** skip SFX on small jokes; never interrupt conversation flow

## Game

- **Density:** 5–8 SFX/min (1.5–2× of talking-head)
- **Bed:** game audio
- **SFX level:** can be louder (game audio absorbs)
- **Beat source:** kill/death/respawn, UI popup, power-up, scene change
- **Special:** fast + heavy allowed; 2 SFX close together OK if action pair (kill+collect)
- **Lessons:** user may override density (request 2–3/min); processed files are shorter than raw files

## Meme

- **Density:** high (sound IS the joke)
- **Bed:** no dialogue
- **SFX level:** normal
- **Beat source:** joke timing, visual gags, punchline
- **Special:** **suspend restraint rules** — repeat same family for comedic effect; wrong-timing sounds become jokes themselves

## Livestream

- **Density:** per hour (alert-driven)
- **Bed:** streamer voice + game + music
- **SFX level:** lowest, never cover alerts
- **Beat source:** sub/follow/donation alerts, segment changes, BRB
- **Special:** place by event timing, not seconds; separate "continuous bed" vs "alert sting"

## Cross-Format Rules (Always Apply)

1. Every SFX needs a 1-line reason
2. No 2 SFX overlapping or <1s apart (except game action pairs)
3. Never guess SFX filenames — always scan first
4. Always dry-run before placing
