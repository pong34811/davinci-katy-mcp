---
type: concept
confidence: medium
source_count: 1
tags:
  - wiki
  - wiki/concept
---

# SFX Quality Evaluation System

Scoring framework for evaluating SFX placement quality. Used during review and verification.

## Scoring Dimensions (0-10 each)

1. **Density Score** — actual SFX/min vs format target. 10 = within target, 5 = ±1 over/under, 0 = way off.
2. **Spacing Score** — no pairs <1s apart. 10 = all clear, 5 = 1-2 warnings, 0 = many violations.
3. **Family Variety Score** — unique families used. 10 = ≥4 families, 7 = 3, 4 = 2, 1 = all same.
4. **Reason Quality Score** — specific vs generic. 10 = timestamp+word+why, 5 = mentions beat type, 0 = generic/empty.
5. **Beat Coverage Score** — high-impact moments covered. 10 = all key beats have SFX, 5 = some missed, 0 = most missed.
6. **Audio Balance Score** — SFX doesn't drown bed. 10 = all within dB range, 5 = 1-2 off, 0 = audio issues.

## Overall Quality

**Average of all 6 scores.**

| Tier | Score | Meaning |
|---|---|---|
| Professional | 8-10 | Ready to ship |
| Acceptable | 6-7 | Minor improvements possible |
| Needs Revision | 4-5 | Significant issues to fix |
| Start Over | 0-3 | Fundamental problems |

## Post-Placement Verification Checklist

From adding-sfx skill, run after every placement:

1. All SFX on correct track at correct frame (CLI verify readback)
2. No SFX drowning bed/dialogue
3. No 2 SFX overlapping within ~1s
4. No family overuse (except meme)
5. Every SFX has explainable reason
6. Volume consistent across placements
7. Format-appropriate density/volume
8. Overall clip feels more lively and intentional
9. CLI readback matches plan (count, frame, track)

## Evaluation During Review

The sfx-review skill uses these dimensions when auditing existing placements:

- **Critical issues**: overlap, wrong timing (>0.5s), missing high-impact beats
- **High priority**: poor reasons, family repetition, wrong family for beat
- **Medium priority**: slight misalignment (<0.3s), missing medium-impact beats
- **Low priority**: density fine-tuning, reason polish

## See Also

- [[sfx/negative-knowledge]] — what NOT to do
- [[video-editing/audio-mixing]] — volume and mixing rules
