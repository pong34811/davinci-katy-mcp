---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-08-27
---

# Timing Intelligence

Precise SFX timing decisions based on content type and context.

## Timing Types

| Type | Offset | Use Case |
|------|--------|----------|
| **Pre-hit** | -0.1s to -0.2s | Anticipation before punchline, build-up moments |
| **On-hit** | 0.0s | Exact moment of impact, emphasis, surprise |
| **Post-hit** | +0.1s to +0.3s | Reactions, aftermath, relief |

## Timing Presets

| Event Type | Timing | Duration | Fade In | Fade Out |
|------------|--------|----------|---------|----------|
| Punchline | Pre-hit | 0.4s | 0.02s | 0.05s |
| Surprise | On-hit | 0.3s | 0.0s | 0.03s |
| Reaction | Post-hit | 0.5s | 0.03s | 0.05s |
| Emphasis | On-hit | 0.3s | 0.0s | 0.04s |
| Transition | Pre-hit | 0.8s | 0.1s | 0.15s |
| Fail | On-hit | 0.5s | 0.0s | 0.08s |
| Success | On-hit | 0.6s | 0.05s | 0.1s |

## Spacing Rules

- Minimum gap from previous SFX: **0.5s**
- Minimum gap to next SFX: **0.5s**
- If overlap detected, shift to next available gap

## Implementation

Located in `scripts/timing_intelligence.py` — use `TimingIntelligence.decide_timing()` for precise timing.
