---
type: concept
confidence: high
source_count: 1
tags: [wiki, wiki/concept]
date_updated: 2026-08-27
---

# SFX Evaluation Framework

System for rating SFX recommendations on 9 quality dimensions.

## Evaluation Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Context Accuracy | 15% | Does SFX fit the scene context? |
| SFX Relevance | 15% | Is SFX relevant to beat type? |
| Timing Accuracy | 15% | Is timing precise? |
| Emotional Match | 15% | Does SFX match emotional tone? |
| Intensity Match | 10% | Is intensity appropriate? |
| Audio Clarity | 10% | Will SFX be clear? |
| Non-Intrusiveness | 10% | Is SFX non-distracting? |
| Variety | 5% | Does this add variety? |
| Viewer Engagement | 5% | Will this engage viewers? |

## Grading Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 8.5-10 | A | Excellent - place as-is |
| 7.0-8.4 | B | Good - minor tweaks needed |
| 5.5-6.9 | C | Acceptable - consider alternatives |
| 4.0-5.4 | D | Poor - should replace |
| 0-3.9 | F | Bad - remove or rethink |

## Implementation

Located in `scripts/sfx_evaluator.py` — use `SFXEvaluator.evaluate()` to rate placements.
