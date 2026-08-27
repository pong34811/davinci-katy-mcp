---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-08-27
---

# Impact Scoring System

Multi-factor scoring system for subtitle segments. Replaces simple keyword matching with weighted scoring across 7 dimensions.

## Dimensions

| Dimension | Weight | Signals |
|-----------|--------|---------|
| Comedy | 15% | laughter patterns, jokes, sarcasm |
| Emotion | 20% | Thai/English emotional words, particles |
| Surprise | 20% | exclamations, disbelief markers |
| Emphasis | 15% | numbers, percentages, rankings |
| Transition | 10% | scene changes, topic shifts |
| Retention | 10% | questions, teasers, curiosity gaps |
| Context | 10% | story arc position, surrounding segments |

## Impact Levels

| Level | Score | SFX Priority |
|-------|-------|-------------|
| CRITICAL | ≥ 0.7 | Always place SFX |
| HIGH | 0.5-0.7 | Strong candidate |
| MEDIUM | 0.3-0.5 | Consider if density allows |
| LOW | 0.15-0.3 | Skip unless empty |
| NONE | < 0.15 | Never place |

## Key Rules

1. **Not every subtitle needs SFX** — only segments with impact ≥ 0.3
2. **Context matters** — a "but" before a surprise doubles the score
3. **Sarcasm = automatic comedy** — always score high for sarcastic segments
4. **Punchlines get bonus** — +0.15 to composite score
5. **Transitions are cheaper** — lower threshold (≥ 0.2) for transition SFX

## Implementation

Located in `scripts/impact_scorer.py` — use `ImpactScorer.score_transcript()` for full analysis.
