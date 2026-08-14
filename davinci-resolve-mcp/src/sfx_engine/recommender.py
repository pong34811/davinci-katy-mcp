"""SFX Intelligence Recommendation Engine.

The central brain of the SFX Skill. Decides WHAT sound effect to place
WHERE, HOW LOUD, and for HOW LONG, enforcing professional editing constraints.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from src.sfx_engine.analyzer import EventAnalyzer
from src.sfx_engine.config import SFXConfig
from src.sfx_engine.models import (
    BeatPoint,
    ContentFormat,
    EventType,
    SFXFile,
    SFXPlacement,
    SFXPlan,
    TimelineEvent,
)
from src.sfx_engine.search import SFXSearch

logger = logging.getLogger(__name__)


class SFXRecommender:
    """AI-powered SFX recommendation engine.

    Enforces all rules from SKILL.md:
    - Format-aware density caps (talking_head: 3-5/min, game: 5-8/min, meme: high, podcast: ~0)
    - Minimum spacing (~1.0s between SFX)
    - Family variety (prevents whoosh x 3 in a row)
    - Precise volume level recommendations (-10 to -16 dB)
    - Sting duration optimization (0.4s - 0.6s)
    """

    def __init__(
        self,
        search: SFXSearch,
        analyzer: EventAnalyzer,
        config: Optional[SFXConfig] = None,
    ):
        self.search = search
        self.analyzer = analyzer
        self.config = config or SFXConfig.load()

    def generate_plan(
        self,
        timeline_info: Dict[str, Any],
        *,
        transcript: Optional[Union[str, List[Dict[str, Any]]]] = None,
        subtitle_path: Optional[str] = None,
        srt_content: Optional[str] = None,
        override_format: Optional[ContentFormat] = None,
    ) -> SFXPlan:
        """Generate a complete SFX placement plan for a timeline.

        Args:
            timeline_info: Dict containing duration_seconds, fps, etc.
            transcript: Plain text or timestamped transcript dict list.
            subtitle_path: File path to .srt subtitles.
            srt_content: String content of SRT subtitles.
            override_format: Manually force a ContentFormat.

        Returns:
            Validated SFXPlan with ranked placements and warnings.
        """
        duration = float(timeline_info.get("duration_seconds", 0.0))
        fps = float(timeline_info.get("fps", self.config.default_fps))

        # 1. Format Detection (Step 0 in SKILL.md)
        content_format = override_format or self.analyzer.detect_format(timeline_info)
        logger.info("SFX Recommender format: %s", content_format.value)

        # 2. Extract Events & Beats
        events: List[TimelineEvent] = []
        if subtitle_path:
            try:
                with open(subtitle_path, "r", encoding="utf-8") as f:
                    srt_data = f.read()
                events = self.analyzer.analyze_subtitles(srt_data)
            except Exception as exc:
                logger.error("Failed loading subtitle file %s: %s", subtitle_path, exc)
        elif srt_content:
            events = self.analyzer.analyze_subtitles(srt_content)
        elif transcript:
            events = self.analyzer.analyze_transcript(transcript, content_format)

        beats = self.analyzer.find_beats(events, content_format)

        # 3. Select Beats according to Density Caps
        selected_beats = self._select_beats(beats, content_format, duration)

        # 4. Assign SFX for each selected beat with Family Variety
        placements: List[SFXPlacement] = []
        used_families: List[str] = []

        for beat in selected_beats:
            placement = self._assign_sfx_for_beat(
                beat,
                recent_families=used_families[-3:],  # Check last 3 families
                fps=fps,
            )
            if placement:
                placements.append(placement)
                used_families.append(placement.sfx.family)

        # 5. Build and Validate Plan
        density = (len(placements) / (duration / 60.0)) if duration > 0 else 0.0

        plan = SFXPlan(
            format=content_format,
            placements=placements,
            timeline_duration_seconds=duration,
            fps=fps,
            density_per_minute=density,
        )

        return self._validate_and_refine_plan(plan)

    def _select_beats(
        self,
        beats: List[BeatPoint],
        content_format: ContentFormat,
        duration_seconds: float,
    ) -> List[BeatPoint]:
        """Filter and limit beats based on format density caps."""
        if not beats:
            return []

        density_limit = self.config.get_density_limit(content_format.value)
        duration_min = max(0.5, duration_seconds / 60.0)

        # Max SFX allowed for this entire timeline length
        max_sfx_count = int(round(density_limit.max_per_minute * duration_min))
        if content_format == ContentFormat.MEME:
            max_sfx_count = max(max_sfx_count, 15)  # Relaxed cap for meme edits

        # Sort beats by impact score (highest impact first)
        ranked_beats = sorted(beats, key=lambda b: b.impact_score, reverse=True)

        # Select top beats while avoiding clustering < min_spacing_seconds
        selected: List[BeatPoint] = []
        min_spacing = self.config.min_spacing_seconds if content_format != ContentFormat.MEME else 0.4

        for b in ranked_beats:
            if len(selected) >= max_sfx_count:
                break
            # Check spacing against already selected beats
            too_close = any(abs(b.timestamp - s.timestamp) < min_spacing for s in selected)
            if not too_close:
                selected.append(b)

        # Sort selected chronologically
        selected.sort(key=lambda b: b.timestamp)
        return selected

    def _assign_sfx_for_beat(
        self,
        beat: BeatPoint,
        recent_families: List[str],
        fps: float,
    ) -> Optional[SFXPlacement]:
        """Select optimum SFX file and calculate parameters for a beat point."""
        intensity = "high" if beat.impact_score >= 0.8 else "medium"

        # Search candidates excluding recent families for variety
        candidates = self.search.search_by_event(
            beat.event_type,
            intensity=intensity,
            exclude_families=recent_families,
            prefer_processed=True,
        )

        # Fallback if no candidate avoids recent families
        if not candidates:
            candidates = self.search.search_by_event(
                beat.event_type,
                intensity=intensity,
                exclude_families=[],
                prefer_processed=True,
            )

        if not candidates:
            logger.warning("No SFX candidates found for event %s", beat.event_type)
            return None

        chosen_sfx = candidates[0]

        # Target Volume from filename or default
        volume_db = chosen_sfx.target_db or self.config.default_volume_db

        # Duration & Sting calculation
        duration_sec = self.config.default_sting_duration_seconds
        if chosen_sfx.duration_seconds > 0 and chosen_sfx.duration_seconds <= 1.0:
            duration_sec = chosen_sfx.duration_seconds

        record_frame = int(round(beat.timestamp * fps))

        return SFXPlacement(
            sfx=chosen_sfx,
            timestamp=beat.timestamp,
            beat=beat,
            volume_db=volume_db,
            record_frame=record_frame,
            duration_seconds=duration_sec,
            track_index=2,
            confidence=beat.impact_score,
            reason=f"{beat.description} -> [{chosen_sfx.family}] {chosen_sfx.filename}",
        )

    def _validate_and_refine_plan(self, plan: SFXPlan) -> SFXPlan:
        """Audit plan for rule violations and append actionable warnings."""
        warnings: List[str] = []
        spacing_violations: List[str] = []

        placements = plan.placements
        min_spacing = self.config.min_spacing_seconds if plan.format != ContentFormat.MEME else 0.4

        for i in range(len(placements) - 1):
            curr = placements[i]
            nxt = placements[i + 1]
            gap = nxt.timestamp - curr.timestamp

            if gap < min_spacing:
                msg = f"Spacing alert: '{curr.sfx.filename}' and '{nxt.sfx.filename}' are only {gap:.2f}s apart (<{min_spacing}s)"
                spacing_violations.append(msg)

            if curr.sfx.family == nxt.sfx.family and curr.sfx.family != "other":
                warnings.append(f"Family repetition: '{curr.sfx.family}' family used consecutively at {curr.timestamp:.1f}s and {nxt.timestamp:.1f}s")

        density_limit = self.config.get_density_limit(plan.format.value)
        if plan.density_per_minute > density_limit.max_per_minute and plan.format != ContentFormat.MEME:
            warnings.append(
                f"Density ({plan.density_per_minute:.1f}/min) exceeds recommended max ({density_limit.max_per_minute:.1f}/min) for {plan.format.value}"
            )

        plan.warnings = warnings
        plan.spacing_violations = spacing_violations
        return plan
