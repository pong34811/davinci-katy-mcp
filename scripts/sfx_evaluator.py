#!/usr/bin/env python3
"""SFX Evaluator — rate SFX recommendations on multiple quality dimensions.

Provides scoring for:
- Context Accuracy
- SFX Relevance
- Timing Accuracy
- Emotional Match
- Intensity Match
- Audio Clarity
- Non-Intrusiveness
- Variety
- Viewer Engagement
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class EvalResult:
    """Result of evaluating an SFX recommendation."""
    # Individual scores (0-10)
    context_accuracy: float = 0.0
    sfx_relevance: float = 0.0
    timing_accuracy: float = 0.0
    emotional_match: float = 0.0
    intensity_match: float = 0.0
    audio_clarity: float = 0.0
    non_intrusiveness: float = 0.0
    variety: float = 0.0
    viewer_engagement: float = 0.0

    # Composite
    overall_score: float = 0.0
    grade: str = ""  # A, B, C, D, F

    # Issues found
    issues: List[str] = field(default_factory=list)

    # Suggestions for improvement
    suggestions: List[str] = field(default_factory=list)


class SFXEvaluator:
    """Evaluates SFX placement recommendations."""

    # Weight map for composite score
    WEIGHTS = {
        "context_accuracy": 0.15,
        "sfx_relevance": 0.15,
        "timing_accuracy": 0.15,
        "emotional_match": 0.15,
        "intensity_match": 0.10,
        "audio_clarity": 0.10,
        "non_intrusiveness": 0.10,
        "variety": 0.05,
        "viewer_engagement": 0.05,
    }

    def evaluate(
        self,
        sfx_placement: Dict[str, Any],
        subtitle_context: Dict[str, Any],
        format_type: str = "talking-head",
    ) -> EvalResult:
        """Evaluate a single SFX placement.

        Args:
            sfx_placement: Dict with sfx_file, timestamp_seconds, duration, reason, etc.
            subtitle_context: Dict with current_subtitle, previous_subtitles, next_subtitles,
                            story_position, impact_score, etc.
            format_type: Content format (talking-head, game, meme, etc.)

        Returns:
            EvalResult with scores and feedback
        """
        result = EvalResult()

        # Evaluate each dimension
        result.context_accuracy = self._eval_context_accuracy(sfx_placement, subtitle_context)
        result.sfx_relevance = self._eval_sfx_relevance(sfx_placement, subtitle_context)
        result.timing_accuracy = self._eval_timing_accuracy(sfx_placement, subtitle_context)
        result.emotional_match = self._eval_emotional_match(sfx_placement, subtitle_context)
        result.intensity_match = self._eval_intensity_match(sfx_placement, subtitle_context, format_type)
        result.audio_clarity = self._eval_audio_clarity(sfx_placement, subtitle_context, format_type)
        result.non_intrusiveness = self._eval_non_intrusiveness(sfx_placement, subtitle_context, format_type)
        result.variety = self._eval_variety(sfx_placement, subtitle_context)
        result.viewer_engagement = self._eval_viewer_engagement(sfx_placement, subtitle_context)

        # Calculate composite
        result.overall_score = self._compute_composite(result)

        # Determine grade
        result.grade = self._grade(result.overall_score)

        # Find issues
        result.issues = self._find_issues(result)

        # Generate suggestions
        result.suggestions = self._generate_suggestions(result, sfx_placement, subtitle_context)

        return result

    def _eval_context_accuracy(self, placement: Dict, context: Dict) -> float:
        """Score: Does the SFX fit the context?"""
        score = 5.0  # Base score

        # Check if reason matches context
        reason = placement.get("reason", "")
        if len(reason) > 20:
            score += 1.0
        if "เพราะ" in reason or "because" in reason.lower():
            score += 0.5

        # Check story position match
        story_pos = context.get("story_position", "")
        if story_pos in ("punchline", "climax") and placement.get("duration", 0.5) <= 0.6:
            score += 1.0
        elif story_pos in ("setup",) and placement.get("duration", 0.5) > 0.6:
            score -= 2.0  # Don't use long SFX in setup

        return max(0, min(10, score))

    def _eval_sfx_relevance(self, placement: Dict, context: Dict) -> float:
        """Score: Is the SFX relevant to the beat type?"""
        score = 5.0

        beat_type = context.get("beat_type", "")
        sfx_file = placement.get("sfx_file", "").lower()

        # Check relevance by keyword matching
        relevance_map = {
            "punchline": ["pop", "blip", "honk", "comedy"],
            "surprise": ["impact", "pop", "scream", "glass"],
            "emphasis": ["ding", "collect", "pop"],
            "transition": ["whoosh", "rise"],
            "fail": ["wrong", "scratch", "bleep"],
            "success": ["collect", "kaching", "ding", "sparkle"],
            "reaction": ["awkward", "huh", "awww"],
        }

        if beat_type in relevance_map:
            relevant_keywords = relevance_map[beat_type]
            if any(kw in sfx_file for kw in relevant_keywords):
                score += 3.0
            else:
                score -= 2.0

        return max(0, min(10, score))

    def _eval_timing_accuracy(self, placement: Dict, context: Dict) -> float:
        """Score: Is the timing accurate?"""
        score = 5.0

        # Check timestamp precision
        timestamp = placement.get("timestamp_seconds", 0)
        if timestamp > 0:
            score += 1.0  # Has valid timestamp

        # Check if timing makes sense for the event
        story_pos = context.get("story_position", "")
        if story_pos == "punchline":
            # Punchline should be on or slightly before the key moment
            subtitle_timing = context.get("subtitle_timing", {})
            if subtitle_timing:
                score += 1.0

        return max(0, min(10, score))

    def _eval_emotional_match(self, placement: Dict, context: Dict) -> float:
        """Score: Does the SFX match the emotional tone?"""
        score = 5.0

        emotions = context.get("detected_emotions", [])
        sfx_file = placement.get("sfx_file", "").lower()

        # Positive emotions should use positive SFX
        positive_emotions = ["excitement", "surprise", "success"]
        negative_emotions = ["sadness", "anger", "fail"]

        if any(e in emotions for e in positive_emotions):
            if any(kw in sfx_file for kw in ["sparkle", "collect", "ding", "pop"]):
                score += 2.0
        if any(e in emotions for e in negative_emotions):
            if any(kw in sfx_file for kw in ["wrong", "scratch", "glass"]):
                score += 2.0

        return max(0, min(10, score))

    def _eval_intensity_match(self, placement: Dict, context: Dict, format_type: str) -> float:
        """Score: Is the intensity appropriate?"""
        score = 5.0

        impact_score = context.get("impact_score", 0.5)
        duration = placement.get("duration", 0.5)

        # High impact should have appropriate duration
        if impact_score > 0.7 and duration <= 0.6:
            score += 2.0
        elif impact_score < 0.3 and duration > 0.6:
            score -= 2.0  # Low impact doesn't need long SFX

        return max(0, min(10, score))

    def _eval_audio_clarity(self, placement: Dict, context: Dict, format_type: str) -> float:
        """Score: Will the SFX be clear without drowning dialogue?"""
        score = 5.0

        # In talking-head, check if SFX would overlap speech
        if format_type == "talking-head":
            # Check if SFX duration is short (sting)
            duration = placement.get("duration", 0.5)
            if duration <= 0.6:
                score += 2.0  # Short stings are clear

        return max(0, min(10, score))

    def _eval_non_intrusiveness(self, placement: Dict, context: Dict, format_type: str) -> float:
        """Score: Is the SFX non-intrusive?"""
        score = 5.0

        # High-impact moments can be more intrusive
        impact_score = context.get("impact_score", 0.5)
        if impact_score > 0.7:
            score += 1.0  # Impact moments justify louder SFX

        # Check format appropriateness
        if format_type in ("podcast", "talking-head"):
            # These formats need more restraint
            duration = placement.get("duration", 0.5)
            if duration > 1.0:
                score -= 2.0

        return max(0, min(10, score))

    def _eval_variety(self, placement: Dict, context: Dict) -> float:
        """Score: Does this add variety or repeat too much?"""
        score = 5.0

        # Check family repetition
        previous_families = context.get("previous_families", [])
        current_family = self._extract_family(placement.get("sfx_file", ""))

        if current_family in previous_families[-3:]:
            score -= 3.0  # Recent repetition

        return max(0, min(10, score))

    def _eval_viewer_engagement(self, placement: Dict, context: Dict) -> float:
        """Score: Will this SFX increase viewer engagement?"""
        score = 5.0

        # Check if this is a high-impact moment
        impact_score = context.get("impact_score", 0.5)
        if impact_score > 0.6:
            score += 2.0

        # Check if this is a turning point
        is_turning_point = context.get("is_turning_point", False)
        if is_turning_point:
            score += 1.5

        return max(0, min(10, score))

    def _compute_composite(self, result: EvalResult) -> float:
        """Compute weighted composite score."""
        total = 0.0
        total += result.context_accuracy * self.WEIGHTS["context_accuracy"]
        total += result.sfx_relevance * self.WEIGHTS["sfx_relevance"]
        total += result.timing_accuracy * self.WEIGHTS["timing_accuracy"]
        total += result.emotional_match * self.WEIGHTS["emotional_match"]
        total += result.intensity_match * self.WEIGHTS["intensity_match"]
        total += result.audio_clarity * self.WEIGHTS["audio_clarity"]
        total += result.non_intrusiveness * self.WEIGHTS["non_intrusiveness"]
        total += result.variety * self.WEIGHTS["variety"]
        total += result.viewer_engagement * self.WEIGHTS["viewer_engagement"]

        return round(total, 1)

    def _grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 8.5:
            return "A"
        elif score >= 7.0:
            return "B"
        elif score >= 5.5:
            return "C"
        elif score >= 4.0:
            return "D"
        else:
            return "F"

    def _find_issues(self, result: EvalResult) -> List[str]:
        """Find specific issues with the evaluation."""
        issues = []

        if result.context_accuracy < 5:
            issues.append("Context accuracy low - SFX may not fit the scene")
        if result.sfx_relevance < 5:
            issues.append("SFX not relevant to beat type")
        if result.timing_accuracy < 5:
            issues.append("Timing may be inaccurate")
        if result.emotional_match < 5:
            issues.append("Emotional tone mismatch")
        if result.variety < 5:
            issues.append("Lack of SFX variety - possible repetition")
        if result.non_intrusiveness < 5:
            issues.append("SFX may be too intrusive for the format")

        return issues

    def _generate_suggestions(self, result: EvalResult, placement: Dict, context: Dict) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []

        if result.context_accuracy < 6:
            suggestions.append("Consider a shorter sting (0.3-0.5s) for better context fit")
        if result.sfx_relevance < 6:
            suggestions.append(f"Try a different family for '{context.get('beat_type', 'unknown')}' beat")
        if result.variety < 6:
            suggestions.append("Rotate to a different SFX family for variety")
        if result.non_intrusiveness < 6:
            suggestions.append("Reduce duration or use processed (normalized) file")

        return suggestions

    def _extract_family(self, filename: str) -> str:
        """Extract SFX family from filename."""
        filename_lower = filename.lower()
        if "pop" in filename_lower:
            return "pop"
        elif "ding" in filename_lower or "bell" in filename_lower:
            return "ding"
        elif "sparkle" in filename_lower or "harp" in filename_lower:
            return "sparkle"
        elif "whoosh" in filename_lower:
            return "whoosh"
        elif "wrong" in filename_lower:
            return "wrong"
        elif "collect" in filename_lower:
            return "collect"
        elif "impact" in filename_lower or "hit" in filename_lower:
            return "impact"
        else:
            return "other"


if __name__ == "__main__":
    evaluator = SFXEvaluator()

    # Test evaluation
    test_placement = {
        "sfx_file": "Pop - Short 06.mp3",
        "timestamp_seconds": 15.5,
        "duration": 0.5,
        "reason": "Surprise reaction to unexpected event",
    }

    test_context = {
        "current_subtitle": "ว้าว! หมูมาจากไหนวะ!",
        "story_position": "punchline",
        "impact_score": 0.85,
        "beat_type": "surprise",
        "detected_emotions": ["surprise", "excitement"],
        "is_turning_point": True,
        "previous_families": ["sparkle", "ding"],
    }

    result = evaluator.evaluate(test_placement, test_context, "talking-head")

    print("=== SFX Evaluation Result ===\n")
    print(f"Overall Score: {result.overall_score}/10 (Grade: {result.grade})\n")
    print("Dimension Scores:")
    print(f"  Context Accuracy:     {result.context_accuracy:.1f}/10")
    print(f"  SFX Relevance:        {result.sfx_relevance:.1f}/10")
    print(f"  Timing Accuracy:      {result.timing_accuracy:.1f}/10")
    print(f"  Emotional Match:      {result.emotional_match:.1f}/10")
    print(f"  Intensity Match:      {result.intensity_match:.1f}/10")
    print(f"  Audio Clarity:        {result.audio_clarity:.1f}/10")
    print(f"  Non-Intrusiveness:    {result.non_intrusiveness:.1f}/10")
    print(f"  Variety:              {result.variety:.1f}/10")
    print(f"  Viewer Engagement:    {result.viewer_engagement:.1f}/10")

    if result.issues:
        print(f"\nIssues:")
        for issue in result.issues:
            print(f"  - {issue}")

    if result.suggestions:
        print(f"\nSuggestions:")
        for sug in result.suggestions:
            print(f"  - {sug}")
