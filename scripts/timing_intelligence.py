#!/usr/bin/env python3
"""Timing Intelligence — precise SFX timing decisions.

Determines the exact timing for SFX placement:
- Pre-hit (anticipation before punchline)
- On-hit (exact moment of impact)
- Post-hit (reaction after the event)

Also handles fade-in/fade-out calculations and overlap prevention.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TimingDecision:
    """Timing decision for an SFX placement."""
    sfx_start_offset: float  # seconds relative to subtitle start (negative = before)
    sfx_end_offset: float    # seconds relative to subtitle end (positive = after)
    timing_type: str         # "pre-hit", "on-hit", "post-hit"
    duration: float          # suggested duration in seconds
    fade_in: float           # fade in duration in seconds
    fade_out: float          # fade out duration in seconds


class TimingIntelligence:
    """Intelligent SFX timing decisions based on content type."""

    # Timing presets by event type
    TIMING_PRESETS = {
        "punchline": TimingDecision(
            sfx_start_offset=-0.1,  # slightly before
            sfx_end_offset=0.0,
            timing_type="pre-hit",
            duration=0.4,
            fade_in=0.02,
            fade_out=0.05,
        ),
        "surprise": TimingDecision(
            sfx_start_offset=0.0,   # exact moment
            sfx_end_offset=0.1,
            timing_type="on-hit",
            duration=0.3,
            fade_in=0.0,
            fade_out=0.03,
        ),
        "reaction": TimingDecision(
            sfx_start_offset=0.2,   # after the word
            sfx_end_offset=0.0,
            timing_type="post-hit",
            duration=0.5,
            fade_in=0.03,
            fade_out=0.05,
        ),
        "emphasis": TimingDecision(
            sfx_start_offset=-0.05,
            sfx_end_offset=0.0,
            timing_type="on-hit",
            duration=0.3,
            fade_in=0.0,
            fade_out=0.04,
        ),
        "transition": TimingDecision(
            sfx_start_offset=-0.2,
            sfx_end_offset=0.3,
            timing_type="pre-hit",
            duration=0.8,
            fade_in=0.1,
            fade_out=0.15,
        ),
        "fail": TimingDecision(
            sfx_start_offset=0.0,
            sfx_end_offset=0.1,
            timing_type="on-hit",
            duration=0.5,
            fade_in=0.0,
            fade_out=0.08,
        ),
        "success": TimingDecision(
            sfx_start_offset=-0.05,
            sfx_end_offset=0.05,
            timing_type="on-hit",
            duration=0.6,
            fade_in=0.05,
            fade_out=0.1,
        ),
    }

    def decide_timing(
        self,
        event_type: str,
        subtitle_start: float,
        subtitle_end: float,
        previous_sfx_end: Optional[float] = None,
        next_sfx_start: Optional[float] = None,
    ) -> TimingDecision:
        """Decide timing for an SFX placement.

        Args:
            event_type: Type of event (punchline, surprise, etc.)
            subtitle_start: Start time of the subtitle in seconds
            subtitle_end: End time of the subtitle in seconds
            previous_sfx_end: End time of previous SFX (for spacing)
            next_sfx_start: Start time of next SFX (for spacing)

        Returns:
            TimingDecision with precise timing parameters
        """
        # Get base timing from preset
        preset = self.TIMING_PRESETS.get(event_type, self.TIMING_PRESETS["on-hit"])

        # Adjust for context
        timing = TimingDecision(
            sfx_start_offset=preset.sfx_start_offset,
            sfx_end_offset=preset.sfx_end_offset,
            timing_type=preset.timing_type,
            duration=preset.duration,
            fade_in=preset.fade_in,
            fade_out=preset.fade_out,
        )

        # Check spacing constraints
        if previous_sfx_end is not None:
            min_gap = 0.5  # minimum gap from previous SFX
            adjusted_start = previous_sfx_end + min_gap
            if adjusted_start > subtitle_start + timing.sfx_start_offset:
                timing.sfx_start_offset = adjusted_start - subtitle_start

        if next_sfx_start is not None:
            min_gap = 0.5
            adjusted_end = next_sfx_start - min_gap
            if adjusted_end < subtitle_end + timing.sfx_end_offset:
                timing.sfx_end_offset = adjusted_end - subtitle_end

        # Ensure duration doesn't exceed subtitle
        max_duration = (subtitle_end + timing.sfx_end_offset) - (subtitle_start + timing.sfx_start_offset)
        if max_duration < 0.2:
            timing.duration = max(0.2, max_duration)
        else:
            timing.duration = min(timing.duration, max_duration)

        return timing

    def check_overlap(
        self,
        current_start: float,
        current_end: float,
        existing_sfx: List[dict],
    ) -> bool:
        """Check if new SFX overlaps with existing ones."""
        for sfx in existing_sfx:
            sfx_start = sfx.get("start_seconds", 0)
            sfx_end = sfx.get("start_seconds", 0) + sfx.get("duration_seconds", 0.5)

            # Check overlap with margin
            margin = 0.3
            if not (current_end + margin < sfx_start or current_start - margin > sfx_end):
                return True  # Overlap detected
        return False

    def get_optimal_start(
        self,
        target_time: float,
        existing_sfx: List[dict],
        min_gap: float = 0.5,
    ) -> float:
        """Find optimal start time avoiding overlaps."""
        start = target_time
        max_attempts = 10

        for _ in range(max_attempts):
            if not self.check_overlap(start, start + 0.5, existing_sfx):
                return start
            start += min_gap

        return target_time  # Return original if no gap found


if __name__ == "__main__":
    ti = TimingIntelligence()

    # Example: punchline at 15.0s
    timing = ti.decide_timing(
        event_type="punchline",
        subtitle_start=14.5,
        subtitle_end=16.0,
    )
    print(f"Punchline timing:")
    print(f"  Start offset: {timing.sfx_start_offset:+.2f}s")
    print(f"  Timing type: {timing.timing_type}")
    print(f"  Duration: {timing.duration}s")
    print(f"  Fade in: {timing.fade_in}s, Fade out: {timing.fade_out}s")
